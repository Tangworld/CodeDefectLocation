import MySQLdb

def main():
    wordmap = open('WordMap.txt', 'r')
    lines = wordmap.readlines()
    wordmap.close()
    words = []
    for line in lines:
        line = line.replace('\n', '')
        words.append(line)
    finalwords = list(set(words))
    wordmap = open('WordMap.txt', 'w')
    for f in finalwords:
        print >> wordmap, f

def word_to_database():
    wordmap = open('WordMap.txt', 'r')
    lines = wordmap.readlines()
    wordmap.close()
    db = MySQLdb.connect("localhost", "bugs", "bugs", "bugs")
    cursor = db.cursor()
    cnt = 1
    for line in lines:
        line = line.replace('\n', '')
        # cursor.execute("insert into bugs(bug_id,assigned_to,bug_file_loc,bug_severity,bug_status,creation_ts,delta_ts,short_desc,op_sys,priority,product_id,rep_platform,reporter,version,component_id,everconfirmed) values(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s',%d,'%s',%d,%d)" % (id,1,fileloc,"enhancement","CONFIRMED",opendate,fixdate,summary,"Linux","Normal",2,"PC",2,"0.1",2,1))
        cursor.execute("insert into wordmap(id, word) values('%d', '%s')" % (cnt, line))
        cnt += 1
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

def file_to_database():
    filemap = open('FileMap.txt', 'r')
    lines = filemap.readlines()
    filemap.close()

    db = MySQLdb.connect("localhost", "bugs", "bugs", "bugs")
    cursor = db.cursor()
    cnt = 1
    for line in lines:
        line = line.replace('\n', '')
        # cursor.execute("insert into bugs(bug_id,assigned_to,bug_file_loc,bug_severity,bug_status,creation_ts,delta_ts,short_desc,op_sys,priority,product_id,rep_platform,reporter,version,component_id,everconfirmed) values(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s',%d,'%s',%d,%d)" % (id,1,fileloc,"enhancement","CONFIRMED",opendate,fixdate,summary,"Linux","Normal",2,"PC",2,"0.1",2,1))
        cursor.execute("insert into filemap(id, fileloc) values('%d', '%s')" % (cnt, line))
        cnt += 1
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

if __name__ == '__main__':
    file_to_database()