import sqlite3

DATE = "2026-06-06"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.500, 0.000, 0.000, 252.00, 0.000, 0.500, 126.00),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 976.000, 0.000, 20.000, 31.00, 620.000, 956.000, 29636.00),
    ('B ELAICHI', 'Kgs', 0.100, 0.000, 0.000, 1995.00, 0.000, 0.100, 199.50),
    ('BAKING PDR', 'PKT', 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ('BESAN', 'Kgs', 56.000, 0.000, 0.000, 94.50, 0.000, 56.000, 5292.00),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.200, 0.000, 0.000, 751.88, 0.000, 1.200, 902.26),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.450, 0.000, 0.000, 752.00, 0.000, 0.450, 338.40),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('DAL ARHAR', 'Kgs', 57.000, 0.000, 0.000, 120.00, 0.000, 57.000, 6840.00),
    ('DAL CHANA', 'Kgs', 62.000, 0.000, 0.000, 80.00, 0.000, 62.000, 4960.00),
    ('DAL CHINI', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 19.000, 0.000, 4.000, 85.00, 340.000, 15.000, 1275.00),
    ('DANIYA (S)', 'Kgs', 1.250, 0.000, 0.050, 199.50, 9.975, 1.200, 239.40),
    ('DEGI MIRCH', 'Kgs', 2.600, 0.000, 0.100, 959.99, 96.000, 2.500, 2399.98),
    ('DESI GHEE', 'Kgs', 20.500, 0.000, 0.500, 504.00, 252.000, 20.000, 10080.00),
    ('DHANIYA PDR', 'Kgs', 4.900, 0.000, 0.100, 199.50, 19.950, 4.800, 957.60),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 2.300, 0.000, 0.100, 120.00, 12.000, 2.200, 264.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 0.700, 0.000, 0.100, 920.00, 92.000, 0.600, 552.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.35),
    ('HALDI PDR', 'Kgs', 6.300, 0.000, 0.100, 231.00, 23.100, 6.200, 1432.20),
    ('HING', 'Nos', 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.000, 0.000, 0.000, 2730.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 1.700, 0.000, 0.050, 315.00, 15.750, 1.650, 519.75),
    ('JEERA PDR', 'Kgs', 1.600, 0.000, 0.000, 420.00, 0.000, 1.600, 672.00),
    ('KALA CHANA', 'Kgs', 87.000, 0.000, 0.000, 78.00, 0.000, 87.000, 6786.00),
    ('KALI MIRCH( S)', 'Kgs', 0.240, 0.000, 0.010, 882.00, 8.820, 0.230, 202.86),
    ('KASURI METHI', 'Kgs', 0.550, 0.000, 0.000, 336.00, 0.000, 0.550, 184.80),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 2.500, 0.000, 0.100, 800.01, 80.000, 2.400, 1920.02),
    ('LAUNG', 'Kgs', 0.100, 0.000, 0.010, 1155.00, 11.550, 0.090, 103.95),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 13.800, 0.000, 10.300, 61.83, 636.850, 3.500, 216.41),
    ('MASUR CRD(Malika)', 'Kgs', 12.000, 0.000, 0.000, 85.00, 0.000, 12.000, 1020.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 8.000, 0.000, 0.000, 60.00, 0.000, 8.000, 480.00),
    ('METHI DANA', 'Kgs', 0.240, 0.000, 0.000, 105.00, 0.000, 0.240, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.450, 0.000, 0.010, 367.50, 3.675, 0.440, 161.70),
    ('MIRCHI PDR', 'Kgs', 4.800, 0.000, 0.100, 315.00, 31.500, 4.700, 1480.50),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('MUMFALI DANA', 'Kgs', 5.000, 0.000, 0.000, 168.00, 0.000, 5.000, 840.00),
    ('PARATHA MASALA', 'Kgs', 7.000, 0.000, 0.000, 10.00, 0.000, 7.000, 70.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 260.000, 0.000, 5.000, 180.92, 904.600, 255.000, 46134.60),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 80.000, 0.000, 0.000, 115.00, 0.000, 80.000, 9200.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.500, 0.000, 0.000, 736.25, 0.000, 1.500, 1104.38),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 660.000, 0.000, 11.500, 68.00, 782.000, 648.500, 44098.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.400, 0.000, 0.000, 880.00, 0.000, 0.400, 352.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 21.000, 0.000, 1.000, 28.00, 28.000, 20.000, 560.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.150, 0.000, 0.000, 105.00, 0.000, 0.150, 15.75),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 42.000, 0.000, 0.000, 94.50, 0.000, 42.000, 3969.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.540, 0.000, 0.020, 168.00, 3.360, 0.520, 87.36),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 3057, 0, 142, 3.186, 452.41, 2915, 9287.19),
    ("FOIL BOX (RICE,SABJI)", "Nos", 694, 0, 284, 1.680, 477.12, 410, 688.80),
    ("ROTI POUCH", "Nos", 4000, 0, 800, 0.236, 188.80, 3200, 755.20),
    ("SALAD PKT", "Nos", 5493, 0, 284, 0.177, 50.27, 5209, 921.99),
    ("SPOON/MINI MEAL", "Nos", 3487, 0, 160, 0.504, 80.64, 3327, 1676.81),
    ("NEPKIN TUSSU PEPAR", "Nos", 8586, 0, 142, 0.354, 50.27, 8444, 2989.18),
    ("SALT POUCH", "Nos", 5817, 0, 142, 0.150, 21.30, 5675, 851.25),
    ("PICKLE & PARATHA", "Nos", 2021, 0, 0, 0.896, 0.00, 2021, 1810.48),
    ("TAPE", "Nos", 1, 0, 0, 23.60, 0.00, 1, 23.60),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 77, 0, 18, 3.360, 60.48, 59, 198.24),
    ("PAPER BOX (LUNCH)", "Nos", 1966, 0, 142, 4.956, 703.75, 1824, 9039.74),
    ("BUTTER ROTI PAPER", "Nos", 0, 0, 0, 0.236, 0.00, 0, 0.00),
    ("PARATHA BOX", "Nos", 2871, 0, 0, 3.360, 0.00, 2871, 9646.56),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 0, 0, 141.60, 0.00, 1, 141.60),
    ("400 ML PP BOX", "Nos", 0, 0, 0, 4.720, 0.00, 0, 0.00),
    ("SILVER FOIL", "Kg", 0.0, 0, 0.0, 708.00, 0.00, 0.000, 0.00),
    ("FOIL SILVER", "Kg", 0.000, 0, 0.000, 531.00, 0.00, 0.000, 0.00),
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 3.0, 0, 3.0, 280.0, 840.00, 0.0, 0.00),
    ("PETHA", "KGS", 0.0, 0, 0.0, 150.0, 0.00, 0.0, 0.00),
    ("GULDANA", "KGS", 0.0, 0, 0.0, 250.0, 0.00, 0.0, 0.00),
]

fresh_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 141.000, 0.000, 0.000, 13.00, 0.00, 141.000, 1833.00),
    ("ONION", "Kgs", 72.000, 0.000, 5.000, 24.00, 120.00, 67.000, 1608.00),
    ("TOMATO", "Kgs", 6.000, 0.000, 6.000, 25.00, 150.00, 0.000, 0.00),
    ("GINGER", "Kgs", 0.500, 0.000, 0.500, 80.00, 40.00, 0.000, 0.00),
    ("GARLIC", "Kgs", 0.500, 0.000, 0.500, 154.00, 77.00, 0.000, 0.00),
    ("PUMPKIN", "Kgs", 31.000, 0.000, 31.000, 15.00, 465.00, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 0.000, 0.000, 0.000, 65.00, 0.00, 0.000, 0.00),
    ("CORRENDER", "Kgs", 0.000, 0.300, 0.300, 166.65, 49.995, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0.000, 0.000, 68.00, 0.00, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0.500, 0.500, 120.00, 60.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.500, 0.500, 80.00, 40.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.500, 0.500, 80.00, 40.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.00, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 18.00, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.00, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 35.000, 0.000, 5.000, 24.00, 120.00, 30.000, 720.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.00, 0.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.340, 0.000, 0.000, 110.00, 0.00, 0.340, 37.40),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.00, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0.000, 0.000, 30.00, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0.000, 0.000, 25.00, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 6.000, 6.000, 35.00, 210.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 142, 140, 70.0, 9800.0, 7799.0),
    ("PARATHA", 72, 0, 40.0, 0.0, 0.0),
    ("DAHI", 240, 0, 10.0, 0.0, 0.0),
    ("CHACH", 200, 0, 10.0, 0.0, 0.0),
    ("MINI", 18, 16, 50.0, 800.0, 470.0),
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
        print("🎉 Database successfully updated for 06 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
