import random
import MySQLdb
import time

def main():
    assignee = ['Roberto', 'Wes Isberg', 'Davi Pires', 'Andrew Clement', 'Abraham Nevado', 'Howard']
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()

    count = [0,0,0,0,0,0,0,0,0,0,0,0]
    cursor.execute("select fixdate from locator_report where assignee='" + assignee[5] + "'")
    dataset = cursor.fetchall()
    print len(dataset)
    for data in dataset:
        time_local = time.localtime(float(data[0]))
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        print dt, type(dt)
        month = int(dt.split('-')[1])
        count[month-1] += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()
    for c in count:
        print c

if __name__ == '__main__':
    main()