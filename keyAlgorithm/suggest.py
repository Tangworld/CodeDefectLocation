#!/usr/local/python
# -*- coding: utf-8 -*-
# encoding=utf-8
import random
from sys import argv
import time
from collections import Counter
import math

'''
def load_multi_data():
    f_data = open('TITLE30K-Wu.txt', 'r')

    tr_data = []
    for l in f_data:
        rec = {'ts': eval(l)[0], 'ws': eval(l)[1]}
        tr_data.append(rec)
    f_data.close()

    g_data = open('Math-Wu.txt', 'r')

    te_data = []
    for l in g_data:
        rec = {'ts': eval(l)[0], 'ws': eval(l)[1]}
        te_data.append(rec)
    g_data.close()

    return tr_data, te_data
'''
outf = None
sourceCom = {}
pro = ""

def load_data():
    """
    数据预处理，从txt文件中读取数据填充到集合类型中
    :return:
        data:集合，存放aspectjReportsNLTK.txt全部内容
        k_vocab_data：全部单词ID的集合
        link_BR_S：空集合
        sourceLen：aspectjSourceLen.txt文件的内容
    """
    global outf
    pro = 'aspectj'
    outf = open(pro.upper()+'output.txt','w')
    f_data = open(pro+'ReportsNLTK.txt', 'r')

    data = []
    for l in f_data:
        rec = {'ts': eval(l)[0], 'ws': eval(l)[1], 'ss':eval(l)[-1]}
        data.append(rec)
        global sourceCom
        for source in rec['ts']:
            if source not in sourceCom:
                sourceCom[source] = set()
            sourceCom[source].add(rec['ss'])
    f_data.close()

    k_vocab_data = []
    k_vocab = open(pro+'SourcesNLTK.txt','r')
    for l in k_vocab:
        rec = eval(l)
        k_vocab_data.append([x[0] for x in rec])
    k_vocab.close()

    link_BR_S = []

    sourceLen = []
    f = open(pro+'SourceLen.txt','r')
    #for l in f:
        #sourceLen.append(eval(l.strip()))
    sourceLen = eval(f.read())
    f.close()

    return data, k_vocab_data, link_BR_S, sourceLen


def split_data(data, fold, f):
    """

    :param data: 存放aspectjReportsNLTK.txt全部内容
    :param fold: 10,十折交叉验证
    :param f:
    :return: tr_data：train_data训练数据集合
             te_data：test_data测试数据集合
    """
    index = 0
    tr_data = []
    te_data = []

    for d in data:                 #随机选取9份数据作为训练数据，剩下的一份作为测试数据
        if (index % fold) != f:
            tr_data.append(d)
        else:
            te_data.append(d)
        index += 1
    
    # print (len(tr_data), len(te_data))

    return tr_data, te_data


def llda_cvb0_init(data, k_vocab, k_vocab_total, link, beta_0, beta_1):
    """

    :param data:
    :param k_vocab:
    :param k_vocab_total:
    :param link:
    :param beta_0:
    :param beta_1:
    :return: t_vocab:全部相关文档总数
             w_vocab:全部单词总数
    """
    t_vocab = []                #相关文档ID集合
    w_vocab = []                #文档中单词集合
    for d in data:
        for t in d['ts']:
            t_vocab.append(t)
        for w in d['ws']:
            w_vocab.append(w)

    # print "word count: %d" % len(w_vocab)
    t_vocab = list(set(t_vocab))
    w_vocab = list(set(w_vocab))

    # print "TV: %d, WV: %d" % (len(t_vocab), len(w_vocab))            #TV：全部相关文档总数   WV：全部单词总数

    # random gamma for words
    gamma = {}
    d_index = 1
    for d in data:
        g = []
        tags = d['ts']
        words = d['ws']

        for w in words:
            ts = {}
            g_sum = 0

            for t in tags:
                ts[t] = {}
                #if w == t:
                if w in k_vocab[t]:
                    r = random.random()
                    g_sum += r
                    ts[t][1] = r
                r = random.random()
                g_sum += r
                ts[t][0] = r

            for t in ts:
                for k in ts[t]:
                    ts[t][k] /= g_sum

            g.append((w, ts))

        gamma[d_index] = g
        d_index += 1

    return gamma, t_vocab, w_vocab


def calc_n0_n0all(gamma_d):
    sum_n0 = {}
    sum_n0_all = 0

    for w, ts in gamma_d:
        for t in ts:
            for k in ts[t]:
                sum_n0[t] = sum_n0.get(t, 0) + ts[t][k]
                sum_n0_all += ts[t][k]

    return sum_n0, sum_n0_all


def calc_n1_n1all_n2_n2all_n3_n3all(gamma, t_vocab, w_vocab, k_vocab, k_vocab_total):
    sum_n1 = {}
    sum_n1_all = {}
    sum_n2 = {}
    sum_n2_all = {}
    sum_n3 = {}
    sum_n3_all = {}

    for t in t_vocab:
        sum_n1[t] = {}
        sum_n2[t] = {}
        sum_n3[t] = {}
        sum_n1_all[t] = 0
        sum_n2_all[t] = 0
        sum_n3_all[t] = 0
        for w in w_vocab:
            sum_n1[t][w] = 0
        for k in xrange(2):
            sum_n2[t][k] = 0
        for w in k_vocab_total:
            sum_n3[t][w] = 0

    for d in gamma:
        for w, ts in gamma[d]:
            for t in ts:
                for k in ts[t]:
                    #if w == t:
                    if w in k_vocab[t]:
                        sum_n2[t][k] += ts[t][k]
                        sum_n2_all[t] += ts[t][k]
                    if k == 0:
                        sum_n1[t][w] += ts[t][k]
                        sum_n1_all[t] += ts[t][k]
                    if k == 1:
                        sum_n3[t][w] += ts[t][k]
                        sum_n3_all[t] += ts[t][k]

    return sum_n1, sum_n1_all, sum_n2, sum_n2_all, sum_n3, sum_n3_all


def llda_cvb0(gamma, t_vocab, w_vocab, k_vocab, k_vocab_total, link, beta_0, beta_1, alpha, sourceAplha, eta, delta, count):
    t_num = len(t_vocab)
    v_num = len(w_vocab)

    alpha_l = alpha/t_num
    veta = v_num*eta
    delta_all = delta*len(k_vocab_total)

    beta_all = beta_0 + beta_1

    theta = {}
    phi = {}
    omega = {}
    pl = {}

    for t in t_vocab:
        phi[t] = {}
        for w in w_vocab:
            phi[t][w] = 0

    for t in t_vocab:
        omega[t] = {}
        for w in k_vocab_total:
            omega[t][w] = 0

    # init theta, pl
    for d in gamma:
        if len(gamma[d]) == 0:
            pass
            # print d
        w, ts = gamma[d][0]
        theta[d] = {}
        for t in ts:
            theta[d][t] = 0

    for t in t_vocab:
        pl[t] = 0

    # calc n1, n1_all, n2, n2_all
    n1, n1_all, n2, n2_all, n3, n3_all = calc_n1_n1all_n2_n2all_n3_n3all(gamma, t_vocab, w_vocab, k_vocab, k_vocab_total)

    for c in xrange(1, count+1):
        start_time = time.clock()
        for d in gamma:
            n0, n0_all = calc_n0_n0all(gamma[d])
            w, ts = gamma[d][0]
            for w, ts in gamma[d]:
                g_sum = 0

                # remove current word, so need re-calc n0, n1, n1_all, sometime re-calc n2, n2_all
                for t in ts:
                    #if w == t:
                    if w in k_vocab[t]:
                        n0[t] -= ts[t][1]
                        for k in ts[t]:
                            n2[t][k] -= ts[t][k]
                            n2_all[t] -= ts[t][k]

                        n3[t][w] -= ts[t][1]
                        n3_all[t] -= ts[t][1]

                    n0[t] -= ts[t][0]
                    n1[t][w] -= ts[t][0]
                    n1_all[t] -= ts[t][0]


                for t in ts:
                    theta_d = n0[t] + alpha_l * sourceAplha[t]
                    #if w == t:
                    if w in k_vocab[t]:
                        g1 = theta_d * (n2[t][1] + beta_1)/(n2_all[t] + beta_all) * (n3[t][w] + delta)/(n3_all[t] + delta_all)
                        ts[t][1] = g1
                        g_sum += g1

                        g0 = theta_d*(n1[t][w] + eta)*(n2[t][0] + beta_0)/((n1_all[t] + veta)*(n2_all[t] + beta_all))
                        ts[t][0] = g0
                        g_sum += g0
                    else:
                        g0 = theta_d*(n1[t][w] + eta)/(n1_all[t] + veta)
                        ts[t][0] = g0
                        g_sum += g0

                for t in ts:
                    for k in ts[t]:
                        ts[t][k] /= g_sum

                # add current word, so need re-calc n1, n1_all, n2, n2_all again
                for t in ts:
                    #if w == t:
                    if w in k_vocab[t]:
                        n0[t] += ts[t][1]
                        for k in ts[t]:
                            n2[t][k] += ts[t][k]
                            n2_all[t] += ts[t][k]

                        n3[t][w] += ts[t][1]
                        n3_all[t] += ts[t][1]

                    n0[t] += ts[t][0]
                    n1[t][w] += ts[t][0]
                    n1_all[t] += ts[t][0]

        # print "%03d, elapse: %d" % (c, time.clock() - start_time)

    for d in gamma:
        n0, n0_all = calc_n0_n0all(gamma[d])
        for t in theta[d]:
            theta[d][t] = (n0[t] + alpha_l * sourceAplha[t])/(n0_all + len(theta[d])*alpha_l)

    for d in theta:
        for t in theta[d]:
            pl[t] += theta[d][t]

    for t in pl:
        pl[t] /= len(theta)

    for t in phi:
        for w in w_vocab:
            phi[t][w] = (n1[t][w] + eta)/(n1_all[t] + veta)

    for t in omega:
        for w in k_vocab_total:
            #print w, t
            omega[t][w] = (n3[t][w] + delta)/(n3_all[t] + delta_all)

    ptw = {}
    for t in n2:
        ptw[t] = (n2[t][1] + beta_1)/(n2_all[t] + beta_all)

    return pl, phi, omega, ptw


def llda_cvb0_train(data, k_vocab, k_vocab_total, link, beta_0, beta_1, alpha, sourceAplha, eta, delta, count):
    """

        进行训练
        t_vocab:全部相关文档总数
        w_vocab:全部单词总数
    """
    gamma, t_vocab, w_vocab = llda_cvb0_init(data, k_vocab, k_vocab_total, link, beta_0, beta_1)
    pl, phi, omega, ptw = llda_cvb0(gamma, t_vocab, w_vocab, k_vocab, k_vocab_total, link, beta_0, beta_1, alpha, sourceAplha, eta, delta, count)
    #print ptw

    return pl, phi, omega, ptw


def calc_pws(ws, t_vocab, pz, phi, omega, ptw):
    pws = {}

    ws = list(set(ws))
    for w in ws:
        pws[w] = 0
        for t in t_vocab:
            if w == t:
                pws[w] += (ptw[w] + (1 - ptw[w])*phi[t][w])*pz[t]
            else:
                pws[w] += phi[t][w]*pz[t]

    return pws


def calc_pwds(ws):
    pwds = {}

    ws_sum = len(ws)
    cws = Counter(ws)
    for w in cws:
        pwds[w] = cws[w]*1.0/ws_sum

    return pwds


def llda_test(data, k_vocab_total, pl, phi, omega, ptw, fold):
    l0 = phi.keys()[0]
    w_vocab = set(phi[l0].keys())
    t_vocab = pl.keys()

    r5 = 0
    r10 = 0
    h5 = 0
    h10 = 0
    p5 = 0
    p10 = 0

    # f_result = open(fn, 'w')
    bugindex = 0
    for d in data:
        wss = d["ws"]
        tags = d["ts"]
        sCom = d['ss']

        ws_temp = wss[:]
        ws = wss[:]
        for w in ws_temp:
            if w not in w_vocab:
                ws.remove(w)
        del ws_temp

        pws = calc_pws(ws, t_vocab, pl, phi, omega, ptw)
        pwds = calc_pwds(ws)

        pzd = {}
        for t in t_vocab:
            pzd[t] = 0
            for w in set(ws):
                #if w == t:
                if w in k_vocab_total:
                    pzd[t] += (ptw[t] * omega[t][w] + (1 - ptw[t])*phi[t][w])*pl[t]*pwds[w]/pws[w]
                else:
                    pzd[t] += phi[t][w]*pl[t]*pwds[w]/pws[w]

        del pwds
        del pws

        pzd_f = {}
        for t in pzd.keys():
            if len(list(set([sCom]) & sourceCom[t])) > 0:
                pzd_f[t] = pzd[t]

        # test one record
        s_ptd = sorted(pzd_f.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        return s_ptd
        #s_ptd = s_ptd[0:20]
        # print >> f_result, tags
        # print >> f_result, s_ptd
    #     ptd_l = []
    #     for t, num in s_ptd:
    #         ptd_l.append(t)
    #     global outf
    #     for t in tags:
    #         if t not in ptd_l:
    #             print >> outf, ','.join([str(bugindex * 10 + fold),str(t),'10000','0'])
    #         else:
    #             print >> outf, ','.join([str(bugindex * 10 + fold),str(t),str(ptd_l.index(t)),str(pzd_f[t])])
    #
    #     count = 0
    #     c5 = 0
    #     c10 = 0
    #     for t, rd in s_ptd[:20]:
    #         if t in tags:
    #             if count < 10:
    #                 c5 += 1
    #             c10 += 1
    #         count += 1
    #
    #     if c5 > 0:
    #         h5 += 1
    #     if c10 > 0:
    #         h10 += 1
    #
    #     r5 += float(c5)/len(tags)
    #     p5 += float(c5)/5
    #     r10 += float(c10)/len(tags)
    #     p10 += float(c10)/10
    #
    #     bugindex += 1
    #
    # data_num = len(data)
    # r5 /= data_num
    # r10 /= data_num
    # h5 /= float(data_num)
    # h10 /= float(data_num)
    # p5 /= data_num
    # p10 /= data_num
    #
    # # print >> f_result, "r5: %.5f, p5: %.5f, h5: %.5f, r10: %.5f, p10: %.5f, h10: %.5f" % (r5, p5, h5, r10, p10, h10)
    # # print "r5: %.5f, p5: %.5f, h5: %.5f, r10: %.5f, p10: %.5f, h10: %.5f" % (r5, p5, h5, r10, p10, h10)
    #
    # # f_result.close()
    #
    # return r5, p5, h5, r10, p10, h10


def main():
    # data:集合，存放aspectjReportsNLTK.txt全部内容
    # k_vocab：全部单词ID的集合
    # link：空集合
    # sourcelen：aspectjSourceLen.txt文件的内容，即每个文档的长度
    data, k_vocab, link, sourcelen = load_data()
    fold = 10

    sourcelen = [math.log(ss+1) for ss in sourcelen]         #对每个文件的长度求对数
    sourcesum = float(sum(sourcelen))/float(len(sourcelen))  #平均源文件长度

    sourceAplha = [float(ss)/sourcesum for ss in sourcelen]  #各文件长度对数除以平均源文件长度（归一化）
    # print "pre sourceAplha:",sourceAplha
    sourceAplha = [1 for ss in sourcelen]
    # print "sourceAplha:",sourceAplha

    k_vocab_total = set()
    for d in k_vocab:
        k_vocab_total = k_vocab_total | set(d)
    k_vocab_total = list(k_vocab_total)                      #将全部单词ID转换成一个list

    beta_0 = 0.1
    beta_1 = 0.1
    alpha = 50.0
    eta = 0.01
    delta = 0.01

    ar5, ap5, ah5, ar10, ap10, ah10 = 0, 0, 0, 0, 0, 0

    avg_train = 0.0
    avg_predict = 0.0

    f_report = open('AspectJsall.txt', 'w')

    data_num = fold

    for f in xrange(fold):                             #进行10次十折交叉验证
        #tr_data, te_data = load_multi_data()
        tr_data, te_data = split_data(data, fold, f)   #获得训练数据集和测试数据集
        train_start = time.time()
        pl, phi, omega, ptw = llda_cvb0_train(tr_data, k_vocab, k_vocab_total, link, beta_0, beta_1, alpha, sourceAplha, eta, delta, 1)
        train_end = time.time()
        train_cost = train_end - train_start             #计时
        # print "fold", f, "train time is", train_cost
        print >> f_report, "fold", f, "train time is", train_cost

        
        predict_start = time.time()                    #测试
        # r5, p5, h5, r10, p10, h10 = llda_test(te_data, k_vocab_total, pl, phi, omega, ptw, f)
        result = llda_test(te_data, k_vocab_total, pl, phi, omega, ptw, f)
        predict_end = time.time()
        predict_cost = predict_end - predict_start
        # print "fold", f, "predict time is", predict_cost
        print >> f_report, "fold", f, "predict time is", predict_cost


        # ar5 += r5
        # ah5 += h5
        # ar10 += r10
        # ah10 += h10
        # ap5 += p5
        # ap10 += p10

        avg_train += train_cost
        avg_predict += predict_cost

        # print "fold-%02d:\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f" % (f, r5, p5, h5, r10, p10, h10)
        # print >> f_report, "%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f" % (r5, p5, h5, r10, p10, h10)

        

        

    ar5 /= data_num
    ap5 /= data_num
    ah5 /= data_num
    ar10 /= data_num
    ap10 /= data_num
    ah10 /= data_num

    avg_train /= 10
    avg_predict /= 10

    # print "--------"
    # print "avg:\t\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f" % (ar5, ap5, ah5, ar10, ap10, ah10)
    # print "avg time", avg_train, avg_predict

    print >> f_report, "---avg---"
    print >> f_report, "%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f" % (ar5, ap5, ah5, ar10, ap10, ah10)
    print >> f_report, "avg time", avg_train, avg_predict
    f_report.close()
    global outf
    outf.close()
    return result


if __name__ == '__main__':
    bugid = argv
    topn = main()
    output = open(pro+'filelist'+bugid[0]+'.txt', 'w')
    print >> output, "bugid:"+bugid+'\n'
    n = 0
    for i in topn:
        n += 1
        print >> output, i[0]+'\n'
        if n == 20:
            break
    output.close()
