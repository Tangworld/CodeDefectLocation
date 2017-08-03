import random
import MySQLdb

def main():
    status =['open', 'unfixed', 'fixed']

    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()

    for i in range(2161, 3047):
        id = random.randint(0, 2)
        current_status = status[id]
        print current_status
        cursor.execute("update locator_report set status = '" + current_status + "'where id=" + str(i))
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()