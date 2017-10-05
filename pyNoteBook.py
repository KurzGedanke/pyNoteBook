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
        self.c.execute('''CREATE TABLE ?(
                        heading text,
                        note text
                        )''', (self.username,))
        self.conn.commit()

    def get_username(self):
        self.c.execute('SELECT * from user')
        userData = self.c.fetchall()
        for data in userData:
            print(data)

    def get_password(self):
        self.c.execute('SELECT password FROM user WHERE username=(?)',
                       (self.username,))
        return self.c.fetchall()

    def create_database(self):
        self.c.execute('''CREATE TABLE (?)(
                        heading text,
                        note text
                        )''', (self.username,))
        self.c.commit


class Notes:
    def __init__(self, c, conn):
        self.c = c
        self.conn = conn


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
                heading text,
                note text
                )''')
        print('Database note created!')
    except:
        print('Database note exist!')

    conn.commit()


def main():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    create_databases(c, conn)
    register(c, conn)

    print('Login: ' + str(login(c, conn)))

    conn.close()


if __name__ == '__main__':
    main()
