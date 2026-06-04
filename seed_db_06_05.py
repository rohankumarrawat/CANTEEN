import sqlite3

DATE = "2026-05-06"

inventory_data = [
    # Vegetables (from 06-05-2026 image)
    ("POTATO", "Vegetables", "Kgs", 12.000, 15.000),
    ("ONION", "Vegetables", "Kgs", 23.000, 14.000),
    ("TOMATO", "Vegetables", "Kgs", 18.000, 12.000),
    ("GINGER", "Vegetables", "Kgs", 80.000, 1.000),
    ("GARLIC", "Vegetables", "Kgs", 132.000, 2.000),
    ("PUMPKIN", "Vegetables", "Kgs", 95.000, 0.000),
    ("GREEN CHILLI", "Vegetables", "Kgs", 55.000, 1.015),
    ("CORRENDER", "Vegetables", "Kgs", 40.000, 0.000),
    ("CAPSICUM", "Vegetables", "Kgs", 31.000, 0.000),
    ("BEANS", "Vegetables", "Kgs", 59.000, 0.000),
    ("CARROT", "Vegetables", "Kgs", 33.000, 0.000),
    ("CAULI FLOWER", "Vegetables", "Kgs", 55.000, 0.000),
    ("GREEN ONION", "Vegetables", "Kgs", 37.000, 0.000),
    ("BOTTLE GD", "Vegetables", "Kgs", 22.000, 0.000),
    ("CABBAGE", "Vegetables", "Kgs", 44.000, 0.000),
    ("CUCUMBER", "Vegetables", "Kgs", 20.000, 14.000),
    ("MATAR", "Vegetables", "Kgs", 100.000, 10.000),
    ("PANEER", "Vegetables", "Kgs", 250.000, 13.000),
    ("LIME S", "Vegetables", "Kgs", 198.000, 0.000),
    ("DAHI", "Vegetables", "Kgs", 75.000, 0.000),
    ("PAV/KULCHA", "Vegetables", "Kgs", 35.000, 0.000),
    
    # Dry Items (from 06-05-2026 image)
    ("ATTA", "Dry", "Kgs", 31.00, 52.000),
    ("RICE", "Dry", "Kgs", 65.00, 40.000),
    ("R/OIL", "Dry", "Ltr", 180.92, 12.000),
    ("Sarso Dana", "Dry", "Kgs", 105.00, 0.000),
    ("RAJMAH", "Dry", "Kgs", 115.00, 18.000),
    ("URD (S)", "Dry", "Kgs", 120.00, 0.000),
    ("DAL CHANA", "Dry", "Kgs", 78.00, 0.000),
    ("BESAN", "Dry", "Kgs", 94.50, 6.000),
    ("DAL ARHAR", "Dry", "Kgs", 120.00, 0.000),
    ("DAL MASOOR (S)", "Dry", "Pkt", 85.00, 0.000),
    ("URD CRD(Chilka)", "Dry", "Kgs", 110.00, 0.000),
    ("MASUR CRD(Malika)", "Dry", "Kgs", 85.00, 0.000),
    ("MOONG Crd(Chilka)", "Dry", "Kgs", 110.00, 0.000),
    ("URD DHULI", "Dry", "Kgs", 140.00, 0.000),
    ("LOBHIYA", "Dry", "Kgs", 100.00, 0.000),
    ("JEERA (S)", "Dry", "Kgs", 315.00, 0.300),
    ("HALDI PDR", "Dry", "Kgs", 231.00, 0.300),
    ("MIRCHI PDR", "Dry", "Kgs", 315.00, 0.300),
    ("DAL CHINI", "Dry", "Kgs", 357.00, 0.010),
    ("LAUNG", "Dry", "Kgs", 1155.00, 0.010),
    ("HING", "Dry", "Nos", 89.25, 0.000),
    ("KITCHEN KING", "Dry", "Kgs", 800.00, 0.200),
    ("DEGI MIRCH", "Dry", "Kgs", 960.00, 0.200),
    ("KASURI METHI", "Dry", "Kgs", 336.00, 0.050),
    ("GARAM MASALA", "Dry", "Kgs", 920.00, 0.200),
    ("SALT", "Dry", "Kgs", 28.00, 3.000),
    ("DANIYA (S)", "Dry", "Kgs", 157.50, 0.050),
    ("JEERA PDR", "Dry", "Kgs", 420.00, 0.400),
    ("CHANA MASALA", "Dry", "Pkt", 736.01, 0.000),
    ("B ELAICHI", "Dry", "Kgs", 1995.00, 0.010),
    ("METHI DANA", "Dry", "Kgs", 105.00, 0.000),
    ("RAJMA MASALA", "Dry", "Pkt", 72.00, 4.000),
    ("TEJ PATTA", "Dry", "Kgs", 168.00, 0.010),
    ("AJINO MOTO", "Dry", "Kgs", 260.00, 0.000),
    ("DESI GHEE", "Dry", "Kgs", 504.00, 1.000),
    ("SARSOO", "Dry", "Kgs", 210.00, 0.000),
    ("CLEAN WRAP", "Dry", "Pkt", 450.00, 0.500),
    ("AJWAIN", "Dry", "Pkt", 252.00, 0.050),
    ("MIRCHI (S)", "Dry", "Kgs", 315.00, 0.050),
    ("CHAT MASALA", "Dry", "Kgs", 752.00, 0.100),
    ("RAJMAH MASALA", "Dry", "Kgs", 736.00, 0.000),
    ("GULAB JAL", "Dry", "BTL", 66.15, 0.000),
    ("CHANA MASALA", "Dry", "Pkt", 736.00, 0.000),
    ("KALA CHANA", "Dry", "Kgs", 78.00, 0.000),
    ("VINAYGER", "Dry", "BTL", 53.00, 0.000),
    ("RED CHILLI SAUCE", "Dry", "BTL", 84.00, 0.000),
    ("MATAR PANEER MASALA", "Dry", "BTL", 35.00, 0.000),
    ("PAV BHAJI MASALA", "Dry", "BTL", 92.00, 0.000),
    ("MATAR TF", "Dry", "Kgs", 60.00, 0.000),
    ("STAR FOOL MASALA", "Dry", "Kgs", 1600.00, 0.000),
    ("FOOD COLOUR", "Dry", "Pkt", 68.44, 0.000),
    ("KEVADA WATER", "Dry", "BTL", 70.80, 0.000),
    ("BIRIYANI MASALA", "Dry", "Pkt", 73.50, 0.000),
    ("ilaychi small Gr", "Dry", "Kgs", 3150.00, 0.000),
    ("DHANIYA PDR", "Dry", "Kgs", 168.00, 0.200),
    ("KALI MIRCH( S)", "Dry", "Kgs", 882.00, 0.010),
    ("MUMFALI DANA", "Dry", "Kgs", 157.50, 2.000),
    ("SAMBHAR MASALA", "Dry", "Pkt", 76.00, 0.000),
    ("LPG", "Dry", "Kgs", 61.83, 20.600),
    ("RAI", "Dry", "Pkt", 315.00, 0.000),
    ("SUGAR", "Dry", "Kgs", 49.00, 0.000),
    ("BAKING PDR", "Dry", "Pkt", 67.20, 0.000),
    ("SAHI PANEER MASALA", "Dry", "Pkt", 86.50, 4.000),
    ("SAHI PANEER MASALA (Kgs)", "Dry", "Kgs", 880.00, 0.000),
    ("SOYA BEAN BADIYA", "Dry", "Kgs", 94.50, 0.000),
    ("JAVTITRI", "Dry", "Kgs", 2730.00, 0.020),
    ("AMCHUR PDR", "Dry", "Pkt", 273.00, 0.000),
    ("DAL MAKHANI MASALA", "Dry", "Pkt", 70.00, 0.000),
    ("BLACK PEPPER PDR", "Dry", "Kgs", 120.00, 0.000),
    ("SABJI MASALA", "Dry", "Pkt", 2100.00, 0.000),
    ("Aachar", "Dry", "Kgs", 147.00, 0.000),
    ("CREAM", "Dry", "Kgs", 220.00, 0.500),
    ("PARATHA MASALA", "Dry", "Kgs", 80.00, 0.000),
    
    # Packaging
    ("PP BOX (DAL) MINI MEAL", "Packaging", "Nos", 3.186, 411.0),
    ("FOIL BOX (RICE,SABJI)", "Packaging", "Nos", 1.575, 822.0),
    ("ROTI POUCH", "Packaging", "Nos", 236.000, 2.800),
    ("SALAD PKT", "Packaging", "Nos", 0.177, 822.0),
    ("SPOON/MINI MEAL", "Packaging", "Nos", 0.504, 472.0),
    ("NEPKIN TUSSU PEPAR", "Packaging", "Nos", 0.354, 411.0),
    ("SALT POUCH", "Packaging", "Nos", 0.150, 411.0),
    ("PICKLE & PARATHA", "Packaging", "Nos", 0.899, 482.0),
    ("TAPE", "Packaging", "Nos", 23.600, 2.0),
    ("BIG FOIL BOX (BIRIYANI)", "Packaging", "Nos", 3.150, 61.0),
    ("PAPER BOX (LUNCH)", "Packaging", "Nos", 4.956, 411.0),
    ("BUTTER ROTI PAPER", "Packaging", "Nos", 236.000, 0.0),
    ("PARATHA BOX", "Packaging", "Nos", 3.360, 71.0),
    ("PARTATION BOX", "Packaging", "Nos", 6.960, 0.0),
    ("BLACK PACKET", "Packaging", "Nos", 141.600, 1.0),
    ("400 ML PP BOX", "Packaging", "Nos", 4.720, 61.0),

    # Sweets
    ("SWEET {BURFI}", "Sweets", "Kgs", 280.000, 12.000),
    ("PETHA", "Sweets", "Kgs", 150.000, 0.000),
    ("GULDANA", "Sweets", "Kgs", 250.000, 0.000),
]

sales_data = [
    ("Lunch", 411, 20),
    ("Mini Mil", 62, 0),
    ("Paratha", 73, 0),
]

def update_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    try:
        print("Updating inventory data rates...")
        for item, cat, unit, rate, issue_qty in inventory_data:
            # Check if item exists
            cursor.execute("SELECT id FROM inventory WHERE item = ?", (item,))
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE inventory SET cp = ? WHERE id = ?", (rate, row[0]))
            else:
                cursor.execute('''
                    INSERT INTO inventory (item, cat, unit, stock, cp) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (item, cat, unit, 0, rate))

        print("Recording sales data...")
        for meal, sold, tasting in sales_data:
            cursor.execute("SELECT id FROM menu WHERE name = ?", (meal,))
            row = cursor.fetchone()
            if row:
                menu_id = row[0]
            else:
                cursor.execute('''
                    INSERT INTO menu (name, sp, active)
                    VALUES (?, 0, 1)
                ''', (meal,))
                menu_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (DATE, menu_id, meal, 0, sold, tasting, 0, "Cash"))

        conn.commit()
        print("Data for 2026-05-06 added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_db()
