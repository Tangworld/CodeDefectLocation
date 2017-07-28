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




def sourcefile():
    contentlist = []
    filemap = open('data/FileMap.txt', 'r')
    files = filemap.readlines()
    filemap.close()

    for file in files:
        file = file.replace('\n', '')
        try:
            source = open('/home/tsj/PycharmProjects/CodeDefectLocation/keyAlgorithm/'+file, 'r')
            lines = source.readlines()
            content = ""
            for line in lines:
                line = line.replace('\n', '')
                content += line
            print content
            print type(content)
            count = test_tokens(content.decode('utf-8'))
            contentlist.append(count)
        except Exception, e:
            print e
            continue

    get_tf_idf(contentlist)

def report():
    contentlist = []
    resource = open('data/aspectj.csv', 'r')
    lines = resource.readlines()
    resource.close()

    descriptions = []
    for line in lines:
        temp = line.split(',')[4:-1]
        r_temp = str(temp)
        r_temp = r_temp.replace('Summary', '')
        print r_temp
        descriptions.append(r_temp)
    print len(descriptions)
    print type(descriptions)
    descriptions = list(set(descriptions))
    print len(descriptions)
    for d in descriptions:
        print type(d)
        count = test_tokens(d.decode('utf-8'))
        contentlist.append(count)

    get_tf_idf(contentlist)

def rm_duplicate():
    wordmap = open('data/WordMap.txt', 'r')
    lines = wordmap.readlines()
    print len(lines)
    wordmap.close()

    lines = list(set(lines))
    print len(lines)
    wordmap = open('data/WordMap.txt', 'w')
    for line in lines:
        print >> wordmap, line
    wordmap.close()

def rm_n():
    wordmap = open('data/WordMap.txt', 'r')
    lines = wordmap.readlines()
    wordmap.close()

    words = []
    r_words = []
    for line in lines:
        line = line.replace('\n', '')
        words.append(line)
    print words
    for w in words:
        if not w == '':
            r_words.append(w)
    wordmap = open('data/WordMap.txt', 'w')
    for r in r_words:
        print >> wordmap, r
    wordmap.close()


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
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

def get_tf_idf(countlist):
    # words = []
    data = []
    wordmap = open('data/WordMap.txt', 'r')
    dictionary = wordmap.readlines()
    r_dictionary = []
    for d in dictionary:
        r_dictionary.append(d.replace('\n', ''))
    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        onefile = []
        for word, score in sorted_words[:15]:
            # words.append(word)
            for i in range(0,len(r_dictionary)):
                if word == r_dictionary[i]:
                    onefile.append((i, 100))
        data.append(onefile)
    source = open('data/Source.txt', 'w')
    for d in data:
        print >> source, d
    source.close()
            # print word
            # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    # words = list(set(words))
    # wordmap = open('data/WordMap.txt', 'a')
    # for w in words:
    #     print >> wordmap, w
    # wordmap.close()

if __name__ == '__main__':
    sourcefile()
