import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

output = []

output.append("=== EXPENDITURE RECORDS ===")
rows = conn.execute("SELECT * FROM expenditure WHERE date >= '2026-07-01' ORDER BY date DESC").fetchall()
for r in rows:
    output.append(f"ID={r['id']}: date={r['date']} | amount={r['amount']:.2f} | category={r['category']} | notes={r['notes']}")

output.append("\n=== STOCK LEDGER RECORDS ===")
rows = conn.execute("SELECT * FROM stock_ledger WHERE date >= '2026-07-01' ORDER BY date DESC").fetchall()
for r in rows:
    output.append(f"ID={r['id']}: date={r['date']} | inv_id={r['inv_id']} | type={r['transaction_type']} | change={r['qty_change']:.3f} | notes={r['notes']}")

with open(os.path.join(os.path.dirname(__file__), 'july_inspection.txt'), 'w') as f:
    f.write("\n".join(output))

conn.close()
print("Inspection written to july_inspection.txt")
