import random
import MySQLdb

def main():
    assignee =['Roberto', 'Wes Isberg', 'Davi Pires', 'Andrew Clement', 'Abraham Nevado', 'Howard']

    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()

    for i in range(2161, 3047):
        id = random.randint(0, 5)
        current_assignee = assignee[id]
        print current_assignee
        cursor.execute("update locator_report set assignee = '" + current_assignee + "'where id=" + str(i))
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()