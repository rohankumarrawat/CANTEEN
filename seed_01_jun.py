import sqlite3

DATE = "2026-06-01"

dry_items = [
    ('Aachar', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.750, 0.000, 0.050, 252.00, 12.600, 0.700, 176.40),
    ('Amchur Powder', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Atta', 'Kgs', 1274.000, 0.000, 63.000, 31.00, 1953.000, 1211.000, 37541.00),
    ('Badi Elaichi', 'Kgs', 0.200, 0.000, 0.050, 1995.00, 99.750, 0.150, 299.25),
    ('Baking Powder', 'PKT', 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ('Besan', 'Kgs', 67.000, 0.000, 0.000, 94.50, 0.000, 67.000, 6331.50),
    ('Biryani Masala', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Chana Masala', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('Chana Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 1.800, 0.000, 0.100, 752.00, 75.200, 1.700, 1278.40),
    ('Chat Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Cream', 'Kgs', 4.500, 0.000, 0.000, 220.00, 0.000, 4.500, 990.00),
    ('Dal Arhar', 'Kgs', 71.000, 0.000, 3.000, 120.00, 360.000, 68.000, 8160.00),
    ('Dal Chana', 'Kgs', 78.000, 0.000, 8.000, 80.00, 640.000, 70.000, 5600.00),
    ('Dal chini', 'Kgs', 0.040, 0.000, 0.040, 357.00, 14.280, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('Dal masoor (s)', 'Pkt', 19.000, 0.000, 0.000, 85.00, 0.000, 19.000, 1615.00),
    ('Dhaniya (s)', 'Kgs', 1.560, 0.000, 0.160, 199.50, 31.921, 1.400, 279.31),
    ('Degi Mirch', 'Kgs', 4.000, 0.000, 0.300, 959.99, 287.998, 3.700, 3551.97),
    ('Desi Ghee', 'Kgs', 28.000, 0.000, 1.500, 504.00, 756.000, 26.500, 13356.00),
    ('Dhaniya Powder', 'Kgs', 6.200, 0.000, 0.300, 199.50, 59.850, 5.900, 1177.05),
    ('Imli', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('Imli (expensive)', 'Pkt', 3.600, 0.000, 0.600, 120.00, 72.000, 3.000, 360.00),
    ('Eno', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('Garam Masala', 'Kgs', 1.900, 0.000, 0.300, 920.00, 275.999, 1.600, 1471.99),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('Gulab Jal', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('Haldi Powder', 'Kgs', 7.900, 0.000, 0.400, 231.00, 92.400, 7.500, 1732.50),
    ('Hing', 'Nos', 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.060, 0.000, 0.010, 2730.00, 27.300, 0.050, 136.50),
    ('Jeera (s)', 'Kgs', 2.090, 0.000, 0.090, 315.00, 28.350, 2.000, 630.00),
    ('Jeera Powder', 'Kgs', 2.200, 0.000, 0.100, 420.00, 42.000, 2.100, 882.00),
    ('Kala Chana', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('Kali Mirch (s)', 'Kgs', 0.374, 0.000, 0.074, 882.00, 65.268, 0.300, 264.60),
    ('Kasuri Methi', 'Kgs', 0.800, 0.000, 0.050, 336.00, 16.800, 0.750, 252.00),
    ('Kewra Water', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Kitchen King', 'Kgs', 4.100, 0.000, 0.400, 800.01, 320.003, 3.700, 2960.02),
    ('Laung', 'Kgs', 0.200, 0.000, 0.040, 1155.00, 46.200, 0.160, 184.80),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 74.600, 56.400, 30.200, 61.83, 1867.296, 100.800, 6232.56),
    ('Masoor Dal (Malika)', 'Kgs', 15.000, 0.000, 3.000, 85.00, 255.000, 12.000, 1020.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 12.000, 0.000, 0.000, 60.00, 0.000, 12.000, 720.00),
    ('Methi Dana', 'Kgs', 0.340, 0.000, 0.000, 105.00, 0.000, 0.340, 35.70),
    ('Mirchi (s)', 'Kgs', 0.750, 0.000, 0.100, 367.50, 36.750, 0.650, 238.88),
    ('Mirchi Powder', 'Kgs', 6.400, 0.000, 0.400, 315.00, 126.000, 6.000, 1890.00),
    ('Moong Dal Chilka', 'Kgs', 15.000, 0.000, 3.000, 110.00, 330.000, 12.000, 1320.00),
    ('Moongphali Dana', 'Kgs', 13.000, 0.000, 0.000, 168.00, 0.000, 13.000, 2184.00),
    ('Paratha Masala', 'Kgs', 11.000, 0.000, 2.000, 10.00, 20.000, 9.000, 90.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/oil', 'Ltr', 307.000, 0.000, 9.000, 180.92, 1628.308, 298.000, 53915.08),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Rajma', 'Kgs', 96.000, 0.000, 0.000, 115.00, 0.000, 96.000, 11040.00),
    ('Rajma Masala (Kgs)', 'Kgs', 1.900, 0.000, 0.000, 736.25, 0.000, 1.900, 1398.88),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Rice', 'Kgs', 870.000, 0.000, 45.000, 68.00, 3060.000, 825.000, 56100.00),
    ('Rice (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Sabudana', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 1.000, 0.000, 0.000, 880.00, 0.000, 1.000, 880.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Salt', 'Kgs', 33.000, 0.000, 4.000, 28.00, 112.000, 29.000, 812.00),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.200, 0.000, 0.000, 105.00, 0.000, 0.200, 21.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Soya Bean Badiya', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.620, 0.000, 0.020, 168.00, 3.360, 0.600, 100.80),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Urad Dal Chilka', 'KGS', 15.000, 0.000, 3.000, 110.00, 330.000, 12.000, 1320.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    ("PP Box (Dal) Mini Meal", "Nos", 2056, 3500, 515, 3.186, 1640.79, 5041, 16060.63),
    ("Foil Box (Rice, Sabji)", "Nos", 1650, 4000, 1030, 1.680, 1730.40, 4620, 7761.60),
    ("Roti pouch", "Nos", 1800, 16000, 2800, 0.236, 660.80, 15000, 3540.00),
    ("Salad Pkt", "Nos", 5044, 5000, 1030, 0.177, 182.31, 9014, 1595.48),
    ("Spoon/Mini Meal", "Nos", 2209, 4000, 515, 0.504, 259.56, 5694, 2869.78),
    ("Napkin Tissue Paper", "Nos", 7154, 4200, 515, 0.354, 182.31, 10839, 3837.01),
    ("Salt Pouch", "Nos", 2295, 6000, 515, 0.150, 77.25, 7780, 1167.00),
    ("Pickle & Paratha", "Nos", 3061, 0, 515, 0.896, 461.35, 2546, 2280.79),
    ("Tape", "Nos", 1, 8, 2, 23.60, 47.20, 7, 165.20),
    ("Big Foil Box (Biryani)", "Nos", 81, 300, 60, 3.360, 201.60, 321, 1078.56),
    ("Paper Box (Lunch)", "Nos", 4444, 0, 515, 4.956, 2552.34, 3929, 19472.12),
    ("Butter Roti Paper", "Nos", 250.0, 0, 50.0, 0.236, 11.80, 200.0, 47.20),
    ("Paratha Box", "Nos", 132, 0, 71, 3.360, 238.56, 61, 204.96),
    ("Partition Box", "Nos", 47, 0, 0, 6.96, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 5, 1, 141.60, 141.60, 5, 708.00),
    ("400 ML PP Box", "Nos", 1, 100, 0, 4.72, 0.00, 101, 476.72),
    ("Silver foil", "Kg", 0.000, 2.000, 0.500, 708.00, 354.00, 1.500, 1062.00),
    ("Foil silver", "Kg", 0, 0, 0, 531.00, 0.00, 0, 0.00),
]

sweets_items = [
    ("Sweet (Burfi)", "KGS", 0.0, 24.0, 0.0, 280.0, 0.0, 24.0, 6720.0),
    ("Petha", "KGS", 15.0, 15.0, 15.0, 150.0, 2250.0, 15.0, 2250.0),
    ("Guldana", "KGS", 0.0, 16.0, 0.0, 250.0, 0.0, 16.0, 4000.0),
]

fresh_items = [
    ("Potato", "Kgs", 132.50, 0.0, 6.00, 13.00, 78.00, 126.50, 1644.50),
    ("Onion", "Kgs", 68.00, 0.0, 14.00, 24.00, 336.00, 54.00, 1296.00),
    ("Tomato", "Kgs", 70.00, 0.0, 14.00, 25.00, 350.00, 56.00, 1400.00),
    ("Ginger", "Kgs", 7.00, 0.0, 1.50, 80.00, 120.00, 5.50, 440.00),
    ("Garlic", "Kgs", 5.09, 0.0, 1.09, 154.00, 167.86, 4.00, 616.00),
    ("Pumpkin", "Kgs", 31.00, 0.0, 0.00, 15.00, 0.00, 31.00, 465.00),
    ("Green chilli", "Kgs", 10.00, 0.0, 2.00, 65.00, 130.00, 8.00, 520.00),
    ("Coriander", "Kgs", 3.00, 0.0, 1.00, 35.00, 35.00, 2.00, 70.00),
    ("Capsicum", "Kgs", 0.00, 0.0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("Beans", "Kgs", 2.105, 0.0, 2.105, 110.00, 231.55, 0.00, 0.00),
    ("Carrot", "Kgs", 3.17, 0.0, 3.17, 37.00, 117.29, 0.00, 0.00),
    ("Cauli flower", "Kgs", 3.075, 0.0, 3.075, 66.00, 202.95, 0.00, 0.00),
    ("Green onion", "Kgs", 0.00, 0.0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("Bottle GD", "Kgs", 90.00, 0.0, 90.00, 18.00, 1620.00, 0.00, 0.00),
    ("Cabbage", "Kgs", 0.00, 0.0, 0.00, 44.00, 0.00, 0.00, 0.00),
    ("Cucumber", "Kgs", 15.67, 0.0, 15.67, 24.00, 376.08, 0.00, 0.00),
    ("Matar", "Kgs", 0.00, 0.0, 0.00, 100.00, 0.00, 0.00, 0.00),
    ("Paneer", "Kgs", 0.00, 0.0, 0.00, 250.00, 0.00, 0.00, 0.00),
    ("Lime S", "Kgs", 0.00, 0.0, 0.00, 198.00, 0.00, 0.00, 0.00),
    ("Dahi", "Kgs", 0.00, 0.0, 0.00, 75.00, 0.00, 0.00, 0.00),
    ("Kulcha", "Kgs", 0.00, 0.0, 0.00, 30.00, 0.00, 0.00, 0.00),
    ("Tori", "Nos", 0.00, 0.0, 0.00, 25.00, 0.00, 0.00, 0.00),
    ("Pav", "Nos", 0.00, 0.0, 0.00, 35.00, 0.00, 0.00, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 515, 512, 70.0, 35840.0, 24842.0),
    ("Paratha", 71, 68, 40.0, 2720.0, 2280.0),
    ("Dahi", 240, 239, 10.0, 2390.0, 2151.0),
    ("Chach", 200, 193, 10.0, 1930.0, 1737.0),
    ("MINI", 60, 58, 50.0, 2900.0, 680.0),
    ("Amul Kool", 17, 17, 25.0, 425.0, 374.0),
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
        print("🎉 Database successfully updated for 01 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
