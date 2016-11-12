#!/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj
# -*- coding: utf-8 -*-
# encoding=utf-8

import urllib
import re
import MySQLdb
from bs4 import BeautifulSoup


def getAllLinks(ofs):
    print ofs
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
            # db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
            # cursor = db.cursor()
            # cursor.execute(
            #     "INSERT INTO assist(bugid, sourcepath, author) VALUES ('%s', '%s', '%s')" % (
            #     BUGID, FILEPATH, AUTHOR))
            # db.commit()
            # cursor.close()
            # db.close()


def getBugid(line):
    num = ""
    for char in line:
        if char.isdigit():
            num += char
    return num

def getFile(url,bugid):
    try:
        path = "/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj/SourceFile/"
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')


        # 爬取文件名信息
        table = soup.find(name='table', attrs={"class": re.compile(r'^diffstat$')})
        print table
        contents = table.children
        print contents
        filename = path + bugid + ".txt"
        f = file(filename, "w+")
        for content in contents:
            if content is None:
                continue
            if isinstance(content, basestring):
                continue
            print content.name
            print content
            tds = content.children
            count = 0
            temp1 = ""
            temp2 = ""
            temp3 = ""
            for td in tds:
                if count == 0:
                    if td.string is not None:
                        temp1 = td.string.encode("utf-8")
                if count == 1:
                    if td.a.string is not None:
                        temp2 = td.a.string.encode("utf-8")
                if count == 2:
                    if td.string is not None:
                        temp3 = td.string.encode("utf-8")
                count += 1
            print type(tds)
            f.write(temp1 + temp2 + temp3 + "\n")
        f.write("\n\n\n")
        f.close()


        # 爬取具体修改的代码
        table = soup.find(name='table', attrs={"class": re.compile(r'^diff$')})
        contents = table.tr.td.children
        print contents

        f = file(filename, "a+")
        for content in contents:
            # print content
            # print content['class']
            print type(content['class'].__getitem__(0))
            if content['class'].__getitem__(0) == u'head':
                print True
                temp = content.children
                for t in temp:
                    if isinstance(t, basestring):
                        f.write(t.string.encode("utf-8"))
                    else:
                        if t.name == 'a':
                            f.write(t.string.encode("utf-8") + "\n")
                        else:
                            f.write("\n")
                f.write("\n\n\n")
            # print content.string
            if content.string is None:
                continue
            print content.string
            f.write(content.string.encode("utf-8")+"\n")
        f.close()
    except Exception, ex:
        print ex
    return filename

if __name__ == '__main__':
    i = 50
    while i < 7700:
        getAllLinks(i)
        i += 50