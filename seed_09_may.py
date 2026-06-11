import sqlite3

DATE = "2026-05-09"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 965.000, 0.000, 20.000, 31.00, 620.000, 945.000, 29295.00),
    ("RICE", "Kgs", 642.000, 0.000, 12.000, 65.00, 780.000, 630.000, 40950.00),
    ("R/OIL", "Ltr", 207.000, 0.000, 5.000, 180.92, 904.615, 202.000, 36546.46),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 65.000, 0.000, 0.000, 115.00, 0.000, 65.000, 7475.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 43.000, 0.000, 0.000, 78.00, 0.000, 43.000, 3354.00),
    ("BESAN", "Kgs", 51.000, 0.000, 0.000, 94.50, 0.000, 51.000, 4819.50),
    ("DAL ARHAR", "Kgs", 47.000, 0.000, 0.000, 120.00, 0.000, 47.000, 5640.00),
    ("DAL MASOOR (S)", "Pkt", 18.000, 0.000, 4.000, 85.00, 340.000, 14.000, 1190.00),
    ("URD CRD(CHILKA)", "KGS", 9.000, 0.000, 0.000, 110.00, 0.000, 9.000, 990.00),
    ("MASUR CRD(Malika)", "Kgs", 9.000, 0.000, 0.000, 85.00, 0.000, 9.000, 765.00),
    ("MOONG Crd(Chilka)", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 0.500, 0.000, 0.100, 315.00, 31.500, 0.400, 126.00),
    ("HALDI PDR", "Kgs", 3.200, 0.000, 0.100, 231.00, 23.100, 3.100, 716.10),
    ("MIRCHI PDR", "Kgs", 3.300, 0.000, 0.100, 315.00, 31.500, 3.200, 1008.00),
    ("DAL CHINI", "Kgs", 0.390, 0.000, 0.010, 357.00, 3.570, 0.380, 135.66),
    ("LAUNG", "Kgs", 0.260, 0.000, 0.010, 1155.00, 11.550, 0.250, 288.75),
    ("HING", "Nos", 20.000, 0.000, 0.000, 89.25, 0.000, 20.000, 1785.00),
    ("KITCHEN KING", "Kgs", 1.800, 0.000, 0.100, 800.00, 80.000, 1.700, 1360.00),
    ("DEGI MIRCH", "Kgs", 1.900, 0.000, 0.100, 960.00, 96.000, 1.800, 1728.00),
    ("KASURI METHI", "Kgs", 0.600, 0.000, 0.000, 336.00, 0.000, 0.600, 201.60),
    ("GARAM MASALA", "Kgs", 1.600, 0.000, 0.100, 920.00, 92.000, 1.500, 1380.00),
    ("SALT", "Kgs", 43.000, 0.000, 2.000, 28.00, 56.000, 41.000, 1148.00),
    ("DANIYA (S)", "Kgs", 1.200, 0.000, 0.050, 157.50, 7.875, 1.150, 181.13),
    ("JEERA PDR", "Kgs", 0.800, 0.000, 0.100, 420.00, 42.000, 0.700, 294.00),
    ("CHANA MASALA (Pkt)", "Pkt", 0.800, 0.000, 0.000, 736.01, 0.000, 0.800, 588.81),
    ("B ELAICHI", "Kgs", 0.260, 0.000, 0.010, 1995.00, 19.950, 0.250, 498.75),
    ("METHI DANA", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("RAJMA MASALA", "Pkt", 2.000, 0.000, 0.000, 72.00, 0.000, 2.000, 144.00),
    ("TEJ PATTA", "Kgs", 0.460, 0.000, 0.010, 168.00, 1.680, 0.450, 75.60),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 20.000, 0.000, 0.500, 504.00, 252.000, 19.500, 9828.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.750, 0.000, 0.000, 600.00, 0.000, 0.750, 450.00),
    ("AJWAIN", "Pkt", 0.750, 0.000, 0.000, 252.00, 0.000, 0.750, 189.00),
    ("MIRCHI (S)", "Kgs", 0.350, 0.000, 0.010, 315.00, 3.150, 0.340, 107.10),
    ("CHAT MASALA", "Kgs", 1.200, 0.000, 0.000, 752.00, 0.000, 1.200, 902.40),
    ("RAJMAH MASALA (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 5.000, 0.000, 0.000, 66.15, 0.000, 5.000, 330.76),
    ("CHANA MASALA", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 58.000, 0.000, 0.000, 78.00, 0.000, 58.000, 4524.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 1.000, 1.000, 90.00, 90.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 9.000, 0.000, 0.000, 60.00, 0.000, 9.000, 540.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 6.000, 0.000, 0.000, 70.80, 0.000, 6.000, 424.80),
    ("BIRIYANI MASALA", "Pkt", 7.000, 0.000, 0.000, 73.50, 0.000, 7.000, 514.50),
    ("ilaychi small Gr", "Kgs", 0.080, 0.000, 0.000, 3150.00, 0.000, 0.080, 252.00),
    ("DHANIYA PDR", "Kgs", 3.900, 0.000, 0.100, 168.00, 16.800, 3.800, 638.40),
    ("KALI MIRCH( S)", "Kgs", 0.360, 0.000, 0.010, 882.00, 8.820, 0.350, 308.70),
    ("MUMFALI DANA", "Kgs", 13.000, 0.000, 0.000, 157.50, 0.000, 13.000, 2047.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 11.400, 56.400, 11.400, 61.83, 704.873, 56.400, 3487.27),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 0.000, 0.000, 0.000, 86.50, 0.000, 0.000, 0.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 1.400, 0.000, 0.000, 880.00, 0.000, 1.400, 1232.00),
    ("SOYA BEAN BADIYA", "kgs", 9.000, 0.000, 0.000, 94.50, 0.000, 9.000, 850.50),
    ("JAVTITRI", "Kgs", 0.560, 0.000, 0.010, 2730.00, 27.300, 0.550, 1501.50),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 4.000, 0.000, 0.000, 147.00, 0.000, 4.000, 588.00),
    ("CREAM", "Kgs", 5.500, 0.000, 0.000, 220.00, 0.000, 5.500, 1210.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 1462, 0, 142, 3.186, 452.41, 1320, 4205.52),
    ("FOIL BOX (RICE,SABJI)", "Nos", 2222, 0, 284, 1.575, 447.30, 1938, 3052.35),
    ("ROTI POUCH", "Nos", 12600, 0, 900, 0.236, 212.40, 11700, 2761.20),
    ("SALAD PKT", "Nos", 3052, 0, 284, 0.177, 50.27, 2768, 489.94),
    ("SPOON/MINI MEAL", "Nos", 774, 0, 142, 0.504, 71.57, 632, 318.53),
    ("NEPKIN TUSSU PEPAR", "Nos", 6157, 0, 142, 0.354, 50.27, 6015, 2129.31),
    ("SALT POUCH", "Nos", 569, 0, 142, 0.150, 21.30, 427, 64.05),
    ("PICKLE & PARATHA", "Nos", 1726, 0, 142, 0.899, 127.70, 1584, 1424.50),
    ("TAPE", "Nos", 3, 0, 1, 23.600, 23.60, 2, 47.20),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 147, 0, 18, 3.150, 56.70, 129, 406.35),
    ("PAPER BOX (LUNCH)", "Nos", 4918, 0, 142, 4.956, 703.75, 4776, 23669.86),
    ("BUTTER ROTI PAPER", "NOS", 1.050, 0, 0.150, 236.000, 35.40, 0.900, 212.40),
    ("PARATHA BOX", "Nos", 1103, 0, 0, 3.360, 0.00, 1103, 3706.08),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 1, 0, 0, 141.600, 0.00, 1, 141.60),
    ("400 ML PP BOX", "Nos", 155, 0, 18, 4.720, 84.96, 137, 646.64),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 4.500, 0, 2.500, 280.00, 700.00, 2.000, 560.00),
    ("PETHA", "KGS", 10.000, 0, 0.000, 150.00, 0.00, 10.000, 1500.00),
    ("GULDANA", "KGS", 0.000, 0, 0.000, 250.00, 0.00, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 19.000, 50.000, 19.000, 10.000, 190.000, 50.000, 500.00),
    ("ONION", "Kgs", 72.000, 53.000, 5.000, 22.000, 110.000, 120.000, 2640.00),
    ("TOMATO", "Kgs", 2.000, 65.000, 2.000, 16.000, 32.000, 65.000, 1040.00),
    ("GINGER", "Kgs", 0.700, 7.000, 0.700, 65.000, 45.500, 7.000, 455.00),
    ("GARLIC", "Kgs", 0.555, 0.000, 0.555, 132.000, 73.260, 0.000, 0.00),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("PUMPKIN", "Kgs", 0.000, 100.000, 0.000, 15.000, 0.000, 100.000, 1500.00),
    ("GREEN CHILLI", "Kgs", 1.020, 6.000, 1.020, 60.000, 61.200, 6.000, 360.00),
    ("CORRENDER", "Kgs", 0.000, 2.000, 0.000, 20.000, 0.000, 2.000, 40.00),
    ("CAPSICUM", "Kgs", 0.000, 15.000, 0.000, 22.000, 0.000, 15.000, 330.00),
    ("BEANS", "Kgs", 0.000, 0.000, 0.000, 59.000, 0.000, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 1.170, 1.170, 33.000, 38.610, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 1.070, 1.070, 55.000, 58.850, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 90.000, 0.000, 12.000, 0.000, 90.000, 1080.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 27.000, 85.000, 5.000, 20.000, 100.000, 107.000, 2140.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 6.000, 6.000, 35.000, 210.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 142, 140, 70.0, 9800, 7814.0),
    ("MINI", 18, 18, 50.0, 900, 387.0),
    ("PARATHA", 0, 0, 40.0, 0, 0.0),
    ("DAHI", 0, 0, 10.0, 0, 0.0),
    ("CHACH", 0, 0, 10.0, 0, 0.0),
    ("AMUL", 0, 0, 25.0, 0, 0.0),
    ("LAHARI JEERA", 0, 0, 10.0, 0, 0.0),
    ("LASSI", 0, 0, 20.0, 0, 0.0),
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
        print("🎉 Database successfully updated for 09 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
