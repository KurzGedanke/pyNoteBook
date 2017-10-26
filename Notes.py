import sqlite3


class Notes:
    '''
    Created notes based on the username and if loggedIn = true. Also lists the
    notes and deletes the notes.
    '''

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

    def delete_notes(self, heading):
        if self.loggedIn:
            try:
                self.c.execute('''DELETE FROM note WHERE heading IN (?)
                           AND username = (?)''', (heading, self.username))
                self.conn.commit()
            except sqlite3.OperationalError as e:
                print(e)
                pass
        else:
            print('You are not logged in!')
