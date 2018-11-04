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
                rdateCheck = datetime.datetime.strptime(rdate,'%Y-%m-%d')
                break
            except ValueError:
                print('The date format you entered is incorrect. Please enter date in YYYY-MM-DD format.')
       
    return rdate

##This function generates a unique RNO for every ride offered
def maxRno():
    conn = sqlite3.connect('C:/SQLite/t.db')
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
def cnoMatch(carNum, email):
    conn = sqlite3.connect('C:/SQLite/t.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    c.execute('''
                        SELECT cno 
                        from cars
                            ''')
    cnoList = c.fetchall()
    
    c.execute('''
                SELECT cno, make, model, year, owner
                FROM cars
                LEFT JOIN  members on owner = email
                where email =  ?''', [email])
    cnoResult = c.fetchall() 
    print(cnoResult)
    
    myCno = []
    
    for each in cnoResult:
        myCno += [each[0]]
    
    
    if not int(carNum) in myCno:
        for x in range (0,3):
            print('The CNO you entered does not match your registered cars. Please try again')
            cnoRecheck = input('What is your CNO? ')
            if int(cnoRecheck) in myCno:
                cno = cnoRecheck
                break
            elif x == 3:
                print('You have entered the incorrect CNO 3 times. CNO will be set to null.')
                cno = ""
    else:
        cno = carNum  
        
    c.execute('''
                            SELECT seats
                            FROM cars
                            where cno = ? ''',[cno])
    seatsResult = c.fetchall()
    print('The correct number of seats in your car is: ', seatsResult[0][0])
     
    return cno, seatsResult

#This function allows members to search for lcode using keywords (city, prov, or address)
#It also allows members to scroll through lcodes if there are more than 5 associated with the keyword
def locationSearch():
    conn = sqlite3.connect('C:/SQLite/t.db')
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
            
        check2 = input('If you see the correct lcode please enter it. If not, type "next", or type "exit" to leave blank.\n**(If you entered incorrectly type "change" to view new queries.)** \n ')
    
        if (check2,) in lcodeList:
            loca = check2
            print()
            break
            False
        elif check2.lower() == 'next':
            offsetValue = offsetValue + 5
        elif check2.lower() == 'exit':
            loca = ""
            False
            break
        elif check2 == 'change':
            loca3 = input('What is your keyword?: ')
            
        else:
            print('Your choice is invalid.')
     
    return loca

#This function enters ride information into the ride table
def insertRides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno):
    conn = sqlite3.connect('C:/SQLite/t.db')
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
def insertEnroute(rno, lcode):
    conn = sqlite3.connect('C:/SQLite/t.db')
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
def rideInfo(email):
    conn = sqlite3.connect('C:/SQLite/t.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    
    rdate = dateCheck()
  
#user inputs info for seats, ppseat, lugagge
    seats1 = input('How many seats are available?: ')
    ppseat = input('How much to you charge per seat?: ')
    luggage = input('What luggage can riders bring?: ')
    
#user keyword is checked against existing lcodes
    print('Please enter your start location as an lcode or keyword.')
    key1 = '' 
    src = locationSearch()
    
#user keyword is checked against existing lcodes
    print('Please enter your end location as an lcode or keyword.')
    key2 = ''
    dst = locationSearch()
    
#user inputed CNO is checked to ensure car is registered to user 
    cnoAsk = input('Do you have a car number (CNO)? (Y/N) ')
    if cnoAsk.startswith('n' or 'N'):
        print('Your CNO will be left blank.')
        cnoAsk = ""
    elif cnoAsk.startswith('y' or 'Y'):
        cnoA = input('What is your cno?: ')
        cnoB, seats2 = cnoMatch(cnoA, email)
        
#enroute the locationSearch() function as well
    enrtCheck = input('Do you have any enroute locations? (Y/N)')
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
            enKey = locationSearch()
            enrtList.append(enKey)
    elif enrtCheck.startswith('n' or 'N'):
        enroute = False
    
#driver is automatically set to member email
    driver = email    
    
#rno is automatically set to the next unique number
    rno = maxRno()
    print(cnoB)
    print(seats2)
    print(src)
    print(dst)
#shows the user the info they entered  
    print('Your info is:\n' +
          'Date = ' + rdate + '; Seats = ',seats2[0][0],'; Price/seat = ' + ppseat
          + '; Luggage = ' + luggage + '; Start of Ride = ' + src + '; End of ride =  ' + dst 
          + '; Car Number = ', cnoB)
#if user entered enroute locations - show them their list of enroute locations
    if enroute == True:
        print('The enroute locations you entered are: ')
        for each in enrtList:
            print (each)
    
#insert into rides table
    insertRides(rno, ppseat, rdate, seats2[0][0], luggage, src, dst, driver, cnoB)
#insert into enroute table
    insertEnroute(rno, enrtList)
    
    conn.commit()


    mainMenu(dbName, email)
  
  
  
