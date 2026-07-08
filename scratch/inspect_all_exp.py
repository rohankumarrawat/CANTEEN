import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

output = []
rows = conn.execute("SELECT date, COUNT(*) as cnt, SUM(amount) as total FROM expenditure GROUP BY date ORDER BY date DESC LIMIT 20").fetchall()
for r in rows:
    output.append(f"{r['date']}: count={r['cnt']} | total={r['total']}")

with open(os.path.join(os.path.dirname(__file__), 'exp_all.txt'), 'w') as f:
    f.write("\n".join(output))

conn.close()
