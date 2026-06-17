import sqlite3

DATE = "2026-05-30"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Aachar', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.750, 0.000, 0.000, 252.00, 0.000, 0.750, 189.00),
    ('Amchur Powder', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Atta', 'Kgs', 1296.000, 0.000, 22.000, 31.00, 682.000, 1274.000, 39494.00),
    ('Badi Elaichi', 'Kgs', 0.210, 0.010, 0.020, 1995.00, 19.950, 0.200, 399.00),
    ('Baking Powder', 'PKT', 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ('Besan', 'Kgs', 67.000, 0.000, 0.000, 94.50, 0.000, 67.000, 6331.50),
    ('Biryani Masala', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Chana Masala', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('Chana Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 1.800, 0.000, 0.000, 752.00, 0.000, 1.800, 1353.60),
    ('Chat Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Cream', 'Kgs', 4.500, 0.000, 0.000, 220.00, 0.000, 4.500, 990.00),
    ('Dal Arhar', 'Kgs', 71.000, 0.000, 0.000, 120.00, 0.000, 71.000, 8520.00),
    ('Dal Chana', 'Kgs', 78.000, 0.000, 0.000, 80.00, 0.000, 78.000, 6240.00),
    ('Dal chini', 'Kgs', 0.050, 0.010, 0.020, 357.00, 3.570, 0.040, 14.28),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('Dal masoor (s)', 'Pkt', 23.000, 0.000, 4.000, 85.00, 340.000, 19.000, 1615.00),
    ('Dhaniya (s)', 'Kgs', 1.660, 0.100, 0.200, 199.50, 19.950, 1.560, 311.23),
    ('Degi Mirch', 'Kgs', 4.100, 0.100, 0.200, 959.99, 95.999, 4.000, 3839.97),
    ('Desi Ghee', 'Kgs', 28.500, 0.500, 1.000, 504.00, 252.000, 28.000, 14112.00),
    ('Dhaniya Powder', 'Kgs', 6.300, 0.100, 0.200, 199.50, 19.950, 6.200, 1236.90),
    ('Imli', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('Imli (expensive)', 'Pkt', 3.700, 0.100, 0.200, 120.00, 12.000, 3.600, 432.00),
    ('Eno', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('Garam Masala', 'Kgs', 2.000, 0.100, 0.200, 920.00, 92.000, 1.900, 1747.99),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('Gulab Jal', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('Haldi Powder', 'Kgs', 8.000, 0.100, 0.200, 231.00, 23.100, 7.900, 1824.90),
    ('Hing', 'Nos', 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.070, 0.010, 0.020, 2730.00, 27.300, 0.060, 163.80),
    ('Jeera (s)', 'Kgs', 2.140, 0.050, 0.100, 315.00, 15.750, 2.090, 658.35),
    ('Jeera Powder', 'Kgs', 2.300, 0.100, 0.200, 420.00, 42.000, 2.200, 924.00),
    ('Kala Chana', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('Kali Mirch (s)', 'Kgs', 0.384, 0.010, 0.020, 882.00, 8.820, 0.374, 329.87),
    ('Kasuri Methi', 'Kgs', 0.850, 0.050, 0.100, 336.00, 16.800, 0.800, 268.80),
    ('Kewra Water', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Kitchen King', 'Kgs', 4.200, 0.100, 0.200, 800.00, 80.001, 4.100, 3280.03),
    ('Laung', 'Kgs', 0.210, 0.010, 0.020, 1155.00, 11.550, 0.200, 231.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 26.700, 56.800, 8.900, 61.83, 550.296, 74.600, 4612.59),
    ('Masoor Dal (Malika)', 'Kgs', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 12.000, 0.000, 0.000, 60.00, 0.000, 12.000, 720.00),
    ('Methi Dana', 'Kgs', 0.340, 0.000, 0.000, 105.00, 0.000, 0.340, 35.70),
    ('Mirchi (s)', 'Kgs', 0.750, 0.000, 0.000, 367.50, 0.000, 0.750, 275.63),
    ('Mirchi Powder', 'Kgs', 6.500, 0.100, 0.200, 315.00, 31.500, 6.400, 2016.00),
    ('Moong Dal Chilka', 'Kgs', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('Moongphali Dana', 'Kgs', 13.000, 0.000, 0.000, 168.00, 0.000, 13.000, 2184.00),
    ('Paratha Masala', 'Kgs', 11.000, 0.000, 0.000, 10.00, 0.000, 11.000, 110.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ('R/oil', 'Ltr', 312.000, 0.000, 5.000, 180.92, 904.615, 307.000, 55543.38),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Rajma', 'Kgs', 96.000, 0.000, 0.000, 115.00, 0.000, 96.000, 11040.00),
    ('Rajma Masala (Kgs)', 'Kgs', 1.900, 0.000, 0.000, 736.25, 0.000, 1.900, 1398.88),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Rice', 'Kgs', 882.000, 0.000, 12.000, 68.00, 816.000, 870.000, 59160.00),
    ('Rice (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Sabudana', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 1.000, 0.000, 0.000, 880.00, 0.000, 1.000, 880.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Salt', 'Kgs', 35.000, 2.000, 4.000, 28.00, 56.000, 33.000, 924.00),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.200, 0.000, 0.000, 105.00, 0.000, 0.200, 21.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Soya Bean Badiya', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.630, 0.010, 0.020, 168.00, 1.680, 0.620, 104.16),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Urad Dal Chilka', 'KGS', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2216, 0, 160, 3.186, 509.76, 2056, 6550.42),
    ("Foil Box (Rice, Sabji)", "Nos", 1934, 0, 284, 1.575, 447.30, 1650, 2598.75),
    ("Roti pouch", "Nos", 2500, 0, 700, 0.236, 165.20, 1800, 424.80),
    ("Salad Pkt", "Nos", 5328, 0, 284, 0.177, 50.27, 5044, 892.79),
    ("Spoon/Mini Meal", "Nos", 2369, 0, 160, 0.504, 80.64, 2209, 1113.34),
    ("Napkin Tissue Paper", "Nos", 7296, 0, 142, 0.354, 50.27, 7154, 2532.52),
    ("Salt Pouch", "Nos", 2437, 0, 142, 0.150, 21.30, 2295, 344.25),
    ("Pickle & Paratha", "Nos", 3203, 0, 142, 0.896, 127.21, 3061, 2742.15),
    ("Tape", "Nos", 2, 0, 1, 23.60, 23.60, 1, 23.60),
    ("Big Foil Box (Biryani)", "Nos", 99, 0, 18, 3.15, 56.70, 81, 255.15),
    ("Paper Box (Lunch)", "Nos", 4586, 0, 142, 4.956, 703.75, 4444, 22024.46),
    ("Butter Roti Paper", "Nos", 300, 0, 50, 0.236, 11.80, 250, 59.00),
    ("Paratha Box", "Nos", 132, 0, 0, 3.36, 0.00, 132, 443.52),
    ("Partition Box", "Nos", 47, 0, 0, 6.96, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 0, 0, 141.60, 0.00, 1, 141.60),
    ("400 ML PP Box", "Nos", 1, 0, 0, 4.72, 0.00, 1, 4.72),
    ("Silver foil", "Kgs", 0.150, 0, 0.150, 708.00, 106.20, 0.000, 0.00),
    ("Foil silver", "Kgs", 0, 0, 0, 531.00, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 2.000, 0, 2.000, 280.00, 560.00, 0.000, 0.00),
    ("Petha", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 43.00, 100.00, 10.50, 13.00, 136.50, 132.50, 1722.50),
    ("Onion", "Kgs", 4.00, 70.00, 6.00, 24.00, 144.00, 68.00, 1632.00),
    ("Tomato", "Kgs", 6.00, 70.00, 6.00, 25.00, 150.00, 70.00, 1750.00),
    ("Ginger", "Kgs", 0.50, 7.00, 0.50, 80.00, 40.00, 7.00, 560.00),
    ("Garlic", "Kgs", 0.54, 5.11, 0.56, 154.00, 86.24, 5.09, 783.86),
    ("Pumpkin", "Kgs", 0.00, 47.00, 16.00, 15.00, 240.00, 31.00, 465.00),
    ("Green chilli", "Kgs", 1.00, 10.00, 1.00, 65.00, 65.00, 10.00, 650.00),
    ("Coriander", "Kgs", 0.00, 3.00, 0.00, 35.00, 0.00, 3.00, 105.00),
    ("Capsicum", "Kgs", 0.00, 0.00, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("Beans", "Kgs", 0.00, 2.105, 0.00, 110.00, 0.00, 2.105, 231.55),
    ("Carrot", "Kgs", 0.00, 3.17, 0.00, 37.00, 0.00, 3.17, 117.29),
    ("Cauli flower", "Kgs", 0.00, 3.075, 0.00, 66.00, 0.00, 3.075, 202.95),
    ("Green onion", "Kgs", 0.00, 0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("Bottle GD", "Kgs", 0.00, 90.00, 0.00, 18.00, 0.00, 90.00, 1620.00),
    ("Cabbage", "Kgs", 0.00, 0, 0.00, 44.00, 0.00, 0.00, 0.00),
    ("Cucumber", "Kgs", 0.80, 19.96, 5.09, 24.00, 122.16, 15.67, 376.08),
    ("Matar", "Kgs", 0.00, 0, 0.00, 100.00, 0.00, 0.00, 0.00),
    ("Paneer", "Kgs", 0.00, 0, 0.00, 250.00, 0.00, 0.00, 0.00),
    ("Lime S", "Kgs", 0.00, 0, 0.00, 198.00, 0.00, 0.00, 0.00),
    ("Dahi", "Kgs", 0.00, 0, 0.00, 75.00, 0.00, 0.00, 0.00),
    ("Kulcha", "Kgs", 0.00, 0, 0.00, 30.00, 0.00, 0.00, 0.00),
    ("Tori", "Nos", 0.00, 0, 0.00, 25.00, 0.00, 0.00, 0.00),
    ("Pav", "Nos", 0.00, 6.00, 6.00, 35.00, 210.00, 0.00, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 142, 140, 70.0, 9800.0, 7870.0),
    ("MINI", 18, 16, 50.0, 800.0, 451.0),
    ("Amul Kool", 14, 14, 25.0, 350.0, 308.0),
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
            ("MINI",     2, "02 X MINI LUNCH SAMPLE", "General"),
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
        print("🎉 Database successfully updated for 30 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
