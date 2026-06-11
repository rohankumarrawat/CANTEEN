import sqlite3

DATE = "2026-05-22"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 329.000, 0.000, 67.000, 31.00, 2077.000, 262.000, 8122.00),
    ('RICE', 'Kgs', 210.000, 0.000, 47.000, 65.00, 3055.000, 163.000, 10595.00),
    ('R/OIL', 'Ltr', 97.500, 0.000, 10.000, 180.92, 1809.231, 87.500, 15830.77),
    ('Sarso Dana', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('RAJMAH', 'Kgs', 31.000, 0.000, 0.000, 115.00, 0.000, 31.000, 3565.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 10.000, 0.000, 10.000, 78.00, 780.000, 0.000, 0.00),
    ('BESAN', 'Kgs', 22.000, 0.000, 2.000, 94.50, 189.000, 20.000, 1890.00),
    ('DAL ARHAR', 'Kgs', 31.000, 0.000, 10.000, 120.00, 1200.000, 21.000, 2520.00),
    ('DAL MASOOR (S)', 'Pkt', 7.000, 0.000, 0.000, 85.00, 0.000, 7.000, 595.00),
    ('URD CRD(CHILKA)', 'KGS', 3.000, 0.000, 0.000, 110.00, 0.000, 3.000, 330.00),
    ('MASUR CRD(Malika)', 'Kgs', 3.000, 0.000, 0.000, 85.00, 0.000, 3.000, 255.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.940, 0.000, 0.000, 315.00, 0.000, 0.940, 296.10),
    ('HALDI PDR', 'Kgs', 2.900, 0.000, 0.300, 231.00, 69.300, 2.600, 600.60),
    ('MIRCHI PDR', 'Kgs', 2.400, 0.000, 0.300, 315.00, 94.500, 2.100, 661.50),
    ('DAL CHINI', 'Kgs', 0.160, 0.000, 0.030, 357.00, 10.710, 0.130, 46.41),
    ('LAUNG', 'Kgs', 0.030, 0.000, 0.030, 1155.00, 34.650, 0.000, 0.00),
    ('HING', 'Nos', 9.000, 0.000, 0.000, 89.25, 0.000, 9.000, 803.25),
    ('KITCHEN KING', 'Kgs', 1.800, 0.000, 0.300, 800.00, 240.000, 1.500, 1200.00),
    ('DEGI MIRCH', 'Kgs', 1.700, 0.000, 0.300, 960.00, 288.000, 1.400, 1344.00),
    ('KASURI METHI', 'Kgs', 0.100, 0.000, 0.050, 336.00, 16.800, 0.050, 16.80),
    ('GARAM MASALA', 'Kgs', 0.000, 0.000, 0.000, 920.00, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 3.000, 0.000, 3.000, 28.00, 84.000, 0.000, 0.00),
    ('DANIYA (S)', 'Kgs', 0.310, 0.000, 0.100, 157.50, 15.750, 0.210, 33.07),
    ('JEERA PDR', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('B ELAICHI', 'Kgs', 0.030, 0.000, 0.030, 1995.00, 59.850, 0.000, 0.00),
    ('METHI DANA', 'Kgs', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.270, 0.000, 0.030, 168.00, 5.040, 0.240, 40.32),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 6.000, 0.000, 1.500, 504.00, 756.000, 4.500, 2268.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.050, 0.000, 0.050, 252.00, 12.600, 0.000, 0.00),
    ('MIRCHI (S)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.400, 0.000, 0.000, 752.00, 0.000, 0.400, 300.80),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.100, 0.000, 0.000, 736.00, 0.000, 1.100, 809.60),
    ('GULAB JAL', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('CHANA MASALA', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('KALA CHANA', 'Kgs', 23.000, 0.000, 0.000, 78.00, 0.000, 23.000, 1794.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 5.000, 0.000, 4.000, 60.00, 240.000, 1.000, 60.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 1.000, 0.000, 0.000, 68.44, 0.000, 1.000, 68.44),
    ('KEVADA WATER', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('BIRIYANI MASALA', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 1.100, 0.000, 0.300, 168.00, 50.400, 0.800, 134.40),
    ('KALI MIRCH( S)', 'Kgs', 0.154, 0.000, 0.030, 882.00, 26.460, 0.124, 109.37),
    ('MUMFALI DANA', 'Kgs', 1.000, 0.000, 1.000, 157.50, 157.500, 0.000, 0.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 43.600, 0.000, 18.000, 61.83, 1112.958, 25.600, 1582.87),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 0.000, 0.000, 0.000, 67.20, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.500, 0.000, 0.400, 880.00, 352.000, 0.100, 88.00),
    ('SOYA BEAN BADIYA', 'kgs', 10.000, 0.000, 0.000, 94.50, 0.000, 10.000, 945.00),
    ('JAVTITRI', 'Kgs', 0.290, 0.000, 0.030, 2730.00, 81.900, 0.260, 709.80),
    ('AMCHUR PDR', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 3.000, 0.000, 2.000, 70.00, 140.000, 1.000, 70.00),
    ('AACHAR', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('CREAM', 'Kgs', 2.500, 0.000, 2.000, 220.00, 440.000, 0.500, 110.00),
    ('PARATHA MASALA', 'Kgs', 31.000, 0.000, 10.000, 10.00, 100.000, 21.000, 210.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 1.000, 0.000, 0.000, 120.00, 0.000, 1.000, 120.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2013, 0, 1126, 3.186, 3587.44, 887, 2825.98),
    ("FOIL BOX (RICE,SABJI)", "Nos", 2809, 0, 533, 1.575, 839.48, 2276, 3584.70),
    ("ROTI POUCH", "Nos", 1800, 2000, 2800, 0.236, 660.80, 1000, 236.00),
    ("SALAD PKT", "Nos", 5196, 0, 1066, 0.177, 188.68, 4130, 731.01),
    ("SPOON/MINI MEAL", "Nos", 1362, 0, 593, 0.504, 298.87, 769, 387.58),
    ("NEPKIN TUSSU PEPAR", "Nos", 8560, 0, 605, 0.354, 214.17, 7955, 2816.07),
    ("SALT POUCH", "Nos", 1641, 0, 533, 0.150, 79.95, 1108, 166.20),
    ("PICKLE & PARATHA", "Nos", 6267, 0, 605, 0.896, 541.98, 5662, 5072.21),
    ("TAPE", "Nos", 3, 0, 2, 23.600, 47.20, 1, 23.60),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 106, 0, 60, 3.150, 189.00, 46, 144.90),
    ("PAPER BOX (LUNCH)", "Nos", 1090, 0, 533, 4.956, 2641.55, 557, 2760.49),
    ("BUTTER ROTI PAPER", "Nos", 1000, 0, 200, 0.236, 47.20, 800, 188.80),
    ("PARATHA BOX", "Nos", 492, 0, 72, 3.360, 241.92, 420, 1411.20),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 0, 1, 141.600, 141.60, 0, 0.00),
    ("400 ML PP BOX", "Nos", 87, 0, 0, 4.720, 0.00, 87, 410.64),
    ("SILVER FOIL", "Kgs", 3.650, 0, 0.750, 708.000, 531.00, 2.900, 2053.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 12.000, 0, 12.000, 280.00, 3360.00, 0.000, 0.00),
    ("PETHA", "KGS", 0.000, 0, 0.000, 150.00, 0.00, 0.000, 0.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 8.000, 0, 0.000, 10.000, 0.00, 8.000, 80.00),
    ("ONION", "Kgs", 83.500, 0, 20.000, 22.000, 440.00, 63.500, 1397.00),
    ("TOMATO", "Kgs", 14.000, 0, 12.000, 25.000, 300.00, 2.000, 50.00),
    ("GINGER", "Kgs", 0.000, 2.045, 1.500, 138.000, 207.00, 0.545, 75.21),
    ("GARLIC", "Kgs", 0.580, 0, 0.500, 154.000, 77.00, 0.080, 12.32),
    ("PUMPKIN", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 4.060, 0, 2.060, 35.000, 72.10, 2.000, 70.00),
    ("CORRENDER", "Kgs", 0.000, 0, 0.000, 45.000, 0.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0, 0.000, 18.000, 0.00, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0, 0.000, 121.000, 0.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0, 0.000, 55.000, 0.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0, 0.000, 15.000, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 13.860, 4.140, 18.000, 20.000, 360.00, 0.000, 0.00),
    ("MATAR", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 16.000, 16.000, 250.000, 4000.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0, 0.000, 75.000, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 30.000, 30.000, 30.000, 900.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0, 0.000, 10.000, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 533, 530, 70.0, 37100, 30694.0),
    ("PARATHA", 71, 70, 40.0, 2800, 1664.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 60, 58, 50.0, 2900, 1108.0),
    ("AMUL", 15, 15, 25.0, 375, 330.0),
    ("LAHARI JEERA", 5, 5, 10.0, 50, 45.0),
    ("LASSI", 20, 20, 20.0, 400, 380.0),
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
        print("🎉 Database successfully updated for 22 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
