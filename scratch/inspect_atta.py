import sqlite3

conn = sqlite3.connect("canteen.db")
conn.row_factory = sqlite3.Row

# Get inv_id
item_row = conn.execute("SELECT id, item, stock, opening FROM inventory WHERE item LIKE 'Atta%'").fetchone()
print(f"Inventory Row: {dict(item_row)}")
inv_id = item_row["id"]

# Get all ledger entries
rows = conn.execute("SELECT * FROM stock_ledger WHERE inv_id=? ORDER BY date, id", (inv_id,)).fetchall()
curr = 0
for r in rows:
    curr += r["qty_change"]
    print(f"Date: {r['date']}, Type: {r['transaction_type']}, Change: {r['qty_change']}, Running Total: {curr:.2f}, Notes: {r['notes']}")

conn.close()
