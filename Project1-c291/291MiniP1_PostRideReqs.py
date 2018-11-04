'''
Created on Nov 1, 2018

@author: Mike
'''

import sqlite3
import datetime


#dateCheck function 
def dateCheck():
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
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

#This function generates a unique max rid for the each request made
def maxRID():
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

'''
NOTE** location search is the same as the one in offer rides (you only need one for integration)
'''
def locationSearch():
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

#Function to insert New Ride Request post into requests table
def insertRequest(rid, email, rdate, pickup, dropoff, amount):
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
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    print('Welcome to ride requests. Please input information about the ride you are requesting: ')
#will ask for rdate and check to ensure string is date format
    requestDate = dateCheck()
#produces unique rno
    requestRID = maxRID()
#finds pick up location using locationSearch func.
    print('Where would you like to be picked up?')
    pickup = locationSearch()
#finds dropoff location using locationSearch func.
    print('Where would you like to be dropped off?')
    dropoff = locationSearch()
#member provides amount willing to pay
    amount = input('How much are you willing pay per seat?: ')
#inserts information into requests table
    insertRequest(requestRID, email, requestDate, pickup, dropoff, amount)
    conn.commit()
    
    #mainMenu(dbName, email)
    
'''
***ONLY FOR TESTING FUNCTIONS (below should be removed before integration)***
'''
#this is the substitute for main (used to test the function)
print('Testing your function.')
dbName = 'C:/SQLite/t.db'
email = input('Hello Member. What is your email?: ')
postRideRequest(dbName, email)
