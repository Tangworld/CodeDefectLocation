
def main():
    resource = open('data/aspectj.csv', 'r')
    lines = resource.readlines()
    resource.close()

    files = []
    for i in range(1, len(lines)):
        print lines[i].split(',')[-1]
        temp = lines[i].split(',')[-1]
        temp = temp.replace('\n', '')
        temp = temp.replace('\r', '')
        temp = temp.replace(' ', '')
        files.append(temp)
    print len(files)
    r_files = list(set(files))
    print len(r_files)
    for f in r_files:
        print f

    filemap = open('data/FileMap.txt', 'w')
    for f in r_files:
        print >> filemap, f
    filemap.close()

if __name__ == '__main__':
    main()