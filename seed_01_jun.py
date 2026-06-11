import sqlite3

DATE = "2026-06-01"

dry_items = [
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.750, 0.000, 0.050, 252.00, 12.600, 0.700, 176.40),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 1274.000, 0.000, 63.000, 31.00, 1953.000, 1211.000, 37541.00),
    ('B ELAICHI', 'Kgs', 0.200, 0.000, 0.050, 1995.00, 99.750, 0.150, 299.25),
    ('BAKING PDR', 'PKT', 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ('BESAN', 'Kgs', 67.000, 0.000, 0.000, 94.50, 0.000, 67.000, 6331.50),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 1.800, 0.000, 0.100, 752.00, 75.200, 1.700, 1278.40),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 4.500, 0.000, 0.000, 220.00, 0.000, 4.500, 990.00),
    ('DAL ARHAR', 'Kgs', 71.000, 0.000, 3.000, 120.00, 360.000, 68.000, 8160.00),
    ('DAL CHANA', 'Kgs', 78.000, 0.000, 8.000, 80.00, 640.000, 70.000, 5600.00),
    ('DAL CHINI', 'Kgs', 0.040, 0.000, 0.040, 357.00, 14.280, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 19.000, 0.000, 0.000, 85.00, 0.000, 19.000, 1615.00),
    ('DANIYA (S)', 'Kgs', 1.560, 0.000, 0.160, 199.50, 31.921, 1.400, 279.31),
    ('DEGI MIRCH', 'Kgs', 4.000, 0.000, 0.300, 959.99, 287.998, 3.700, 3551.97),
    ('DESI GHEE', 'Kgs', 28.000, 0.000, 1.500, 504.00, 756.000, 26.500, 13356.00),
    ('DHANIYA PDR', 'Kgs', 6.200, 0.000, 0.300, 199.50, 59.850, 5.900, 1177.05),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.600, 0.000, 0.600, 120.00, 72.000, 3.000, 360.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 1.900, 0.000, 0.300, 920.00, 275.999, 1.600, 1471.99),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('HALDI PDR', 'Kgs', 7.900, 0.000, 0.400, 231.00, 92.400, 7.500, 1732.50),
    ('HING', 'Nos', 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.060, 0.000, 0.010, 2730.00, 27.300, 0.050, 136.50),
    ('JEERA (S)', 'Kgs', 2.090, 0.000, 0.090, 315.00, 28.350, 2.000, 630.00),
    ('JEERA PDR', 'Kgs', 2.200, 0.000, 0.100, 420.00, 42.000, 2.100, 882.00),
    ('KALA CHANA', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('KALI MIRCH( S)', 'Kgs', 0.374, 0.000, 0.074, 882.00, 65.268, 0.300, 264.60),
    ('KASURI METHI', 'Kgs', 0.800, 0.000, 0.050, 336.00, 16.800, 0.750, 252.00),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 4.100, 0.000, 0.400, 800.01, 320.003, 3.700, 2960.02),
    ('LAUNG', 'Kgs', 0.200, 0.000, 0.040, 1155.00, 46.200, 0.160, 184.80),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 74.600, 56.400, 30.200, 61.83, 1867.296, 100.800, 6232.56),
    ('MASUR CRD(Malika)', 'Kgs', 15.000, 0.000, 3.000, 85.00, 255.000, 12.000, 1020.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 12.000, 0.000, 0.000, 60.00, 0.000, 12.000, 720.00),
    ('METHI DANA', 'Kgs', 0.340, 0.000, 0.000, 105.00, 0.000, 0.340, 35.70),
    ('MIRCHI (S)', 'Kgs', 0.750, 0.000, 0.100, 367.50, 36.750, 0.650, 238.88),
    ('MIRCHI PDR', 'Kgs', 6.400, 0.000, 0.400, 315.00, 126.000, 6.000, 1890.00),
    ('MOONG Crd(Chilka)', 'Kgs', 15.000, 0.000, 3.000, 110.00, 330.000, 12.000, 1320.00),
    ('MUMFALI DANA', 'Kgs', 13.000, 0.000, 0.000, 168.00, 0.000, 13.000, 2184.00),
    ('PARATHA MASALA', 'Kgs', 11.000, 0.000, 2.000, 10.00, 20.000, 9.000, 90.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 307.000, 0.000, 9.000, 180.92, 1628.308, 298.000, 53915.08),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 96.000, 0.000, 0.000, 115.00, 0.000, 96.000, 11040.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.900, 0.000, 0.000, 736.25, 0.000, 1.900, 1398.88),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 870.000, 0.000, 45.000, 68.00, 3060.000, 825.000, 56100.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.000, 0.000, 0.000, 880.00, 0.000, 1.000, 880.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 33.000, 0.000, 4.000, 28.00, 112.000, 29.000, 812.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.200, 0.000, 0.000, 105.00, 0.000, 0.200, 21.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.620, 0.000, 0.020, 168.00, 3.360, 0.600, 100.80),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 15.000, 0.000, 3.000, 110.00, 330.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    ("PP BOX (DAL) MINI MEAL", "Nos", 2056, 3500, 515, 3.186, 1640.79, 5041, 16060.63),
    ("FOIL BOX (RICE,SABJI)", "Nos", 1650, 4000, 1030, 1.680, 1730.40, 4620, 7761.60),
    ("ROTI POUCH", "Nos", 1800, 16000, 2800, 0.236, 660.80, 15000, 3540.00),
    ("SALAD PKT", "Nos", 5044, 5000, 1030, 0.177, 182.31, 9014, 1595.48),
    ("SPOON/MINI MEAL", "Nos", 2209, 4000, 515, 0.504, 259.56, 5694, 2869.78),
    ("NEPKIN TUSSU PEPAR", "Nos", 7154, 4200, 515, 0.354, 182.31, 10839, 3837.01),
    ("SALT POUCH", "Nos", 2295, 6000, 515, 0.150, 77.25, 7780, 1167.00),
    ("PICKLE & PARATHA", "Nos", 3061, 0, 515, 0.896, 461.35, 2546, 2280.79),
    ("TAPE", "Nos", 1, 8, 2, 23.60, 47.20, 7, 165.20),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 81, 300, 60, 3.360, 201.60, 321, 1078.56),
    ("PAPER BOX (LUNCH)", "Nos", 4444, 0, 515, 4.956, 2552.34, 3929, 19472.12),
    ("BUTTER ROTI PAPER", "Nos", 250.0, 0, 50.0, 0.236, 11.80, 200.0, 47.20),
    ("PARATHA BOX", "Nos", 132, 0, 71, 3.360, 238.56, 61, 204.96),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.96, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 5, 1, 141.60, 141.60, 5, 708.00),
    ("400 ML PP BOX", "Nos", 1, 100, 0, 4.72, 0.00, 101, 476.72),
    ("SILVER FOIL", "Kg", 0.000, 2.000, 0.500, 708.00, 354.00, 1.500, 1062.00),
    ("FOIL SILVER", "Kg", 0, 0, 0, 531.00, 0.00, 0, 0.00),
]

sweets_items = [
    ("SWEET (BURFI)", "KGS", 0.0, 24.0, 0.0, 280.0, 0.0, 24.0, 6720.0),
    ("PETHA", "KGS", 15.0, 15.0, 15.0, 150.0, 2250.0, 15.0, 2250.0),
    ("GULDANA", "KGS", 0.0, 16.0, 0.0, 250.0, 0.0, 16.0, 4000.0),
]

fresh_items = [
    ("POTATO", "Kgs", 132.50, 0.0, 6.00, 13.00, 78.00, 126.50, 1644.50),
    ("ONION", "Kgs", 68.00, 0.0, 14.00, 24.00, 336.00, 54.00, 1296.00),
    ("TOMATO", "Kgs", 70.00, 0.0, 14.00, 25.00, 350.00, 56.00, 1400.00),
    ("GINGER", "Kgs", 7.00, 0.0, 1.50, 80.00, 120.00, 5.50, 440.00),
    ("GARLIC", "Kgs", 5.09, 0.0, 1.09, 154.00, 167.86, 4.00, 616.00),
    ("PUMPKIN", "Kgs", 31.00, 0.0, 0.00, 15.00, 0.00, 31.00, 465.00),
    ("GREEN CHILLI", "Kgs", 10.00, 0.0, 2.00, 65.00, 130.00, 8.00, 520.00),
    ("CORRENDER", "Kgs", 3.00, 0.0, 1.00, 35.00, 35.00, 2.00, 70.00),
    ("CAPSICUM", "Kgs", 0.00, 0.0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("BEANS", "Kgs", 2.105, 0.0, 2.105, 110.00, 231.55, 0.00, 0.00),
    ("CARROT", "Kgs", 3.17, 0.0, 3.17, 37.00, 117.29, 0.00, 0.00),
    ("CAULI FLOWER", "Kgs", 3.075, 0.0, 3.075, 66.00, 202.95, 0.00, 0.00),
    ("GREEN ONION", "Kgs", 0.00, 0.0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("BOTTLE GD", "Kgs", 90.00, 0.0, 90.00, 18.00, 1620.00, 0.00, 0.00),
    ("CABBAGE", "Kgs", 0.00, 0.0, 0.00, 44.00, 0.00, 0.00, 0.00),
    ("CUCUMBER", "Kgs", 15.67, 0.0, 15.67, 24.00, 376.08, 0.00, 0.00),
    ("MATAR", "Kgs", 0.00, 0.0, 0.00, 100.00, 0.00, 0.00, 0.00),
    ("PANEER", "Kgs", 0.00, 0.0, 0.00, 250.00, 0.00, 0.00, 0.00),
    ("LIME S", "Kgs", 0.00, 0.0, 0.00, 198.00, 0.00, 0.00, 0.00),
    ("DAHI", "Kgs", 0.00, 0.0, 0.00, 75.00, 0.00, 0.00, 0.00),
    ("KULCHA", "Kgs", 0.00, 0.0, 0.00, 30.00, 0.00, 0.00, 0.00),
    ("TORI", "Nos", 0.00, 0.0, 0.00, 25.00, 0.00, 0.00, 0.00),
    ("PAV", "Nos", 0.00, 0.0, 0.00, 35.00, 0.00, 0.00, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 515, 512, 70.0, 35840.0, 24842.0),
    ("PARATHA", 71, 68, 40.0, 2720.0, 2280.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930.0, 1737.0),
    ("MINI", 60, 58, 50.0, 2900.0, 680.0),
    ("AMUL", 17, 17, 25.0, 425.0, 374.0),
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
        print("🎉 Database successfully updated for 01 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
