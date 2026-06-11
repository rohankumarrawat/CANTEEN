import sqlite3

DATE = "2026-06-04"

dry_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.600, 0.000, 0.050, 252.00, 12.600, 0.550, 138.60),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 1098.000, 0.000, 66.000, 31.00, 2046.000, 1032.000, 31992.00),
    ('B ELAICHI', 'Kgs', 0.130, 0.000, 0.010, 1995.00, 19.950, 0.120, 239.40),
    ('BAKING PDR', 'PKT', 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ('BESAN', 'Kgs', 56.000, 0.000, 0.000, 94.50, 0.000, 56.000, 5292.00),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.600, 0.000, 0.400, 751.88, 300.750, 1.200, 902.25),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.600, 0.000, 0.100, 752.00, 75.200, 0.500, 376.00),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 4.500, 0.000, 0.000, 220.00, 0.000, 4.500, 990.00),
    ('DAL ARHAR', 'Kgs', 68.000, 0.000, 3.000, 120.00, 360.000, 65.000, 7800.00),
    ('DAL CHANA', 'Kgs', 70.000, 0.000, 0.000, 80.00, 0.000, 70.000, 5600.00),
    ('DAL CHINI', 'Kgs', 0.000, 0.000, 0.000, 357.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 19.000, 0.000, 0.000, 85.00, 0.000, 19.000, 1615.00),
    ('DANIYA (S)', 'Kgs', 1.350, 0.000, 0.050, 199.50, 9.975, 1.300, 259.36),
    ('DEGI MIRCH', 'Kgs', 3.200, 0.000, 0.400, 959.99, 383.997, 2.800, 2687.98),
    ('DESI GHEE', 'Kgs', 24.000, 0.000, 2.000, 504.00, 1008.000, 22.000, 11088.00),
    ('DHANIYA PDR', 'Kgs', 5.400, 0.000, 0.300, 199.50, 59.850, 5.100, 1017.45),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.000, 0.000, 0.500, 120.00, 60.000, 2.500, 300.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 1.100, 0.000, 0.300, 920.00, 275.999, 0.800, 736.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('HALDI PDR', 'Kgs', 7.000, 0.000, 0.400, 231.00, 92.400, 6.600, 1524.60),
    ('HING', 'Nos', 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.000, 0.000, 0.000, 2730.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 1.800, 0.000, 0.050, 315.00, 15.750, 1.750, 551.25),
    ('JEERA PDR', 'Kgs', 2.100, 0.000, 0.300, 420.00, 126.000, 1.800, 756.00),
    ('KALA CHANA', 'Kgs', 103.000, 0.000, 16.000, 78.00, 1248.000, 87.000, 6786.00),
    ('KALI MIRCH( S)', 'Kgs', 0.270, 0.000, 0.010, 882.00, 8.820, 0.260, 229.32),
    ('KASURI METHI', 'Kgs', 0.650, 0.000, 0.050, 336.00, 16.800, 0.600, 201.60),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 3.200, 0.000, 0.400, 800.01, 320.003, 2.800, 2240.02),
    ('LAUNG', 'Kgs', 0.140, 0.000, 0.020, 1155.00, 23.100, 0.120, 138.60),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 72.400, 28.400, 28.400, 61.83, 1756.000, 44.000, 2720.56),
    ('MASUR CRD(Malika)', 'Kgs', 12.000, 0.000, 0.000, 85.00, 0.000, 12.000, 1020.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 12.000, 0.000, 0.000, 60.00, 0.000, 12.000, 720.00),
    ('METHI DANA', 'Kgs', 0.240, 0.000, 0.000, 105.00, 0.000, 0.240, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.550, 0.000, 0.050, 367.50, 18.375, 0.500, 183.75),
    ('MIRCHI PDR', 'Kgs', 5.500, 0.000, 0.400, 315.00, 126.000, 5.100, 1606.50),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('MUMFALI DANA', 'Kgs', 9.000, 0.000, 0.000, 168.00, 0.000, 9.000, 1512.00),
    ('PARATHA MASALA', 'Kgs', 9.000, 0.000, 0.000, 10.00, 0.000, 9.000, 90.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 279.000, 0.000, 9.000, 180.92, 1628.308, 270.000, 48849.23),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 80.000, 0.000, 0.000, 115.00, 0.000, 80.000, 9200.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.500, 0.000, 0.000, 736.25, 0.000, 1.500, 1104.38),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 740.000, 0.000, 40.000, 68.00, 2720.000, 700.000, 47600.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 3.000, 3.000, 30.00, 90.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.600, 0.000, 0.000, 880.00, 0.000, 0.600, 528.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 25.000, 0.000, 2.000, 28.00, 56.000, 23.000, 644.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.150, 0.000, 0.000, 105.00, 0.000, 0.150, 15.75),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 8.000, 94.50, 756.000, 42.000, 3969.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.570, 0.000, 0.010, 168.00, 1.680, 0.560, 94.08),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 1.000, 1.000, 140.00, 140.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 4097, 0, 520, 3.186, 1656.72, 3577, 11396.32),
    ("FOIL BOX (RICE,SABJI)", "Nos", 2774, 0, 1040, 1.680, 1747.20, 1734, 2913.12),
    ("ROTI POUCH", "Nos", 9600, 0, 2800, 0.236, 660.80, 6800, 1604.80),
    ("SALAD PKT", "Nos", 7573, 0, 1040, 0.177, 184.08, 6533, 1156.34),
    ("SPOON/MINI MEAL", "Nos", 4649, 0, 582, 0.504, 293.33, 4067, 2049.77),
    ("NEPKIN TUSSU PEPAR", "Nos", 9771, 0, 593, 0.354, 209.92, 9178, 3249.01),
    ("SALT POUCH", "Nos", 6857, 0, 520, 0.150, 78.00, 6337, 950.55),
    ("PICKLE & PARATHA", "Nos", 1478, 0, 593, 0.896, 531.23, 885, 792.81),
    ("TAPE", "Nos", 4, 0, 1, 23.60, 23.60, 3, 70.80),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 199, 0, 62, 3.360, 208.32, 137, 460.32),
    ("PAPER BOX (LUNCH)", "Nos", 3006, 0, 520, 4.956, 2577.12, 2486, 12320.62),
    ("BUTTER ROTI PAPER", "Nos", 150, 0, 0, 0.236, 0.00, 150, 35.40),
    ("PARATHA BOX", "Nos", 3016, 0, 73, 3.360, 245.28, 2943, 9888.48),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 4, 0, 1, 141.600, 141.60, 3, 424.80),
    ("400 ML PP BOX", "Nos", 0, 0, 0, 4.720, 0.00, 0, 0.00),
    ("SILVER FOIL", "Kg", 0.600, 0, 0.300, 708.000, 212.40, 0.300, 212.40),
    ("FOIL SILVER", "Kg", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 15.0, 0, 0.0, 280.0, 0.00, 15.0, 4200.00),
    ("PETHA", "KGS", 15.0, 0, 15.0, 150.0, 2250.00, 0.0, 0.00),
    ("GULDANA", "KGS", 0.0, 0, 0.0, 250.0, 0.00, 0.0, 0.00),
]

fresh_items = [
    # (item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 71.000, 0.000, 65.000, 13.00, 845.00, 6.000, 78.00),
    ("ONION", "Kgs", 18.000, 0.000, 12.000, 24.00, 288.00, 6.000, 144.00),
    ("TOMATO", "Kgs", 32.000, 0.000, 14.000, 25.00, 350.00, 18.000, 450.00),
    ("GINGER", "Kgs", 3.000, 0.000, 1.500, 80.00, 120.00, 1.500, 120.00),
    ("GARLIC", "Kgs", 2.000, 0.000, 1.000, 154.00, 154.00, 1.000, 154.00),
    ("PUMPKIN", "Kgs", 31.000, 0.000, 0.000, 15.00, 0.00, 31.000, 465.00),
    ("GREEN CHILLI", "Kgs", 3.000, 0.000, 1.000, 65.00, 65.00, 2.000, 130.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0.000, 0.000, 68.00, 0.00, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 110.00, 0.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 1.000, 1.000, 50.00, 50.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 1.000, 1.000, 40.00, 40.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.00, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 18.00, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.00, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 53.000, 0.000, 18.000, 24.00, 432.00, 35.000, 840.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.00, 0.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.00, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.00, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0.000, 0.000, 30.00, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0.000, 0.000, 25.00, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0.000, 0.000, 35.00, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 520, 517, 70.0, 36190.0, 24679.0),
    ("PARATHA", 73, 71, 40.0, 2840.0, 1520.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940.0, 1746.0),
    ("MINI", 61, 59, 50.0, 2950.0, 920.0),
    ("AMUL", 3, 3, 25.0, 75.0, 66.0),
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
        print("🎉 Database successfully updated for 04 Jun 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
