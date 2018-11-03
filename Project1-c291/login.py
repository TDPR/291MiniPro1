import re
import getpass
import sqlite3

#Login Menu that the user will refer back to until logged in
def loginMenu(dbName):
    print('\nWelcome! Control this menu using numbers')
    print('1. Login')
    print('2. Sign Up')
    print('3. Exit')
    res = input()

    if res == '1':
        logIn(dbName)

    elif res == '2':
        print('\nSigning Up')
        signUp(dbName)

    elif res == '3':
        print('Goodbye\n')
        exit()

    else:
        print('\nInput is Invalid, Please Try Again')
        loginMenu(dbName)

#logIn
def logIn(dbName):
    print('\nLog In\nEnter your email or Back to go back')
    emailInput = input('Email: ')
    
    if emailInput.lower() == 'back':
        loginMenu(dbName)
    
    elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$', emailInput):
        print('\nInvalid Input')
        logIn(dbName)
    
    #log in attempt
    else:
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute(' PRAGMA foreign_keys=ON; ') 
        password = getpass.getpass('Password: ')
        c.execute('''SELECT * 
            FROM members
            WHERE email LIKE :email
            AND pwd=:pwd;''', 
            {"email": emailInput, 'pwd': password})
        fetchResult = c.fetchall()
        conn.commit()
        conn.close()
        
        #login attempt pathing
        if not fetchResult:
            print('\nUsername or Password is incorrect')
            logIn(dbName)
        
        elif len(fetchResult) == 1:
            print('\nWelcome ' + fetchResult[0][1])
            from menu import mainMenu
            mainMenu(dbName,emailInput)
        
        else:
            print('Something went wrong, please try again')
            loginMenu(dbName)


#signup
def signUp(dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    print('Please enter your desired email (15 char max) or Back to go back')
    email = input('Email: ')
    if email.lower() == 'back':
        loginMenu(dbName)

    elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$', email) or len(email) > 15:
        print('\nInvalid Input')
        signUp(dbName)

    c.execute('''SELECT *
        FROM members
        WHERE email LIKE :email;''',
        {"email": email})
    fetchResult = c.fetchall()
        
    #signup form if email wasn't in use
    if not fetchResult:
        name= ''
        password=''
        passwordConf = ''
        phone=''
        print('\nEmail is available, please fill the rest of the form')
        print('Email: ' + email)

        while password != passwordConf or len(password) > 6 or len(password) == 0:
            password=''
            passwordConf = ''
            password = getpass.getpass('Password max 6 char: ')
            passwordConf = getpass.getpass('Confrim Password: ')
     
        while len(name) > 20 or len(name) == 0:
            name = input('Full Name max 20 char: ')

        while not phone.isdigit() or len(phone) > 12 or len(phone) == 0:
            phone = input('Phone number max 12 digits: ')

        print('\nConfirm Your Information')
        print('Email: ' + email)
        print('Name: ' + name)
        print('Phone: ' + phone)
        print('Confirm y|n')
        res=''
        
        while res.lower() != 'y' and res.lower() != 'n':
            res = input()
        
        #sign up confirm
        if res.lower() == 'y':
            signUpInfo = [email,name,phone,password]
            c.execute('''INSERT INTO members(email,name,phone,pwd)
                VALUES (?,?,?,?);''',
                signUpInfo) 
            conn.commit()
            conn.close()
            print("You've successfully signed up! Please Login")
            loginMenu(dbName)
        
        elif res.lower() == 'n':
            conn.commit()
            conn.close()
            signUp(dbName)

    #email in use  
    else: 
        print('\nEmail is in use: Please try again')
        conn.commit()
        conn.close()
        signUp(dbName)
