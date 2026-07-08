# Script to execute matched stock updates for July 7, 2026
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

# Load the exact matched updates from the map script
from map_stock_updates import matched_updates

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Starting transaction to update stock...")
try:
    updated_count = 0
    for m in matched_updates:
        inv_id = m["id"]
        new_stock = m["new_stock"]
        new_cp = m["new_cp"]
        
        # Get current stock to calculate delta
        row = cursor.execute("SELECT stock FROM inventory WHERE id = ?", (inv_id,)).fetchone()
        cur_stock = row[0] if row else 0.0
        
        # Calculate delta
        delta = new_stock - cur_stock
        
        # 1. Update CP in inventory
        cursor.execute("UPDATE inventory SET cp = ? WHERE id = ?", (new_cp, inv_id))
        
        # 2. If stock has changed, insert Adjustment in stock_ledger
        if abs(delta) > 1e-4:
            cursor.execute(
                "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                "VALUES ('2026-07-07', ?, 'Adjustment', ?, 'Stock alignment for 07 July 2026')",
                (inv_id, delta)
            )
            updated_count += 1
            print(f"  {m['db_name']}: stock adjusted by {delta:+.3f} to reach {new_stock:.3f}, CP updated to Rs. {new_cp:.2f}")
        else:
            print(f"  {m['db_name']}: stock is already {new_stock:.3f}, CP updated to Rs. {new_cp:.2f}")

    # 3. Run sync_inventory_stock to recalculate all items' stock levels
    cursor.execute("""
        UPDATE inventory
        SET stock = COALESCE((
            SELECT SUM(qty_change)
            FROM stock_ledger
            WHERE inv_id = inventory.id
        ), 0)
    """)
    
    conn.commit()
    print(f"\n✅ SUCCESS: Successfully updated CP for {len(matched_updates)} items, and adjusted stock for {updated_count} items.")

except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e} - Changes rolled back.")
    raise
finally:
    conn.close()
