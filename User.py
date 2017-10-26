import hashlib


class User:
    '''
    The user class which creates the user in the databse and returns the
    hashed password from the database.
    '''

    def __init__(self, username, password, c, conn):
        self.username = username
        self.password = password
        self.c = c
        self.conn = conn

    def create_user(self):
        '''
        Creates the user in the database and hashes it password with
        a sha256 hash + a very secret salt. ;)
        '''

        pwdHash = hashlib.sha256(self.password.encode('UTF-8') +
                                 "magic salt".encode('UTF-8'))
        self.c.execute('INSERT into user(username, password) VALUES (?, ?)',
                       (self.username, pwdHash.hexdigest()))
        self.conn.commit()

    def get_password(self):
        self.c.execute('SELECT password FROM user WHERE username=(?)',
                       (self.username,))
        return self.c.fetchall()
