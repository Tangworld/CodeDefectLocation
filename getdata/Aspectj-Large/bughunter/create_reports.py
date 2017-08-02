#coding=utf-8

import string
import nltk
import math
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *

id_dictionary = []
w_dictionary = []
f_dictionary = []
linkedfile = []

def main():
    pre()
    contentlist = []
    resource = open('data/aspectj.csv', 'r')
    lines = resource.readlines()
    resource.close()

    descriptions = []
    for id in id_dictionary:
        count = []
        onefile = []
        for i in range(1, len(lines)):
            currentid = lines[i].split(',')[0]
            if id == currentid:
                temp = lines[i].split(',')[4:-1]
                r_temp = str(temp)
                r_temp = r_temp.replace('Summary', '')
                count = test_tokens(r_temp.decode('utf-8'))

                sourcefile = lines[i].split(',')[-1]
                sourcefile = sourcefile.replace(' ', '')
                sourcefile = sourcefile.replace('\n', '')
                sourcefile = sourcefile.replace('\r', '')
                for f in range(0, len(f_dictionary)):
                    if sourcefile == f_dictionary[f]:
                        print "sourcefile:::", sourcefile, "dictionary:::", f_dictionary[f]
                        onefile.append(f)

        contentlist.append(count)
        linkedfile.append(onefile)

    get_tf_idf(contentlist)


def pre():
    bugidmap = open('data/BugidMap.txt', 'r')
    wordmap = open('data/WordMap.txt', 'r')
    filemap = open('data/FileMap.txt', 'r')
    bugids = bugidmap.readlines()
    dictionary = wordmap.readlines()
    files = filemap.readlines()
    bugidmap.close()
    wordmap.close()
    filemap.close()
    for d in dictionary:
        temp = d.replace('\n', '')
        w_dictionary.append(temp)
    for f in files:
        temp = f.replace('\n', '')
        f_dictionary.append(temp)
    for id in bugids:
        temp = id.replace('\n', '')
        id_dictionary.append(temp)


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

    data = []
    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        onefile = []
        for word, score in sorted_words[:15]:
            # words.append(word)
            for i in range(0, len(w_dictionary)):
                if word == w_dictionary[i]:
                    onefile.append(i)
        data.append(onefile)
    result = []
    print len(data)
    print len(linkedfile)
    reports = open('data/Reports.txt', 'w')
    for i in range(0, len(data)):
        result.append((linkedfile[i], data[i], ['aspectj'], 'compiler'))
    for r in result:
        print >> reports, r
    reports.close()



if __name__ == '__main__':
    main()