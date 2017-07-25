import nltk
import string
from nltk.corpus import stopwords
def main():
    pre = "/var/www/html/bugzilla/"
    input = open("FileMap.txt", "r")
    wordmap = open("WordMap.txt","r")
    dictionary = wordmap.readlines()
    lines = input.readlines()
    input.close()
    wordmap.close()
    print len(lines)

    realword = []

    for line in lines:
        try:
            words = []
            num = []
            line = line.replace('\n', '')
            filename = pre + line
            myfile = open(filename, "r")
            linenum = myfile.readlines()
            print line

            delset = string.punctuation
            for l in linenum:
                l = l.lower()
                for c in delset:
                    l = l.replace(c, " ")
                sens = nltk.sent_tokenize(l)
                for sent in sens:
                    words.append(nltk.word_tokenize(sent))
            for w in words:
                for ww in w:
                    if ww not in realword:
                        realword.append(ww)
            # print num
        except Exception,ex:
            print ex
            continue
    for r in realword:
        print r
    output = open("WordMap.txt","a")
    for r in realword:
        if r not in dictionary:
            print >> output,r
    output.close()


def createSourceTXT():
    pre = "/var/www/html/bugzilla/"
    wordmap = open("WordMap.txt", "r")
    input = open("FileMap.txt", "r")
    keywords = open("keywords.txt","r")
    remove = keywords.readlines()
    lines = input.readlines()
    dictionary = wordmap.readlines()
    print len(dictionary)
    source = open("source.txt","w")
    delset = string.punctuation
    mystopwords = stopwords.words('english')
    finalremove = []
    for my in mystopwords:
        finalremove.append(my)
    for rem in remove:
        finalremove.append(rem)
    indexl = 0
    print len(lines)
    for line in lines:
        try:
            #print line
            words = []
            num = []
            line = line.replace('\n', '')
            filename = pre + line
            myfile = open(filename, "r")
            linenum = myfile.readlines()

            for l in linenum:
                l = l.lower()
                for c in delset:
                    l = l.replace(c, " ")
                sens = nltk.sent_tokenize(l)
                for sent in sens:
                    words.append(nltk.word_tokenize(sent))
            for i in range(0,len(dictionary)):
                dictionary[i] = dictionary[i].replace('\n', "")
                for w in words:
                    for ww in w:
                        if ww == dictionary[i]:
                            if ww not in finalremove:
                                #print ww
                                num.append(i)
            realnum = []
            for p in range(0,len(num)):
                cnt = 0
                for q in range(p+1,len(num)):
                    if num[q] == num[p]:
                        cnt += 1
                if cnt > 39:
                    if num[p] not in realnum:
                        realnum.append(num[p])
            finalnum = []
            for n in realnum:
                finalnum.append((n,100))
            print finalnum
            print >> source,finalnum
        except Exception, ex:
            print ex
            print >> source, [(0, 100)]
            continue

if __name__ == "__main__":
    # main()
    createSourceTXT()