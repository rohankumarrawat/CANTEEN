import sqlite3

conn = sqlite3.connect("canteen.db")
conn.row_factory = sqlite3.Row

start = "2026-04-30"
end = "2026-04-30"

inv_query = """
    SELECT
        i.item, i.cat, i.unit, i.min_lvl,
        COALESCE((SELECT SUM(qty_change) FROM stock_ledger
                   WHERE inv_id = i.id AND (date < ? OR (date = ? AND transaction_type = 'Opening'))), 0) AS opening,
        COALESCE((SELECT SUM(qty_change) FROM stock_ledger
                   WHERE inv_id = i.id AND date >= ? AND date <= ?
                   AND transaction_type = 'Received'), 0) AS received,
        COALESCE((SELECT SUM(qty_change) FROM stock_ledger
                   WHERE inv_id = i.id AND date <= ?), 0) AS closing
    FROM inventory i
    ORDER BY i.cat, i.item
"""

print(f"Results for range {start} to {end}:")
print("-" * 80)
print(f"{'Item':<25} | {'Cat':<10} | {'Unit':<5} | {'Opening':<10} | {'Received':<10} | {'Closing':<10}")
print("-" * 80)
for r in conn.execute(inv_query, (start, start, start, end, end)).fetchall():
    if r["opening"] != 0 or r["received"] != 0 or r["closing"] != 0:
        print(f"{r['item']:<25} | {r['cat']:<10} | {r['unit']:<5} | {r['opening']:<10.2f} | {r['received']:<10.2f} | {r['closing']:<10.2f}")

conn.close()
