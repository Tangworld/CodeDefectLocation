import nltk
import string
from nltk.corpus import stopwords
import MySQLdb
def createSourceTXT():
    data = []
    source = open('source.txt', 'r')
    lines = source.readlines()
    source.close()
    db = MySQLdb.connect("localhost", "bugs", "bugs", "bugs")
    cursor = db.cursor()
    for line in lines:
        temp = []
        line = eval(line)

        for l in line:
            try:
                l = l.replace('\n', '')
                # print l
                # cursor.execute("insert into bugs(bug_id,assigned_to,bug_file_loc,bug_severity,bug_status,creation_ts,delta_ts,short_desc,op_sys,priority,product_id,rep_platform,reporter,version,component_id,everconfirmed) values(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s',%d,'%s',%d,%d)" % (id,1,fileloc,"enhancement","CONFIRMED",opendate,fixdate,summary,"Linux","Normal",2,"PC",2,"0.1",2,1))
                cursor.execute("select id from wordmap where word='%s'" % (l))
                result = cursor.fetchone()
                temp.append((int(result[0]), 100))
            except Exception, e:
                print e
                continue
        print temp
        data.append(temp)

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()
    source = open('source.txt', 'w')
    for d in data:
        print >> source, d
    source.close()
    print len(data)

if __name__ == "__main__":
    # main()
    createSourceTXT()