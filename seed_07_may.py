import sqlite3

DATE = "2026-05-07"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Atta", "Kgs", 1097.000, 0.000, 66.000, 31.00, 2046.000, 1031.000, 31961.00),
    ("Rice", "Kgs", 729.000, 0.000, 47.000, 65.00, 3055.000, 682.000, 44330.00),
    ("R/oil", "Ltr", 227.000, 0.000, 12.000, 180.92, 2171.077, 215.000, 38898.46),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("Rajma", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("Urad (s)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Dal Chana", "Kgs", 55.000, 0.000, 0.000, 78.00, 0.000, 55.000, 4290.00),
    ("Besan", "Kgs", 54.000, 0.000, 2.000, 94.50, 189.000, 52.000, 4914.00),
    ("Dal Arhar", "Kgs", 55.000, 0.000, 0.000, 120.00, 0.000, 55.000, 6600.00),
    ("Dal masoor (s)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("Urad Dal Chilka", "KGS", 9.000, 0.000, 0.000, 110.00, 0.000, 9.000, 990.00),
    ("Masoor Dal (Malika)", "Kgs", 9.000, 0.000, 0.000, 85.00, 0.000, 9.000, 765.00),
    ("Moong Dal Chilka", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ("Urad Dhuli", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("Lobia", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("Jeera (s)", "Kgs", 1.000, 0.000, 0.200, 315.00, 63.000, 0.800, 252.00),
    ("Haldi Powder", "Kgs", 3.800, 0.000, 0.300, 231.00, 69.300, 3.500, 808.50),
    ("Mirchi Powder", "Kgs", 3.900, 0.000, 0.300, 315.00, 94.500, 3.600, 1134.00),
    ("Dal chini", "Kgs", 0.410, 0.000, 0.010, 357.00, 3.570, 0.400, 142.80),
    ("Laung", "Kgs", 0.280, 0.000, 0.010, 1155.00, 11.550, 0.270, 311.85),
    ("Hing", "Nos", 21.000, 0.000, 1.000, 89.25, 89.250, 20.000, 1785.00),
    ("Kitchen King", "Kgs", 2.200, 0.000, 0.200, 800.00, 160.000, 2.000, 1600.00),
    ("Degi Mirch", "Kgs", 2.300, 0.000, 0.200, 960.00, 192.000, 2.100, 2016.00),
    ("Kasuri Methi", "Kgs", 0.700, 0.000, 0.050, 336.00, 16.800, 0.650, 218.40),
    ("Garam Masala", "Kgs", 2.100, 0.000, 0.300, 920.00, 276.000, 1.800, 1656.00),
    ("Salt", "Kgs", 51.000, 0.000, 4.000, 28.00, 112.000, 47.000, 1316.00),
    ("Dhaniya (s)", "Kgs", 1.300, 0.000, 0.050, 157.50, 7.875, 1.250, 196.88),
    ("Jeera Powder", "Kgs", 1.400, 0.000, 0.400, 420.00, 168.000, 1.000, 420.00),
    ("Chana Masala (pkt)", "Pkt", 1.000, 0.000, 0.200, 736.01, 147.203, 0.800, 588.81),
    ("Badi Elaichi", "Kgs", 0.280, 0.000, 0.010, 1995.00, 19.950, 0.270, 538.65),
    ("Methi Dana", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("Rajma Masala", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("Tej Patta", "Kgs", 0.480, 0.000, 0.010, 168.00, 1.680, 0.470, 78.96),
    ("Ajinomoto", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("Desi Ghee", "Kgs", 22.000, 0.000, 1.000, 504.00, 504.000, 21.000, 10584.00),
    ("Sarson", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("Clean Wrap", "Pkt", 0.750, 0.000, 0.750, 450.00, 337.500, 0.000, 0.00),
    ("Ajwain", "Pkt", 0.850, 0.000, 0.050, 252.00, 12.600, 0.800, 201.60),
    ("Mirchi (s)", "Kgs", 0.450, 0.000, 0.050, 315.00, 15.750, 0.400, 126.00),
    ("Chat Masala", "Kgs", 1.400, 0.000, 0.100, 752.00, 75.200, 1.300, 977.60),
    ("Rajma Masala (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("Gulab Jal", "BTL", 6.000, 0.000, 1.000, 66.15, 66.152, 5.000, 330.76),
    ("Chana Masala", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("Kala Chana", "Kgs", 76.000, 0.000, 18.000, 78.00, 1404.000, 58.000, 4524.00),
    ("Vinegar", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("Red Chilli Sauce", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("Matar Paneer Masala", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("Pav Bhaji Masala", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("Matar (TF)", "Kgs", 13.000, 0.000, 0.000, 60.00, 0.000, 13.000, 780.00),
    ("Star Phool Masala", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("Food Colour", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("Kewra Water", "BTL", 7.000, 0.000, 1.000, 70.80, 70.800, 6.000, 424.80),
    ("Biryani Masala", "Pkt", 10.000, 0.000, 3.000, 73.50, 220.500, 7.000, 514.50),
    ("Elaichi Small Gr", "Kgs", 0.100, 0.000, 0.020, 3150.00, 63.000, 0.080, 252.00),
    ("Dhaniya Powder", "Kgs", 4.500, 0.000, 0.300, 168.00, 50.400, 4.200, 705.60),
    ("Kali Mirch (s)", "Kgs", 0.380, 0.000, 0.010, 882.00, 8.820, 0.370, 326.34),
    ("Moongphali Dana", "Kgs", 17.000, 0.000, 0.000, 157.50, 0.000, 17.000, 2677.50),
    ("Sambhar Masala", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 44.000, 0.000, 28.600, 61.83, 1768.338, 15.400, 952.20),
    ("Rai", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("Sugar", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("Baking Powder", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("Shahi Paneer Masala (pkt)", "PKT", 2.000, 0.000, 2.000, 86.50, 173.000, 0.000, 0.00),
    ("Shahi Paneer Masala (kgs)", "kgs", 2.000, 0.000, 0.200, 880.00, 176.000, 1.800, 1584.00),
    ("Soya Bean Badiya", "kgs", 21.000, 0.000, 12.000, 94.50, 1134.000, 9.000, 850.50),
    ("Javitri", "Kgs", 0.580, 0.000, 0.010, 2730.00, 27.300, 0.570, 1556.10),
    ("Amchur Powder", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("Dal Makhani Masala", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("Black Pepper Powder", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Khus Khus", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("Aachar", "Kgs", 5.000, 0.000, 1.000, 147.00, 147.000, 4.000, 588.00),
    ("Cream", "Kgs", 6.500, 0.000, 0.000, 220.00, 0.000, 6.500, 1430.00),
    ("Gud", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2585, 0, 523, 3.186, 1666.28, 2062, 6569.53),
    ("Foil Box (Rice, Sabji)", "Nos", 4348, 0, 1046, 1.575, 1647.45, 3302, 5200.65),
    ("Roti pouch", "Nos", 18200, 0, 2800, 0.236, 660.80, 15400, 3634.40),
    ("Salad Pkt", "Nos", 5178, 0, 1046, 0.177, 185.14, 4132, 731.36),
    ("Spoon/Mini Meal", "Nos", 1898, 0, 584, 0.504, 294.34, 1314, 662.26),
    ("Napkin Tissue Paper", "Nos", 7361, 0, 594, 0.354, 210.28, 6767, 2395.52),
    ("Salt Pouch", "Nos", 132, 1500, 523, 0.150, 78.45, 1109, 166.35),
    ("Pickle & Paratha", "Nos", 2930, 0, 594, 0.899, 534.19, 2336, 2100.78),
    ("Tape", "Nos", 7, 0, 2, 23.600, 47.20, 5, 118.00),
    ("Big Foil Box (Biryani)", "Nos", 268, 0, 61, 3.150, 192.15, 207, 652.05),
    ("Paper Box (Lunch)", "Nos", 5981, 0, 523, 4.956, 2591.99, 5458, 27049.85),
    ("Butter Roti Paper", "NOS", 1.150, 0, 0.050, 236.000, 11.80, 1.100, 259.60),
    ("Paratha Box", "Nos", 1244, 0, 71, 3.360, 238.56, 1173, 3941.28),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 2, 0, 1, 141.600, 141.60, 1, 141.60),
    ("400 ML PP Box", "Nos", 155, 0, 0, 4.720, 0.00, 155, 731.60),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 16.500, 0, 0.000, 280.00, 0.00, 16.500, 4620.00),
    ("Petha", "KGS", 25.000, 0, 15.000, 150.00, 2250.00, 10.000, 1500.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 0.000, 50.000, 15.000, 10.000, 150.000, 35.000, 350.00),
    ("Onion", "Kgs", 98.000, 0.000, 14.000, 23.000, 322.000, 84.000, 1932.00),
    ("Tomato", "Kgs", 24.000, 0.000, 10.000, 18.000, 180.000, 14.000, 252.00),
    ("Ginger", "Kgs", 0.000, 3.000, 1.000, 135.000, 135.000, 2.000, 270.00),
    ("Garlic", "Kgs", 3.055, 0.000, 1.500, 132.000, 198.000, 1.555, 205.26),
    ("Peas green", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 1.000, 0.000, 1.000, 55.000, 55.000, 0.000, 0.00),
    ("Coriander", "Kgs", 0.000, 0.000, 0.000, 40.000, 0.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 15.000, 0.000, 15.000, 31.000, 465.000, 0.000, 0.00),
    ("Beans", "Kgs", 14.975, 0.000, 14.975, 59.000, 883.525, 0.000, 0.00),
    ("Carrot", "Kgs", 25.140, 0.000, 25.140, 33.000, 829.620, 0.000, 0.00),
    ("Cauli flower", "Kgs", 35.360, 0.000, 35.360, 55.000, 1944.800, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0.000, 0.000, 22.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 69.000, 0.000, 21.000, 20.000, 420.000, 48.000, 960.00),
    ("Matar", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 523, 520, 70.0, 36400, 28924.0),
    ("Paratha", 71, 70, 40.0, 2800, 2180.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 195, 10.0, 1950, 1755.0),
    ("MINI", 61, 59, 50.0, 2950, 1377.0),
    ("Amul Kool", 2, 2, 25.0, 50, 44.0),
    ("Lahori Zeera", 10, 10, 10.0, 100, 90.0),
    ("Lassi", 8, 8, 20.0, 160, 152.0),
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
        print("🎉 Database successfully updated for 07 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
