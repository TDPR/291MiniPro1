import sqlite3

def bookingMenu(dbName, email):
    print('Control this menu using numbers')
    print('1.List Bookings')
    print('2.Book Members')
    print('3.Cancel Bookings')
    print('4.Go back to the Main Menu')
    res = input()

    if res == '1':
        print('1')
    
    elif res == '2':
        print('2')
    
    elif res == '3':
        print('3')

    elif res == '4':
        from menu import mainMenu
        mainMenu(dbName,email)

    else:
        print('Invalid Input\n')
        bookingMenu(dbName,email)

def listBookings(dbName,email):
    return

def bookMembers(dbName,email):
    return

def cancelBookings(dbName,email):
    return