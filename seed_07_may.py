import sqlite3

DATE = "2026-05-07"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 1097.000, 0.000, 66.000, 31.00, 2046.000, 1031.000, 31961.00),
    ("RICE", "Kgs", 729.000, 0.000, 47.000, 65.00, 3055.000, 682.000, 44330.00),
    ("R/OIL", "Ltr", 227.000, 0.000, 12.000, 180.92, 2171.077, 215.000, 38898.46),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 55.000, 0.000, 0.000, 78.00, 0.000, 55.000, 4290.00),
    ("BESAN", "Kgs", 54.000, 0.000, 2.000, 94.50, 189.000, 52.000, 4914.00),
    ("DAL ARHAR", "Kgs", 55.000, 0.000, 0.000, 120.00, 0.000, 55.000, 6600.00),
    ("DAL MASOOR (S)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("URD CRD(CHILKA)", "KGS", 9.000, 0.000, 0.000, 110.00, 0.000, 9.000, 990.00),
    ("MASUR CRD(Malika)", "Kgs", 9.000, 0.000, 0.000, 85.00, 0.000, 9.000, 765.00),
    ("MOONG Crd(Chilka)", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 1.000, 0.000, 0.200, 315.00, 63.000, 0.800, 252.00),
    ("HALDI PDR", "Kgs", 3.800, 0.000, 0.300, 231.00, 69.300, 3.500, 808.50),
    ("MIRCHI PDR", "Kgs", 3.900, 0.000, 0.300, 315.00, 94.500, 3.600, 1134.00),
    ("DAL CHINI", "Kgs", 0.410, 0.000, 0.010, 357.00, 3.570, 0.400, 142.80),
    ("LAUNG", "Kgs", 0.280, 0.000, 0.010, 1155.00, 11.550, 0.270, 311.85),
    ("HING", "Nos", 21.000, 0.000, 1.000, 89.25, 89.250, 20.000, 1785.00),
    ("KITCHEN KING", "Kgs", 2.200, 0.000, 0.200, 800.00, 160.000, 2.000, 1600.00),
    ("DEGI MIRCH", "Kgs", 2.300, 0.000, 0.200, 960.00, 192.000, 2.100, 2016.00),
    ("KASURI METHI", "Kgs", 0.700, 0.000, 0.050, 336.00, 16.800, 0.650, 218.40),
    ("GARAM MASALA", "Kgs", 2.100, 0.000, 0.300, 920.00, 276.000, 1.800, 1656.00),
    ("SALT", "Kgs", 51.000, 0.000, 4.000, 28.00, 112.000, 47.000, 1316.00),
    ("DANIYA (S)", "Kgs", 1.300, 0.000, 0.050, 157.50, 7.875, 1.250, 196.88),
    ("JEERA PDR", "Kgs", 1.400, 0.000, 0.400, 420.00, 168.000, 1.000, 420.00),
    ("CHANA MASALA (Pkt)", "Pkt", 1.000, 0.000, 0.200, 736.01, 147.203, 0.800, 588.81),
    ("B ELAICHI", "Kgs", 0.280, 0.000, 0.010, 1995.00, 19.950, 0.270, 538.65),
    ("METHI DANA", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("RAJMA MASALA", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("TEJ PATTA", "Kgs", 0.480, 0.000, 0.010, 168.00, 1.680, 0.470, 78.96),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 22.000, 0.000, 1.000, 504.00, 504.000, 21.000, 10584.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.750, 0.000, 0.750, 450.00, 337.500, 0.000, 0.00),
    ("AJWAIN", "Pkt", 0.850, 0.000, 0.050, 252.00, 12.600, 0.800, 201.60),
    ("MIRCHI (S)", "Kgs", 0.450, 0.000, 0.050, 315.00, 15.750, 0.400, 126.00),
    ("CHAT MASALA", "Kgs", 1.400, 0.000, 0.100, 752.00, 75.200, 1.300, 977.60),
    ("RAJMAH MASALA (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 6.000, 0.000, 1.000, 66.15, 66.152, 5.000, 330.76),
    ("CHANA MASALA", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 76.000, 0.000, 18.000, 78.00, 1404.000, 58.000, 4524.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 13.000, 0.000, 0.000, 60.00, 0.000, 13.000, 780.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 7.000, 0.000, 1.000, 70.80, 70.800, 6.000, 424.80),
    ("BIRIYANI MASALA", "Pkt", 10.000, 0.000, 3.000, 73.50, 220.500, 7.000, 514.50),
    ("ilaychi small Gr", "Kgs", 0.100, 0.000, 0.020, 3150.00, 63.000, 0.080, 252.00),
    ("DHANIYA PDR", "Kgs", 4.500, 0.000, 0.300, 168.00, 50.400, 4.200, 705.60),
    ("KALI MIRCH( S)", "Kgs", 0.380, 0.000, 0.010, 882.00, 8.820, 0.370, 326.34),
    ("MUMFALI DANA", "Kgs", 17.000, 0.000, 0.000, 157.50, 0.000, 17.000, 2677.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 44.000, 0.000, 28.600, 61.83, 1768.338, 15.400, 952.20),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 2.000, 0.000, 2.000, 86.50, 173.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 2.000, 0.000, 0.200, 880.00, 176.000, 1.800, 1584.00),
    ("SOYA BEAN BADIYA", "kgs", 21.000, 0.000, 12.000, 94.50, 1134.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.580, 0.000, 0.010, 2730.00, 27.300, 0.570, 1556.10),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 5.000, 0.000, 1.000, 147.00, 147.000, 4.000, 588.00),
    ("CREAM", "Kgs", 6.500, 0.000, 0.000, 220.00, 0.000, 6.500, 1430.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2585, 0, 523, 3.186, 1666.28, 2062, 6569.53),
    ("FOIL BOX (RICE,SABJI)", "Nos", 4348, 0, 1046, 1.575, 1647.45, 3302, 5200.65),
    ("ROTI POUCH", "Nos", 18200, 0, 2800, 0.236, 660.80, 15400, 3634.40),
    ("SALAD PKT", "Nos", 5178, 0, 1046, 0.177, 185.14, 4132, 731.36),
    ("SPOON/MINI MEAL", "Nos", 1898, 0, 584, 0.504, 294.34, 1314, 662.26),
    ("NEPKIN TUSSU PEPAR", "Nos", 7361, 0, 594, 0.354, 210.28, 6767, 2395.52),
    ("SALT POUCH", "Nos", 132, 1500, 523, 0.150, 78.45, 1109, 166.35),
    ("PICKLE & PARATHA", "Nos", 2930, 0, 594, 0.899, 534.19, 2336, 2100.78),
    ("TAPE", "Nos", 7, 0, 2, 23.600, 47.20, 5, 118.00),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 268, 0, 61, 3.150, 192.15, 207, 652.05),
    ("PAPER BOX (LUNCH)", "Nos", 5981, 0, 523, 4.956, 2591.99, 5458, 27049.85),
    ("BUTTER ROTI PAPER", "NOS", 1.150, 0, 0.050, 236.000, 11.80, 1.100, 259.60),
    ("PARATHA BOX", "Nos", 1244, 0, 71, 3.360, 238.56, 1173, 3941.28),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 2, 0, 1, 141.600, 141.60, 1, 141.60),
    ("400 ML PP BOX", "Nos", 155, 0, 0, 4.720, 0.00, 155, 731.60),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 16.500, 0, 0.000, 280.00, 0.00, 16.500, 4620.00),
    ("PETHA", "KGS", 25.000, 0, 15.000, 150.00, 2250.00, 10.000, 1500.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 0.000, 50.000, 15.000, 10.000, 150.000, 35.000, 350.00),
    ("ONION", "Kgs", 98.000, 0.000, 14.000, 23.000, 322.000, 84.000, 1932.00),
    ("TOMATO", "Kgs", 24.000, 0.000, 10.000, 18.000, 180.000, 14.000, 252.00),
    ("GINGER", "Kgs", 0.000, 3.000, 1.000, 135.000, 135.000, 2.000, 270.00),
    ("GARLIC", "Kgs", 3.055, 0.000, 1.500, 132.000, 198.000, 1.555, 205.26),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 1.000, 0.000, 1.000, 55.000, 55.000, 0.000, 0.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 40.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 15.000, 0.000, 15.000, 31.000, 465.000, 0.000, 0.00),
    ("BEANS", "Kgs", 14.975, 0.000, 14.975, 59.000, 883.525, 0.000, 0.00),
    ("CARROT", "Kgs", 25.140, 0.000, 25.140, 33.000, 829.620, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 35.360, 0.000, 35.360, 55.000, 1944.800, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 22.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 69.000, 0.000, 21.000, 20.000, 420.000, 48.000, 960.00),
    ("MATAR", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 523, 520, 70.0, 36400, 28924.0),
    ("PARATHA", 71, 70, 40.0, 2800, 2180.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 195, 10.0, 1950, 1755.0),
    ("MINI", 61, 59, 50.0, 2950, 1377.0),
    ("AMUL", 2, 2, 25.0, 50, 44.0),
    ("LAHARI JEERA", 10, 10, 10.0, 100, 90.0),
    ("LASSI", 8, 8, 20.0, 160, 152.0),
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
        print("🎉 Database successfully updated for 07 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
