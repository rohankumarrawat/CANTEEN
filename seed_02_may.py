import sqlite3

DATE = "2026-05-02"

dry_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("ATTA", "Kgs", 1301.000, 0.000, 20.000, 31.00, 620.000, 1281.000, 39711.00),
    ("RICE", "Kgs", 863.000, 0.000, 12.000, 65.00, 780.000, 851.000, 55315.00),
    ("R/OIL", "Ltr", 266.000, 0.000, 5.000, 180.92, 904.615, 261.000, 47220.92),
    ("Sarso Dana", "Kgs", 0.500, 0.000, 0.000, 105.00, 0.000, 0.500, 52.50),
    ("RAJMAH", "Kgs", 83.000, 0.000, 0.000, 115.00, 0.000, 83.000, 9545.00),
    ("URD (S)", "Kgs", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("DAL CHANA", "Kgs", 70.000, 0.000, 0.000, 78.00, 0.000, 70.000, 5460.00),
    ("BESAN", "Kgs", 70.000, 0.000, 0.000, 94.50, 0.000, 70.000, 6615.00),
    ("DAL ARHAR", "Kgs", 58.000, 0.000, 0.000, 120.00, 0.000, 58.000, 6960.00),
    ("DAL MASOOR (S)", "Pkt", 18.000, 0.000, 0.000, 85.00, 0.000, 18.000, 1530.00),
    ("URD CRD(CHILKA)", "KGS", 12.000, 0.000, 0.000, 110.00, 0.000, 12.000, 1320.00),
    ("MASUR CRD(Malika)", "Kgs", 16.000, 0.000, 4.000, 85.00, 340.000, 12.000, 1020.00),
    ("MOONG Crd(Chilka)", "Kgs", 18.000, 0.000, 0.000, 110.00, 0.000, 18.000, 1980.00),
    ("URD DHULI", "Kgs", 0.000, 0.000, 0.000, 140.00, 0.000, 0.000, 0.00),
    ("LOBHIYA", "Kgs", 0.000, 0.000, 0.000, 100.00, 0.000, 0.000, 0.00),
    ("JEERA (S)", "Kgs", 1.800, 0.000, 0.100, 315.00, 31.500, 1.700, 535.50),
    ("HALDI PDR", "Kgs", 4.800, 0.000, 0.100, 231.00, 23.100, 4.700, 1085.70),
    ("MIRCHI PDR", "Kgs", 4.900, 0.000, 0.100, 315.00, 31.500, 4.800, 1512.00),
    ("DAL CHINI", "Kgs", 0.450, 0.000, 0.010, 357.00, 3.570, 0.440, 157.08),
    ("LAUNG", "Kgs", 0.320, 0.000, 0.010, 1155.00, 11.550, 0.310, 358.05),
    ("HING", "Nos", 25.000, 0.000, 0.000, 89.25, 0.000, 25.000, 2231.25),
    ("KITCHEN KING", "Kgs", 2.900, 0.000, 0.100, 800.00, 80.000, 2.800, 2240.00),
    ("DEGI MIRCH", "Kgs", 3.000, 0.000, 0.100, 960.00, 96.000, 2.900, 2784.00),
    ("KASURI METHI", "Kgs", 0.900, 0.000, 0.050, 336.00, 16.800, 0.850, 285.60),
    ("GARAM MASALA", "Kgs", 2.900, 0.000, 0.100, 920.00, 92.000, 2.800, 2576.00),
    ("SALT", "Kgs", 64.000, 0.000, 2.000, 28.00, 56.000, 62.000, 1736.00),
    ("DANIYA (S)", "Kgs", 1.700, 0.000, 0.050, 157.50, 7.875, 1.650, 259.88),
    ("JEERA PDR", "Kgs", 2.000, 0.000, 0.000, 420.00, 0.000, 2.000, 840.00),
    ("CHANA MASALA (Pkt)", "Pkt", 1.100, 0.000, 0.000, 736.01, 0.000, 1.100, 809.61),
    ("B ELAICHI", "Kgs", 0.320, 0.000, 0.010, 1995.00, 19.950, 0.310, 618.45),
    ("METHI DANA", "Kgs", 0.370, 0.000, 0.000, 105.00, 0.000, 0.370, 38.85),
    ("RAJMA MASALA", "Pkt", 6.000, 0.000, 0.000, 72.00, 0.000, 6.000, 432.00),
    ("TEJ PATTA", "Kgs", 0.520, 0.000, 0.010, 168.00, 1.680, 0.510, 85.68),
    ("AJINO MOTO", "Kgs", 0.000, 0.000, 0.000, 260.00, 0.000, 0.000, 0.00),
    ("DESI GHEE", "Kgs", 26.000, 0.000, 0.000, 504.00, 0.000, 26.000, 13104.00),
    ("SARSOO", "Kgs", 0.000, 0.000, 0.000, 210.00, 0.000, 0.000, 0.00),
    ("CHAT MASALA (Pkt)", "Pkt", 0.000, 0.000, 0.000, 75.20, 0.000, 0.000, 0.00),
    ("AJWAIN", "Pkt", 1.000, 0.000, 0.010, 252.00, 2.520, 0.990, 249.48),
    ("MIRCHI (S)", "Kgs", 0.700, 0.000, 0.020, 315.00, 6.300, 0.680, 214.20),
    ("CHAT MASALA (Kgs)", "Kgs", 1.700, 0.000, 0.000, 752.00, 0.000, 1.700, 1278.40),
    ("RAJMAH MASALA", "Kgs", 2.000, 0.000, 0.000, 736.00, 0.000, 2.000, 1472.00),
    ("GULAB JAL", "BTL", 6.000, 0.000, 0.000, 66.15, 0.000, 6.000, 396.91),
    ("CHANA MASALA (Pkt) 2", "Pkt", 0.000, 0.000, 0.000, 736.00, 0.000, 0.000, 0.00),
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
    ("DHANIYA PDR", "Kgs", 5.400, 0.000, 0.100, 168.00, 16.800, 5.300, 890.40),
    ("KALI MIRCH( S)", "Kgs", 0.420, 0.000, 0.010, 882.00, 8.820, 0.410, 361.62),
    ("MUMFALI DANA", "Kgs", 19.000, 0.000, 0.000, 157.50, 0.000, 19.000, 2992.50),
    ("SAMBHAR MASALA", "Pkt", 0.000, 0.000, 0.000, 76.00, 0.000, 0.000, 0.00),
    ("LPG", "Kgs", 32.200, 0.000, 8.000, 61.83, 494.648, 24.200, 1496.31),
    ("RAI", "Pkt", 0.000, 0.000, 0.000, 315.00, 0.000, 0.000, 0.00),
    ("SUGAR", "kgs", 0.000, 0.000, 0.000, 49.00, 0.000, 0.000, 0.00),
    ("BAKING PDR", "PKT", 3.000, 0.000, 0.000, 67.20, 0.000, 3.000, 201.60),
    ("SAHI PANEER MASALA (Pkt)", "PKT", 6.000, 0.000, 0.000, 86.50, 0.000, 6.000, 519.00),
    ("SAHI PANEER MASALA (Kgs)", "kgs", 2.000, 0.000, 0.000, 880.00, 0.000, 2.000, 1760.00),
    ("SOYA BEAN BADIYA", "kgs", 24.000, 0.000, 3.000, 94.50, 283.500, 21.000, 1984.50),
    ("JAVTITRI", "Kgs", 0.630, 0.000, 0.010, 2730.00, 27.300, 0.620, 1692.60),
    ("AMCHUR PDR", "Pkt", 0.000, 0.000, 0.000, 273.00, 0.000, 0.000, 0.00),
    ("DAL MAKHANI MASALA", "Pkt", 0.000, 0.000, 0.000, 70.00, 0.000, 0.000, 0.00),
    ("BLACK PEPPER PDR", "Pkt", 0.000, 0.000, 0.000, 120.00, 0.000, 0.000, 0.00),
    ("KHAS KHAS", "PKT", 0.000, 0.000, 0.000, 2100.00, 0.000, 0.000, 0.00),
    ("AACHAR", "Kgs", 5.000, 0.000, 0.000, 147.00, 0.000, 5.000, 735.00),
    ("CREAM", "Kgs", 7.000, 0.000, 0.000, 220.00, 0.000, 7.000, 1540.00),
    ("GUD", "Kgs", 0.000, 0.000, 0.000, 80.00, 0.000, 0.000, 0.00),
]

packaging_items = [
    # (name, unit, bbf, issue, rate, amt, bcf, bcf_amt)
    ("PP BOX (DAL) MINI MEAL", "Nos", 2192.0, 159.0, 3.186, 506.57, 2033.0, 6477.14),
    ("FOIL BOX (RICE,SABJI)", "Nos", 3526.0, 282.0, 1.575, 444.15, 3244.0, 5109.30),
    ("ROTI POUCH", "Nos", 9.100, 0.800, 236.000, 188.80, 8.300, 1958.80),
    ("SALAD PKT", "Nos", 6356.0, 282.0, 0.177, 49.91, 6074.0, 1075.10),
    ("SPOON/MINI MEAL", "Nos", 1668.0, 141.0, 0.504, 71.06, 1527.0, 769.61),
    ("NEPKIN TUSSU PEPAR", "Nos", 5496.0, 141.0, 0.354, 49.91, 5355.0, 1895.67),
    ("SALT POUCH", "Nos", 721.0, 141.0, 0.150, 21.15, 580.0, 87.00),
    ("PICKLE & PARATHA", "Nos", 4736.0, 141.0, 0.899, 126.80, 4595.0, 4132.31),
    ("TAPE", "Nos", 4.0, 0.0, 23.600, 0.00, 4.0, 94.40),
    ("BIG FOIL BOX (BIRIYANI)", "Nos", 167.0, 18.0, 3.150, 56.70, 149.0, 469.35),
    ("PAPER BOX (LUNCH)", "Nos", 7570.0, 141.0, 4.956, 698.80, 7429.0, 36818.12),
    ("BUTTER ROTI PAPER", "NOS", 0.400, 0.100, 236.000, 23.60, 0.300, 70.80), # Wait, BCF AMT is 70.80. 0.3 * 236 = 70.80. Perfect!
    ("PARATHA BOX", "Nos", 1461.0, 0.0, 3.360, 0.00, 1461.0, 4908.96),
    ("PARTATION BOX", "Nos", 47.0, 0.0, 6.960, 0.00, 47.0, 327.12),
    ("BLACK PACKET", "Nos", 2.0, 1.0, 141.600, 141.60, 1.0, 141.60),
    ("400 ML PP BOX", "Nos", 277.0, 0.0, 4.720, 0.00, 277.0, 1307.44),
]

sweets_items = [
    # (name, unit, bbf, issue, rate, amt, bcf, bcf_amt)
    ("SWEET (BURFI)", "KGS", 12.000, 2.500, 280.000, 700.00, 9.500, 2660.00),
    ("PETHA", "KGS", 8.000, 0.000, 150.000, 0.00, 8.000, 1200.00),
]

fresh_items = [
    # (name, unit, bbf, received, issue, rate, amt, bcf, bcf_amt)
    ("POTATO", "Kgs", 50.400, 0.000, 20.400, 12.000, 244.800, 30.000, 360.00),
    ("ONION", "Kgs", 34.095, 107.000, 5.095, 23.000, 117.185, 136.000, 3128.00),
    ("TOMATO", "Kgs", 6.000, 60.000, 6.000, 18.000, 108.000, 60.000, 1080.00),
    ("GINGER", "Kgs", 0.060, 3.000, 0.060, 80.000, 4.800, 3.000, 240.00),
    ("GARLIC", "Kgs", 0.660, 0.000, 0.660, 132.000, 87.120, 0.000, 0.00),
    ("PEAS GREEN", "Kgs", 0.000, 0.000, 0.000, 95.000, 0.000, 0.000, 0.00),
    ("GREEN CHILLI", "Kgs", 0.620, 3.000, 0.620, 60.000, 37.200, 3.000, 180.00),
    ("CORRENDER", "Kgs", 0.800, 1.000, 0.800, 40.000, 32.000, 1.000, 40.00),
    ("CAPSICUM", "Kgs", 0.000, 16.095, 1.095, 31.000, 33.945, 15.000, 465.00),
    ("BEANS", "Kgs", 0.000, 1.075, 1.075, 55.000, 59.125, 0.000, 0.00),
    ("CARROT", "Kgs", 0.000, 0.000, 0.000, 33.000, 0.000, 0.000, 0.00),
    ("CAULI FLOWER", "Kgs", 0.000, 1.070, 1.070, 55.000, 58.850, 0.000, 0.00),
    ("GREEN ONION", "Kgs", 0.000, 0.000, 0.000, 37.000, 0.000, 0.000, 0.00),
    ("BOTTLE GD", "Kgs", 0.000, 90.000, 0.000, 22.000, 0.000, 90.000, 1980.00),
    ("CABBAGE", "Kgs", 0.000, 0.000, 0.000, 44.000, 0.000, 0.000, 0.00),
    ("CUCUMBER", "Kgs", 38.000, 90.000, 8.000, 20.000, 160.000, 120.000, 2400.00),
    ("MATAR", "Kgs", 0.000, 0.000, 0.000, 100.000, 0.000, 0.000, 0.00),
    ("PANEER", "Kgs", 0.000, 0.000, 0.000, 250.000, 0.000, 0.000, 0.00),
    ("LIME S", "Kgs", 0.000, 0.000, 0.000, 198.000, 0.000, 0.000, 0.00),
    ("DAHI", "Kgs", 0.000, 0.000, 0.000, 75.000, 0.000, 0.000, 0.00),
    ("PAV/KULCHA", "Kgs", 0.000, 6.000, 6.000, 35.000, 210.000, 0.000, 0.00),
]

sales_summary = [
    # (name, prepared, sold, rate, income, expdr)
    ("LUNCH", 141, 140, 70.0, 9800.0, 7712.0),
    ("MINI", 18, 18, 50.0, 900.0, 476.0),
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
                # 1. Update/check item in inventory
                cursor.execute("SELECT id, received FROM inventory WHERE item = ? COLLATE NOCASE", (item,))
                row = cursor.fetchone()
                if row:
                    inv_id = row[0]
                    # Update stock, cp, updated
                    new_received = (row[1] or 0.0) + received
                    cursor.execute('''
                        UPDATE inventory
                        SET stock = ?, cp = ?, received = ?, updated = ?
                        WHERE id = ?
                    ''', (bcf, rate, new_received, DATE, inv_id))
                else:
                    # If it doesn't exist, create it (should not happen, but good for safety)
                    cursor.execute('''
                        INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated)
                        VALUES (?, ?, ?, ?, 0.0, ?, ?, ?, ?)
                    ''', (item, category, unit, bcf, bbf, received, rate, DATE))
                    inv_id = cursor.lastrowid
                    cursor.execute('''
                        INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                        VALUES (?, ?, 'Opening', ?, 'Opening balance BBF')
                    ''', (DATE, inv_id, bbf))

                # 2. Log stock ledger & goods received
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
        pkg_items_mapped = [
            (item[0], item[1], item[2], 0.0, item[3], item[4], item[5], item[6], item[7])
            for item in packaging_items
        ]
        process_item_list(pkg_items_mapped, 'Misc')

        print("Processing Sweets items...")
        sw_items_mapped = [
            (item[0], item[1], item[2], 0.0, item[3], item[4], item[5], item[6], item[7])
            for item in sweets_items
        ]
        process_item_list(sw_items_mapped, 'Misc')

        print("Processing Fresh vegetables...")
        process_item_list(fresh_items, 'Fresh')

        print("Processing Sales logs & Menu updates...")
        for meal, prepared, sold, rate, income, expdr in sales_summary:
            # Check if menu item exists
            cursor.execute("SELECT id FROM menu WHERE name = ? COLLATE NOCASE", (meal,))
            menu_row = cursor.fetchone()
            cpu = expdr / prepared
            if menu_row:
                menu_id = menu_row[0]
                cursor.execute("UPDATE menu SET sp = ?, cogs = ?, active = 1 WHERE id = ?", (rate, cpu, menu_id))
            else:
                cursor.execute('''
                    INSERT INTO menu (name, sp, active, cogs)
                    VALUES (?, ?, 1, ?)
                ''', (meal, rate, cpu))
                menu_id = cursor.lastrowid

            # Ingest sale log
            wastage = prepared - sold
            cursor.execute('''
                INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Cash')
            ''', (DATE, menu_id, meal, rate, sold, wastage, expdr))

            # Ingest batch prep
            cursor.execute('''
                INSERT INTO batch_prep (date, menu_id, qty_prepared)
                VALUES (?, ?, ?)
            ''', (DATE, menu_id, prepared))

            # Ingest expenditure log
            cursor.execute('''
                INSERT INTO expenditure (date, amount, category, notes)
                VALUES (?, ?, 'Raw Materials', ?)
            ''', (DATE, expdr, f"Auto-expenditure for {meal} batch"))

        conn.commit()
        print("🎉 Database successfully updated for 02 May 2026!")

    except Exception as e:
        print(f"Error seeding DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
