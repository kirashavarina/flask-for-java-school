import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO albums (title, author, year_album) VALUES (?, ?, ?)",
            ('Jazz', 'Queen', 1978)
            )

cur.execute("INSERT INTO albums (title, author, year_album) VALUES (?, ?, ?)",
            ('The Wall', 'Pink Floyd', 1979)
            )

connection.commit()
connection.close()
