import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (user_name, password) VALUES (?, ?)",
            ('GraceE', 'grace123456'))

#cur.execute("INSERT INTO TBR (U_ID, B_ID) VALUES (?, ?)",
           # (1, 1))

cur.execute("INSERT INTO book (Title, Author, Genre) VALUES (?, ?, ?)",
            ("The Hobbit","J.R.R Tolkien", "Fiction"))

connection.commit()
connection.close()