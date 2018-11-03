import sqlite3
import datetime

def bookingMenu(dbName, email):
    print('Control this menu using numbers')
    print('1.List Bookings')
    print('2.Book Members')
    print('3.Cancel Bookings')
    print('4.Go back to the Main Menu')
    res = input()

    if res == '1':
        listBookings(dbName, email)
        bookingMenu(dbName,email)
    
    elif res == '2':
        print('2')
    
    elif res == '3':
        print('\nCancelling')
        cancelBookings(dbName,email)

    elif res == '4':
        from menu import mainMenu
        mainMenu(dbName,email)

    else:
        print('Invalid Input\n')
        bookingMenu(dbName,email)

def listBookings(dbName,email):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    c.execute('''SELECT b.bno, b.email, b.cost, b. seats, b.pickup, b.dropoff 
        FROM bookings b, rides r
        WHERE b.rno = r.rno
        AND r.driver LIKE :email; ''', 
        {"email": email})
    bookings = c.fetchall()
    conn.commit()
    conn.close()
    print(bookings)
    print('\nHere are your bookings')
    for x in bookings:
        print('BNO: ' + str(x[0]))
        print('Rider: ' + x[1] + ' | Cost: ' + str(x[2]) + ' | Seats: ' + str(x[3]))
        print('Pick up: ' + str(x[4]) + ' | Drop off: ' + str(x[5]) + '\n')
    return

def bookMembers(dbName,email):
    return

def cancelBookings(dbName,email):
    print('Enter the BNO of the booking you want to cancel')
    print('Type List to list your bookings')
    print('Type Back to return to Booking Menu')
    res = input()

    if res.lower() == 'list':
        listBookings(dbName,email)
        cancelBookings(dbName,email)

    elif res.lower() == 'back':
        bookingMenu(dbName,email)

    #cancel func
    elif res.isdigit():
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute(' PRAGMA foreign_keys=ON; ')
        c.execute('''SELECT b.bno, b.email, b.cost, b. seats, b.pickup, b.dropoff, r.rno 
            FROM bookings b, rides r
            WHERE b.rno = r.rno
            AND r.driver LIKE :email
            AND b.bno = :bno; ''', 
            {"email": email, "bno": res})
        bookings = c.fetchone()
        
        #bno exists
        if bookings:
            print('\nPlease confirm this is the booking you want to cancel')
            print('BNO: ' + str(bookings[0]))
            print('Rider: ' + bookings[1] + ' | Cost: ' + str(bookings[2]) + ' | Seats: ' + str(bookings[3]))
            print('Pick up: ' + str(bookings[4]) + ' | Drop off: ' + str(bookings[5]) + '\n')
            print('Confim y|n')
            res=''

            while res.lower() != 'y' and res.lower() != 'n':
                res=input()
            
            #Confirm
            if res.lower() == 'y':
                cancelMsg = [bookings[1],datetime.datetime.now().date(),email,
                    'Your driver has cancelled the booking with BNO: ' + str(bookings[0]), bookings[6], 'n']

                c = conn.cursor()
                c.execute(' PRAGMA foreign_keys=ON; ')
                #TODO fix this query search doesn't work just yet
                c.execute('''DELETE
                    FROM bookings
                    WHERE bno IN (SELECT b.bno
                        FROM bookings b, rides r
                        WHERE b.rno = r.rno
                        AND r.driver LIKE :email
                        AND b.bno = :bno); ''', 
                    {"email": email, "bno": res})
                print('Hello World')
                c.execute('''INSERT 
                    INTO inbox(email,msgTimestamp,sender,content,rno,seen)
                    VALUES (?,?,?,?,?,?);''',
                    cancelMsg)
                
                conn.commit()
                conn.close()
                print('\nYour booking with BNO: ' + str(bookings[0]) + ' has been cancelled\n')
                cancelBookings(dbName,email)
            else:
                print('\n')
                cancelBookings(dbName,email)

        #booking not found
        else:
            conn.commit()
            conn.close()
            print("\nCouldn't find that booking number, Please try again")
            cancelBookings(dbName,email)

    else:
        print('Invalid Input')
        cancelBookings(dbName,email)
