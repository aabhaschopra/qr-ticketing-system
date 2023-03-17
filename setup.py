import sqlite3

conn = sqlite3.connect('tickets.db')

conn.execute('''CREATE TABLE tickets
                (id INT PRIMARY KEY NOT NULL,
                status TEXT NOT NULL);''')
    
# conn.execute('''DROP TABLE tickets;''')

conn.commit()
conn.close()
