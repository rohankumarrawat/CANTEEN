import os
import sqlite3
import datetime as _dt

def get_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    return conn

def run_test():
    print("Starting automated database unit test for daily menu EDIT and DELETE...")
    
    date_str = "2026-06-16"
    meal_type = "Lunch"
    qty = 10
    samp_qty = 2
    staff_qty = 3

    with get_db() as conn:
        menu_item = conn.execute(
            "SELECT m.id, m.name, m.sp, m.cogs "
            "FROM menu m "
            "WHERE m.active=1 "
            "AND EXISTS (SELECT 1 FROM recipes r WHERE r.menu_id=m.id) "
            "LIMIT 1"
        ).fetchone()
        
        if not menu_item:
            print("❌ No menu item with recipes found for testing!")
            return
            
        mid = menu_item["id"]
        sel = menu_item["name"]
        sp = menu_item["sp"]
        cogs_per = menu_item["cogs"] if menu_item["cogs"] else 0.0
        
        print(f"Selected menu item: {sel} (ID: {mid})")
        
        recipes = conn.execute(
            "SELECT r.menu_id, r.qty_per_unit, i.id as inv_id, i.item, i.cp "
            "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
            "WHERE r.menu_id=?", (mid,)
        ).fetchall()
        
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        try:
            # Capture initial inventory
            initial_stock = {}
            for r in recipes:
                initial_stock[r["inv_id"]] = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]

            print("\n--- TEST SAVE DAILY MENU ---")
            # Create daily menu entry
            conn.execute(
                "INSERT INTO batch_prep (date, menu_id, qty_prepared, samples, staff) "
                "VALUES (?,?,?,?,?)",
                (date_str, mid, qty, samp_qty, staff_qty))
            
            bp_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            
            # Deduct stock & log ledger
            total_raw = 0.0
            for r in recipes:
                deduct = r["qty_per_unit"] * qty
                conn.execute("UPDATE inventory SET stock = stock - ? WHERE id=?", (deduct, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'DAILY_MENU', ?, ?)",
                    (date_str, r["inv_id"], -deduct, f"Daily menu: {sel} ({meal_type}) x{qty}")
                )
                total_raw += deduct * (r["cp"] or 0.0)
                
            # Log expenditure
            if total_raw > 0:
                conn.execute(
                    "INSERT INTO expenditure (date, amount, category, notes) "
                    "VALUES (?, ?, 'Raw Material', ?)",
                    (date_str, round(total_raw, 2), f"Auto: {sel} x{qty}")
                )
                
            # General sample
            if samp_qty > 0:
                conn.execute(
                    "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                    "VALUES (?, ?, 'Lunch', ?, ?, ?, 'General', ?)",
                    (date_str, mid, sp, samp_qty, round(cogs_per * samp_qty, 2), f"Auto from daily menu: {sel}")
                )
                
            # Staff sample
            if staff_qty > 0:
                conn.execute(
                    "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                    "VALUES (?, ?, 'Lunch', ?, ?, ?, 'Staff', ?)",
                    (date_str, mid, sp, staff_qty, round(cogs_per * staff_qty, 2), f"Auto from daily menu: {sel}")
                )
                
            # Verify they exist
            assert conn.execute("SELECT COUNT(*) FROM batch_prep WHERE id=?", (bp_id,)).fetchone()[0] == 1
            assert conn.execute("SELECT COUNT(*) FROM expenditure WHERE date=? AND notes=?", (date_str, f"Auto: {sel} x{qty}")).fetchone()[0] == 1
            assert conn.execute("SELECT COUNT(*) FROM samples WHERE date=? AND menu_id=? AND notes=?", (date_str, mid, f"Auto from daily menu: {sel}")).fetchone()[0] == 2
            
            print("Save daily menu verified successfully!")

            print("\n--- TEST EDIT DAILY MENU (DELTA) ---")
            new_qty = 15
            new_samp = 4
            new_staff = 0 # should delete staff samples
            
            delta_qty = new_qty - qty
            new_raw = 0.0
            
            for r in recipes:
                deduct_delta = r["qty_per_unit"] * delta_qty
                conn.execute("UPDATE inventory SET stock = stock - ? WHERE id=?", (deduct_delta, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'DAILY_MENU_EDIT', ?, ?)",
                    (date_str, r["inv_id"], -deduct_delta, f"Daily menu edit: {sel} ({qty} -> {new_qty})")
                )
                new_raw += (r["qty_per_unit"] * new_qty) * (r["cp"] or 0.0)
                
            # Expenditure update
            old_exp_notes = f"Auto: {sel} x{qty}"
            new_exp_notes = f"Auto: {sel} x{new_qty}"
            exp_exists = conn.execute(
                "SELECT id FROM expenditure WHERE date = ? AND category = 'Raw Material' AND notes = ?",
                (date_str, old_exp_notes)
            ).fetchone()
            
            if exp_exists:
                conn.execute(
                    "UPDATE expenditure SET amount = ?, notes = ? WHERE id = ?",
                    (round(new_raw, 2), new_exp_notes, exp_exists["id"])
                )
                
            # Samples update
            samp_notes = f"Auto from daily menu: {sel}"
            
            # General Samples
            gen_exists = conn.execute(
                "SELECT id FROM samples WHERE date = ? AND menu_id = ? AND given_to = 'General' AND notes = ?",
                (date_str, mid, samp_notes)
            ).fetchone()
            if gen_exists:
                conn.execute(
                    "UPDATE samples SET qty = ?, cost = ? WHERE id = ?",
                    (new_samp, round(cogs_per * new_samp, 2), gen_exists["id"])
                )
                
            # Staff Meals (should delete because new_staff is 0)
            staff_exists = conn.execute(
                "SELECT id FROM samples WHERE date = ? AND menu_id = ? AND given_to = 'Staff' AND notes = ?",
                (date_str, mid, samp_notes)
            ).fetchone()
            if staff_exists:
                conn.execute("DELETE FROM samples WHERE id = ?", (staff_exists["id"],))
                
            # Update batch_prep
            conn.execute(
                "UPDATE batch_prep SET qty_prepared = ?, samples = ?, staff = ? WHERE id = ?",
                (new_qty, new_samp, new_staff, bp_id)
            )
            
            # Verify edits
            bp_edited = conn.execute("SELECT * FROM batch_prep WHERE id=?", (bp_id,)).fetchone()
            assert bp_edited["qty_prepared"] == new_qty
            assert bp_edited["samples"] == new_samp
            assert bp_edited["staff"] == new_staff
            
            # Verify expenditure notes and amount
            exp_edited = conn.execute("SELECT * FROM expenditure WHERE date=? AND notes=?", (date_str, new_exp_notes)).fetchone()
            assert exp_edited is not None
            assert abs(exp_edited["amount"] - round(new_raw, 2)) < 1e-5
            
            # Verify general samples quantity, staff samples deleted
            assert conn.execute("SELECT qty FROM samples WHERE date=? AND menu_id=? AND given_to='General' AND notes=?", (date_str, mid, samp_notes)).fetchone()["qty"] == new_samp
            assert conn.execute("SELECT COUNT(*) FROM samples WHERE date=? AND menu_id=? AND given_to='Staff' AND notes=?", (date_str, mid, samp_notes)).fetchone()[0] == 0
            
            # Verify inventory stock delta-wise
            for r in recipes:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                expected_stock = initial_stock[r["inv_id"]] - (r["qty_per_unit"] * new_qty)
                assert abs(stock_val - expected_stock) < 1e-5
                
            print("Edit daily menu verified successfully!")

            print("\n--- TEST DELETE DAILY MENU ---")
            # 1. Fetch menu recipes to return ingredients stock
            for r in recipes:
                restore_qty = r["qty_per_unit"] * new_qty
                conn.execute("UPDATE inventory SET stock = stock + ? WHERE id = ?", (restore_qty, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'DAILY_MENU_DELETE', ?, ?)",
                    (date_str, r["inv_id"], restore_qty, f"Daily menu delete: {sel} x{new_qty} (reverted)")
                )
                
            # 2. Delete expenditure
            conn.execute(
                "DELETE FROM expenditure WHERE date = ? AND category = 'Raw Material' AND notes = ?",
                (date_str, f"Auto: {sel} x{new_qty}")
            )
            
            # 3. Delete samples
            conn.execute(
                "DELETE FROM samples WHERE date = ? AND menu_id = ? AND notes = ?",
                (date_str, mid, f"Auto from daily menu: {sel}")
            )
            
            # 4. Delete the batch_prep record
            conn.execute("DELETE FROM batch_prep WHERE id = ?", (bp_id,))
            
            # Verify deletions
            assert conn.execute("SELECT COUNT(*) FROM batch_prep WHERE id=?", (bp_id,)).fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM expenditure WHERE date=? AND notes=?", (date_str, new_exp_notes)).fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM samples WHERE date=? AND menu_id=? AND notes=?", (date_str, mid, samp_notes)).fetchone()[0] == 0
            
            # Verify inventory returned to original initial stock levels
            for r in recipes:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - initial_stock[r["inv_id"]]) < 1e-5
                
            print("Delete daily menu verified successfully!")
            print("\n🎉 ALL EDIT AND DELETE DATABASE PERSISTENCE TESTS PASSED!")

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
