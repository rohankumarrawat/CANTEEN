import os
import sqlite3
import datetime as _dt
from app import parse_payment_field

def get_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    return conn

def run_test():
    print("Starting database unit test for sales modal ADD, EDIT and DELETE...")
    
    d = "2026-06-16"
    
    with get_db() as conn:
        # Get two active items with recipes
        items = conn.execute(
            "SELECT m.id, m.name, m.sp, m.cogs "
            "FROM menu m "
            "WHERE m.active=1 "
            "AND EXISTS (SELECT 1 FROM recipes r WHERE r.menu_id=m.id) "
            "LIMIT 2"
        ).fetchall()
        
        if len(items) < 2:
            print("❌ Need at least two items with recipes in DB to run the test!")
            return
            
        item1, item2 = items[0], items[1]
        
        # Test item 1
        mid1 = item1["id"]
        meal1 = item1["name"]
        sp1 = item1["sp"]
        cogs_per1 = item1["cogs"] if item1["cogs"] else 0.0
        
        # Test item 2
        mid2 = item2["id"]
        meal2 = item2["name"]
        sp2 = item2["sp"]
        cogs_per2 = item2["cogs"] if item2["cogs"] else 0.0
        
        print(f"Item 1: {meal1} (ID: {mid1})")
        print(f"Item 2: {meal2} (ID: {mid2})")
        
        recipes1 = conn.execute(
            "SELECT r.inv_id, r.qty_per_unit, i.item, i.cp FROM recipes r JOIN inventory i ON i.id=r.inv_id WHERE r.menu_id=?",
            (mid1,)
        ).fetchall()
        
        recipes2 = conn.execute(
            "SELECT r.inv_id, r.qty_per_unit, i.item, i.cp FROM recipes r JOIN inventory i ON i.id=r.inv_id WHERE r.menu_id=?",
            (mid2,)
        ).fetchall()
        
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        try:
            # Capture initial stocks
            initial_stock1 = {}
            for r in recipes1:
                initial_stock1[r["inv_id"]] = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                
            initial_stock2 = {}
            for r in recipes2:
                initial_stock2[r["inv_id"]] = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                
            print("\n--- TEST ADD SALE ---")
            prep = 20
            sold = 15
            staff = 3
            samp = 2
            cogs = 120.0
            pmt = "Cash: 1050, UPI: 0, Card: 0"
            wast = prep - (sold + staff + samp) # 20 - 20 = 0
            
            # 1. Deduct ingredients stock
            for r in recipes1:
                deduct = r["qty_per_unit"] * prep
                conn.execute("UPDATE inventory SET stock = stock - ? WHERE id=?", (deduct, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (d, r["inv_id"], -deduct, f"Daily menu: {meal1} (Sale) x{prep}")
                )
                
            # 2. Insert sales record
            conn.execute(
                "INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment, staff, samples) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (d, mid1, meal1, sp1, sold, wast, cogs, pmt, staff, samp)
            )
            sale_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            
            # 3. Insert batch_prep record
            conn.execute(
                "INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                (d, mid1, prep)
            )
            
            # 4. Insert expenditure
            conn.execute(
                "INSERT INTO expenditure (date, amount, category, notes) VALUES (?, ?, 'Raw Materials', ?)",
                (d, cogs, f"Auto-expenditure for {meal1} batch")
            )
            
            # 5. Insert samples
            conn.execute(
                "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                "VALUES (?, ?, ?, ?, ?, ?, 'General', ?)",
                (d, mid1, meal1, sp1, samp, round(cogs_per1 * samp, 2), f"Auto from sales: {meal1}")
            )
            conn.execute(
                "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                "VALUES (?, ?, ?, ?, ?, ?, 'Staff', ?)",
                (d, mid1, meal1, sp1, staff, round(cogs_per1 * staff, 2), f"Auto from sales: {meal1}")
            )
            
            # Verify creations
            s_row = conn.execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
            assert s_row["meal"] == meal1
            assert s_row["staff"] == staff
            assert s_row["samples"] == samp
            assert s_row["wastage"] == wast
            
            # Verify stock deduction
            for r in recipes1:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - (initial_stock1[r["inv_id"]] - r["qty_per_unit"] * prep)) < 1e-5
                
            print("Add sale verified successfully!")

            print("\n--- TEST EDIT SALE (SAME ITEM, NEW QUANTITIES) ---")
            new_prep = 30
            new_sold = 22
            new_staff = 5
            new_samp = 3
            new_cogs = 180.0
            new_pmt = "Cash: 1000, UPI: 540, Card: 0" # total 1540 (70 * 22)
            new_wast = new_prep - (new_sold + new_staff + new_samp) # 30 - 30 = 0
            
            # 1. Adjust ingredients stock delta-wise (delta is +10 prep)
            for r in recipes1:
                deduct_delta = r["qty_per_unit"] * (new_prep - prep)
                conn.execute("UPDATE inventory SET stock = stock - ? WHERE id=?", (deduct_delta, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (d, r["inv_id"], -deduct_delta, f"Daily menu edit: {meal1} (Sale) ({prep} -> {new_prep})")
                )
                
            # 2. Update sales record
            conn.execute(
                "UPDATE sales SET meal=?, sp=?, sold=?, wastage=?, cogs=?, payment=?, staff=?, samples=? WHERE id=?",
                (meal1, sp1, new_sold, new_wast, new_cogs, new_pmt, new_staff, new_samp, sale_id)
            )
            
            # 3. Update batch_prep qty
            conn.execute(
                "UPDATE batch_prep SET qty_prepared=? WHERE date=? AND menu_id=?",
                (new_prep, d, mid1)
            )
            
            # 4. Sync expenditure
            conn.execute(
                "UPDATE expenditure SET amount=? WHERE date=? AND notes LIKE ?",
                (new_cogs, d, f"%{meal1}%")
            )
            
            # 5. Sync samples
            conn.execute(
                "UPDATE samples SET qty=?, cost=? WHERE date=? AND menu_id=? AND given_to='General' AND notes=?",
                (new_samp, round(cogs_per1 * new_samp, 2), d, mid1, f"Auto from sales: {meal1}")
            )
            conn.execute(
                "UPDATE samples SET qty=?, cost=? WHERE date=? AND menu_id=? AND given_to='Staff' AND notes=?",
                (new_staff, round(cogs_per1 * new_staff, 2), d, mid1, f"Auto from sales: {meal1}")
            )
            
            # Verify edits
            s_row = conn.execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
            assert s_row["sold"] == new_sold
            assert s_row["staff"] == new_staff
            assert s_row["samples"] == new_samp
            assert s_row["payment"] == new_pmt
            
            for r in recipes1:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - (initial_stock1[r["inv_id"]] - r["qty_per_unit"] * new_prep)) < 1e-5
                
            print("Edit sale (same item) verified successfully!")

            print("\n--- TEST EDIT SALE (CHANGE TO ITEM 2) ---")
            # Now change the meal item to meal2!
            # 1. Revert full ingredients stock of item 1
            for r in recipes1:
                restore = r["qty_per_unit"] * new_prep
                conn.execute("UPDATE inventory SET stock = stock + ? WHERE id=?", (restore, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (d, r["inv_id"], restore, f"Daily menu edit (Revert old item): {meal1} (Sale) x{new_prep}")
                )
                
            # 2. Deduct full ingredients stock of item 2
            # Let's say prep for item2 is 25, sold is 20, staff is 2, samples is 3
            prep2 = 25
            sold2 = 20
            staff2 = 2
            samp2 = 3
            cogs2 = 150.0
            pmt2 = f"Cash: {sp2 * sold2}, UPI: 0, Card: 0"
            wast2 = prep2 - (sold2 + staff2 + samp2) # 0
            
            for r in recipes2:
                deduct = r["qty_per_unit"] * prep2
                conn.execute("UPDATE inventory SET stock = stock - ? WHERE id=?", (deduct, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (d, r["inv_id"], -deduct, f"Daily menu edit (New item): {meal2} (Sale) x{prep2}")
                )
                
            # 3. Update sales record
            conn.execute(
                "UPDATE sales SET meal=?, sp=?, sold=?, wastage=?, cogs=?, payment=?, staff=?, samples=?, menu_id=? WHERE id=?",
                (meal2, sp2, sold2, wast2, cogs2, pmt2, staff2, samp2, mid2, sale_id)
            )
            
            # 4. Update batch_prep menu_id and qty
            conn.execute(
                "UPDATE batch_prep SET qty_prepared=?, menu_id=? WHERE date=? AND menu_id=?",
                (prep2, mid2, d, mid1)
            )
            
            # 5. Sync expenditure (update notes to meal2)
            conn.execute(
                "UPDATE expenditure SET amount=?, notes=? WHERE date=? AND notes LIKE ?",
                (cogs2, f"Auto-expenditure for {meal2} batch", d, f"%{meal1}%")
            )
            
            # 6. Sync samples (update notes and menu_id)
            # General
            conn.execute(
                "UPDATE samples SET qty=?, cost=?, notes=?, menu_id=?, meal=? WHERE date=? AND menu_id=? AND given_to='General'",
                (samp2, round(cogs_per2 * samp2, 2), f"Auto from sales: {meal2}", mid2, meal2, d, mid1)
            )
            # Staff
            conn.execute(
                "UPDATE samples SET qty=?, cost=?, notes=?, menu_id=?, meal=? WHERE date=? AND menu_id=? AND given_to='Staff'",
                (staff2, round(cogs_per2 * staff2, 2), f"Auto from sales: {meal2}", mid2, meal2, d, mid1)
            )
            
            # Verify changes to Item 2
            s_row = conn.execute("SELECT * FROM sales WHERE id=?", (sale_id,)).fetchone()
            assert s_row["meal"] == meal2
            assert s_row["menu_id"] == mid2
            assert s_row["sold"] == sold2
            
            # Verify Item 1 stock returned to initial
            for r in recipes1:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - initial_stock1[r["inv_id"]]) < 1e-5
                
            # Verify Item 2 stock deducted correctly
            for r in recipes2:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - (initial_stock2[r["inv_id"]] - r["qty_per_unit"] * prep2)) < 1e-5
                
            print("Edit sale (change item) verified successfully!")

            print("\n--- TEST DELETE SALE ---")
            # 1. Fetch menu recipes to return ingredients stock for item 2
            for r in recipes2:
                restore_qty = r["qty_per_unit"] * prep2
                conn.execute("UPDATE inventory SET stock = stock + ? WHERE id = ?", (restore_qty, r["inv_id"]))
                conn.execute(
                    "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                    "VALUES (?, ?, 'Batch_Prep', ?, ?)",
                    (d, r["inv_id"], restore_qty, f"Daily menu delete: {meal2} (Sale) x{prep2} (reverted)")
                )
                
            # 2. Delete expenditure
            conn.execute(
                "DELETE FROM expenditure WHERE date = ? AND category = 'Raw Materials' AND notes LIKE ?",
                (d, f"%{meal2}%")
            )
            
            # 3. Delete samples
            conn.execute(
                "DELETE FROM samples WHERE date = ? AND menu_id = ? AND notes LIKE ?",
                (d, mid2, f"Auto from sales: {meal2}")
            )
            
            # 4. Delete batch_prep
            conn.execute("DELETE FROM batch_prep WHERE date=? AND menu_id=?", (d, mid2))
            
            # 5. Delete sale record
            conn.execute("DELETE FROM sales WHERE id=?", (sale_id,))
            
            # Verify deletions and stock restoration
            assert conn.execute("SELECT COUNT(*) FROM sales WHERE id=?", (sale_id,)).fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM batch_prep WHERE date=? AND menu_id=?", (d, mid2)).fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM samples WHERE date=? AND menu_id=?", (d, mid2)).fetchone()[0] == 0
            
            for r in recipes2:
                stock_val = conn.execute("SELECT stock FROM inventory WHERE id=?", (r["inv_id"],)).fetchone()["stock"]
                assert abs(stock_val - initial_stock2[r["inv_id"]]) < 1e-5
                
            print("Delete sale verified successfully!")
            print("\n🎉 ALL SALES EDIT/DELETE PERSISTENCE TESTS PASSED!")
            
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
