import sqlite3

def mainMenu(dbName, email):
    getMessages(dbName, email)

    print('\nControl this menu using numbers')
    print('1. Offer a ride')
    print('2. Search for rides')
    print('3. Book members or cancel bookings')
    print('4. Post ride requests')
    print('5. Search and delete ride requests')
    print('6. Log Out')
    res = input()
    if res == '6':
        print('Logging Out')
        from login import loginMenu
        loginMenu(dbName)

def getMessages(dbName, email):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    c.execute('''SELECT * 
        FROM inbox
        WHERE email LIKE :email
        AND seen= 'n'; ''', 
        {"email": email})
    inbox = c.fetchall()
    c.execute('''UPDATE inbox
        SET seen = 'y'
        WHERE seen = 'n'
        AND email Like :email;''',
        {"email": email})
    conn.commit()
    conn.close()
    if inbox:
        print('\nNew Messages:')
        for x in inbox:
            print('From: ' + x[2])
            print('Message: ' + x[3])
    else:
       print('\nNo New Messages') 