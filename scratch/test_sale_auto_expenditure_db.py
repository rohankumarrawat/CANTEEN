import os
import sqlite3
import datetime as _dt

def get_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    return conn

def run_test():
    print("Starting automated database unit test for sale auto-expenditure and ingredient stock deductions...")
    
    date_str = "2026-06-17"
    qty_prepared = 20
    qty_sold = 15
    qty_staff = 2
    qty_samp = 1
    sp_val = 100.0

    with get_db() as conn:
        # Fetch active menu item with recipes
        menu_item = conn.execute(
            "SELECT m.id, m.name, m.sp, m.cogs "
            "FROM menu m "
            "WHERE m.active=1 "
            "AND EXISTS (SELECT 1 FROM recipes r WHERE r.menu_id=m.id) "
            "LIMIT 1"
        ).fetchone()
        
        if not menu_item:
            print("❌ No active menu item with recipes found for testing!")
            return
            
        mid = menu_item["id"]
        meal_name = menu_item["name"]
        cogs_per = menu_item["cogs"] if menu_item["cogs"] else 0.0
        
        print(f"Selected menu item: {meal_name} (ID: {mid}, COGS per plate: {cogs_per})")
        
        recipes = conn.execute(
            "SELECT r.menu_id, r.qty_per_unit, i.id as inv_id, i.item, i.cp "
            "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
            "WHERE r.menu_id=?", (mid,)
        ).fetchall()
        
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        try:
            # Set high initial stock for recipe items to prevent clamping to 0
            for r in recipes:
                conn.execute("UPDATE inventory SET stock = 1000.0 WHERE id = ?", (r["inv_id"],))

            # Capture initial inventory (which is now 1000.0)
            initial_stock = {}
            for r in recipes:
                initial_stock[r["inv_id"]] = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]

            print("\n--- TEST ADD SALE (AUTO COGS & EXPENDITURE) ---")
            
            # Calculate cogs automatically
            new_cogs = round(cogs_per * qty_prepared, 2)
            payment_str = f"Cash: {int(sp_val * qty_sold)}, UPI: 0, Card: 0"
            wastage_val = max(0, qty_prepared - (qty_sold + qty_staff + qty_samp))

            # 1. Deduct ingredients stock
            for r in recipes:
                deduct = r["qty_per_unit"] * qty_prepared
                conn.execute("UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id = ?", (deduct, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (date_str, r["inv_id"], -deduct, f"Daily menu: {meal_name} (Sale) x{qty_prepared}")
                )

            # 2. Insert sales record
            conn.execute(
                "INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment, staff, samples) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (date_str, mid, meal_name, sp_val, qty_sold, wastage_val, new_cogs, payment_str, qty_staff, qty_samp)
            )
            sale_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # 3. Insert batch_prep record
            conn.execute(
                "INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                (date_str, mid, qty_prepared)
            )

            # 4. Insert expenditure
            if new_cogs > 0:
                conn.execute(
                    "INSERT INTO expenditure (date, amount, category, notes) VALUES (?,?,?,?)",
                    (date_str, new_cogs, "Raw Materials", f"Auto-expenditure for {meal_name} batch")
                )

            # Verify insertion and auto cogs calculation
            sale_row = conn.execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
            assert sale_row["cogs"] == new_cogs
            print(f"✅ Sale cogs: {sale_row['cogs']} matches calculated: {new_cogs}")
            
            exp_row = conn.execute("SELECT * FROM expenditure WHERE date=? AND category='Raw Materials' AND notes=?", (date_str, f"Auto-expenditure for {meal_name} batch")).fetchone()
            assert exp_row is not None
            assert exp_row["amount"] == new_cogs
            print(f"✅ Expenditure record matches calculated cogs: {exp_row['amount']}")

            # Verify ingredient stock deduction
            for r in recipes:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                expected_stock = max(0.0, initial_stock[r["inv_id"]] - (r["qty_per_unit"] * qty_prepared))
                assert abs(stock_val - expected_stock) < 1e-5
            print("✅ Ingredient stocks correctly deducted")


            print("\n--- TEST EDIT SALE (AUTO COGS & EXPENDITURE UPDATE) ---")
            
            # Edit: change qty_prepared to 30
            new_qty_prepared = 30
            updated_cogs = round(cogs_per * new_qty_prepared, 2)
            updated_wastage_val = max(0, new_qty_prepared - (qty_sold + qty_staff + qty_samp))
            
            # Delta-wise stock adjustment (same meal item)
            for r in recipes:
                deduct_delta = r["qty_per_unit"] * (new_qty_prepared - qty_prepared)
                conn.execute("UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id = ?", (deduct_delta, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (date_str, r["inv_id"], -deduct_delta, f"Daily menu edit: {meal_name} (Sale) ({qty_prepared} -> {new_qty_prepared})")
                )

            # Update sales record cogs and wastage
            conn.execute(
                "UPDATE sales SET cogs=?, wastage=? WHERE id=?",
                (updated_cogs, updated_wastage_val, sale_id)
            )

            # Update batch_prep
            conn.execute(
                "UPDATE batch_prep SET qty_prepared=? WHERE date=? AND menu_id=?",
                (new_qty_prepared, date_str, mid)
            )

            # Sync expenditure
            old_exp_notes = f"Auto-expenditure for {meal_name} batch"
            new_exp_notes = f"Auto-expenditure for {meal_name} batch"
            exp_exists = conn.execute(
                "SELECT id FROM expenditure WHERE date = ? AND category = 'Raw Materials' AND notes LIKE ?",
                (date_str, f"%{meal_name}%")
            ).fetchone()
            if exp_exists:
                if updated_cogs > 0:
                    conn.execute(
                        "UPDATE expenditure SET amount = ?, notes = ? WHERE id = ?",
                        (updated_cogs, new_exp_notes, exp_exists["id"])
                    )
                else:
                    conn.execute("DELETE FROM expenditure WHERE id = ?", (exp_exists["id"],))

            # Verify update
            sale_row_edited = conn.execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
            assert sale_row_edited["cogs"] == updated_cogs
            print(f"✅ Edited sale cogs: {sale_row_edited['cogs']} matches calculated: {updated_cogs}")
            
            exp_row_edited = conn.execute("SELECT * FROM expenditure WHERE date=? AND category='Raw Materials' AND notes=?", (date_str, new_exp_notes)).fetchone()
            assert exp_row_edited is not None
            assert exp_row_edited["amount"] == updated_cogs
            print(f"✅ Edited expenditure amount matches updated cogs: {exp_row_edited['amount']}")

            for r in recipes:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                expected_stock = max(0.0, initial_stock[r["inv_id"]] - (r["qty_per_unit"] * new_qty_prepared))
                assert abs(stock_val - expected_stock) < 1e-5
            print("✅ Ingredient stocks correctly updated by delta")


            print("\n--- TEST DELETE SALE (REVERT INGREDIENTS & DELETE EXPENDITURES) ---")
            
            # Revert ingredients stock
            for r in recipes:
                restore_qty = r["qty_per_unit"] * new_qty_prepared
                conn.execute("UPDATE inventory SET stock = stock + ? WHERE id = ?", (restore_qty, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (date_str, r["inv_id"], restore_qty, f"Daily menu delete: {meal_name} (Sale) x{new_qty_prepared} (reverted)")
                )
                
            conn.execute(
                "DELETE FROM expenditure WHERE date = ? AND category = 'Raw Materials' AND notes LIKE ?",
                (date_str, f"%{meal_name}%")
            )
            
            conn.execute("DELETE FROM sales WHERE id=?", (sale_id,))
            conn.execute("DELETE FROM batch_prep WHERE date=? AND menu_id=?", (date_str, mid))

            # Verify deletion
            assert conn.execute("SELECT COUNT(*) FROM sales WHERE id=?", (sale_id,)).fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM batch_prep WHERE date=? AND menu_id=?", (date_str, mid)).fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM expenditure WHERE date=? AND category='Raw Materials' AND notes LIKE ?", (date_str, f"%{meal_name}%")).fetchone()[0] == 0
            
            for r in recipes:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - (initial_stock[r["inv_id"]])) < 1e-5
            print("✅ Ingredient stocks fully restored to initial levels")

            print("\n🎉 ALL SALES AUTO-EXPENDITURE PERSISTENCE TESTS PASSED!")

        except Exception as e:
            print("❌ TEST FAILED WITH EXCEPTION:")
            import traceback
            traceback.print_exc()
            raise e
        finally:
            conn.execute("ROLLBACK")
            print("Database transaction rolled back. Clean state preserved.")

if __name__ == "__main__":
    run_test()
