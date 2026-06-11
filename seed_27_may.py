import sqlite3

DATE = "2026-05-27"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 1412.000, 0.000, 50.000, 31.00, 1550.000, 1362.000, 42222.00),
    ('RICE', 'Kgs', 958.000, 0.000, 38.000, 68.00, 2584.000, 920.000, 62560.00),
    ('R/OIL', 'Ltr', 330.000, 0.000, 9.000, 180.92, 1628.308, 330.000, 58076.31),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('RAJMAH', 'Kgs', 111.000, 0.000, 15.000, 115.00, 1725.000, 96.000, 11040.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 90.000, 0.000, 0.000, 80.00, 0.000, 90.000, 7200.00),
    ('BESAN', 'Kgs', 70.000, 0.000, 3.000, 94.50, 283.500, 67.000, 6331.50),
    ('DAL ARHAR', 'Kgs', 79.000, 0.000, 0.000, 120.00, 0.000, 79.000, 9480.00),
    ('DAL MASOOR (S)', 'Pkt', 23.000, 0.000, 0.000, 85.00, 0.000, 23.000, 1955.00),
    ('URD CRD(CHILKA)', 'KGS', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('MASUR CRD(Malika)', 'Kgs', 15.000, 0.000, 0.000, 85.00, 0.000, 15.000, 1275.00),
    ('MOONG Crd(Chilka)', 'Kgs', 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 2.440, 0.000, 0.200, 315.00, 63.000, 2.240, 705.60),
    ('HALDI PDR', 'Kgs', 8.600, 0.000, 0.300, 231.00, 69.300, 8.300, 1917.30),
    ('MIRCHI PDR', 'Kgs', 7.100, 0.000, 0.300, 315.00, 94.500, 6.800, 2142.00),
    ('DAL CHINI', 'Kgs', 0.070, 0.000, 0.010, 357.00, 3.570, 0.060, 21.42),
    ('LAUNG', 'Kgs', 0.240, 0.000, 0.020, 1155.00, 23.100, 0.220, 254.10),
    ('HING', 'Nos', 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ('KITCHEN KING', 'Kgs', 4.600, 0.000, 0.200, 800.00, 160.001, 4.400, 3520.03),
    ('DEGI MIRCH', 'Kgs', 4.500, 0.000, 0.200, 959.99, 191.999, 4.300, 4127.97),
    ('KASURI METHI', 'Kgs', 0.950, 0.000, 0.050, 336.00, 16.800, 0.900, 302.40),
    ('GARAM MASALA', 'Kgs', 2.500, 0.000, 0.200, 920.00, 183.999, 2.300, 2115.99),
    ('SALT', 'Kgs', 43.000, 0.000, 4.000, 28.00, 112.000, 39.000, 1092.00),
    ('DANIYA (S)', 'Kgs', 1.960, 0.000, 0.200, 199.50, 39.901, 1.760, 351.13),
    ('JEERA PDR', 'Kgs', 2.700, 0.000, 0.200, 420.00, 84.000, 2.500, 1050.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('B ELAICHI', 'Kgs', 0.240, 0.000, 0.020, 1995.00, 39.900, 0.220, 438.90),
    ('METHI DANA', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.660, 0.000, 0.020, 168.00, 3.360, 0.640, 107.52),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 31.500, 0.000, 1.500, 504.00, 756.000, 30.000, 15120.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.900, 0.000, 0.100, 252.00, 25.200, 0.800, 201.60),
    ('MIRCHI (S)', 'Kgs', 0.900, 0.000, 0.100, 367.50, 36.750, 0.800, 294.00),
    ('CHAT MASALA', 'Kgs', 2.100, 0.000, 0.200, 752.00, 150.400, 1.900, 1428.80),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 2.300, 0.000, 0.400, 736.25, 294.500, 1.900, 1398.88),
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
    ('DHANIYA PDR', 'Kgs', 6.800, 0.000, 0.200, 199.50, 39.900, 6.600, 1316.70),
    ('KALI MIRCH( S)', 'Kgs', 0.454, 0.000, 0.050, 882.00, 44.100, 0.404, 356.33),
    ('MUMFALI DANA', 'Kgs', 20.000, 0.000, 3.000, 168.00, 504.000, 17.000, 2856.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 66.700, 0.000, 15.000, 61.83, 927.465, 51.700, 3196.66),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.700, 0.000, 0.300, 880.00, 264.000, 1.400, 1232.00),
    ('SOYA BEAN BADIYA', 'kgs', 50.000, 0.000, 0.000, 94.50, 0.000, 50.000, 4725.00),
    ('JAVTITRI', 'Kgs', 0.150, 0.000, 0.060, 2730.00, 163.800, 0.090, 245.70),
    ('AMCHUR PDR', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 3.750, 0.000, 0.000, 120.00, 0.000, 3.750, 450.00),
    ('SABUDANA', 'Pkt', 10.000, 0.000, 0.000, 105.00, 0.000, 10.000, 1050.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 3159, 0, 403, 3.186, 1283.96, 2756, 8780.62),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3820, 0, 806, 1.575, 1269.45, 3014, 4747.05),
    ("ROTI POUCH", "Nos", 8300, 0, 2900, 0.236, 684.40, 5400, 1274.40),
    ("SALAD PKT", "Nos", 6674, 0, 806, 0.177, 142.66, 5868, 1038.64),
    ("SPOON/MINI MEAL", "Nos", 3431, 0, 462, 0.504, 232.85, 2969, 1496.38),
    ("NEPKIN TUSSU PEPAR", "Nos", 8385, 0, 476, 0.354, 168.50, 7909, 2799.79),
    ("SALT POUCH", "Nos", 3380, 0, 403, 0.150, 60.45, 2977, 446.55),
    ("PICKLE & PARATHA", "Nos", 4292, 0, 476, 0.896, 426.42, 3816, 3418.50),
    ("TAPE", "Nos", 6, 0, 2, 23.600, 47.20, 4, 94.40),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 218, 0, 59, 3.150, 185.85, 159, 500.85),
    ("PAPER BOX (LUNCH)", "Nos", 5529, 0, 403, 4.956, 1997.27, 5126, 25404.46),
    ("BUTTER ROTI PAPER", "Nos", 600, 0, 50, 0.236, 11.80, 550, 129.80),
    ("PARATHA BOX", "Nos", 278, 0, 73, 3.360, 245.28, 205, 688.80),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 4, 0, 1, 141.600, 141.60, 3, 424.80),
    ("400 ML PP BOX", "Nos", 120, 0, 59, 4.720, 278.48, 61, 287.92),
    ("SILVER FOIL", "Kgs", 1.400, 0, 0.500, 708.000, 354.00, 0.900, 637.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 24.000, 0, 10.000, 280.00, 2800.00, 14.000, 3920.00),
    ("PETHA", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 48.000, 0, 5.000, 13.000, 65.00, 43.000, 559.00),
    ("ONION", "Kgs", 71.000, 0, 28.000, 24.000, 672.00, 43.000, 1032.00),
    ("TOMATO", "Kgs", 38.000, 0, 12.000, 25.000, 300.00, 26.000, 650.00),
    ("GINGER", "Kgs", 3.000, 0, 1.000, 70.000, 70.00, 2.000, 140.00),
    ("GARLIC", "Kgs", 3.040, 0, 1.000, 154.000, 154.00, 2.040, 314.16),
    ("PUMPKIN", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 1.000, 0, 1.000, 65.000, 65.00, 0.000, 0.00),
    ("CORRENDER", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 14.460, 14.460, 35.000, 506.10, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 1.410, 1.410, 94.000, 132.54, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 2.730, 2.730, 35.000, 95.55, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 3.140, 3.140, 61.000, 191.54, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0, 0.000, 20.000, 0.00, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 20.800, 0, 10.000, 22.000, 220.00, 10.800, 237.60),
    ("MATAR", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 12.000, 12.000, 250.000, 3000.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0, 0.000, 75.000, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 0, 0.000, 35.000, 0.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 403, 400, 70.0, 28000.0, 24515.0),
    ("PARATHA", 73, 71, 40.0, 2840.0, 2445.0),
    ("DAHI", 240, 239, 10.0, 2390.0, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930.0, 1737.0),
    ("MINI", 59, 57, 50.0, 2850.0, 1174.0),
    ("AMUL", 5, 5, 25.0, 125.0, 110.0),
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
        print("🎉 Database successfully updated for 27 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
