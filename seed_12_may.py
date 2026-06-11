import sqlite3

DATE = "2026-05-12"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 879.000, 0.000, 66.000, 31.00, 2046.000, 813.000, 25203.00),
    ("RICE", "Kgs", 583.000, 0.000, 46.000, 65.00, 2990.000, 537.000, 34905.00),
    ("R/OIL", "Ltr", 193.000, 0.000, 12.000, 180.92, 2171.077, 181.000, 32747.08),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.150, 105.00, 15.750, 0.350, 36.75),
    ("RAJMAH", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 35.000, 0.000, 0.000, 78.00, 0.000, 35.000, 2730.00),
    ("BESAN", "Kgs", 51.000, 0.000, 12.000, 94.50, 1134.000, 39.000, 3685.50),
    ("DAL ARHAR", "Kgs", 44.000, 0.000, 0.000, 120.00, 0.000, 44.000, 5280.00),
    ("DAL MASOOR (S)", "Pkt", 14.000, 0.000, 0.000, 85.00, 0.000, 14.000, 1190.00),
    ("URD CRD(CHILKA)", "KGS", 6.000, 0.000, 0.000, 110.00, 0.000, 6.000, 660.00),
    ("MASUR CRD(Malika)", "Kgs", 6.000, 0.000, 0.000, 85.00, 0.000, 6.000, 510.00),
    ("MOONG Crd(Chilka)", "Kgs", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 0.350, 0.000, 0.050, 315.00, 15.750, 0.300, 94.50),
    ("HALDI PDR", "Kgs", 2.900, 0.000, 0.200, 231.00, 46.200, 2.700, 623.70),
    ("MIRCHI PDR", "Kgs", 3.000, 0.000, 0.200, 315.00, 63.000, 2.800, 882.00),
    ("DAL CHINI", "Kgs", 0.370, 0.000, 0.010, 357.00, 3.570, 0.360, 128.52),
    ("LAUNG", "Kgs", 0.240, 0.000, 0.010, 1155.00, 11.550, 0.230, 265.65),
    ("HING", "Nos", 20.000, 0.000, 4.000, 89.25, 357.000, 16.000, 1428.00),
    ("KITCHEN KING", "Kgs", 1.500, 0.000, 0.200, 800.00, 160.000, 1.300, 1040.00),
    ("DEGI MIRCH", "Kgs", 1.600, 0.000, 0.200, 960.00, 192.000, 1.400, 1344.00),
    ("KASURI METHI", "Kgs", 0.550, 0.000, 0.050, 336.00, 16.800, 0.500, 168.00),
    ("GARAM MASALA", "Kgs", 1.300, 0.000, 0.200, 920.00, 184.000, 1.100, 1012.00),
    ("SALT", "Kgs", 37.000, 0.000, 4.000, 28.00, 112.000, 33.000, 924.00),
    ("DANIYA (S)", "Kgs", 1.100, 0.000, 0.100, 157.50, 15.750, 1.000, 157.50),
    ("JEERA PDR", "Kgs", 0.600, 0.000, 0.100, 420.00, 42.000, 0.500, 210.00),
    ("CHANA MASALA (Pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("B ELAICHI", "Kgs", 0.240, 0.000, 0.010, 1995.00, 19.950, 0.230, 458.85),
    ("METHI DANA", "Kgs", 0.210, 0.000, 0.100, 105.00, 10.500, 0.110, 11.55),
    ("RAJMA MASALA", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("TEJ PATTA", "Kgs", 0.440, 0.000, 0.010, 168.00, 1.680, 0.430, 72.24),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 18.000, 0.000, 1.000, 504.00, 504.000, 17.000, 8568.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.000, 0.000, 0.000, 600.00, 0.000, 0.000, 0.00),
    ("AJWAIN", "Pkt", 0.700, 0.000, 0.100, 252.00, 25.200, 0.600, 151.20),
    ("MIRCHI (S)", "Kgs", 0.300, 0.000, 0.050, 315.00, 15.750, 0.250, 78.75),
    ("CHAT MASALA", "Kgs", 1.100, 0.000, 0.100, 752.00, 75.200, 1.000, 752.00),
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
    ("ilaychi small Gr", "Kgs", 0.070, 0.000, 0.010, 3150.00, 31.500, 0.070, 220.50),
    ("DHANIYA PDR", "Kgs", 3.600, 0.000, 0.200, 168.00, 33.600, 3.400, 571.20),
    ("KALI MIRCH( S)", "Kgs", 0.340, 0.000, 0.010, 882.00, 8.820, 0.330, 291.06),
    ("MUMFALI DANA", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 82.400, 0.000, 9.800, 61.83, 605.944, 72.600, 4488.93),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("SOYA BEAN BADIYA", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.540, 0.000, 0.010, 2730.00, 27.300, 0.530, 1446.90),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 5.000, 0.000, 0.000, 70.00, 0.000, 5.000, 350.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("SABJI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("CREAM", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("PARATHA MASALA", "Kgs", 0.000, 5.000, 5.000, 10.00, 10.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 3800, 0, 521, 3.186, 1659.91, 3279, 10446.89),
    ("FOIL BOX (RICE,SABJI)", "Nos", 6898, 0, 1042, 1.575, 1641.15, 5856, 9223.20),
    ("ROTI POUCH", "Nos", 24900, 0, 2800, 0.236, 660.80, 22100, 5215.60),
    ("SALAD PKT", "Nos", 7728, 0, 1042, 0.177, 184.43, 6686, 1183.42),
    ("SPOON/MINI MEAL", "Nos", 3051, 0, 581, 0.504, 292.82, 2470, 1244.88),
    ("NEPKIN TUSSU PEPAR", "Nos", 9034, 0, 591, 0.354, 209.21, 8443, 2988.82),
    ("SALT POUCH", "Nos", 2907, 0, 521, 0.150, 78.15, 2386, 357.90),
    ("PICKLE & PARATHA", "Nos", 5035, 0, 591, 0.896, 529.54, 4444, 3981.08),
    ("TAPE", "Nos", 9, 0, 2, 23.600, 47.20, 7, 165.20),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 307, 0, 60, 3.150, 189.00, 247, 778.05),
    ("PAPER BOX (LUNCH)", "Nos", 4256, 0, 521, 4.956, 2582.08, 3735, 18510.66),
    ("BUTTER ROTI PAPER", "NOS", 1.800, 0, 0.050, 236.000, 11.80, 1.750, 413.00),
    ("PARATHA BOX", "Nos", 1042, 0, 70, 3.360, 235.20, 972, 3265.92),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 5, 0, 1, 141.600, 141.60, 4, 566.40),
    ("400 ML PP BOX", "Nos", 287, 0, 60, 4.720, 283.20, 227, 1071.44),
    ("SILVER FOIL", "Kgs", 4, 0, 0, 708.000, 0.00, 4, 2832.00),
    ("FOIL SILVER", "Kgs", 1, 0, 1, 531.000, 531.00, 0, 0.00),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 14.000, 0, 0.000, 280.00, 0.00, 14.000, 3920.00),
    ("PETHA", "KGS", 15.000, 0, 0.000, 150.00, 0.00, 15.000, 2250.00),
    ("GULDANA", "KGS", 14.000, 0, 14.000, 250.00, 3500.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 45.000, 0.000, 15.000, 10.000, 150.000, 30.000, 300.00),
    ("ONION", "Kgs", 108.000, 0.000, 12.000, 22.000, 264.000, 96.000, 2112.00),
    ("TOMATO", "Kgs", 53.000, 0.000, 12.000, 16.000, 192.000, 41.000, 656.00),
    ("GINGER", "Kgs", 9.000, 0.000, 2.000, 135.000, 270.000, 7.000, 945.00),
    ("GARLIC", "Kgs", 3.480, 0.000, 1.000, 143.000, 143.000, 2.480, 354.64),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("PUMPKIN", "Kgs", 100.000, 0.000, 100.000, 15.000, 1500.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 9.020, 0.000, 3.000, 60.000, 180.000, 6.020, 361.20),
    ("CORRENDER", "Kgs", 2.000, 0.000, 2.000, 20.000, 40.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 12.000, 0.000, 0.000, 22.000, 0.000, 12.000, 264.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 0.000, 0.000, 55.000, 0.000, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 12.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 88.000, 0.000, 21.000, 20.000, 420.000, 67.000, 1340.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 521, 519, 70.0, 36330, 25044.0),
    ("PARATHA", 71, 70, 40.0, 2800, 1837.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 194, 10.0, 1940, 1746.0),
    ("MINI", 60, 59, 50.0, 2950, 1152.0),
    ("AMUL", 1, 1, 25.0, 25, 22.0),
    ("LAHARI JEERA", 15, 15, 10.0, 150, 135.0),
    ("LASSI", 17, 17, 20.0, 340, 323.0),
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
        print("🎉 Database successfully updated for 12 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
