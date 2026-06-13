import sqlite3

DATE = "2026-04-30"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 1367.000, 0.000, 66.000, 31.00, 2046.000, 1301.000, 40331.00),
    ("RICE", "Kgs", 909.000, 0.000, 46.000, 65.00, 2990.000, 863.000, 56095.00),
    ("R/OIL", "Ltr", 275.000, 0.000, 9.000, 180.92, 1628.308, 266.000, 48125.54),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 83.000, 0.000, 0.000, 115.00, 0.000, 83.000, 9545.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 70.000, 0.000, 0.000, 78.00, 0.000, 70.000, 5460.00),
    ("BESAN", "Kgs", 70.000, 0.000, 0.000, 94.50, 0.000, 70.000, 6615.00),
    ("DAL ARHAR", "Kgs", 58.000, 0.000, 0.000, 120.00, 0.000, 58.000, 6960.00),
    ("DAL MASOOR (S)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("URD CRD(CHILKA)", "KGS", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("MASUR CRD(Malika)", "Kgs", 16.000, 0.000, 0.000, 85.00, 0.000, 16.000, 1360.00),
    ("MOONG Crd(Chilka)", "Kgs", 18.000, 0.000, 0.000, 110.00, 0.000, 18.000, 1980.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 2.000, 0.000, 0.200, 315.00, 63.000, 1.800, 567.00),
    ("HALDI PDR", "Kgs", 5.000, 0.000, 0.200, 231.00, 46.200, 4.800, 1108.80),
    ("MIRCHI PDR", "Kgs", 5.100, 0.000, 0.200, 315.00, 63.000, 4.900, 1543.50),
    ("DAL CHINI", "Kgs", 0.460, 0.000, 0.010, 357.00, 3.570, 0.450, 160.65),
    ("LAUNG", "Kgs", 0.330, 0.000, 0.010, 1155.00, 11.550, 0.320, 369.60),
    ("HING", "Nos", 26.000, 0.000, 1.000, 89.25, 89.250, 25.000, 2231.25),
    ("KITCHEN KING", "Kgs", 3.100, 0.000, 0.200, 800.00, 160.000, 2.900, 2320.00),
    ("DEGI MIRCH", "Kgs", 3.200, 0.000, 0.200, 960.00, 192.000, 3.000, 2880.00),
    ("KASURI METHI", "Kgs", 1.000, 0.000, 0.100, 336.00, 33.600, 0.900, 302.40),
    ("GARAM MASALA", "Kgs", 3.100, 0.000, 0.200, 920.00, 184.000, 2.900, 2668.00),
    ("SALT", "Kgs", 67.000, 0.000, 3.000, 28.00, 84.000, 64.000, 1792.00),
    ("DANIYA (S)", "Kgs", 1.800, 0.000, 0.100, 157.50, 15.750, 1.700, 267.75),
    ("JEERA PDR", "Kgs", 2.200, 0.000, 0.200, 420.00, 84.000, 2.000, 840.00),
    ("CHANA MASALA (Pkt)", "Pkt", 1.500, 0.000, 0.400, 736.01, 294.405, 1.100, 809.61),
    ("B ELAICHI", "Kgs", 0.330, 0.000, 0.010, 1995.00, 19.950, 0.320, 638.40),
    ("METHI DANA", "Kgs", 0.380, 0.000, 0.010, 105.00, 1.050, 0.370, 38.85),
    ("RAJMA MASALA", "Pkt", 6.000, 0.000, 0.000, 72.00, 0.000, 6.000, 432.00),
    ("TEJ PATTA", "Kgs", 0.540, 0.000, 0.020, 168.00, 3.360, 0.520, 87.36),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 27.000, 0.000, 1.000, 504.00, 504.000, 26.000, 13104.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CHAT MASALA (Pkt)", "Pkt", 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ("AJWAIN", "Pkt", 1.050, 0.000, 0.050, 252.00, 12.600, 1.000, 252.00),
    ("MIRCHI (S)", "Kgs", 0.750, 0.000, 0.050, 315.00, 15.750, 0.700, 220.50),
    ("CHAT MASALA (Kgs)", "Kgs", 1.800, 0.000, 0.100, 752.00, 75.200, 1.700, 1278.40),
    ("RAJMAH MASALA", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 7.000, 0.000, 1.000, 66.15, 66.152, 6.000, 396.91),
    ("CHANA MASALA (Pkt) 2", "Pkt", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 94.000, 0.000, 18.000, 78.00, 1404.000, 76.000, 5928.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 13.000, 0.000, 0.000, 60.00, 0.000, 13.000, 780.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 8.000, 0.000, 1.000, 70.80, 70.800, 7.000, 495.60),
    ("BIRIYANI MASALA", "Pkt", 14.000, 0.000, 4.000, 73.50, 294.000, 10.000, 735.00),
    ("ilaychi small Gr", "Kgs", 0.100, 0.000, 0.000, 3150.00, 0.000, 0.100, 315.00),
    ("DHANIYA PDR", "Kgs", 5.600, 0.000, 0.200, 168.00, 33.600, 5.400, 907.20),
    ("KALI MIRCH( S)", "Kgs", 0.430, 0.000, 0.010, 882.00, 8.820, 0.420, 370.44),
    ("MUMFALI DANA", "Kgs", 19.000, 0.000, 0.000, 157.50, 0.000, 19.000, 2992.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 29.800, 28.400, 26.000, 61.83, 1607.606, 32.200, 1990.96),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 6.000, 0.000, 0.000, 86.50, 0.000, 6.000, 519.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 2.000, 0.000, 0.000, 880.00, 0.000, 2.000, 1760.00),
    ("SOYA BEAN BADIYA", "kgs", 24.000, 0.000, 0.000, 94.50, 0.000, 24.000, 2268.00),
    ("JAVTITRI", "Kgs", 0.640, 0.000, 0.010, 2730.00, 27.300, 0.630, 1719.90),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 6.000, 0.000, 1.000, 147.00, 147.000, 5.000, 735.00),
    ("CREAM", "Kgs", 7.000, 0.000, 0.000, 220.00, 0.000, 7.000, 1540.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2713.0, 521.0, 3.186, 1659.91, 2192.0, 6983.71),
    ("FOIL BOX (RICE,SABJI)", "Nos", 4568.0, 1042.0, 1.575, 1641.15, 3526.0, 5553.45),
    ("ROTI POUCH", "Nos", 12.600, 3.500, 236.000, 826.00, 9.100, 2147.60),
    ("SALAD PKT", "Nos", 7398.0, 1042.0, 0.177, 184.43, 6356.0, 1125.01),
    ("SPOON/MINI MEAL", "Nos", 2250.0, 582.0, 0.504, 293.33, 1668.0, 840.67),
    ("NEPKIN TUSSU PEPAR", "Nos", 6090.0, 594.0, 0.354, 210.28, 5496.0, 1945.58),
    ("SALT POUCH", "Nos", 1242.0, 521.0, 0.150, 78.15, 721.0, 108.15),
    ("PICKLE & PARATHA", "Nos", 5330.0, 594.0, 0.899, 534.19, 4736.0, 4259.11),
    ("TAPE", "Nos", 5.0, 1.0, 23.600, 23.60, 4.0, 94.40),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 228.0, 61.0, 3.150, 192.15, 167.0, 526.05),
    ("PAPER BOX (LUNCH)", "Nos", 8091.0, 521.0, 4.956, 2582.08, 7570.0, 37516.92),
    ("BUTTER ROTI PAPER", "NOS", 0.450, 0.050, 236.000, 11.80, 0.400, 94.40),
    ("PARATHA BOX", "Nos", 1534.0, 73.0, 3.360, 245.28, 1461.0, 4908.96),
    ("PARTATION BOX", "Nos", 47.0, 0.0, 6.960, 0.00, 47.0, 327.12),
    ("BLACK PACKET", "Nos", 3.0, 1.0, 141.600, 141.60, 2.0, 283.20),
    ("400 ML PP BOX", "Nos", 277.0, 0.0, 4.720, 0.00, 277.0, 1307.44),
]

sweets_items = [
    # (name, unit, bbf, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 12.000, 0.000, 280.000, 0.00, 12.000, 3360.00),
    ("PETHA", "KGS", 20.000, 12.000, 150.000, 1800.00, 8.000, 1200.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 95.400, 0.000, 45.000, 12.000, 540.000, 50.400, 604.80),
    ("ONION", "Kgs", 46.095, 0.000, 12.000, 22.000, 264.000, 34.095, 750.09),
    ("TOMATO", "Kgs", 20.000, 0.000, 14.000, 30.000, 420.000, 6.000, 180.00),
    ("GINGER", "Kgs", 1.060, 0.000, 1.000, 65.000, 65.000, 0.060, 3.90),
    ("GARLIC", "Kgs", 0.085, 2.575, 2.000, 132.000, 264.000, 0.660, 87.12),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 1.620, 0.000, 1.000, 55.000, 55.000, 0.620, 34.10),
    ("CORRENDER", "Kgs", 1.800, 0.000, 1.000, 40.000, 40.000, 0.800, 32.00),
    ("CAPSICUM", "Kgs", 15.000, 0.000, 15.000, 18.000, 270.000, 0.000, 0.00),
    ("BEANS", "Kgs", 4.605, 0.000, 4.605, 55.000, 253.275, 0.000, 0.00),
    ("CARROT", "Kgs", 20.000, 0.000, 20.000, 33.000, 660.000, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 30.035, 0.000, 30.035, 55.000, 1651.925, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 55.000, 0.000, 17.000, 15.000, 255.000, 38.000, 570.00),
    ("MATAR", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

# (name, sp, prepared, sold, rate, income, expdr, profit)
sales_summary = [
    ("LUNCH", 70.0, 521, 520, 70.0, 36400.0, 25521.0, 10879.0),
    ("PARATHA", 40.0, 73, 72, 40.0, 2880.0, 2048.0, 832.0),
    ("DAHI", 10.0, 240, 239, 10.0, 2390.0, 2151.0, 239.0),
    ("CHACH", 10.0, 200, 195, 10.0, 1950.0, 1755.0, 195.0),
    ("MINI", 50.0, 61, 60, 50.0, 3000.0, 873.0, 2127.0),
    ("AMUL", 25.0, 5, 5, 25.0, 125.0, 110.0, 15.0),
    ("LAHARI JEERA", 10.0, 15, 15, 10.0, 150.0, 135.0, 15.0),
    ("LASSI", 20.0, 18, 18, 20.0, 360.0, 342.0, 18.0),
]

def seed_db():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()

    try:
        # 1. Clear existing transactional tables (except users, roles, user_roles)
        cursor.execute("DELETE FROM batch_prep")
        cursor.execute("DELETE FROM expenditure")
        cursor.execute("DELETE FROM goods_received")
        cursor.execute("DELETE FROM sales")
        cursor.execute("DELETE FROM stock_ledger")
        cursor.execute("DELETE FROM daily_menu")
        cursor.execute("DELETE FROM waste_tracker")
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM menu")
        cursor.execute("DELETE FROM recipes")
        cursor.execute("DELETE FROM samples")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('batch_prep','expenditure','goods_received','sales','stock_ledger','daily_menu','waste_tracker','inventory','menu','recipes','samples')")

        print("Ingesting Dry items...")
        for item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt in dry_items:
            cursor.execute('''
                INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated)
                VALUES (?, 'Dry', ?, ?, 0.0, ?, ?, ?, ?)
            ''', (item, unit, bcf, bbf, received, rate, DATE))
            inv_id = cursor.lastrowid

            # Stock ledger entries
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

        print("Ingesting Packaging items...")
        for item, unit, bbf, issue, rate, amt, bcf, bcf_amt in packaging_items:
            cursor.execute('''
                INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated)
                VALUES (?, 'Misc', ?, ?, 0.0, ?, 0.0, ?, ?)
            ''', (item, unit, bcf, bbf, rate, DATE))
            inv_id = cursor.lastrowid

            cursor.execute('''
                INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                VALUES (?, ?, 'Opening', ?, 'Opening balance BBF')
            ''', (DATE, inv_id, bbf))

            if issue > 0:
                cursor.execute('''
                    INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                    VALUES (?, ?, 'Batch_Prep', ?, 'Material used for production')
                ''', (DATE, inv_id, -issue))

        print("Ingesting Sweets items...")
        for item, unit, bbf, issue, rate, amt, bcf, bcf_amt in sweets_items:
            cursor.execute('''
                INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated)
                VALUES (?, 'Misc', ?, ?, 0.0, ?, 0.0, ?, ?)
            ''', (item, unit, bcf, bbf, rate, DATE))
            inv_id = cursor.lastrowid

            cursor.execute('''
                INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                VALUES (?, ?, 'Opening', ?, 'Opening balance BBF')
            ''', (DATE, inv_id, bbf))

            if issue > 0:
                cursor.execute('''
                    INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                    VALUES (?, ?, 'Batch_Prep', ?, 'Material used for production')
                ''', (DATE, inv_id, -issue))

        print("Ingesting Fresh vegetables...")
        for item, unit, bbf, received, issue, rate, amt, bcf, bcf_amt in fresh_items:
            cursor.execute('''
                INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated)
                VALUES (?, 'Fresh', ?, ?, 0.0, ?, ?, ?, ?)
            ''', (item, unit, bcf, bbf, received, rate, DATE))
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

        print("Ingesting sales & menu data...")
        # Flat list: (meal_name, qty, notes, given_to)
        # CHACH has 2 rows: 1 General sample + 5 Ladies
        samples_list = [
            ("LUNCH",    1, "01 X LUNCH SAMPLE",      "General"),
            ("PARATHA",  1, "01 X PARATHA SAMPLE",    "General"),
            ("MINI",     1, "01 X MINI LUNCH SAMPLE", "General"),
            ("DAHI",     1, "01 X DAHI SAMPLE",       "General"),
            ("CHACH",    1, "01 X CHACH SAMPLE",      "General"),
            ("CHACH",    5, "05 X CHACH FOR LADIES",  "Ladies"),
        ]

        for meal, sp, prepared, sold, rate, income, expdr, profit in sales_summary:
            cpu = expdr / prepared if prepared > 0 else 0.0
            cursor.execute('''
                INSERT INTO menu (name, sp, active, cogs)
                VALUES (?, ?, 1, ?)
            ''', (meal, sp, cpu))
            menu_id = cursor.lastrowid

            # Insert all sample rows for this meal
            total_sample_qty = 0
            for sml_meal, qty, notes, given_to in samples_list:
                if sml_meal == meal:
                    total_sample_qty += qty
                    cost = qty * cpu
                    cursor.execute('''
                        INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (DATE, menu_id, meal, sp, qty, cost, given_to, notes))

            # Calculate wastage excluding samples (cap at 0)
            wastage = max(0, prepared - sold - total_sample_qty)

            # Insert into sales log
            cursor.execute('''
                INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Cash')
            ''', (DATE, menu_id, meal, sp, sold, wastage, expdr))

            # Insert into batch preps
            cursor.execute('''
                INSERT INTO batch_prep (date, menu_id, qty_prepared)
                VALUES (?, ?, ?)
            ''', (DATE, menu_id, prepared))

            # Insert into expenditures
            cursor.execute('''
                INSERT INTO expenditure (date, amount, category, notes)
                VALUES (?, ?, 'Raw Materials', ?)
            ''', (DATE, expdr, f"Auto-expenditure for {meal} batch"))

        # ── Day-specific menu items & Weekly Schedule ──────────────────────────
        # Revised Menu: Monday–Saturday with specific Lunch, Paratha, Mini Meal
        day_menu_plan = [
            # (day, meal_type, menu_name, sp)
            ("Monday",    "Lunch",     "PANCHRATNA THALI",   70.0),
            ("Monday",    "Paratha",   "MIXED VEG PARANTHA", 40.0),
            ("Monday",    "Mini Meal", "TAMARIND RICE",      50.0),
            ("Tuesday",   "Lunch",     "ALOO SHIMLA THALI",  70.0),
            ("Tuesday",   "Paratha",   "FRIED ALOO PARANTHA",40.0),
            ("Tuesday",   "Mini Meal", "KADHI CHAWAL",       50.0),
            ("Wednesday", "Lunch",     "KADHAI PANEER THALI",70.0),
            ("Wednesday", "Paratha",   "MIX VEG PARANTHA",   40.0),
            ("Wednesday", "Mini Meal", "RAJMAH RICE",        50.0),
            ("Thursday",  "Lunch",     "ALOO SOYABEAN THALI",70.0),
            ("Thursday",  "Paratha",   "FRIED ALOO PARANTHA",40.0),
            ("Thursday",  "Mini Meal", "VEG BIRYANI",        50.0),
            ("Friday",    "Lunch",     "SHAHI PANEER THALI", 70.0),
            ("Friday",    "Paratha",   "DAL CHANA PARANTHA", 40.0),
            ("Friday",    "Mini Meal", "MATAR KULCHA",       50.0),
            ("Saturday",  "Lunch",     "TORI KADOO THALI",   70.0),
            ("Saturday",  "Mini Meal", "PAV BHAJJI",         50.0),
        ]

        for day, meal_type, menu_name, sp in day_menu_plan:
            cursor.execute("SELECT id FROM menu WHERE name = ? COLLATE NOCASE", (menu_name,))
            row = cursor.fetchone()
            if row:
                dm_menu_id = row[0]
                cursor.execute("UPDATE menu SET sp=?, active=1 WHERE id=?", (sp, dm_menu_id))
            else:
                cursor.execute("INSERT INTO menu (name, sp, active, cogs) VALUES (?, ?, 1, 0)", (menu_name, sp))
                dm_menu_id = cursor.lastrowid
            cursor.execute(
                "INSERT OR REPLACE INTO daily_menu (day, meal_type, menu_id) VALUES (?, ?, ?)",
                (day, meal_type, dm_menu_id)
            )

        conn.commit()
        print("🎉 Database successfully seeded for 30 Apr 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
