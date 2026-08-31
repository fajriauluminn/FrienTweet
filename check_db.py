import sqlite3

conn = sqlite3.connect("tweets.db")
c = conn.cursor()

c.execute("SELECT * FROM tweets")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()