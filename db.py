import sqlite3

def init_db():
    conn = sqlite3.connect("tweets.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        text TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()