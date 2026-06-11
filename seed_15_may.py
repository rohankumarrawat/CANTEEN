import sqlite3

DATE = "2026-05-15"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ('ATTA', 'Kgs', 679.000, 0.000, 66.000, 31.00, 2046.000, 613.000, 19003.00),
    ('RICE', 'Kgs', 449.000, 0.000, 48.000, 65.00, 3120.000, 401.000, 26065.00),
    ('R/OIL', 'Ltr', 157.500, 0.000, 11.000, 180.92, 1990.154, 146.500, 26505.23),
    ('Sarso Dana', 'Kgs', 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ('RAJMAH', 'Kgs', 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ('URD (S)', 'Kgs', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('DAL CHANA', 'Kgs', 31.000, 0.000, 13.000, 78.00, 1014.000, 18.000, 1404.00),
    ('BESAN', 'Kgs', 37.000, 0.000, 0.000, 94.50, 0.000, 37.000, 3496.50),
    ('DAL ARHAR', 'Kgs', 44.000, 0.000, 8.000, 120.00, 960.000, 36.000, 4320.00),
    ('DAL MASOOR (S)', 'Pkt', 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ('URD CRD(CHILKA)', 'KGS', 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ('MASUR CRD(Malika)', 'Kgs', 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ('MOONG Crd(Chilka)', 'Kgs', 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ('URD DHULI', 'Kgs', 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ('LOBHIYA', 'Kgs', 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ('JEERA (S)', 'Kgs', 0.200, 0.000, 0.100, 315.00, 31.500, 0.100, 31.50),
    ('HALDI PDR', 'Kgs', 2.200, 0.000, 0.600, 231.00, 138.600, 1.600, 369.60),
    ('MIRCHI PDR', 'Kgs', 2.300, 0.000, 0.500, 315.00, 157.500, 1.800, 567.00),
    ('DAL CHINI', 'Kgs', 0.330, 0.000, 0.040, 357.00, 14.280, 0.290, 103.53),
    ('LAUNG', 'Kgs', 0.200, 0.000, 0.040, 1155.00, 46.200, 0.160, 184.80),
    ('HING', 'Nos', 14.000, 0.000, 0.000, 89.25, 0.000, 14.000, 1249.50),
    ('KITCHEN KING', 'Kgs', 0.800, 0.000, 0.400, 800.00, 320.000, 0.400, 320.00),
    ('DEGI MIRCH', 'Kgs', 0.900, 0.000, 0.200, 960.00, 192.000, 0.700, 672.00),
    ('KASURI METHI', 'Kgs', 0.400, 0.000, 0.050, 336.00, 16.800, 0.350, 117.60),
    ('GARAM MASALA', 'Kgs', 0.600, 0.000, 0.200, 920.00, 184.000, 0.400, 368.00),
    ('SALT', 'Kgs', 26.000, 0.000, 4.000, 28.00, 112.000, 22.000, 616.00),
    ('DANIYA (S)', 'Kgs', 0.910, 0.000, 0.200, 157.50, 31.500, 0.710, 111.83),
    ('JEERA PDR', 'Kgs', 0.000, 0.000, 0.000, 420.00, 0.000, 0.000, 0.00),
    ('CHANA MASALA (Pkt)', 'Pkt', 0.400, 0.000, 0.000, 736.01, 0.000, 0.400, 294.41),
    ('B ELAICHI', 'Kgs', 0.190, 0.000, 0.050, 1995.00, 99.750, 0.140, 279.30),
    ('METHI DANA', 'Kgs', 0.100, 0.000, 0.000, 105.00, 0.000, 0.100, 10.50),
    ('RAJMA MASALA', 'Pkt', 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ('TEJ PATTA', 'Kgs', 0.420, 0.000, 0.050, 168.00, 8.400, 0.370, 62.16),
    ('AJINO MOTO', 'Kgs', 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ('DESI GHEE', 'Kgs', 14.000, 0.000, 2.000, 504.00, 1008.000, 12.000, 6048.00),
    ('SARSOO', 'Kgs', 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ('CLEAN WRAP', 'Pkt', 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ('AJWAIN', 'Pkt', 0.470, 0.000, 0.100, 252.00, 25.200, 0.370, 93.24),
    ('MIRCHI (S)', 'Kgs', 0.100, 0.000, 0.100, 315.00, 31.500, 0.000, 0.00),
    ('CHAT MASALA', 'Kgs', 0.800, 0.000, 0.100, 752.00, 75.200, 0.700, 526.40),
    ('RAJMAH MASALA (Kgs)', 'Kgs', 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
    ('GULAB JAL', 'BTL', 4.000, 0.000, 0.000, 66.15, 0.000, 4.000, 264.61),
    ('CHANA MASALA', 'Kgs', 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ('KALA CHANA', 'Kgs', 41.000, 0.000, 0.000, 78.00, 0.000, 41.000, 3198.00),
    ('VINAYGER', 'BTL', 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ('RED CHILLI SAUCE', 'BTL', 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ('MATAR PANEER MASALA', 'BTL', 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ('PAV BHAJI MASALA', 'BTL', 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ('MATAR TF', 'Kgs', 9.000, 0.000, 4.000, 60.00, 240.000, 5.000, 300.00),
    ('STAR FOOL MASALA', 'Kgs', 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ('FOOD COLOUR', 'PKT', 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ('KEVADA WATER', 'BTL', 5.000, 0.000, 0.000, 70.80, 0.000, 5.000, 354.00),
    ('BIRIYANI MASALA', 'Pkt', 4.000, 0.000, 0.000, 73.50, 0.000, 4.000, 294.00),
    ('ilaychi small Gr', 'Kgs', 0.040, 0.000, 0.040, 3150.00, 126.000, 0.000, 0.00),
    ('DHANIYA PDR', 'Kgs', 2.900, 0.000, 0.400, 168.00, 67.200, 2.500, 420.00),
    ('KALI MIRCH( S)', 'Kgs', 0.300, 0.000, 0.020, 882.00, 17.640, 0.280, 246.96),
    ('MUMFALI DANA', 'Kgs', 13.000, 0.000, 4.000, 157.50, 630.000, 9.000, 1417.50),
    ('SAMBHAR MASALA', 'Pkt', 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ('LPG', 'Kgs', 20.900, 28.400, 20.900, 61.83, 1292.268, 28.400, 1756.00),
    ('RAI', 'Pkt', 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ('SUGAR', 'kgs', 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ('BAKING PDR', 'PKT', 1.000, 0.000, 0.000, 67.20, 0.000, 1.000, 67.20),
    ('SAHI PANEER MASALA (Pkt)', 'PKT', 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ('SAHI PANEER MASALA (Kgs)', 'kgs', 1.400, 0.000, 0.500, 880.00, 440.000, 0.900, 792.00),
    ('SOYA BEAN BADIYA', 'kgs', 0.000, 0.000, 0.000, 94.50, 0.000, 0.000, 0.00),
    ('JAVTITRI', 'Kgs', 0.480, 0.000, 0.070, 2730.00, 191.100, 0.410, 1119.30),
    ('AMCHUR PDR', 'Pkt', 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ('DAL MAKHANI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('BLACK PEPPER PDR', 'Pkt', 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ('SABJI MASALA', 'Pkt', 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ('AACHAR', 'Kgs', 3.000, 0.000, 0.000, 147.00, 0.000, 3.000, 441.00),
    ('CREAM', 'Kgs', 5.500, 0.000, 2.000, 220.00, 440.000, 3.500, 770.00),
    ('PARATHA MASALA', 'Kgs', 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ('KHAS KHAS', 'PKT', 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ('GUD', 'Kgs', 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2291, 0, 1046, 3.186, 3332.56, 1245, 3966.57),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3880, 0, 643, 1.575, 1012.73, 3237, 5098.28),
    ("ROTI POUCH", "Nos", 16400, 0, 2900, 0.236, 684.40, 13500, 3186.00),
    ("SALAD PKT", "Nos", 4710, 0, 1086, 0.177, 192.22, 3624, 641.45),
    ("SPOON/MINI MEAL", "Nos", 1360, 0, 543, 0.504, 273.67, 817, 411.77),
    ("NEPKIN TUSSU PEPAR", "Nos", 7323, 0, 616, 0.354, 218.06, 6707, 2374.28),
    ("SALT POUCH", "Nos", 1398, 0, 543, 0.150, 81.45, 855, 128.25),
    ("PICKLE & PARATHA", "Nos", 3324, 0, 616, 0.896, 551.83, 2708, 2425.92),
    ("TAPE", "Nos", 5, 0, 2, 23.600, 47.20, 3, 70.80),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 125, 0, 60, 3.150, 189.00, 65, 204.75),
    ("PAPER BOX (LUNCH)", "Nos", 2747, 0, 543, 4.956, 2691.11, 2204, 10923.02),
    ("BUTTER ROTI PAPER", "NOS", 1650, 0, 250, 0.236, 59.00, 1400, 330.40),
    ("PARATHA BOX", "Nos", 840, 0, 73, 3.360, 245.28, 767, 2577.12),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 0, 1, 141.600, 141.60, 0, 0.00),
    ("400 ML PP BOX", "Nos", 166, 0, 0, 4.720, 0.00, 166, 783.52),
    ("SILVER FOIL", "Kgs", 3.0, 0, 0.500, 708.000, 354.00, 2.400, 1699.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 2.000, 12.000, 12.000, 280.00, 3360.00, 2.000, 560.00),
    ("PETHA", "KGS", 0.000, 0, 0.000, 150.00, 0.00, 0.000, 0.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 16.000, 0.000, 0.000, 10.000, 0.000, 16.000, 160.00),
    ("ONION", "Kgs", 68.000, 0.000, 14.000, 22.000, 308.000, 54.000, 1188.00),
    ("TOMATO", "Kgs", 13.000, 0.000, 11.000, 16.000, 176.000, 2.000, 32.00),
    ("GINGER", "Kgs", 3.000, 0.000, 2.000, 135.000, 270.000, 1.000, 135.00),
    ("GARLIC", "Kgs", 0.780, 0.000, 0.500, 143.000, 71.500, 0.280, 40.04),
    ("PUMPKIN", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 2.020, 0.000, 1.600, 60.000, 96.000, 0.420, 25.20),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0.000, 0.000, 22.000, 0.000, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 121.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 28.000, 0.000, 23.000, 20.000, 460.000, 5.000, 100.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 16.000, 16.000, 250.000, 4000.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 30.000, 30.000, 30.000, 900.000, 0.000, 0.00),
    ("TORI", "Nos", 10.000, 0.000, 0.000, 25.000, 0.000, 10.000, 250.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800, 31136.0),
    ("PARATHA", 73, 72, 40.0, 2880, 1716.0),
    ("DAHI", 120, 119, 10.0, 1190, 1071.0),
    ("CHACH", 320, 314, 10.0, 3140, 2826.0),
    ("MINI", 60, 59, 50.0, 2950, 1930.0),
    ("AMUL", 11, 11, 25.0, 275, 242.0),
    ("LAHARI JEERA", 11, 11, 10.0, 110, 99.0),
    ("LASSI", 15, 15, 20.0, 300, 285.0),
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
        print("🎉 Database successfully updated for 15 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
