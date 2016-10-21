#!/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj
# -*- coding: utf-8 -*-
# encoding=utf-8

import urllib
import re
import MySQLdb
from bs4 import BeautifulSoup


def getAllLinks():
    prefix = "https://git.eclipse.org"
    begin = 'https://git.eclipse.org/c/aspectj/org.aspectj.git/log/'
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

def getBugid(line):
    num = ""
    for char in line:
        if char.isdigit():
            num += char
    return num
if __name__ == '__main__':
    getAllLinks()
