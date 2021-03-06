import sqlite3
import hashlib
from User import User
from Notes import Notes


def login(c, conn):
    '''
    Logs the user in and if sucessful return a tuple of the username and
    True or False.
    '''

    print('LOGIN: \n-----------------------------')
    username = input('Please enter your Usernamn: \n')
    password = input('Please enter your password: \n')
    pwdHash = hashlib.sha256(password.encode('UTF-8') +
                             "magic salt".encode('UTF-8'))
    usr = User(username,
               pwdHash,
               c,
               conn)

    if usr.get_password()[0][0] == pwdHash.hexdigest():
        print('Is true!')
        return username, True
    else:
        return username, False


def register(c, conn):
    '''
    Registers the user in the databse by calling the User class.
    '''

    print('REGISTER: \n-----------------------------')
    username = input('Please enter a Username: \n')
    password = input('Please enter a Password: \n')
    exist = False

    for row in c.execute('SELECT username FROM user'):
        if row[0] == username:
            exist = True
        else:
            exist = False

    if exist:
        print('Your Username exist')
    else:
        print('User created!')
        usr = User(username, password, c, conn)
        usr.create_user()


def create_databases(c, conn):
    '''
    Trys to create the databse and if the database exists it throws and passes
    an error.
    '''
    try:
        c.execute('''CREATE TABLE user(
                id integer primary key,
                username text,
                password text
                )''')
        print('Database user created!')
    except sqlite3.OperationalError as e:
        print(e)
        pass

    try:
        c.execute('''CREATE TABLE note(
                id integer primary key,
                username text,
                heading text,
                note text
                )''')
        print('Database note created!')
    except sqlite3.OperationalError as e:
        print(e)
        pass

    conn.commit()


def list_notes(noteobj, c, conn):
    '''
    Lists the notes which returns from the note class
    '''

    notes = noteobj.get_notes()
    index = 0
    for key, val in notes:
        print(f'{index}. Heading:\n {key}')
        print(f'{index}. Notes:\n {val}')
        index += 1


def delete_note(noteobj, c, conn):
    '''
    First lists the notes and then asks for the heading for the one to
    delete.
    '''
    notes = noteobj.get_notes()
    index = 0
    for key, val in notes:
        print(f'{index}. Heading:\n {key}')
        print(f'{index}. Notes:\n {val}')
        index += 1
    toDelte = input(
        'Please enter the heading of the note you want to delete.\n')
    noteobj.delete_notes(toDelte)


def menu(c, conn):
    loggedIn = '', False
    noteInput = 0
    loginInput = int(input('Welcome to pyNoteBook!\t1. Login\t2. Register\n'))
    if loginInput == 1:
        loggedIn = login(c, conn)
    elif loginInput == 2:
        register(c, conn)
        return
    else:
        print('Can\'t recognise your input.')

    while noteInput != 4:
        if loggedIn[1]:
            print(f'Welcome {loggedIn[0]}, you are logged in!')
            note = Notes(loggedIn[0], loggedIn[1], c, conn)
            noteInput = int(input('1. Show your Notes\t2. New Note\t'
                                  '3. Delete Note\t4. Exit programm\n'))
            if noteInput == 1:
                list_notes(note, c, conn)
            elif noteInput == 2:
                note.new_note()
            elif noteInput == 3:
                delete_note(note, c, conn)
            elif noteInput == 4:
                print('Bye! Bye! My old friend...')
            else:
                print('Can\'t recognise your input.')


def main():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    create_databases(c, conn)
    menu(c, conn)

    conn.close()


if __name__ == '__main__':
    main()
