import sqlite3

DATE = "2026-05-20"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 461.000, 0.000, 66.000, 31.00, 2046.000, 395.000, 12245.00),
    ('Rice', 'Kgs', 296.000, 0.000, 46.000, 65.00, 2990.000, 250.000, 16250.00),
    ('R/oil', 'Ltr', 118.500, 0.000, 11.000, 180.92, 1990.154, 107.500, 19449.23),
    ('Sarso Dana', 'Kgs', 0.200, 0.000, 0.000, 105.00, 0.000, 0.200, 21.00),
    ('Rajma', 'Kgs', 48.000, 0.000, 17.000, 115.00, 1955.000, 31.000, 3565.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 10.000, 0.000, 0.000, 78.00, 0.000, 10.000, 780.00),
    ('Besan', 'Kgs', 24.000, 0.000, 0.000, 94.50, 0.000, 24.000, 2268.00),
    ('Dal Arhar', 'Kgs', 33.000, 0.000, 0.000, 120.00, 0.000, 33.000, 3960.00),
    ('Dal masoor (s)', 'Pkt', 7.000, 0.000, 0.000, 85.00, 0.000, 7.000, 595.00),
    ('Urad Dal Chilka', 'KGS', 3.000, 0.000, 0.000, 110.00, 0.000, 3.000, 330.00),
    ('Masoor Dal (Malika)', 'Kgs', 3.000, 0.000, 0.000, 85.00, 0.000, 3.000, 255.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Haldi Powder', 'Kgs', 0.700, 0.000, 0.400, 231.00, 92.400, 0.300, 69.30),
    ('Mirchi Powder', 'Kgs', 1.100, 0.000, 0.300, 315.00, 94.500, 0.800, 252.00),
    ('Dal chini', 'Kgs', 0.240, 0.000, 0.040, 357.00, 14.280, 0.200, 71.40),
    ('Laung', 'Kgs', 0.110, 0.000, 0.040, 1155.00, 46.200, 0.070, 80.85),
    ('Hing', 'Nos', 9.000, 0.000, 0.000, 89.25, 0.000, 9.000, 803.25),
    ('Kitchen King', 'Kgs', 0.100, 0.000, 0.000, 800.00, 0.000, 0.100, 80.00),
    ('Degi Mirch', 'Kgs', 0.100, 0.000, 0.000, 960.00, 0.000, 0.100, 96.00),
    ('Kasuri Methi', 'Kgs', 0.200, 0.000, 0.050, 336.00, 16.800, 0.150, 50.40),
    ('Garam Masala', 'Kgs', 0.000, 0.000, 0.000, 920.00, 0.000, 0.000, 0.00),
    ('Salt', 'Kgs', 11.000, 0.000, 4.000, 28.00, 112.000, 7.000, 196.00),
    ('Dhaniya (s)', 'Kgs', 0.510, 0.000, 0.100, 157.50, 15.750, 0.410, 64.57),
    ('Jeera Powder', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('Badi Elaichi', 'Kgs', 0.090, 0.000, 0.030, 1995.00, 59.850, 0.060, 119.70),
    ('Methi Dana', 'Kgs', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.320, 0.000, 0.030, 168.00, 5.040, 0.290, 48.72),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Desi Ghee', 'Kgs', 8.000, 0.000, 1.000, 504.00, 504.000, 7.000, 3528.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.200, 0.000, 0.100, 252.00, 25.200, 0.100, 25.20),
    ('Mirchi (s)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 0.500, 0.000, 0.100, 752.00, 75.200, 0.400, 300.80),
    ('Rajma Masala (Kgs)', 'Kgs', 1.600, 0.000, 0.500, 736.00, 368.000, 1.100, 809.60),
    ('Gulab Jal', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('Chana Masala', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Kala Chana', 'Kgs', 41.000, 0.000, 0.000, 78.00, 0.000, 41.000, 3198.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 5.000, 0.000, 0.000, 60.00, 0.000, 5.000, 300.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ('Kewra Water', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('Biryani Masala', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Dhaniya Powder', 'Kgs', 1.800, 0.000, 0.400, 168.00, 67.200, 1.400, 235.20),
    ('Kali Mirch (s)', 'Kgs', 0.220, 0.000, 0.036, 882.00, 31.752, 0.184, 162.29),
    ('Moongphali Dana', 'Kgs', 9.000, 0.000, 4.000, 157.50, 630.000, 5.000, 787.50),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 88.600, 0.000, 26.400, 61.83, 1632.338, 62.200, 3845.89),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Baking Powder', 'PKT', 0.000, 0.000, 0.000, 67.20, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 0.900, 0.000, 0.400, 880.00, 352.000, 0.500, 440.00),
    ('Soya Bean Badiya', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.350, 0.000, 0.040, 2730.00, 109.200, 0.310, 846.30),
    ('Amchur Powder', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Aachar', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('Cream', 'Kgs', 3.500, 0.000, 1.000, 220.00, 220.000, 2.500, 550.00),
    ('Paratha Masala', 'Kgs', 2.000, 0.000, 1.000, 10.00, 10.000, 1.000, 10.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2999, 0, 443, 3.186, 1411.40, 2556, 8143.42),
    ("Foil Box (Rice, Sabji)", "Nos", 4781, 0, 886, 1.575, 1395.45, 3895, 6134.63),
    ("Roti pouch", "Nos", 7300, 0, 2700, 0.236, 637.20, 4600, 1085.60),
    ("Salad Pkt", "Nos", 7168, 0, 886, 0.177, 156.82, 6282, 1111.91),
    ("Spoon/Mini Meal", "Nos", 2465, 0, 502, 0.504, 253.01, 1963, 989.35),
    ("Napkin Tissue Paper", "Nos", 9678, 0, 502, 0.354, 177.71, 9176, 3248.30),
    ("Salt Pouch", "Nos", 2627, 0, 443, 0.150, 66.45, 2184, 327.60),
    ("Pickle & Paratha", "Nos", 7385, 0, 502, 0.896, 449.71, 6883, 6166.02),
    ("Tape", "Nos", 7, 0, 2, 23.600, 47.20, 5, 118.00),
    ("Big Foil Box (Biryani)", "Nos", 223, 0, 59, 3.150, 185.85, 164, 516.60),
    ("Paper Box (Lunch)", "Nos", 976, 0, 443, 4.956, 2195.51, 533, 2641.55),
    ("Butter Roti Paper", "NOS", 1200, 0, 100, 0.236, 23.60, 1100, 259.60),
    ("Paratha Box", "Nos", 624, 0, 59, 3.360, 198.24, 565, 1898.40),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 2, 0, 1, 141.600, 141.60, 1, 141.60),
    ("400 ML PP Box", "Nos", 204, 0, 59, 4.720, 278.48, 145, 684.40),
    ("Silver foil", "Kgs", 4.900, 0, 0.500, 708.000, 354.00, 4.400, 3115.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 24.000, 0, 12.000, 280.00, 3360.00, 12.000, 3360.00),
    ("Petha", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 124.000, 0, 65.000, 10.000, 650.000, 59.000, 590.00),
    ("Onion", "Kgs", 69.500, 50.000, 22.000, 22.000, 484.000, 97.500, 2145.00),
    ("Tomato", "Kgs", 18.000, 0, 12.000, 25.000, 300.000, 6.000, 150.00),
    ("Ginger", "Kgs", 2.000, 0, 1.000, 85.000, 85.000, 1.000, 85.00),
    ("Garlic", "Kgs", 0.980, 2.600, 2.000, 154.000, 308.000, 1.580, 243.32),
    ("Pumpkin", "Kgs", 0.000, 4.500, 0.000, 17.000, 0.000, 4.500, 76.50),
    ("Green chilli", "Kgs", 0.000, 6.060, 2.000, 61.000, 122.000, 4.060, 247.66),
    ("Coriander", "Kgs", 0.000, 0, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 8.000, 0, 0.000, 18.000, 0.000, 8.000, 144.00),
    ("Beans", "Kgs", 0.000, 1.945, 1.945, 121.000, 235.345, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 2.810, 2.810, 35.000, 98.350, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 3.090, 3.090, 55.000, 169.950, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 14.860, 15.200, 26.200, 23.000, 602.600, 3.860, 88.78),
    ("Matar", "Kgs", 0.000, 0, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 0, 0.000, 25.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 443, 440, 70.0, 30800, 24780.0),
    ("Paratha", 59, 57, 40.0, 2280, 2023.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 59, 58, 50.0, 2900, 1144.0),
    ("Amul Kool", 1, 1, 25.0, 25, 22.0),
    ("Lahori Zeera", 10, 0, 10.0, 0, 0.0),
    ("Lassi", 10, 0, 20.0, 0, 0.0),
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
            ("Paratha",  2, "02 X PARATHA SAMPLE",    "General"),
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
        print("🎉 Database successfully updated for 20 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
