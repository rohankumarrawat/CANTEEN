import sqlite3

DATE = "2026-05-23"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 262.000, 0.000, 18.000, 31.00, 558.000, 244.000, 7564.00),
    ('RICE', 'Kgs', 163.000, 0.000, 13.000, 65.00, 845.000, 150.000, 9750.00),
    ('R/OIL', 'Ltr', 87.500, 0.000, 5.500, 180.92, 995.077, 82.000, 14835.69),
    ('Sarso Dana', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('RAJMAH', 'Kgs', 31.000, 0.000, 0.000, 115.00, 0.000, 31.000, 3565.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 0.000, 0.000, 0.000, 78.00, 0.000, 0.000, 0.00),
    ('BESAN', 'Kgs', 20.000, 0.000, 0.000, 94.50, 0.000, 20.000, 1890.00),
    ('DAL ARHAR', 'Kgs', 21.000, 0.000, 0.000, 120.00, 0.000, 21.000, 2520.00),
    ('DAL MASOOR (S)', 'Pkt', 7.000, 0.000, 4.000, 85.00, 340.000, 3.000, 255.00),
    ('URD CRD(CHILKA)', 'KGS', 3.000, 0.000, 0.000, 110.00, 0.000, 3.000, 330.00),
    ('MASUR CRD(Malika)', 'Kgs', 3.000, 0.000, 0.000, 85.00, 0.000, 3.000, 255.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.940, 0.000, 0.000, 315.00, 0.000, 0.940, 296.10),
    ('HALDI PDR', 'Kgs', 2.600, 0.000, 0.100, 231.00, 23.100, 2.500, 577.50),
    ('MIRCHI PDR', 'Kgs', 2.100, 0.000, 0.100, 315.00, 31.500, 2.000, 630.00),
    ('DAL CHINI', 'Kgs', 0.130, 0.000, 0.010, 357.00, 3.570, 0.120, 42.84),
    ('LAUNG', 'Kgs', 0.000, 0.000, 0.000, 1155.00, 0.000, 0.000, 0.00),
    ('HING', 'Nos', 9.000, 0.000, 0.000, 89.25, 0.000, 9.000, 803.25),
    ('KITCHEN KING', 'Kgs', 1.500, 0.000, 0.100, 800.00, 80.000, 1.400, 1120.00),
    ('DEGI MIRCH', 'Kgs', 1.400, 0.000, 0.100, 960.00, 96.000, 1.300, 1248.00),
    ('KASURI METHI', 'Kgs', 0.050, 0.000, 0.000, 336.00, 0.000, 0.050, 16.80),
    ('GARAM MASALA', 'Kgs', 0.000, 0.000, 0.000, 920.00, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 0.000, 0.000, 0.000, 28.00, 0.000, 0.000, 0.00),
    ('DANIYA (S)', 'Kgs', 0.210, 0.000, 0.050, 157.50, 7.875, 0.160, 25.20),
    ('JEERA PDR', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.000, 0.000, 0.000, 736.01, 0.000, 0.000, 0.00),
    ('B ELAICHI', 'Kgs', 0.000, 0.000, 0.000, 1995.00, 0.000, 0.000, 0.00),
    ('METHI DANA', 'Kgs', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.240, 0.000, 0.010, 168.00, 1.680, 0.230, 38.64),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 4.500, 0.000, 0.500, 504.00, 252.000, 4.000, 2016.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.000, 0.000, 0.000, 252.00, 0.000, 0.000, 0.00),
    ('MIRCHI (S)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.400, 0.000, 0.000, 752.00, 0.000, 0.400, 300.80),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.100, 0.000, 0.000, 736.00, 0.000, 1.100, 809.60),
    ('GULAB JAL', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('CHANA MASALA', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('KALA CHANA', 'Kgs', 23.000, 0.000, 0.000, 78.00, 0.000, 23.000, 1794.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 1.000, 0.000, 0.000, 60.00, 0.000, 1.000, 60.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 1.000, 0.000, 0.000, 68.44, 0.000, 1.000, 68.44),
    ('KEVADA WATER', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('BIRIYANI MASALA', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('ilaychi small Gr', 'Kgs', 0.000, 0.000, 0.000, 3150.00, 0.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 0.800, 0.000, 0.100, 168.00, 16.800, 0.700, 117.60),
    ('KALI MIRCH( S)', 'Kgs', 0.124, 0.000, 0.010, 882.00, 8.820, 0.114, 100.55),
    ('MUMFALI DANA', 'Kgs', 0.000, 0.000, 0.000, 157.50, 0.000, 0.000, 0.00),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 25.600, 56.800, 7.800, 61.83, 482.282, 74.600, 4612.59),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 0.000, 0.000, 0.000, 67.20, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.100, 0.000, 0.000, 880.00, 0.000, 0.100, 88.00),
    ('SOYA BEAN BADIYA', 'kgs', 10.000, 0.000, 0.000, 94.50, 0.000, 10.000, 945.00),
    ('JAVTITRI', 'Kgs', 0.260, 0.000, 0.010, 2730.00, 27.300, 0.250, 682.50),
    ('AMCHUR PDR', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 1.000, 0.000, 1.000, 70.00, 70.000, 0.000, 0.00),
    ('AACHAR', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('CREAM', 'Kgs', 0.500, 0.000, 0.000, 220.00, 0.000, 0.500, 110.00),
    ('PARATHA MASALA', 'Kgs', 21.000, 0.000, 0.000, 10.00, 0.000, 21.000, 210.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
    ('ENO', 'Pkt', 0.000, 0.000, 0.000, 60.00, 0.000, 0.000, 0.00),
    ('EMLI', 'Pkt', 0.000, 0.000, 0.000, 45.00, 0.000, 0.000, 0.00),
    ('RICE (cheaper)', 'Kgs', 0.000, 0.000, 0.000, 30.00, 0.000, 0.000, 0.00),
    ('EMLI (expensive)', 'Pkt', 1.000, 0.000, 0.000, 120.00, 0.000, 1.000, 120.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 887, 0, 142, 3.186, 452.41, 745, 2373.57),
    ("FOIL BOX (RICE,SABJI)", "Nos", 2276, 0, 284, 1.575, 447.30, 1992, 3137.40),
    ("ROTI POUCH", "Nos", 1000, 0, 900, 0.236, 212.40, 100, 23.60),
    ("SALAD PKT", "Nos", 4130, 0, 284, 0.177, 50.27, 3846, 680.74),
    ("SPOON/MINI MEAL", "Nos", 769, 0, 142, 0.504, 71.57, 627, 316.01),
    ("NEPKIN TUSSU PEPAR", "Nos", 7955, 0, 142, 0.354, 50.27, 7813, 2765.80),
    ("SALT POUCH", "Nos", 1108, 0, 142, 0.150, 21.30, 966, 144.90),
    ("PICKLE & PARATHA", "Nos", 5662, 0, 142, 0.896, 127.21, 5520, 4945.00),
    ("TAPE", "Nos", 3, 0, 1, 23.600, 23.60, 0, 0.00),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 46, 0, 18, 3.150, 56.70, 28, 88.20),
    ("PAPER BOX (LUNCH)", "Nos", 557, 0, 142, 4.956, 703.75, 415, 2056.74),
    ("BUTTER ROTI PAPER", "Nos", 800, 0, 100, 0.236, 23.60, 700, 165.20),
    ("PARATHA BOX", "Nos", 420, 0, 0, 3.360, 0.00, 420, 1411.20),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 0, 0, 0, 141.600, 0.00, 0, 0.00),
    ("400 ML PP BOX", "Nos", 87, 0, 18, 4.720, 84.96, 69, 325.68),
    ("SILVER FOIL", "Kgs", 2.900, 0, 0.000, 708.000, 0.00, 2.900, 2053.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 0.000, 3.000, 3.000, 280.00, 840.00, 0.000, 0.00),
    ("PETHA", "KGS", 0.000, 0, 0.000, 150.00, 0.00, 0.000, 0.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 8.000, 150.000, 20.000, 13.000, 260.00, 138.000, 1794.00),
    ("ONION", "Kgs", 63.500, 60.000, 8.500, 24.000, 204.00, 115.000, 2760.00),
    ("TOMATO", "Kgs", 2.000, 65.000, 2.000, 25.000, 50.00, 65.000, 1625.00),
    ("GINGER", "Kgs", 0.545, 6.000, 0.545, 70.000, 38.15, 6.000, 420.00),
    ("GARLIC", "Kgs", 0.080, 5.060, 0.100, 154.000, 15.40, 5.040, 776.16),
    ("PUMPKIN", "Kgs", 0.000, 0, 0.000, 17.000, 0.00, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 2.000, 6.000, 1.000, 65.000, 65.00, 7.000, 455.00),
    ("CORRENDER", "Kgs", 0.000, 2.000, 0.000, 30.000, 0.00, 2.000, 60.00),
    ("CAPSICUM", "Kgs", 0.000, 30.000, 0.000, 30.000, 0.00, 30.000, 900.00),
    ("BEANS", "Kgs", 0.000, 1.090, 1.090, 116.000, 126.44, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 1.035, 1.035, 35.000, 36.225, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 1.000, 1.000, 55.000, 55.00, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0, 0.000, 37.000, 0.00, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 90.000, 0.000, 20.000, 0.00, 90.000, 1800.00),
    ("CABBAGE", "Kgs", 0.000, 0, 0.000, 44.000, 0.00, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 0.000, 70.860, 8.860, 22.000, 194.92, 62.000, 1364.00),
    ("MATAR", "Kgs", 0.000, 0, 0.000, 100.000, 0.00, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0, 0.000, 250.000, 0.00, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0, 0.000, 198.000, 0.00, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0, 0.000, 75.000, 0.00, 0.000, 0.00),
    ("KULCHA", "Kgs", 0.000, 0, 0.000, 30.000, 0.00, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0, 0.000, 25.000, 0.00, 0.000, 0.00),
    ("PAV", "Nos", 0.000, 6.000, 6.000, 35.000, 210.00, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 142, 140, 70.0, 9800, 7667.0),
    ("MINI", 18, 17, 50.0, 850, 683.0),
    ("AMUL", 5, 5, 25.0, 125, 110.0),
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
        print("🎉 Database successfully updated for 23 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
