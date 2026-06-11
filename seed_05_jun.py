import sqlite3

DATE = "2026-06-05"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.550, 0.000, 0.050, 252.00, 12.600, 0.500, 126.00),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 1032.000, 0.000, 56.000, 31.00, 1736.000, 976.000, 30256.00),
    ('B ELAICHI', 'Kgs', 0.120, 0.000, 0.020, 1995.00, 39.900, 0.100, 199.50),
    ('BAKING PDR', 'PKT', 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ('BESAN', 'Kgs', 56.000, 0.000, 0.000, 94.50, 0.000, 56.000, 5292.00),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.200, 0.000, 0.000, 751.88, 0.000, 1.200, 902.25),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.500, 0.000, 0.050, 752.00, 37.600, 0.450, 338.40),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 4.500, 1.000, 1.000, 220.00, 220.000, 3.500, 770.00),
    ('DAL ARHAR', 'Kgs', 65.000, 8.000, 8.000, 120.00, 960.000, 57.000, 6840.00),
    ('DAL CHANA', 'Kgs', 70.000, 8.000, 8.000, 80.00, 640.000, 62.000, 4960.00),
    ('DAL CHINI', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 19.000, 0.000, 0.000, 85.00, 0.000, 19.000, 1615.00),
    ('DANIYA (S)', 'Kgs', 1.300, 0.000, 0.050, 199.50, 9.975, 1.250, 249.38),
    ('DEGI MIRCH', 'Kgs', 2.800, 0.000, 0.200, 959.99, 191.999, 2.600, 2495.98),
    ('DESI GHEE', 'Kgs', 22.000, 1.500, 1.500, 504.00, 756.000, 20.500, 10332.00),
    ('DHANIYA PDR', 'Kgs', 5.100, 0.000, 0.200, 199.50, 39.900, 4.900, 977.55),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 2.500, 0.000, 0.200, 120.00, 24.000, 2.300, 276.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 0.800, 0.000, 0.100, 920.00, 92.000, 0.700, 644.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('HALDI PDR', 'Kgs', 6.600, 0.000, 0.300, 231.00, 69.300, 6.300, 1455.30),
    ('HING', 'Nos', 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.000, 0.000, 0.000, 2730.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 1.750, 0.000, 0.050, 315.00, 15.750, 1.700, 535.50),
    ('JEERA PDR', 'Kgs', 1.800, 0.000, 0.200, 420.00, 84.000, 1.600, 672.00),
    ('KALA CHANA', 'Kgs', 87.000, 0.000, 0.000, 78.00, 0.000, 87.000, 6786.00),
    ('KALI MIRCH( S)', 'Kgs', 0.260, 0.000, 0.020, 882.00, 17.640, 0.240, 211.68),
    ('KASURI METHI', 'Kgs', 0.600, 0.000, 0.050, 336.00, 16.800, 0.550, 184.80),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 2.800, 0.000, 0.300, 800.01, 240.002, 2.500, 2000.02),
    ('LAUNG', 'Kgs', 0.120, 0.000, 0.020, 1155.00, 23.100, 0.100, 115.50),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 44.000, 30.200, 30.200, 61.83, 1867.296, 13.800, 853.27),
    ('MASUR CRD(Malika)', 'Kgs', 12.000, 0.000, 0.000, 85.00, 0.000, 12.000, 1020.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 12.000, 4.000, 4.000, 60.00, 240.000, 8.000, 480.00),
    ('METHI DANA', 'Kgs', 0.240, 0.000, 0.000, 105.00, 0.000, 0.240, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.500, 0.000, 0.050, 367.50, 18.375, 0.450, 165.38),
    ('MIRCHI PDR', 'Kgs', 5.100, 0.000, 0.300, 315.00, 94.500, 4.800, 1512.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('MUMFALI DANA', 'Kgs', 9.000, 4.000, 4.000, 168.00, 672.000, 5.000, 840.00),
    ('PARATHA MASALA', 'Kgs', 9.000, 2.000, 2.000, 10.00, 20.000, 7.000, 70.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 270.000, 10.000, 10.000, 180.92, 1809.231, 260.000, 47040.00),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 80.000, 0.000, 0.000, 115.00, 0.000, 80.000, 9200.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.500, 0.000, 0.000, 736.25, 0.000, 1.500, 1104.38),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 700.000, 0.000, 40.000, 68.00, 2720.000, 660.000, 44880.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.600, 0.000, 0.200, 880.00, 176.000, 0.400, 352.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 23.000, 0.000, 2.000, 28.00, 56.000, 21.000, 588.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.150, 0.000, 0.000, 105.00, 0.000, 0.150, 15.75),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 42.000, 0.000, 0.000, 94.50, 0.000, 42.000, 3969.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.560, 0.000, 0.020, 168.00, 3.360, 0.540, 90.72),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 3577, 0, 520, 3.186, 1656.72, 3057, 9739.60),
    ("FOIL BOX (RICE,SABJI)", "Nos", 1734, 0, 1040, 1.680, 1747.20, 694, 1165.92),
    ("ROTI POUCH", "Nos", 8800, 0, 2800, 0.236, 660.80, 4000, 944.00),
    ("SALAD PKT", "Nos", 6533, 0, 1040, 0.177, 184.08, 5493, 972.26),
    ("SPOON/MINI MEAL", "Nos", 4067, 0, 580, 0.504, 292.32, 3487, 1757.45),
    ("NEPKIN TUSSU PEPAR", "Nos", 9178, 0, 592, 0.354, 209.57, 8586, 3039.44),
    ("SALT POUCH", "Nos", 6337, 0, 520, 0.150, 78.00, 5817, 872.55),
    ("PICKLE & PARATHA", "Nos", 885, 1728, 592, 0.896, 530.33, 2021, 1810.48),
    ("TAPE", "Nos", 3, 0, 2, 23.60, 47.20, 1, 23.60),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 137, 0, 60, 3.360, 201.60, 77, 258.72),
    ("PAPER BOX (LUNCH)", "Nos", 2486, 0, 520, 4.956, 2577.12, 1966, 9743.50),
    ("BUTTER ROTI PAPER", "Nos", 150, 0, 150, 0.236, 35.40, 0, 0.00),
    ("PARATHA BOX", "Nos", 2943, 0, 72, 3.360, 241.92, 2871, 9646.56),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 3, 0, 2, 141.60, 283.20, 1, 141.60),
    ("400 ML PP BOX", "Nos", 0, 0, 0, 4.720, 0.00, 0, 0.00),
    ("SILVER FOIL", "Kg", 0.300, 0, 0.300, 708.00, 212.40, 0.000, 0.00),
    ("FOIL SILVER", "Kg", 0.000, 0, 0.000, 531.00, 0.00, 0.000, 0.00),
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 15.0, 0, 12.0, 280.0, 3360.00, 3.0, 840.00),
    ("PETHA", "KGS", 0.0, 0, 0.0, 150.0, 0.00, 0.0, 0.00),
    ("GULDANA", "KGS", 0.0, 0, 0.0, 250.0, 0.00, 0.0, 0.00),
]

fresh_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 6.000, 150.000, 15.000, 13.00, 195.00, 141.000, 1833.00),
    ("ONION", "Kgs", 6.000, 80.000, 14.000, 24.00, 336.00, 72.000, 1728.00),
    ("TOMATO", "Kgs", 18.000, 0.000, 12.000, 25.00, 300.00, 6.000, 150.00),
    ("GINGER", "Kgs", 1.500, 0.000, 1.000, 80.00, 80.00, 0.500, 40.00),
    ("GARLIC", "Kgs", 1.000, 0.000, 0.500, 154.00, 77.00, 0.500, 77.00),
    ("PUMPKIN", "Kgs", 31.000, 0.000, 0.000, 15.00, 0.00, 31.000, 465.00),
    ("GREEN CHILLI", "Kgs", 2.000, 0.000, 2.000, 65.00, 130.00, 0.000, 0.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0.000, 0.000, 68.00, 0.00, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 110.00, 0.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 50.00, 0.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.000, 0.000, 40.00, 0.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.00, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 18.00, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.00, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 35.000, 0.000, 0.000, 24.00, 0.00, 35.000, 840.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 16.000, 16.000, 250.00, 4000.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.540, 0.200, 110.00, 22.00, 0.340, 37.40),
    ("DAHI", "Kgs", 0.000, 30.000, 30.000, 30.00, 900.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0.000, 0.000, 30.00, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0.000, 0.000, 25.00, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 520, 518, 70.0, 36260.0, 28596.0),
    ("PARATHA", 72, 70, 40.0, 2800.0, 1236.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930.0, 1737.0),
    ("MINI", 60, 58, 50.0, 2900.0, 1429.0),
    ("AMUL", 16, 16, 25.0, 400.0, 352.0),
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
                # Resolve specific name overrides for Sweets (BUNDI -> GULDANA)
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
        print("🎉 Database successfully updated for 05 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
