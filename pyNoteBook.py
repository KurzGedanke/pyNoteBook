import sqlite3
import hashlib


class User:
    def __init__(self, username, password, c, conn):
        self.username = username
        self.password = password
        self.c = c
        self.conn = conn

    def create_user(self):
        pwdHash = hashlib.sha256(self.password.encode('UTF-8') +
                                 "magic salt".encode('UTF-8'))
        self.c.execute('INSERT into user(username, password) VALUES (?, ?)',
                       (self.username, pwdHash.hexdigest()))
        self.conn.commit()

    def get_password(self):
        self.c.execute('SELECT password FROM user WHERE username=(?)',
                       (self.username,))
        return self.c.fetchall()


class Notes:
    def __init__(self, username, loggedIn, c, conn):
        self.username = username
        self.loggedIn = loggedIn
        self.c = c
        self.conn = conn

    def new_note(self):
        if self.loggedIn:
            heading = input('Please enter your heading: \n')
            note = input('Please enter your notes: \n')
            self.c.execute('''INSERT into note(username, heading, note) VALUES
                           (?, ?, ?)''', (self.username, heading, note))
            self.conn.commit()
        else:
            print('You are not logged in!')

    def get_notes(self):
        if self.loggedIn:
            self.c.execute('SELECT heading, note FROM note where username=(?)',
                           (self.username, ))
            return self.c.fetchall()
        else:
            print('You are not logged in!')

    def delete_notes(self):
        pass


def login(c, conn):
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
    try:
        c.execute('''CREATE TABLE user(
                id integer primary key,
                username text,
                password text
                )''')
        print('Database user created!')
    except:
        print('Database user exist!')

    try:
        c.execute('''CREATE TABLE note(
                id integer primary key,
                username text,
                heading text,
                note text
                )''')
        print('Database note created!')
    except:
        print('Database note exist!')

    conn.commit()


def list_notes(noteobj, c, conn):
    notes = noteobj.get_notes()
    for key, val in notes:
        print("Heading:\n" + key)
        print("Notes:\n" + val)


def menu(c, conn):
    loggedIn = '', False
    noteInput = 0
    logInput = int(input('Welcome to pyNoteBook!\n1. Login\n2. Register\n'))
    if logInput == 1:
        loggedIn = login(c, conn)
    elif logInput == 2:
        register(c, conn)
        return
    else:
        print('Can\'t recognise your input.')

    while noteInput != 4:
        if loggedIn[1]:
            print('Welcome %s, you are logged in!'.format(loggedIn[0]))
            note = Notes(loggedIn[0], loggedIn[1], c, conn)
            noteInput = int(input('1. Show your Notes\n2. New Note\n3. Delete Note\n4. Exit programm\n'))
            if noteInput == 1:
                list_notes(note, c, conn)
            elif noteInput == 2:
                note.new_note()
            elif noteInput == 3:
                pass
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
