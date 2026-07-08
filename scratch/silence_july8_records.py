# Corrected script to make July 8 database changes completely silent (remove expenditures and ledger traces)
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Converting July 8 transactions into silent baseline updates...")
try:
    # 1. Delete all expenditure records for July 8
    cursor.execute("DELETE FROM expenditure WHERE date = '2026-07-08'")
    exp_deleted = cursor.rowcount
    print(f"Deleted {exp_deleted} expenditure records on July 8.")

    # 2. Delete all goods_received records for July 8
    cursor.execute("DELETE FROM goods_received WHERE date = '2026-07-08'")
    gr_deleted = cursor.rowcount
    print(f"Deleted {gr_deleted} goods_received records on July 8.")

    # 3. Get all ledger entries on July 8 grouped by inv_id
    ledger_summary = cursor.execute("""
        SELECT inv_id, SUM(qty_change) 
        FROM stock_ledger 
        WHERE date = '2026-07-08' 
        GROUP BY inv_id
    """).fetchall()
    
    print(f"Found {len(ledger_summary)} items with July 8 stock changes.")

    updated_count = 0
    created_count = 0

    for inv_id, net_change in ledger_summary:
        # Find the earliest Opening record for this item in stock_ledger before July 8
        opening = cursor.execute(
            "SELECT id, qty_change FROM stock_ledger WHERE inv_id = ? AND transaction_type = 'Opening' AND date < '2026-07-08' ORDER BY date LIMIT 1",
            (inv_id,)
        ).fetchone()

        # Get final BCF stock of the item from inventory table
        bcf = cursor.execute("SELECT stock FROM inventory WHERE id = ?", (inv_id,)).fetchone()[0]

        if opening:
            op_id, op_qty = opening
            # Add the net change to the baseline Opening
            cursor.execute(
                "UPDATE stock_ledger SET qty_change = ROUND(qty_change + ?, 4) WHERE id = ?",
                (net_change, op_id)
            )
            # Update inventory.opening
            cursor.execute(
                "UPDATE inventory SET opening = ROUND(opening + ?, 4) WHERE id = ?",
                (net_change, inv_id)
            )
            updated_count += 1
        else:
            # This is a new item created on July 8! Set its baseline opening stock on 2026-04-30 to exactly BCF
            baseline_date = "2026-04-30"
            cursor.execute(
                "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                "VALUES (?, ?, 'Opening', ?, 'Initial opening stock')",
                (baseline_date, inv_id, bcf)
            )
            cursor.execute(
                "UPDATE inventory SET opening = ROUND(?, 4) WHERE id = ?",
                (bcf, inv_id)
            )
            created_count += 1

    # 4. Delete ALL July 8 ledger entries
    cursor.execute("DELETE FROM stock_ledger WHERE date = '2026-07-08'")
    deleted_ledger = cursor.rowcount
    print(f"Deleted {deleted_ledger} stock_ledger entries from July 8.")

    # 5. Sync inventory stock to keep everything consistent
    cursor.execute("""
        UPDATE inventory
        SET stock = COALESCE((
            SELECT SUM(qty_change)
            FROM stock_ledger
            WHERE inv_id = inventory.id
        ), 0)
    """)

    conn.commit()
    print(f"\n✅ SUCCESS:")
    print(f"  - Baseline opening entries updated: {updated_count}")
    print(f"  - Baseline opening entries created: {created_count}")
    print(f"  - Deleted all July 8 transaction traces and expenditures.")

except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e} - Changes rolled back.")
    raise
finally:
    conn.close()
