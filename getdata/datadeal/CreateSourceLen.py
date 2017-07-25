def main():
    try:
        cnt = 0
        lengths = []
        pre = "/var/www/html/bugzilla/"
        input = open("FileMap.txt","r")

        lines = input.readlines()
        input.close()
        print len(lines)
        for line in lines:
            print "line:",line
        # while line:
            cnt += 1
            line = line.replace('\n','')
            # print >> test,line
            # print line
            filename = pre + line
            myfile = open(filename,"r")
            linenum = myfile.readlines()
            # print line
            # print len(linenum)
            lengths.append(len(linenum))
        #     line = input.readline()

    except Exception, ex:
        print ex
        lengths.append(0)
    print "cnt:",cnt
    return lengths

if __name__ == "__main__":
    result = main()
    test = open("sourceLen.txt", "a")
    for length in result:
        print >> test,length
    test.close()
    print len(result)
    # arr = []
    # test = open("sourceLen.txt","r")
    # test2 = open("test.txt","w")
    # temp = test.readlines()
    # for t in temp:
    #     num = int(t)
    #     arr.append(num)
    # print >> test2,arr
    # test.close()
    # test2.close()
    # test3 = open("sourceLen.txt","w")
    # print >> test3,arr
    # test3.close()
