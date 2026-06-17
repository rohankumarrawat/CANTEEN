import sqlite3

DATE = "2026-05-04"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Atta", "Kgs", 1281.000, 0.000, 66.000, 31.00, 2046.000, 1215.000, 37665.00),
    ("Rice", "Kgs", 851.000, 0.000, 36.000, 65.00, 2340.000, 815.000, 52975.00),
    ("R/oil", "Ltr", 261.000, 0.000, 7.000, 180.92, 1266.462, 254.000, 45954.46),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("Rajma", "Kgs", 83.000, 0.000, 0.000, 115.00, 0.000, 83.000, 9545.00),
    ("Urad (s)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Dal Chana", "Kgs", 70.000, 0.000, 15.000, 78.00, 1170.000, 55.000, 4290.00),
    ("Besan", "Kgs", 70.000, 0.000, 0.000, 94.50, 0.000, 70.000, 6615.00),
    ("Dal Arhar", "Kgs", 58.000, 0.000, 3.000, 120.00, 360.000, 55.000, 6600.00),
    ("Dal masoor (s)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("Urad Dal Chilka", "KGS", 12.000, 0.000, 3.000, 110.00, 330.000, 9.000, 990.00),
    ("Masoor Dal (Malika)", "Kgs", 12.000, 0.000, 3.000, 85.00, 255.000, 9.000, 765.00),
    ("Moong Dal Chilka", "Kgs", 18.000, 0.000, 3.000, 110.00, 330.000, 15.000, 1650.00),
    ("Urad Dhuli", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("Lobia", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("Jeera (s)", "Kgs", 1.700, 0.000, 0.100, 315.00, 31.500, 1.600, 504.00),
    ("Haldi Powder", "Kgs", 4.700, 0.000, 0.300, 231.00, 69.300, 4.400, 1016.40),
    ("Mirchi Powder", "Kgs", 4.800, 0.000, 0.300, 315.00, 94.500, 4.500, 1417.50),
    ("Dal chini", "Kgs", 0.440, 0.000, 0.010, 357.00, 3.570, 0.430, 153.51),
    ("Laung", "Kgs", 0.310, 0.000, 0.010, 1155.00, 11.550, 0.300, 346.50),
    ("Hing", "Nos", 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ("Kitchen King", "Kgs", 2.800, 0.000, 0.200, 800.00, 160.000, 2.600, 2080.00),
    ("Degi Mirch", "Kgs", 2.900, 0.000, 0.200, 960.00, 192.000, 2.700, 2592.00),
    ("Kasuri Methi", "Kgs", 0.850, 0.000, 0.050, 336.00, 16.800, 0.800, 268.80),
    ("Garam Masala", "Kgs", 2.800, 0.000, 0.300, 920.00, 276.000, 2.500, 2300.00),
    ("Salt", "Kgs", 62.000, 0.000, 4.000, 28.00, 112.000, 58.000, 1624.00),
    ("Dhaniya (s)", "Kgs", 1.650, 0.000, 0.200, 157.50, 31.500, 1.450, 228.38),
    ("Jeera Powder", "Kgs", 2.000, 0.000, 0.000, 420.00, 0.000, 2.000, 840.00),
    ("Chana Masala (pkt)", "Pkt", 1.100, 0.000, 0.100, 736.01, 73.601, 1.000, 736.01),
    ("Badi Elaichi", "Kgs", 0.310, 0.000, 0.010, 1995.00, 19.950, 0.300, 598.50),
    ("Methi Dana", "Kgs", 0.370, 0.000, 0.010, 105.00, 1.050, 0.360, 37.80),
    ("Rajma Masala", "Pkt", 6.000, 0.000, 0.000, 72.00, 0.000, 6.000, 432.00),
    ("Tej Patta", "Kgs", 0.510, 0.000, 0.010, 168.00, 1.680, 0.500, 84.00),
    ("Ajinomoto", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("Desi Ghee", "Kgs", 26.000, 0.000, 1.500, 504.00, 756.000, 24.500, 12348.00),
    ("Sarson", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("Clean Wrap", "Pkt", 0.000, 2.000, 2.000, 123.00, 246.000, 0.000, 0.00),
    ("Ajwain", "Pkt", 0.990, 0.000, 0.050, 252.00, 12.600, 0.940, 236.88),
    ("Mirchi (s)", "Kgs", 0.680, 0.000, 0.050, 315.00, 15.750, 0.630, 198.45),
    ("Chat Masala", "Kgs", 1.700, 0.000, 0.100, 752.00, 75.200, 1.600, 1203.20),
    ("Rajma Masala (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("Gulab Jal", "BTL", 6.000, 0.000, 0.000, 66.15, 0.000, 6.000, 396.91),
    ("Chana Masala", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("Kala Chana", "Kgs", 76.000, 0.000, 0.000, 78.00, 0.000, 76.000, 5928.00),
    ("Vinegar", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("Red Chilli Sauce", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("Matar Paneer Masala", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("Pav Bhaji Masala", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("Matar (TF)", "Kgs", 13.000, 0.000, 0.000, 60.00, 0.000, 13.000, 780.00),
    ("Star Phool Masala", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("Food Colour", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("Kewra Water", "BTL", 7.000, 0.000, 0.000, 70.80, 0.000, 7.000, 495.60),
    ("Biryani Masala", "Pkt", 10.000, 0.000, 0.000, 73.50, 0.000, 10.000, 735.00),
    ("Elaichi Small Gr", "Kgs", 0.100, 0.000, 0.000, 3150.00, 0.000, 0.100, 315.00),
    ("Dhaniya Powder", "Kgs", 5.300, 0.000, 0.300, 168.00, 50.400, 5.000, 840.00),
    ("Kali Mirch (s)", "Kgs", 0.410, 0.000, 0.010, 882.00, 8.820, 0.400, 352.80),
    ("Moongphali Dana", "Kgs", 19.000, 0.000, 0.000, 157.50, 0.000, 19.000, 2992.50),
    ("Sambhar Masala", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 24.200, 56.800, 36.800, 61.83, 2275.380, 44.200, 2732.93),
    ("Rai", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("Sugar", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("Baking Powder", "PKT", 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ("Shahi Paneer Masala (pkt)", "PKT", 6.000, 0.000, 0.000, 86.50, 0.000, 6.000, 519.00),
    ("Shahi Paneer Masala (kgs)", "kgs", 2.000, 0.000, 0.000, 880.00, 0.000, 2.000, 1760.00),
    ("Soya Bean Badiya", "kgs", 21.000, 0.000, 0.000, 94.50, 0.000, 21.000, 1984.50),
    ("Javitri", "Kgs", 0.620, 0.000, 0.010, 2730.00, 27.300, 0.610, 1665.30),
    ("Amchur Powder", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("Dal Makhani Masala", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("Black Pepper Powder", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Khus Khus", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("Aachar", "Kgs", 5.000, 0.000, 0.000, 147.00, 0.000, 5.000, 735.00),
    ("Cream", "Kgs", 7.000, 0.000, 0.000, 220.00, 0.000, 7.000, 1540.00),
    ("Gud", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2033, 2000, 536, 3.186, 1707.70, 3497, 11141.44),
    ("Foil Box (Rice, Sabji)", "Nos", 3244, 4000, 1072, 1.575, 1688.40, 6172, 9720.90),
    ("Roti pouch", "Nos", 8300, 19000, 3500, 0.236, 826.00, 23800, 5616.80),
    ("Salad Pkt", "Nos", 6074, 2000, 1072, 0.177, 189.74, 7002, 1239.35),
    ("Spoon/Mini Meal", "Nos", 1527, 2000, 595, 0.504, 299.88, 2932, 1477.73),
    ("Napkin Tissue Paper", "Nos", 5355, 3600, 609, 0.354, 215.59, 8346, 2954.48),
    ("Salt Pouch", "Nos", 580, 1000, 536, 0.150, 80.40, 1044, 156.60),
    ("Pickle & Paratha", "Nos", 4595, 0, 609, 0.899, 547.68, 3986, 3584.63),
    ("Tape", "Nos", 4, 8, 1, 23.600, 23.60, 11, 259.60),
    ("Big Foil Box (Biryani)", "Nos", 149, 300, 59, 3.150, 195.85, 390, 1228.50),
    ("Paper Box (Lunch)", "Nos", 7429, 0, 536, 4.956, 2656.42, 6893, 34161.71),
    ("Butter Roti Paper", "NOS", 0.300, 1.000, 0, 236.000, 11.80, 1.250, 295.00),
    ("Paratha Box", "Nos", 1461, 0, 73, 3.360, 245.28, 1388, 4663.68),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 5, 1, 141.600, 141.60, 5, 708.00),
    ("400 ML PP Box", "Nos", 277, 0, 0, 4.720, 0.00, 277, 1307.44),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 9.500, 21.000, 0.000, 280.000, 0.000, 30.500, 8540.00),
    ("Petha", "KGS", 8.000, 35.000, 18.000, 150.000, 2700.000, 25.000, 3750.00),
    ("Guldana", "KGS", 0.000, 10.000, 0.000, 250.000, 0.000, 10.000, 2500.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 30.000, 0.000, 0.000, 12.000, 0.000, 30.000, 360.00),
    ("Onion", "Kgs", 136.000, 0.000, 12.000, 23.000, 276.000, 124.000, 2852.00),
    ("Tomato", "Kgs", 60.000, 0.000, 12.000, 18.000, 216.000, 48.000, 864.00),
    ("Ginger", "Kgs", 3.000, 0.000, 1.000, 80.000, 80.000, 2.000, 160.00),
    ("Garlic", "Kgs", 0.000, 2.000, 1.000, 132.000, 132.000, 1.000, 132.00),
    ("Peas green", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 3.000, 0.000, 1.500, 60.000, 90.000, 1.500, 90.00),
    ("Coriander", "Kgs", 1.000, 0.000, 1.000, 40.000, 40.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 15.000, 0.000, 0.000, 31.000, 0.000, 15.000, 465.00),
    ("Beans", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 90.000, 0.000, 90.000, 22.000, 1980.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 120.000, 0.000, 18.000, 20.000, 360.000, 102.000, 2040.00),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 536, 535, 70.0, 37450, 25145.0),
    ("Paratha", 71, 70, 40.0, 2800, 1344.0),
    ("Dahi", 260, 259, 10.0, 2590, 2331.0),
    ("Chach", 200, 195, 10.0, 1950, 1755.0),
    ("MINI", 60, 59, 50.0, 2950, 866.0),
    ("Amul Kool", 2, 2, 25.0, 50, 44.0),
    ("Lahori Zeera", 13, 13, 10.0, 130, 117.0),
    ("Lassi", 10, 10, 20.0, 200, 190.0),
    ("Brownie", 1, 1, 40.0, 40, 40.0),
    ("Plum Cake", 1, 1, 20.0, 20, 20.0),
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
        # Flat list: (meal_name, qty, notes, given_to)
        # CHACH has 2 rows: 1 General sample + 5 Ladies
        samples_list = [
            ("LUNCH",    1, "01 X LUNCH SAMPLE",      "General"),
            ("Paratha",  1, "01 X PARATHA SAMPLE",    "General"),
            ("MINI",     1, "01 X MINI LUNCH SAMPLE", "General"),
            ("Dahi",     1, "01 X DAHI SAMPLE",       "General"),
            ("Chach",    1, "01 X CHACH SAMPLE",      "General"),
            ("Chach", 5, "05 X CHACH FOR LADIES", "Staff"),
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
        print("🎉 Database successfully updated for 04 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
