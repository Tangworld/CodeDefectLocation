
def main():
    filemap = open('data/FileMap.txt', 'r')
    files = filemap.readlines()
    filemap.close()

    lens = []
    for file in files:
        file = file.replace('\n', '')
        try:
            source = open('/home/tsj/PycharmProjects/CodeDefectLocation/keyAlgorithm/'+file, 'r')
            lines = source.readlines()
            lens.append(len(lines))
            print len(lines)
        except Exception, e:
            print e
            lens.append(0)
            continue

    print len(lens)
    print lens
    SourceLen = open('data/SourceLen.txt', 'w')
    print >> SourceLen, lens
    SourceLen.close()



if __name__ == '__main__':
    main()