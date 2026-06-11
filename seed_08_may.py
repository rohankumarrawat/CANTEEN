import sqlite3

DATE = "2026-05-08"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 1031.000, 0.000, 66.000, 31.00, 2046.000, 965.000, 29915.00),
    ("RICE", "Kgs", 682.000, 0.000, 40.000, 65.00, 2600.000, 642.000, 41730.00),
    ("R/OIL", "Ltr", 215.000, 0.000, 8.000, 180.92, 1447.385, 207.000, 37451.08),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 55.000, 0.000, 12.000, 78.00, 936.000, 43.000, 3354.00),
    ("BESAN", "Kgs", 52.000, 0.000, 1.000, 94.50, 94.500, 51.000, 4819.50),
    ("DAL ARHAR", "Kgs", 55.000, 0.000, 8.000, 120.00, 960.000, 47.000, 5640.00),
    ("DAL MASOOR (S)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("URD CRD(CHILKA)", "KGS", 9.000, 0.000, 0.000, 110.00, 0.000, 9.000, 990.00),
    ("MASUR CRD(Malika)", "Kgs", 9.000, 0.000, 0.000, 85.00, 0.000, 9.000, 765.00),
    ("MOONG Crd(Chilka)", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 0.800, 0.000, 0.300, 315.00, 94.500, 0.500, 157.50),
    ("HALDI PDR", "Kgs", 3.500, 0.000, 0.300, 231.00, 69.300, 3.200, 739.20),
    ("MIRCHI PDR", "Kgs", 3.600, 0.000, 0.300, 315.00, 94.500, 3.300, 1039.50),
    ("DAL CHINI", "Kgs", 0.400, 0.000, 0.010, 357.00, 3.570, 0.390, 139.23),
    ("LAUNG", "Kgs", 0.270, 0.000, 0.010, 1155.00, 11.550, 0.260, 300.30),
    ("HING", "Nos", 20.000, 0.000, 0.000, 89.25, 0.000, 20.000, 1785.00),
    ("KITCHEN KING", "Kgs", 2.000, 0.000, 0.200, 800.00, 160.000, 1.800, 1440.00),
    ("DEGI MIRCH", "Kgs", 2.100, 0.000, 0.200, 960.00, 192.000, 1.900, 1824.00),
    ("KASURI METHI", "Kgs", 0.650, 0.000, 0.050, 336.00, 16.800, 0.600, 201.60),
    ("GARAM MASALA", "Kgs", 1.800, 0.000, 0.200, 920.00, 184.000, 1.600, 1472.00),
    ("SALT", "Kgs", 47.000, 0.000, 4.000, 28.00, 112.000, 43.000, 1204.00),
    ("DANIYA (S)", "Kgs", 1.250, 0.000, 0.050, 157.50, 7.875, 1.200, 189.00),
    ("JEERA PDR", "Kgs", 1.000, 0.000, 0.200, 420.00, 84.000, 0.800, 336.00),
    ("CHANA MASALA (Pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("B ELAICHI", "Kgs", 0.270, 0.000, 0.010, 1995.00, 19.950, 0.260, 518.70),
    ("METHI DANA", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("RAJMA MASALA", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("TEJ PATTA", "Kgs", 0.470, 0.000, 0.010, 168.00, 1.680, 0.460, 77.28),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 21.000, 0.000, 1.000, 504.00, 504.000, 20.000, 10080.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.000, 1.000, 0.250, 600.00, 150.000, 0.750, 450.00),
    ("AJWAIN", "Pkt", 0.800, 0.000, 0.050, 252.00, 12.600, 0.750, 189.00),
    ("MIRCHI (S)", "Kgs", 0.400, 0.000, 0.050, 315.00, 15.750, 0.350, 110.25),
    ("CHAT MASALA", "Kgs", 1.300, 0.000, 0.100, 752.00, 75.200, 1.200, 902.40),
    ("RAJMAH MASALA (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 5.000, 0.000, 0.000, 66.15, 0.000, 5.000, 330.76),
    ("CHANA MASALA", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 58.000, 0.000, 0.000, 78.00, 0.000, 58.000, 4524.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 13.000, 0.000, 4.000, 60.00, 240.000, 9.000, 540.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 6.000, 0.000, 0.000, 70.80, 0.000, 6.000, 424.80),
    ("BIRIYANI MASALA", "Pkt", 7.000, 0.000, 0.000, 73.50, 0.000, 7.000, 514.50),
    ("ilaychi small Gr", "Kgs", 0.080, 0.000, 0.000, 3150.00, 0.000, 0.080, 252.00),
    ("DHANIYA PDR", "Kgs", 4.200, 0.000, 0.300, 168.00, 50.400, 3.900, 655.20),
    ("KALI MIRCH( S)", "Kgs", 0.370, 0.000, 0.010, 882.00, 8.820, 0.360, 317.52),
    ("MUMFALI DANA", "Kgs", 17.000, 0.000, 4.000, 157.50, 630.000, 13.000, 2047.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 15.400, 28.400, 32.400, 61.83, 2003.324, 11.400, 704.87),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 1.800, 0.000, 0.400, 880.00, 352.000, 1.400, 1232.00),
    ("SOYA BEAN BADIYA", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.570, 0.000, 0.010, 2730.00, 27.300, 0.560, 1528.80),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("CREAM", "Kgs", 6.500, 0.000, 1.000, 220.00, 220.000, 5.500, 1210.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2062, 0, 600, 3.186, 1911.60, 1462, 4657.93),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3302, 0, 1080, 1.575, 1701.00, 2222, 3499.65),
    ("ROTI POUCH", "Nos", 15400, 0, 2800, 0.236, 660.80, 12600, 2973.60),
    ("SALAD PKT", "Nos", 4132, 0, 1080, 0.177, 191.16, 3052, 540.20),
    ("SPOON/MINI MEAL", "Nos", 1314, 0, 540, 0.504, 272.16, 774, 390.10),
    ("NEPKIN TUSSU PEPAR", "Nos", 6767, 0, 610, 0.354, 215.94, 6157, 2179.58),
    ("SALT POUCH", "Nos", 1109, 0, 540, 0.150, 81.00, 569, 85.35),
    ("PICKLE & PARATHA", "Nos", 2336, 0, 610, 0.899, 548.38, 1726, 1552.20),
    ("TAPE", "Nos", 5, 0, 2, 23.600, 47.20, 3, 70.80),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 207, 0, 60, 3.150, 189.00, 147, 463.05),
    ("PAPER BOX (LUNCH)", "Nos", 5458, 0, 540, 4.956, 2676.24, 4918, 24373.61),
    ("BUTTER ROTI PAPER", "NOS", 1.100, 0, 0.050, 236.000, 11.80, 1.050, 247.80),
    ("PARATHA BOX", "Nos", 1173, 0, 70, 3.360, 235.20, 1103, 3706.08),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 0, 0, 141.600, 0.00, 1, 141.60),
    ("400 ML PP BOX", "Nos", 155, 0, 0, 4.720, 0.00, 155, 731.60),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 16.500, 0, 12.000, 280.00, 3360.00, 4.500, 1260.00),
    ("PETHA", "KGS", 10.000, 0, 0.000, 150.00, 0.00, 10.000, 1500.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 35.000, 0.000, 16.000, 10.000, 160.000, 19.000, 190.00),
    ("ONION", "Kgs", 84.000, 0.000, 12.000, 23.000, 276.000, 72.000, 1656.00),
    ("TOMATO", "Kgs", 14.000, 0.000, 12.000, 18.000, 216.000, 2.000, 36.00),
    ("GINGER", "Kgs", 2.000, 0.000, 1.300, 135.000, 175.500, 0.700, 94.50),
    ("GARLIC", "Kgs", 1.555, 0.000, 1.000, 132.000, 132.000, 0.555, 73.26),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 0.000, 3.020, 2.000, 60.000, 120.000, 1.020, 61.20),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 40.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 0.000, 0.000, 0.000, 31.000, 0.000, 0.000, 0.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 22.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 48.000, 0.000, 21.000, 20.000, 420.000, 27.000, 540.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 16.000, 16.000, 250.000, 4000.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 30.000, 30.000, 30.000, 900.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 540, 537, 70.0, 37590, 28591.0),
    ("PARATHA", 70, 68, 40.0, 2720, 1803.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 195, 10.0, 1950, 1755.0),
    ("MINI", 60, 60, 50.0, 3000, 1532.0),
    ("AMUL", 7, 7, 25.0, 175, 154.0),
    ("LAHARI JEERA", 10, 10, 10.0, 100, 90.0),
    ("LASSI", 10, 10, 20.0, 200, 190.0),
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
        print("🎉 Database successfully updated for 08 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
