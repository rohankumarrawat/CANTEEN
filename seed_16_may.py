import sqlite3

DATE = "2026-05-16"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 613.000, 0.000, 20.000, 31.00, 620.000, 593.000, 18383.00),
    ('RICE', 'Kgs', 401.000, 0.000, 12.000, 65.00, 780.000, 389.000, 25285.00),
    ('R/OIL', 'Ltr', 146.500, 0.000, 5.000, 180.92, 904.615, 141.500, 25600.62),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('RAJMAH', 'Kgs', 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 18.000, 0.000, 0.000, 78.00, 0.000, 18.000, 1404.00),
    ('BESAN', 'Kgs', 37.000, 0.000, 0.000, 94.50, 0.000, 37.000, 3496.50),
    ('DAL ARHAR', 'Kgs', 36.000, 0.000, 0.000, 120.00, 0.000, 36.000, 4320.00),
    ('DAL MASOOR (S)', 'Pkt', 14.000, 0.000, 4.000, 85.00, 340.000, 10.000, 850.00),
    ('URD CRD(CHILKA)', 'KGS', 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ('MASUR CRD(Malika)', 'Kgs', 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.100, 0.000, 0.000, 315.00, 0.000, 0.100, 31.50),
    ('HALDI PDR', 'Kgs', 1.600, 0.000, 0.100, 231.00, 23.100, 1.500, 346.50),
    ('MIRCHI PDR', 'Kgs', 1.800, 0.000, 0.100, 315.00, 31.500, 1.700, 535.50),
    ('DAL CHINI', 'Kgs', 0.290, 0.000, 0.010, 357.00, 3.570, 0.280, 99.96),
    ('LAUNG', 'Kgs', 0.160, 0.000, 0.010, 1155.00, 11.550, 0.150, 173.25),
    ('HING', 'Nos', 14.000, 0.000, 0.000, 89.25, 0.000, 14.000, 1249.50),
    ('KITCHEN KING', 'Kgs', 0.400, 0.000, 0.100, 800.00, 80.000, 0.300, 240.00),
    ('DEGI MIRCH', 'Kgs', 0.700, 0.000, 0.100, 960.00, 96.000, 0.600, 576.00),
    ('KASURI METHI', 'Kgs', 0.350, 0.000, 0.000, 336.00, 0.000, 0.350, 117.60),
    ('GARAM MASALA', 'Kgs', 0.400, 0.000, 0.100, 920.00, 92.000, 0.300, 276.00),
    ('SALT', 'Kgs', 22.000, 0.000, 2.000, 28.00, 56.000, 20.000, 560.00),
    ('DANIYA (S)', 'Kgs', 0.710, 0.000, 0.000, 157.50, 0.000, 0.710, 111.83),
    ('JEERA PDR', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('B ELAICHI', 'Kgs', 0.140, 0.000, 0.010, 1995.00, 19.950, 0.130, 259.35),
    ('METHI DANA', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.370, 0.000, 0.000, 168.00, 0.000, 0.370, 62.16),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 12.000, 0.000, 0.500, 504.00, 252.000, 11.500, 5796.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.370, 0.000, 0.010, 252.00, 2.520, 0.360, 90.72),
    ('MIRCHI (S)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.700, 0.000, 0.000, 752.00, 0.000, 0.700, 526.40),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
    ('GULAB JAL', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('CHANA MASALA', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('KALA CHANA', 'Kgs', 41.000, 0.000, 0.000, 78.00, 0.000, 41.000, 3198.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 5.000, 0.000, 0.000, 60.00, 0.000, 5.000, 300.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ('KEVADA WATER', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('BIRIYANI MASALA', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 2.500, 0.000, 0.100, 168.00, 16.800, 2.400, 403.20),
    ('KALI MIRCH( S)', 'Kgs', 0.280, 0.000, 0.010, 882.00, 8.820, 0.270, 238.14),
    ('MUMFALI DANA', 'Kgs', 9.000, 0.000, 0.000, 157.50, 0.000, 9.000, 1417.50),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 28.400, 56.800, 10.500, 61.83, 649.225, 74.700, 4618.77),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 1.000, 0.000, 0.000, 67.20, 0.000, 1.000, 67.20),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.900, 0.000, 0.000, 880.00, 0.000, 0.900, 792.00),
    ('SOYA BEAN BADIYA', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.410, 0.000, 0.010, 2730.00, 27.300, 0.400, 1092.00),
    ('AMCHUR PDR', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('AACHAR', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('CREAM', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('PARATHA MASALA', 'Kgs', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 1245, 0, 160, 3.186, 509.76, 1085, 3456.81),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3237, 0, 284, 1.575, 447.30, 2953, 4650.98),
    ("ROTI POUCH", "Nos", 13500, 0, 700, 0.236, 165.20, 12800, 3020.80),
    ("SALAD PKT", "Nos", 3624, 0, 284, 0.177, 50.27, 3340, 591.18),
    ("SPOON/MINI MEAL", "Nos", 817, 0, 142, 0.504, 71.57, 675, 340.20),
    ("NEPKIN TUSSU PEPAR", "Nos", 6707, 0, 0, 0.354, 0.00, 6707, 2374.28),
    ("SALT POUCH", "Nos", 855, 0, 142, 0.150, 21.30, 713, 106.95),
    ("PICKLE & PARATHA", "Nos", 2708, 0, 142, 0.896, 127.21, 2566, 2298.71),
    ("TAPE", "Nos", 3, 0, 1, 23.600, 23.60, 2, 47.20),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 65, 0, 18, 3.150, 56.70, 47, 148.05),
    ("PAPER BOX (LUNCH)", "Nos", 2204, 0, 142, 4.956, 703.75, 2062, 10219.27),
    ("BUTTER ROTI PAPER", "NOS", 1400, 0, 0, 0.236, 0.00, 1400, 330.40),
    ("PARATHA BOX", "Nos", 767, 0, 0, 3.360, 0.00, 767, 2577.12),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 0, 0, 0, 141.600, 0.00, 0, 0.00),
    ("400 ML PP BOX", "Nos", 166, 0, 0, 4.720, 0.00, 166, 783.52),
    ("SILVER FOIL", "Kgs", 2.4, 0, 0.000, 708.000, 0.00, 2.400, 1699.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 2.000, 0, 2.000, 280.00, 560.00, 0.000, 0.00),
    ("PETHA", "KGS", 0.000, 0, 0.000, 150.00, 0.00, 0.000, 0.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 16.000, 4.000, 20.000, 10.000, 200.000, 0.000, 0.00),
    ("ONION", "Kgs", 54.000, 0.000, 5.500, 22.000, 121.000, 48.500, 1067.00),
    ("TOMATO", "Kgs", 2.000, 0.000, 2.000, 16.000, 32.000, 0.000, 0.00),
    ("GINGER", "Kgs", 1.000, 0.000, 1.000, 135.000, 135.000, 0.000, 0.00),
    ("GARLIC", "Kgs", 0.280, 0.000, 0.280, 143.000, 40.040, 0.000, 0.00),
    ("PUMPKIN", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 0.420, 0.000, 0.420, 60.000, 25.200, 0.000, 0.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 1.015, 1.015, 22.000, 22.330, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 121.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 1.050, 1.050, 35.000, 36.750, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.955, 0.955, 55.000, 52.525, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 5.000, 4.860, 5.000, 29.000, 145.000, 4.860, 140.94),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 6.000, 6.000, 35.000, 210.000, 0.000, 0.00),
    ("TORI", "Nos", 10.000, 0.000, 10.000, 25.000, 250.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 142, 140, 70.0, 9800, 7675.0),
    ("PARATHA", 70, 0, 40.0, 0, 0.0),
    ("DAHI", 240, 0, 10.0, 0, 0.0),
    ("CHACH", 200, 0, 10.0, 0, 0.0),
    ("MINI", 18, 17, 50.0, 850, 436.0),
    ("AMUL", 0, 0, 25.0, 0, 0.0),
    ("LAHARI JEERA", 9, 9, 10.0, 90, 81.0),
    ("LASSI", 9, 9, 20.0, 180, 171.0),
    ("BROWENI", 0, 0, 40.0, 0, 0.0),
    ("PLUM CAKE", 0, 0, 20.0, 0, 0.0),
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
        print("🎉 Database successfully updated for 16 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
