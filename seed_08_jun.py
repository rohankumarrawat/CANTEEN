import sqlite3

DATE = "2026-06-08"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('Aachar', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('Ajinomoto', 'Kgs', 0.100, 0.100, 0.100, 350.00, 35.000, 0.000, 0.00),
    ('Ajwain', 'Pkt', 0.500, 0.000, 0.050, 252.00, 12.600, 0.450, 113.40),
    ('Amchur Powder', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('Atta', 'Kgs', 956.000, 0.000, 66.000, 31.00, 2046.000, 890.000, 27590.00),
    ('Badi Elaichi', 'Kgs', 0.100, 0.000, 0.010, 1995.00, 19.950, 0.090, 179.55),
    ('Baking Powder', 'PKT', 2.000, 0.000, 0.020, 67.20, 1.344, 1.980, 133.06),
    ('Besan', 'Kgs', 56.000, 0.000, 0.000, 94.50, 0.000, 56.000, 5292.00),
    ('Biryani Masala', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('Black Pepper Powder', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Chana Masala', 'Kgs', 1.200, 0.000, 0.000, 751.88, 0.000, 1.200, 902.26),
    ('Chana Masala (pkt)', 'Pkt', -0.000, 0.000, 0.000, 736.01, 0.000, -0.000, -0.00),
    ('Chana Masala (pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('Chat Masala', 'Kgs', 0.450, 0.000, 0.000, 752.00, 0.000, 0.450, 338.40),
    ('Chat Masala (pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('Clean Wrap', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('Corn flour', 'PKT', 0.000, 2.000, 1.000, 80.00, 80.000, 1.000, 80.00),
    ('Cream', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('Dal Arhar', 'Kgs', 57.000, 0.000, 3.000, 120.00, 360.000, 54.000, 6480.00),
    ('Dal Chana', 'Kgs', 62.000, 0.000, 4.000, 80.00, 320.000, 58.000, 4640.00),
    ('Dal chini', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('Dal Makhani Masala', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('Dal masoor (s)', 'Pkt', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('Dhaniya (s)', 'Kgs', 1.200, 0.000, 0.050, 199.50, 9.975, 1.150, 229.43),
    ('Degi Mirch', 'Kgs', 2.500, 0.000, 0.000, 959.99, 0.000, 2.500, 2399.97),
    ('Desi Ghee', 'Kgs', 20.000, 0.000, 1.500, 504.00, 756.000, 18.500, 9324.00),
    ('Dhaniya Powder', 'Kgs', 4.800, 0.000, 0.300, 199.50, 59.850, 4.500, 897.75),
    ('Imli', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('Imli (expensive)', 'Pkt', 2.200, 0.000, 0.000, 120.00, 0.000, 2.200, 264.00),
    ('Eno', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('Food Colour', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('Garam Masala', 'Kgs', 0.600, 0.000, 0.000, 920.00, 0.000, 0.600, 552.00),
    ('Gud', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('Gulab Jal', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.35),
    ('Haldi Powder', 'Kgs', 6.200, 0.000, 0.300, 231.00, 69.300, 5.900, 1362.90),
    ('Hing', 'Nos', 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ('Elaichi Small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('Javitri', 'Kgs', -0.000, 0.000, 0.000, 2730.00, 0.000, -0.000, -0.00),
    ('Jeera (s)', 'Kgs', 1.650, 0.000, 0.100, 315.00, 31.500, 1.550, 488.25),
    ('Jeera Powder', 'Kgs', 1.600, 0.000, 0.000, 420.00, 0.000, 1.600, 672.00),
    ('Kala Chana', 'Kgs', 87.000, 0.000, 0.000, 78.00, 0.000, 87.000, 6786.00),
    ('Kali mirch pdr', 'PKT', 0.000, 1.000, 1.000, 65.00, 65.000, 0.000, 0.00),
    ('Kali Mirch (s)', 'Kgs', 0.230, 0.000, 0.030, 882.00, 26.460, 0.200, 176.40),
    ('Kasuri Methi', 'Kgs', 0.550, 0.000, 0.050, 336.00, 16.800, 0.500, 168.00),
    ('Kewra Water', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('Khus Khus', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('Kitchen King', 'Kgs', 2.400, 0.000, 0.000, 800.01, 0.000, 2.400, 1920.02),
    ('Laung', 'Kgs', 0.090, 0.000, 0.000, 1155.00, 0.000, 0.090, 103.95),
    ('Lobia', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 60.300, 56.800, 30.300, 63.87, 1935.359, 30.000, 1916.20),
    ('Maida', 'Kgs', 0.000, 2.000, 2.000, 70.00, 140.000, 0.000, 0.00),
    ('Masoor Dal (Malika)', 'Kgs', 12.000, 0.000, 3.000, 85.00, 255.000, 9.000, 765.00),
    ('Matar Paneer Masala', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('Matar (TF)', 'Kgs', 8.000, 0.000, 0.000, 60.00, 0.000, 8.000, 480.00),
    ('Methi Dana', 'Kgs', 0.240, 0.000, 0.000, 105.00, 0.000, 0.240, 25.20),
    ('Mirchi (s)', 'Kgs', 0.440, 0.000, 0.040, 367.50, 14.700, 0.400, 147.00),
    ('Mirchi Powder', 'Kgs', 4.700, 0.000, 0.300, 315.00, 94.500, 4.400, 1386.00),
    ('Moong Dal Chilka', 'Kgs', 12.000, 0.000, 3.000, 110.00, 330.000, 9.000, 990.00),
    ('Moongphali Dana', 'Kgs', 5.000, 0.000, 0.000, 168.00, 0.000, 5.000, 840.00),
    ('Paratha Masala', 'Kgs', 7.000, 0.000, 0.500, 10.00, 5.000, 6.500, 65.00),
    ('Pav Bhaji Masala', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/oil', 'Ltr', 255.000, 0.000, 9.000, 180.92, 1628.308, 246.000, 44507.08),
    ('Rai', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('Rajma Masala', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('Rajma', 'Kgs', 80.000, 0.000, 0.000, 115.00, 0.000, 80.000, 9200.00),
    ('Rajma Masala (Kgs)', 'Kgs', 1.500, 0.000, 0.000, 736.25, 0.000, 1.500, 1104.38),
    ('Red Chilli Sauce', 'BTL', 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ('Rice', 'Kgs', 648.500, 0.000, 42.000, 68.00, 2856.000, 606.500, 41242.00),
    ('Rice (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('Sabji Masala', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('Sabudana', 'Pkt', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('Shahi Paneer Masala (kgs)', 'kgs', 0.400, 0.000, 0.000, 880.00, 0.000, 0.400, 352.00),
    ('Shahi Paneer Masala (pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('Salt', 'Kgs', 20.000, 0.000, 2.000, 28.00, 56.000, 18.000, 504.00),
    ('Sambhar Masala', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.150, 0.000, 0.000, 105.00, 0.000, 0.150, 15.75),
    ('Sarson', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('Soya sauce', 'BTL', 0.000, 2.000, 2.000, 70.00, 140.000, 0.000, 0.00),
    ('Soya Bean Badiya', 'kgs', 42.000, 0.000, 0.000, 94.50, 0.000, 42.000, 3969.00),
    ('Star Phool Masala', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('Sugar', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('Tej Patta', 'Kgs', 0.520, 0.000, 0.020, 168.00, 3.360, 0.500, 84.00),
    ('Urad (s)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('Urad Dal Chilka', 'KGS', 12.000, 0.000, 3.000, 110.00, 330.000, 9.000, 990.00),
    ('Urad Dhuli', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('Vinegar', 'BTL', 0.000, 1.000, 1.000, 84.00, 84.000, 0.000, 0.00),
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP Box (Dal) Mini Meal", "Nos", 2915, 3500, 585, 3.186, 1863.81, 5830, 18574.38),
    ("Foil Box (Rice, Sabji)", "Nos", 410, 6000, 1050, 1.680, 1764.00, 5360, 9004.80),
    ("Roti pouch", "Nos", 3200, 16000, 2700, 0.236, 637.20, 16500, 3894.00),
    ("Salad Pkt", "Nos", 5209, 6000, 1050, 0.177, 185.85, 10159, 1798.14),
    ("Spoon/Mini Meal", "Nos", 3327, 4000, 585, 0.504, 294.84, 6742, 3397.97),
    ("Napkin Tissue Paper", "Nos", 8444, 3400, 657, 0.354, 232.58, 11187, 3960.20),
    ("Salt Pouch", "Nos", 5675, 0, 525, 0.150, 78.75, 5150, 772.50),
    ("Pickle & Paratha", "Nos", 2021, 5184, 597, 0.896, 534.81, 6608, 5919.67),
    ("Tape", "Nos", 1, 8, 1, 23.60, 23.60, 8, 188.80),
    ("Big Foil Box (Biryani)", "Nos", 59, 300, 60, 3.360, 201.60, 299, 1004.64),
    ("Paper Box (Lunch)", "Nos", 1824, 0, 525, 4.956, 2601.90, 1299, 6437.84),
    ("Butter Roti Paper", "Nos", 0, 1000, 200, 0.236, 47.20, 800, 188.80),
    ("Paratha Box", "Nos", 2871, 0, 72, 3.360, 241.92, 2799, 9404.64),
    ("Partition Box", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("Black Packet", "Nos", 1, 5, 1, 141.60, 141.60, 5, 708.00),
    ("400 ML PP Box", "Nos", 0, 150, 0, 4.720, 0.00, 150, 708.00),
    ("Silver foil", "Kg", 0.0, 0, 0.0, 708.00, 0.00, 0.000, 0.00),
    ("Foil silver", "Kg", 0.000, 0, 0.000, 531.00, 0.00, 0.000, 0.00),
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Sweet (Burfi)", "KGS", 0.0, 24.000, 0.0, 280.0, 0.00, 24.0, 6720.00),
    ("Petha", "KGS", 0.0, 15.000, 15.0, 150.0, 2250.00, 0.0, 0.00),
    ("Guldana", "KGS", 0.0, 16.000, 0.0, 250.0, 0.00, 16.0, 4000.00),
]

fresh_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("Potato", "Kgs", 141.000, 150.000, 15.000, 13.00, 195.00, 276.000, 3588.00),
    ("Onion", "Kgs", 67.000, 80.000, 12.000, 24.00, 288.00, 135.000, 3240.00),
    ("Tomato", "Kgs", 0.000, 52.000, 10.000, 25.00, 250.00, 42.000, 1050.00),
    ("Ginger", "Kgs", 0.000, 5.000, 1.000, 110.00, 110.00, 4.000, 440.00),
    ("Garlic", "Kgs", 0.000, 6.040, 1.000, 154.00, 154.00, 5.040, 776.16),
    ("Pumpkin", "Kgs", 0.000, 30.000, 0.000, 12.00, 0.00, 30.000, 360.00),
    ("Green chilli", "Kgs", 0.000, 5.000, 2.000, 55.00, 110.00, 3.000, 165.00),
    ("Coriander", "Kgs", 0.000, 1.000, 1.000, 35.00, 35.00, 0.000, 0.00),
    ("Capsicum", "Kgs", 0.000, 33.000, 2.000, 48.00, 96.00, 31.000, 1488.00),
    ("Beans", "Kgs", 0.000, 1.000, 1.000, 160.00, 160.00, 0.000, 0.00),
    ("Carrot", "Kgs", 0.000, 3.000, 3.000, 80.00, 240.00, 0.000, 0.00),
    ("Cauli flower", "Kgs", 0.000, 2.100, 2.100, 64.00, 134.40, 0.000, 0.00),
    ("Green onion", "Kgs", 0.000, 1.000, 1.000, 35.00, 35.00, 0.000, 0.00),
    ("Bottle GD", "Kgs", 0.000, 90.000, 90.000, 20.00, 1800.00, 0.000, 0.00),
    ("Cabbage", "Kgs", 0.000, 3.000, 0.000, 40.00, 0.00, 3.000, 120.00),
    ("Cucumber", "Kgs", 30.000, 51.000, 17.000, 18.00, 306.00, 64.000, 1152.00),
    ("Matar", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ("Paneer", "Kgs", 0.000, 0.000, 0.000, 250.00, 0.00, 0.000, 0.00),
    ("Lime S", "Kgs", 0.340, 1.000, 0.200, 60.00, 12.00, 1.140, 68.40),
    ("Dahi", "Kgs", 0.000, 0.000, 0.000, 75.00, 0.00, 0.000, 0.00),
    ("Kulcha", "Kgs", 0.000, 0.000, 0.000, 30.00, 0.00, 0.000, 0.00),
    ("Tori", "Nos", 0.000, 0.000, 0.000, 25.00, 0.00, 0.000, 0.00),
    ("Pav", "Nos", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 525, 520, 70.0, 36400.0, 22957.0),
    ("Paratha", 72, 70, 40.0, 2800.0, 1323.0),
    ("Dahi", 240, 239, 10.0, 2390.0, 2151.0),
    ("Chach", 200, 192, 10.0, 1920.0, 1728.0),
    ("MINI", 60, 57, 50.0, 2850.0, 2657.0),
    ("Amul Kool", 16, 0, 25.0, 0.0, 0.0),
    ("Lahori Zeera", 10, 0, 10.0, 0.0, 0.0),
    ("Lassi", 11, 0, 20.0, 0.0, 0.0),
]

def seed_db():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM sales WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM batch_prep WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM goods_received WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM expenditure WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM stock_ledger WHERE date = ?", (DATE,))
        cursor.execute("DELETE FROM samples WHERE date = ?", (DATE,))

        def process_item_list(items, category):
            for item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt in items:
                if item == 'BUNDI':
                    search_item = 'Guldana'
                elif item == 'Vinegar':
                    search_item = 'Vinegar'
                else:
                    search_item = item

                cursor.execute("SELECT id, received FROM inventory WHERE item = ? COLLATE NOCASE", (search_item,))
                row = cursor.fetchone()
                if row:
                    inv_id = row[0]
                    cursor.execute("SELECT COALESCE(SUM(qty_change), 0.0) FROM stock_ledger WHERE inv_id = ? AND date < ?", (inv_id, DATE))
                    db_stock = cursor.fetchone()[0]

                    cursor.execute("SELECT COALESCE(SUM(qty_change), 0.0) FROM stock_ledger WHERE inv_id = ? AND date < ? AND transaction_type = 'Received'", (inv_id, DATE))
                    db_received_before = cursor.fetchone()[0]
                    new_received = db_received_before + received
                    
                    reconciliation_start = bbf - db_stock
                    if abs(reconciliation_start) > 0.001:
                        print(f"Reconciling {search_item} BBF mismatch: DB={db_stock:.3f}, Register BBF={bbf:.3f}, Diff={reconciliation_start:.3f}")
                        cursor.execute('''
                            INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                            VALUES (?, ?, 'Reconciliation', ?, 'Manual register BBF discrepancy reconciliation')
                        ''', (DATE, inv_id, reconciliation_start))

                    reconciliation_end = bcf - (bbf + received - issue)
                    if abs(reconciliation_end) > 0.001:
                        print(f"Reconciling {search_item} BCF math mismatch: Register BBF={bbf:.3f}, BCF={bcf:.3f}, Expected BCF={bbf+received-issue:.3f}, Diff={reconciliation_end:.3f}")
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
                    ''', (search_item, category, unit, bcf, bbf, received, rate, DATE))
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
            ("LUNCH",     1, "01 X LUNCH SAMPLE",       "General"),
            ("Paratha",   1, "01 X PARATHA SAMPLE",     "General"),
            ("Dahi",      1, "01 X DAHI SAMPLE",        "General"),
            ("Chach",     1, "01 X CHACH SAMPLE",       "General"),
            ("Chach", 6, "06 X CHACH FOR LADIES", "Staff"),
            ("Amul Kool",     16, "16 X AMUL KOOL SAMPLE",        "General"),
            ("Lahori Zeera", 10, "10 X LAHORI ZEERA SAMPLE", "General"),
            ("Lassi",    11, "11 X LASSI SAMPLE",       "General"),
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
        print("🎉 Database successfully updated for 08 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
