# Script to update July 8 spellings and add Paneer stock silently
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

DATE = "2026-07-08"

print("Updating July 8 spellings in sales and expenditure tables...")
try:
    # 1. Update sales meal names
    sales_updates = [
        ("Lahori Zeera (LAHORI ZEE)", "Lahori Zeera (Lahori Zeera)"),
        ("Amul Cool (AMUL COOL)", "Amul Kool (Amul Kool)"),
        ("Dahi (DAHI)", "Dahi (Dahi)"),
        ("Chach (CHACH)", "Chach (Chach)")
    ]
    for old_name, new_name in sales_updates:
        cursor.execute(
            "UPDATE sales SET meal = ? WHERE date = ? AND meal = ?",
            (new_name, DATE, old_name)
        )
        print(f"  Sales table update: '{old_name}' -> '{new_name}' (row count: {cursor.rowcount})")

    # 2. Update expenditure notes
    exp_updates = [
        ("Auto-expenditure for DAHI batch", "Auto-expenditure for Dahi batch"),
        ("Auto-expenditure for CHACH batch", "Auto-expenditure for Chach batch"),
        ("Auto-expenditure for AMUL COOL batch", "Auto-expenditure for Amul Kool batch"),
        ("Auto-expenditure for LAHORI ZEE batch", "Auto-expenditure for Lahori Zeera batch")
    ]
    for old_notes, new_notes in exp_updates:
        cursor.execute(
            "UPDATE expenditure SET notes = ? WHERE date = ? AND notes = ?",
            (new_notes, DATE, old_notes)
        )
        print(f"  Expenditure table update: '{old_notes}' -> '{new_notes}' (row count: {cursor.rowcount})")

    # 3. Update Paneer stock silently (bought 13kgs at same price 250.0)
    print("\nUpdating Paneer stock silently (bought 13kgs)...")
    paneer_inv = cursor.execute("SELECT id, stock, opening FROM inventory WHERE item = 'Paneer'").fetchone()
    if paneer_inv:
        p_id, p_stock, p_opening = paneer_inv
        # Get earliest Opening ledger record for Paneer
        p_ledger_op = cursor.execute(
            "SELECT id, qty_change FROM stock_ledger WHERE inv_id = ? AND transaction_type = 'Opening' ORDER BY date LIMIT 1",
            (p_id,)
        ).fetchone()
        
        if p_ledger_op:
            op_id, op_qty = p_ledger_op
            # Update the baseline Opening record to add 13.0 kgs
            cursor.execute(
                "UPDATE stock_ledger SET qty_change = ROUND(qty_change + 13.0, 4) WHERE id = ?",
                (op_id,)
            )
            # Update inventory.opening
            cursor.execute(
                "UPDATE inventory SET opening = ROUND(opening + 13.0, 4) WHERE id = ?",
                (p_id,)
            )
            print(f"  Updated Paneer baseline Opening in ledger from {op_qty} to {op_qty + 13.0}")
            
            # Sync inventory stock
            cursor.execute("""
                UPDATE inventory
                SET stock = COALESCE((
                    SELECT SUM(qty_change)
                    FROM stock_ledger
                    WHERE inv_id = inventory.id
                ), 0)
                WHERE id = ?
            """, (p_id,))
            
            new_stock = cursor.execute("SELECT stock FROM inventory WHERE id = ?", (p_id,)).fetchone()[0]
            print(f"  New Paneer Stock in inventory: {new_stock} (expected: 13.0)")
        else:
            print("  ❌ Error: Paneer baseline Opening record not found in ledger!")
    else:
        print("  ❌ Error: Paneer not found in inventory table!")

    conn.commit()
    print("\n✅ Successfully completed updates.")

except Exception as e:
    conn.rollback()
    print(f"❌ ERROR: {e}")
    raise
finally:
    conn.close()
