import sqlite3

DATE = "2026-05-20"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 461.000, 0.000, 66.000, 31.00, 2046.000, 395.000, 12245.00),
    ('RICE', 'Kgs', 296.000, 0.000, 46.000, 65.00, 2990.000, 250.000, 16250.00),
    ('R/OIL', 'Ltr', 118.500, 0.000, 11.000, 180.92, 1990.154, 107.500, 19449.23),
    ('Sarso Dana', 'Kgs', 0.200, 0.000, 0.000, 105.00, 0.000, 0.200, 21.00),
    ('RAJMAH', 'Kgs', 48.000, 0.000, 17.000, 115.00, 1955.000, 31.000, 3565.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 10.000, 0.000, 0.000, 78.00, 0.000, 10.000, 780.00),
    ('BESAN', 'Kgs', 24.000, 0.000, 0.000, 94.50, 0.000, 24.000, 2268.00),
    ('DAL ARHAR', 'Kgs', 33.000, 0.000, 0.000, 120.00, 0.000, 33.000, 3960.00),
    ('DAL MASOOR (S)', 'Pkt', 7.000, 0.000, 0.000, 85.00, 0.000, 7.000, 595.00),
    ('URD CRD(CHILKA)', 'KGS', 3.000, 0.000, 0.000, 110.00, 0.000, 3.000, 330.00),
    ('MASUR CRD(Malika)', 'Kgs', 3.000, 0.000, 0.000, 85.00, 0.000, 3.000, 255.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('HALDI PDR', 'Kgs', 0.700, 0.000, 0.400, 231.00, 92.400, 0.300, 69.30),
    ('MIRCHI PDR', 'Kgs', 1.100, 0.000, 0.300, 315.00, 94.500, 0.800, 252.00),
    ('DAL CHINI', 'Kgs', 0.240, 0.000, 0.040, 357.00, 14.280, 0.200, 71.40),
    ('LAUNG', 'Kgs', 0.110, 0.000, 0.040, 1155.00, 46.200, 0.070, 80.85),
    ('HING', 'Nos', 9.000, 0.000, 0.000, 89.25, 0.000, 9.000, 803.25),
    ('KITCHEN KING', 'Kgs', 0.100, 0.000, 0.000, 800.00, 0.000, 0.100, 80.00),
    ('DEGI MIRCH', 'Kgs', 0.100, 0.000, 0.000, 960.00, 0.000, 0.100, 96.00),
    ('KASURI METHI', 'Kgs', 0.200, 0.000, 0.050, 336.00, 16.800, 0.150, 50.40),
    ('GARAM MASALA', 'Kgs', 0.000, 0.000, 0.000, 920.00, 0.000, 0.000, 0.00),
    ('SALT', 'Kgs', 11.000, 0.000, 4.000, 28.00, 112.000, 7.000, 196.00),
    ('DANIYA (S)', 'Kgs', 0.510, 0.000, 0.100, 157.50, 15.750, 0.410, 64.57),
    ('JEERA PDR', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('B ELAICHI', 'Kgs', 0.090, 0.000, 0.030, 1995.00, 59.850, 0.060, 119.70),
    ('METHI DANA', 'Kgs', 0.000, 0.000, 0.000, 105.00, 0.000, 0.000, 0.00),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.320, 0.000, 0.030, 168.00, 5.040, 0.290, 48.72),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 8.000, 0.000, 1.000, 504.00, 504.000, 7.000, 3528.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.200, 0.000, 0.100, 252.00, 25.200, 0.100, 25.20),
    ('MIRCHI (S)', 'Kgs', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.500, 0.000, 0.100, 752.00, 75.200, 0.400, 300.80),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.600, 0.000, 0.500, 736.00, 368.000, 1.100, 809.60),
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
    ('DHANIYA PDR', 'Kgs', 1.800, 0.000, 0.400, 168.00, 67.200, 1.400, 235.20),
    ('KALI MIRCH( S)', 'Kgs', 0.220, 0.000, 0.036, 882.00, 31.752, 0.184, 162.29),
    ('MUMFALI DANA', 'Kgs', 9.000, 0.000, 4.000, 157.50, 630.000, 5.000, 787.50),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 88.600, 0.000, 26.400, 61.83, 1632.338, 62.200, 3845.89),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 0.000, 0.000, 0.000, 67.20, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 0.900, 0.000, 0.400, 880.00, 352.000, 0.500, 440.00),
    ('SOYA BEAN BADIYA', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.350, 0.000, 0.040, 2730.00, 109.200, 0.310, 846.30),
    ('AMCHUR PDR', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('AACHAR', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('CREAM', 'Kgs', 3.500, 0.000, 1.000, 220.00, 220.000, 2.500, 550.00),
    ('PARATHA MASALA', 'Kgs', 2.000, 0.000, 1.000, 10.00, 10.000, 1.000, 10.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2999, 0, 443, 3.186, 1411.40, 2556, 8143.42),
    ("FOIL BOX (RICE,SABJI)", "Nos", 4781, 0, 886, 1.575, 1395.45, 3895, 6134.63),
    ("ROTI POUCH", "Nos", 7300, 0, 2700, 0.236, 637.20, 4600, 1085.60),
    ("SALAD PKT", "Nos", 7168, 0, 886, 0.177, 156.82, 6282, 1111.91),
    ("SPOON/MINI MEAL", "Nos", 2465, 0, 502, 0.504, 253.01, 1963, 989.35),
    ("NEPKIN TUSSU PEPAR", "Nos", 9678, 0, 502, 0.354, 177.71, 9176, 3248.30),
    ("SALT POUCH", "Nos", 2627, 0, 443, 0.150, 66.45, 2184, 327.60),
    ("PICKLE & PARATHA", "Nos", 7385, 0, 502, 0.896, 449.71, 6883, 6166.02),
    ("TAPE", "Nos", 7, 0, 2, 23.600, 47.20, 5, 118.00),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 223, 0, 59, 3.150, 185.85, 164, 516.60),
    ("PAPER BOX (LUNCH)", "Nos", 976, 0, 443, 4.956, 2195.51, 533, 2641.55),
    ("BUTTER ROTI PAPER", "NOS", 1200, 0, 100, 0.236, 23.60, 1100, 259.60),
    ("PARATHA BOX", "Nos", 624, 0, 59, 3.360, 198.24, 565, 1898.40),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 2, 0, 1, 141.600, 141.60, 1, 141.60),
    ("400 ML PP BOX", "Nos", 204, 0, 59, 4.720, 278.48, 145, 684.40),
    ("SILVER FOIL", "Kgs", 4.900, 0, 0.500, 708.000, 354.00, 4.400, 3115.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 24.000, 0, 12.000, 280.00, 3360.00, 12.000, 3360.00),
    ("PETHA", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 124.000, 0, 65.000, 10.000, 650.000, 59.000, 590.00),
    ("ONION", "Kgs", 69.500, 50.000, 22.000, 22.000, 484.000, 97.500, 2145.00),
    ("TOMATO", "Kgs", 18.000, 0, 12.000, 25.000, 300.000, 6.000, 150.00),
    ("GINGER", "Kgs", 2.000, 0, 1.000, 85.000, 85.000, 1.000, 85.00),
    ("GARLIC", "Kgs", 0.980, 2.600, 2.000, 154.000, 308.000, 1.580, 243.32),
    ("PUMPKIN", "Kgs", 0.000, 4.500, 0.000, 17.000, 0.000, 4.500, 76.50),
    ("GREEN CHILLI", "Kgs", 0.000, 6.060, 2.000, 61.000, 122.000, 4.060, 247.66),
    ("CORRENDER", "Kgs", 0.000, 0, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 8.000, 0, 0.000, 18.000, 0.000, 8.000, 144.00),
    ("BEANS", "Kgs", 0.000, 1.945, 1.945, 121.000, 235.345, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 2.810, 2.810, 35.000, 98.350, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 3.090, 3.090, 55.000, 169.950, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 14.860, 15.200, 26.200, 23.000, 602.600, 3.860, 88.78),
    ("MATAR", "Kgs", 0.000, 0, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 0, 0.000, 25.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 443, 440, 70.0, 30800, 24780.0),
    ("PARATHA", 59, 57, 40.0, 2280, 2023.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 193, 10.0, 1930, 1737.0),
    ("MINI", 59, 58, 50.0, 2900, 1144.0),
    ("AMUL", 1, 1, 25.0, 25, 22.0),
    ("LAHARI JEERA", 10, 0, 10.0, 0, 0.0),
    ("LASSI", 10, 0, 20.0, 0, 0.0),
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
        print("🎉 Database successfully updated for 20 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
