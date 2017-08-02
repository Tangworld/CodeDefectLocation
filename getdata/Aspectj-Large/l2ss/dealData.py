# -*- coding: UTF-8 -*-
import MySQLdb

def main():
    input = open("aspectj.txt")
    lines = input.readlines()
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()

    cnt = 0

    for line in lines:
        temp = eval(line)
        priority = str(temp['pr'])
        opendate = str(temp['tm'])
        reporter = temp['rp']
        component = str(temp['cm'])
        tr = str(temp['tr'])
        fileloc = str(temp['ts'])
        print reporter
        severity = str(temp['sv'])
        version = str(temp['vs'])
        keywords = str(temp['ws'])
        platform = str(temp['pf'])
        os = str(temp['os'])
        bugid = str(temp['id'])
        #cursor.execute("INSERT INTO Report(reporter,opendate,fileloc,component,version,platform,os,priority,severity,bugid,keywords)"
        #               " VALUES("+reporter+","+opendate+","+fileloc+","+component+","+version+","+platform+","+os+","+priority+","+severity+","+bugid+","+keywords+")")
        print bugid
        cnt += 1
    print cnt

if __name__ == "__main__":
    main()