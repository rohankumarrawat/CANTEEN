import sqlite3

DATE = "2026-05-26"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 1478.000, 0.000, 66.000, 31.00, 2046.000, 1412.000, 43772.00),
    ('Rice', 'Kgs', 1004.000, 0.000, 46.000, 68.00, 3128.000, 958.000, 65144.00),
    ('R/oil', 'Ltr', 342.000, 0.000, 12.000, 180.92, 2171.077, 330.000, 59704.62),
    ('Sarso Dana', 'Kgs', 0.600, 0.000, 0.250, 105.00, 26.250, 0.350, 36.75),
    ('Rajma', 'Kgs', 111.000, 0.000, 0.000, 115.00, 0.000, 111.000, 12765.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 90.000, 0.000, 0.000, 80.00, 0.000, 90.000, 7200.00),
    ('Besan', 'Kgs', 80.000, 0.000, 10.000, 94.50, 945.000, 70.000, 6615.00),
    ('Dal Arhar', 'Kgs', 80.000, 0.000, 1.000, 120.00, 120.000, 79.000, 9480.00),
    ('Dal masoor (s)', 'Pkt', 23.000, 0.000, 0.000, 85.00, 0.000, 23.000, 1955.00),
    ('Urad Dal Chilka', 'KGS', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('Masoor Dal (Malika)', 'Kgs', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('Moong Dal Chilka', 'Kgs', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 2.940, 0.000, 0.500, 315.00, 157.500, 2.440, 768.60),
    ('Haldi Powder', 'Kgs', 9.100, 0.000, 0.500, 231.00, 115.500, 8.600, 1986.60),
    ('Mirchi Powder', 'Kgs', 7.600, 0.000, 0.500, 315.00, 157.500, 7.100, 2236.50),
    ('Dal chini', 'Kgs', 0.090, 0.000, 0.020, 357.00, 7.140, 0.070, 24.99),
    ('Laung', 'Kgs', 0.270, 0.000, 0.030, 1155.00, 34.650, 0.240, 277.20),
    ('Hing', 'Nos', 29.000, 0.000, 4.000, 89.25, 357.000, 25.000, 2231.25),
    ('Kitchen King', 'Kgs', 5.100, 0.000, 0.500, 800.00, 400.003, 4.600, 3680.03),
    ('Degi Mirch', 'Kgs', 5.000, 0.000, 0.500, 959.99, 479.997, 4.500, 4319.97),
    ('Kasuri Methi', 'Kgs', 1.000, 0.000, 0.050, 336.00, 16.800, 0.950, 319.20),
    ('Garam Masala', 'Kgs', 3.000, 0.000, 0.500, 920.00, 459.998, 2.500, 2299.99),
    ('Salt', 'Kgs', 47.000, 0.000, 4.000, 28.00, 112.000, 43.000, 1204.00),
    ('Dhaniya (s)', 'Kgs', 2.460, 0.000, 0.500, 199.50, 99.752, 1.960, 391.03),
    ('Jeera Powder', 'Kgs', 3.000, 0.000, 0.300, 420.00, 126.000, 2.700, 1134.00),
    ('Chana Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('Badi Elaichi', 'Kgs', 0.280, 0.000, 0.040, 1995.00, 79.800, 0.240, 478.80),
    ('Methi Dana', 'Kgs', 0.500, 0.000, 0.150, 105.00, 15.750, 0.350, 36.75),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.690, 0.000, 0.030, 168.00, 5.040, 0.660, 110.88),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Desi Ghee', 'Kgs', 32.500, 0.000, 1.000, 504.00, 504.000, 31.500, 15876.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.950, 0.000, 0.050, 252.00, 12.600, 0.900, 226.80),
    ('Mirchi (s)', 'Kgs', 1.000, 0.000, 0.100, 367.50, 36.750, 0.900, 330.75),
    ('Chat Masala', 'Kgs', 2.400, 0.000, 0.300, 752.00, 225.600, 2.100, 1579.20),
    ('Rajma Masala (Kgs)', 'Kgs', 2.700, 0.000, 0.400, 736.25, 294.500, 2.300, 1693.38),
    ('Gulab Jal', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('Chana Masala', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('Kala Chana', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 16.000, 0.000, 0.000, 60.00, 0.000, 16.000, 960.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('Kewra Water', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('Biryani Masala', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Dhaniya Powder', 'Kgs', 7.300, 0.000, 0.500, 199.50, 99.750, 6.800, 1356.60),
    ('Kali Mirch (s)', 'Kgs', 0.484, 0.000, 0.030, 882.00, 26.460, 0.454, 400.43),
    ('Moongphali Dana', 'Kgs', 20.000, 0.000, 0.000, 168.00, 0.000, 20.000, 3360.00),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 96.900, 0.000, 30.200, 61.83, 1867.266, 66.700, 4124.13),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Baking Powder', 'PKT', 4.000, 0.000, 1.000, 67.20, 67.200, 3.000, 201.60),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 1.700, 0.000, 0.000, 880.00, 0.000, 1.700, 1496.00),
    ('Soya Bean Badiya', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('Javitri', 'Kgs', 0.200, 0.000, 0.050, 2730.00, 136.500, 0.150, 409.50),
    ('Amchur Powder', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Rice (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('Imli', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('Imli (expensive)', 'Pkt', 3.750, 0.000, 0.000, 120.00, 0.000, 3.750, 450.00),
    ('Sabudana', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 3702, 0, 543, 3.186, 1730.00, 3159, 10064.57),
    ("Foil Box (Rice, Sabji)", "Nos", 4906, 0, 1086, 1.575, 1710.45, 3820, 6016.50),
    ("Roti pouch", "Nos", 11200, 0, 2900, 0.236, 684.40, 8300, 1958.80),
    ("Salad Pkt", "Nos", 7760, 0, 1086, 0.177, 192.22, 6674, 1181.30),
    ("Spoon/Mini Meal", "Nos", 4023, 0, 592, 0.504, 298.37, 3431, 1729.22),
    ("Napkin Tissue Paper", "Nos", 8999, 0, 614, 0.354, 217.36, 8385, 2968.29),
    ("Salt Pouch", "Nos", 3923, 0, 543, 0.150, 81.45, 3380, 507.00),
    ("Pickle & Paratha", "Nos", 4906, 0, 614, 0.896, 550.04, 4292, 3844.92),
    ("Tape", "Nos", 8, 0, 2, 23.600, 47.20, 6, 141.60),
    ("Big Foil Box (Biryani)", "Nos", 267, 0, 49, 3.150, 154.35, 218, 686.70),
    ("Paper Box (Lunch)", "Nos", 2972, 3100, 543, 4.956, 2691.11, 5529, 27401.72),
    ("Butter Roti Paper", "Nos", 650, 0, 50, 0.236, 11.80, 600, 141.60),
    ("Paratha Box", "Nos", 349, 0, 71, 3.360, 238.56, 278, 934.08),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 5, 0, 1, 141.600, 141.60, 4, 566.40),
    ("400 ML PP Box", "Nos", 169, 0, 49, 4.720, 231.28, 120, 566.40),
    ("Silver foil", "Kgs", 2.150, 0, 0.750, 708.000, 531.00, 1.400, 991.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 24.000, 0, 0.000, 280.00, 0.00, 24.000, 6720.00),
    ("Petha", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("Guldana", "KGS", 16.000, 0, 16.000, 250.00, 4000.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 133.000, 0, 85.000, 13.000, 1105.00, 48.000, 624.00),
    ("Onion", "Kgs", 98.000, 0, 27.000, 24.000, 648.00, 71.000, 1704.00),
    ("Tomato", "Kgs", 52.000, 0, 14.000, 25.000, 350.00, 38.000, 950.00),
    ("Ginger", "Kgs", 5.000, 0, 2.000, 70.000, 140.00, 3.000, 210.00),
    ("Garlic", "Kgs", 4.040, 0, 1.000, 154.000, 154.00, 3.040, 468.16),
    ("Pumpkin", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("Green chilli", "Kgs", 5.000, 0, 4.000, 65.000, 260.00, 1.000, 65.00),
    ("Coriander", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("Capsicum", "Kgs", 30.000, 0, 30.000, 30.000, 900.00, 0.000, 0.00),
    ("Beans", "Kgs", 0.000, 0, 0.000, 105.000, 0.00, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0, 0.000, 61.000, 0.00, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0, 0.000, 20.000, 0.00, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("Cucumber", "Kgs", 43.800, 0, 23.000, 22.000, 506.00, 20.800, 457.60),
    ("Matar", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0, 0.000, 250.000, 0.00, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 15.000, 15.000, 75.000, 1125.00, 0.000, 0.00),
    ("Kulcha", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("Pav", "Nos", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800.0, 29900.0),
    ("Paratha", 71, 70, 40.0, 2800.0, 2040.0),
    ("Dahi", 240, 239, 10.0, 2390.0, 2151.0),
    ("Chach", 200, 186, 10.0, 1860.0, 1674.0),
    ("MINI", 49, 48, 50.0, 2400.0, 1090.0),
    ("Amul Kool", 18, 18, 25.0, 450.0, 396.0),
    ("Lahori Zeera", 2, 0, 10.0, 0.0, 0.0),
    ("Lassi", 4, 0, 20.0, 0.0, 0.0),
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
        process_item_list(packaging_items, 'Misc')

        print("Processing Sweets items...")
        process_item_list(sweets_items, 'Misc')

        print("Processing Fresh vegetables...")
        process_item_list(fresh_items, 'Fresh')

        print("Processing Sales logs & Menu updates...")
        samples_list = [
            ("LUNCH",    3, "03 X LUNCH SAMPLE",      "General"),
            ("Paratha",  1, "01 X PARATHA SAMPLE",    "General"),
            ("MINI",     1, "01 X MINI LUNCH SAMPLE", "General"),
            ("Dahi",     1, "01 X DAHI SAMPLE",       "General"),
            ("Chach",    1, "01 X CHACH SAMPLE",      "General"),
            ("Chach", 7, "07 X CHACH FOR LADIES", "Staff"),
        ]
        # Get the day of the week for DATE
        from datetime import datetime as _dt
        day_name = _dt.strptime(DATE, "%Y-%m-%d").strftime("%A")
        
        # Map of generic meal name to daily_menu meal_type
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
                # Fall back to looking up by name
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
            # Update menu item's sp and cogs
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
            # Only insert if prepared > 0 or sold > 0 (some templates check this, some don't, but checking is safer)
            if prepared > 0 or sold > 0:
                cursor.execute('''
                    INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'Cash')
                ''', (DATE, menu_id, formatted_meal_name, rate, sold, wastage, expdr))

                cursor.execute('''
                    INSERT INTO batch_prep (date, menu_id, qty_prepared)
                    VALUES (?, ?, ?)
                ''', (DATE, menu_id, prepared))

                cursor.execute('''
                    INSERT INTO expenditure (date, amount, category, notes)
                    VALUES (?, ?, 'Raw Materials', ?)
                ''', (DATE, expdr, f"Auto-expenditure for {meal} batch"))

        conn.commit()
        print("🎉 Database successfully updated for 26 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
