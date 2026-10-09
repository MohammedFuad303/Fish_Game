import sqlite3

DB_FILE = "fish_game.db"


def create_tables():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT PRIMARY KEY, score INTEGER NOT NULL, rounds INTEGER NOT NULL)") #username primary key, so each player has exactly one row
    conn.commit() #saves to disk
    conn.close() #closes the file


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


def save_score(username, score, rounds):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT or REPLACE INTO scores VALUES (?, ?, ?)",(username, score, rounds))
    conn.commit()
    conn.close()
# INSERT OR REPLACE adds a new row, or overwrites the existing one if that username alrewady has a row
# The three placehoulders ? are filled with (username, score, rounds), in the same order as the columns in the table


def get_score(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT score, rounds FROM scores WHERE username =?", (username,)).fetchone() #asks for two columns, so row holds two values
    conn.close()

    if row is None:
        return 0, 0       #If the player has no row yet, it returns [0, 0] so anew player simply starts from zero
    return row[0], row[1] #row[0]is the score, row[1] is the rounds


if __name__ == "__main__":
    create_tables()
    print(get_score("fuad2"))