#coding=utf-8
import  xml.dom.minidom
import MySQLdb
import nltk
import string

#用来将数据集AspectJBugRepository.xml中的数据插入到Bugzilla的数据库中
#打开xml文档
dom = xml.dom.minidom.parse('AspectJBugRepository.xml')

#得到文档元素对象
root = dom.documentElement
# print root.nodeName
# print root.nodeValue
# print root.nodeType
# print root.ELEMENT_NODE
bugidwrite = []
filewrite = []
words = []

bugs = root.getElementsByTagName('bug')
summaries = root.getElementsByTagName('summary')
descriptions = root.getElementsByTagName('description')
files = root.getElementsByTagName('file')
print len(bugs)
print len(summaries)
print len(descriptions)
print len(files)
# errorid=[]
#
# filenum = 0
# for i in range(0, 286, 1):
#     try:
#         id = int(bugs[i].getAttribute("id"))
#         bugidwrite.append(id)
#         opendate = bugs[i].getAttribute("opendate")
#         fixdate = bugs[i].getAttribute("fixdate")
#         summary = summaries[i].firstChild.data
#         summary = summary.lower()
#         description = descriptions[i].firstChild.data
#         description = description.lower()
#         content = summary + description
#         delset = string.punctuation
#         for c in delset:
#             content = content.replace(c," ")
#         sens = nltk.sent_tokenize(content)
#         for sent in sens:
#             words.append(nltk.word_tokenize(sent))
#         fileloc = ""
#         textfile = bugs[i].childNodes[3]
#         files = textfile.childNodes
#         for file in files:
#             if file.nodeName == "file":
#                 filenum += 1
#                 fileloc += "$"+file.firstChild.data
#                 filewrite.append(file.firstChild.data)

        # print id
        # print opendate
        # print fixdate
        # print summary
        # print description
        # print fileloc
        # db = MySQLdb.connect("localhost", "bugs", "bugs", "bugs")
        # cursor = db.cursor()
        # # cursor.execute("insert into bugs(bug_id,assigned_to,bug_file_loc,bug_severity,bug_status,creation_ts,delta_ts,short_desc,op_sys,priority,product_id,rep_platform,reporter,version,component_id,everconfirmed) values(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s',%d,'%s',%d,%d)" % (id,1,fileloc,"enhancement","CONFIRMED",opendate,fixdate,summary,"Linux","Normal",2,"PC",2,"0.1",2,1))
        # cursor.execute("insert into longdescs(bug_id,who,bug_when,thetext) values(%d,%d,'%s','%s')" % (id,2,opendate,description))
        # db.commit()  # Commit the transaction
        # cursor.close()
        # db.close()
        # print "finish"
#     except Exception, ex:
#         print ex
#         errorid.append(id)
#         continue
# realword = []
# output = open("WordMap.txt","w")
# for w in words:
#     for ww in w:
#         if ww not in realword:
#             realword.append(ww)
#
# for r in realword:
#     print >> output, r
#
# output.close()
# print "filenum:"
# print filenum
# for i in bugidwrite:
#     print i
# for f in filewrite:
#     print f
# output = open("BugidMap.txt","w")
# output2 = open("FileMap.txt","w")
# for i in bugidwrite:
#     print >> output,i
# for f in filewrite:
#     print >> output2,f
# output.close()
# output2.close()
