import sqlite3

DATE = "2026-05-29"

dry_items = [
    ('AACHAR', 'Kgs', 7.000, 0.000, 0.000, 147.00, 0.000, 7.000, 1029.00),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.800, 0.000, 0.050, 252.00, 12.600, 0.750, 189.00),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('ATTA', 'Kgs', 1362.000, 0.000, 66.000, 31.00, 2046.000, 1296.000, 40176.00),
    ('B ELAICHI', 'Kgs', 0.220, 0.000, 0.010, 1995.00, 19.950, 0.210, 418.95),
    ('BAKING PDR', 'PKT', 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ('BESAN', 'Kgs', 67.000, 0.000, 0.000, 94.50, 0.000, 67.000, 6331.50),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt) 2', 'Pkt', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 1.900, 0.000, 0.100, 752.00, 75.200, 1.800, 1353.60),
    ('CHAT MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('CREAM', 'Kgs', 5.500, 0.000, 1.000, 220.00, 220.000, 4.500, 990.00),
    ('DAL ARHAR', 'Kgs', 79.000, 0.000, 8.000, 120.00, 960.000, 71.000, 8520.00),
    ('DAL CHANA', 'Kgs', 90.000, 0.000, 12.000, 80.00, 960.000, 78.000, 6240.00),
    ('DAL CHINI', 'Kgs', 0.060, 0.000, 0.010, 357.00, 3.570, 0.050, 17.85),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('DAL MASOOR (S)', 'Pkt', 23.000, 0.000, 0.000, 85.00, 0.000, 23.000, 1955.00),
    ('DANIYA (S)', 'Kgs', 1.760, 0.000, 0.100, 199.50, 19.950, 1.660, 331.18),
    ('DEGI MIRCH', 'Kgs', 4.300, 0.000, 0.200, 959.99, 191.999, 4.100, 3935.97),
    ('DESI GHEE', 'Kgs', 30.000, 0.000, 1.500, 504.00, 756.000, 28.500, 14364.00),
    ('DHANIYA PDR', 'Kgs', 6.600, 0.000, 0.300, 199.50, 59.850, 6.300, 1256.85),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.750, 0.000, 0.050, 120.00, 6.000, 3.700, 444.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('GARAM MASALA', 'Kgs', 2.300, 0.000, 0.300, 920.00, 275.995, 2.000, 1839.99),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('HALDI PDR', 'Kgs', 8.300, 0.000, 0.300, 231.00, 69.300, 8.000, 1848.00),
    ('HING', 'Nos', 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.090, 0.000, 0.020, 2730.00, 54.600, 0.070, 191.10),
    ('JEERA (S)', 'Kgs', 2.240, 0.000, 0.100, 315.00, 31.500, 2.140, 674.10),
    ('JEERA PDR', 'Kgs', 2.500, 0.000, 0.200, 420.00, 84.000, 2.300, 966.00),
    ('KALA CHANA', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('KALI MIRCH( S)', 'Kgs', 0.404, 0.000, 0.020, 882.00, 17.640, 0.384, 338.69),
    ('KASURI METHI', 'Kgs', 0.900, 0.000, 0.050, 336.00, 16.800, 0.850, 285.60),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('KITCHEN KING', 'Kgs', 4.400, 0.000, 0.200, 800.00, 160.001, 4.200, 3360.03),
    ('LAUNG', 'Kgs', 0.220, 0.000, 0.010, 1155.00, 11.550, 0.210, 242.55),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 51.700, 0.000, 25.000, 61.83, 1545.775, 26.700, 1650.89),
    ('MASUR CRD(Malika)', 'Kgs', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 16.000, 0.000, 4.000, 60.00, 240.000, 12.000, 720.00),
    ('METHI DANA', 'Kgs', 0.350, 0.000, 0.010, 105.00, 1.050, 0.340, 35.70),
    ('MIRCHI (S)', 'Kgs', 0.800, 0.000, 0.050, 367.50, 18.375, 0.750, 275.63),
    ('MIRCHI PDR', 'Kgs', 6.800, 0.000, 0.300, 315.00, 94.500, 6.500, 2047.50),
    ('MOONG Crd(Chilka)', 'Kgs', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('MUMFALI DANA', 'Kgs', 17.000, 0.000, 4.000, 168.00, 672.000, 13.000, 2184.00),
    ('PARATHA MASALA', 'Kgs', 11.000, 0.000, 0.000, 10.00, 0.000, 11.000, 110.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('R/OIL', 'Ltr', 321.000, 0.000, 9.000, 180.92, 1628.308, 312.000, 56448.00),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('RAJMAH', 'Kgs', 96.000, 0.000, 0.000, 115.00, 0.000, 96.000, 11040.00),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.900, 0.000, 0.000, 736.25, 0.000, 1.900, 1398.88),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('RICE', 'Kgs', 920.000, 0.000, 38.000, 68.00, 2584.000, 882.000, 59976.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('SABUDANA', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.400, 0.000, 0.400, 880.00, 352.000, 1.000, 880.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 39.000, 0.000, 4.000, 28.00, 112.000, 35.000, 980.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.150, 105.00, 15.750, 0.200, 21.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.640, 0.000, 0.010, 168.00, 1.680, 0.630, 105.84),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('URD CRD(CHILKA)', 'KGS', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2756, 0, 540, 3.186, 1720.44, 2216, 7060.18),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3014, 0, 1080, 1.575, 1701.00, 1934, 3046.05),
    ("ROTI POUCH", "Nos", 5400, 0, 2900, 0.236, 684.40, 2500, 590.00),
    ("SALAD PKT", "Nos", 5868, 0, 540, 0.177, 95.58, 5328, 943.06),
    ("SPOON/MINI MEAL", "Nos", 2969, 0, 600, 0.504, 302.40, 2369, 1193.98),
    ("NEPKIN TUSSU PEPAR", "Nos", 7909, 0, 613, 0.354, 217.00, 7296, 2582.78),
    ("SALT POUCH", "Nos", 2977, 0, 540, 0.150, 81.00, 2437, 365.55),
    ("PICKLE & PARATHA", "Nos", 3816, 0, 613, 0.896, 549.15, 3203, 2869.35),
    ("TAPE", "Nos", 4, 0, 2, 23.60, 47.20, 2, 47.20),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 159, 0, 60, 3.15, 189.00, 99, 311.85),
    ("PAPER BOX (LUNCH)", "Nos", 5126, 0, 540, 4.956, 2676.24, 4586, 22728.22),
    ("BUTTER ROTI PAPER", "Nos", 550, 0, 250, 0.236, 59.00, 300, 70.80),
    ("PARATHA BOX", "Nos", 205, 0, 73, 3.36, 245.28, 132, 443.52),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.96, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 3, 0, 2, 141.60, 283.20, 1, 141.60),
    ("400 ML PP BOX", "Nos", 61, 0, 60, 4.72, 283.20, 1, 4.72),
    ("SILVER FOIL", "Kgs", 0.900, 0, 0.750, 708.00, 531.00, 0.150, 106.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.00, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 14.000, 0, 12.000, 280.00, 3360.00, 2.000, 560.00),
    ("PETHA", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 43.00, 0, 0.00, 13.00, 0.00, 43.00, 559.00),
    ("ONION", "Kgs", 43.00, 0, 39.00, 24.00, 936.00, 4.00, 96.00),
    ("TOMATO", "Kgs", 26.00, 0, 20.00, 25.00, 500.00, 6.00, 150.00),
    ("GINGER", "Kgs", 2.00, 0, 1.50, 70.00, 105.00, 0.50, 35.00),
    ("GARLIC", "Kgs", 2.04, 0, 1.50, 154.00, 231.00, 0.54, 83.16),
    ("PUMPKIN", "Kgs", 0.00, 0, 0.00, 17.00, 0.00, 0.00, 0.00),
    ("GREEN CHILLI", "Kgs", 0.00, 3.00, 2.00, 65.00, 130.00, 1.00, 65.00),
    ("CORRENDER", "Kgs", 0.00, 0, 0.00, 30.00, 0.00, 0.00, 0.00),
    ("CAPSICUM", "Kgs", 0.00, 0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("BEANS", "Kgs", 0.00, 0, 0.00, 94.00, 0.00, 0.00, 0.00),
    ("CARROT", "Kgs", 0.00, 0, 0.00, 35.00, 0.00, 0.00, 0.00),
    ("CAULI FLOWER", "Kgs", 0.00, 0, 0.00, 61.00, 0.00, 0.00, 0.00),
    ("GREEN ONION", "Kgs", 0.00, 0, 0.00, 37.00, 0.00, 0.00, 0.00),
    ("BOTTLE GD", "Kgs", 0.00, 0, 0.00, 20.00, 0.00, 0.00, 0.00),
    ("CABBAGE", "Kgs", 0.00, 0, 0.00, 44.00, 0.00, 0.00, 0.00),
    ("CUCUMBER", "Kgs", 10.80, 0, 10.00, 22.00, 220.00, 0.80, 17.60),
    ("MATAR", "Kgs", 0.00, 0, 0.00, 100.00, 0.00, 0.00, 0.00),
    ("PANEER", "Kgs", 0.00, 16.00, 16.00, 250.00, 4000.00, 0.00, 0.00),
    ("LIME S", "Kgs", 0.00, 0, 0.00, 198.00, 0.00, 0.00, 0.00),
    ("DAHI", "Kgs", 0.00, 0, 0.00, 75.00, 0.00, 0.00, 0.00),
    ("KULCHA", "Kgs", 0.00, 30.00, 30.00, 30.00, 900.00, 0.00, 0.00),
    ("TORI", "Nos", 0.00, 0, 0.00, 25.00, 0.00, 0.00, 0.00),
    ("PAV", "Nos", 0.00, 0, 0.00, 35.00, 0.00, 0.00, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 540, 515, 70.0, 36050.0, 30223.0),
    ("PARATHA", 73, 71, 40.0, 2840.0, 1692.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930.0, 1737.0),
    ("MINI", 60, 51, 50.0, 2550.0, 1450.0),
    ("AMUL", 12, 12, 25.0, 300.0, 264.0),
    ("LAHARI JEERA", 4, 4, 10.0, 40.0, 36.0),
    ("LASSI", 10, 10, 20.0, 200.0, 190.0),
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
        print("🎉 Database successfully updated for 29 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
