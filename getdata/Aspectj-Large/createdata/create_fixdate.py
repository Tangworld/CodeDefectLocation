import time
import random
import MySQLdb

def main():
    date = []
    year = '2017'
    month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']
    hour = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    minute = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    second = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    for m in month:
        for d in day:
            for h in hour:
                for mi in minute:
                    for s in second:
                        temp = year +'-'+ m +'-'+ d +' '+ h +':'+ mi + ':' + s
                        date.append(temp)

    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()

    print len(date)
    for i in range(2161, 3047):
        id = random.randint(0, 3628800)
        current_date = date[id]
        timestamp = time.mktime(time.strptime(current_date, '%Y-%m-%d %H:%M:%S'))
        int_timestamp = int(timestamp)
        print int_timestamp, current_date
        cursor.execute("update locator_report set fixdate = '" + str(int_timestamp) + "'where id=" + str(i))
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()