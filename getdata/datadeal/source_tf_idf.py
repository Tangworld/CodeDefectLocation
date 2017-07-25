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
allwords = []
countlist = []

def main():

    filemap = open('FileMap.txt', 'r')
    files = filemap.readlines()
    pre = "/var/www/html/bugzilla/"
    for line in files:
        line = line.replace('\n', '')
        filename = pre + line
        try:
            source = open(filename, 'r')
        except Exception, e:
            print e
            fill = unicode('None')
            count = test_tokens(fill)
            countlist.append(count)
            continue

        content = ''
        slines = source.readlines()
        for sl in slines:
            sl = sl.replace('\n', '')
            content += sl
        content = content.decode("utf-8")
        count = test_tokens(content)
        countlist.append(count)


    get_tf_idf(countlist)


def get_tokens(text):
    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
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
    print count, '  ', word, ' ', type(count), ' ', type(word)
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

def get_tf_idf(countlist):
    reports = open('source.txt', 'w')
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
        realkeywords = []
        for keyw in keywords:
            realkeywords.append((keyw, 100))
        print >> reports, realkeywords
    reports.close()
    wordmap = open('WordMap.txt', 'a')
    for allword in allwords:
        print >> wordmap, allword
    wordmap.close()

if __name__ == '__main__':
    main()
