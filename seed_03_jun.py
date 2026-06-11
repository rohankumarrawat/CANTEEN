import sqlite3

DATE = "2026-06-03"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.650, 0.000, 0.050, 252.00, 12.600, 0.600, 151.20),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 1148.000, 0.000, 50.000, 31.00, 1550.000, 1098.000, 34038.00),
    ('B ELAICHI', 'Kgs', 0.140, 0.000, 0.010, 1995.00, 19.950, 0.130, 259.35),
    ('BAKING PDR', 'PKT', 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ('BESAN', 'Kgs', 57.000, 0.000, 1.000, 94.50, 94.500, 56.000, 5292.00),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 1.600, 0.000, 1.000, 752.00, 752.000, 0.600, 451.20),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 4.500, 0.000, 0.000, 220.00, 0.000, 4.500, 990.00),
    ('DAL ARHAR', 'Kgs', 68.000, 0.000, 0.000, 120.00, 0.000, 68.000, 8160.00),
    ('DAL CHANA', 'Kgs', 70.000, 0.000, 0.000, 80.00, 0.000, 70.000, 5600.00),
    ('DAL CHINI', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 19.000, 0.000, 0.000, 85.00, 0.000, 19.000, 1615.00),
    ('DANIYA (S)', 'Kgs', 1.350, 0.000, 0.000, 199.50, 0.000, 1.350, 269.33),
    ('DEGI MIRCH', 'Kgs', 3.400, 0.000, 0.200, 959.99, 191.999, 3.200, 3071.98),
    ('DESI GHEE', 'Kgs', 25.000, 0.000, 1.000, 504.00, 504.000, 24.000, 12096.00),
    ('DHANIYA PDR', 'Kgs', 5.600, 0.000, 0.200, 199.50, 39.900, 5.400, 1077.30),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.000, 0.000, 0.000, 120.00, 0.000, 3.000, 360.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 1.300, 0.000, 0.200, 920.00, 183.999, 1.100, 1012.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('HALDI PDR', 'Kgs', 7.200, 0.000, 0.200, 231.00, 46.200, 7.000, 1617.00),
    ('HING', 'Nos', 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.000, 0.000, 0.000, 2730.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 1.900, 0.000, 0.100, 315.00, 31.500, 1.800, 567.00),
    ('JEERA PDR', 'Kgs', 2.100, 0.000, 0.000, 420.00, 0.000, 2.100, 882.00),
    ('KALA CHANA', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('KALI MIRCH( S)', 'Kgs', 0.290, 0.000, 0.020, 882.00, 17.640, 0.270, 238.14),
    ('KASURI METHI', 'Kgs', 0.700, 0.000, 0.050, 336.00, 16.800, 0.650, 218.40),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 3.400, 0.000, 0.200, 800.01, 160.001, 3.200, 2560.02),
    ('LAUNG', 'Kgs', 0.150, 0.000, 0.010, 1155.00, 11.550, 0.140, 161.70),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 98.800, 26.400, 26.400, 61.83, 1632.338, 72.400, 4476.56),
    ('MASUR CRD(Malika)', 'Kgs', 12.000, 0.000, 0.000, 85.00, 0.000, 12.000, 1020.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 12.000, 0.000, 0.000, 60.00, 0.000, 12.000, 720.00),
    ('METHI DANA', 'Kgs', 0.240, 0.000, 0.000, 105.00, 0.000, 0.240, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.600, 0.000, 0.050, 367.50, 18.375, 0.550, 202.13),
    ('MIRCHI PDR', 'Kgs', 5.700, 0.000, 0.200, 315.00, 63.000, 5.500, 1732.50),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('MUMFALI DANA', 'Kgs', 13.000, 0.000, 4.000, 168.00, 672.000, 9.000, 1512.00),
    ('PARATHA MASALA', 'Kgs', 9.000, 0.000, 0.000, 10.00, 0.000, 9.000, 90.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 286.000, 0.000, 7.000, 180.92, 1266.462, 279.000, 50477.54),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 96.000, 0.000, 16.000, 115.00, 1840.000, 80.000, 9200.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.900, 0.000, 0.400, 736.25, 294.500, 1.500, 1104.38),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 779.000, 0.000, 39.000, 68.00, 2652.000, 740.000, 50320.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.000, 0.000, 0.400, 880.00, 352.000, 0.600, 528.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 27.000, 0.000, 2.000, 28.00, 56.000, 25.000, 700.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.150, 0.000, 0.000, 105.00, 0.000, 0.150, 15.75),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.580, 0.000, 0.010, 168.00, 1.680, 0.570, 95.76),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 4523, 0, 426, 3.186, 1357.24, 4097, 13053.04),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3590, 0, 810, 1.680, 1360.80, 2774, 4660.32),
    ("ROTI POUCH", "Nos", 12200, 0, 2600, 0.236, 613.60, 9600, 2265.60),
    ("SALAD PKT", "Nos", 7984, 0, 405, 0.177, 71.69, 7573, 1340.42),
    ("SPOON/MINI MEAL", "Nos", 5124, 0, 466, 0.504, 234.86, 4649, 2343.10),
    ("NEPKIN TUSSU PEPAR", "Nos", 10249, 0, 478, 0.354, 169.21, 9771, 3458.93),
    ("SALT POUCH", "Nos", 7262, 0, 405, 0.150, 60.75, 6857, 1028.55),
    ("PICKLE & PARATHA", "Nos", 1956, 0, 478, 0.896, 428.21, 1478, 1324.24),
    ("TAPE", "Nos", 5, 0, 1, 23.60, 23.60, 4, 94.40),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 260, 0, 61, 3.360, 204.96, 199, 668.64),
    ("PAPER BOX (LUNCH)", "Nos", 3411, 0, 405, 4.956, 2007.18, 3006, 14897.74),
    ("BUTTER ROTI PAPER", "Nos", 150, 0, 0, 0.236, 0.00, 150, 35.40),
    ("PARATHA BOX", "Nos", 3089, 0, 73, 3.360, 245.28, 3016, 10133.76),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 4, 0, 0, 141.600, 0.00, 4, 566.40),
    ("400 ML PP BOX", "Nos", 40, 0, 40, 4.720, 188.80, 0, 0.00),
    ("SILVER FOIL", "Kg", 1.000, 0, 0.400, 708.000, 283.20, 0.600, 424.80),
    ("FOIL SILVER", "Kg", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 24.0, 0, 9.0, 280.0, 2520.00, 15.0, 4200.00),
    ("PETHA", "KGS", 15.0, 0, 0.0, 150.0, 0.00, 15.0, 2250.00),
    ("GULDANA", "KGS", 0.0, 0, 0.0, 250.0, 0.00, 0.0, 0.00),
]

fresh_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 31.500, 50.000, 10.500, 13.00, 136.50, 71.000, 923.00),
    ("ONION", "Kgs", 32.000, 0.000, 14.000, 24.00, 336.00, 18.000, 432.00),
    ("TOMATO", "Kgs", 44.000, 0.000, 12.000, 25.00, 300.00, 32.000, 800.00),
    ("GINGER", "Kgs", 4.000, 0.000, 1.000, 80.00, 80.00, 3.000, 240.00),
    ("GARLIC", "Kgs", 3.000, 0.000, 1.000, 154.00, 154.00, 2.000, 308.00),
    ("PUMPKIN", "Kgs", 31.000, 0.000, 0.000, 15.00, 0.00, 31.000, 465.00),
    ("GREEN CHILLI", "Kgs", 5.000, 0.000, 2.000, 65.00, 130.00, 3.000, 195.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0.000, 15.000, 68.00, 1020.00, 0.000, 0.00),
    ("BEANS", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 37.00, 0.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.000, 0.000, 66.00, 0.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.00, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 18.00, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.00, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 8.000, 60.000, 15.000, 24.00, 360.00, 53.000, 1272.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 13.000, 13.000, 250.00, 3250.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.00, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.00, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0.000, 0.000, 30.00, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0.000, 0.000, 25.00, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 405, 400, 70.0, 28000.0, 24656.0),
    ("PARATHA", 72, 70, 40.0, 2800.0, 2257.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940.0, 1746.0),
    ("MINI", 61, 59, 50.0, 2950.0, 1103.0),
    ("AMUL", 8, 8, 25.0, 200.0, 176.0),
    ("LAHARI JEERA", 0, 0, 10.0, 0.0, 0.0),
    ("LASSI", 0, 0, 20.0, 0.0, 0.0),
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
            # Insert sales only if sold > 0 or prepared > 0 to match database patterns
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
        print("🎉 Database successfully updated for 03 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
