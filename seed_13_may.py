import sqlite3

DATE = "2026-05-13"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 813.000, 0.000, 66.000, 31.00, 2046.000, 747.000, 23157.00),
    ("RICE", "Kgs", 537.000, 0.000, 40.000, 65.00, 2600.000, 497.000, 32305.00),
    ("R/OIL", "Ltr", 181.000, 0.000, 11.500, 180.92, 2080.615, 169.500, 30666.46),
    ("Sarso Dana", "Kgs", 0.350, 0.000, 0.000, 105.00, 0.000, 0.350, 36.75),
    ("RAJMAH", "Kgs", 65.000, 0.000, 17.000, 115.00, 1955.000, 48.000, 5520.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 35.000, 0.000, 4.000, 78.00, 312.000, 31.000, 2418.00),
    ("BESAN", "Kgs", 39.000, 0.000, 0.000, 94.50, 0.000, 39.000, 3685.50),
    ("DAL ARHAR", "Kgs", 44.000, 0.000, 0.000, 120.00, 0.000, 44.000, 5280.00),
    ("DAL MASOOR (S)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("URD CRD(CHILKA)", "KGS", 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ("MASUR CRD(Malika)", "Kgs", 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ("MOONG Crd(Chilka)", "Kgs", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 0.300, 0.000, 0.050, 315.00, 15.750, 0.250, 78.75),
    ("HALDI PDR", "Kgs", 2.700, 0.000, 0.200, 231.00, 46.200, 2.500, 577.50),
    ("MIRCHI PDR", "Kgs", 2.800, 0.000, 0.200, 315.00, 63.000, 2.600, 819.00),
    ("DAL CHINI", "Kgs", 0.360, 0.000, 0.010, 357.00, 3.570, 0.350, 124.95),
    ("LAUNG", "Kgs", 0.230, 0.000, 0.010, 1155.00, 11.550, 0.220, 254.10),
    ("HING", "Nos", 16.000, 0.000, 1.000, 89.25, 89.250, 15.000, 1338.75),
    ("KITCHEN KING", "Kgs", 1.300, 0.000, 0.300, 800.00, 240.000, 1.000, 800.00),
    ("DEGI MIRCH", "Kgs", 1.400, 0.000, 0.300, 960.00, 288.000, 1.100, 1056.00),
    ("KASURI METHI", "Kgs", 0.500, 0.000, 0.050, 336.00, 16.800, 0.450, 151.20),
    ("GARAM MASALA", "Kgs", 1.100, 0.000, 0.300, 920.00, 276.000, 0.800, 736.00),
    ("SALT", "Kgs", 33.000, 0.000, 3.000, 28.00, 84.000, 30.000, 840.00),
    ("DANIYA (S)", "Kgs", 1.000, 0.000, 0.050, 157.50, 7.875, 0.950, 149.63),
    ("JEERA PDR", "Kgs", 0.500, 0.000, 0.300, 420.00, 126.000, 0.200, 84.00),
    ("CHANA MASALA (Pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("B ELAICHI", "Kgs", 0.230, 0.000, 0.010, 1995.00, 19.950, 0.220, 438.90),
    ("METHI DANA", "Kgs", 0.110, 0.000, 0.000, 105.00, 0.000, 0.110, 11.55),
    ("RAJMA MASALA", "Pkt", 2.000, 0.000, 2.000, 72.00, 144.000, 0.000, 0.00),
    ("TEJ PATTA", "Kgs", 0.430, 0.000, 0.010, 168.00, 1.680, 0.420, 70.56),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 17.000, 0.000, 1.000, 504.00, 504.000, 16.000, 8064.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ("AJWAIN", "Pkt", 0.600, 0.000, 0.080, 252.00, 20.160, 0.520, 131.04),
    ("MIRCHI (S)", "Kgs", 0.250, 0.000, 0.100, 315.00, 31.500, 0.150, 47.25),
    ("CHAT MASALA", "Kgs", 1.000, 0.000, 0.100, 752.00, 75.200, 0.900, 676.80),
    ("RAJMAH MASALA (Kgs)", "Kgs", 2.000, 0.000, 0.400, 736.00, 294.400, 1.600, 1177.60),
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
    ("ilaychi small Gr", "Kgs", 0.070, 0.000, 0.010, 3150.00, 31.500, 0.060, 189.00),
    ("DHANIYA PDR", "Kgs", 3.400, 0.000, 0.200, 168.00, 33.600, 3.200, 537.60),
    ("KALI MIRCH( S)", "Kgs", 0.330, 0.000, 0.010, 882.00, 8.820, 0.320, 282.24),
    ("MUMFALI DANA", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 72.600, 0.000, 23.500, 61.83, 1453.028, 49.100, 3035.90),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("SOYA BEAN BADIYA", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.530, 0.000, 0.030, 2730.00, 81.900, 0.500, 1365.00),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 5.000, 0.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("SABJI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("CREAM", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("PARATHA MASALA", "Kgs", 0.000, 0.000, 0.000, 10.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 3279, 0, 445, 3.186, 1417.77, 2834, 9029.12),
    ("FOIL BOX (RICE,SABJI)", "Nos", 5856, 0, 890, 1.575, 1401.75, 4966, 7821.45),
    ("ROTI POUCH", "Nos", 22100, 0, 2900, 0.236, 684.40, 19200, 4531.20),
    ("SALAD PKT", "Nos", 6686, 0, 890, 0.177, 157.53, 5796, 1025.89),
    ("SPOON/MINI MEAL", "Nos", 2470, 0, 506, 0.504, 255.02, 1964, 989.86),
    ("NEPKIN TUSSU PEPAR", "Nos", 8443, 0, 509, 0.354, 180.19, 7934, 2808.64),
    ("SALT POUCH", "Nos", 2386, 0, 445, 0.150, 66.75, 1941, 291.15),
    ("PICKLE & PARATHA", "Nos", 4444, 0, 509, 0.896, 455.98, 3935, 3525.10),
    ("TAPE", "Nos", 7, 0, 1, 23.600, 23.60, 6, 141.60),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 247, 0, 61, 3.150, 192.15, 186, 585.90),
    ("PAPER BOX (LUNCH)", "Nos", 3735, 0, 445, 4.956, 2205.42, 3290, 16305.24),
    ("BUTTER ROTI PAPER", "NOS", 1750, 0, 50, 0.236, 11.80, 1700, 401.20),
    ("PARATHA BOX", "Nos", 972, 0, 64, 3.360, 215.04, 908, 3050.88),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 4, 0, 1, 141.600, 141.60, 3, 424.80),
    ("400 ML PP BOX", "Nos", 227, 0, 61, 4.720, 287.92, 166, 783.52),
    ("SILVER FOIL", "Kgs", 4, 0, 0.500, 708.000, 354.00, 3.500, 2478.00),
    ("FOIL SILVER", "Kgs", 0, 0, 0, 531.000, 0.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 14.000, 0, 12.000, 280.00, 3360.00, 2.000, 560.00),
    ("PETHA", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 30.000, 0.000, 0.000, 10.000, 0.000, 30.000, 300.00),
    ("ONION", "Kgs", 96.000, 0.000, 14.000, 22.000, 308.000, 82.000, 1804.00),
    ("TOMATO", "Kgs", 41.000, 0.000, 14.000, 16.000, 224.000, 27.000, 432.00),
    ("GINGER", "Kgs", 7.000, 0.000, 2.000, 135.000, 270.000, 5.000, 675.00),
    ("GARLIC", "Kgs", 2.480, 0.000, 1.000, 143.000, 143.000, 1.480, 211.64),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("PUMPKIN", "Kgs", 0.000, 0.000, 0.000, 15.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 6.020, 0.000, 2.000, 60.000, 120.000, 4.020, 241.20),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 20.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 12.000, 0.000, 0.000, 22.000, 0.000, 12.000, 264.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 67.000, 0.000, 20.000, 20.000, 400.000, 47.000, 940.00),
    ("MATAR", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 445, 442, 70.0, 30940, 24366.0),
    ("PARATHA", 64, 62, 40.0, 2480, 2158.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 61, 60, 50.0, 3000, 1161.0),
    ("AMUL", 4, 4, 25.0, 100, 88.0),
    ("LAHARI JEERA", 6, 6, 10.0, 60, 54.0),
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
        print("🎉 Database successfully updated for 13 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
