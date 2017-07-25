#coding=utf-8
import  xml.dom.minidom
import nltk
import string

def main():
    dom = xml.dom.minidom.parse('AspectJBugRepository.xml')

    # 得到文档元素对象
    root = dom.documentElement
    bugidwrite = []
    filewrite = []


    bugs = root.getElementsByTagName('bug')
    summaries = root.getElementsByTagName('summary')
    descriptions = root.getElementsByTagName('description')

    wordsmap = open("WordMap.txt", "r")
    reports = open("reports.txt","w")
    dictionary = wordsmap.readlines()
    print type(dictionary)
    # for d in dictionary:
    #     d = d.replace('\n','')
    #     print d
    wordsmap.close()
    filenum = 0
    for i in range(0, 286, 1):
        try:
            words = []
            linkedFile = []
            wordindex = []
            report = []
            realword = []
            id = int(bugs[i].getAttribute("id"))
            opendate = bugs[i].getAttribute("opendate")
            fixdate = bugs[i].getAttribute("fixdate")
            summary = summaries[i].firstChild.data
            summary = summary.lower()
            description = descriptions[i].firstChild.data
            content = summary+description
            content = content.lower()
            delset = string.punctuation
            for c in delset:
                content = content.replace(c, " ")
            sens = nltk.sent_tokenize(content)
            for sent in sens:
                words.append(nltk.word_tokenize(sent))
            fileloc = ""
            textfile = bugs[i].childNodes[3]
            files = textfile.childNodes
            for file in files:
                if file.nodeName == "file":
                    linkedFile.append(filenum)
                    filenum += 1


            # print len(dictionary)
            # print len(words)
            # for w in words:
            #     for ww in w:
            #         print ww
            for j in range(0,len(dictionary)):
                dictionary[j] = dictionary[j].replace('\n',"")
                # print dictionary[j]
                for w in words:
                    for ww in w:
                        if ww == dictionary[j]:
                            # print ww,dictionary[j]
                            wordindex.append(j)
            for p in range(0,len(wordindex)):
                cnt = 0
                for q in range(p+1,len(wordindex)):
                    if wordindex[q] == wordindex[p]:
                        cnt += 1
                # print cnt
                if cnt > 2:
                    if wordindex[p] not in realword:
                        realword.append(wordindex[p])
            report.append(linkedFile)
            report.append(realword)
            report.append("aspectj")
            report.append("hey")
            print >> reports,report

        except Exception, ex:
            print ex
            continue
    reports.close()
    # for w in words:
    #     for ww in w:
    #         print ww


if __name__ == "__main__":
    main()