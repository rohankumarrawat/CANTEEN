# Script to move July 8 ledger entries to July 7 and remove any July 8 expenditures
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Moving July 8 entries to July 7...")
try:
    # 1. Update stock_ledger dates
    cursor.execute(
        "UPDATE stock_ledger SET date = '2026-07-07' WHERE date = '2026-07-08'"
    )
    ledger_moved = cursor.rowcount
    
    # 2. Update goods_received dates (if any)
    cursor.execute(
        "UPDATE goods_received SET date = '2026-07-07' WHERE date = '2026-07-08'"
    )
    goods_moved = cursor.rowcount

    # 3. Delete any expenditure records on July 8
    cursor.execute(
        "DELETE FROM expenditure WHERE date = '2026-07-08'"
    )
    exp_deleted = cursor.rowcount

    # 4. Sync inventory stock to keep everything consistent
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
    print(f"  - Moved {ledger_moved} stock ledger entries from July 8 to July 7.")
    print(f"  - Moved {goods_moved} goods received entries from July 8 to July 7.")
    print(f"  - Deleted {exp_deleted} expenditure records on July 8.")

except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e} - Changes rolled back.")
    raise
finally:
    conn.close()
