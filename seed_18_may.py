import sqlite3

DATE = "2026-05-18"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 593.000, 0.000, 66.000, 31.00, 2046.000, 527.000, 16337.00),
    ('Rice', 'Kgs', 389.000, 0.000, 46.000, 65.00, 2990.000, 343.000, 22295.00),
    ('R/oil', 'Ltr', 141.500, 0.000, 9.000, 180.92, 1628.308, 132.500, 23972.31),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('Rajma', 'Kgs', 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 18.000, 0.000, 8.000, 78.00, 624.000, 10.000, 780.00),
    ('Besan', 'Kgs', 37.000, 0.000, 0.000, 94.50, 0.000, 37.000, 3496.50),
    ('Dal Arhar', 'Kgs', 36.000, 0.000, 3.000, 120.00, 360.000, 33.000, 3960.00),
    ('Dal masoor (s)', 'Pkt', 10.000, 0.000, 3.000, 85.00, 255.000, 7.000, 595.00),
    ('Urad Dal Chilka', 'KGS', 6.000, 0.000, 3.000, 110.00, 330.000, 3.000, 330.00),
    ('Masoor Dal (Malika)', 'Kgs', 6.000, 0.000, 3.000, 85.00, 255.000, 3.000, 255.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 0.100, 0.000, 0.050, 315.00, 15.750, 0.050, 15.75),
    ('Haldi Powder', 'Kgs', 1.500, 0.000, 0.400, 231.00, 92.400, 1.100, 254.10),
    ('Mirchi Powder', 'Kgs', 1.700, 0.000, 0.300, 315.00, 94.500, 1.400, 441.00),
    ('Dal chini', 'Kgs', 0.280, 0.000, 0.010, 357.00, 3.570, 0.270, 96.39),
    ('Laung', 'Kgs', 0.140, 0.000, 0.010, 1155.00, 11.550, 0.130, 161.70),
    ('Hing', 'Nos', 14.000, 0.000, 0.000, 89.25, 0.000, 14.000, 1249.50),
    ('Kitchen King', 'Kgs', 0.300, 0.000, 0.200, 800.00, 160.000, 0.100, 80.00),
    ('Degi Mirch', 'Kgs', 0.600, 0.000, 0.200, 960.00, 192.000, 0.400, 384.00),
    ('Kasuri Methi', 'Kgs', 0.350, 0.000, 0.070, 336.00, 23.520, 0.280, 94.08),
    ('Garam Masala', 'Kgs', 0.300, 0.000, 0.200, 920.00, 184.000, 0.100, 92.00),
    ('Salt', 'Kgs', 20.000, 0.000, 4.000, 28.00, 112.000, 16.000, 448.00),
    ('Dhaniya (s)', 'Kgs', 0.710, 0.000, 0.050, 157.50, 7.875, 0.660, 103.95),
    ('Jeera Powder', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('Badi Elaichi', 'Kgs', 0.130, 0.000, 0.010, 1995.00, 19.950, 0.120, 239.40),
    ('Methi Dana', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.370, 0.000, 0.020, 168.00, 3.360, 0.350, 58.80),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Desi Ghee', 'Kgs', 11.500, 0.000, 2.000, 504.00, 1008.000, 9.500, 4788.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.360, 0.000, 0.080, 252.00, 20.160, 0.280, 70.56),
    ('Mirchi (s)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 0.700, 0.000, 0.100, 752.00, 75.200, 0.600, 451.20),
    ('Rajma Masala (Kgs)', 'Kgs', 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
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
    ('Dhaniya Powder', 'Kgs', 2.400, 0.000, 0.300, 168.00, 50.400, 2.100, 352.80),
    ('Kali Mirch (s)', 'Kgs', 0.270, 0.000, 0.010, 882.00, 8.820, 0.260, 229.32),
    ('Moongphali Dana', 'Kgs', 9.000, 0.000, 0.000, 157.50, 0.000, 9.000, 1417.50),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 74.700, 56.400, 34.300, 61.83, 2120.803, 96.800, 5985.24),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Baking Powder', 'PKT', 1.000, 0.000, 0.000, 67.20, 0.000, 1.000, 67.20),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 0.900, 0.000, 0.000, 880.00, 0.000, 0.900, 792.00),
    ('Soya Bean Badiya', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.400, 0.000, 0.010, 2730.00, 27.300, 0.390, 1064.70),
    ('Amchur Powder', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 2.000, 2.000, 70.00, 140.000, 0.000, 0.00),
    ('Aachar', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('Cream', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('Paratha Masala', 'Kgs', 0.000, 10.000, 8.000, 10.00, 10.000, 2.000, 20.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 1085, 3000, 543, 3.186, 1730.00, 3542, 11284.81),
    ("Foil Box (Rice, Sabji)", "Nos", 2953, 4000, 1086, 1.575, 1710.45, 5867, 9240.53),
    ("Roti pouch", "Nos", 12800, 0, 2800, 0.236, 660.80, 10000, 2360.00),
    ("Salad Pkt", "Nos", 3340, 6000, 1086, 0.177, 192.22, 8254, 1460.96),
    ("Spoon/Mini Meal", "Nos", 675, 3000, 605, 0.504, 304.92, 3070, 1547.28),
    ("Napkin Tissue Paper", "Nos", 6707, 4200, 615, 0.354, 217.71, 10292, 3643.37),
    ("Salt Pouch", "Nos", 713, 3000, 543, 0.150, 81.45, 3170, 475.50),
    ("Pickle & Paratha", "Nos", 2566, 6048, 615, 0.896, 550.94, 7999, 7165.77),
    ("Tape", "Nos", 2, 8, 1, 23.600, 23.60, 9, 212.40),
    ("Big Foil Box (Biryani)", "Nos", 47, 300, 62, 3.150, 195.30, 285, 897.75),
    ("Paper Box (Lunch)", "Nos", 2062, 0, 543, 4.956, 2691.11, 1519, 7528.16),
    ("Butter Roti Paper", "NOS", 1400, 0, 100, 0.236, 23.60, 1300, 306.80),
    ("Paratha Box", "Nos", 767, 0, 72, 3.360, 241.92, 695, 2335.20),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 0, 5, 2, 141.600, 283.20, 3, 424.80),
    ("400 ML PP Box", "Nos", 166, 100, 0, 4.720, 0.00, 266, 1255.52),
    ("Silver foil", "Kgs", 2.400, 4.000, 0.750, 708.000, 531.00, 5.650, 4000.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 0.000, 24.000, 0.000, 280.00, 0.00, 24.000, 6720.00),
    ("Petha", "KGS", 0.000, 30.000, 15.000, 150.00, 2250.00, 15.000, 2250.00),
    ("Guldana", "KGS", 0.000, 16.000, 0.000, 250.00, 0.00, 16.000, 4000.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 0.000, 146.000, 6.000, 10.000, 60.000, 140.000, 1400.00),
    ("Onion", "Kgs", 48.500, 50.000, 15.000, 22.000, 330.000, 83.500, 1837.00),
    ("Tomato", "Kgs", 0.000, 40.000, 12.000, 25.000, 300.000, 28.000, 700.00),
    ("Ginger", "Kgs", 0.000, 4.000, 1.000, 85.000, 85.000, 3.000, 255.00),
    ("Garlic", "Kgs", 0.000, 2.510, 1.000, 154.000, 154.000, 1.510, 232.54),
    ("Pumpkin", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 0.000, 4.000, 2.000, 45.000, 90.000, 2.000, 90.00),
    ("Coriander", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 0.000, 33.000, 0.000, 18.000, 0.000, 33.000, 594.00),
    ("Beans", "Kgs", 0.000, 3.030, 3.030, 132.000, 399.960, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 3.050, 3.050, 35.000, 106.750, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 3.105, 3.105, 55.000, 170.775, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 90.000, 90.000, 15.000, 1350.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 4.860, 45.000, 20.000, 18.000, 360.000, 29.860, 537.48),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 0.000, 0.000, 25.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800, 25419.0),
    ("Paratha", 72, 70, 40.0, 2800, 1738.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 62, 60, 50.0, 3000, 877.0),
    ("Amul Kool", 14, 14, 25.0, 350, 308.0),
    ("Lahori Zeera", 18, 18, 10.0, 180, 162.0),
    ("Lassi", 30, 30, 20.0, 600, 570.0),
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
            ("MINI",     2, "02 X MINI LUNCH SAMPLE", "General"),
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
        print("🎉 Database successfully updated for 18 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
