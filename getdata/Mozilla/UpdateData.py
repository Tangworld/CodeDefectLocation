#!/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj
# -*- coding: utf-8 -*-
# encoding=utf-8
import MySQLdb
import urllib
import re
from bs4 import BeautifulSoup


def update():
    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()
    cursor.execute('select * from aspectj')
    dataset1 = cursor.fetchall()
    print type(dataset1)
    cursor.execute("select * from assist")
    dataset2 = cursor.fetchall()
    for i in dataset1:
        idd = i[1]
        for j in dataset2:
            if j[1] == idd:
                print j
                des = i[11]
                ori = i[2]
                sta = i[9]
                if (des is None) or (ori is None) or (sta is None):
                    continue
                cursor.execute("update assist set original = '"+ori+"' ,description = '"+des+"', status='"+sta+"'")

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

def minor():
    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()
    cursor.execute("select * from mozilla")
    dataset = cursor.fetchall()
    cursor.close()
    db.close()
    dataset = list(dataset)
    for i in range(0, 14328, 1):
        dataset[i] = list(dataset[i])
    for i in range(0, 14328, 1):
        j = i+1
        while j < 14328:
            # print dataset[j][1]
            if dataset[j][1] == dataset[i][1]:
                # print dataset[j]
                dataset[j][1] = "000000"
            j += 1
    print dataset.__len__()
    # for i in range(0,2480,1):
    #     print dataset[i]
    for i in range(0, 14328, 1):
        if dataset[i][1] == "000000":
            db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
            cursor = db.cursor()
            cursor.execute("update mozilla set bugid = '000000' where id='%s'" % dataset[i][0])
            db.commit()  # Commit the transaction
            cursor.close()
            db.close()


def getHistory(bugid):
    """
    挖掘tossing信息，进入history页面查找是否有assignee的变更
    :param url: history页面的地址
    :return: 填充得到的assignee列表
    """
    try:
        historyprefix = "https://bugzilla.mozilla.org/show_activity.cgi?id="
        url = historyprefix+bugid
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        assignees = []
        # div = soup.find(name='div', attrs={"id": re.compile(r'^bugzilla-body$')})
        # print div.table
        temp = soup.body.div.next_sibling.next_sibling.table.tr.next_siblings
        # print temp
        for t in temp:
            if isinstance(t, basestring) | (t is None):
                continue
            # print t.string
            # print t.td
            flag = False
            s = t.children
            for ss in s:
                if ss.string is None:
                    continue
                if ss.string.strip() == "Assignee":
                    print ss.next_sibling.next_sibling
                    assi = ss.next_sibling.next_sibling
                    assignees.append(assi.string.strip())
        # if s.string == "Assignee":
        #     print "true"
        #     print s.next_sibling.next_sibling
            # assignees.append(s.next_sibling.next_sibling.string.trim())
    except Exception, ex:
        return assignees
    return assignees


def getAssignees():
    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()
    cursor.execute("select * from mozilla where current1='yes' ")
    dataset = cursor.fetchall()
    cursor.close()
    db.close()

    for data in dataset:
        print data[1]
        assignees = getHistory(data[1])
        db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
        cursor = db.cursor()
        for i in range(0, assignees.__len__(), 1):
            if i > 5:
                break
            cursor.execute("update mozilla set current"+str(i+1)+" = '"+assignees[i]+"' where bugid='"+data[1]+"' ")

        db.commit()  # Commit the transaction
        cursor.close()
        db.close()

    print "\n"

if __name__ == "__main__":
    getAssignees()