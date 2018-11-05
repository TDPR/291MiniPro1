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

    if res == '1':
        print('Offer a ride')
        from offerRides import rideInfo
        rideInfo(dbName, email)

    elif res == '2':
        print('Search rides')
        from searchRides import searchRides
        searchRides(dbName, email)

    elif res == '3':
        print('\nBooking Menu')
        from booking import bookingMenu
        bookingMenu(dbName, email)
        
    elif res == '4':
        print ('Post a ride request')
        from postRideReqs import postRideRequest
        postRideRequest(dbName, email)
    
    elif res == '5':
        print('Delete and search requests')
        from searchRequests import deleteOrSearchRequests
        deleteOrSearchRequests(dbName, email)

    elif res == '6':
        print('Logging Out')
        from login import loginMenu
        loginMenu(dbName)

    else:
        print('Invalid Input')
        mainMenu(dbName, email)

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
            print('From: ' + x[2] + ' | Sent: ' + x[1])
            print('Message: ' + x[3])
    else:
       print('\nNo New Messages')
