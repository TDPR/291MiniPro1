import sqlite3
import datetime


#dateCheck function 
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

#This function generates a unique max rid for the each request made
def maxRID(dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    c.execute( '''
                SELECT MAX(rid)
                FROM requests;
                ''')
    rid = c.fetchone()
    rid = rid[0] + 1    
    
    return rid

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
            print()
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

#Function to insert New Ride Request post into requests table
def insertRequest(rid, email, rdate, pickup, dropoff, amount, dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    #this SQL query inserts ride information into the requests table  
    c.execute('''
                        INSERT INTO requests(rid, email, rdate, pickup, dropoff, amount)
                        VALUES(?, ?, ?, ?, ?, ?);
                        ''', [rid, email, rdate, pickup, dropoff, amount])
    
    
    print('Your ride request has been added.')
    conn.commit()
    return


#This is the Post Ride Requests Primary Function
def postRideRequest(dbName, email):
    from menu import mainMenu
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
<<<<<<< HEAD
#allows user to leave before they start
    print('Welcome to post ride request.')
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

#will ask for rdate and check to ensure string is date format
=======
    print('Welcome to ride requests. Please input information about the ride you are requesting: ')
    #will ask for rdate and check to ensure string is date format
>>>>>>> 3b1e793b543f96aacd5d90de2fd54fe5c32aa708
    requestDate = dateCheck()
    #produces unique rno
    requestRID = maxRID(dbName)
    #finds pick up location using locationSearch func.
    print('Where would you like to be picked up?')
    pickup = locationSearch(dbName)
    #finds dropoff location using locationSearch func.
    print('Where would you like to be dropped off?')
    dropoff = locationSearch(dbName)
<<<<<<< HEAD
#member provides amount willing to pay
    while(True):
        try:        
            amount = int(input('How much are you willing to pay per seat?: '))
        except ValueError:
            print ('Please enter amount as a whole number.')
        else:
            False
            break
#inserts information into requests table
=======
    #member provides amount willing to pay
    amount = input('How much are you willing pay per seat?: ')
    #inserts information into requests table
>>>>>>> 3b1e793b543f96aacd5d90de2fd54fe5c32aa708
    insertRequest(requestRID, email, requestDate, pickup, dropoff, amount, dbName)
    conn.commit()
    
    mainMenu(dbName, email)


