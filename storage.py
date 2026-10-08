import sqlite3

DB_FILE = "fish_game.db"


def create_tables():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database ready")