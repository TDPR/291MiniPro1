import sqlite3
import datetime


#This function checks date input to make sure it is in a valid YYYY-MM-DD date format
def dateCheck():
    
    for x in range (0, 3):
        rdate = input('When will the ride be? (YYYY-MM-DD): ')
        if (len(rdate.split('-')) < 3 or len(rdate.split('-')) > 3):
            if x == 2:
                print('The you have entered the wrong date 3 times. Ride Date will be left blank.' )  
            print('The date that you entered is incorrect. Please try again')
            print('You have ' + str(2-x) +' tries available. Or it will be left blank')
        else:
            try:
                datetime.datetime.strptime(rdate,'%Y-%m-%d')
                break
            except ValueError:
                print('The date format you entered is incorrect. Please enter date in YYYY-MM-DD format.')
       
    return rdate

##This function generates a unique RNO for every ride offered
def maxRno(dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
   
    c.execute( '''
                SELECT MAX(rno)
                FROM rides;
                ''')
    n = c.fetchone()
    n = n[0] + 1    
    
    return n

#This function checks to make sure the car number entered is registered to the member offering a ride
#It also checks seat number input and corrects seat input if member entered incorrectly
def cnoMatch(carNum, email, seats1, dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    c.execute('''
                        SELECT cno 
                        from cars
                            ''')
    c.fetchall()
    
    c.execute('''
                SELECT cno, make, model, year, owner
                FROM cars
                LEFT JOIN  members on owner = email
                where email =  ?''', [email])
    cnoResult = c.fetchall() 
    
    myCno = []
    
    for each in cnoResult:
        myCno += [each[0]]
    
    
    if not int(carNum) in myCno:
        while(True):
            print('The CNO you entered does not match your registered cars. \nPlease try again or type \'exit\' to leave CNO blank')
            print(cnoResult)
            cnoRecheck = input('What is your CNO? ')
            if cnoRecheck == 'exit':
                print('CNO will be set to null.')
                cno = None
                seatsSend = seats1
                break
            elif cnoRecheck.isdigit():
                if int(cnoRecheck) in myCno:
                    cno = cnoRecheck
                    break
    else:
        cno = carNum  
    if cnoRecheck != 'exit': 
        c.execute('''
                                SELECT seats
                                FROM cars
                                where cno = ? ''',[cno])
        seatsResult = c.fetchall()
        print('The correct number of seats in your car is: ', seatsResult[0][0])
        seatsCheck = seatsResult[0][0]
        if seats1 < seatsCheck:
            print('You have ' + str(seatsCheck-seats1) + ' seats still available.')
            seatsAsk = input('Would you like to adjust the number of seats you are offering? (Y/N):')
            if seatsAsk.startswith('n' or 'N'):
                print('Your offered seats will not be adjusted.')
                seatsSend = seats1
            elif seatsAsk.startswith('y' or 'Y'):
                seats1 = int(input('What is your seat number?: '))
                while seats1 > seatsCheck:
                    print('The value you entered is too high. Please enter a number lower than ' + str(seatsResult[0][0]))
                    seats1 = int(input('What is your seat number?: '))

        elif seats1 > seatsResult[0][0]:
            while seats1 > seatsCheck:
                print('You have entered ' + str(seats1) +'. The number of seats you have entered are more than the seats you have.')
                seats1 = int(input('Please input a value less than or equal to ' + str(seatsResult[0][0]) + ': '))
    
        seatsSend = seats1

    return cno, seatsSend

#This function allows members to search for lcode using keywords (city, prov, or address)
#It also allows members to scroll through lcodes if there are more than 5 associated with the keyword
def locationSearch(dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    offsetValue = 0
    
    loca = ""
    
    c.execute('''
                SELECT lcode
                FROM locations
                ''')
    lcodeList = c.fetchall()
 
    loca2 = input('Please enter your keyword (city, province, or address) to find lcode: ')
     
    loca3 = '%' + loca2 + '%'
    while(True):
        c.execute( '''
                    SELECT *
                    FROM locations
                    WHERE city LIKE ?
                    OR prov LIKE ?
                    OR address LIKE ?
                    GROUP BY lcode
                    ORDER BY lcode DESC
                    LIMIT 5 OFFSET ?;
                    ''', [loca3, loca3, loca3, offsetValue])
        results = c.fetchall()
    
        for each in results:
            print(each)
            
        check2 = input('''If you see the correct lcode please enter it. \nIf not, type "next", or type "exit" to leave blank.\n**(If you entered incorrectly type "change" to view new queries.)** \n ''')
    
        if (check2,) in lcodeList:
            loca = check2
            False
            break
        elif check2.lower() == 'next':
            offsetValue = offsetValue + 5
        elif check2.lower() == 'exit':
            loca = None
            False
            break
        elif check2 == 'change':
            loca3 = input('What is your keyword?: ')
            
        else:
            print('Your choice is invalid.')
     
    return loca

#This function enters ride information into the ride table
def insertRides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno, dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    #this SQL query enters ride information into the ride table  
    c.execute('''
                        INSERT INTO rides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
                        ''', [rno, price, rdate, seats, lugDesc, src, dst, driver, cno])
    
    
    print('Your ride offer has been added.')
    conn.commit()
    return

#This function enters enroute information into the ride table
def insertEnroute(rno, lcode, dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    #this SQL query enters each of the enroute destinations as separate tuples into the table
    for each in lcode:      
        c.execute('''
                                INSERT INTO enroute(rno, lcode)
                                VALUES(?, ?)    
                                ''', [rno, each])
    
    print('Your enroute info has been added.')
    conn.commit()
    return

#This is the primary ride offer function. Here members are prompted to insert information about their ride
#This function calls all of the helper functions associated with ride info
def rideInfo(dbName, email):
    from menu import mainMenu
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    #allows user to leave before they start
    print('Welcome to offer rides.')
    while(True):
        cont = input('Type \'y\' to continue or \'n\' to return to main menu. ')
        if cont.startswith('n' or 'N'):
            print('Bye Bye.')
            mainMenu(dbName, email)
            False
            break
        elif cont.startswith('y' or 'Y'):
            ('Please begin.')
            False
            break
        else:
            print("Please enter either \'Y\' or \'N\'.")

    #accepts user input for date and checks that it is correct
    rdate = dateCheck()
  
    #user inputs info for seats, ppseat, lugagge
    while(True):
        try:
            seats1 = int(input('How many seats are available?: '))
        except ValueError:
            print('Please enter a whole number (integer).')
        else:
            False 
            break

    while(True):
        try:        
            ppseat = int(input('How much will you charge per seat?: '))
        except ValueError:
            print ('Please enter amount as a whole number.')
        else:
            False
            break
    
    luggage = input('What luggage can riders bring?: ')
    
    #user keyword is checked against existing lcodes
    print('Please enter your start location as an lcode or keyword.')
    src = locationSearch(dbName)
    
    #user keyword is checked against existing lcodes
    print('Please enter your end location as an lcode or keyword.')
    dst = locationSearch(dbName)
    
    #user inputed CNO is checked to ensure car is registered to user 
    while(True):
        cnoAsk = input('Do you have a car number (CNO)? (Y/N) ')
        if cnoAsk.startswith('n' or 'N'):
            print('Your CNO and seats will be left blank.')
            #cnoB = None
            cnoB = None
            seats2 = seats1
            False
            break
        elif cnoAsk.startswith('y' or 'Y'):
            cnoA = input('What is your cno?: ')
            cnoB, seats2 = cnoMatch(cnoA, email, seats1, dbName)
            False
            break
        else:
            print("Please enter either \'Y\' or \'N\'.")
        
    #enroute the locationSearch() function as well
    enrtCheck = input('Do you have any enroute locations? (Y/N)')
    while (True):
        if enrtCheck.startswith('y' or 'Y'):
            enroute = True
            enrtList = []
            while True:
                try:
                    num = int(input('Enter the number of enroute locations you plan to have: '))
                except ValueError:
                    print('Please enter the number of your locations as an integer.')
                    continue
                else:
                    break
        
            for x in range(num):
                print('Please input an lcode or a keyword for your enroute location(s): ')
                enKey = locationSearch(dbName)
                enrtList.append(enKey)
            False
            break
        elif enrtCheck.startswith('n' or 'N'):
            enroute = False
            False
            break
        else:
            print("Please enter either \'Y\' or \'N\'.")

    
    #driver is automatically set to member email
    driver = email    
    
    #rno is automatically set to the next unique number
    rno = maxRno(dbName)
    
    #verifies the user has entered info
    print('Your ride info has been recorded')
    #if user entered enroute locations - show them their list of enroute locations
    if enroute == True:
        print('The enroute locations you entered are: ')
        for each in enrtList:
            print (each)
    else:
        print('You do not have any enroute locations.')
    
    #insert into rides table
    insertRides(rno, ppseat, rdate, seats2, luggage, src, dst, driver, cnoB, dbName)
    #insert into enroute table
    if enroute == True:
        insertEnroute(rno, enrtList, dbName)
    else:
        print('')
    
    conn.commit()


    mainMenu(dbName, email)


  

