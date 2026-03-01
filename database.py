import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        paid INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users(user_id, username) VALUES(?,?)",
                (user_id, username))
    conn.commit()
    conn.close()

def set_paid(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET paid=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_paid(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT paid FROM users WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result and result[0] == 1

def get_all_users():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, paid FROM users")
    result = cur.fetchall()
    conn.close()
    return result
