# Script to convert July 7 adjustments into silent baseline updates
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Starting transaction to make stock updates silent...")
try:
    # 1. Find all adjustments we created on July 7, 2026
    adjustments = cursor.execute(
        "SELECT id, inv_id, qty_change FROM stock_ledger WHERE date = '2026-07-07' AND notes = 'Stock alignment for 07 July 2026'"
    ).fetchall()
    
    print(f"Found {len(adjustments)} adjustment entries to convert.")
    
    updated_count = 0
    created_count = 0
    
    for adj_id, inv_id, qty_change in adjustments:
        # Find the earliest Opening record for this item in stock_ledger
        opening = cursor.execute(
            "SELECT id, qty_change, date FROM stock_ledger WHERE inv_id = ? AND transaction_type = 'Opening' ORDER BY date LIMIT 1",
            (inv_id,)
        ).fetchone()
        
        if opening:
            op_id, op_qty, op_date = opening
            # Update the original opening qty by adding the delta
            cursor.execute(
                "UPDATE stock_ledger SET qty_change = ROUND(qty_change + ?, 4) WHERE id = ?",
                (qty_change, op_id)
            )
            # Also update inventory.opening if it's the main baseline
            cursor.execute(
                "UPDATE inventory SET opening = ROUND(opening + ?, 4) WHERE id = ?",
                (qty_change, inv_id)
            )
            print(f"  Item ID {inv_id}: Added {qty_change:+.3f} to original Opening on {op_date}")
            updated_count += 1
        else:
            # No Opening record exists, create one at the baseline start date (e.g. 2026-04-30)
            baseline_date = "2026-04-30"
            cursor.execute(
                "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                "VALUES (?, ?, 'Opening', ?, 'Initial opening stock')",
                (baseline_date, inv_id, qty_change)
            )
            cursor.execute(
                "UPDATE inventory SET opening = ROUND(opening + ?, 4) WHERE id = ?",
                (qty_change, inv_id)
            )
            print(f"  Item ID {inv_id}: Created new baseline Opening of {qty_change:.3f} on {baseline_date}")
            created_count += 1
            
        # Delete the July 7 adjustment entry
        cursor.execute("DELETE FROM stock_ledger WHERE id = ?", (adj_id,))

    # 2. Run sync_inventory_stock to verify/recalculate all items' stock levels
    cursor.execute("""
        UPDATE inventory
        SET stock = COALESCE((
            SELECT SUM(qty_change)
            FROM stock_ledger
            WHERE inv_id = inventory.id
        ), 0)
    """)
    
    conn.commit()
    print(f"\n✅ SUCCESS: Silent stock update completed.")
    print(f"  - Original opening entries updated: {updated_count}")
    print(f"  - New baseline opening entries created: {created_count}")
    print(f"  - July 7 adjustment traces deleted successfully.")

except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e} - Changes rolled back.")
    raise
finally:
    conn.close()
