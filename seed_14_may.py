import sqlite3

DATE = "2026-05-14"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 747.000, 0.000, 68.000, 31.00, 2108.000, 679.000, 21049.00),
    ("RICE", "Kgs", 497.000, 0.000, 48.000, 65.00, 3120.000, 449.000, 29185.00),
    ("R/OIL", "Ltr", 169.500, 0.000, 12.000, 180.92, 2171.077, 157.500, 28495.38),
    ("Sarso Dana", "Kgs", 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ("RAJMAH", "Kgs", 48.000, 0.000, 0.000, 115.00, 0.000, 48.000, 5520.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 31.000, 0.000, 0.000, 78.00, 0.000, 31.000, 2418.00),
    ("BESAN", "Kgs", 39.000, 0.000, 2.000, 94.50, 189.000, 37.000, 3496.50),
    ("DAL ARHAR", "Kgs", 44.000, 0.000, 0.000, 120.00, 0.000, 44.000, 5280.00),
    ("DAL MASOOR (S)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("URD CRD(CHILKA)", "KGS", 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ("MASUR CRD(Malika)", "Kgs", 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ("MOONG Crd(Chilka)", "Kgs", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 0.250, 0.000, 0.050, 315.00, 15.750, 0.200, 63.00),
    ("HALDI PDR", "Kgs", 2.500, 0.000, 0.300, 231.00, 69.300, 2.200, 508.20),
    ("MIRCHI PDR", "Kgs", 2.600, 0.000, 0.300, 315.00, 94.500, 2.300, 724.50),
    ("DAL CHINI", "Kgs", 0.350, 0.000, 0.020, 357.00, 7.140, 0.330, 117.81),
    ("LAUNG", "Kgs", 0.220, 0.000, 0.020, 1155.00, 23.100, 0.200, 231.00),
    ("HING", "Nos", 15.000, 0.000, 1.000, 89.25, 89.250, 14.000, 1249.50),
    ("KITCHEN KING", "Kgs", 1.000, 0.000, 0.200, 800.00, 160.000, 0.800, 640.00),
    ("DEGI MIRCH", "Kgs", 1.100, 0.000, 0.200, 960.00, 192.000, 0.900, 864.00),
    ("KASURI METHI", "Kgs", 0.450, 0.000, 0.050, 336.00, 16.800, 0.400, 134.40),
    ("GARAM MASALA", "Kgs", 0.800, 0.000, 0.200, 920.00, 184.000, 0.600, 552.00),
    ("SALT", "Kgs", 30.000, 0.000, 4.000, 28.00, 112.000, 26.000, 728.00),
    ("DANIYA (S)", "Kgs", 0.950, 0.000, 0.040, 157.50, 6.300, 0.910, 143.33),
    ("JEERA PDR", "Kgs", 0.200, 0.000, 0.200, 420.00, 84.000, 0.000, 0.00),
    ("CHANA MASALA (Pkt)", "Pkt", 0.800, 0.000, 0.400, 736.01, 294.405, 0.400, 294.41),
    ("B ELAICHI", "Kgs", 0.220, 0.000, 0.030, 1995.00, 59.850, 0.190, 379.05),
    ("METHI DANA", "Kgs", 0.110, 0.000, 0.010, 105.00, 1.050, 0.100, 10.50),
    ("RAJMA MASALA", "Pkt", 0.000, 0.000, 0.000, 72.00, 0.000, 0.000, 0.00),
    ("TEJ PATTA", "Kgs", 0.420, 0.000, 0.010, 168.00, 1.680, 0.410, 68.88),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 16.000, 0.000, 2.000, 504.00, 1008.000, 14.000, 7056.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ("AJWAIN", "Pkt", 0.520, 0.000, 0.050, 252.00, 12.600, 0.470, 118.44),
    ("MIRCHI (S)", "Kgs", 0.150, 0.000, 0.050, 315.00, 15.750, 0.100, 31.50),
    ("CHAT MASALA", "Kgs", 0.900, 0.000, 0.100, 752.00, 75.200, 0.800, 601.60),
    ("RAJMAH MASALA (Kgs)", "Kgs", 1.600, 0.000, 0.000, 736.00, 0.000, 1.600, 1177.60),
    ("GULAB JAL", "BTL", 5.000, 0.000, 1.000, 66.15, 66.152, 4.000, 264.61),
    ("CHANA MASALA", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 58.000, 0.000, 17.000, 78.00, 1326.000, 41.000, 3198.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 9.000, 0.000, 0.000, 60.00, 0.000, 9.000, 540.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 6.000, 0.000, 1.000, 70.80, 70.800, 5.000, 354.00),
    ("BIRIYANI MASALA", "Pkt", 7.000, 0.000, 3.000, 73.50, 220.500, 4.000, 294.00),
    ("ilaychi small Gr", "Kgs", 0.060, 0.000, 0.020, 3150.00, 63.000, 0.040, 126.00),
    ("DHANIYA PDR", "Kgs", 3.200, 0.000, 0.300, 168.00, 50.400, 2.900, 487.20),
    ("KALI MIRCH( S)", "Kgs", 0.320, 0.000, 0.020, 882.00, 17.640, 0.300, 264.60),
    ("MUMFALI DANA", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 49.100, 0.000, 28.200, 61.83, 1743.634, 20.900, 1292.27),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("SOYA BEAN BADIYA", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.500, 0.000, 0.020, 2730.00, 54.600, 0.480, 1310.40),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 5.000, 0.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("SABJI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 4.000, 0.000, 1.000, 147.00, 147.000, 3.000, 441.00),
    ("CREAM", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("PARATHA MASALA", "Kgs", 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2834, 0, 543, 3.186, 1730.00, 2291, 7299.13),
    ("FOIL BOX (RICE,SABJI)", "Nos", 4966, 0, 1086, 1.575, 1710.45, 3880, 6111.00),
    ("ROTI POUCH", "Nos", 19200, 0, 2800, 0.236, 660.80, 16400, 3870.40),
    ("SALAD PKT", "Nos", 5796, 0, 1086, 0.177, 192.22, 4710, 833.67),
    ("SPOON/MINI MEAL", "Nos", 1964, 0, 604, 0.504, 304.42, 1360, 685.44),
    ("NEPKIN TUSSU PEPAR", "Nos", 7934, 0, 611, 0.354, 216.29, 7323, 2592.34),
    ("SALT POUCH", "Nos", 1941, 0, 543, 0.150, 81.45, 1398, 209.70),
    ("PICKLE & PARATHA", "Nos", 3935, 0, 611, 0.896, 547.35, 3324, 2977.75),
    ("TAPE", "Nos", 6, 0, 1, 23.600, 23.60, 5, 118.00),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 186, 0, 61, 3.150, 192.15, 125, 393.75),
    ("PAPER BOX (LUNCH)", "Nos", 3290, 0, 543, 4.956, 2691.11, 2747, 13614.13),
    ("BUTTER ROTI PAPER", "NOS", 1700, 0, 50, 0.236, 11.80, 1650, 389.40),
    ("PARATHA BOX", "Nos", 908, 0, 68, 3.360, 228.48, 840, 2822.40),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 3, 0, 2, 141.600, 283.20, 1, 141.60),
    ("400 ML PP BOX", "Nos", 166, 0, 0, 4.720, 0.00, 166, 783.52),
    ("SILVER FOIL", "Kgs", 3.5, 0, 0.600, 708.000, 424.80, 2.900, 2053.20),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 2.000, 0, 0.000, 280.00, 0.00, 2.000, 560.00),
    ("PETHA", "KGS", 15.000, 0, 15.000, 150.00, 2250.00, 0.000, 0.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 30.000, 47.000, 61.000, 10.000, 610.000, 16.000, 160.00),
    ("ONION", "Kgs", 82.000, 0.000, 14.000, 22.000, 308.000, 68.000, 1496.00),
    ("TOMATO", "Kgs", 27.000, 0.000, 14.000, 16.000, 224.000, 13.000, 208.00),
    ("GINGER", "Kgs", 5.000, 0.000, 2.000, 135.000, 270.000, 3.000, 405.00),
    ("GARLIC", "Kgs", 1.480, 0.000, 0.700, 143.000, 100.100, 0.780, 111.54),
    ("PUMPKIN", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 4.020, 0.000, 2.000, 60.000, 120.000, 2.020, 121.20),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 12.000, 0.000, 12.000, 22.000, 264.000, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 10.045, 10.045, 121.000, 1215.445, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 20.280, 20.280, 35.000, 709.800, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 30.625, 30.625, 55.000, 1684.375, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 47.000, 0.000, 19.000, 20.000, 380.000, 28.000, 560.00),
    ("MATAR", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
    ("TORI", "Nos", 0.000, 10.000, 0.000, 25.000, 0.000, 10.000, 250.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 543, 540, 70.0, 37800, 29612.0),
    ("PARATHA", 68, 67, 40.0, 2680, 1819.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 61, 59, 50.0, 2950, 873.0),
    ("AMUL", 9, 9, 25.0, 225, 198.0),
    ("LAHARI JEERA", 11, 11, 10.0, 110, 99.0),
    ("LASSI", 11, 11, 20.0, 220, 209.0),
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
                    new_received = (row[1] or 0.0) + received
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
        print("🎉 Database successfully updated for 14 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
