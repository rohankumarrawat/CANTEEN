import sqlite3

DATE = "2026-05-06"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 1149.000, 0.000, 52.000, 31.00, 1612.000, 1097.000, 34007.00),
    ("RICE", "Kgs", 769.000, 0.000, 40.000, 65.00, 2600.000, 729.000, 47385.00),
    ("R/OIL", "Ltr", 239.000, 0.000, 12.000, 180.92, 2171.077, 227.000, 41069.54),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 83.000, 0.000, 18.000, 115.00, 2070.000, 65.000, 7475.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 55.000, 0.000, 0.000, 78.00, 0.000, 55.000, 4290.00),
    ("BESAN", "Kgs", 60.000, 0.000, 6.000, 94.50, 567.000, 54.000, 5103.00),
    ("DAL ARHAR", "Kgs", 55.000, 0.000, 0.000, 120.00, 0.000, 55.000, 6600.00),
    ("DAL MASOOR (S)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("URD CRD(CHILKA)", "KGS", 9.000, 0.000, 0.000, 110.00, 0.000, 9.000, 990.00),
    ("MASUR CRD(Malika)", "Kgs", 9.000, 0.000, 0.000, 85.00, 0.000, 9.000, 765.00),
    ("MOONG Crd(Chilka)", "Kgs", 15.000, 0.000, 0.000, 110.00, 0.000, 15.000, 1650.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 1.300, 0.000, 0.300, 315.00, 94.500, 1.000, 315.00),
    ("HALDI PDR", "Kgs", 4.100, 0.000, 0.300, 231.00, 69.300, 3.800, 877.80),
    ("MIRCHI PDR", "Kgs", 4.200, 0.000, 0.300, 315.00, 94.500, 3.900, 1228.50),
    ("DAL CHINI", "Kgs", 0.420, 0.000, 0.010, 357.00, 3.570, 0.410, 146.37),
    ("LAUNG", "Kgs", 0.290, 0.000, 0.010, 1155.00, 11.550, 0.280, 323.40),
    ("HING", "Nos", 21.000, 0.000, 0.000, 89.25, 0.000, 21.000, 1874.25),
    ("KITCHEN KING", "Kgs", 2.400, 0.000, 0.200, 800.00, 160.000, 2.200, 1760.00),
    ("DEGI MIRCH", "Kgs", 2.500, 0.000, 0.200, 960.00, 192.000, 2.300, 2208.00),
    ("KASURI METHI", "Kgs", 0.750, 0.000, 0.050, 336.00, 16.800, 0.700, 235.20),
    ("GARAM MASALA", "Kgs", 2.300, 0.000, 0.200, 920.00, 184.000, 2.100, 1932.00),
    ("SALT", "Kgs", 54.000, 0.000, 3.000, 28.00, 84.000, 51.000, 1428.00),
    ("DANIYA (S)", "Kgs", 1.350, 0.000, 0.050, 157.50, 7.875, 1.300, 204.75),
    ("JEERA PDR", "Kgs", 1.800, 0.000, 0.400, 420.00, 168.000, 1.400, 588.00),
    ("CHANA MASALA (Pkt)", "Pkt", 1.000, 0.000, 0.000, 736.01, 0.000, 1.000, 736.01),
    ("B ELAICHI", "Kgs", 0.290, 0.000, 0.010, 1995.00, 19.950, 0.280, 558.60),
    ("METHI DANA", "Kgs", 0.210, 0.000, 0.000, 105.00, 0.000, 0.210, 22.05),
    ("RAJMA MASALA", "Pkt", 6.000, 0.000, 4.000, 72.00, 288.000, 2.000, 144.00),
    ("TEJ PATTA", "Kgs", 0.490, 0.000, 0.010, 168.00, 1.680, 0.480, 80.64),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 23.000, 0.000, 1.000, 504.00, 504.000, 22.000, 11088.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CLEAN WRAP", "Pkt", 0.250, 1.000, 0.500, 450.00, 225.000, 0.750, 337.50),
    ("AJWAIN", "Pkt", 0.900, 0.000, 0.050, 252.00, 12.600, 0.850, 214.20),
    ("MIRCHI (S)", "Kgs", 0.500, 0.000, 0.050, 315.00, 15.750, 0.450, 141.75),
    ("CHAT MASALA", "Kgs", 1.500, 0.000, 0.100, 752.00, 75.200, 1.400, 1052.80),
    ("RAJMAH MASALA (Kgs)", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 6.000, 0.000, 0.000, 66.15, 0.000, 6.000, 396.91),
    ("CHANA MASALA", "Kgs", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
    ("KALA CHANA", "Kgs", 76.000, 0.000, 0.000, 78.00, 0.000, 76.000, 5928.00),
    ("VINAYGER", "BTL", 0.000, 0.000, 0.000, 53.00, 0.000, 0.000, 0.00),
    ("RED CHILLI SAUCE", "BTL", 0.000, 0.000, 0.000, 84.00, 0.000, 0.000, 0.00),
    ("MATAR PANEER MASALA", "BTL", 0.000, 0.000, 0.000, 35.00, 0.000, 0.000, 0.00),
    ("PAV BHAJI MASALA", "BTL", 0.000, 0.000, 0.000, 92.00, 0.000, 0.000, 0.00),
    ("MATAR TF", "Kgs", 13.000, 0.000, 0.000, 60.00, 0.000, 13.000, 780.00),
    ("STAR FOOL MASALA", "Kgs", 0.000, 0.000, 0.000, 1600.00, 0.000, 0.000, 0.00),
    ("FOOD COLOUR", "PKT", 2.000, 0.000, 0.000, 68.44, 0.000, 2.000, 136.88),
    ("KEVADA WATER", "BTL", 7.000, 0.000, 0.000, 70.80, 0.000, 7.000, 495.60),
    ("BIRIYANI MASALA", "Pkt", 10.000, 0.000, 0.000, 73.50, 0.000, 10.000, 735.00),
    ("ilaychi small Gr", "Kgs", 0.100, 0.000, 0.000, 3150.00, 0.000, 0.100, 315.00),
    ("DHANIYA PDR", "Kgs", 4.700, 0.000, 0.200, 168.00, 33.600, 4.500, 756.00),
    ("KALI MIRCH( S)", "Kgs", 0.390, 0.000, 0.010, 882.00, 8.820, 0.380, 335.16),
    ("MUMFALI DANA", "Kgs", 19.000, 0.000, 2.000, 157.50, 315.000, 17.000, 2677.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 64.600, 0.000, 20.600, 61.83, 1273.718, 44.000, 2720.56),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 2.000, 0.000, 0.000, 67.20, 0.000, 2.000, 134.40),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 6.000, 0.000, 4.000, 86.50, 346.000, 2.000, 173.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 2.000, 0.000, 0.000, 880.00, 0.000, 2.000, 1760.00),
    ("SOYA BEAN BADIYA", "kgs", 21.000, 0.000, 0.000, 94.50, 0.000, 21.000, 1984.50),
    ("JAVTITRI", "Kgs", 0.600, 0.000, 0.020, 2730.00, 54.600, 0.580, 1583.40),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 5.000, 0.000, 0.000, 147.00, 0.000, 5.000, 735.00),
    ("CREAM", "Kgs", 7.000, 0.000, 0.500, 220.00, 110.000, 6.500, 1430.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2996, 0, 411, 3.186, 1309.45, 2585, 8235.81),
    ("FOIL BOX (RICE,SABJI)", "Nos", 5170, 0, 822, 1.575, 1294.65, 4348, 6848.10),
    ("ROTI POUCH", "Nos", 21000, 0, 2800, 0.236, 660.80, 18200, 4295.20),
    ("SALAD PKT", "Nos", 6000, 0, 822, 0.177, 145.49, 5178, 916.51),
    ("SPOON/MINI MEAL", "Nos", 2370, 0, 472, 0.504, 237.89, 1898, 956.59),
    ("NEPKIN TUSSU PEPAR", "Nos", 7772, 0, 411, 0.354, 145.49, 7361, 2605.79),
    ("SALT POUCH", "Nos", 543, 0, 411, 0.150, 61.65, 132, 19.80),
    ("PICKLE & PARATHA", "Nos", 3412, 0, 482, 0.899, 433.47, 2930, 2634.97),
    ("TAPE", "Nos", 9, 0, 2, 23.600, 47.20, 7, 165.20),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 329, 0, 61, 3.150, 192.15, 268, 844.20),
    ("PAPER BOX (LUNCH)", "Nos", 6392, 0, 411, 4.956, 2036.92, 5981, 29641.84),
    ("BUTTER ROTI PAPER", "NOS", 1.200, 0, 0.050, 236.000, 11.80, 1.150, 271.40),
    ("PARATHA BOX", "Nos", 1315, 0, 71, 3.360, 238.56, 1244, 4179.84),
    ("PARTATION BOX", "Nos", 47, 0, 0, 6.960, 0.00, 47, 327.12),
    ("BLACK PACKET", "Nos", 3, 0, 1, 141.600, 141.60, 2, 283.20),
    ("400 ML PP BOX", "Nos", 216, 0, 61, 4.720, 287.92, 155, 731.60),
]

sweets_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 28.500, 0.000, 12.000, 280.000, 3360.000, 16.500, 4620.00),
    ("PETHA", "KGS", 25.000, 0.000, 0.000, 150.000, 0.000, 25.000, 3750.00),
    ("GULDANA", "KGS", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 15.000, 0.000, 15.000, 12.000, 180.000, 0.000, 0.00),
    ("ONION", "Kgs", 112.000, 0.000, 14.000, 23.000, 322.000, 98.000, 2254.00),
    ("TOMATO", "Kgs", 36.000, 0.000, 12.000, 18.000, 216.000, 24.000, 432.00),
    ("GINGER", "Kgs", 1.000, 0.000, 1.000, 80.000, 80.000, 0.000, 0.00),
    ("GARLIC", "Kgs", 0.000, 5.055, 2.000, 132.000, 264.000, 3.055, 403.26),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 0.000, 2.015, 1.015, 55.000, 55.825, 1.000, 55.00),
    ("CORRENDER", "Kgs", 0.000, 0.000, 0.000, 40.000, 0.000, 0.000, 0.00),
    ("CAPSICUM", "Kgs", 15.000, 0.000, 0.000, 31.000, 0.000, 15.000, 465.00),
    ("BEANS", "Kgs", 0.000, 14.975, 0.000, 59.000, 0.000, 14.975, 883.53),
    ("CARROT", "Kgs", 0.000, 25.140, 0.000, 33.000, 0.000, 25.140, 829.62),
    ("CAULI FLOWER", "Kgs", 0.000, 35.360, 0.000, 55.000, 0.000, 35.360, 1944.80),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 0.000, 0.000, 22.000, 0.000, 0.000, 0.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 83.000, 0.000, 14.000, 20.000, 280.000, 69.000, 1380.00),
    ("MATAR", "Kgs", 0.000, 10.000, 10.000, 100.000, 1000.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 13.000, 13.000, 250.000, 3250.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 0.000, 0.000, 35.000, 0.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 411, 410, 70.0, 28700, 26398.0),
    ("PARATHA", 71, 70, 40.0, 2800, 2084.0),
    ("DAHI", 240, 239, 10.0, 2390, 2151.0),
    ("CHACH", 200, 195, 10.0, 1950, 1755.0),
    ("MINI", 61, 60, 50.0, 3000, 1161.0),
    ("AMUL", 1, 1, 25.0, 25, 22.0),
    ("LAHARI JEERA", 13, 13, 10.0, 130, 117.0),
    ("LASSI", 2, 2, 20.0, 40, 38.0),
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
        print("🎉 Database successfully updated for 06 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
