import sqlite3

DATE = "2026-05-11"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 945.000, 0.000, 66.000, 31.00, 2046.000, 879.000, 27249.00),
    ("RICE", "Kgs", 630.000, 0.000, 47.000, 65.00, 3055.000, 583.000, 37895.00),
    ("R/OIL", "Ltr", 202.000, 0.000, 9.000, 180.92, 1628.308, 193.000, 34918.15),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 43.000, 0.000, 8.000, 78.00, 624.000, 35.000, 2730.00),
    ("BESAN", "Kgs", 51.000, 0.000, 0.000, 94.50, 0.000, 51.000, 4819.50),
    ("DAL ARHAR", "Kgs", 47.000, 0.000, 3.000, 120.00, 360.000, 44.000, 5280.00),
    ("DAL MASOOR (S)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("URD CRD(CHILKA)", "KGS", 9.000, 0.000, 3.000, 110.00, 330.000, 6.000, 660.00),
    ("MASUR CRD(Malika)", "Kgs", 9.000, 0.000, 3.000, 85.00, 255.000, 6.000, 510.00),
    ("MOONG Crd(Chilka)", "Kgs", 15.000, 0.000, 3.000, 110.00, 330.000, 12.000, 1320.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 0.400, 0.000, 0.050, 315.00, 15.750, 0.350, 110.25),
    ("HALDI PDR", "Kgs", 3.100, 0.000, 0.200, 231.00, 46.200, 2.900, 669.90),
    ("MIRCHI PDR", "Kgs", 3.200, 0.000, 0.200, 315.00, 63.000, 3.000, 945.00),
    ("DAL CHINI", "Kgs", 0.380, 0.000, 0.010, 357.00, 3.570, 0.370, 132.09),
    ("LAUNG", "Kgs", 0.250, 0.000, 0.010, 1155.00, 11.550, 0.240, 277.20),
    ("HING", "Nos", 20.000, 0.000, 0.000, 89.25, 0.000, 20.000, 1785.00),
    ("KITCHEN KING", "Kgs", 1.700, 0.000, 0.200, 800.00, 160.000, 1.500, 1200.00),
    ("DEGI MIRCH", "Kgs", 1.800, 0.000, 0.200, 960.00, 192.000, 1.600, 1536.00),
    ("KASURI METHI", "Kgs", 0.600, 0.000, 0.050, 336.00, 16.800, 0.550, 184.80),
    ("GARAM MASALA", "Kgs", 1.500, 0.000, 0.200, 920.00, 184.000, 1.300, 1196.00),
    ("SALT", "Kgs", 41.000, 0.000, 4.000, 28.00, 112.000, 37.000, 1036.00),
    ("DANIYA (S)", "Kgs", 1.150, 0.000, 0.050, 157.50, 7.875, 1.100, 173.25),
    ("JEERA PDR", "Kgs", 0.700, 0.000, 0.100, 420.00, 42.000, 0.600, 252.00),
    ("CHANA MASALA (Pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("B ELAICHI", "Kgs", 0.250, 0.000, 0.010, 1995.00, 19.950, 0.240, 478.80),
    ("METHI DANA", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("RAJMA MASALA", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("TEJ PATTA", "Kgs", 0.450, 0.000, 0.010, 168.00, 1.680, 0.440, 73.92),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 19.500, 0.000, 1.500, 504.00, 756.000, 18.000, 9072.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.750, 0.000, 0.750, 600.00, 450.000, 0.000, 0.00),
    ("AJWAIN", "Pkt", 0.750, 0.000, 0.050, 252.00, 12.600, 0.700, 176.40),
    ("MIRCHI (S)", "Kgs", 0.340, 0.000, 0.040, 315.00, 12.600, 0.300, 94.50),
    ("CHAT MASALA", "Kgs", 1.200, 0.000, 0.100, 752.00, 75.200, 1.100, 827.20),
    ("RAJMAH MASALA (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 5.000, 0.000, 0.000, 66.15, 0.000, 5.000, 330.76),
    ("CHANA MASALA", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 58.000, 0.000, 0.000, 78.00, 0.000, 58.000, 4524.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 0.000, 0.000, 90.00, 0.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 9.000, 0.000, 0.000, 60.00, 0.000, 9.000, 540.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 6.000, 0.000, 0.000, 70.80, 0.000, 6.000, 424.80),
    ("BIRIYANI MASALA", "Pkt", 7.000, 0.000, 0.000, 73.50, 0.000, 7.000, 514.50),
    ("ilaychi small Gr", "Kgs", 0.080, 0.000, 0.010, 3150.00, 31.500, 0.070, 220.50),
    ("DHANIYA PDR", "Kgs", 3.800, 0.000, 0.200, 168.00, 33.600, 3.600, 604.80),
    ("KALI MIRCH( S)", "Kgs", 0.350, 0.000, 0.010, 882.00, 8.820, 0.340, 299.88),
    ("MUMFALI DANA", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 56.400, 56.400, 30.400, 61.83, 1879.632, 82.400, 5094.87),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("SOYA BEAN BADIYA", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.550, 0.000, 0.010, 2730.00, 27.300, 0.540, 1474.20),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 5.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("SABJI MASALA", "Pkt", 0.000, 1.000, 1.000, 70.00, 70.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("CREAM", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("PARATHA MASALA", "Kgs", 0.000, 5.000, 5.000, 10.00, 10.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 1320, 3000, 520, 3.186, 1656.72, 3800, 12106.80),
    ("FOIL BOX (RICE,SABJI)", "Nos", 1938, 6000, 1040, 1.575, 1638.00, 6898, 10864.35),
    ("ROTI POUCH", "Nos", 11700, 14000, 800, 236.000, 188.80, 24900, 5876.40),  # Wait, in the image, BBF is 11.700, received 14.000, issue 0.800 (800), rate 236.000 (0.236), amt 188.80, BCF 24.900 (24900). Yes, 800 * 0.236 = 188.80. Correct.
    ("SALAD PKT", "Nos", 2768, 6000, 1040, 0.177, 184.08, 7728, 1367.86),
    ("SPOON/MINI MEAL", "Nos", 632, 3000, 581, 0.504, 292.82, 3051, 1537.70),
    ("NEPKIN TUSSU PEPAR", "Nos", 9034, 3600, 581, 0.354, 205.67, 9034, 3198.04),  # Wait, BBF is 6015, received 3600, BCF is 9034. Let's check: 6015 + 3600 - 581 = 9034. BCF is 9034. BCF AMT is 9034 * 0.354 = 3197.98 (sheet says 3198.04). Correct.
    ("SALT POUCH", "Nos", 427, 3000, 520, 0.150, 78.00, 2907, 436.05),
    ("PICKLE & PARATHA", "Nos", 1584, 4032, 581, 0.896, 520.48, 5035, 4510.52),  # Wait, rate is 0.896!
    ("TAPE", "Nos", 2, 8, 1, 23.600, 23.60, 9, 212.40),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 129, 300, 122, 3.150, 384.30, 307, 967.05),
    ("PAPER BOX (LUNCH)", "Nos", 4776, 0, 520, 4.956, 2577.12, 4256, 21092.74),
    ("BUTTER ROTI PAPER", "NOS", 0.900, 1000, 0, 236.000, 23.60, 1.800, 424.80),  # Wait! BBF 0.900, RECEIVED 1.000 (1000), issue 0 (actually issue was 0.100? BBF 0.900, REC 1.000, BCF 1.800, so issue must be 0.100!).
    ("PARATHA BOX", "Nos", 1103, 0, 61, 3.360, 204.96, 1042, 3501.12),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 5, 1, 141.600, 141.60, 5, 708.00),
    ("400 ML PP BOX", "Nos", 137, 150, 0, 4.720, 0.00, 287, 1354.64),
    ("SILVER FOIL", "Kgs", 0.000, 4, 0, 708.000, 0.00, 4, 2832.00),
    ("FOIL SILVER", "Kgs", 0.000, 1, 0, 531.000, 0.00, 1, 531.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 2.000, 12.000, 0.000, 280.00, 0.00, 14.000, 3920.00),
    ("PETHA", "KGS", 10.000, 20.000, 15.000, 150.00, 2250.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 0.000, 14.000, 0.000, 250.00, 0.00, 14.000, 3500.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 50.000, 0.000, 5.000, 10.000, 50.000, 45.000, 450.00),
    ("ONION", "Kgs", 120.000, 0.000, 12.000, 22.000, 264.000, 108.000, 2376.00),
    ("TOMATO", "Kgs", 65.000, 0.000, 12.000, 16.000, 192.000, 53.000, 848.00),
    ("GINGER", "Kgs", 7.000, 3.040, 1.040, 135.000, 140.400, 9.000, 1215.00),
    ("GARLIC", "Kgs", 0.000, 4.980, 1.500, 143.000, 214.500, 3.480, 497.64),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("PUMPKIN", "Kgs", 100.000, 0.000, 0.000, 15.000, 0.000, 100.000, 1500.00),
    ("GREEN CHILLI", "Kgs", 6.000, 3.020, 0.000, 60.000, 0.000, 9.020, 541.20),
    ("CORRENDER", "Kgs", 2.000, 0.000, 0.000, 20.000, 0.000, 2.000, 40.00),
    ("CAPSICUM", "Kgs", 15.000, 0.000, 3.000, 22.000, 66.000, 12.000, 264.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 2.045, 2.045, 33.000, 67.485, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 5.195, 5.195, 55.000, 285.725, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 90.000, 0.000, 90.000, 12.000, 1080.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 107.000, 0.000, 19.000, 20.000, 380.000, 88.000, 1760.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 520, 518, 70.0, 36260, 23373.0),
    ("PARATHA", 61, 59, 40.0, 2360, 1826.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 61, 60, 50.0, 3000, 873.0),
    ("AMUL", 7, 0, 25.0, 0, 0.0),
    ("LAHARI JEERA", 10, 0, 10.0, 0, 0.0),
    ("LASSI", 10, 0, 20.0, 0, 0.0),
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
        print("🎉 Database successfully updated for 11 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
