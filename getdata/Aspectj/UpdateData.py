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

if __name__ == "__main__":
    update()