import sqlite3

DATE = "2026-06-02"

dry_items = [
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.700, 0.000, 0.050, 252.00, 12.600, 0.650, 163.80),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 1211.000, 0.000, 63.000, 31.00, 1953.000, 1148.000, 35588.00),
    ('B ELAICHI', 'Kgs', 0.150, 0.000, 0.010, 1995.00, 19.950, 0.140, 279.30),
    ('BAKING PDR', 'PKT', 3.000, 0.000, 1.000, 67.20, 67.200, 2.000, 134.40),
    ('BESAN', 'Kgs', 67.000, 0.000, 10.000, 94.50, 945.000, 57.000, 5186.50),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 1.700, 0.000, 0.100, 752.00, 75.200, 1.600, 1203.20),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 4.500, 0.000, 0.000, 220.00, 0.000, 4.500, 990.00),
    ('DAL ARHAR', 'Kgs', 68.000, 0.000, 0.000, 120.00, 0.000, 68.000, 8160.00),
    ('DAL CHANA', 'Kgs', 70.000, 0.000, 0.000, 80.00, 0.000, 70.000, 5600.00),
    ('DAL CHINI', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 19.000, 0.000, 0.000, 85.00, 0.000, 19.000, 1615.00),
    ('DANIYA (S)', 'Kgs', 1.400, 0.000, 0.050, 199.50, 9.975, 1.350, 269.33),
    ('DEGI MIRCH', 'Kgs', 3.700, 0.000, 0.300, 959.99, 287.998, 3.400, 3263.98),
    ('DESI GHEE', 'Kgs', 26.500, 0.000, 1.500, 504.00, 756.000, 25.000, 12600.00),
    ('DHANIYA PDR', 'Kgs', 5.900, 0.000, 0.300, 199.50, 59.850, 5.600, 1117.20),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.000, 0.000, 0.000, 120.00, 0.000, 3.000, 360.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 1.600, 0.000, 0.300, 920.00, 275.999, 1.300, 1196.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('HALDI PDR', 'Kgs', 7.500, 0.000, 0.300, 231.00, 69.300, 7.200, 1663.20),
    ('HING', 'Nos', 25.000, 0.000, 4.000, 89.25, 357.000, 21.000, 1874.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.050, 0.000, 0.050, 2730.00, 136.500, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 2.000, 0.000, 0.100, 315.00, 31.500, 1.900, 598.50),
    ('JEERA PDR', 'Kgs', 2.100, 0.000, 0.000, 420.00, 0.000, 2.100, 882.00),
    ('KALA CHANA', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('KALI MIRCH( S)', 'Kgs', 0.300, 0.000, 0.010, 882.00, 8.820, 0.290, 255.78),
    ('KASURI METHI', 'Kgs', 0.750, 0.000, 0.050, 336.00, 16.800, 0.700, 235.20),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 3.700, 0.000, 0.300, 800.01, 240.002, 3.400, 2720.02),
    ('LAUNG', 'Kgs', 0.160, 0.000, 0.010, 1155.00, 11.550, 0.150, 173.25),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 100.800, 28.400, 30.400, 61.83, 1879.662, 98.800, 6108.90),
    ('MASUR CRD(Malika)', 'Kgs', 12.000, 0.000, 0.000, 85.00, 0.000, 12.000, 1020.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 12.000, 0.000, 0.000, 60.00, 0.000, 12.000, 720.00),
    ('METHI DANA', 'Kgs', 0.340, 0.000, 0.100, 105.00, 10.500, 0.240, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.650, 0.000, 0.050, 367.50, 18.375, 0.600, 220.50),
    ('MIRCHI PDR', 'Kgs', 6.000, 0.000, 0.300, 315.00, 94.500, 5.700, 1795.50),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('MUMFALI DANA', 'Kgs', 13.000, 0.000, 0.000, 168.00, 0.000, 13.000, 2184.00),
    ('PARATHA MASALA', 'Kgs', 9.000, 0.000, 0.000, 10.00, 0.000, 9.000, 90.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 298.000, 0.000, 12.000, 180.92, 2171.077, 286.000, 51744.00),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 96.000, 0.000, 0.000, 115.00, 0.000, 96.000, 11040.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.900, 0.000, 0.000, 736.25, 0.000, 1.900, 1398.88),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 825.000, 0.000, 46.000, 68.00, 3128.000, 779.000, 52972.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.000, 0.000, 0.000, 880.00, 0.000, 1.000, 880.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 29.000, 0.000, 2.000, 28.00, 56.000, 27.000, 756.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.200, 0.000, 0.050, 105.00, 5.250, 0.150, 15.75),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.600, 0.000, 0.020, 168.00, 3.360, 0.580, 97.44),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    ("PP BOX (DAL) MINI MEAL", "Nos", 5041, 0, 518, 3.186, 1650.35, 4523, 14410.28),
    ("FOIL BOX (RICE,SABJI)", "Nos", 4620, 0, 1030, 1.680, 1730.40, 3590, 6031.20),
    ("ROTI POUCH", "Nos", 15000, 0, 2800, 0.236, 660.80, 12200, 2879.20),
    ("SALAD PKT", "Nos", 9014, 0, 1030, 0.177, 182.31, 7984, 1413.17),
    ("SPOON/MINI MEAL", "Nos", 5694, 0, 570, 0.504, 287.28, 5124, 2582.50),
    ("NEPKIN TUSSU PEPAR", "Nos", 10839, 0, 590, 0.354, 208.86, 10249, 3628.15),
    ("SALT POUCH", "Nos", 7780, 0, 518, 0.150, 77.70, 7262, 1089.30),
    ("PICKLE & PARATHA", "Nos", 2546, 0, 590, 0.896, 528.64, 1956, 1752.58),
    ("TAPE", "Nos", 7, 0, 2, 23.60, 47.20, 5, 118.00),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 321, 0, 61, 3.360, 204.96, 260, 873.60),
    ("PAPER BOX (LUNCH)", "Nos", 3929, 0, 518, 4.956, 2567.21, 3411, 16904.92),
    ("BUTTER ROTI PAPER", "Nos", 200.0, 0, 50.0, 0.236, 11.80, 150.0, 35.40),
    ("PARATHA BOX", "Nos", 61, 3100, 72, 3.360, 241.92, 3089, 10379.04),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.96, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 5, 0, 1, 141.60, 141.60, 4, 566.40),
    ("400 ML PP BOX", "Nos", 101, 0, 61, 4.72, 287.92, 40, 188.80),
    ("SILVER FOIL", "Kg", 1.500, 0, 0.500, 708.000, 354.00, 1.000, 708.00),
    ("FOIL SILVER", "Kg", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    ("SWEET (BURFI)", "KGS", 24.0, 0, 0.0, 280.0, 0.0, 24.0, 6720.0),
    ("PETHA", "KGS", 15.0, 0, 0.0, 150.0, 0.0, 15.0, 2250.0),
    ("GULDANA", "KGS", 16.0, 0, 16.0, 250.0, 4000.0, 0.0, 0.0),
]

fresh_items = [
    ("POTATO", "Kgs", 126.50, 0.0, 95.00, 13.00, 1235.00, 31.50, 409.50),
    ("ONION", "Kgs", 54.00, 0.0, 22.00, 24.00, 528.00, 32.00, 768.00),
    ("TOMATO", "Kgs", 56.00, 0.0, 12.00, 25.00, 300.00, 44.00, 1100.00),
    ("GINGER", "Kgs", 5.50, 0.0, 1.50, 80.00, 120.00, 4.00, 320.00),
    ("GARLIC", "Kgs", 4.00, 0.0, 1.00, 154.00, 154.00, 3.00, 462.00),
    ("PUMPKIN", "Kgs", 31.00, 0.0, 0.00, 15.00, 0.00, 31.00, 465.00),
    ("GREEN CHILLI", "Kgs", 8.00, 0.0, 3.00, 65.00, 195.00, 5.00, 325.00),
    ("CORRENDER", "Kgs", 2.00, 0.0, 2.00, 35.00, 70.00, 0.00, 0.00),
    ("CAPSICUM", "Kgs", 0.00, 0.0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("BEANS", "Kgs", 0.00, 36.285, 21.285, 68.00, 1447.38, 15.00, 1020.00),
    ("CARROT", "Kgs", 0.00, 0.0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("CAULI FLOWER", "Kgs", 0.00, 0.0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("GREEN ONION", "Kgs", 0.00, 0.0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("BOTTLE GD", "Kgs", 0.00, 0.0, 0.00, 18.00, 0.00, 0.00, 0.00),
    ("CABBAGE", "Kgs", 0.00, 0.0, 0.00, 44.00, 0.00, 0.00, 0.00),
    ("CUCUMBER", "Kgs", 0.00, 30.25, 22.25, 24.00, 534.00, 8.00, 192.00),
    ("MATAR", "Kgs", 0.00, 0.0, 0.00, 100.00, 0.00, 0.00, 0.00),
    ("PANEER", "Kgs", 0.00, 0.0, 0.00, 250.00, 0.00, 0.00, 0.00),
    ("LIME S", "Kgs", 0.00, 0.0, 0.00, 198.00, 0.00, 0.00, 0.00),
    ("DAHI", "Kgs", 0.00, 15.0, 15.0, 75.0, 1125.00, 0.00, 0.00),
    ("KULCHA", "Kgs", 0.00, 0.0, 0.00, 30.00, 0.00, 0.00, 0.00),
    ("TORI", "Nos", 0.00, 0.0, 0.00, 25.00, 0.00, 0.00, 0.00),
    ("PAV", "Nos", 0.00, 0.0, 0.00, 35.00, 0.00, 0.00, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 518, 514, 70.0, 35980.0, 28687.0),
    ("PARATHA", 72, 70, 40.0, 2800.0, 1717.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940.0, 1746.0),
    ("MINI", 61, 59, 50.0, 2950.0, 1204.0),
    ("AMUL", 21, 21, 25.0, 525.0, 462.0),
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
        print("🎉 Database successfully updated for 02 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
