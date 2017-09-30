import sqlite3
import hashlib


class User:
    def __init__(self, username, password, curs, conn):
        self.username = username
        self.password = password
        self.curs = curs
        self.conn = conn

    def create_user(self):
        pwdHash = hashlib.sha256(self.password.encode('UTF-8') +
                                 "magic salt".encode('UTF-8'))
        self.curs.execute('INSERT into user(username, password) VALUES (?, ?)',
                          (self.username, pwdHash.hexdigest()))
        self.conn.commit()

    def get_username(self):
        self.curs.execute('SELECT * from user')
        userData = self.curs.fetchall()
        for data in userData:
            print(data)

    def get_password(self):
        self.curs.execute('SELECT password FROM user WHERE username=(?)',
                          (self.username,))
        return self.curs.fetchall()


class Notes:
    def __init__(self, user, note):
        self.user = user
        self.note = note


def login(conn, c):
    username = input('Please enter your Usernamn: \n')
    password = input('Please enter your password: \n')
    pwdHash = hashlib.sha256(password.encode('UTF-8') +
                             "magic salt".encode('UTF-8'))
    usr = User(username,
               pwdHash,
               c,
               conn
               )

    if usr.get_password()[0][0] == pwdHash.hexdigest():
        print('Is true!')
        return username, True
    else:
        return username, False


def register():
    pass


def create_databases(conn, c):
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
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    create_databases(conn, c)
    usr = User('Thore', 'Password', c, conn)
    usr.create_user()
    usr.get_username()

    print('Login: ' + str(login(conn, c)))

    conn.close()


if __name__ == '__main__':
    main()
