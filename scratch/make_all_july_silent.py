# Script to move all July 7 and July 8 adjustments to baseline Opening records silently
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Converting all remaining July 7 & 8 adjustments to baseline silently...")
try:
    # 1. Find all remaining adjustments on July 7 and 8
    adjustments = cursor.execute(
        "SELECT id, inv_id, qty_change, date, notes FROM stock_ledger WHERE (date = '2026-07-07' OR date = '2026-07-08') AND transaction_type = 'Adjustment'"
    ).fetchall()
    
    print(f"Found {len(adjustments)} adjustment entries to convert.")
    
    updated_count = 0
    created_count = 0
    
    for adj_id, inv_id, qty_change, date, notes in adjustments:
        # Find the earliest Opening record for this item in stock_ledger
        opening = cursor.execute(
            "SELECT id, qty_change, date FROM stock_ledger WHERE inv_id = ? AND transaction_type = 'Opening' ORDER BY date LIMIT 1",
            (inv_id,)
        ).fetchone()
        
        if opening:
            op_id, op_qty, op_date = opening
            # Update original opening qty
            cursor.execute(
                "UPDATE stock_ledger SET qty_change = ROUND(qty_change + ?, 4) WHERE id = ?",
                (qty_change, op_id)
            )
            # Update inventory.opening
            cursor.execute(
                "UPDATE inventory SET opening = ROUND(opening + ?, 4) WHERE id = ?",
                (qty_change, inv_id)
            )
            updated_count += 1
        else:
            # Create new baseline Opening
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
            created_count += 1
            
        # Delete the adjustment entry
        cursor.execute("DELETE FROM stock_ledger WHERE id = ?", (adj_id,))

    # 2. Sync inventory stock to keep everything consistent
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
    print(f"  - Original opening entries updated: {updated_count}")
    print(f"  - New baseline opening entries created: {created_count}")
    print(f"  - Removed all July 7 & July 8 adjustment traces.")

except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e} - Changes rolled back.")
    raise
finally:
    conn.close()
