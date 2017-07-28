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

contentlist = []


def main():
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
    words = []
    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:15]:
            words.append(word)
            print word
            # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    words = list(set(words))
    wordmap = open('data/WordMap.txt', 'a')
    for w in words:
        print >> wordmap, w
    wordmap.close()

if __name__ == '__main__':
    main()
