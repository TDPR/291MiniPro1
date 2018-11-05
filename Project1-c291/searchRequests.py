# This file conatins Function 5 of the assignmet spec and all the functions that depend on it.


import sqlite3
import menu

def printRequests(rows):
    print(' (#) | rid |  email | rdate | pickup | dropoff | amount ')
    i = 0
    for row in rows:
        print(' ({num}) | {rid} | {em} | {rdate} | {pick} | {drop} | {am} '
        .format(num=i , rid=row[0], em=row[1], rdate=row[2], pick=row[3],
        drop=row[4], am=row[5]))
        i += 1
    print('')
    return

def selectDeleteRequest():
    while True:
        print('Input a number 1-5 to select a request to delete.')
        print('Or type next to go to the next page or type back to go the previous page.')
        print('(type !esc to return to the main menu)')
        inp = input()
        if inp == '!esc' or inp == 'next' or inp == 'back':
            return inp
        elif int(inp) < 1 or int(inp)> 5:
            print('Your input was out of bounds.')
        elif int(inp) >=1 and int(inp) <= 5:
            return int(inp)
        else:
            print('There was something wrong with your input.')

def selectSearchedRequest():
    while True:
        print('Input a number 0-4 to select a request to message the poster of the request.')
        print('Or type next to go to the next page or type back to go the previous page.')
        print('(type !esc to return to the main menu)')
        inp = input()
        if inp == '!esc' or inp == 'next' or inp == 'back':
            return inp
        elif int(inp) < 0 or int(inp)> 4:
            print('Your input was out of bounds.')
        elif int(inp) >=0 and int(inp) <= 4:
            return int(inp)
        else:
            print('There was something wrong with your input.')

def messageMemberRequest(dbName, email, reciever):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    while True:
        print('Please input the rno from the ride you want to message {member} about'
        .format(member=reciever))
        rno = input()
        if rno.isdigit():
            c.execute("""SELECT rno FROM rides WHERE rno=?""", [int(rno)])
            rows = c.fetchall()
            if len(rows) == 0:
                print('There is not a ride with that rno.')
            else:
                print('Messaging {member}, what do you want to say?'.format(member=reciever))
                print('(type !esc to leave to main menu)')
                inp = input()
                if inp == '!esc':
                    return
                else:
                    c.execute("""INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) 
                    VALUES (?, DATETIME('now'), ?, ?, ?, 'n');""", (reciever, email, inp, rno))
                    print('Message sent')
                    return
        else:
            print('There was something wrong with your input')

# Function 5 of assignment spec
def deleteOrSearchRequests(dbName, email):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    while True:
        print('Type 1 to see your requests or 2 to search requests by location code or city.')
        print('(type !esc to return to main menu)')
        inp = input()
        if inp == '!esc':
            menu.mainMenu(dbName, email)
        elif inp == '1':
            c.execute("""SELECT r.rid, r.email, r.rdate, r.pickup,
                    r.dropoff, r.amount
                    FROM requests r
                    WHERE r.email LIKE ?""", [email])
            rows = c.fetchall()
            printRequests(rows)
            while True:
                print('Type in a number to select a ride to delete')
                print('(type !esc to go back to main menu)')
                inp = input()
                if inp == '!esc':
                    menu.mainMenu(dbName, email)
                elif int(inp) in range(0, (len(rows))): #user entered a valid integer
                    print('Are you sure you want to delete the request? y or n')
                    check = input()
                    if check == 'y':
                        c.execute('DELETE FROM requests WHERE requests.id=?', (rows[int(inp)-1][0]))
                        print('Ride Deleted')
                        menu.mainMenu(dbName, email)
                    # if the user doesn't want to delete their request, we just let the while loop iterate again
                else: 
                    print('Something was wrong with your input')

        elif inp == '2':
            offset = 0
            while True:
                print('Enter a location code or city name')
                print('(type !esc to exit to main menu)')
                inp = input()
                if inp == '!esc':
                    menu.mainMenu(dbName, email)
                inp = '%'+inp+'%'
                c.execute("""SELECT r.rid, r.email, r.rdate, r.pickup,
                r.dropoff, r.amount 
                FROM requests r, 
                (SELECT lcode FROM locations 
                WHERE (lcode LIKE ?
                OR city LIKE ?))
                WHERE lcode = r.pickup
                LIMIT 5 OFFSET ?""", [inp, inp, offset])
                rows = c.fetchall()
                if len(rows) > 0:
                    printRequests(rows)
                    inp = selectSearchedRequest()
                    if inp == 'next':
                        offset += 5
                    elif inp == 'back':
                        if offset >=5:
                            offset-= 5
                        else:
                            print('You cannot go back anymore')
                    elif inp == '!esc':
                            menu.mainMenu(dbName,email)
                    else:
                        messageMemberRequest(dbName, email, rows[inp][1])
                        menu.mainMenu(dbName, email)
                else:
                    print('There were no location codes or city names matching {key}, '.format(key=inp))
        else:
            print('There was something wrong with your input')