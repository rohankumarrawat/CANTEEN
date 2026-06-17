import sqlite3

DATE = "2026-05-29"

dry_items = [
    ('Aachar', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('Ajinomoto', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.800, 0.000, 0.050, 252.00, 12.600, 0.750, 189.00),
    ('Amchur Powder', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Atta', 'Kgs', 1362.000, 0.000, 66.000, 31.00, 2046.000, 1296.000, 40176.00),
    ('Badi Elaichi', 'Kgs', 0.220, 0.000, 0.010, 1995.00, 19.950, 0.210, 418.95),
    ('Baking Powder', 'PKT', 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ('Besan', 'Kgs', 67.000, 0.000, 0.000, 94.50, 0.000, 67.000, 6331.50),
    ('Biryani Masala', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Chana Masala', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('Chana Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('Chana Masala (pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 1.900, 0.000, 0.100, 752.00, 75.200, 1.800, 1353.60),
    ('Chat Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Cream', 'Kgs', 5.500, 0.000, 1.000, 220.00, 220.000, 4.500, 990.00),
    ('Dal Arhar', 'Kgs', 79.000, 0.000, 8.000, 120.00, 960.000, 71.000, 8520.00),
    ('Dal Chana', 'Kgs', 90.000, 0.000, 12.000, 80.00, 960.000, 78.000, 6240.00),
    ('Dal chini', 'Kgs', 0.060, 0.000, 0.010, 357.00, 3.570, 0.050, 17.85),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('Dal masoor (s)', 'Pkt', 23.000, 0.000, 0.000, 85.00, 0.000, 23.000, 1955.00),
    ('Dhaniya (s)', 'Kgs', 1.760, 0.000, 0.100, 199.50, 19.950, 1.660, 331.18),
    ('Degi Mirch', 'Kgs', 4.300, 0.000, 0.200, 959.99, 191.999, 4.100, 3935.97),
    ('Desi Ghee', 'Kgs', 30.000, 0.000, 1.500, 504.00, 756.000, 28.500, 14364.00),
    ('Dhaniya Powder', 'Kgs', 6.600, 0.000, 0.300, 199.50, 59.850, 6.300, 1256.85),
    ('Imli', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('Imli (expensive)', 'Pkt', 3.750, 0.000, 0.050, 120.00, 6.000, 3.700, 444.00),
    ('Eno', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('Garam Masala', 'Kgs', 2.300, 0.000, 0.300, 920.00, 275.995, 2.000, 1839.99),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('Gulab Jal', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('Haldi Powder', 'Kgs', 8.300, 0.000, 0.300, 231.00, 69.300, 8.000, 1848.00),
    ('Hing', 'Nos', 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', 0.090, 0.000, 0.020, 2730.00, 54.600, 0.070, 191.10),
    ('Jeera (s)', 'Kgs', 2.240, 0.000, 0.100, 315.00, 31.500, 2.140, 674.10),
    ('Jeera Powder', 'Kgs', 2.500, 0.000, 0.200, 420.00, 84.000, 2.300, 966.00),
    ('Kala Chana', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('Kali Mirch (s)', 'Kgs', 0.404, 0.000, 0.020, 882.00, 17.640, 0.384, 338.69),
    ('Kasuri Methi', 'Kgs', 0.900, 0.000, 0.050, 336.00, 16.800, 0.850, 285.60),
    ('Kewra Water', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Kitchen King', 'Kgs', 4.400, 0.000, 0.200, 800.00, 160.001, 4.200, 3360.03),
    ('Laung', 'Kgs', 0.220, 0.000, 0.010, 1155.00, 11.550, 0.210, 242.55),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 51.700, 0.000, 25.000, 61.83, 1545.775, 26.700, 1650.89),
    ('Masoor Dal (Malika)', 'Kgs', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 16.000, 0.000, 4.000, 60.00, 240.000, 12.000, 720.00),
    ('Methi Dana', 'Kgs', 0.350, 0.000, 0.010, 105.00, 1.050, 0.340, 35.70),
    ('Mirchi (s)', 'Kgs', 0.800, 0.000, 0.050, 367.50, 18.375, 0.750, 275.63),
    ('Mirchi Powder', 'Kgs', 6.800, 0.000, 0.300, 315.00, 94.500, 6.500, 2047.50),
    ('Moong Dal Chilka', 'Kgs', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('Moongphali Dana', 'Kgs', 17.000, 0.000, 4.000, 168.00, 672.000, 13.000, 2184.00),
    ('Paratha Masala', 'Kgs', 11.000, 0.000, 0.000, 10.00, 0.000, 11.000, 110.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/oil', 'Ltr', 321.000, 0.000, 9.000, 180.92, 1628.308, 312.000, 56448.00),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Rajma', 'Kgs', 96.000, 0.000, 0.000, 115.00, 0.000, 96.000, 11040.00),
    ('Rajma Masala (Kgs)', 'Kgs', 1.900, 0.000, 0.000, 736.25, 0.000, 1.900, 1398.88),
    ('Red Chilli Sauce', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('Rice', 'Kgs', 920.000, 0.000, 38.000, 68.00, 2584.000, 882.000, 59976.00),
    ('Rice (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Sabudana', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 1.400, 0.000, 0.400, 880.00, 352.000, 1.000, 880.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Salt', 'Kgs', 39.000, 0.000, 4.000, 28.00, 112.000, 35.000, 980.00),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.150, 105.00, 15.750, 0.200, 21.00),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Soya Bean Badiya', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.640, 0.000, 0.010, 168.00, 1.680, 0.630, 105.84),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Urad Dal Chilka', 'KGS', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Vinegar', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2756, 0, 540, 3.186, 1720.44, 2216, 7060.18),
    ("Foil Box (Rice, Sabji)", "Nos", 3014, 0, 1080, 1.575, 1701.00, 1934, 3046.05),
    ("Roti pouch", "Nos", 5400, 0, 2900, 0.236, 684.40, 2500, 590.00),
    ("Salad Pkt", "Nos", 5868, 0, 540, 0.177, 95.58, 5328, 943.06),
    ("Spoon/Mini Meal", "Nos", 2969, 0, 600, 0.504, 302.40, 2369, 1193.98),
    ("Napkin Tissue Paper", "Nos", 7909, 0, 613, 0.354, 217.00, 7296, 2582.78),
    ("Salt Pouch", "Nos", 2977, 0, 540, 0.150, 81.00, 2437, 365.55),
    ("Pickle & Paratha", "Nos", 3816, 0, 613, 0.896, 549.15, 3203, 2869.35),
    ("Tape", "Nos", 4, 0, 2, 23.60, 47.20, 2, 47.20),
    ("Big Foil Box (Biryani)", "Nos", 159, 0, 60, 3.15, 189.00, 99, 311.85),
    ("Paper Box (Lunch)", "Nos", 5126, 0, 540, 4.956, 2676.24, 4586, 22728.22),
    ("Butter Roti Paper", "Nos", 550, 0, 250, 0.236, 59.00, 300, 70.80),
    ("Paratha Box", "Nos", 205, 0, 73, 3.36, 245.28, 132, 443.52),
    ("Partition Box", "Nos", 47, 0, 0, 6.96, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 3, 0, 2, 141.60, 283.20, 1, 141.60),
    ("400 ML PP Box", "Nos", 61, 0, 60, 4.72, 283.20, 1, 4.72),
    ("Silver foil", "Kgs", 0.900, 0, 0.750, 708.00, 531.00, 0.150, 106.20),
    ("Foil silver", "Kgs", 0, 0, 0, 531.00, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 14.000, 0, 12.000, 280.00, 3360.00, 2.000, 560.00),
    ("Petha", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("Guldana", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 43.00, 0, 0.00, 13.00, 0.00, 43.00, 559.00),
    ("Onion", "Kgs", 43.00, 0, 39.00, 24.00, 936.00, 4.00, 96.00),
    ("Tomato", "Kgs", 26.00, 0, 20.00, 25.00, 500.00, 6.00, 150.00),
    ("Ginger", "Kgs", 2.00, 0, 1.50, 70.00, 105.00, 0.50, 35.00),
    ("Garlic", "Kgs", 2.04, 0, 1.50, 154.00, 231.00, 0.54, 83.16),
    ("Pumpkin", "Kgs", 0.00, 0, 0.00, 17.00, 0.00, 0.00, 0.00),
    ("Green chilli", "Kgs", 0.00, 3.00, 2.00, 65.00, 130.00, 1.00, 65.00),
    ("Coriander", "Kgs", 0.00, 0, 0.00, 30.00, 0.00, 0.00, 0.00),
    ("Capsicum", "Kgs", 0.00, 0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("Beans", "Kgs", 0.00, 0, 0.00, 94.00, 0.00, 0.00, 0.00),
    ("Carrot", "Kgs", 0.00, 0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("Cauli flower", "Kgs", 0.00, 0, 0.00, 61.00, 0.00, 0.00, 0.00),
    ("Green onion", "Kgs", 0.00, 0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("Bottle GD", "Kgs", 0.00, 0, 0.00, 20.00, 0.00, 0.00, 0.00),
    ("Cabbage", "Kgs", 0.00, 0, 0.00, 44.00, 0.00, 0.00, 0.00),
    ("Cucumber", "Kgs", 10.80, 0, 10.00, 22.00, 220.00, 0.80, 17.60),
    ("Matar", "Kgs", 0.00, 0, 0.00, 100.00, 0.00, 0.00, 0.00),
    ("Paneer", "Kgs", 0.00, 16.00, 16.00, 250.00, 4000.00, 0.00, 0.00),
    ("Lime S", "Kgs", 0.00, 0, 0.00, 198.00, 0.00, 0.00, 0.00),
    ("Dahi", "Kgs", 0.00, 0, 0.00, 75.00, 0.00, 0.00, 0.00),
    ("Kulcha", "Kgs", 0.00, 30.00, 30.00, 30.00, 900.00, 0.00, 0.00),
    ("Tori", "Nos", 0.00, 0, 0.00, 25.00, 0.00, 0.00, 0.00),
    ("Pav", "Nos", 0.00, 0, 0.00, 35.00, 0.00, 0.00, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 540, 515, 70.0, 36050.0, 30223.0),
    ("Paratha", 73, 71, 40.0, 2840.0, 1692.0),
    ("Dahi", 240, 239, 10.0, 2390.0, 2151.0),
    ("Chach", 200, 193, 10.0, 1930.0, 1737.0),
    ("MINI", 60, 51, 50.0, 2550.0, 1450.0),
    ("Amul Kool", 12, 12, 25.0, 300.0, 264.0),
    ("Lahori Zeera", 4, 4, 10.0, 40.0, 36.0),
    ("Lassi", 10, 10, 20.0, 200.0, 190.0),
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
            ("Paratha",  2, "02 X PARATHA SAMPLE",    "General"),
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
        print("🎉 Database successfully updated for 29 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
