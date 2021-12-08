import sqlite3

conn = sqlite3.connect('bookstore.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE books
          (id INTEGER PRIMARY KEY ASC,
           timestamp DATETIME NOT NULL,
           title VARCHAR(250),
           author VARCHAR(250),
           rating INTEGER,
           price REAL
          )
          ''')

conn.commit()
conn.close()
