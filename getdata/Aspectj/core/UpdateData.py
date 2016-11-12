#!/home/tsj/PycharmProjects/CodeDefectLocation/getdata/Aspectj
# -*- coding: utf-8 -*-
# encoding=utf-8
import MySQLdb


def update():
    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()
    cursor.execute('select * from aspectj')
    dataset1 = cursor.fetchall()
    print type(dataset1)
    cursor.execute("select * from assist")
    dataset2 = cursor.fetchall()
    for i in dataset1:
        idd = i[1]
        for j in dataset2:
            if j[1] == idd:
                print j
                des = i[11]
                ori = i[2]
                sta = i[9]
                if (des is None) or (ori is None) or (sta is None):
                    continue
                cursor.execute("update assist set original = '"+ori+"' ,description = '"+des+"', status='"+sta+"'")

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

def minor():
    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()
    cursor.execute("select * from assist")
    dataset = cursor.fetchall()
    cursor.close()
    db.close()
    dataset = list(dataset)
    for i in range(0, 2480, 1):
        dataset[i] = list(dataset[i])
    for i in range(0, 2480, 1):
        j = i+1
        while j < 2480:
            # print dataset[j][1]
            if dataset[j][1] == dataset[i][1]:
                # print dataset[j]
                dataset[j][1] = "000000"
            j += 1
    print dataset.__len__()
    # for i in range(0,2480,1):
    #     print dataset[i]
    for i in range(0, 2480, 1):
        if dataset[i][1] == "000000":
            db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
            cursor = db.cursor()
            cursor.execute("update assist set bugid = '000000' where id='%s'" % dataset[i][0])
            db.commit()  # Commit the transaction
            cursor.close()
            db.close()


if __name__ == "__main__":
    minor()