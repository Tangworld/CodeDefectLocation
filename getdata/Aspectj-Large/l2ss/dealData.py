# -*- coding: UTF-8 -*-
import MySQLdb

def main():
    input = open("../data/l2ss/aspectj.txt")
    lines = input.readlines()
    input.close()
    bugidmap = open('../data/bughunter/BugidMap.txt')
    d_lines = bugidmap.readlines()
    bugidmap.close()
    # db = MySQLdb.connect("localhost", "root", "root", "locator")
    # cursor = db.cursor()
    dictionary = []
    for d in d_lines:
        d = d.replace('\n', '')
        dictionary.append(d)
    cnt = 0

    for i in range(0, 1000):
        temp = eval(lines[i])
        bugid = str(temp['id'])
        if bugid in dictionary:
            print bugid
            cnt += 1
    # for line in lines:
    #     temp = eval(line)
    #     priority = str(temp['pr'])
    #     opendate = str(temp['tm'])
    #     reporter = temp['rp']
    #     component = str(temp['cm'])
    #     tr = str(temp['tr'])
    #     fileloc = str(temp['ts'])
    #     # print reporter
    #     severity = str(temp['sv'])
    #     version = str(temp['vs'])
    #     keywords = str(temp['ws'])
    #     platform = str(temp['pf'])
    #     os = str(temp['os'])
    #     bugid = str(temp['id'])
        #cursor.execute("INSERT INTO Report(reporter,opendate,fileloc,component,version,platform,os,priority,severity,bugid,keywords)"
        #               " VALUES("+reporter+","+opendate+","+fileloc+","+component+","+version+","+platform+","+os+","+priority+","+severity+","+bugid+","+keywords+")")

    # db.commit()  # Commit the transaction
    # cursor.close()
    # db.close()
    print cnt

if __name__ == "__main__":
    main()