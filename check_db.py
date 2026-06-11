import sqlite3

conn = sqlite3.connect('canteen.db')
conn.row_factory = sqlite3.Row

# Get all table names
tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

for t in sorted(tables):
    try:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"Table: {t:20} Row Count: {count}")
        if count > 0 and t not in ('users', 'roles', 'user_roles'):
            # Print first 2 rows
            rows = conn.execute(f"SELECT * FROM {t} LIMIT 2").fetchall()
            for r in rows:
                print("   ", dict(r))
    except Exception as e:
        print(f"Error reading {t}: {e}")

conn.close()
