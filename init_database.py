"""
Purpose: to create the database
"""

import _sqlite3

connection = _sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO books (title, author, genre, rating) VALUES(?,?,?,?)",
               ('The Hunger Games', 'Suzanne Collins', 'Young Adult', '4.2'))
cursor.execute("INSERT INTO user_info (email) VALUES(?)",
               ('aleg101@live.com'))

connection.commit()
connection.close()
