import sqlite3

DATE = "2026-05-19"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 527.000, 0.000, 66.000, 31.00, 2046.000, 461.000, 14291.00),
    ('Rice', 'Kgs', 343.000, 0.000, 47.000, 65.00, 3055.000, 296.000, 19240.00),
    ('R/oil', 'Ltr', 132.500, 0.000, 14.000, 180.92, 2532.923, 118.500, 21439.38),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.150, 105.00, 15.750, 0.200, 21.00),
    ('Rajma', 'Kgs', 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 10.000, 0.000, 0.000, 78.00, 0.000, 10.000, 780.00),
    ('Besan', 'Kgs', 37.000, 0.000, 13.000, 94.50, 1228.500, 24.000, 2268.00),
    ('Dal Arhar', 'Kgs', 33.000, 0.000, 0.000, 120.00, 0.000, 33.000, 3960.00),
    ('Dal masoor (s)', 'Pkt', 7.000, 0.000, 0.000, 85.00, 0.000, 7.000, 595.00),
    ('Urad Dal Chilka', 'KGS', 3.000, 0.000, 0.000, 110.00, 0.000, 3.000, 330.00),
    ('Masoor Dal (Malika)', 'Kgs', 3.000, 0.000, 0.000, 85.00, 0.000, 3.000, 255.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 0.050, 0.000, 0.050, 315.00, 15.750, 0.000, 0.00),
    ('Haldi Powder', 'Kgs', 1.100, 0.000, 0.400, 231.00, 92.400, 0.700, 161.70),
    ('Mirchi Powder', 'Kgs', 1.400, 0.000, 0.300, 315.00, 94.500, 1.100, 346.50),
    ('Dal chini', 'Kgs', 0.270, 0.000, 0.030, 357.00, 10.710, 0.240, 85.68),
    ('Laung', 'Kgs', 0.140, 0.000, 0.030, 1155.00, 34.650, 0.110, 127.05),
    ('Hing', 'Nos', 14.000, 0.000, 5.000, 89.25, 446.250, 9.000, 803.25),
    ('Kitchen King', 'Kgs', 0.100, 0.000, 0.000, 800.00, 0.000, 0.100, 80.00),
    ('Degi Mirch', 'Kgs', 0.400, 0.000, 0.300, 960.00, 288.000, 0.100, 96.00),
    ('Kasuri Methi', 'Kgs', 0.280, 0.000, 0.080, 336.00, 26.880, 0.200, 67.20),
    ('Garam Masala', 'Kgs', 0.100, 0.000, 0.100, 920.00, 92.000, 0.000, 0.00),
    ('Salt', 'Kgs', 16.000, 0.000, 5.000, 28.00, 140.000, 11.000, 308.00),
    ('Dhaniya (s)', 'Kgs', 0.660, 0.000, 0.150, 157.50, 23.625, 0.510, 80.32),
    ('Jeera Powder', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('Badi Elaichi', 'Kgs', 0.120, 0.000, 0.030, 1995.00, 59.850, 0.090, 179.55),
    ('Methi Dana', 'Kgs', 0.100, 0.000, 0.100, 105.00, 10.500, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.350, 0.000, 0.030, 168.00, 5.040, 0.320, 53.76),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Desi Ghee', 'Kgs', 9.500, 0.000, 1.500, 504.00, 756.000, 8.000, 4032.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.280, 0.000, 0.080, 252.00, 20.160, 0.200, 50.40),
    ('Mirchi (s)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 0.600, 0.000, 0.100, 752.00, 75.200, 0.500, 376.00),
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
    ('Dhaniya Powder', 'Kgs', 2.100, 0.000, 0.300, 168.00, 50.400, 1.800, 302.40),
    ('Kali Mirch (s)', 'Kgs', 0.260, 0.000, 0.040, 882.00, 35.280, 0.220, 194.40),
    ('Moongphali Dana', 'Kgs', 9.000, 0.000, 0.000, 157.50, 0.000, 9.000, 1417.50),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 96.800, 28.400, 36.600, 61.83, 2263.014, 88.600, 5478.22),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Baking Powder', 'PKT', 1.000, 0.000, 1.000, 67.20, 67.200, 0.000, 0.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 0.900, 0.000, 0.000, 880.00, 0.000, 0.900, 792.00),
    ('Soya Bean Badiya', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.390, 0.000, 0.040, 2730.00, 109.200, 0.350, 955.50),
    ('Amchur Powder', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Aachar', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('Cream', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('Paratha Masala', 'Kgs', 2.000, 0.000, 0.000, 10.00, 0.000, 2.000, 20.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 3542, 0, 543, 3.186, 1730.00, 2999, 9554.81),
    ("Foil Box (Rice, Sabji)", "Nos", 5867, 0, 1086, 1.575, 1710.45, 4781, 7530.08),
    ("Roti pouch", "Nos", 10000, 0, 2700, 0.236, 637.20, 7300, 1722.80),
    ("Salad Pkt", "Nos", 8254, 0, 1086, 0.177, 192.22, 7168, 1268.74),
    ("Spoon/Mini Meal", "Nos", 3070, 0, 605, 0.504, 304.92, 2465, 1242.36),
    ("Napkin Tissue Paper", "Nos", 10292, 0, 614, 0.354, 217.36, 9678, 3426.01),
    ("Salt Pouch", "Nos", 3170, 0, 543, 0.150, 81.45, 2627, 394.05),
    ("Pickle & Paratha", "Nos", 7999, 0, 614, 0.896, 550.04, 7385, 6615.73),
    ("Tape", "Nos", 9, 0, 2, 23.600, 47.20, 7, 165.20),
    ("Big Foil Box (Biryani)", "Nos", 285, 0, 62, 3.150, 195.30, 223, 702.45),
    ("Paper Box (Lunch)", "Nos", 1519, 0, 543, 4.956, 2691.11, 976, 4837.06),
    ("Butter Roti Paper", "NOS", 1300, 0, 100, 0.236, 23.60, 1200, 283.20),
    ("Paratha Box", "Nos", 695, 0, 71, 3.360, 238.56, 624, 2096.64),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 3, 0, 1, 141.600, 141.60, 2, 283.20),
    ("400 ML PP Box", "Nos", 266, 0, 62, 4.720, 292.64, 204, 962.88),
    ("Silver foil", "Kgs", 5.650, 0, 0.750, 708.000, 531.00, 4.900, 3469.20),
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
    ("Potato", "Kgs", 140.000, 0, 16.000, 10.000, 160.000, 124.000, 1240.00),
    ("Onion", "Kgs", 83.500, 0, 14.000, 22.000, 308.000, 69.500, 1529.00),
    ("Tomato", "Kgs", 28.000, 0, 10.000, 25.000, 250.000, 18.000, 450.00),
    ("Ginger", "Kgs", 3.000, 0, 1.000, 85.000, 85.000, 2.000, 170.00),
    ("Garlic", "Kgs", 1.510, 0, 0.530, 154.000, 81.620, 0.980, 150.92),
    ("Pumpkin", "Kgs", 0.000, 0, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 2.000, 0, 2.000, 45.000, 90.000, 0.000, 0.00),
    ("Coriander", "Kgs", 0.000, 0, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 33.000, 0, 25.000, 18.000, 450.000, 8.000, 144.00),
    ("Beans", "Kgs", 0.000, 0, 0.000, 132.000, 0.000, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 0, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 29.860, 0, 15.000, 18.000, 270.000, 14.860, 267.48),
    ("Matar", "Kgs", 0.000, 0, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 15.000, 15.000, 75.000, 1125.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 0, 0.000, 25.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800, 26974.0),
    ("Paratha", 71, 70, 40.0, 2800, 1856.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 61, 60, 50.0, 3000, 1169.0),
    ("Amul Kool", 16, 16, 25.0, 400, 352.0),
    ("Lahori Zeera", 25, 25, 10.0, 250, 225.0),
    ("Lassi", 31, 31, 20.0, 620, 589.0),
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
        print("🎉 Database successfully updated for 19 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
