import sqlite3

DATE = "2026-05-25"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 244.000, 1300.000, 66.000, 31.00, 2046.000, 1478.000, 45818.00),
    ('RICE', 'Kgs', 150.000, 900.000, 46.000, 68.00, 3128.000, 1004.000, 68272.00),
    ('R/OIL', 'Ltr', 82.000, 260.000, 0.000, 180.92, 0.000, 342.000, 61875.69),
    ('Sarso Dana', 'Kgs', 0.100, 0.500, 0.000, 105.00, 0.000, 0.600, 63.00),
    ('RAJMAH', 'Kgs', 31.000, 80.000, 0.000, 115.00, 0.000, 111.000, 12765.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 0.000, 90.000, 0.000, 78.00, 0.000, 90.000, 7200.00),
    ('BESAN', 'Kgs', 20.000, 60.000, 0.000, 94.50, 0.000, 80.000, 7560.00),
    ('DAL ARHAR', 'Kgs', 21.000, 60.000, 0.000, 120.00, 0.000, 80.000, 9600.00),
    ('DAL MASOOR (S)', 'Pkt', 3.000, 20.000, 0.000, 85.00, 0.000, 23.000, 1955.00),
    ('URD CRD(CHILKA)', 'KGS', 3.000, 15.000, 3.000, 110.00, 330.000, 15.000, 1650.00),
    ('MASUR CRD(Malika)', 'Kgs', 3.000, 15.000, 3.000, 85.00, 255.000, 15.000, 1275.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 15.000, 12.000, 110.00, 1320.000, 15.000, 1650.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.940, 2.000, 0.000, 315.00, 0.000, 2.940, 926.10),
    ('HALDI PDR', 'Kgs', 2.500, 7.000, 0.400, 231.00, 92.400, 9.100, 2102.10),
    ('MIRCHI PDR', 'Kgs', 2.000, 6.000, 0.400, 315.00, 126.000, 7.600, 2394.00),
    ('DAL CHINI', 'Kgs', 0.120, 0.000, 0.030, 357.00, 10.710, 0.090, 32.13),
    ('LAUNG', 'Kgs', 0.000, 0.300, 0.030, 1155.00, 34.650, 0.270, 311.85),
    ('HING', 'Nos', 9.000, 20.000, 0.000, 89.25, 0.000, 29.000, 2588.25),
    ('KITCHEN KING', 'Kgs', 1.400, 4.000, 0.300, 800.00, 240.000, 5.100, 4080.03),
    ('DEGI MIRCH', 'Kgs', 1.300, 4.000, 0.300, 959.99, 287.998, 5.000, 4799.97),
    ('KASURI METHI', 'Kgs', 0.050, 1.000, 0.050, 336.00, 16.800, 1.000, 336.00),
    ('GARAM MASALA', 'Kgs', 0.000, 3.000, 0.000, 920.00, 0.000, 3.000, 2759.99),
    ('SALT', 'Kgs', 0.000, 50.000, 3.000, 28.00, 84.000, 47.000, 1316.00),
    ('DANIYA (S)', 'Kgs', 0.160, 2.500, 0.200, 199.50, 39.901, 2.460, 490.78),
    ('JEERA PDR', 'Kgs', 0.000, 3.000, 0.000, 420.00, 0.000, 3.000, 1260.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('B ELAICHI', 'Kgs', 0.000, 0.300, 0.020, 1995.00, 39.900, 0.280, 558.60),
    ('METHI DANA', 'Kgs', 0.000, 0.500, 0.000, 105.00, 0.000, 0.500, 52.50),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.230, 0.500, 0.040, 168.00, 6.720, 0.690, 115.92),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 4.000, 30.000, 1.500, 504.00, 756.000, 32.500, 16380.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.000, 1.000, 0.050, 252.00, 12.600, 0.950, 239.40),
    ('MIRCHI (S)', 'Kgs', 0.000, 1.000, 0.000, 315.00, 0.000, 1.000, 367.50),
    ('CHAT MASALA', 'Kgs', 0.400, 2.000, 0.000, 752.00, 0.000, 2.400, 1804.80),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.100, 1.600, 0.000, 736.00, 0.000, 2.700, 1987.88),
    ('GULAB JAL', 'BTL', 4.000, 5.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('CHANA MASALA', 'Kgs', 0.000, 1.600, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('KALA CHANA', 'Kgs', 23.000, 80.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 1.000, 15.000, 0.000, 60.00, 0.000, 16.000, 960.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 1.000, 4.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('KEVADA WATER', 'BTL', 5.000, 5.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('BIRIYANI MASALA', 'Pkt', 4.000, 10.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 0.700, 7.000, 0.400, 199.50, 79.800, 7.300, 1456.35),
    ('KALI MIRCH( S)', 'Kgs', 0.114, 0.400, 0.030, 882.00, 26.460, 0.484, 426.89),
    ('MUMFALI DANA', 'Kgs', 0.000, 20.000, 0.000, 168.00, 0.000, 20.000, 3360.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 74.600, 56.800, 34.500, 61.83, 2133.169, 96.900, 5991.42),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 0.000, 4.000, 0.000, 67.20, 0.000, 4.000, 268.80),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.100, 1.600, 0.000, 880.00, 0.000, 1.700, 1496.00),
    ('SOYA BEAN BADIYA', 'kgs', 10.000, 40.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('JAVTITRI', 'Kgs', 0.250, 0.000, 0.050, 2730.00, 136.500, 0.200, 546.00),
    ('AMCHUR PDR', 'Pkt', 0.000, 10.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 1.000, 0.000, 1.000, 70.00, 70.000, 0.000, 0.00),
    ('AACHAR', 'Kgs', 3.000, 4.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('CREAM', 'Kgs', 0.500, 6.000, 0.000, 220.00, 0.000, 6.500, 1430.00),
    ('PARATHA MASALA', 'Kgs', 21.000, 0.000, 5.000, 10.00, 50.000, 16.000, 160.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 1.000, 3.000, 0.250, 120.00, 30.000, 3.750, 450.00),
    ('SABUDANA', 'Pkt', 0.000, 10.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 745, 3500, 543, 3.186, 1730.00, 3702, 11794.57),
    ("FOIL BOX (RICE,SABJI)", "Nos", 1992, 4000, 1086, 1.575, 1710.45, 4906, 7726.95),
    ("ROTI POUCH", "Nos", 100, 14000, 2900, 0.236, 684.40, 11200, 2643.20),
    ("SALAD PKT", "Nos", 3846, 5000, 1086, 0.177, 192.22, 7760, 1373.52),
    ("SPOON/MINI MEAL", "Nos", 627, 4000, 604, 0.504, 304.42, 4023, 2027.59),
    ("NEPKIN TUSSU PEPAR", "Nos", 7813, 1800, 614, 0.354, 217.36, 8999, 3185.65),
    ("SALT POUCH", "Nos", 966, 3500, 543, 0.150, 81.45, 3923, 588.45),
    ("PICKLE & PARATHA", "Nos", 5520, 0, 614, 0.896, 550.14, 4906, 4394.96),
    ("TAPE", "Nos", 0, 8, 0, 23.600, 0.00, 8, 188.80),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 28, 300, 61, 3.150, 192.15, 267, 841.05),
    ("PAPER BOX (LUNCH)", "Nos", 415, 3100, 543, 4.956, 2691.11, 2972, 14729.23),
    ("BUTTER ROTI PAPER", "Nos", 700, 0, 50, 0.236, 11.80, 650, 153.40),
    ("PARATHA BOX", "Nos", 420, 0, 71, 3.360, 238.56, 349, 1172.64),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 0, 5, 0, 141.600, 0.00, 5, 708.00),
    ("400 ML PP BOX", "Nos", 69, 100, 0, 4.720, 0.00, 169, 797.68),
    ("SILVER FOIL", "Kgs", 2.900, 0, 0.750, 708.000, 531.00, 2.150, 1522.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 0.000, 24.000, 0.000, 280.00, 0.00, 24.000, 6720.00),
    ("PETHA", "KGS", 0.000, 30.000, 15.000, 150.00, 2250.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 0.000, 16.000, 0.000, 250.00, 0.00, 16.000, 4000.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 138.000, 0, 5.000, 13.000, 65.00, 133.000, 1729.00),
    ("ONION", "Kgs", 115.000, 0, 17.000, 24.000, 408.00, 98.000, 2352.00),
    ("TOMATO", "Kgs", 65.000, 0, 13.000, 25.000, 325.00, 52.000, 1300.00),
    ("GINGER", "Kgs", 6.000, 0, 1.000, 70.000, 70.00, 5.000, 350.00),
    ("GARLIC", "Kgs", 5.040, 0, 1.000, 154.000, 154.00, 4.040, 622.16),
    ("PUMPKIN", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 7.000, 0, 2.000, 65.000, 130.00, 5.000, 325.00),
    ("CORRENDER", "Kgs", 2.000, 0, 2.000, 30.000, 60.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 30.000, 0, 0.000, 30.000, 0.00, 30.000, 900.00),
    ("BEANS", "Kgs", 0.000, 3.065, 3.065, 105.000, 321.825, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 3.115, 3.115, 35.000, 109.025, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 3.170, 3.170, 61.000, 193.370, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 90.000, 0, 90.000, 20.000, 1800.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 62.000, 0, 18.200, 22.000, 400.40, 43.800, 963.60),
    ("MATAR", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0, 0.000, 250.000, 0.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0, 0.000, 75.000, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 532, 70.0, 37240.0, 23956.0),
    ("PARATHA", 71, 69, 40.0, 2760.0, 1935.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 199, 10.0, 1990.0, 1791.0),
    ("MINI", 61, 59, 50.0, 2950.0, 933.0),
    ("AMUL", 16, 16, 25.0, 400.0, 352.0),
    ("LAHARI JEERA", 2, 2, 10.0, 20.0, 18.0),
    ("LASSI", 4, 4, 20.0, 80.0, 76.0),
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
        print("🎉 Database successfully updated for 25 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
