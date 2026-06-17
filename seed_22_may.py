import sqlite3

DATE = "2026-05-22"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Atta', 'Kgs', 329.000, 0.000, 67.000, 31.00, 2077.000, 262.000, 8122.00),
    ('Rice', 'Kgs', 210.000, 0.000, 47.000, 65.00, 3055.000, 163.000, 10595.00),
    ('R/oil', 'Ltr', 97.500, 0.000, 10.000, 180.92, 1809.231, 87.500, 15830.77),
    ('Sarso Dana', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('Rajma', 'Kgs', 31.000, 0.000, 0.000, 115.00, 0.000, 31.000, 3565.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Dal Chana', 'Kgs', 10.000, 0.000, 10.000, 78.00, 780.000, 0.000, 0.00),
    ('Besan', 'Kgs', 22.000, 0.000, 2.000, 94.50, 189.000, 20.000, 1890.00),
    ('Dal Arhar', 'Kgs', 31.000, 0.000, 10.000, 120.00, 1200.000, 21.000, 2520.00),
    ('Dal masoor (s)', 'Pkt', 7.000, 0.000, 0.000, 85.00, 0.000, 7.000, 595.00),
    ('Urad Dal Chilka', 'KGS', 3.000, 0.000, 0.000, 110.00, 0.000, 3.000, 330.00),
    ('Masoor Dal (Malika)', 'Kgs', 3.000, 0.000, 0.000, 85.00, 0.000, 3.000, 255.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('Jeera (s)', 'Kgs', 0.940, 0.000, 0.000, 315.00, 0.000, 0.940, 296.10),
    ('Haldi Powder', 'Kgs', 2.900, 0.000, 0.300, 231.00, 69.300, 2.600, 600.60),
    ('Mirchi Powder', 'Kgs', 2.400, 0.000, 0.300, 315.00, 94.500, 2.100, 661.50),
    ('Dal chini', 'Kgs', 0.160, 0.000, 0.030, 357.00, 10.710, 0.130, 46.41),
    ('Laung', 'Kgs', 0.030, 0.000, 0.030, 1155.00, 34.650, 0.000, 0.00),
    ('Hing', 'Nos', 9.000, 0.000, 0.000, 89.25, 0.000, 9.000, 803.25),
    ('Kitchen King', 'Kgs', 1.800, 0.000, 0.300, 800.00, 240.000, 1.500, 1200.00),
    ('Degi Mirch', 'Kgs', 1.700, 0.000, 0.300, 960.00, 288.000, 1.400, 1344.00),
    ('Kasuri Methi', 'Kgs', 0.100, 0.000, 0.050, 336.00, 16.800, 0.050, 16.80),
    ('Garam Masala', 'Kgs', 0.000, 0.000, 0.000, 920.00, 0.000, 0.000, 0.00),
    ('Salt', 'Kgs', 3.000, 0.000, 3.000, 28.00, 84.000, 0.000, 0.00),
    ('Dhaniya (s)', 'Kgs', 0.310, 0.000, 0.100, 157.50, 15.750, 0.210, 33.07),
    ('Jeera Powder', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('Badi Elaichi', 'Kgs', 0.030, 0.000, 0.030, 1995.00, 59.850, 0.000, 0.00),
    ('Methi Dana', 'Kgs', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.270, 0.000, 0.030, 168.00, 5.040, 0.240, 40.32),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Desi Ghee', 'Kgs', 6.000, 0.000, 1.500, 504.00, 756.000, 4.500, 2268.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.050, 0.000, 0.050, 252.00, 12.600, 0.000, 0.00),
    ('Mirchi (s)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 0.400, 0.000, 0.000, 752.00, 0.000, 0.400, 300.80),
    ('Rajma Masala (Kgs)', 'Kgs', 1.100, 0.000, 0.000, 736.00, 0.000, 1.100, 809.60),
    ('Gulab Jal', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('Chana Masala', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Kala Chana', 'Kgs', 23.000, 0.000, 0.000, 78.00, 0.000, 23.000, 1794.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 5.000, 0.000, 4.000, 60.00, 240.000, 1.000, 60.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 1.000, 0.000, 0.000, 68.44, 0.000, 1.000, 68.44),
    ('Kewra Water', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('Biryani Masala', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Dhaniya Powder', 'Kgs', 1.100, 0.000, 0.300, 168.00, 50.400, 0.800, 134.40),
    ('Kali Mirch (s)', 'Kgs', 0.154, 0.000, 0.030, 882.00, 26.460, 0.124, 109.37),
    ('Moongphali Dana', 'Kgs', 1.000, 0.000, 1.000, 157.50, 157.500, 0.000, 0.00),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 43.600, 0.000, 18.000, 61.83, 1112.958, 25.600, 1582.87),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Baking Powder', 'PKT', 0.000, 0.000, 0.000, 67.20, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 0.500, 0.000, 0.400, 880.00, 352.000, 0.100, 88.00),
    ('Soya Bean Badiya', 'kgs', 10.000, 0.000, 0.000, 94.50, 0.000, 10.000, 945.00),
    ('Javitri', 'Kgs', 0.290, 0.000, 0.030, 2730.00, 81.900, 0.260, 709.80),
    ('Amchur Powder', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 3.000, 0.000, 2.000, 70.00, 140.000, 1.000, 70.00),
    ('Aachar', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('Cream', 'Kgs', 2.500, 0.000, 2.000, 220.00, 440.000, 0.500, 110.00),
    ('Paratha Masala', 'Kgs', 31.000, 0.000, 10.000, 10.00, 100.000, 21.000, 210.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('Eno', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('Imli', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('Rice (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('Imli (expensive)', 'Pkt', 1.000, 0.000, 0.000, 120.00, 0.000, 1.000, 120.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2013, 0, 1126, 3.186, 3587.44, 887, 2825.98),
    ("Foil Box (Rice, Sabji)", "Nos", 2809, 0, 533, 1.575, 839.48, 2276, 3584.70),
    ("Roti pouch", "Nos", 1800, 2000, 2800, 0.236, 660.80, 1000, 236.00),
    ("Salad Pkt", "Nos", 5196, 0, 1066, 0.177, 188.68, 4130, 731.01),
    ("Spoon/Mini Meal", "Nos", 1362, 0, 593, 0.504, 298.87, 769, 387.58),
    ("Napkin Tissue Paper", "Nos", 8560, 0, 605, 0.354, 214.17, 7955, 2816.07),
    ("Salt Pouch", "Nos", 1641, 0, 533, 0.150, 79.95, 1108, 166.20),
    ("Pickle & Paratha", "Nos", 6267, 0, 605, 0.896, 541.98, 5662, 5072.21),
    ("Tape", "Nos", 3, 0, 2, 23.600, 47.20, 1, 23.60),
    ("Big Foil Box (Biryani)", "Nos", 106, 0, 60, 3.150, 189.00, 46, 144.90),
    ("Paper Box (Lunch)", "Nos", 1090, 0, 533, 4.956, 2641.55, 557, 2760.49),
    ("Butter Roti Paper", "Nos", 1000, 0, 200, 0.236, 47.20, 800, 188.80),
    ("Paratha Box", "Nos", 492, 0, 72, 3.360, 241.92, 420, 1411.20),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 0, 1, 141.600, 141.60, 0, 0.00),
    ("400 ML PP Box", "Nos", 87, 0, 0, 4.720, 0.00, 87, 410.64),
    ("Silver foil", "Kgs", 3.650, 0, 0.750, 708.000, 531.00, 2.900, 2053.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 12.000, 0, 12.000, 280.00, 3360.00, 0.000, 0.00),
    ("Petha", "KGS", 0.000, 0, 0.000, 150.00, 0.00, 0.000, 0.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 8.000, 0, 0.000, 10.000, 0.00, 8.000, 80.00),
    ("Onion", "Kgs", 83.500, 0, 20.000, 22.000, 440.00, 63.500, 1397.00),
    ("Tomato", "Kgs", 14.000, 0, 12.000, 25.000, 300.00, 2.000, 50.00),
    ("Ginger", "Kgs", 0.000, 2.045, 1.500, 138.000, 207.00, 0.545, 75.21),
    ("Garlic", "Kgs", 0.580, 0, 0.500, 154.000, 77.00, 0.080, 12.32),
    ("Pumpkin", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("Green chilli", "Kgs", 4.060, 0, 2.060, 35.000, 72.10, 2.000, 70.00),
    ("Coriander", "Kgs", 0.000, 0, 0.000, 45.000, 0.00, 0.000, 0.00),
    ("Capsicum", "Kgs", 0.000, 0, 0.000, 18.000, 0.00, 0.000, 0.00),
    ("Beans", "Kgs", 0.000, 0, 0.000, 121.000, 0.00, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0, 0.000, 55.000, 0.00, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0, 0.000, 15.000, 0.00, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("Cucumber", "Kgs", 13.860, 4.140, 18.000, 20.000, 360.00, 0.000, 0.00),
    ("Matar", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 16.000, 16.000, 250.000, 4000.00, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0, 0.000, 75.000, 0.00, 0.000, 0.00),
    ("Kulcha", "Kgs", 0.000, 30.000, 30.000, 30.000, 900.00, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("Pav", "Nos", 0.000, 0, 0.000, 10.000, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 533, 530, 70.0, 37100, 30694.0),
    ("Paratha", 71, 70, 40.0, 2800, 1664.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 60, 58, 50.0, 2900, 1108.0),
    ("Amul Kool", 15, 15, 25.0, 375, 330.0),
    ("Lahori Zeera", 5, 5, 10.0, 50, 45.0),
    ("Lassi", 20, 20, 20.0, 400, 380.0),
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
        print("🎉 Database successfully updated for 22 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
