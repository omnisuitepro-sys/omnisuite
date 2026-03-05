import sqlite3
conn = sqlite3.connect(r"C:\OmniSuite\backend\omni_core.db")
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
conn.close()