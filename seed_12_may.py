import sqlite3

DATE = "2026-05-12"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Atta", "Kgs", 879.000, 0.000, 66.000, 31.00, 2046.000, 813.000, 25203.00),
    ("Rice", "Kgs", 583.000, 0.000, 46.000, 65.00, 2990.000, 537.000, 34905.00),
    ("R/oil", "Ltr", 193.000, 0.000, 12.000, 180.92, 2171.077, 181.000, 32747.08),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.150, 105.00, 15.750, 0.350, 36.75),
    ("Rajma", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("Urad (s)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Dal Chana", "Kgs", 35.000, 0.000, 0.000, 78.00, 0.000, 35.000, 2730.00),
    ("Besan", "Kgs", 51.000, 0.000, 12.000, 94.50, 1134.000, 39.000, 3685.50),
    ("Dal Arhar", "Kgs", 44.000, 0.000, 0.000, 120.00, 0.000, 44.000, 5280.00),
    ("Dal masoor (s)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("Urad Dal Chilka", "KGS", 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ("Masoor Dal (Malika)", "Kgs", 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ("Moong Dal Chilka", "Kgs", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("Urad Dhuli", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("Lobia", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("Jeera (s)", "Kgs", 0.350, 0.000, 0.050, 315.00, 15.750, 0.300, 94.50),
    ("Haldi Powder", "Kgs", 2.900, 0.000, 0.200, 231.00, 46.200, 2.700, 623.70),
    ("Mirchi Powder", "Kgs", 3.000, 0.000, 0.200, 315.00, 63.000, 2.800, 882.00),
    ("Dal chini", "Kgs", 0.370, 0.000, 0.010, 357.00, 3.570, 0.360, 128.52),
    ("Laung", "Kgs", 0.240, 0.000, 0.010, 1155.00, 11.550, 0.230, 265.65),
    ("Hing", "Nos", 20.000, 0.000, 4.000, 89.25, 357.000, 16.000, 1428.00),
    ("Kitchen King", "Kgs", 1.500, 0.000, 0.200, 800.00, 160.000, 1.300, 1040.00),
    ("Degi Mirch", "Kgs", 1.600, 0.000, 0.200, 960.00, 192.000, 1.400, 1344.00),
    ("Kasuri Methi", "Kgs", 0.550, 0.000, 0.050, 336.00, 16.800, 0.500, 168.00),
    ("Garam Masala", "Kgs", 1.300, 0.000, 0.200, 920.00, 184.000, 1.100, 1012.00),
    ("Salt", "Kgs", 37.000, 0.000, 4.000, 28.00, 112.000, 33.000, 924.00),
    ("Dhaniya (s)", "Kgs", 1.100, 0.000, 0.100, 157.50, 15.750, 1.000, 157.50),
    ("Jeera Powder", "Kgs", 0.600, 0.000, 0.100, 420.00, 42.000, 0.500, 210.00),
    ("Chana Masala (pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("Badi Elaichi", "Kgs", 0.240, 0.000, 0.010, 1995.00, 19.950, 0.230, 458.85),
    ("Methi Dana", "Kgs", 0.210, 0.000, 0.100, 105.00, 10.500, 0.110, 11.55),
    ("Rajma Masala", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("Tej Patta", "Kgs", 0.440, 0.000, 0.010, 168.00, 1.680, 0.430, 72.24),
    ("Ajinomoto", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("Desi Ghee", "Kgs", 18.000, 0.000, 1.000, 504.00, 504.000, 17.000, 8568.00),
    ("Sarson", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("Clean Wrap", "Pkt", 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ("Ajwain", "Pkt", 0.700, 0.000, 0.100, 252.00, 25.200, 0.600, 151.20),
    ("Mirchi (s)", "Kgs", 0.300, 0.000, 0.050, 315.00, 15.750, 0.250, 78.75),
    ("Chat Masala", "Kgs", 1.100, 0.000, 0.100, 752.00, 75.200, 1.000, 752.00),
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
    ("Elaichi Small Gr", "Kgs", 0.070, 0.000, 0.010, 3150.00, 31.500, 0.070, 220.50),
    ("Dhaniya Powder", "Kgs", 3.600, 0.000, 0.200, 168.00, 33.600, 3.400, 571.20),
    ("Kali Mirch (s)", "Kgs", 0.340, 0.000, 0.010, 882.00, 8.820, 0.330, 291.06),
    ("Moongphali Dana", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("Sambhar Masala", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 82.400, 0.000, 9.800, 61.83, 605.944, 72.600, 4488.93),
    ("Rai", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("Sugar", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("Baking Powder", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("Shahi Paneer Masala (pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("Shahi Paneer Masala (kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("Soya Bean Badiya", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("Javitri", "Kgs", 0.540, 0.000, 0.010, 2730.00, 27.300, 0.530, 1446.90),
    ("Amchur Powder", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("Dal Makhani Masala", "Pkt", 5.000, 0.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("Black Pepper Powder", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("Sabji Masala", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("Aachar", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("Cream", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("Paratha Masala", "Kgs", 0.000, 5.000, 5.000, 10.00, 10.000, 0.000, 0.00),
    ("Khus Khus", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("Gud", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 3800, 0, 521, 3.186, 1659.91, 3279, 10446.89),
    ("Foil Box (Rice, Sabji)", "Nos", 6898, 0, 1042, 1.575, 1641.15, 5856, 9223.20),
    ("Roti pouch", "Nos", 24900, 0, 2800, 0.236, 660.80, 22100, 5215.60),
    ("Salad Pkt", "Nos", 7728, 0, 1042, 0.177, 184.43, 6686, 1183.42),
    ("Spoon/Mini Meal", "Nos", 3051, 0, 581, 0.504, 292.82, 2470, 1244.88),
    ("Napkin Tissue Paper", "Nos", 9034, 0, 591, 0.354, 209.21, 8443, 2988.82),
    ("Salt Pouch", "Nos", 2907, 0, 521, 0.150, 78.15, 2386, 357.90),
    ("Pickle & Paratha", "Nos", 5035, 0, 591, 0.896, 529.54, 4444, 3981.08),
    ("Tape", "Nos", 9, 0, 2, 23.600, 47.20, 7, 165.20),
    ("Big Foil Box (Biryani)", "Nos", 307, 0, 60, 3.150, 189.00, 247, 778.05),
    ("Paper Box (Lunch)", "Nos", 4256, 0, 521, 4.956, 2582.08, 3735, 18510.66),
    ("Butter Roti Paper", "NOS", 1.800, 0, 0.050, 236.000, 11.80, 1.750, 413.00),
    ("Paratha Box", "Nos", 1042, 0, 70, 3.360, 235.20, 972, 3265.92),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 5, 0, 1, 141.600, 141.60, 4, 566.40),
    ("400 ML PP Box", "Nos", 287, 0, 60, 4.720, 283.20, 227, 1071.44),
    ("Silver foil", "Kgs", 4, 0, 0, 708.000, 0.00, 4, 2832.00),
    ("Foil silver", "Kgs", 1, 0, 1, 531.000, 531.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 14.000, 0, 0.000, 280.00, 0.00, 14.000, 3920.00),
    ("Petha", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("Guldana", "KGS", 14.000, 0, 14.000, 250.00, 3500.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 45.000, 0.000, 15.000, 10.000, 150.000, 30.000, 300.00),
    ("Onion", "Kgs", 108.000, 0.000, 12.000, 22.000, 264.000, 96.000, 2112.00),
    ("Tomato", "Kgs", 53.000, 0.000, 12.000, 16.000, 192.000, 41.000, 656.00),
    ("Ginger", "Kgs", 9.000, 0.000, 2.000, 135.000, 270.000, 7.000, 945.00),
    ("Garlic", "Kgs", 3.480, 0.000, 1.000, 143.000, 143.000, 2.480, 354.64),
    ("Peas green", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("Pumpkin", "Kgs", 100.000, 0.000, 100.000, 15.000, 1500.000, 0.000, 0.00),
    ("Green chilli", "Kgs", 9.020, 0.000, 3.000, 60.000, 180.000, 6.020, 361.20),
    ("Coriander", "Kgs", 2.000, 0.000, 2.000, 20.000, 40.000, 0.000, 0.00),
    ("Capsicum", "Kgs", 12.000, 0.000, 0.000, 22.000, 0.000, 12.000, 264.00),
    ("Beans", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("Cucumber", "Kgs", 88.000, 0.000, 21.000, 20.000, 420.000, 67.000, 1340.00),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("Lime S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("Pav/Kulcha", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 521, 519, 70.0, 36330, 25044.0),
    ("Paratha", 71, 70, 40.0, 2800, 1837.0),
    ("Dahi", 240, 239, 10.0, 2390, 2151.0),
    ("Chach", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 60, 59, 50.0, 2950, 1152.0),
    ("Amul Kool", 1, 1, 25.0, 25, 22.0),
    ("Lahori Zeera", 15, 15, 10.0, 150, 135.0),
    ("Lassi", 17, 17, 20.0, 340, 323.0),
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
        print("🎉 Database successfully updated for 12 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
