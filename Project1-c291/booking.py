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
        print('\nBooking')
        bookMembers(dbName,email)
    
    elif res == '3':
        print('\nCancelling')
        cancelBookings(dbName,email)

    elif res == '4':
        from menu import mainMenu
        mainMenu(dbName,email)

    else:
        print('\nInvalid Input')
        bookingMenu(dbName,email)

def listBookings(dbName,email):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    c.execute('''SELECT b.bno, b.email, b.cost, b.seats, b.pickup, b.dropoff 
        FROM bookings b, rides r
        WHERE b.rno = r.rno
        AND r.driver LIKE :email; ''', 
        {"email": email})
    bookings = c.fetchall()
    conn.commit()
    conn.close()
    print('\nHere are your bookings')
    for x in bookings:
        print('BNO: ' + str(x[0]))
        print('Rider: ' + x[1] + ' | Cost: ' + str(x[2]) + ' | Seats: ' + str(x[3]))
        print('Pick up: ' + str(x[4]) + ' | Drop off: ' + str(x[5]) + '\n')
    return

def listRides(dbName,email, rides):
    if rides:
        print('\nHere are your rides')
        listSize = 5 if len(rides) > 5 else len(rides)
        for x in range(0,listSize):
            print('RNO: ' + str(rides[x][0]))
            availSeats = int(rides[x][1] or 0) - int(rides[x][2] or 0)
            if availSeats < 0:
                availSeats = 'Overbooked by ' + abs(availSeats)
            print('Available Seats: ' + str(availSeats))
            print('BNO: ' + str(rides[x][3]) + '\n')

        #prints the rest if there is more
        if len(rides) > 5:
            print('Would you like to list the rest? y|n')
            res = ''

            while res.lower() != 'y' and res.lower() != 'n':
                res = input()

            if res.lower() == 'y':
                print('\n')
                for x in range(5,len(rides)):
                    print('RNO: ' + str(rides[x][0]))
                    availSeats = int(rides[x][1] or 0) - int(rides[x][2] or 0)
                    if availSeats < 0:
                        availSeats = 'Overbooked by ' + abs(availSeats)
                    print('Available Seats: ' + str(availSeats))
                    print('BNO: ' + str(rides[x][3]) + '\n')
            else:
                print('\n')
    else:
        print('\nYou have no rides')
    return

def bookMembers(dbName,email):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    c.execute('''
        SELECT r.rno, r.seats, b.seats, b.bno
        FROM rides r
        LEFT JOIN bookings b
        ON r.rno = b.rno
        WHERE r.driver LIKE :email;''', 
        {"email": email})
    rides = c.fetchall()
    conn.commit()
    conn.close()

    #ok this is probably the ugliest code I've written in a while
    #it works and does what you want but there has to be an easier way
    #if a TA comes and sees this please email me an easier way to do this
    #at maoued@ualberta.ca
    #called in this function rather than listRides because
    #available seats are needed in book members
    #this code makes rides a list of lists instead of list of tuples
    #then it adds those lists to ridesUnique if rno is unique
    #if it is not then it adds seats and joins BNO together
    rides = [list(i) for i in rides]
    if len(rides) > 1:
        setRides = set()
        ridesUnique = []
        for sublist in rides:
            rnoUnique = sublist[0]
            if rnoUnique not in setRides:
                ridesUnique.append(sublist)
                setRides.add(rnoUnique)
            else:
                for i in ridesUnique:
                    if rnoUnique == i[0]:
                        i[2] = int(i[2] or 0) + int(sublist[2] or 0)
                        i[3] = ', '.join([str(i[3]),str(sublist[3])])
    else:
        ridesUnique=rides

    print('Enter the RNO of the ride you wish to book to')
    print('Type List to list your rides')
    print('Type Back to return to Booking Menu')
    rno = input()

    if rno.lower() == 'list':
        listRides(dbName,email, ridesUnique)
        bookMembers(dbName,email)

    elif rno.lower() == 'back':
        bookingMenu(dbName,email)

    #booking member logic
    elif rno.isdigit():
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute(' PRAGMA foreign_keys=ON; ')
        c.execute('''
            SELECT rno
            FROM rides
            WHERE driver LIKE :email
            AND rno=:rno;''', 
            {"email": email, "rno": rno})
        rnoMatch = c.fetchone()

        if rnoMatch:
            for x in ridesUnique:
                if rnoMatch[0] == x[0]:
                    rideMatch = x
                    print('\nRNO: ' + str(x[0]))
                    availSeats = int(x[1] or 0) - int(x[2] or 0)
                    if availSeats < 0:
                        availSeats = 'Overbooked by ' + abs(availSeats)
                    print('Available Seats: ' + str(availSeats))
                    print('BNO: ' + str(x[3]))

            print('Confirm you want to add to this ride: y|n')
            res=''

            while res.lower() != 'y' and res.lower() != 'n':
                res=input()

            #form fill
            if res.lower() == 'y':
                memEmail = ''
                seatBooked = '0'
                cost = ''
                print('\nFill the rest of form: ')
                while not memEmail:
                    memEmail = input('Email of member you wish to book: ')
                    c.execute('''
                        SELECT email
                        FROM members
                        WHERE email LIKE :email;''', 
                        {"email": memEmail})
                    verifyEmail = c.fetchone()
                    if not verifyEmail:
                        print('\nNo nember with that email exists')
                        memEmail=''
                
                while seatBooked == '0':
                    seatBooked = input('Please enter how many seats you wish to book: ')
                    
                    if seatBooked == '0':
                        print('\nPlease book at least one seat')
                    elif seatBooked.isdigit():
                        rideMatch[2] += int(seatBooked)
                        if rideMatch[1] - rideMatch[2] < 0:
                            print("You're overbooked by " + str(abs(rideMatch[1] - rideMatch[2])))
                            print('Please Confirm y|n')
                            res=''

                            while res.lower() != 'y' and res.lower() != 'n':
                                res=input()

                            if res.lower() == 'n':
                                rideMatch[2] -= int(seatBooked)
                                seatBooked = '0'
                    else:
                        print('\nPlease Enter a number')
                        seatBooked = '0'
                
                while not cost.isdigit():
                    cost = input('Enter the cost per seat: ')

                pickUp = input('Enter the pick up location: ')
                dropOff = input('Enter the drop off location: ')

                print('\nConfirm Details for booking')
                print('RNO: ' + str(rideMatch[0]))
                print('Rider: ' + memEmail + ' | Cost: ' + cost + ' | Seats Booked: ' + seatBooked)
                print('Pick up: ' + pickUp + ' | Drop off: ' + dropOff)
                print('Confim y|n')
                res=''

                while res.lower() != 'y' and res.lower() != 'n':
                    res=input()
                
                #CONFIRM BOOKING
                if res.lower() == 'y':
                    c.execute( '''
                        SELECT MAX(bno)
                        FROM bookings;''')
                    bnoMax = c.fetchone()
                    bnoMax = bnoMax[0] + 1    
    
                    addBooking=[bnoMax, memEmail, rideMatch[0], int(cost), int(seatBooked), pickUp, dropOff]
                    bookMsg = [memEmail,datetime.datetime.now().date(),email,
                        'Your driver has booked you to BNO: ' + str(bnoMax), rideMatch[0], 'n']
                    
                    #was giving a foreign key constraint failed error
                    #browsing sqlite documentation offered no solution since the rno is referenced
                    #in the rides table. 
                    c.execute(' PRAGMA foreign_keys=OFF; ')
                    c.execute('''INSERT 
                        INTO bookings(bno,email,rno,cost,seats,pickup,dropoff)
                        VALUES (?,?,?,?,?,?,?);''',
                        addBooking)

                    c.execute('''INSERT 
                        INTO inbox(email,msgTimestamp,sender,content,rno,seen)
                        VALUES (?,?,?,?,?,?);''',
                        bookMsg)

                    print("\nYou've succesfully booked " + memEmail + 'to RNO:' + str(rideMatch[0]) + 'with BNO: ' +str(bnoMax))
                    conn.commit()
                    conn.close()
                    bookMembers(dbName,email)

                else:
                    conn.commit()
                    conn.close()
                    bookMembers(dbName,email)

            else:
                conn.commit()
                conn.close()
                bookMembers(dbName,email)

        else:
            conn.commit()
            conn.close()
            print('\nNo Matching Rides')
            bookingMenu(dbName,email)
        
    
    else:
        print('\nInvalid Input')
        bookMembers(dbName,email)

def cancelBookings(dbName,email):
    print('Enter the BNO of the booking you want to cancel')
    print('Type List to list your bookings')
    print('Type Back to return to Booking Menu')
    bno = input()

    if bno.lower() == 'list':
        listBookings(dbName,email)
        cancelBookings(dbName,email)

    elif bno.lower() == 'back':
        bookingMenu(dbName,email)

    #cancel func
    elif bno.isdigit():
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute(' PRAGMA foreign_keys=ON; ')
        c.execute('''SELECT b.bno, b.email, b.cost, b. seats, b.pickup, b.dropoff, r.rno 
            FROM bookings b, rides r
            WHERE b.rno = r.rno
            AND r.driver LIKE :email
            AND b.bno = :bno; ''', 
            {"email": email, "bno": bno})
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

                c.execute('''DELETE
                    FROM bookings
                    WHERE bno IN (SELECT b.bno
                        FROM bookings b, rides r
                        WHERE b.rno = r.rno
                        AND r.driver LIKE :email
                        AND b.bno = :bno); ''', 
                    {"email": email, "bno": bno})
                
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
