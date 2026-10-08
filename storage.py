import sqlite3

DB_FILE = "fish_game.db"


def create_tables():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT PRIMARY KEY, score INTEGER NOT NULL, rounds INTEGER NOT NULL)") #username primary key, so each player has exactly one row
    conn.commit()
    conn.close()


def add_user(username, password_hash):
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("INSERT INTO users VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_password_hash(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row is None:
        return None
    return row[0]


if __name__ == "__main__":
    create_tables()
    print(get_password_hash("test3"))
    print(get_password_hash("nobody"))