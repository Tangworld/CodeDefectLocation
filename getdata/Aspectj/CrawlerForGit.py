#!/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj
# -*- coding: utf-8 -*-
# encoding=utf-8

import urllib
import re
import MySQLdb
from bs4 import BeautifulSoup


def getAllLinks(ofs):
    prefix = "https://git.eclipse.org"
    begin = 'https://git.eclipse.org/c/aspectj/org.aspectj.git/log/?ofs='+str(ofs)
    html = urllib.urlopen(begin).read()
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find(name='tr', attrs={"class": re.compile(r'nohover')}).next_siblings
    for tr in trs:
        if isinstance(tr, basestring):
            continue
        message = tr.td.next_sibling.a.string
        BUGID= getBugid(message)
        if BUGID.__len__() == 6:
            print message+"     ",
            AUTHOR = tr.td.next_sibling.next_sibling.string.strip()
            print AUTHOR
            page = tr.td.next_sibling.a["href"]
            url = prefix + page
            print url
            FILEPATH = getFile(url, BUGID)
            db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO assist(bugid, sourcepath, author) VALUES ('%s', '%s', '%s')" % (
                BUGID, FILEPATH, AUTHOR))
            db.commit()
            cursor.close()
            db.close()


def getBugid(line):
    num = ""
    for char in line:
        if char.isdigit():
            num += char
    return num

def getFile(url,bugid):
    path = "/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj/SourceFile/"
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(name='table', attrs={"class": re.compile(r'^diff$')})
    contents = table.tr.td.children
    print contents
    filename = path + bugid + ".txt"
    f = file(filename, "a+")
    for content in contents:
        # print content.string
        if content.string is None:
            continue
        print type(content.string)
        f.write(content.string.encode("utf-8")+"\n")
    f.close()
    return filename

if __name__ == '__main__':
    i = 450
    while i < 1000:
        getAllLinks(i)
        i += 50