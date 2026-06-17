import sqlite3

DATE = "2026-05-16"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 613.000, 0.000, 20.000, 31.00, 620.000, 593.000, 18383.00),
    ('Rice', 'Kgs', 401.000, 0.000, 12.000, 65.00, 780.000, 389.000, 25285.00),
    ('R/oil', 'Ltr', 146.500, 0.000, 5.000, 180.92, 904.615, 141.500, 25600.62),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('Rajma', 'Kgs', 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 18.000, 0.000, 0.000, 78.00, 0.000, 18.000, 1404.00),
    ('Besan', 'Kgs', 37.000, 0.000, 0.000, 94.50, 0.000, 37.000, 3496.50),
    ('Dal Arhar', 'Kgs', 36.000, 0.000, 0.000, 120.00, 0.000, 36.000, 4320.00),
    ('Dal masoor (s)', 'Pkt', 14.000, 0.000, 4.000, 85.00, 340.000, 10.000, 850.00),
    ('Urad Dal Chilka', 'KGS', 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ('Masoor Dal (Malika)', 'Kgs', 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 0.100, 0.000, 0.000, 315.00, 0.000, 0.100, 31.50),
    ('Haldi Powder', 'Kgs', 1.600, 0.000, 0.100, 231.00, 23.100, 1.500, 346.50),
    ('Mirchi Powder', 'Kgs', 1.800, 0.000, 0.100, 315.00, 31.500, 1.700, 535.50),
    ('Dal chini', 'Kgs', 0.290, 0.000, 0.010, 357.00, 3.570, 0.280, 99.96),
    ('Laung', 'Kgs', 0.160, 0.000, 0.010, 1155.00, 11.550, 0.150, 173.25),
    ('Hing', 'Nos', 14.000, 0.000, 0.000, 89.25, 0.000, 14.000, 1249.50),
    ('Kitchen King', 'Kgs', 0.400, 0.000, 0.100, 800.00, 80.000, 0.300, 240.00),
    ('Degi Mirch', 'Kgs', 0.700, 0.000, 0.100, 960.00, 96.000, 0.600, 576.00),
    ('Kasuri Methi', 'Kgs', 0.350, 0.000, 0.000, 336.00, 0.000, 0.350, 117.60),
    ('Garam Masala', 'Kgs', 0.400, 0.000, 0.100, 920.00, 92.000, 0.300, 276.00),
    ('Salt', 'Kgs', 22.000, 0.000, 2.000, 28.00, 56.000, 20.000, 560.00),
    ('Dhaniya (s)', 'Kgs', 0.710, 0.000, 0.000, 157.50, 0.000, 0.710, 111.83),
    ('Jeera Powder', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('Badi Elaichi', 'Kgs', 0.140, 0.000, 0.010, 1995.00, 19.950, 0.130, 259.35),
    ('Methi Dana', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.370, 0.000, 0.000, 168.00, 0.000, 0.370, 62.16),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Desi Ghee', 'Kgs', 12.000, 0.000, 0.500, 504.00, 252.000, 11.500, 5796.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.370, 0.000, 0.010, 252.00, 2.520, 0.360, 90.72),
    ('Mirchi (s)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 0.700, 0.000, 0.000, 752.00, 0.000, 0.700, 526.40),
    ('Rajma Masala (Kgs)', 'Kgs', 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
    ('Gulab Jal', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('Chana Masala', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Kala Chana', 'Kgs', 41.000, 0.000, 0.000, 78.00, 0.000, 41.000, 3198.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 5.000, 0.000, 0.000, 60.00, 0.000, 5.000, 300.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ('Kewra Water', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('Biryani Masala', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Dhaniya Powder', 'Kgs', 2.500, 0.000, 0.100, 168.00, 16.800, 2.400, 403.20),
    ('Kali Mirch (s)', 'Kgs', 0.280, 0.000, 0.010, 882.00, 8.820, 0.270, 238.14),
    ('Moongphali Dana', 'Kgs', 9.000, 0.000, 0.000, 157.50, 0.000, 9.000, 1417.50),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 28.400, 56.800, 10.500, 61.83, 649.225, 74.700, 4618.77),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Baking Powder', 'PKT', 1.000, 0.000, 0.000, 67.20, 0.000, 1.000, 67.20),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 0.900, 0.000, 0.000, 880.00, 0.000, 0.900, 792.00),
    ('Soya Bean Badiya', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.410, 0.000, 0.010, 2730.00, 27.300, 0.400, 1092.00),
    ('Amchur Powder', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Aachar', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('Cream', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('Paratha Masala', 'Kgs', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 1245, 0, 160, 3.186, 509.76, 1085, 3456.81),
    ("Foil Box (Rice, Sabji)", "Nos", 3237, 0, 284, 1.575, 447.30, 2953, 4650.98),
    ("Roti pouch", "Nos", 13500, 0, 700, 0.236, 165.20, 12800, 3020.80),
    ("Salad Pkt", "Nos", 3624, 0, 284, 0.177, 50.27, 3340, 591.18),
    ("Spoon/Mini Meal", "Nos", 817, 0, 142, 0.504, 71.57, 675, 340.20),
    ("Napkin Tissue Paper", "Nos", 6707, 0, 0, 0.354, 0.00, 6707, 2374.28),
    ("Salt Pouch", "Nos", 855, 0, 142, 0.150, 21.30, 713, 106.95),
    ("Pickle & Paratha", "Nos", 2708, 0, 142, 0.896, 127.21, 2566, 2298.71),
    ("Tape", "Nos", 3, 0, 1, 23.600, 23.60, 2, 47.20),
    ("Big Foil Box (Biryani)", "Nos", 65, 0, 18, 3.150, 56.70, 47, 148.05),
    ("Paper Box (Lunch)", "Nos", 2204, 0, 142, 4.956, 703.75, 2062, 10219.27),
    ("Butter Roti Paper", "NOS", 1400, 0, 0, 0.236, 0.00, 1400, 330.40),
    ("Paratha Box", "Nos", 767, 0, 0, 3.360, 0.00, 767, 2577.12),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 0, 0, 0, 141.600, 0.00, 0, 0.00),
    ("400 ML PP Box", "Nos", 166, 0, 0, 4.720, 0.00, 166, 783.52),
    ("Silver foil", "Kgs", 2.4, 0, 0.000, 708.000, 0.00, 2.400, 1699.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 2.000, 0, 2.000, 280.00, 560.00, 0.000, 0.00),
    ("Petha", "KGS", 0.000, 0, 0.000, 150.00, 0.00, 0.000, 0.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 16.000, 4.000, 20.000, 10.000, 200.000, 0.000, 0.00),
    ("Onion", "Kgs", 54.000, 0.000, 5.500, 22.000, 121.000, 48.500, 1067.00),
    ("Tomato", "Kgs", 2.000, 0.000, 2.000, 16.000, 32.000, 0.000, 0.00),
    ("Ginger", "Kgs", 1.000, 0.000, 1.000, 135.000, 135.000, 0.000, 0.00),
    ("Garlic", "Kgs", 0.280, 0.000, 0.280, 143.000, 40.040, 0.000, 0.00),
    ("Pumpkin", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 0.420, 0.000, 0.420, 60.000, 25.200, 0.000, 0.00),
    ("Coriander", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 0.000, 1.015, 1.015, 22.000, 22.330, 0.000, 0.00),
    ("Beans", "Kgs", 0.000, 0.000, 0.000, 121.000, 0.000, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 1.050, 1.050, 35.000, 36.750, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0.955, 0.955, 55.000, 52.525, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 5.000, 4.860, 5.000, 29.000, 145.000, 4.860, 140.94),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 6.000, 6.000, 35.000, 210.000, 0.000, 0.00),
    ("Tori", "Nos", 10.000, 0.000, 10.000, 25.000, 250.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 142, 140, 70.0, 9800, 7675.0),
    ("Paratha", 70, 0, 40.0, 0, 0.0),
    ("Dahi", 240, 0, 10.0, 0, 0.0),
    ("Chach", 200, 0, 10.0, 0, 0.0),
    ("MINI", 18, 17, 50.0, 850, 436.0),
    ("Amul Kool", 0, 0, 25.0, 0, 0.0),
    ("Lahori Zeera", 9, 9, 10.0, 90, 81.0),
    ("Lassi", 9, 9, 20.0, 180, 171.0),
    ("Brownie", 0, 0, 40.0, 0, 0.0),
    ("Plum Cake", 0, 0, 20.0, 0, 0.0),
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
            ("LUNCH",    2, "02 X LUNCH SAMPLE",      "General"),
            ("MINI",     1, "01 X MINI LUNCH SAMPLE", "General"),
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
        print("🎉 Database successfully updated for 16 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
