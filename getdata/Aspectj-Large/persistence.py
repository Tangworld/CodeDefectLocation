import MySQLdb

def bugidinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    bugidmap = open('data/BugidMap.txt', 'r')
    lines = bugidmap.readlines()
    bugidmap.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_bugidmap(bugidnumber, bugid) values('"+str(cnt)+"', '"+line+"')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

def fileinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    filemap = open('data/FileMap.txt', 'r')
    lines = filemap.readlines()
    filemap.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_filemap(filenumber, filepath) values('" + str(cnt) + "', '" + line + "')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

def reportinsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    reports = open('data/Reports.txt', 'r')
    lines = reports.readlines()
    reports.close()
    cnt = 0
    for line in lines:
        line = line.replace('\n', '')
        temp = eval(line)
        tempp = (temp[0], temp[1])
        cursor.execute("insert into locator_reports(reportnumber, content) values('" + str(cnt) + "', '" + str(tempp) + "')")
        cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

if __name__ == '__main__':
    reportinsert()