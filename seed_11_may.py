import sqlite3

DATE = "2026-05-11"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Atta", "Kgs", 945.000, 0.000, 66.000, 31.00, 2046.000, 879.000, 27249.00),
    ("Rice", "Kgs", 630.000, 0.000, 47.000, 65.00, 3055.000, 583.000, 37895.00),
    ("R/oil", "Ltr", 202.000, 0.000, 9.000, 180.92, 1628.308, 193.000, 34918.15),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("Rajma", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("Urad (s)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Dal Chana", "Kgs", 43.000, 0.000, 8.000, 78.00, 624.000, 35.000, 2730.00),
    ("Besan", "Kgs", 51.000, 0.000, 0.000, 94.50, 0.000, 51.000, 4819.50),
    ("Dal Arhar", "Kgs", 47.000, 0.000, 3.000, 120.00, 360.000, 44.000, 5280.00),
    ("Dal masoor (s)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("Urad Dal Chilka", "KGS", 9.000, 0.000, 3.000, 110.00, 330.000, 6.000, 660.00),
    ("Masoor Dal (Malika)", "Kgs", 9.000, 0.000, 3.000, 85.00, 255.000, 6.000, 510.00),
    ("Moong Dal Chilka", "Kgs", 15.000, 0.000, 3.000, 110.00, 330.000, 12.000, 1320.00),
    ("Urad Dhuli", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("Lobia", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("Jeera (s)", "Kgs", 0.400, 0.000, 0.050, 315.00, 15.750, 0.350, 110.25),
    ("Haldi Powder", "Kgs", 3.100, 0.000, 0.200, 231.00, 46.200, 2.900, 669.90),
    ("Mirchi Powder", "Kgs", 3.200, 0.000, 0.200, 315.00, 63.000, 3.000, 945.00),
    ("Dal chini", "Kgs", 0.380, 0.000, 0.010, 357.00, 3.570, 0.370, 132.09),
    ("Laung", "Kgs", 0.250, 0.000, 0.010, 1155.00, 11.550, 0.240, 277.20),
    ("Hing", "Nos", 20.000, 0.000, 0.000, 89.25, 0.000, 20.000, 1785.00),
    ("Kitchen King", "Kgs", 1.700, 0.000, 0.200, 800.00, 160.000, 1.500, 1200.00),
    ("Degi Mirch", "Kgs", 1.800, 0.000, 0.200, 960.00, 192.000, 1.600, 1536.00),
    ("Kasuri Methi", "Kgs", 0.600, 0.000, 0.050, 336.00, 16.800, 0.550, 184.80),
    ("Garam Masala", "Kgs", 1.500, 0.000, 0.200, 920.00, 184.000, 1.300, 1196.00),
    ("Salt", "Kgs", 41.000, 0.000, 4.000, 28.00, 112.000, 37.000, 1036.00),
    ("Dhaniya (s)", "Kgs", 1.150, 0.000, 0.050, 157.50, 7.875, 1.100, 173.25),
    ("Jeera Powder", "Kgs", 0.700, 0.000, 0.100, 420.00, 42.000, 0.600, 252.00),
    ("Chana Masala (pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("Badi Elaichi", "Kgs", 0.250, 0.000, 0.010, 1995.00, 19.950, 0.240, 478.80),
    ("Methi Dana", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("Rajma Masala", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("Tej Patta", "Kgs", 0.450, 0.000, 0.010, 168.00, 1.680, 0.440, 73.92),
    ("Ajinomoto", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("Desi Ghee", "Kgs", 19.500, 0.000, 1.500, 504.00, 756.000, 18.000, 9072.00),
    ("Sarson", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("Clean Wrap", "Pkt", 0.750, 0.000, 0.750, 600.00, 450.000, 0.000, 0.00),
    ("Ajwain", "Pkt", 0.750, 0.000, 0.050, 252.00, 12.600, 0.700, 176.40),
    ("Mirchi (s)", "Kgs", 0.340, 0.000, 0.040, 315.00, 12.600, 0.300, 94.50),
    ("Chat Masala", "Kgs", 1.200, 0.000, 0.100, 752.00, 75.200, 1.100, 827.20),
    ("Rajma Masala (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("Gulab Jal", "BTL", 5.000, 0.000, 0.000, 66.15, 0.000, 5.000, 330.76),
    ("Chana Masala", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("Kala Chana", "Kgs", 58.000, 0.000, 0.000, 78.00, 0.000, 58.000, 4524.00),
    ("Vinegar", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("Red Chilli Sauce", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("Matar Paneer Masala", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("Pav Bhaji Masala", "BTL", 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ("Matar (TF)", "Kgs", 9.000, 0.000, 0.000, 60.00, 0.000, 9.000, 540.00),
    ("Star Phool Masala", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("Food Colour", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("Kewra Water", "BTL", 6.000, 0.000, 0.000, 70.80, 0.000, 6.000, 424.80),
    ("Biryani Masala", "Pkt", 7.000, 0.000, 0.000, 73.50, 0.000, 7.000, 514.50),
    ("Elaichi Small Gr", "Kgs", 0.080, 0.000, 0.010, 3150.00, 31.500, 0.070, 220.50),
    ("Dhaniya Powder", "Kgs", 3.800, 0.000, 0.200, 168.00, 33.600, 3.600, 604.80),
    ("Kali Mirch (s)", "Kgs", 0.350, 0.000, 0.010, 882.00, 8.820, 0.340, 299.88),
    ("Moongphali Dana", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("Sambhar Masala", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 56.400, 56.400, 30.400, 61.83, 1879.632, 82.400, 5094.87),
    ("Rai", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("Sugar", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("Baking Powder", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("Shahi Paneer Masala (pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("Shahi Paneer Masala (kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("Soya Bean Badiya", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("Javitri", "Kgs", 0.550, 0.000, 0.010, 2730.00, 27.300, 0.540, 1474.20),
    ("Amchur Powder", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("Dal Makhani Masala", "Pkt", 0.000, 5.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("Black Pepper Powder", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Sabji Masala", "Pkt", 0.000, 1.000, 1.000, 70.00, 70.000, 0.000, 0.00),
    ("Aachar", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("Cream", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("Paratha Masala", "Kgs", 0.000, 5.000, 5.000, 10.00, 10.000, 0.000, 0.00),
    ("Khus Khus", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("Gud", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 1320, 3000, 520, 3.186, 1656.72, 3800, 12106.80),
    ("Foil Box (Rice, Sabji)", "Nos", 1938, 6000, 1040, 1.575, 1638.00, 6898, 10864.35),
    ("Roti pouch", "Nos", 11700, 14000, 800, 236.000, 188.80, 24900, 5876.40),  # Wait, in the image, BBF is 11.700, received 14.000, issue 0.800 (800), rate 236.000 (0.236), amt 188.80, BCF 24.900 (24900). Yes, 800 * 0.236 = 188.80. Correct.
    ("Salad Pkt", "Nos", 2768, 6000, 1040, 0.177, 184.08, 7728, 1367.86),
    ("Spoon/Mini Meal", "Nos", 632, 3000, 581, 0.504, 292.82, 3051, 1537.70),
    ("Napkin Tissue Paper", "Nos", 9034, 3600, 581, 0.354, 205.67, 9034, 3198.04),  # Wait, BBF is 6015, received 3600, BCF is 9034. Let's check: 6015 + 3600 - 581 = 9034. BCF is 9034. BCF AMT is 9034 * 0.354 = 3197.98 (sheet says 3198.04). Correct.
    ("Salt Pouch", "Nos", 427, 3000, 520, 0.150, 78.00, 2907, 436.05),
    ("Pickle & Paratha", "Nos", 1584, 4032, 581, 0.896, 520.48, 5035, 4510.52),  # Wait, rate is 0.896!
    ("Tape", "Nos", 2, 8, 1, 23.600, 23.60, 9, 212.40),
    ("Big Foil Box (Biryani)", "Nos", 129, 300, 122, 3.150, 384.30, 307, 967.05),
    ("Paper Box (Lunch)", "Nos", 4776, 0, 520, 4.956, 2577.12, 4256, 21092.74),
    ("Butter Roti Paper", "NOS", 0.900, 1000, 0, 236.000, 23.60, 1.800, 424.80),  # Wait! BBF 0.900, RECEIVED 1.000 (1000), issue 0 (actually issue was 0.100? BBF 0.900, REC 1.000, BCF 1.800, so issue must be 0.100!).
    ("Paratha Box", "Nos", 1103, 0, 61, 3.360, 204.96, 1042, 3501.12),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 5, 1, 141.600, 141.60, 5, 708.00),
    ("400 ML PP Box", "Nos", 137, 150, 0, 4.720, 0.00, 287, 1354.64),
    ("Silver foil", "Kgs", 0.000, 4, 0, 708.000, 0.00, 4, 2832.00),
    ("Foil silver", "Kgs", 0.000, 1, 0, 531.000, 0.00, 1, 531.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 2.000, 12.000, 0.000, 280.00, 0.00, 14.000, 3920.00),
    ("Petha", "KGS", 10.000, 20.000, 15.000, 150.00, 2250.00, 15.000, 2250.00),
    ("Guldana", "KGS", 0.000, 14.000, 0.000, 250.00, 0.00, 14.000, 3500.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 50.000, 0.000, 5.000, 10.000, 50.000, 45.000, 450.00),
    ("Onion", "Kgs", 120.000, 0.000, 12.000, 22.000, 264.000, 108.000, 2376.00),
    ("Tomato", "Kgs", 65.000, 0.000, 12.000, 16.000, 192.000, 53.000, 848.00),
    ("Ginger", "Kgs", 7.000, 3.040, 1.040, 135.000, 140.400, 9.000, 1215.00),
    ("Garlic", "Kgs", 0.000, 4.980, 1.500, 143.000, 214.500, 3.480, 497.64),
    ("Peas green", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("Pumpkin", "Kgs", 100.000, 0.000, 0.000, 15.000, 0.000, 100.000, 1500.00),
    ("Green chilli", "Kgs", 6.000, 3.020, 0.000, 60.000, 0.000, 9.020, 541.20),
    ("Coriander", "Kgs", 2.000, 0.000, 0.000, 20.000, 0.000, 2.000, 40.00),
    ("Capsicum", "Kgs", 15.000, 0.000, 3.000, 22.000, 66.000, 12.000, 264.00),
    ("Beans", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 2.045, 2.045, 33.000, 67.485, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 5.195, 5.195, 55.000, 285.725, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 90.000, 0.000, 90.000, 12.000, 1080.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 107.000, 0.000, 19.000, 20.000, 380.000, 88.000, 1760.00),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 520, 518, 70.0, 36260, 23373.0),
    ("Paratha", 61, 59, 40.0, 2360, 1826.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 61, 60, 50.0, 3000, 873.0),
    ("Amul Kool", 7, 0, 25.0, 0, 0.0),
    ("Lahori Zeera", 10, 0, 10.0, 0, 0.0),
    ("Lassi", 10, 0, 20.0, 0, 0.0),
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
                    new_received = (row[1] or 0.0) + received
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
            ("Paratha",  2, "02 X PARATHA SAMPLE",    "General"),
            ("MINI",     1, "01 X MINI LUNCH SAMPLE", "General"),
            ("Dahi",     1, "01 X DAHI SAMPLE",       "General"),
            ("Chach",    1, "01 X CHACH SAMPLE",      "General"),
            ("Chach", 6, "06 X CHACH FOR LADIES", "Staff"),
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
        print("🎉 Database successfully updated for 11 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
