import sqlite3
from datetime import datetime as _dt

DATE = "2026-07-08"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 1370.000, 0.000, 50.000, 31.00, 1550.00, 1320.000, 40920.00),
    ('Rice', 'Kgs', 615.500, 0.000, 35.000, 68.00, 2380.00, 580.500, 39474.00),
    ('Refined Oil (Expensive)', 'Ltr', 20.000, 0.000, 11.500, 180.92, 2080.615, 8.500, 1537.85),
    ('Refined Oil', 'Ltr', 240.000, 0.000, 0.000, 175.00, 0.00, 240.000, 42000.00),
    ('Sarson Dana', 'Kgs', 0.440, 0.000, 0.020, 120.00, 2.40, 0.420, 50.40),
    ('Kali Sarson', 'Kgs', 0.000, 0.000, 0.000, 200.00, 0.00, 0.000, 0.00),
    ('Panch Phuran', 'Kgs', 0.000, 0.000, 0.000, 400.00, 0.00, 0.000, 0.00),
    ('Rajma', 'Kgs', 13.000, 0.000, 13.000, 115.00, 1495.00, 0.000, 0.00),
    ('Rajma (Expensive)', 'Kgs', 80.000, 0.000, 4.000, 125.00, 500.00, 76.000, 9500.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.00, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 52.000, 0.000, 0.000, 80.00, 0.00, 52.000, 4160.00),
    ('Besan Expensive', 'Kgs', 0.000, 0.000, 0.000, 94.50, 0.00, 0.000, 0.00),
    ('Besan', 'Kgs', 50.000, 0.000, 0.000, 90.00, 0.00, 50.000, 4500.00),
    ('Dal Arhar', 'Kgs', 50.000, 0.000, 0.000, 120.00, 0.00, 50.000, 6000.00),
    ('Dal Masoor (s)', 'Kgs', 16.000, 0.000, 0.000, 84.00, 0.00, 16.000, 1344.00),
    ('Urad Dal Chilka', 'Kgs', 0.000, 0.000, 0.000, 110.00, 0.00, 0.000, 0.00),
    ('URD CRD CHILKAT (Expensive)', 'Kgs', 13.000, 0.000, 0.000, 120.00, 0.00, 13.000, 1560.00),
    ('Masoor Dal Malka', 'Kgs', 12.000, 0.000, 0.000, 84.00, 0.00, 12.000, 1008.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 0.000, 115.00, 0.00, 12.000, 1380.00),
    ('Urad Dhuli', 'Kgs', 10.000, 0.000, 0.000, 135.00, 0.00, 10.000, 1350.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 3.450, 0.000, 0.200, 300.00, 60.00, 3.250, 975.00),
    ('Haldi Powder', 'Kgs', 0.100, 0.000, 0.100, 231.00, 23.10, 0.000, 0.00),
    ('Haldi Powder(Expensive)', 'Kgs', 8.000, 0.000, 0.100, 290.00, 29.00, 7.900, 2291.00),
    ('Mirchi Powder(Expensive)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.00, 0.000, 0.00),
    ('Mirchi Powder', 'Kgs', 5.900, 0.000, 0.200, 300.00, 60.00, 5.700, 1710.00),
    ('Dalchini', 'Kgs', 0.270, 0.000, 0.020, 400.00, 8.00, 0.250, 100.00),
    ('Laung', 'Kgs', 0.000, 0.000, 0.000, 1800.00, 0.00, 0.000, 0.00),
    ('Hing', 'Nos', 5.000, 0.000, 1.000, 89.25, 89.25, 4.000, 357.00),
    ('Hing Expensive', 'Pkt', 30.000, 0.000, 0.000, 130.00, 0.00, 30.000, 3900.00),
    ('Kitchen King', 'Kgs', 42.000, 0.000, 0.200, 76.00, 15.20, 41.800, 3176.80),
    ('Deggi Mirch', 'Kgs', 40.000, 0.000, 0.200, 106.00, 21.20, 39.800, 4218.80),
    ('Kasuri Methi', 'Kgs', 0.000, 0.000, 0.000, 700.00, 0.00, 0.000, 0.00),
    ('Kasuri methi (Expensive)', 'Kgs', 0.800, 0.000, 0.050, 200.00, 10.00, 0.750, 150.00),
    ('Garam Masala', 'Kgs', 41.000, 0.000, 0.200, 95.00, 19.00, 40.800, 3876.00),
    ('Salt', 'Kgs', 44.000, 0.000, 2.000, 28.00, 56.00, 42.000, 1176.00),
    ('Dhaniya (s)', 'Kgs', 0.000, 0.000, 0.000, 199.50, 0.00, 0.000, 0.00),
    ('Jeera Powder', 'Kgs', 24.900, 0.000, 0.200, 70.00, 14.00, 24.700, 1729.00),
    ('Badi Elaichi', 'Kgs', 0.000, 0.000, 0.000, 1995.00, 0.00, 0.000, 0.00),
    ('Methi Dana', 'Kgs', 0.000, 0.000, 0.000, 105.00, 0.00, 0.000, 0.00),
    ('Methi Dana(Expensive)', 'Kgs', 0.380, 0.000, 0.050, 120.00, 6.00, 0.330, 39.60),
    ('Rajma Masala', 'Kgs', 0.000, 0.000, 0.000, 85.00, 0.00, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.000, 0.000, 0.000, 168.00, 0.00, 0.000, 0.00),
    ('Tej Patta(Expensive)', 'Kgs', 0.380, 0.000, 0.020, 200.00, 4.00, 0.360, 72.00),
    ('Ajinomoto', 'Kgs', 2.000, 0.000, 0.000, 130.00, 0.00, 2.000, 260.00),
    ('Desi Ghee', 'Kgs', 24.500, 0.000, 1.000, 475.00, 475.00, 23.500, 11162.50),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.00, 0.000, 0.00),
    ('Eno', 'Kgs', 1.000, 0.000, 0.000, 55.04, 0.00, 1.000, 55.04),
    ('Ajwain', 'Kgs', 1.150, 0.000, 0.050, 400.00, 20.00, 1.100, 440.00),
    ('Mirchi (s)', 'Kgs', 0.650, 0.000, 0.000, 340.00, 0.00, 0.650, 221.00),
    ('Dhaniya Powder(Expensive)', 'Kgs', 2.100, 0.000, 0.200, 190.00, 38.00, 1.900, 361.00),
    ('Dhaniya Powder', 'Kgs', 8.000, 0.000, 0.000, 180.00, 0.00, 8.000, 1440.00),
    ('Kali Mirch (s)', 'Kgs', 0.500, 0.000, 0.000, 850.00, 0.00, 0.500, 425.00),
    ('Kali Mirch Powder', 'Kgs', 3.000, 0.000, 0.000, 120.00, 0.00, 3.000, 360.00),
    ('Moongphali Dana', 'Kgs', 17.000, 0.000, 0.000, 160.00, 0.00, 17.000, 2720.00),
    ('Sambhar Masala', 'Kgs', 0.000, 0.000, 0.000, 74.00, 0.00, 0.000, 0.00),
    ('LPG', 'Kgs', 68.600, 0.000, 26.900, 63.87, 1718.190, 41.700, 2663.51),
    ('Rai', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.00, 0.000, 0.00),
    ('Imli (Expensive)', 'Kgs', 0.650, 0.000, 0.100, 120.00, 12.00, 0.550, 66.00),
    ('Baking Powder', 'Kgs', 0.000, 0.000, 0.000, 67.20, 0.00, 0.000, 0.00),
    ('Baking Powder(Expensive)', 'Kgs', 4.000, 0.000, 0.000, 20.00, 0.00, 4.000, 80.00),
    ('Schezwan Sauce', 'Kgs', 2.000, 0.000, 0.000, 85.00, 0.00, 2.000, 170.00),
    ('Shahi Paneer Masala (kgs)', 'Kgs', 16.000, 0.000, 2.000, 88.00, 176.00, 14.000, 1232.00),
    ('Shahi Paneer Masala (pkt)', 'Kgs', 0.000, 0.000, 0.000, 90.00, 0.00, 0.000, 0.00),
    ('Sabzi Masala', 'Kgs', 11.900, 0.000, 0.000, 70.00, 0.00, 11.900, 833.00),
    ('Soya Bean Badiya', 'Kgs', 17.000, 0.000, 0.000, 94.50, 0.00, 17.000, 1606.50),
    ('Maida', 'Kgs', 2.800, 0.000, 0.000, 40.00, 0.00, 2.800, 112.00),
    ('Soya Sauce', 'Kgs', 2.000, 0.000, 0.000, 80.00, 0.00, 2.000, 160.00),
    ('Vinegar', 'Kgs', 2.000, 0.000, 0.000, 45.00, 0.00, 2.000, 90.00),
    ('Corn Flour', 'Kgs', 2.800, 0.000, 0.000, 80.00, 0.00, 2.800, 224.00),
    ('Achar', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.00, 7.000, 1029.00),
    ('Cream', 'Kgs', 4.000, 0.000, 1.000, 220.00, 220.00, 3.000, 660.00),
    ('Paratha Masala', 'Kgs', 0.000, 0.000, 0.000, 10.00, 0.00, 0.000, 0.00)
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('PP Box (Dal) Mini Meal', 'Nos', 8762, 0, 800, 3.186, 2548.80, 7962, 25366.93),
    ('Foil Box (Rice, Sabji)', 'Nos', 7816, 0, 400, 1.680, 672.00, 7416, 12458.88),
    ('Roti Pouch', 'Nos', 21100, 0, 2300, 0.236, 542.80, 18800, 4436.80),
    ('Salad Pkt', 'Nos', 9155, 0, 800, 0.177, 141.60, 8355, 1478.84),
    ('Spoon / Mini Meal', 'Nos', 4272, 0, 440, 0.504, 221.76, 3832, 1931.33),
    ('Napkin Tissue Paper', 'Nos', 3191, 0, 472, 0.354, 167.09, 2719, 962.53),
    ('Salt Pouch', 'Nos', 7407, 0, 400, 0.150, 60.00, 7007, 1051.05),
    ('Pickle & Paratha', 'Nos', 2722, 0, 472, 0.896, 422.83, 2250, 2015.62),
    ('Tape', 'Nos', 6, 0, 1, 23.60, 23.60, 5, 118.00),
    ('Big Foil Box (Biryani)', 'Nos', 143, 0, 40, 3.360, 134.40, 103, 346.08),
    ('Paper Box (Lunch)', 'Nos', 3827, 0, 400, 4.956, 1982.40, 3427, 16984.21),
    ('Butter Roti Paper', 'Nos', 1250, 0, 150, 0.236, 35.40, 1100, 259.60),
    ('Paratha Box', 'Nos', 1505, 0, 72, 3.360, 241.92, 1433, 4814.88),
    ('Partition Box', 'Nos', 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ('Black Packet', 'Nos', 1, 0, 0, 141.60, 0.00, 1, 141.60),
    ('400ml PP Box', 'Nos', 170, 0, 40, 4.720, 188.80, 130, 613.60),
    ('Silver Foil', 'Kgs', 5.200, 0, 0.500, 708.00, 354.00, 4.700, 3327.60)
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Barfi', 'Kgs', 21.0, 0, 12.0, 280.0, 3360.00, 9.0, 2520.00),
    ('Petha', 'Kgs', 10.0, 0, 0.0, 150.0, 0.00, 10.0, 1500.00),
    ('Bundi', 'Kgs', 0.0, 0, 0.0, 250.0, 0.00, 0.0, 0.00)
]

fresh_items = []

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 405, 400, 70.0, 28000.0, 20168.722),
    ("Paratha", 72, 70, 40.0, 2800.0, 1800.920),
    ("MINI", 40, 40, 50.0, 2000.0, 1169.964)
]

def seed_db():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()

    try:
        # Clear existing logs for this date to make the run idempotent
        cursor.execute("DELETE FROM sales WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM batch_prep WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM goods_received WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM expenditure WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM stock_ledger WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM samples WHERE date = ?", (DATE,))

        def process_item_list(items, category):
            for item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt in items:
                cursor.execute("SELECT id, received FROM inventory WHERE item = ? COLLATE NOCASE", (item,))
                row = cursor.fetchone()
                if row:
                    inv_id = row[0]
                    # Compute current stock up to the day before DATE (idempotent stock calculation)
                    cursor.execute("SELECT COALESCE(SUM(qty_change), 0.0) FROM stock_ledger WHERE inv_id = ? AND date < ?", (inv_id, DATE))
                    db_stock = cursor.fetchone()[0]

                    # Compute current received up to the day before DATE (idempotent received calculation)
                    cursor.execute("SELECT COALESCE(SUM(qty_change), 0.0) FROM stock_ledger WHERE inv_id = ? AND date < ? AND transaction_type = 'Received'", (inv_id, DATE))
                    db_received_before = cursor.fetchone()[0]
                    new_received = db_received_before + received
                    
                    # 1. Reconciliation of starting BBF mismatch (BBF - DB_Stock)
                    reconciliation_start = bbf - db_stock
                    if abs(reconciliation_start) > 0.001:
                        print(f"Reconciling {item} BBF mismatch: DB={db_stock:.3f}, Register BBF={bbf:.3f}, Diff={reconciliation_start:.3f}")
                        cursor.execute('''
                            INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                            VALUES (?, ?, 'Reconciliation', ?, 'Manual register BBF discrepancy reconciliation')
                        ''', (DATE, inv_id, reconciliation_start))

                    # 2. Reconciliation of register math/rounding error at end of day: BCF - (BBF + Received - Issue)
                    reconciliation_end = bcf - (bbf + received - issue)
                    if abs(reconciliation_end) > 0.001:
                        print(f"Reconciling {item} BCF math mismatch: Register BBF={bbf:.3f}, BCF={bcf:.3f}, Expected BCF={bbf+received-issue:.3f}, Diff={reconciliation_end:.3f}")
                        cursor.execute('''
                            INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                            VALUES (?, ?, 'Reconciliation', ?, 'Manual register BCF math reconciliation')
                        ''', (DATE, inv_id, reconciliation_end))

                    cursor.execute('''
                        UPDATE inventory
                        SET stock = ?, cp = ?, received = ?, updated = ?
                        WHERE id = ?
                    ''', (bcf, rate, new_received, DATE, inv_id))
                else:
                    cursor.execute('''
                        INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated)
                        VALUES (?, ?, ?, ?, 0.0, ?, ?, ?, ?)
                    ''', (item, category, unit, bcf, bbf, received, rate, DATE))
                    inv_id = cursor.lastrowid
                    cursor.execute('''
                        INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                        VALUES (?, ?, 'Opening', ?, 'Opening balance BBF')
                    ''', (DATE, inv_id, bbf))

                if received > 0:
                    cursor.execute('''
                        INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                        VALUES (?, ?, 'Received', ?, 'Stock Received')
                    ''', (DATE, inv_id, received))
                    cursor.execute('''
                        INSERT INTO goods_received (date, inv_id, qty, total_cost)
                        VALUES (?, ?, ?, ?)
                    ''', (DATE, inv_id, received, received * rate))

                if issue > 0:
                    cursor.execute('''
                        INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                        VALUES (?, ?, 'Batch_Prep', ?, 'Material used for production')
                    ''', (DATE, inv_id, -issue))

        print("Processing Dry items...")
        process_item_list(dry_items, 'Dry')

        print("Processing Packaging items...")
        process_item_list(packaging_items, 'Packing Material')

        print("Processing Sweets items...")
        process_item_list(sweets_items, 'Milk Based Product')

        print("Processing Sales logs & Menu updates...")
        samples_list = [
            ("LUNCH",     1, "01 X LUNCH SAMPLE",       "General"),
            ("Paratha",   1, "01 X PARATHA SAMPLE",     "General")
        ]
        # Get the day of the week for DATE
        day_name = _dt.strptime(DATE, "%Y-%m-%d").strftime("%A")
        
        meal_type_map = {
            "LUNCH": "Lunch",
            "PARATHA": "Paratha",
            "MINI": "Mini Meal",
            "MINI MEAL": "Mini Meal"
        }

        for meal, prepared, sold, rate, income, expdr in sales_summary:
            meal_upper = meal.upper()
            menu_id = None
            specific_name = meal
            if meal_upper in meal_type_map:
                mtype = meal_type_map[meal_upper]
                # Query daily_menu for the specific menu_id
                cursor.execute(
                    "SELECT dm.menu_id, m.name FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id WHERE dm.day = ? AND dm.meal_type = ?",
                    (day_name, mtype)
                )
                spec_row = cursor.fetchone()
                if spec_row:
                    menu_id = spec_row[0]
                    specific_name = spec_row[1]
            
            if menu_id is None:
                cursor.execute("SELECT id FROM menu WHERE name = ? COLLATE NOCASE", (meal,))
                menu_row = cursor.fetchone()
                if menu_row:
                    menu_id = menu_row[0]
                else:
                    cursor.execute('''
                        INSERT INTO menu (name, sp, active, cogs)
                        VALUES (?, ?, 1, ?)
                    ''', (meal, rate, 0.0))
                    menu_id = cursor.lastrowid

            cpu = (expdr / prepared) if prepared > 0 else 0.0
            cursor.execute("UPDATE menu SET sp = ?, cogs = ?, active = 1 WHERE id = ?", (rate, cpu, menu_id))

            # Insert all sample rows for this meal
            mtype = meal_type_map.get(meal_upper)
            formatted_meal_name = f"{mtype} ({specific_name})" if mtype else specific_name

            total_sample_qty = 0
            for sml_meal, qty, notes, given_to in samples_list:
                if sml_meal == meal:
                    total_sample_qty += qty
                    cost = qty * cpu
                    cursor.execute('''
                        INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (DATE, menu_id, formatted_meal_name, rate, qty, cost, given_to, notes))

            wastage = max(0, prepared - sold - total_sample_qty)
            if prepared > 0 or sold > 0:
                # Add Cash/UPI split
                if meal == "LUNCH":
                    cash_amt, upi_amt = 20400.0, 7600.0
                    payment_str = 'Cash: 20400, UPI: 7600, Card: 0'
                elif meal == "Paratha":
                    cash_amt, upi_amt = 2040.0, 760.0
                    payment_str = 'Cash: 2040, UPI: 760, Card: 0'
                else: # MINI
                    cash_amt, upi_amt = 1460.0, 540.0
                    payment_str = 'Cash: 1460, UPI: 540, Card: 0'

                cursor.execute('''
                    INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment, cash_amt, upi_amt, card_amt)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0.0)
                ''', (DATE, menu_id, formatted_meal_name, rate, sold, wastage, expdr, payment_str, cash_amt, upi_amt))

                cursor.execute('''
                    INSERT INTO batch_prep (date, menu_id, qty_prepared)
                    VALUES (?, ?, ?)
                ''', (DATE, menu_id, prepared))

                cursor.execute('''
                    INSERT INTO expenditure (date, amount, category, notes)
                    VALUES (?, ?, 'Raw Materials', ?)
                ''', (DATE, expdr, f"Auto-expenditure for {meal} batch"))

        conn.commit()
        print("🎉 Database successfully updated for 08 Jul 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
