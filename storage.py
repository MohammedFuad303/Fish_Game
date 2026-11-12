import sqlite3

DB_FILE = "fish_game.db"

# A function which creates the users, scores and admins tables if they don’t exist yet
def create_tables():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS scores (username TEXT PRIMARY KEY, score INTEGER NOT NULL, rounds INTEGER NOT NULL)") #username primary key, so each player has exactly one row
    conn.execute("CREATE TABLE IF NOT EXISTS admins (username TEXT PRIIMARY KEY)")
    conn.commit() #saves to disk
    conn.close() #closes the file


# A function which saves a new user, and returns False if the username is taken
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

#  function which returns the stored hash for a user, or None if there’s no such user
def get_password_hash(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row is None:
        return None
    return row[0]


# a function which saves or overwrites a player’s score row
def save_score(username, score, rounds):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT or REPLACE INTO scores VALUES (?, ?, ?)",(username, score, rounds))
    conn.commit()
    conn.close()


# A function which returns a player’s saved score and rounds, or (0, 0) for a new player
def get_score(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT score, rounds FROM scores WHERE username =?", (username,)).fetchone() 
    conn.close()

    if row is None:
        return 0, 0       
    return row[0], row[1] 


# A function which returns the highest scores, best first
def get_top_scores(limit=5):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT username, score, rounds FROM scores ORDER BY score DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return rows


# A function which adds a user to the admins table
def make_admin(username):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT OR IGNORE INTO admins VALUES (?)", (username,))
    conn.commit()
    conn.close()

# A function which checks if a user is an admin
def is_admin(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT 1 FROM admins WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row is not None

# A function which returns a list of all registered usernames
def get_all_usernames():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT username FROM users ORDER BY username").fetchall()
    conn.close()
    return [row[0] for row in rows]


if __name__ == "__main__":
    create_tables()
    print(get_all_usernames())