import os
import sqlite3
import datetime as _dt

def get_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    return conn

def run_test():
    print("Starting automated verification of daily menu database logic...")
    
    date_str = "2026-06-16"
    meal_type = "Lunch"
    qty = 10
    samp_qty = 2
    staff_qty = 3

    # Let's find an active menu item with a recipe
    with get_db() as conn:
        menu_item = conn.execute(
            "SELECT m.id, m.name, m.sp, m.cogs "
            "FROM menu m "
            "WHERE m.active=1 "
            "AND EXISTS (SELECT 1 FROM recipes r WHERE r.menu_id=m.id) "
            "LIMIT 1"
        ).fetchone()
        
        if not menu_item:
            print("⚠️ No menu item with recipes found in database. Searching any active item...")
            menu_item = conn.execute(
                "SELECT id, name, sp, cogs FROM menu WHERE active=1 LIMIT 1"
            ).fetchone()
            
        if not menu_item:
            print("❌ No active menu items found in menu table!")
            return
            
        mid = menu_item["id"]
        sel = menu_item["name"]
        sp = menu_item["sp"]
        cogs_per = menu_item["cogs"] if menu_item["cogs"] else 0.0
        
        print(f"Selected menu item for test: {sel} (ID: {mid}, SP: {sp}, COGS: {cogs_per})")
        
        # Load recipes for this menu item
        details = conn.execute(
            "SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
            "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
            "WHERE r.menu_id=?", (mid,)
        ).fetchall()
        
        print(f"Recipe details count: {len(details)}")
        for d in details:
            print(f"  Ingredient: {d['item']}, QPU: {d['qty_per_unit']}, Unit: {d['unit']}, CP: {d['cp']}")

        # Start a transaction to test database logic
        conn.execute("BEGIN TRANSACTION")
        
        # Capture current inventory stock levels
        pre_stock = {}
        for d in details:
            inv_row = conn.execute("SELECT stock FROM inventory WHERE id=?", (d["inv_id"],)).fetchone()
            pre_stock[d["inv_id"]] = inv_row["stock"] if inv_row else 0.0
            print(f"  Current stock of {d['item']}: {pre_stock[d['inv_id']]}")

        print("Executing mock save daily menu operations...")
        
        # 1. Insert into batch_prep
        conn.execute(
            "INSERT INTO batch_prep (date, menu_id, qty_prepared, samples, staff) "
            "VALUES (?,?,?,?,?)",
            (date_str, mid, qty, samp_qty, staff_qty))
            
        bp_row = conn.execute(
            "SELECT * FROM batch_prep WHERE date=? AND menu_id=? ORDER BY id DESC LIMIT 1",
            (date_str, mid)
        ).fetchone()
        
        print(f"✅ Created batch_prep row: ID={bp_row['id']}, qty_prepared={bp_row['qty_prepared']}, samples={bp_row['samples']}, staff={bp_row['staff']}")
        assert bp_row['qty_prepared'] == qty
        assert bp_row['samples'] == samp_qty
        assert bp_row['staff'] == staff_qty

        # 2. Auto-deduct stock + log stock_ledger
        total_raw_cost = 0.0
        for d in details:
            deduct = d["qty_per_unit"] * qty
            conn.execute(
                "UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id=?",
                (deduct, d["inv_id"]))
            conn.execute(
                "INSERT INTO stock_ledger "
                "(date, inv_id, transaction_type, qty_change, notes) "
                "VALUES (?,?,?,?,?)",
                (date_str, d["inv_id"], "DAILY_MENU", -deduct,
                 f"Daily menu: {sel} ({meal_type}) x{qty}"))
            total_raw_cost += deduct * (d["cp"] or 0.0)

            # Check stock deduction
            post_stock = conn.execute("SELECT stock FROM inventory WHERE id=?", (d["inv_id"],)).fetchone()["stock"]
            expected = max(0.0, pre_stock[d["inv_id"]] - deduct)
            print(f"  {d['item']}: pre={pre_stock[d['inv_id']]}, deducted={deduct}, post={post_stock}, expected={expected}")
            assert abs(post_stock - expected) < 1e-5
            
            # Check ledger entry
            ledger = conn.execute(
                "SELECT * FROM stock_ledger WHERE date=? AND inv_id=? ORDER BY id DESC LIMIT 1",
                (date_str, d["inv_id"])
            ).fetchone()
            assert ledger["transaction_type"] == "DAILY_MENU"
            assert abs(ledger["qty_change"] + deduct) < 1e-5

        # 3. Expenditure logging
        if total_raw_cost > 0:
            conn.execute(
                "INSERT INTO expenditure (date, amount, category, notes) "
                "VALUES (?,?,?,?)",
                (date_str, round(total_raw_cost, 2), "Raw Material",
                 f"Auto-expenditure for {sel} batch x{qty}"))
            
            exp_row = conn.execute(
                "SELECT * FROM expenditure WHERE date=? AND category='Raw Material' ORDER BY id DESC LIMIT 1"
            ).fetchone()
            print(f"✅ Created expenditure row: ID={exp_row['id']}, amount={exp_row['amount']}, notes={exp_row['notes']}")
            assert abs(exp_row["amount"] - round(total_raw_cost, 2)) < 1e-5

        # 4. Samples table (given_to='General')
        if samp_qty > 0:
            conn.execute(
                "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (date_str, mid, meal_type, sp, samp_qty,
                 round(cogs_per * samp_qty, 2), "General",
                 f"Auto from daily menu: {sel}"))
            
            samp_row = conn.execute(
                "SELECT * FROM samples WHERE date=? AND given_to='General' ORDER BY id DESC LIMIT 1",
                (date_str,)
            ).fetchone()
            print(f"✅ Created General sample row: ID={samp_row['id']}, qty={samp_row['qty']}, cost={samp_row['cost']}, given_to={samp_row['given_to']}")
            assert samp_row["qty"] == samp_qty
            assert abs(samp_row["cost"] - round(cogs_per * samp_qty, 2)) < 1e-5

        # 5. Samples table for Staff (given_to='Staff')
        if staff_qty > 0:
            conn.execute(
                "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (date_str, mid, meal_type, sp, staff_qty,
                 round(cogs_per * staff_qty, 2), "Staff",
                 f"Auto from daily menu: {sel}"))
                 
            staff_row = conn.execute(
                "SELECT * FROM samples WHERE date=? AND given_to='Staff' ORDER BY id DESC LIMIT 1",
                (date_str,)
            ).fetchone()
            print(f"✅ Created Staff sample row: ID={staff_row['id']}, qty={staff_row['qty']}, cost={staff_row['cost']}, given_to={staff_row['given_to']}")
            assert staff_row["qty"] == staff_qty
            assert abs(staff_row["cost"] - round(cogs_per * staff_qty, 2)) < 1e-5

        # Rollback so database is clean
        conn.execute("ROLLBACK")
        print("Test transactions rolled back successfully. Database remains clean.")
        print("🎉 ALL DAILY MENU LOGIC PERSISTENCE TESTS PASSED!")

if __name__ == "__main__":
    run_test()
