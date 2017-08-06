# -*- coding: utf-8 -*-
import MySQLdb
import urllib
import re
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def bugidinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    bugidmap = open('../data/bughunter/BugidMap.txt', 'r')
    lines = bugidmap.readlines()
    bugidmap.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_bugidmap(bugidnumber, bugid) values('"+str(cnt)+"', '"+line+"')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()


def fileinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    filemap = open('../data/bughunter/FileMap.txt', 'r')
    lines = filemap.readlines()
    filemap.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_filemap(filenumber, filepath) values('" + str(cnt) + "', '" + line + "')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()


def reportinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    reports = open('../data/bughunter/Reports.txt', 'r')
    lines = reports.readlines()
    reports.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        temp = eval(line)
        tempp = (temp[0], temp[1])
        cursor.execute("insert into locator_reports(reportnumber, content) values('" + str(cnt) + "', '" + str(tempp) + "')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()


def wordinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    wordmap = open('../data/bughunter/WordMap.txt', 'r')
    lines = wordmap.readlines()
    wordmap.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        print line
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_wordmap(wordID, word) values('" + str(cnt) + "', '" + line + "')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()


def update_description():
    prefix = "https://bugs.eclipse.org/bugs/show_bug.cgi?id="
    common = open('../data/l2ss/common.txt', 'r')
    lines = common.readlines()
    common.close()
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()

    for line in lines:
        line = line.replace('\n', '')
        current_url = prefix + line
        # 得到html页面
        html = urllib.urlopen(current_url).read()
        print 'get'
        soup = BeautifulSoup(html, 'html.parser')
        first_div = soup.find(name='div', attrs={"class": re.compile(r'^bz_first_comment_head$')})
        # print first_div
        # if first_div is not None:
        #     first_div = first_div.string.encode("utf-8").strip()
        #     print first_div
        des = first_div.next_sibling.next_sibling.children
        for d in des:
            print d
            description = str(d)
            print description
            description = description.replace("'", "''")
            try:
                cursor.execute("update locator_report set description = '" + description + "'where bugid='" + line + "'")
            except Exception, e:
                print e
                continue

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()


if __name__ == '__main__':
    update_description()