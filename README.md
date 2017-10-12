# A commandline notebook in Python

![Python3.6](https://img.shields.io/badge/Python-3.6-blue.svg)

A simple command line notebook writen in python, based on sqlite3.

- [x] writing/reading from database
- [x] creating user
- [x] hashing password
- [x] logging in
- [x] adding notes
- [x] listing notes
- [x] deleting notes
- [ ] formating
- [ ] input correction
- [ ] mark up

```bash
╭─loki@Loki ~/Developer/pyNoteBook  ‹master›
╰─$ python3 pyNoteBook.py                                                   1 ↵
Database user created!
Database note created!
Welcome to pyNoteBook!  1. Login    2. Register
2
REGISTER:
-----------------------------
Please enter a Username:
KurzGedanke
Please enter a Password:
password
User created!
╭─loki@Loki ~/Developer/pyNoteBook  ‹master›
╰─$ python3 pyNoteBook.py                                                   1 ↵
table user already exists
table note already exists
Welcome to pyNoteBook!  1. Login    2. Register
1
LOGIN:
-----------------------------
Please enter your Usernamn:
KurzGedanke
Please enter your password:
password
Is true!
Welcome KurzGedanke, you are logged in!
1. Show your Notes  2. New Note 3. Delete Note  4. Exit programm
2
Please enter your heading:
This is a new Heading!
Please enter your notes:
This is a new Note!
Welcome KurzGedanke, you are logged in!
1. Show your Notes  2. New Note 3. Delete Note  4. Exit programm
1
0. Heading:
 This is a new Heading!
0. Notes:
 This is a new Note!
Welcome KurzGedanke, you are logged in!
1. Show your Notes  2. New Note 3. Delete Note  4. Exit programm
3
0. Heading:
 This is a new Heading!
0. Notes:
 This is a new Note!
Please enter the heading of the note you want to delete.
This is a new Heading!
Welcome KurzGedanke, you are logged in!
1. Show your Notes  2. New Note 3. Delete Note  4. Exit programm
1
Welcome KurzGedanke, you are logged in!
1. Show your Notes  2. New Note 3. Delete Note  4. Exit programm
4
Bye! Bye! My old friend...
```
