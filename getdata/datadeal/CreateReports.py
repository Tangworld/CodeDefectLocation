#coding=utf-8
import  xml.dom.minidom
import nltk
import string
import MySQLdb

def main():
    alllinks = []
    finaldata = []
    dom = xml.dom.minidom.parse('AspectJBugRepository.xml')
    # 得到文档元素对象
    root = dom.documentElement
    bugs = root.getElementsByTagName('bug')
    cnt = 0
    for i in range(0, 286, 1):
        # try:
        linkedFile = []
        textfile = bugs[i].childNodes[3]
        files = textfile.childNodes

        for file in files:
            if file.nodeName == "file":
                # print file.firstChild.data
                linkedFile.append(file.firstChild.data)
                cnt += 1
        alllinks.append(linkedFile)
    print cnt
    print len(alllinks)
    for link in alllinks:
        print link
    reports = open('reports.txt', 'r')
    lines = reports.readlines()
    reports.close()
    lines2 = []
    for line in lines:
        line = line.replace('\n', '')
        line = eval(line)
        lines2.append(line)
        print type(line)
    reports = open('reports.txt', 'w')
    for i in range(0, 286, 1):
        finaldata.append((alllinks[i], lines2[i], ['aspectj'], 'compiler'))
    for f in finaldata:
        print >> reports, f


def reports_index():
    data = []
    db = MySQLdb.connect("localhost", "bugs", "bugs", "bugs")
    cursor = db.cursor()
    reports = open('reports.txt', 'r')
    lines = reports.readlines()
    reports.close()
    for line in lines:
        link = []
        words = []
        line = eval(line)
        for l in line[0]:
            try:
                cursor.execute("select id from filemap where fileloc='%s'" % l)
                result = cursor.fetchone()
                link.append(int(result[0]))
            except Exception, e:
                print e
                continue

        for w in line[1]:
            try:
                cursor.execute("select id from wordmap where word='%s'" % w)
                result = cursor.fetchone()
                words.append(int(result[0]))
            except Exception, e:
                print e
                continue

        data.append((link, words, line[2], line[3]))
    print len(data)
    reports = open('reports.txt', 'w')
    for d in data:
        print d
        print >> reports, d



if __name__ == "__main__":
    reports_index()