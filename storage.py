import sqlite3

conn = sqlite3.connect("fish_game.db")
conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)")
conn.commit()
conn.close()

print("Database ready")