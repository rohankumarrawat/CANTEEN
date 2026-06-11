import sqlite3

DATE = "2026-05-18"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 593.000, 0.000, 66.000, 31.00, 2046.000, 527.000, 16337.00),
    ('RICE', 'Kgs', 389.000, 0.000, 46.000, 65.00, 2990.000, 343.000, 22295.00),
    ('R/OIL', 'Ltr', 141.500, 0.000, 9.000, 180.92, 1628.308, 132.500, 23972.31),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('RAJMAH', 'Kgs', 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 18.000, 0.000, 8.000, 78.00, 624.000, 10.000, 780.00),
    ('BESAN', 'Kgs', 37.000, 0.000, 0.000, 94.50, 0.000, 37.000, 3496.50),
    ('DAL ARHAR', 'Kgs', 36.000, 0.000, 3.000, 120.00, 360.000, 33.000, 3960.00),
    ('DAL MASOOR (S)', 'Pkt', 10.000, 0.000, 3.000, 85.00, 255.000, 7.000, 595.00),
    ('URD CRD(CHILKA)', 'KGS', 6.000, 0.000, 3.000, 110.00, 330.000, 3.000, 330.00),
    ('MASUR CRD(Malika)', 'Kgs', 6.000, 0.000, 3.000, 85.00, 255.000, 3.000, 255.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.100, 0.000, 0.050, 315.00, 15.750, 0.050, 15.75),
    ('HALDI PDR', 'Kgs', 1.500, 0.000, 0.400, 231.00, 92.400, 1.100, 254.10),
    ('MIRCHI PDR', 'Kgs', 1.700, 0.000, 0.300, 315.00, 94.500, 1.400, 441.00),
    ('DAL CHINI', 'Kgs', 0.280, 0.000, 0.010, 357.00, 3.570, 0.270, 96.39),
    ('LAUNG', 'Kgs', 0.140, 0.000, 0.010, 1155.00, 11.550, 0.130, 161.70),
    ('HING', 'Nos', 14.000, 0.000, 0.000, 89.25, 0.000, 14.000, 1249.50),
    ('KITCHEN KING', 'Kgs', 0.300, 0.000, 0.200, 800.00, 160.000, 0.100, 80.00),
    ('DEGI MIRCH', 'Kgs', 0.600, 0.000, 0.200, 960.00, 192.000, 0.400, 384.00),
    ('KASURI METHI', 'Kgs', 0.350, 0.000, 0.070, 336.00, 23.520, 0.280, 94.08),
    ('GARAM MASALA', 'Kgs', 0.300, 0.000, 0.200, 920.00, 184.000, 0.100, 92.00),
    ('SALT', 'Kgs', 20.000, 0.000, 4.000, 28.00, 112.000, 16.000, 448.00),
    ('DANIYA (S)', 'Kgs', 0.710, 0.000, 0.050, 157.50, 7.875, 0.660, 103.95),
    ('JEERA PDR', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('B ELAICHI', 'Kgs', 0.130, 0.000, 0.010, 1995.00, 19.950, 0.120, 239.40),
    ('METHI DANA', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.370, 0.000, 0.020, 168.00, 3.360, 0.350, 58.80),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 11.500, 0.000, 2.000, 504.00, 1008.000, 9.500, 4788.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.360, 0.000, 0.080, 252.00, 20.160, 0.280, 70.56),
    ('MIRCHI (S)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.700, 0.000, 0.100, 752.00, 75.200, 0.600, 451.20),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
    ('GULAB JAL', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('CHANA MASALA', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('KALA CHANA', 'Kgs', 41.000, 0.000, 0.000, 78.00, 0.000, 41.000, 3198.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 5.000, 0.000, 0.000, 60.00, 0.000, 5.000, 300.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ('KEVADA WATER', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('BIRIYANI MASALA', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 2.400, 0.000, 0.300, 168.00, 50.400, 2.100, 352.80),
    ('KALI MIRCH( S)', 'Kgs', 0.270, 0.000, 0.010, 882.00, 8.820, 0.260, 229.32),
    ('MUMFALI DANA', 'Kgs', 9.000, 0.000, 0.000, 157.50, 0.000, 9.000, 1417.50),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 74.700, 56.400, 34.300, 61.83, 2120.803, 96.800, 5985.24),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 1.000, 0.000, 0.000, 67.20, 0.000, 1.000, 67.20),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.900, 0.000, 0.000, 880.00, 0.000, 0.900, 792.00),
    ('SOYA BEAN BADIYA', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.400, 0.000, 0.010, 2730.00, 27.300, 0.390, 1064.70),
    ('AMCHUR PDR', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 2.000, 2.000, 70.00, 140.000, 0.000, 0.00),
    ('AACHAR', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('CREAM', 'Kgs', 3.500, 0.000, 0.000, 220.00, 0.000, 3.500, 770.00),
    ('PARATHA MASALA', 'Kgs', 0.000, 10.000, 8.000, 10.00, 10.000, 2.000, 20.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 1085, 3000, 543, 3.186, 1730.00, 3542, 11284.81),
    ("FOIL BOX (RICE,SABJI)", "Nos", 2953, 4000, 1086, 1.575, 1710.45, 5867, 9240.53),
    ("ROTI POUCH", "Nos", 12800, 0, 2800, 0.236, 660.80, 10000, 2360.00),
    ("SALAD PKT", "Nos", 3340, 6000, 1086, 0.177, 192.22, 8254, 1460.96),
    ("SPOON/MINI MEAL", "Nos", 675, 3000, 605, 0.504, 304.92, 3070, 1547.28),
    ("NEPKIN TUSSU PEPAR", "Nos", 6707, 4200, 615, 0.354, 217.71, 10292, 3643.37),
    ("SALT POUCH", "Nos", 713, 3000, 543, 0.150, 81.45, 3170, 475.50),
    ("PICKLE & PARATHA", "Nos", 2566, 6048, 615, 0.896, 550.94, 7999, 7165.77),
    ("TAPE", "Nos", 2, 8, 1, 23.600, 23.60, 9, 212.40),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 47, 300, 62, 3.150, 195.30, 285, 897.75),
    ("PAPER BOX (LUNCH)", "Nos", 2062, 0, 543, 4.956, 2691.11, 1519, 7528.16),
    ("BUTTER ROTI PAPER", "NOS", 1400, 0, 100, 0.236, 23.60, 1300, 306.80),
    ("PARATHA BOX", "Nos", 767, 0, 72, 3.360, 241.92, 695, 2335.20),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 0, 5, 2, 141.600, 283.20, 3, 424.80),
    ("400 ML PP BOX", "Nos", 166, 100, 0, 4.720, 0.00, 266, 1255.52),
    ("SILVER FOIL", "Kgs", 2.400, 4.000, 0.750, 708.000, 531.00, 5.650, 4000.20),
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
    ("POTATO", "Kgs", 0.000, 146.000, 6.000, 10.000, 60.000, 140.000, 1400.00),
    ("ONION", "Kgs", 48.500, 50.000, 15.000, 22.000, 330.000, 83.500, 1837.00),
    ("TOMATO", "Kgs", 0.000, 40.000, 12.000, 25.000, 300.000, 28.000, 700.00),
    ("GINGER", "Kgs", 0.000, 4.000, 1.000, 85.000, 85.000, 3.000, 255.00),
    ("GARLIC", "Kgs", 0.000, 2.510, 1.000, 154.000, 154.000, 1.510, 232.54),
    ("PUMPKIN", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 0.000, 4.000, 2.000, 45.000, 90.000, 2.000, 90.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 33.000, 0.000, 18.000, 0.000, 33.000, 594.00),
    ("BEANS", "Kgs", 0.000, 3.030, 3.030, 132.000, 399.960, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 3.050, 3.050, 35.000, 106.750, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 3.105, 3.105, 55.000, 170.775, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 90.000, 90.000, 15.000, 1350.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 4.860, 45.000, 20.000, 18.000, 360.000, 29.860, 537.48),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0.000, 0.000, 25.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800, 25419.0),
    ("PARATHA", 72, 70, 40.0, 2800, 1738.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 62, 60, 50.0, 3000, 877.0),
    ("AMUL", 14, 14, 25.0, 350, 308.0),
    ("LAHARI JEERA", 18, 18, 10.0, 180, 162.0),
    ("LASSI", 30, 30, 20.0, 600, 570.0),
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
        print("🎉 Database successfully updated for 18 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
