import sqlite3

conn = sqlite3.connect('tickets.db')

conn.execute('''CREATE TABLE tickets
                (id INT PRIMARY KEY NOT NULL,
                status TEXT NOT NULL);''')

ids = []
for id in ids:
    conn.execute('''INSERT INTO tickets
                    VALUES ({}, 'unused');'''.format(id))

# conn.execute('''DELETE FROM tickets;''')

conn.commit()
conn.close()
