import sqlite3

DATE = "2026-05-08"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Atta", "Kgs", 1031.000, 0.000, 66.000, 31.00, 2046.000, 965.000, 29915.00),
    ("Rice", "Kgs", 682.000, 0.000, 40.000, 65.00, 2600.000, 642.000, 41730.00),
    ("R/oil", "Ltr", 215.000, 0.000, 8.000, 180.92, 1447.385, 207.000, 37451.08),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("Rajma", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("Urad (s)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Dal Chana", "Kgs", 55.000, 0.000, 12.000, 78.00, 936.000, 43.000, 3354.00),
    ("Besan", "Kgs", 52.000, 0.000, 1.000, 94.50, 94.500, 51.000, 4819.50),
    ("Dal Arhar", "Kgs", 55.000, 0.000, 8.000, 120.00, 960.000, 47.000, 5640.00),
    ("Dal masoor (s)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("Urad Dal Chilka", "KGS", 9.000, 0.000, 0.000, 110.00, 0.000, 9.000, 990.00),
    ("Masoor Dal (Malika)", "Kgs", 9.000, 0.000, 0.000, 85.00, 0.000, 9.000, 765.00),
    ("Moong Dal Chilka", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ("Urad Dhuli", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("Lobia", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("Jeera (s)", "Kgs", 0.800, 0.000, 0.300, 315.00, 94.500, 0.500, 157.50),
    ("Haldi Powder", "Kgs", 3.500, 0.000, 0.300, 231.00, 69.300, 3.200, 739.20),
    ("Mirchi Powder", "Kgs", 3.600, 0.000, 0.300, 315.00, 94.500, 3.300, 1039.50),
    ("Dal chini", "Kgs", 0.400, 0.000, 0.010, 357.00, 3.570, 0.390, 139.23),
    ("Laung", "Kgs", 0.270, 0.000, 0.010, 1155.00, 11.550, 0.260, 300.30),
    ("Hing", "Nos", 20.000, 0.000, 0.000, 89.25, 0.000, 20.000, 1785.00),
    ("Kitchen King", "Kgs", 2.000, 0.000, 0.200, 800.00, 160.000, 1.800, 1440.00),
    ("Degi Mirch", "Kgs", 2.100, 0.000, 0.200, 960.00, 192.000, 1.900, 1824.00),
    ("Kasuri Methi", "Kgs", 0.650, 0.000, 0.050, 336.00, 16.800, 0.600, 201.60),
    ("Garam Masala", "Kgs", 1.800, 0.000, 0.200, 920.00, 184.000, 1.600, 1472.00),
    ("Salt", "Kgs", 47.000, 0.000, 4.000, 28.00, 112.000, 43.000, 1204.00),
    ("Dhaniya (s)", "Kgs", 1.250, 0.000, 0.050, 157.50, 7.875, 1.200, 189.00),
    ("Jeera Powder", "Kgs", 1.000, 0.000, 0.200, 420.00, 84.000, 0.800, 336.00),
    ("Chana Masala (pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("Badi Elaichi", "Kgs", 0.270, 0.000, 0.010, 1995.00, 19.950, 0.260, 518.70),
    ("Methi Dana", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("Rajma Masala", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("Tej Patta", "Kgs", 0.470, 0.000, 0.010, 168.00, 1.680, 0.460, 77.28),
    ("Ajinomoto", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("Desi Ghee", "Kgs", 21.000, 0.000, 1.000, 504.00, 504.000, 20.000, 10080.00),
    ("Sarson", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("Clean Wrap", "Pkt", 0.000, 1.000, 0.250, 600.00, 150.000, 0.750, 450.00),
    ("Ajwain", "Pkt", 0.800, 0.000, 0.050, 252.00, 12.600, 0.750, 189.00),
    ("Mirchi (s)", "Kgs", 0.400, 0.000, 0.050, 315.00, 15.750, 0.350, 110.25),
    ("Chat Masala", "Kgs", 1.300, 0.000, 0.100, 752.00, 75.200, 1.200, 902.40),
    ("Rajma Masala (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("Gulab Jal", "BTL", 5.000, 0.000, 0.000, 66.15, 0.000, 5.000, 330.76),
    ("Chana Masala", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("Kala Chana", "Kgs", 58.000, 0.000, 0.000, 78.00, 0.000, 58.000, 4524.00),
    ("Vinegar", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("Red Chilli Sauce", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("Matar Paneer Masala", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("Pav Bhaji Masala", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("Matar (TF)", "Kgs", 13.000, 0.000, 4.000, 60.00, 240.000, 9.000, 540.00),
    ("Star Phool Masala", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("Food Colour", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("Kewra Water", "BTL", 6.000, 0.000, 0.000, 70.80, 0.000, 6.000, 424.80),
    ("Biryani Masala", "Pkt", 7.000, 0.000, 0.000, 73.50, 0.000, 7.000, 514.50),
    ("Elaichi Small Gr", "Kgs", 0.080, 0.000, 0.000, 3150.00, 0.000, 0.080, 252.00),
    ("Dhaniya Powder", "Kgs", 4.200, 0.000, 0.300, 168.00, 50.400, 3.900, 655.20),
    ("Kali Mirch (s)", "Kgs", 0.370, 0.000, 0.010, 882.00, 8.820, 0.360, 317.52),
    ("Moongphali Dana", "Kgs", 17.000, 0.000, 4.000, 157.50, 630.000, 13.000, 2047.50),
    ("Sambhar Masala", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 15.400, 28.400, 32.400, 61.83, 2003.324, 11.400, 704.87),
    ("Rai", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("Sugar", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("Baking Powder", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("Shahi Paneer Masala (pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("Shahi Paneer Masala (kgs)", "kgs", 1.800, 0.000, 0.400, 880.00, 352.000, 1.400, 1232.00),
    ("Soya Bean Badiya", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("Javitri", "Kgs", 0.570, 0.000, 0.010, 2730.00, 27.300, 0.560, 1528.80),
    ("Amchur Powder", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("Dal Makhani Masala", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("Black Pepper Powder", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Khus Khus", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("Aachar", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("Cream", "Kgs", 6.500, 0.000, 1.000, 220.00, 220.000, 5.500, 1210.00),
    ("Gud", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2062, 0, 600, 3.186, 1911.60, 1462, 4657.93),
    ("Foil Box (Rice, Sabji)", "Nos", 3302, 0, 1080, 1.575, 1701.00, 2222, 3499.65),
    ("Roti pouch", "Nos", 15400, 0, 2800, 0.236, 660.80, 12600, 2973.60),
    ("Salad Pkt", "Nos", 4132, 0, 1080, 0.177, 191.16, 3052, 540.20),
    ("Spoon/Mini Meal", "Nos", 1314, 0, 540, 0.504, 272.16, 774, 390.10),
    ("Napkin Tissue Paper", "Nos", 6767, 0, 610, 0.354, 215.94, 6157, 2179.58),
    ("Salt Pouch", "Nos", 1109, 0, 540, 0.150, 81.00, 569, 85.35),
    ("Pickle & Paratha", "Nos", 2336, 0, 610, 0.899, 548.38, 1726, 1552.20),
    ("Tape", "Nos", 5, 0, 2, 23.600, 47.20, 3, 70.80),
    ("Big Foil Box (Biryani)", "Nos", 207, 0, 60, 3.150, 189.00, 147, 463.05),
    ("Paper Box (Lunch)", "Nos", 5458, 0, 540, 4.956, 2676.24, 4918, 24373.61),
    ("Butter Roti Paper", "NOS", 1.100, 0, 0.050, 236.000, 11.80, 1.050, 247.80),
    ("Paratha Box", "Nos", 1173, 0, 70, 3.360, 235.20, 1103, 3706.08),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 0, 0, 141.600, 0.00, 1, 141.60),
    ("400 ML PP Box", "Nos", 155, 0, 0, 4.720, 0.00, 155, 731.60),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 16.500, 0, 12.000, 280.00, 3360.00, 4.500, 1260.00),
    ("Petha", "KGS", 10.000, 0, 0.000, 150.00, 0.00, 10.000, 1500.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 35.000, 0.000, 16.000, 10.000, 160.000, 19.000, 190.00),
    ("Onion", "Kgs", 84.000, 0.000, 12.000, 23.000, 276.000, 72.000, 1656.00),
    ("Tomato", "Kgs", 14.000, 0.000, 12.000, 18.000, 216.000, 2.000, 36.00),
    ("Ginger", "Kgs", 2.000, 0.000, 1.300, 135.000, 175.500, 0.700, 94.50),
    ("Garlic", "Kgs", 1.555, 0.000, 1.000, 132.000, 132.000, 0.555, 73.26),
    ("Peas green", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 0.000, 3.020, 2.000, 60.000, 120.000, 1.020, 61.20),
    ("Coriander", "Kgs", 0.000, 0.000, 0.000, 40.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 0.000, 0.000, 0.000, 31.000, 0.000, 0.000, 0.00),
    ("Beans", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0.000, 0.000, 22.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 48.000, 0.000, 21.000, 20.000, 420.000, 27.000, 540.00),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 16.000, 16.000, 250.000, 4000.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 30.000, 30.000, 30.000, 900.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 540, 537, 70.0, 37590, 28591.0),
    ("Paratha", 70, 68, 40.0, 2720, 1803.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 195, 10.0, 1950, 1755.0),
    ("MINI", 60, 60, 50.0, 3000, 1532.0),
    ("Amul Kool", 7, 7, 25.0, 175, 154.0),
    ("Lahori Zeera", 10, 10, 10.0, 100, 90.0),
    ("Lassi", 10, 10, 20.0, 200, 190.0),
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
            ("Paratha",  2, "02 X PARATHA SAMPLE",    "General"),
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
        print("🎉 Database successfully updated for 08 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
