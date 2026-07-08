import sqlite3

conn = sqlite3.connect("canteen.db")
conn.row_factory = sqlite3.Row

print("ITEM | DB STOCK | LEDGER SUM | DIFF | OPENING")
print("-" * 50)
for r in conn.execute("SELECT id, item, stock, opening FROM inventory ORDER BY item").fetchall():
    ledger_sum = conn.execute("SELECT SUM(qty_change) FROM stock_ledger WHERE inv_id=?", (r["id"],)).fetchone()[0] or 0.0
    diff = r["stock"] - ledger_sum
    if abs(diff) > 0.01 or r["stock"] < 0:
        print(f"{r['item']}: DB={r['stock']:.2f}, Ledger={ledger_sum:.2f}, Diff={diff:.2f}, Opening={r['opening']:.2f}")

conn.close()
