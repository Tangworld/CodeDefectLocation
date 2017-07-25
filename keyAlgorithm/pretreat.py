# coding : UTF-8
import xml.dom.minidom as xdom
import time
import nltk
import codecs
import numpy as np
import random
import json
import os
from math import log
from gensim import corpora, models, similarities
import re

wordsByFrequency = open("words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(wordsByFrequency)))) for i,k in enumerate(wordsByFrequency))
maxword = max(len(x) for x in wordsByFrequency)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return out
    
class BugCollector:
    
    def __init__(self,file):
        self.dict = []
        self.matrixBR = []
        self.matrixS = []
        self.bugReports = []
        self.sourceFiles = []
        self.links = {}
        self.linksEX = {}
        self.bugReportHash = []
        self.sourceFilesHash = {}
        self.file = file
        self.readFile()
        self.d = {}
        self.hasS = []

    
    
    def readFile(self):
        dom = xdom.parse(self.file)
        root = dom.documentElement
        bugxml = root.getElementsByTagName('bug')
        
        sourceFileIndex = 0
        bugReportIndex = 0
        for bug in bugxml:
            bugreport = bug.getElementsByTagName('buginformation')[0]
            bugId = bug.getAttribute('id')
            opendate = bug.getAttribute('opendate')
            fixdate = bug.getAttribute('fixdate')
            summary = bugreport.getElementsByTagName('summary')[0]
            descri = bugreport.getElementsByTagName('description')[0]
            summ = summary.firstChild.data if type(summary.firstChild) != type(None) else ''
            des = descri.firstChild.data if type(descri.firstChild) != type(None) else ''
            self.bugReports.append(summ + des)

            # print "bugreport:",self.bugReports
            self.bugReportHash.append(bugId)
            self.links[bugReportIndex] = []
            
            fixedFiles = bug.getElementsByTagName('fixedFiles')[0]
            files = fixedFiles.getElementsByTagName('file')

            fileexists = 0
            for file in files:
                fileName = file.firstChild.data
                #token = fileName.split('.')
                # filepath = 'buggy/'+fileName.replace(r'/','.')
                filepath = '/var/www/html/bugzilla/'+fileName
                print filepath
                if not os.path.isfile(filepath):
                    continue
                fileexists += 1
                sourceFile = 0
                if not self.sourceFilesHash.has_key(fileName):
                    self.sourceFiles.append(fileName)
                    self.sourceFilesHash[fileName] = sourceFileIndex
                    sourceFile = sourceFileIndex
                    sourceFileIndex += 1
                else:
                    sourceFile = self.sourceFilesHash[fileName]
                    
                self.links[bugReportIndex].append(sourceFile)
                if self.linksEX.has_key(sourceFile):
                    self.linksEX[sourceFile].append(bugReportIndex)
                else:
                    self.linksEX[sourceFile] = []
                    self.linksEX[sourceFile].append(bugReportIndex)
            if fileexists == 0:
                self.bugReports.pop()
                self.bugReportHash.pop()
                del self.links[bugReportIndex]
                continue       
            bugReportIndex = bugReportIndex + 1
        print "bugreports2:",self.bugReports

            
            
        
    
    def nltkMatrix(self):
        stemmer = nltk.stem.porter.PorterStemmer()
        stopword = set(nltk.corpus.stopwords.words('english'))
        skeywords = []
        f = codecs.open('keywords.txt',encoding='UTF-8')
        line = f.readline()
        print "line:",line
        while line:
            stopword.add(line[:-1])
            line = f.readline()
        f.close()
        tokenizer = nltk.tokenize.RegexpTokenizer(r'[A-Za-z]+')
        globalDict = nltk.FreqDist()

        f = open("aspectjtf.txt","w")
        index = 1
        print self.bugReports
        for report_index in xrange(len(self.bugReports)):

            '''
            pattern = r'(org|sun)(\.[a-zA-Z_0-9]+)+'
            ret  = re.search(pattern, report)
            retnum = 0
            while ret != None:
                retnum += 1
                ret = re.search(pattern, report[ret.span()[1]:])
                if retnum > 2:
                    self.hasS.append(index-1)
                    print >> f, (index-1)
                    break
            '''
            tokens = tokenizer.tokenize(self.bugReports[report_index])
            words = [token.lower() for token in tokens if token.lower() not in stopword and len(token) > 2]
            s = []
            for word in words:
                infered = infer_spaces(word)
                if len(infered) > 1:
                    s.append(word)
                s.extend(infered)
            #words = infer_spaces(s)
            words = [stemmer.stem(ss) for ss in s]
            #[globalDict.inc(word) for word in words]
            
            sourcen = []
            for source in self.links[report_index]:
                name = self.sourceFiles[source]
                name = name.replace(r'/','.')
                sourcen.append(name)
            print >> f , (sourcen, " ".join(words))


            self.matrixBR.append(words)
            self.dict.extend(words)
            
            # print 'bug report:',index
            index += 1
        f.close()
        exit()
        print len(self.hasS)
        sourcedic = {}
        index = 0
        nofile = 0
        sourcelen = []
        asfile = open("tfaspectj.txt","w")
        for source in self.sourceFiles:
            sourcetext = []
            
            basepath = '../data/'
            path = basepath + source
            r = ''
            if os.path.isfile(path):
                file = open(path)
                r = file.read()
            else:
                nofile += 1
                print 'missing file',source
                continue
            
            
            code, anno = " "," "
            # anno
            words = tokenizer.tokenize(anno)
            words = [token.lower() for token in words if token.lower() not in stopword and len(token) > 3]
            words = [stemmer.stem(word) for word in words]
            words = [token.lower() for token in words if token.lower() not in stopword and len(token) > 3]
            sourcetext.extend(words)
            
            # code
            sourcelen.append(len(code.split('\n')))
            words = tokenizer.tokenize(code)
            words = [token.lower() for token in words if token.lower() not in stopword and len(token) > 3]
            s = []
            for word in words:
                infered = infer_spaces(word)
                if len(infered) > 1:
                    s.append(word)
                s.extend(infered)
            #words = infer_spaces(s)
            words = [stemmer.stem(word) for word in s]
            words = [token.lower() for token in words if token.lower() not in stopword and len(token) > 3]
            sourcetext.extend(words)
            
            
            self.matrixS.append(sourcetext)
            self.dict.extend(words)
            ss = source.replace(r'/','.')
            token = ss.split('org')
            ss = 'org'+token[-1]
            sourcedic[index] = ss
            
            print 'source file:',index
            index += 1
        
        f = open("sourcelen.txt","w")
        print >> f, sourcelen
        f.close()
        print 'nofile num',nofile
        file = open('./sourcedic.json','w')
        file.write(json.dumps(sourcedic,encoding='UTF-8',ensure_ascii=False))
        file.close()
        self.dict = sorted(set(self.dict))

    def getMatrixBR(self):
        return self.matrixBR        

    def getMatrixS(self):
        return self.matrixS

    def getLinks(self):
        return self.links

    def doTest(self):
        matrixBR = self.matrixBR
        matrixS = self.matrixS
        
        #print int(1/10.0*len(matrixBR)+1)
        S = set()
        for d in matrixS:
            S = S | set(d)
        for d in matrixBR:
            S = S | set(d)
            
        dic = list(S)
        print len(dic)
        dict = {}
        for i in range(len(dic)):
            dict[dic[i]] = i
        BR = []
        S = []
        for d in matrixBR:
            BR.append([])
        for d in range(len(matrixBR)):
            for z in range(len(matrixBR[d])):
                BR[d].append(dict[matrixBR[d][z]])
        for d in matrixS:
            S.append([])
        for d in range(len(matrixS)):
            for z in range(len(matrixS[d])):
                S[d].append(dict[matrixS[d][z]])
        '''
        file = open('./wordResults.txt',"w")
        x = []
        for d in xrange(len(BR)):
            lis = []
            for s in self.links[d]:
                for si in S[s]:
                    if si in BR[d]:
                        if si not in lis:
                            lis.append(si)
            print >> file, (len(lis), lis)
            x.append(len(lis))
        file.close()
        print sum(x)/len(x)
        '''
        file = open("AspectJDataset.txt","w")
        g = open("AspectJBfig.txt","w")
        for d in xrange(len(BR)):
            print >> file, (self.links[d], BR[d])
            wordsInS = []
            wordsInBoth = {}
            for s in self.links[d]:
                wordsInS.extend(S[s])
            
            for w in BR[d]:
                if w in wordsInS:
                    wordsInBoth[w] = 1 + wordsInBoth.get(w,0)
            print >> g, len(wordsInBoth.items())
        file.close()
        g.close()
        
        file = open("AspectJSource.txt","w")
        g = open("AspectJSfig.txt","w")
        for s in xrange(len(S)):
            wordsInS = []
            wordsInBoth = {}
            for d in self.linksEX[s]:
                wordsInS.extend(BR[d])
            
            for w in S[s]:
                if w in wordsInS:
                    wordsInBoth[w] = 1 + wordsInBoth.get(w,0)
           
            sortedWord = sorted(wordsInBoth.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
            print >> file, sortedWord[:50]
            print >> g, len(sortedWord)
        file.close()
        g.close()
        
        stb = []
        f = open("splited.txt","r")
        for l in f:
            x = eval(l)
            stb.append(x)
        f.close()
        # genetare VSM input
        dictionary = corpora.Dictionary(matrixBR+matrixS)
        dictionary.save("VSMdictionary.txt")
        
        docBR = []
        docSF = []
        for d in matrixBR:
            docBR.append(dictionary.doc2bow(d))
        for d in matrixS:
            docSF.append(dictionary.doc2bow(d))
            
        lBR = len(docBR)
        lSF = len(docSF)
        notthis = {}
        inthis = {}
        allthis = set([])
        for x in xrange(10):
            notthis[x] = set([])
            inthis[x] = set([])
        for x in xrange(lBR):
            fold = x % 10
            notthis[fold] = notthis[fold] | set(self.links[x])
        for x in xrange(10):
            allthis = allthis | notthis[x]
        for x in xrange(10):
            for y in xrange(10):
                if y != x:
                    inthis[x] = inthis[x] | notthis[y]
        #print inthis[0]   
        tfidf = models.TfidfModel(docBR+docSF)
        index = similarities.SparseMatrixSimilarity(docBR+docSF, num_features = len(dic))
        hit5,hit10,hit20 = 0.0,0.0,0.0
        p5,p10,p20 = 0.0,0.0,0.0
        r5,r10,r20 = 0.0,0.0,0.0
        sthit = 0.0
        fhit = 0.0
        for d in xrange(len(docBR)):
            fold = d % 10
            #if d in self.hasS:
                #continue
            sims = list(enumerate(index[docBR[d]]))
            sims = sorted(sims,key=lambda x : x[0], reverse = True)[:lSF]
            #print sims
            s = sorted(sims, key=lambda x : x[1], reverse = True)
            count = 0
            h5,h10,h20 = 0.0,0.0,0.0
            findex = -1
            for item in s:
                findex += 1
                if item[0]-lBR in inthis[fold]:
                    if item[0]-lBR in self.links[d]:
                        break
            fhit += findex
            #print findex
            for item in s:
                if count >= 20:
                    break
                if item[0]-lBR in inthis[fold]:
                    if item[0]-lBR in self.links[d]:
                        #print item[0]-lBR, self.links[d]
                        if count < 5:
                            h5 += 1
                        if count < 10:
                            h10 += 1
                        h20 += 1
                    count += 1
                
                    
            #print h5,h10,h20, len(self.links[d])
            r5 += h5/len(self.links[d])
            r10 += h10/len(self.links[d])
            r20 += h20/len(self.links[d])
            p5 += h5/5
            p10 += h10/10
            p20 += h20/20
            
            if h5 > 0:
                hit5 += 1
            if h10 > 0:
                hit10 += 1
            if h20 > 0:
                hit20 += 1
                if d in stb:
                    sthit += 1
        nsthit = (hit20 - sthit)/(len(docBR)-len(stb))
        sthit /= len(stb)
        fhit /= lBR
        hitlen = lBR# - len(self.hasS)
        print "hit@5:%.4f hit@10:%.4f hit@20:%.4f" % (hit5/hitlen, hit10/hitlen, hit20/hitlen)
        print "recall@5:%.4f recall@10:%.4f recall@20:%.4f" % (r5/hitlen, r10/hitlen, r20/hitlen)
        print "precision@5:%.4f precision@10:%.4f precision@20:%.4f" % (p5/hitlen, p10/hitlen , p20/hitlen)
        print sthit, nsthit
        print lBR
        '''
        file = open('./BugReports.data','w')
        for d in BR:
            file.write(','.join(d))
            file.write('\n')
        file.close()
        
        file = open('./SourceFiles.data','w')
        for d in S:
            file.write(','.join(d))
            file.write('\n')
        file.close()
        
        file = open('./dict.json','w')
        file.write(json.dumps(dict,encoding='UTF-8',ensure_ascii=False))
        file.close()
        file = open('./link_S-BR.json','w')
        file.write(json.dumps(self.linksEX,encoding='UTF-8',ensure_ascii=False))
        file.close()
        file = open('./link_BR-S.json','w')
        file.write(json.dumps(self.links,encoding='UTF-8',ensure_ascii=False))
        file.close()
        '''
        
        return
        
def main():

    bug = BugCollector('AspectJBugRepository.xml')
    bug.nltkMatrix()

    bug.doTest()
    # bug.test()


if __name__ == '__main__':
    main()
