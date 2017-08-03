# -*- coding: UTF-8 -*-
import MySQLdb

def main():
    data = []
    input = open("../data/l2ss/aspectj.txt")
    lines = input.readlines()
    input.close()
    bugidmap = open('../data/bughunter/BugidMap.txt')
    d_lines = bugidmap.readlines()
    bugidmap.close()

    db = MySQLdb.connect("localhost", "root", "root", "locator")
    db.set_character_set('utf8')
    cursor = db.cursor()

    dictionary = []
    for d in d_lines:
        d = d.replace('\n', '')
        dictionary.append(d)
    cnt = 0
    for line in lines:
        temp = eval(line)
        priority = str(temp['pr'])
        opendate = str(temp['tm'])
        reporter = temp['rp']
        component = str(temp['cm'])
        tr = str(temp['tr'])
        fileloc = str(temp['ts'])
        # print reporter
        severity = str(temp['sv'])
        version = str(temp['vs'])
        keywords = str(temp['ws'])
        platform = str(temp['pf'])
        os = str(temp['os'])
        bugid = str(temp['id'])
        if bugid in dictionary:
            data.append(bugid)
            print reporter, opendate, component, version, platform, os, priority, severity,bugid
            cnt += 1
            # cursor.execute("INSERT INTO locator_report(reporter,opendate,component,version,platform,os,priority,severity,bugid)"
            #             " VALUES('"+reporter+"','"+opendate+"','"+component+"','"+version+"','"+platform+"','"+os+"','"+priority+"','"+severity+"','"+bugid+"')")

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()
    print cnt
    print len(data)
    data = list(set(data))
    common = open('../data/l2ss/common.txt', 'w')
    for d in data:
        print >> common, d
    common.close()

def update():
    dictionary = []
    input = open("../data/l2ss/common.txt", 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.replace('\n', '')
        dictionary.append(line)

    aspectj = open("../data/bughunter/aspectj.csv", 'r')
    data = aspectj.readlines()
    aspectj.close()

    db = MySQLdb.connect("localhost", "root", "root", "locator")
    db.set_character_set('utf8')
    cursor = db.cursor()

    for d in dictionary:
        for i in range(1, len(data)):
            currentid = data[i].split(',')[0]
            currentid = currentid.replace('\n', '')
            if d == currentid:
                temp = data[i].split(',')[4:-1]
                summary = temp[0]
                description = temp[1]
                summary = summary.replace('Summary:    ', '')
                summary = summary.replace("'", "''")
                description = description.replace("'", "''")
                print summary
                print description
                cursor.execute("update locator_report set summary = '"+summary+"' , description = '"+description+"'where bugid='"+d+"'")
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

def update_fullfilter():
    r_filter = []
    dictionary = []
    input = open("../data/l2ss/common.txt", 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.replace('\n', '')
        dictionary.append(line)

    aspectj = open("../data/l2ss/aspectjfullfilter.txt", 'r')
    data = aspectj.readlines()
    aspectj.close()
    for d in data:
        temp = eval(d)
        bugid = str(temp['id'])
        if bugid in dictionary:
            r_filter.append(d.replace('\n', ''))

    output = open('../data/l2ss/aspectjfullfilter2.txt', 'w')
    for r in r_filter:
        print >> output, r
    output.close()

if __name__ == "__main__":
    update()
