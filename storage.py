import sqlite3

DB_FILE = "fish_game.db"


def create_tables():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT PRIMARY KEY, score INTEGER NOT NULL, rounds INTEGER NOT NULL)") #username primary key, so each player has exactly one row
    conn.execute("CREATE TABLE IF NOT EXISTS admins (username TEXT PRIIMARY KEY)")
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


def get_top_scores(limit=5):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT username, score, rounds FROM scores ORDER BY score DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return rows
#ORDER BY score DESC sorts the rows from the highest score to the lowest (DESC means descending).
#LIMIT ? returns only the first few rows, 5 by default.
#fetchall() returns all the matching rows as a list, where fetchone() returned just one.
#Each row is a group of three values: username, score and rounds.
#limit=5 is a default value. Calling get_top_scores() uses 5, and get_top_scores(10) would use 10.


def make_admin(username):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT OR IGNORE INTO admins VALUES (?)", (username,))
    conn.commit()
    conn.close()


def is_admin(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT 1 FROM admins WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row is not None
#The admins table has one column, username. If a name is in the table, that user is an admin.
#INSERT OR IGNORE adds the name, and does nothing if it’s already there, so running it twice is safe.
#SELECT 1 ... WHERE username = ? only checks whether a matching row exists. We don’t need its contents.
#return row is not None gives True if a row was found and False if not. You used is not None earlier, in the API check.


if __name__ == "__main__":
    create_tables()
    make_admin("fuad2")
    print(is_admin("fuad2"))
    print(is_admin("testa"))