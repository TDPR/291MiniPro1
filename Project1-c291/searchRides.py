import sqlite3
import menu

def printSearchedRows(rows):
    print(""" (#) | rno |  price | rdate | seats | lugDesc | src | dst | driver | cno | make | model | year | seats | owner""")
    i = 0
    for row in rows:
        print(""" ({num})) | {rno} | {prc} | {rd} | {rsts} | {ld} | {src} | {dst} | {drv} | {cno} | {mk} | {md} | {yr} | {csts} | {own}"""
        .format(num=i , rno=row[0], prc=row[1], rd=row[2], rsts=row[3], ld=row[4], src=row[5], dst=row[6], drv=row[7], cno=row[8], mk=row[9], md=row[10], yr=row[11], csts=row[12], own=row[13]))
        i += 1
    print('')
    return

def messageMember(dbName, email, rEmail, rno):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    print('Messaging {member}, what do you want to say?'.format(member=rEmail))
    print('(type !esc to leave to main menu)')
    inp = input()
    if inp == '!esc':
        return
    else:
        c.execute("""INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) 
        VALUES (?, DATETIME('now'), ?, ?, ?, 'n');""",[rEmail, email, inp, rno])
        conn.commit()
        conn.close()
        print('Message sent')
        return

def selectRides():
    cont = True
    while cont:
        print('Input a number 0-4 to select a ride to message the driver about the ride.')
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

# Function 2 
def searchRides(dbName, email):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    while True:
        print('To search for a ride, enter 1 to 3 location keywords, each separated by a space.')
        print('(type !esc to return to main menu)')
        inp = input()
        if inp == '!esc':
            conn.close()
            menu.mainMenu(dbName, email) # returns to main menu
        keys = [i for i in inp.split()]
        keys = ['%'+k+'%' for k in keys]
        offset = 0
        while True:
            if len(keys) == 1:
                while True:
                    c.execute("""SELECT rec.rno, rec.price, rec.rdate, rec.seats,
                    rec.lugDesc, rec.src, rec.dst, rec.driver, rec.cno, rec.make,
                    rec.model, rec.year, rec.seats, rec.owner
                    FROM 
                    (SELECT * 
                    FROM rides LEFT OUTER JOIN cars ON rides.cno=cars.cno
                    LEFT OUTER JOIN enroute ON rides.rno=enroute.rno) as rec,
                    (SELECT lcode 
                    FROM locations l
                    WHERE (l.lcode LIKE ?
                    OR l.prov LIKE ?
                    OR l.city LIKE ?
                    OR l.address LIKE ?)) as l
                    WHERE (l.lcode = rec.lcode
                    OR l.lcode = rec.src
                    OR l.lcode = rec.dst)
                    LIMIT 5 OFFSET ?;""",[keys[0], keys[0], keys[0], keys[0], offset])
                    rows = c.fetchall()
                    if len(rows) > 0:
                        printSearchedRows(rows)
                        inp = selectRides()
                        if inp == 'next':
                            offset += 5
                        elif inp == 'back':
                            if offset >= 5:
                                offset -=5
                            else: 
                                print('You cannot go back any more.')
                        elif inp == '!esc':
                            conn.close()
                            menu.mainMenu(dbName, email)
                        else:
                            messageMember(dbName, email, rows[inp][7], rows[inp][0])
                            conn.close()
                            menu.mainMenu(dbName, email) # back to main menu
                    else:
                        print('There were no locations with keyword {key}'.format(key=keys[0]))
            elif len(keys) == 2:
                while True: 
                    c.execute("""SELECT rec.rno, rec.price, rec.rdate, rec.seats,
                    rec.lugDesc, rec.src, rec.dst, rec.driver, rec.cno, rec.make,
                    rec.model, rec.year, rec.seats, rec.owner
                    FROM 
                    (SELECT * 
                    FROM rides LEFT OUTER JOIN cars ON rides.cno=cars.cno
                    LEFT OUTER JOIN enroute ON rides.rno=enroute.rno) as rec,
                    (SELECT lcode 
                    FROM locations l
                    WHERE (l.lcode LIKE ?
                    OR l.prov LIKE ?
                    OR l.city LIKE ?
                    OR l.address LIKE ?)) as l
                    WHERE (l.lcode = rec.lcode
                    OR l.lcode = rec.src
                    OR l.lcode = rec.dst)
                    INTERSECT
                    SELECT rec.rno, rec.price, rec.rdate, rec.seats,
                    rec.lugDesc, rec.src, rec.dst, rec.driver, rec.cno, rec.make,
                    rec.model, rec.year, rec.seats, rec.owner
                    FROM 
                    (SELECT * 
                    FROM rides LEFT OUTER JOIN cars ON rides.cno=cars.cno
                    LEFT OUTER JOIN enroute ON rides.rno=enroute.rno) as rec,
                    (SELECT lcode 
                    FROM locations l
                    WHERE (l.lcode LIKE ?
                    OR l.prov LIKE ?
                    OR l.city LIKE ?
                    OR l.address LIKE ?)) as l
                    WHERE (l.lcode = rec.lcode
                    OR l.lcode = rec.src
                    OR l.lcode = rec.dst)
                    LIMIT 5 OFFSET ?;""", [keys[0], keys[0], keys[0], keys[0], keys[1], keys[1], keys[1], keys[1], offset])
                    rows = c.fetchall()
                    if len(rows) > 0:
                        printSearchedRows(rows)
                        inp = selectRides()
                        if inp == 'next':
                            offset += 5
                        elif inp == 'back':
                            if offset >= 5:
                                offset -=5
                            else: 
                                print('You cannot go back any more.')
                        elif inp == '!esc':
                            conn.close()
                            menu.mainMenu(dbName, email)
                        elif type(inp)== int:
                            messageMember(dbName, email, rows[inp][7], rows[inp][0])
                            conn.close()
                            menu.mainMenu(dbName, email)
                        else:
                            print('Something was wrong with your input')
                    else:
                        print('There were no locations with keywords {key1}, {key2}'.format(key1=keys[0], key2=keys[1]))
            elif len(keys) == 3:
                while True:
                    c.execute("""SELECT rec.rno, rec.price, rec.rdate, rec.seats,
                    rec.lugDesc, rec.src, rec.dst, rec.driver, rec.cno, rec.make,
                    rec.model, rec.year, rec.seats, rec.owner
                    FROM 
                    (SELECT * 
                    FROM rides LEFT OUTER JOIN cars ON rides.cno=cars.cno
                    LEFT OUTER JOIN enroute ON rides.rno=enroute.rno) as rec,
                    (SELECT lcode 
                    FROM locations l
                    WHERE (l.lcode LIKE ?
                    OR l.prov LIKE ?
                    OR l.city LIKE ?
                    OR l.address LIKE ?)) as l
                    WHERE (l.lcode = rec.lcode
                    OR l.lcode = rec.src
                    OR l.lcode = rec.dst)
                    INTERSECT
                    SELECT rec.rno, rec.price, rec.rdate, rec.seats,
                    rec.lugDesc, rec.src, rec.dst, rec.driver, rec.cno, rec.make,
                    rec.model, rec.year, rec.seats, rec.owner
                    FROM 
                    (SELECT * 
                    FROM rides LEFT OUTER JOIN cars ON rides.cno=cars.cno
                    LEFT OUTER JOIN enroute ON rides.rno=enroute.rno) as rec,
                    (SELECT lcode 
                    FROM locations l
                    WHERE (l.lcode LIKE ?
                    OR l.prov LIKE ?
                    OR l.city LIKE ?
                    OR l.address LIKE ?)) as l
                    WHERE (l.lcode = rec.lcode
                    OR l.lcode = rec.src
                    OR l.lcode = rec.dst)
                    INTERSECT
                    SELECT rec.rno, rec.price, rec.rdate, rec.seats,
                    rec.lugDesc, rec.src, rec.dst, rec.driver, rec.cno, rec.make,
                    rec.model, rec.year, rec.seats, rec.owner
                    FROM 
                    (SELECT * 
                    FROM rides LEFT OUTER JOIN cars ON rides.cno=cars.cno
                    LEFT OUTER JOIN enroute ON rides.rno=enroute.rno) as rec,
                    (SELECT lcode 
                    FROM locations l
                    WHERE (l.lcode LIKE ?
                    OR l.prov LIKE ?
                    OR l.city LIKE ?
                    OR l.address LIKE ?)) as l
                    WHERE (l.lcode = rec.lcode
                    OR l.lcode = rec.src
                    OR l.lcode = rec.dst)
                    LIMIT 5 OFFSET ?;""",
                    [keys[0], keys[0], keys[0], keys[0], keys[1], keys[1], keys[1], keys[1], keys[2], keys[2], keys[2], keys[2], offset])
                    rows = c.fetchall()
                    if len(rows) > 0:
                        printSearchedRows(rows)
                        inp = selectRides()
                        if inp == 'next':
                            offset += 5
                        elif inp == 'back':
                            if offset >= 5:
                                offset -=5
                            else: 
                                print('You cannot go back any more.')
                        elif inp == '!esc':
                            conn.close()
                            menu.mainMenu(dbName, email)
                        else:
                            messageMember(dbName, email, rows[inp][7], rows[inp][0])
                            conn.close()
                            menu.mainMenu(dbName, email) # back to main menu
                    else:
                        print('There were no locations with keywords {key1}, {key2}, {key3}'.format(key1=keys[0], key2=keys[1], key3=keys[2]))
            elif len(keys) == 0:
                print('No keyword entered.')
            elif len(keys) > 3:
                print('Too many keywords.')
            else:
                print('There was something wrong with your input.')
