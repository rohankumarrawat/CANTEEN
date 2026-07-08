import sqlite3

conn = sqlite3.connect("canteen.db")
conn.row_factory = sqlite3.Row

# Show differences before sync
print("Discrepancies before sync:")
print("-" * 50)
diff_count = 0
for r in conn.execute("SELECT id, item, stock FROM inventory ORDER BY item").fetchall():
    ledger_sum = conn.execute("SELECT SUM(qty_change) FROM stock_ledger WHERE inv_id=?", (r["id"],)).fetchone()[0] or 0.0
    if abs(r["stock"] - ledger_sum) > 0.001:
        print(f"{r['item']}: DB Stock={r['stock']:.2f}, Ledger Sum={ledger_sum:.2f}")
        diff_count += 1

print(f"Total out-of-sync items: {diff_count}")

# Perform the sync
conn.execute("""
    UPDATE inventory
    SET stock = COALESCE((
        SELECT SUM(qty_change)
        FROM stock_ledger
        WHERE inv_id = inventory.id
    ), 0)
""")
conn.commit()

print("\nDifferences after sync:")
print("-" * 50)
diff_count_after = 0
for r in conn.execute("SELECT id, item, stock FROM inventory ORDER BY item").fetchall():
    ledger_sum = conn.execute("SELECT SUM(qty_change) FROM stock_ledger WHERE inv_id=?", (r["id"],)).fetchone()[0] or 0.0
    if abs(r["stock"] - ledger_sum) > 0.001:
        print(f"{r['item']}: DB Stock={r['stock']:.2f}, Ledger Sum={ledger_sum:.2f}")
        diff_count_after += 1
print(f"Total out-of-sync items after: {diff_count_after}")

conn.close()
