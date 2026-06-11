import sqlite3

DATE = "2026-06-08"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.100, 0.100, 0.100, 350.00, 35.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.500, 0.000, 0.050, 252.00, 12.600, 0.450, 113.40),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 956.000, 0.000, 66.000, 31.00, 2046.000, 890.000, 27590.00),
    ('B ELAICHI', 'Kgs', 0.100, 0.000, 0.010, 1995.00, 19.950, 0.090, 179.55),
    ('BAKING PDR', 'PKT', 2.000, 0.000, 0.020, 67.20, 1.344, 1.980, 133.06),
    ('BESAN', 'Kgs', 56.000, 0.000, 0.000, 94.50, 0.000, 56.000, 5292.00),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.200, 0.000, 0.000, 751.88, 0.000, 1.200, 902.26),
    ('CHANA MASALA (Pkt)', 'Pkt', -0.000, 0.000, 0.000, 736.01, 0.000, -0.000, -0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.450, 0.000, 0.000, 752.00, 0.000, 0.450, 338.40),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CORN FLOUR', 'PKT', 0.000, 2.000, 1.000, 80.00, 80.000, 1.000, 80.00),
    ('CREAM', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('DAL ARHAR', 'Kgs', 57.000, 0.000, 3.000, 120.00, 360.000, 54.000, 6480.00),
    ('DAL CHANA', 'Kgs', 62.000, 0.000, 4.000, 80.00, 320.000, 58.000, 4640.00),
    ('DAL CHINI', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('DANIYA (S)', 'Kgs', 1.200, 0.000, 0.050, 199.50, 9.975, 1.150, 229.43),
    ('DEGI MIRCH', 'Kgs', 2.500, 0.000, 0.000, 959.99, 0.000, 2.500, 2399.97),
    ('DESI GHEE', 'Kgs', 20.000, 0.000, 1.500, 504.00, 756.000, 18.500, 9324.00),
    ('DHANIYA PDR', 'Kgs', 4.800, 0.000, 0.300, 199.50, 59.850, 4.500, 897.75),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 2.200, 0.000, 0.000, 120.00, 0.000, 2.200, 264.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 0.600, 0.000, 0.000, 920.00, 0.000, 0.600, 552.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.35),
    ('HALDI PDR', 'Kgs', 6.200, 0.000, 0.300, 231.00, 69.300, 5.900, 1362.90),
    ('HING', 'Nos', 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', -0.000, 0.000, 0.000, 2730.00, 0.000, -0.000, -0.00),
    ('JEERA (S)', 'Kgs', 1.650, 0.000, 0.100, 315.00, 31.500, 1.550, 488.25),
    ('JEERA PDR', 'Kgs', 1.600, 0.000, 0.000, 420.00, 0.000, 1.600, 672.00),
    ('KALA CHANA', 'Kgs', 87.000, 0.000, 0.000, 78.00, 0.000, 87.000, 6786.00),
    ('KALI MIRCH PDR', 'PKT', 0.000, 1.000, 1.000, 65.00, 65.000, 0.000, 0.00),
    ('KALI MIRCH( S)', 'Kgs', 0.230, 0.000, 0.030, 882.00, 26.460, 0.200, 176.40),
    ('KASURI METHI', 'Kgs', 0.550, 0.000, 0.050, 336.00, 16.800, 0.500, 168.00),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 2.400, 0.000, 0.000, 800.01, 0.000, 2.400, 1920.02),
    ('LAUNG', 'Kgs', 0.090, 0.000, 0.000, 1155.00, 0.000, 0.090, 103.95),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 60.300, 56.800, 30.300, 63.87, 1935.359, 30.000, 1916.20),
    ('MAIDA', 'Kgs', 0.000, 2.000, 2.000, 70.00, 140.000, 0.000, 0.00),
    ('MASUR CRD(Malika)', 'Kgs', 12.000, 0.000, 3.000, 85.00, 255.000, 9.000, 765.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 8.000, 0.000, 0.000, 60.00, 0.000, 8.000, 480.00),
    ('METHI DANA', 'Kgs', 0.240, 0.000, 0.000, 105.00, 0.000, 0.240, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.440, 0.000, 0.040, 367.50, 14.700, 0.400, 147.00),
    ('MIRCHI PDR', 'Kgs', 4.700, 0.000, 0.300, 315.00, 94.500, 4.400, 1386.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 3.000, 110.00, 330.000, 9.000, 990.00),
    ('MUMFALI DANA', 'Kgs', 5.000, 0.000, 0.000, 168.00, 0.000, 5.000, 840.00),
    ('PARATHA MASALA', 'Kgs', 7.000, 0.000, 0.500, 10.00, 5.000, 6.500, 65.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 255.000, 0.000, 9.000, 180.92, 1628.308, 246.000, 44507.08),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 80.000, 0.000, 0.000, 115.00, 0.000, 80.000, 9200.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.500, 0.000, 0.000, 736.25, 0.000, 1.500, 1104.38),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ('RICE', 'Kgs', 648.500, 0.000, 42.000, 68.00, 2856.000, 606.500, 41242.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.400, 0.000, 0.000, 880.00, 0.000, 0.400, 352.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 20.000, 0.000, 2.000, 28.00, 56.000, 18.000, 504.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.150, 0.000, 0.000, 105.00, 0.000, 0.150, 15.75),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SAYA SAUCE', 'BTL', 0.000, 2.000, 2.000, 70.00, 140.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 42.000, 0.000, 0.000, 94.50, 0.000, 42.000, 3969.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.520, 0.000, 0.020, 168.00, 3.360, 0.500, 84.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 12.000, 0.000, 3.000, 110.00, 330.000, 9.000, 990.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 1.000, 1.000, 84.00, 84.000, 0.000, 0.00),
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2915, 3500, 585, 3.186, 1863.81, 5830, 18574.38),
    ("FOIL BOX (RICE,SABJI)", "Nos", 410, 6000, 1050, 1.680, 1764.00, 5360, 9004.80),
    ("ROTI POUCH", "Nos", 3200, 16000, 2700, 0.236, 637.20, 16500, 3894.00),
    ("SALAD PKT", "Nos", 5209, 6000, 1050, 0.177, 185.85, 10159, 1798.14),
    ("SPOON/MINI MEAL", "Nos", 3327, 4000, 585, 0.504, 294.84, 6742, 3397.97),
    ("NEPKIN TUSSU PEPAR", "Nos", 8444, 3400, 657, 0.354, 232.58, 11187, 3960.20),
    ("SALT POUCH", "Nos", 5675, 0, 525, 0.150, 78.75, 5150, 772.50),
    ("PICKLE & PARATHA", "Nos", 2021, 5184, 597, 0.896, 534.81, 6608, 5919.67),
    ("TAPE", "Nos", 1, 8, 1, 23.60, 23.60, 8, 188.80),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 59, 300, 60, 3.360, 201.60, 299, 1004.64),
    ("PAPER BOX (LUNCH)", "Nos", 1824, 0, 525, 4.956, 2601.90, 1299, 6437.84),
    ("BUTTER ROTI PAPER", "Nos", 0, 1000, 200, 0.236, 47.20, 800, 188.80),
    ("PARATHA BOX", "Nos", 2871, 0, 72, 3.360, 241.92, 2799, 9404.64),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 5, 1, 141.60, 141.60, 5, 708.00),
    ("400 ML PP BOX", "Nos", 0, 150, 0, 4.720, 0.00, 150, 708.00),
    ("SILVER FOIL", "Kg", 0.0, 0, 0.0, 708.00, 0.00, 0.000, 0.00),
    ("FOIL SILVER", "Kg", 0.000, 0, 0.000, 531.00, 0.00, 0.000, 0.00),
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 0.0, 24.000, 0.0, 280.0, 0.00, 24.0, 6720.00),
    ("PETHA", "KGS", 0.0, 15.000, 15.0, 150.0, 2250.00, 0.0, 0.00),
    ("GULDANA", "KGS", 0.0, 16.000, 0.0, 250.0, 0.00, 16.0, 4000.00),
]

fresh_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 141.000, 150.000, 15.000, 13.00, 195.00, 276.000, 3588.00),
    ("ONION", "Kgs", 67.000, 80.000, 12.000, 24.00, 288.00, 135.000, 3240.00),
    ("TOMATO", "Kgs", 0.000, 52.000, 10.000, 25.00, 250.00, 42.000, 1050.00),
    ("GINGER", "Kgs", 0.000, 5.000, 1.000, 110.00, 110.00, 4.000, 440.00),
    ("GARLIC", "Kgs", 0.000, 6.040, 1.000, 154.00, 154.00, 5.040, 776.16),
    ("PUMPKIN", "Kgs", 0.000, 30.000, 0.000, 12.00, 0.00, 30.000, 360.00),
    ("GREEN CHILLI", "Kgs", 0.000, 5.000, 2.000, 55.00, 110.00, 3.000, 165.00),
    ("CORRENDER", "Kgs", 0.000, 1.000, 1.000, 35.00, 35.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 33.000, 2.000, 48.00, 96.00, 31.000, 1488.00),
    ("BEANS", "Kgs", 0.000, 1.000, 1.000, 160.00, 160.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 3.000, 3.000, 80.00, 240.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 2.100, 2.100, 64.00, 134.40, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 1.000, 1.000, 35.00, 35.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 90.000, 90.000, 20.00, 1800.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 3.000, 0.000, 40.00, 0.00, 3.000, 120.00),
    ("CUCUMBER", "Kgs", 30.000, 51.000, 17.000, 18.00, 306.00, 64.000, 1152.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.00, 0.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.340, 1.000, 0.200, 60.00, 12.00, 1.140, 68.40),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.00, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0.000, 0.000, 30.00, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0.000, 0.000, 25.00, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 525, 520, 70.0, 36400.0, 22957.0),
    ("PARATHA", 72, 70, 40.0, 2800.0, 1323.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 192, 10.0, 1920.0, 1728.0),
    ("MINI", 60, 57, 50.0, 2850.0, 2657.0),
    ("AMUL", 16, 0, 25.0, 0.0, 0.0),
    ("LAHARI JEERA", 10, 0, 10.0, 0.0, 0.0),
    ("LASSI", 11, 0, 20.0, 0.0, 0.0),
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

        def process_item_list(items, category):
            for item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt in items:
                if item == 'BUNDI':
                    search_item = 'GULDANA'
                elif item == 'VINEGAR':
                    search_item = 'VINAYGER'
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
        for meal, prepared, sold, rate, income, expdr in sales_summary:
            cursor.execute("SELECT id FROM menu WHERE name = ? COLLATE NOCASE", (meal,))
            menu_row = cursor.fetchone()
            cpu = (expdr / prepared) if prepared > 0 else 0.0
            if menu_row:
                menu_id = menu_row[0]
                cursor.execute("UPDATE menu SET sp = ?, cogs = ?, active = 1 WHERE id = ?", (rate, cpu, menu_id))
            else:
                cursor.execute('''
                    INSERT INTO menu (name, sp, active, cogs)
                    VALUES (?, ?, 1, ?)
                ''', (meal, rate, cpu))
                menu_id = cursor.lastrowid

            wastage = prepared - sold
            if prepared > 0 or sold > 0:
                cursor.execute('''
                    INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'Cash')
                ''', (DATE, menu_id, meal, rate, sold, wastage, expdr))

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
