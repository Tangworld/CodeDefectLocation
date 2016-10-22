#!/usr/local/python
# -*- coding: utf-8 -*-
# encoding=utf-8
import urllib
import re
import MySQLdb
from bs4 import BeautifulSoup


def getAllLinks():
    """
    @author:tsj
    从AspectJ的bug列表开始，找到每一个bug的页面并进入，获取bugid，bug的状态，
    开始时负责修复bug的人以及真正的修复者
    :return: null
    """
    prefix = "https://bugs.eclipse.org/bugs/"


    html = urllib.urlopen('https://bugs.eclipse.org/bugs/buglist.cgi?bug_status=RESOLVED&bug_status=VERIFIED&product=AspectJ&query_format=advanced&resolution=FIXED').read()
    soup = BeautifulSoup(html, 'html.parser')
    #urls = soup.html.body.div.next_sibling.next_sibling.table.children

    #获取了关于AspectJ的所有bug页面链接
    urls = soup.findAll(name='a', attrs={"href": re.compile(r'^show_bug.cgi')})
    count = 0
    print type(urls)
    print urls.__len__()

    flag = False
    for url in urls:
        if count!=0:
            #进入具体页面
            try:
                print "enter"
                url = prefix+url["href"].encode("utf-8")
                BUGID = url[url.index('=')+1:].strip()
                if BUGID == "350855":
                    flag = True
                if flag == True:
                    print url
                    page = urllib.urlopen(url).read()
                    soup2 = BeautifulSoup(page, 'html.parser')
                    STATUS = soup2.find(name='span', attrs={"id": re.compile(r'^static_bug_status')})
                    if STATUS is not None:
                        STATUS = STATUS.string.encode("utf-8").strip()
                    ORIGINAL = soup2.find(name='span', attrs={"class": re.compile(r'^fn')})
                    if ORIGINAL is not None:
                        ORIGINAL = ORIGINAL.string.encode("utf-8").strip()
                    DESCRIPTION = soup2.find(name='span', attrs={"id": re.compile(r'^short_desc_nonedit_display')}).string
                    if DESCRIPTION is not None:
                        DESCRIPTION = DESCRIPTION.strip()
                    print type(DESCRIPTION)
                    ASSIGNEES = []
                    ASSIGNEES = getHistory(BUGID)
                    STATUS = STATUS.replace("\n", "")
                    print BUGID + "   " + STATUS + "    " + ORIGINAL + "      " + DESCRIPTION
                    save(BUGID, STATUS, ORIGINAL, ASSIGNEES, None, DESCRIPTION)
            except Exception, ex:
                continue
        count += 1
        # if count == 15:
        #     cursor.close()
        #     db.close()
        #     db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
        #     cursor = db.cursor()

    print count

def getHistory(bugid):
    """
    挖掘tossing信息，进入history页面查找是否有assignee的变更
    :param url: history页面的地址
    :return: 填充得到的assignee列表
    """
    historyprefix = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="
    url = historyprefix+bugid
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    assignees = []
    temp = soup.body.div.next_sibling.next_sibling.table.tr.next_siblings
    for t in temp:
        if isinstance(t, basestring) | (t is None):
            continue
        # print t.td
        flag = False
        for tdd in t.td:
            if tdd.string.strip() == "Assignee":
                flag = True
            if flag is True:
                assignees.append(tdd.string.strip())
    return assignees

def save(bugid,status,original,current,path,description):
    """
    爬取到所需的信息后则调用该函数将数据插入到数据库中
    :param bugid: bug编号
    :param status: 状态
    :param original: 初始时的fixer
    :param current: 真正的fixer
    :param path: sourcefile存储的路径
    :return: null
    """
    # 链接数据库

    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()
    # 插入数据
    if current.__len__() > 0:
        cursor.execute("INSERT INTO aspectj(bugid,original,current1,status,description) VALUES ('%s', '%s', '%s', '%s', '%s')" % (bugid, original, "yes", status, description))
    else:
        cursor.execute("INSERT INTO aspectj(bugid, original, status, description) VALUES ('%s', '%s', '%s', '%s')" % (bugid, original, status, description))
    # data = cursor.fetchall()
    # for da in data:
    #     print da

    # 关闭数据库
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

if __name__ == '__main__':
    getAllLinks()
    # getHistory("https://bugs.eclipse.org/bugs/show_activity.cgi?id=50045")
    # save()
