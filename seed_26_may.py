import sqlite3

DATE = "2026-05-26"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 1478.000, 0.000, 66.000, 31.00, 2046.000, 1412.000, 43772.00),
    ('RICE', 'Kgs', 1004.000, 0.000, 46.000, 68.00, 3128.000, 958.000, 65144.00),
    ('R/OIL', 'Ltr', 342.000, 0.000, 12.000, 180.92, 2171.077, 330.000, 59704.62),
    ('Sarso Dana', 'Kgs', 0.600, 0.000, 0.250, 105.00, 26.250, 0.350, 36.75),
    ('RAJMAH', 'Kgs', 111.000, 0.000, 0.000, 115.00, 0.000, 111.000, 12765.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 90.000, 0.000, 0.000, 80.00, 0.000, 90.000, 7200.00),
    ('BESAN', 'Kgs', 80.000, 0.000, 10.000, 94.50, 945.000, 70.000, 6615.00),
    ('DAL ARHAR', 'Kgs', 80.000, 0.000, 1.000, 120.00, 120.000, 79.000, 9480.00),
    ('DAL MASOOR (S)', 'Pkt', 23.000, 0.000, 0.000, 85.00, 0.000, 23.000, 1955.00),
    ('URD CRD(CHILKA)', 'KGS', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('MASUR CRD(Malika)', 'Kgs', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('MOONG Crd(Chilka)', 'Kgs', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 2.940, 0.000, 0.500, 315.00, 157.500, 2.440, 768.60),
    ('HALDI PDR', 'Kgs', 9.100, 0.000, 0.500, 231.00, 115.500, 8.600, 1986.60),
    ('MIRCHI PDR', 'Kgs', 7.600, 0.000, 0.500, 315.00, 157.500, 7.100, 2236.50),
    ('DAL CHINI', 'Kgs', 0.090, 0.000, 0.020, 357.00, 7.140, 0.070, 24.99),
    ('LAUNG', 'Kgs', 0.270, 0.000, 0.030, 1155.00, 34.650, 0.240, 277.20),
    ('HING', 'Nos', 29.000, 0.000, 4.000, 89.25, 357.000, 25.000, 2231.25),
    ('KITCHEN KING', 'Kgs', 5.100, 0.000, 0.500, 800.00, 400.003, 4.600, 3680.03),
    ('DEGI MIRCH', 'Kgs', 5.000, 0.000, 0.500, 959.99, 479.997, 4.500, 4319.97),
    ('KASURI METHI', 'Kgs', 1.000, 0.000, 0.050, 336.00, 16.800, 0.950, 319.20),
    ('GARAM MASALA', 'Kgs', 3.000, 0.000, 0.500, 920.00, 459.998, 2.500, 2299.99),
    ('SALT', 'Kgs', 47.000, 0.000, 4.000, 28.00, 112.000, 43.000, 1204.00),
    ('DANIYA (S)', 'Kgs', 2.460, 0.000, 0.500, 199.50, 99.752, 1.960, 391.03),
    ('JEERA PDR', 'Kgs', 3.000, 0.000, 0.300, 420.00, 126.000, 2.700, 1134.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('B ELAICHI', 'Kgs', 0.280, 0.000, 0.040, 1995.00, 79.800, 0.240, 478.80),
    ('METHI DANA', 'Kgs', 0.500, 0.000, 0.150, 105.00, 15.750, 0.350, 36.75),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.690, 0.000, 0.030, 168.00, 5.040, 0.660, 110.88),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 32.500, 0.000, 1.000, 504.00, 504.000, 31.500, 15876.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.950, 0.000, 0.050, 252.00, 12.600, 0.900, 226.80),
    ('MIRCHI (S)', 'Kgs', 1.000, 0.000, 0.100, 367.50, 36.750, 0.900, 330.75),
    ('CHAT MASALA', 'Kgs', 2.400, 0.000, 0.300, 752.00, 225.600, 2.100, 1579.20),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 2.700, 0.000, 0.400, 736.25, 294.500, 2.300, 1693.38),
    ('GULAB JAL', 'BTL', 9.000, 0.000, 0.000, 66.15, 0.000, 9.000, 595.37),
    ('CHANA MASALA', 'Kgs', 1.600, 0.000, 0.000, 751.88, 0.000, 1.600, 1203.00),
    ('KALA CHANA', 'Kgs', 103.000, 0.000, 0.000, 78.00, 0.000, 103.000, 8034.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 16.000, 0.000, 0.000, 60.00, 0.000, 16.000, 960.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 5.000, 0.000, 0.000, 68.44, 0.000, 5.000, 342.20),
    ('KEVADA WATER', 'BTL', 10.000, 0.000, 0.000, 70.80, 0.000, 10.000, 708.00),
    ('BIRIYANI MASALA', 'Pkt', 14.000, 0.000, 0.000, 73.50, 0.000, 14.000, 1029.00),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 7.300, 0.000, 0.500, 199.50, 99.750, 6.800, 1356.60),
    ('KALI MIRCH( S)', 'Kgs', 0.484, 0.000, 0.030, 882.00, 26.460, 0.454, 400.43),
    ('MUMFALI DANA', 'Kgs', 20.000, 0.000, 0.000, 168.00, 0.000, 20.000, 3360.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 96.900, 0.000, 30.200, 61.83, 1867.266, 66.700, 4124.13),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 4.000, 0.000, 1.000, 67.20, 67.200, 3.000, 201.60),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.700, 0.000, 0.000, 880.00, 0.000, 1.700, 1496.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('JAVTITRI', 'Kgs', 0.200, 0.000, 0.050, 2730.00, 136.500, 0.150, 409.50),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.750, 0.000, 0.000, 120.00, 0.000, 3.750, 450.00),
    ('SABUDANA', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 3702, 0, 543, 3.186, 1730.00, 3159, 10064.57),
    ("FOIL BOX (RICE,SABJI)", "Nos", 4906, 0, 1086, 1.575, 1710.45, 3820, 6016.50),
    ("ROTI POUCH", "Nos", 11200, 0, 2900, 0.236, 684.40, 8300, 1958.80),
    ("SALAD PKT", "Nos", 7760, 0, 1086, 0.177, 192.22, 6674, 1181.30),
    ("SPOON/MINI MEAL", "Nos", 4023, 0, 592, 0.504, 298.37, 3431, 1729.22),
    ("NEPKIN TUSSU PEPAR", "Nos", 8999, 0, 614, 0.354, 217.36, 8385, 2968.29),
    ("SALT POUCH", "Nos", 3923, 0, 543, 0.150, 81.45, 3380, 507.00),
    ("PICKLE & PARATHA", "Nos", 4906, 0, 614, 0.896, 550.04, 4292, 3844.92),
    ("TAPE", "Nos", 8, 0, 2, 23.600, 47.20, 6, 141.60),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 267, 0, 49, 3.150, 154.35, 218, 686.70),
    ("PAPER BOX (LUNCH)", "Nos", 2972, 3100, 543, 4.956, 2691.11, 5529, 27401.72),
    ("BUTTER ROTI PAPER", "Nos", 650, 0, 50, 0.236, 11.80, 600, 141.60),
    ("PARATHA BOX", "Nos", 349, 0, 71, 3.360, 238.56, 278, 934.08),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 5, 0, 1, 141.600, 141.60, 4, 566.40),
    ("400 ML PP BOX", "Nos", 169, 0, 49, 4.720, 231.28, 120, 566.40),
    ("SILVER FOIL", "Kgs", 2.150, 0, 0.750, 708.000, 531.00, 1.400, 991.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 24.000, 0, 0.000, 280.00, 0.00, 24.000, 6720.00),
    ("PETHA", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 16.000, 0, 16.000, 250.00, 4000.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 133.000, 0, 85.000, 13.000, 1105.00, 48.000, 624.00),
    ("ONION", "Kgs", 98.000, 0, 27.000, 24.000, 648.00, 71.000, 1704.00),
    ("TOMATO", "Kgs", 52.000, 0, 14.000, 25.000, 350.00, 38.000, 950.00),
    ("GINGER", "Kgs", 5.000, 0, 2.000, 70.000, 140.00, 3.000, 210.00),
    ("GARLIC", "Kgs", 4.040, 0, 1.000, 154.000, 154.00, 3.040, 468.16),
    ("PUMPKIN", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 5.000, 0, 4.000, 65.000, 260.00, 1.000, 65.00),
    ("CORRENDER", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 30.000, 0, 30.000, 30.000, 900.00, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0, 0.000, 105.000, 0.00, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0, 0.000, 61.000, 0.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0, 0.000, 20.000, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 43.800, 0, 23.000, 22.000, 506.00, 20.800, 457.60),
    ("MATAR", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0, 0.000, 250.000, 0.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 15.000, 15.000, 75.000, 1125.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800.0, 29900.0),
    ("PARATHA", 71, 70, 40.0, 2800.0, 2040.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 186, 10.0, 1860.0, 1674.0),
    ("MINI", 49, 48, 50.0, 2400.0, 1090.0),
    ("AMUL", 18, 18, 25.0, 450.0, 396.0),
    ("LAHARI JEERA", 2, 0, 10.0, 0.0, 0.0),
    ("LASSI", 4, 0, 20.0, 0.0, 0.0),
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
        print("🎉 Database successfully updated for 26 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
