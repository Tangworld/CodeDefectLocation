import time
from collections import Counter
import copy
import sys

beta_0 = 0.1
beta_1 = 0.1
alpha = 50.0
eta = 0.01
repeat = 0
mini_count = 1
AFH_MAX = 10
t_vocab = []
if len(sys.argv) == 1:
    PROJECT = raw_input('Project:')

else:
    PROJECT = sys.argv[1]

ranks_dic = {}
component_t = {'cm': {}, 'vs': {}, 'os':{}, 'pf': {}, 'sv': {}, 'pr': {}}
def load_data(fn):
    f_data = open(fn)
    data = []
    global t_vocab
    file_len = {}
    for line in open('../data/' + PROJECT + '.csv'):
        line = line.lower()
        file_len[line.split(',')[0]] = int(line.split(',')[1])


    for l in f_data:
        rec = eval(l)

        t_vocab += rec['ts']
        for tr in rec['tr']:
            if tr in file_len.keys():
                t_vocab.append(tr)
        data.append(rec)
    t_vocab = list(set(t_vocab))

    return data


def isSpecialWord(w, t):
    return len(w) >= mini_count and t.find(w) >= 0


def split_data(data, fold, f):
    index = 0
    tr_data = []
    te_data = []

    for d in data:
        if (index % fold) != f:
            tr_data.append(d)
        else:
            te_data.append(d)
        index += 1

    print (len(tr_data), len(te_data))

    return tr_data, te_data


def l2ss_cvb0_init(data):
    global mini_count, t_vocab
    w_vocab = []
    global component_t
    component_t = {k: {} for k in component_t}
    for d in data:
        for md in component_t:

            cm = d[md].strip()
            if not component_t[md].has_key(cm):
                component_t[md][cm] = set([])
            for t in d['ts']:
                component_t[md][cm].add(t)
        for w in d['ws']:
            w_vocab.append(w)
    print "word count: %d" % len(w_vocab)
    count_w = Counter(w_vocab)

    sort_w = sorted([(w, count_w[w]) for w in count_w], lambda x, y: cmp(x[1], y[1]), reverse=True)
    # highw = [t[0] for t in sort_w[:3]]
    w_vocab = [w for w in set(w_vocab) if count_w[w] > 10 and count_w[w] < 6000]
    r_sort_w = sort_w[:]
    r_sort_w.reverse()
    print "TV: %d, WV: %d" % (len(t_vocab), len(w_vocab))

    substring_count = 0

    # random gamma for words
    gamma = {}
    doc_cm = {}
    doc_tr = {}
    d_index = 1
    tr_sum = 0.0
    for d in data:
        g = []
        tags = d['ts']
        words = d['ws']
        #cm = d[metadata]
        for w in words:
            if count_w[w] > 10 and count_w[w] < 6000:
                ts = {}
                g_sum = 0

                for t in tags:
                    ts[t] = {}
                    if isSpecialWord(w, t):
                        # print t, w
                        substring_count += 1

                        r = 1.0
                        g_sum += r
                        ts[t][1] = r
                    r = 1.0
                    g_sum += r
                    ts[t][0] = r

                for t in ts:
                    for k in ts[t]:
                        ts[t][k] /= g_sum

                g.append((w, ts))
        if len(g) == 0:
            continue
        doc_cm[d_index] = {}
        for md in component_t:
            doc_cm[d_index][md] = d[md]
        doc_tr[d_index] = d['tr']

        gamma[d_index] = g
        d_index += 1



    # print substring_count, len(set(ss_vocab))
    return gamma, t_vocab, w_vocab, doc_cm, doc_tr


# n0 represents doc-domain n_d_t distribution
def calc_n0_n0all(gamma_d):
    sum_n0 = {}
    sum_n0_all = 0

    for w, ts in gamma_d:
        for t in ts:
            for k in ts[t]:
                sum_n0[t] = sum_n0.get(t, 0) + ts[t][k]
                sum_n0_all += ts[t][k]

    return sum_n0, sum_n0_all


# n1 represents global-domain n_t_w distribution
# n2 represents topic-domain n_t_x distribution
def calc_n1_n1all_n2_n2all_n3_n3all(gamma, t_vocab, w_vocab):
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

    for d in gamma:
        for w, ts in gamma[d]:
            for t in ts:
                if isSpecialWord(w, t):
                    sum_n2[t][1] += ts[t][1]
                    sum_n2[t][0] += ts[t][0]
                    sum_n2_all[t] += ts[t][1] + ts[t][0]
                    sum_n3[t][w] = sum_n3[t].get(w, 0) + ts[t][1]
                    sum_n3_all[t] += ts[t][1]
                sum_n1[t][w] += ts[t][0]

                sum_n1_all[t] += ts[t][0]

    return sum_n1, sum_n1_all, sum_n2, sum_n2_all, sum_n3, sum_n3_all


def l2ss_cvb0(gamma, t_vocab, w_vocab, beta_0, beta_1, alpha, eta, count, doc_cm, doc_tr):
    global component_t
    t_num = len(t_vocab)
    v_num = len(w_vocab)
    alpha_l = alpha / t_num
    veta = v_num * eta

    beta_all = beta_0 + beta_1

    theta = {}
    phi = {}
    pl = {}
    phi2 = {}
    for t in t_vocab:
        phi[t] = {}
        phi2[t] = {}
        for w in w_vocab:
            phi[t][w] = 0

    # init theta, pl
    for d in gamma:

        w, ts = gamma[d][0]

        theta[d] = {}
        for t in ts:
            theta[d][t] = 0

    for md in component_t:
        pl[md] = {}
        for tk in component_t[md]:
            pl[md][tk] = {}

    # calc n1, n1_all, n2, n2_all
    n1, n1_all, n2, n2_all, n3, n3_all = calc_n1_n1all_n2_n2all_n3_n3all(gamma, t_vocab, w_vocab)

    for c in xrange(1, count + 1):
        start_time = time.clock()
        for d in gamma:
            n0, n0_all = calc_n0_n0all(gamma[d])
            index = 0

            for w, ts in gamma[d]:

                g_sum = 0

                # remove current word, so need re-calc n0, n1, n1_all, sometime re-calc n2, n2_all
                for t in ts:
                    if isSpecialWord(w, t):
                        n0[t] -= ts[t][1]
                        n3[t][w] -= ts[t][1]
                        n3_all[t] -= ts[t][1]
                        for k in ts[t]:
                            n2[t][k] -= ts[t][k]
                            n2_all[t] -= ts[t][k]

                    n0[t] -= ts[t][0]
                    n1[t][w] -= ts[t][0]
                    n1_all[t] -= ts[t][0]

                for t in ts:
                    theta_d = n0[t] + alpha_l
                    if isSpecialWord(w, t):
                        g1 = theta_d * (n3[t][w] + eta) / (n3_all[t] + beta_all) * (n2[t][1] + beta_1) / (
                        n2_all[t] + beta_all)
                        ts[t][1] = g1
                        g_sum += g1

                        g0 = theta_d * (n1[t][w] + eta) / (n1_all[t] + veta) * (n2[t][0] + beta_0) / (
                        n2_all[t] + beta_all)
                        ts[t][0] = g0
                        g_sum += g0
                    else:
                        g0 = theta_d * (n1[t][w] + eta) / (n1_all[t] + veta)

                        ts[t][0] = g0
                        g_sum += g0

                for t in ts:
                    for k in ts[t]:
                        ts[t][k] /= g_sum

                # add current word, so need re-calc n1, n1_all, n2, n2_all again
                for t in ts:
                    if isSpecialWord(w, t):
                        n0[t] += ts[t][1]
                        n3[t][w] += ts[t][1]
                        n3_all[t] += ts[t][1]
                        for k in ts[t]:
                            n2[t][k] += ts[t][k]
                            n2_all[t] += ts[t][k]

                    n0[t] += ts[t][0]
                    n1[t][w] += ts[t][0]
                    n1_all[t] += ts[t][0]

                gamma[d][index] = (w, ts)
                index += 1

        print "%03d, elapse: %d" % (c, time.clock() - start_time)

    for d in gamma:
        n0, n0_all = calc_n0_n0all(gamma[d])
        for t in theta[d]:
            theta[d][t] = (n0[t] + alpha_l) / (n0_all + len(theta[d]) * alpha_l)

    cm_count = {k: {tk: 0 for tk in component_t[k]} for k in component_t}
    for k in cm_count:
        for kt in cm_count[k]:
            for t in t_vocab:
                pl[k][kt][t] = alpha / len(t_vocab)
    for d in theta:
        for md in doc_cm[d]:
            cm_count[md][doc_cm[d][md]] += 1
            for t in theta[d]:
                pl[md][doc_cm[d][md]][t] = pl[md][doc_cm[d][md]][t] + theta[d][t]
    tr_dis = 0.0
    tr_num = 0
    for d in theta:
        for tr in doc_tr[d]:
            tr_num += 1
            if tr in theta[d].keys():
                tr_dis += theta[d][tr]
    if tr_num == 0:
        tr_dis = 1
    else:
        tr_dis /= tr_num

    for md in component_t:
        for c in component_t[md]:
            for t in pl[md][c]:
                pl[md][c][t] /= cm_count[md][c]


    for t in phi:
        for w in w_vocab:
            phi[t][w] = (n1[t][w] + eta) / (n1_all[t] + veta)

    for t in n3:
        t_size = len(n3[t].keys())
        for w in n3[t]:
            phi2[t][w] = (n3[t][w] + eta) / (n3_all[t] + eta * t_size)

    ptw = {}
    for t in n2:
        ptw[t] = (n2[t][1] + beta_1) / (n2_all[t] + beta_all)

    epl = {}

    for t in t_vocab:
        epl[t] = 0

    for d in theta:

        for t in theta[d]:
            epl[t] += theta[d][t]

    for t in t_vocab:
        epl[t] /= len(theta)

    return epl, pl, phi, ptw, phi2, tr_dis


def l2ss_cvb0_train(data, beta_0, beta_1, alpha, eta, count):
    gamma, t_vocab, w_vocab, doc_cm, doc_tr = l2ss_cvb0_init(data)
    epl, pl, phi, ptw, phi2, tr_dis = l2ss_cvb0(gamma, t_vocab, w_vocab, beta_0, beta_1, alpha, eta, count, doc_cm, doc_tr)
    # print ptw

    return epl, pl, phi, ptw, phi2, tr_dis


def calc_pws(ws, t_vocab, pz, phi, phi2, ptw):
    pws = {}

    ws = list(set(ws))
    for w in ws:
        pws[w] = 0
        for t in t_vocab:
            if isSpecialWord(w, t):
                pws[w] += (ptw[t] * phi2[t].get(w, 0) + (1 - ptw[t]) * phi[t][w]) * pz[t]
            else:
                pws[w] += phi[t][w] * pz[t]

    return pws


def calc_pwds(ws):
    pwds = {}

    ws_sum = len(ws)
    cws = Counter(ws)
    for w in cws:
        pwds[w] = cws[w] * 1.0 / ws_sum

    return pwds


def getHitResult(ranks):
    hits = {i: 0.0 for i in xrange(20)}
    recalls = {i: 0.0 for i in xrange(20)}
    precision = {i : 0.0 for i in xrange(20)}
    hit_rank_num = 0.0
    mapnum = 0
    for i in xrange(20):
        if hit_rank_num < len(ranks):
            if ranks[int(hit_rank_num)] <= i:
                hit_rank_num = hit_rank_num + 1
        if hit_rank_num > 0:
            hits[i] = 1.0
        recalls[i] = hit_rank_num / len(ranks)
        precision[i] = hit_rank_num / (i + 1)
    for i, rank in enumerate(ranks):
        mapnum += (i + 1.0) / (rank + 1.0)
    afh = min(AFH_MAX, min(ranks))
    return hits, precision, recalls, mapnum / len(ranks), float(afh)


def l2ss_test(data, epl, pl, phi, phi2, ptw, tr_dis):
    global component_t
    l0 = phi.keys()[0]
    w_vocab = set(phi[l0].keys())
    global t_vocab

    hit_dic = {i: 0 for i in xrange(20)}
    recall_dic = {i: 0 for i in xrange(20)}
    precision_dic = {i: 0 for i in xrange(20)}
    e_map = 0
    e_afh = 0
    # f_result = open(fn, 'w')
    for d in data:
        wss = d["ws"]
        tags = d["ts"]
        trs = d['tr']
        ws_temp = wss[:]
        ws = wss[:]
        for w in ws_temp:
            if w not in w_vocab:
                ws.remove(w)
        del ws_temp

        # pws = calc_pws(ws, t_vocab, pl, phi, phi2, ptw)
        pwds = calc_pwds(ws)
        ptv = {t: 1.0 for t in t_vocab}
        for md in component_t:
            if not pl[md].has_key(d[md]):
                for t in t_vocab:
                    ptv[t] *= epl[t]
            else:
                for t in t_vocab:
                    ptv[t] *= pl[md][d[md]][t]
        ptr = {}
        pc = 1.0
        for tr in trs:
            ptr[tr] = tr_dis
            pc -= tr_dis
        for t in t_vocab:
            if t not in trs:
                ptr[t] = pc / (len(t_vocab) - len(trs))
            ptv[t] *= ptr[t]

        pzd = {k: 0 for k in ptv}
        for w in set(ws):
            pzw = {}
            sum_pzw = 0
            for t in ptv:
                if isSpecialWord(w, t):
                    pzw[t] = pzw.get(t, 0) + (ptw[t] * phi2[t].get(w, 0) + (1 - ptw[t]) * phi[t][w]) * ptv[t]
                else:
                    pzw[t] = pzw.get(t, 0) + phi[t][w] * ptv[t]
                sum_pzw += pzw[t]
            for t in ptv:
                pzw[t] /= sum_pzw
                pzd[t] += pzw[t] * pwds[w]

        del pwds
        # del pws


        # test one record
        s_ptd = sorted(pzd.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        # final_rank = [ll[0] for ll in s_ptd[:20]]
        # ranks_dic[d['id']] = final_rank

        rank_dic = {}
        rank = 0
        contain = 0
        for t, rd in s_ptd:
            if t in tags:
                contain += 1
                rank_dic[t] = rank
            if contain == len(tags):
                break
            rank += 1
        ranks = rank_dic.values()
        ranks.sort()

        hits, precision, recalls, mapnum, afh = getHitResult(ranks)
        e_map += mapnum / len(data)
        e_afh += afh / len(data)
        for i in xrange(20):
            hit_dic[i] += hits[i] / len(data)
            recall_dic[i] += recalls[i] / len(data)
            precision_dic[i] += precision[i] / len(data)




    # print >> f_result, "r5: %.5f, p5: %.5f, h5: %.5f, r10: %.5f, p10: %.5f, h10: %.5f" % (r5, p5, h5, r10, p10, h10)
    # print "r5: %.5f, p5: %.5f, h5: %.5f, r10: %.5f, p10: %.5f, h10: %.5f" % (r5, p5, h5, r10, p10, h10)

    # f_result.close()

    return hit_dic, precision_dic, recall_dic, e_map, e_afh


def main():
    data = load_data(PROJECT + 'fullfilter2.txt')
    fold = 10

    beta_0 = 0.1
    beta_1 = 0.1
    alpha = 50.0
    eta = 0.01

    ahit_dic = {i: 0 for i in xrange(20)}
    arecall_dic = {i: 0 for i in xrange(20)}
    aprecision_dic = {i: 0 for i in xrange(20)}
    amap = 0.0
    aafh = 0.0
    avg_train = 0.0
    avg_predict = 0.0

    f_report = open('../result/' + PROJECT +'/'+ '_'.join(component_t.keys()) + 'L2SS.txt', 'w')

    data_num = fold

    for f in xrange(fold):
        # tr_data, te_data = load_multi_data()
        tr_data, te_data = split_data(data, fold, f)
        train_start = time.time()
        epl, pl, phi, ptw, phi2, tr_dis = l2ss_cvb0_train(tr_data, beta_0, beta_1, alpha, eta, repeat)
        train_end = time.time()
        train_cost = train_end - train_start
        print "fold", f, "train time is", train_cost
        print >> f_report, "fold", f, "train time is", train_cost

        predict_start = time.time()
        hit_dic, precision_dic, recall_dic, e_map, e_afh = l2ss_test(te_data, epl, pl, phi, phi2, ptw, tr_dis)
        predict_end = time.time()
        predict_cost = predict_end - predict_start
        print "fold", f, "predict time is", predict_cost
        print >> f_report, "fold", f, "predict time is", predict_cost
        for i in xrange(20):
            ahit_dic[i] += hit_dic[i] / 10.0
            arecall_dic[i] += recall_dic[i] / 10.0
            aprecision_dic[i] += precision_dic[i] / 10.0
        amap += e_map / 10.0
        aafh += e_afh / 10.0
        avg_train += train_cost
        avg_predict += predict_cost

        print "fold-%02d:" % (f)
        print "hit:", hit_dic
        print "recall:", recall_dic
        print "precision:", precision_dic
        print "map:", e_map
        print >> f_report, [hit_dic, recall_dic, precision_dic, e_map]


    avg_train /= 10
    avg_predict /= 10

    print "--------"
    print "avg:"
    print "avg time:", avg_train, avg_predict
    print "hit:", ahit_dic
    print "recall:", arecall_dic
    print "precision:", aprecision_dic
    print "map:", amap
    print >> f_report, "---avg---"
    print >> f_report, "avg time", avg_train, avg_predict
    result = {"hit:": ahit_dic, "recall:": arecall_dic, "precision:": aprecision_dic, "map:": amap, "AFH:": aafh}
    print >> f_report, result


    f_report.close()


if __name__ == '__main__':

    main()
    # f = open("C:\\Users\\shelfee\\work\\lda_llda_hllda\\QRS\\RVSM\\rVSMresult\\%s%sL2SSranks.txt"%(PROJECT,metadata), 'w')
    # print >>f, ranks_dic
    # f.close()