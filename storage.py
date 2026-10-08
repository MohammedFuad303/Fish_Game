import sqlite3

DB_FILE = "fish_game.db"


def create_tables():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
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

if __name__ == "__main__":
    create_tables()
    
    print(add_user("test4", "fakehash")) 