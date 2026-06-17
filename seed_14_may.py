import sqlite3

DATE = "2026-05-14"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Atta", "Kgs", 747.000, 0.000, 68.000, 31.00, 2108.000, 679.000, 21049.00),
    ("Rice", "Kgs", 497.000, 0.000, 48.000, 65.00, 3120.000, 449.000, 29185.00),
    ("R/oil", "Ltr", 169.500, 0.000, 12.000, 180.92, 2171.077, 157.500, 28495.38),
    ("Sarso Dana", "Kgs", 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ("Rajma", "Kgs", 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ("Urad (s)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Dal Chana", "Kgs", 31.000, 0.000, 0.000, 78.00, 0.000, 31.000, 2418.00),
    ("Besan", "Kgs", 39.000, 0.000, 2.000, 94.50, 189.000, 37.000, 3496.50),
    ("Dal Arhar", "Kgs", 44.000, 0.000, 0.000, 120.00, 0.000, 44.000, 5280.00),
    ("Dal masoor (s)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("Urad Dal Chilka", "KGS", 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ("Masoor Dal (Malika)", "Kgs", 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ("Moong Dal Chilka", "Kgs", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("Urad Dhuli", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("Lobia", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("Jeera (s)", "Kgs", 0.250, 0.000, 0.050, 315.00, 15.750, 0.200, 63.00),
    ("Haldi Powder", "Kgs", 2.500, 0.000, 0.300, 231.00, 69.300, 2.200, 508.20),
    ("Mirchi Powder", "Kgs", 2.600, 0.000, 0.300, 315.00, 94.500, 2.300, 724.50),
    ("Dal chini", "Kgs", 0.350, 0.000, 0.020, 357.00, 7.140, 0.330, 117.81),
    ("Laung", "Kgs", 0.220, 0.000, 0.020, 1155.00, 23.100, 0.200, 231.00),
    ("Hing", "Nos", 15.000, 0.000, 1.000, 89.25, 89.250, 14.000, 1249.50),
    ("Kitchen King", "Kgs", 1.000, 0.000, 0.200, 800.00, 160.000, 0.800, 640.00),
    ("Degi Mirch", "Kgs", 1.100, 0.000, 0.200, 960.00, 192.000, 0.900, 864.00),
    ("Kasuri Methi", "Kgs", 0.450, 0.000, 0.050, 336.00, 16.800, 0.400, 134.40),
    ("Garam Masala", "Kgs", 0.800, 0.000, 0.200, 920.00, 184.000, 0.600, 552.00),
    ("Salt", "Kgs", 30.000, 0.000, 4.000, 28.00, 112.000, 26.000, 728.00),
    ("Dhaniya (s)", "Kgs", 0.950, 0.000, 0.040, 157.50, 6.300, 0.910, 143.33),
    ("Jeera Powder", "Kgs", 0.200, 0.000, 0.200, 420.00, 84.000, 0.000, 0.00),
    ("Chana Masala (pkt)", "Pkt", 0.800, 0.000, 0.400, 736.01, 294.405, 0.400, 294.41),
    ("Badi Elaichi", "Kgs", 0.220, 0.000, 0.030, 1995.00, 59.850, 0.190, 379.05),
    ("Methi Dana", "Kgs", 0.110, 0.000, 0.010, 105.00, 1.050, 0.100, 10.50),
    ("Rajma Masala", "Pkt", 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ("Tej Patta", "Kgs", 0.420, 0.000, 0.010, 168.00, 1.680, 0.410, 68.88),
    ("Ajinomoto", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("Desi Ghee", "Kgs", 16.000, 0.000, 2.000, 504.00, 1008.000, 14.000, 7056.00),
    ("Sarson", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("Clean Wrap", "Pkt", 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ("Ajwain", "Pkt", 0.520, 0.000, 0.050, 252.00, 12.600, 0.470, 118.44),
    ("Mirchi (s)", "Kgs", 0.150, 0.000, 0.050, 315.00, 15.750, 0.100, 31.50),
    ("Chat Masala", "Kgs", 0.900, 0.000, 0.100, 752.00, 75.200, 0.800, 601.60),
    ("Rajma Masala (Kgs)", "Kgs", 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
    ("Gulab Jal", "BTL", 5.000, 0.000, 1.000, 66.15, 66.152, 4.000, 264.61),
    ("Chana Masala", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("Kala Chana", "Kgs", 58.000, 0.000, 17.000, 78.00, 1326.000, 41.000, 3198.00),
    ("Vinegar", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("Red Chilli Sauce", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("Matar Paneer Masala", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("Pav Bhaji Masala", "BTL", 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ("Matar (TF)", "Kgs", 9.000, 0.000, 0.000, 60.00, 0.000, 9.000, 540.00),
    ("Star Phool Masala", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("Food Colour", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("Kewra Water", "BTL", 6.000, 0.000, 1.000, 70.80, 70.800, 5.000, 354.00),
    ("Biryani Masala", "Pkt", 7.000, 0.000, 3.000, 73.50, 220.500, 4.000, 294.00),
    ("Elaichi Small Gr", "Kgs", 0.060, 0.000, 0.020, 3150.00, 63.000, 0.040, 126.00),
    ("Dhaniya Powder", "Kgs", 3.200, 0.000, 0.300, 168.00, 50.400, 2.900, 487.20),
    ("Kali Mirch (s)", "Kgs", 0.320, 0.000, 0.020, 882.00, 17.640, 0.300, 264.60),
    ("Moongphali Dana", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("Sambhar Masala", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 49.100, 0.000, 28.200, 61.83, 1743.634, 20.900, 1292.27),
    ("Rai", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("Sugar", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("Baking Powder", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("Shahi Paneer Masala (pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("Shahi Paneer Masala (kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("Soya Bean Badiya", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("Javitri", "Kgs", 0.500, 0.000, 0.020, 2730.00, 54.600, 0.480, 1310.40),
    ("Amchur Powder", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("Dal Makhani Masala", "Pkt", 5.000, 0.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("Black Pepper Powder", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Sabji Masala", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("Aachar", "Kgs", 4.000, 0.000, 1.000, 147.00, 147.000, 3.000, 441.00),
    ("Cream", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("Paratha Masala", "Kgs", 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ("Khus Khus", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("Gud", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2834, 0, 543, 3.186, 1730.00, 2291, 7299.13),
    ("Foil Box (Rice, Sabji)", "Nos", 4966, 0, 1086, 1.575, 1710.45, 3880, 6111.00),
    ("Roti pouch", "Nos", 19200, 0, 2800, 0.236, 660.80, 16400, 3870.40),
    ("Salad Pkt", "Nos", 5796, 0, 1086, 0.177, 192.22, 4710, 833.67),
    ("Spoon/Mini Meal", "Nos", 1964, 0, 604, 0.504, 304.42, 1360, 685.44),
    ("Napkin Tissue Paper", "Nos", 7934, 0, 611, 0.354, 216.29, 7323, 2592.34),
    ("Salt Pouch", "Nos", 1941, 0, 543, 0.150, 81.45, 1398, 209.70),
    ("Pickle & Paratha", "Nos", 3935, 0, 611, 0.896, 547.35, 3324, 2977.75),
    ("Tape", "Nos", 6, 0, 1, 23.600, 23.60, 5, 118.00),
    ("Big Foil Box (Biryani)", "Nos", 186, 0, 61, 3.150, 192.15, 125, 393.75),
    ("Paper Box (Lunch)", "Nos", 3290, 0, 543, 4.956, 2691.11, 2747, 13614.13),
    ("Butter Roti Paper", "NOS", 1700, 0, 50, 0.236, 11.80, 1650, 389.40),
    ("Paratha Box", "Nos", 908, 0, 68, 3.360, 228.48, 840, 2822.40),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 3, 0, 2, 141.600, 283.20, 1, 141.60),
    ("400 ML PP Box", "Nos", 166, 0, 0, 4.720, 0.00, 166, 783.52),
    ("Silver foil", "Kgs", 3.5, 0, 0.600, 708.000, 424.80, 2.900, 2053.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 2.000, 0, 0.000, 280.00, 0.00, 2.000, 560.00),
    ("Petha", "KGS", 15.000, 0, 15.000, 150.00, 2250.00, 0.000, 0.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 30.000, 47.000, 61.000, 10.000, 610.000, 16.000, 160.00),
    ("Onion", "Kgs", 82.000, 0.000, 14.000, 22.000, 308.000, 68.000, 1496.00),
    ("Tomato", "Kgs", 27.000, 0.000, 14.000, 16.000, 224.000, 13.000, 208.00),
    ("Ginger", "Kgs", 5.000, 0.000, 2.000, 135.000, 270.000, 3.000, 405.00),
    ("Garlic", "Kgs", 1.480, 0.000, 0.700, 143.000, 100.100, 0.780, 111.54),
    ("Pumpkin", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 4.020, 0.000, 2.000, 60.000, 120.000, 2.020, 121.20),
    ("Coriander", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 12.000, 0.000, 12.000, 22.000, 264.000, 0.000, 0.00),
    ("Beans", "Kgs", 0.000, 10.045, 10.045, 121.000, 1215.445, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 20.280, 20.280, 35.000, 709.800, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 30.625, 30.625, 55.000, 1684.375, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 47.000, 0.000, 19.000, 20.000, 380.000, 28.000, 560.00),
    ("Matar", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 10.000, 0.000, 25.000, 0.000, 10.000, 250.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800, 29612.0),
    ("Paratha", 68, 67, 40.0, 2680, 1819.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 61, 59, 50.0, 2950, 873.0),
    ("Amul Kool", 9, 9, 25.0, 225, 198.0),
    ("Lahori Zeera", 11, 11, 10.0, 110, 99.0),
    ("Lassi", 11, 11, 20.0, 220, 209.0),
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
            ("LUNCH",    3, "03 X LUNCH SAMPLE",      "General"),
            ("Paratha",  1, "01 X PARATHA SAMPLE",    "General"),
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
        print("🎉 Database successfully updated for 14 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
