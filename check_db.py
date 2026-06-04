import sqlite3
import traceback

conn = sqlite3.connect('canteen.db')
conn.row_factory = sqlite3.Row

# Get all table names
tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

# Extract schema
schema = {}
for t in tables:
    schema[t] = [row[1] for row in conn.execute(f"PRAGMA table_info({t})").fetchall()]

print(schema)
