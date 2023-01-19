import sqlite3

con = sqlite3.connect('database.sqlite')
cur = con.cursor()
with open('create_database.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
