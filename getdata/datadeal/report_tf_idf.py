#coding=utf-8
import  xml.dom.minidom
import MySQLdb
import nltk
import string
import nltk
import math
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
# 解决编码问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#用来将数据集AspectJBugRepository.xml中的数据插入到Bugzilla的数据库中
allwords = []
countlist = []

def main():

    #打开xml文档
    dom = xml.dom.minidom.parse('AspectJBugRepository.xml')

    #得到文档元素对象
    root = dom.documentElement
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
    for i in range(0, 286, 1):
        try:
            id = int(bugs[i].getAttribute("id"))
            bugidwrite.append(id)
            opendate = bugs[i].getAttribute("opendate")
            fixdate = bugs[i].getAttribute("fixdate")
            summary = summaries[i].firstChild.data
            summary = summary.lower()
            description = descriptions[i].firstChild.data
            description = description.lower()
            content = summary + description
            print id
            print
            count = test_tokens(content)
            countlist.append(count)

        except Exception, e:
            print e

    get_tf_idf(countlist)


def get_tokens(text):
    lowers = text.lower()
    print type(lowers)
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    print type(remove_punctuation_map)
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


def test_tokens(content):
    tokens = get_tokens(content)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered, stemmer)
    count = Counter(stemmed)
    return count


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tf(word, count):
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

def get_tf_idf(countlist):
    reports = open('reports.txt', 'w')
    for i, count in enumerate(countlist):
        keywords = []
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:15]:
            keywords.append(word)
            allwords.append(word)
            print word
            # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
        print >> reports, keywords
    reports.close()
    # wordmap = open('WordMap.txt', 'w')
    # for allword in allwords:
    #     print >> wordmap, allword
    # wordmap.close()

if __name__ == '__main__':
    main()
