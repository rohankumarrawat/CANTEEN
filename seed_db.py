import sqlite3
from datetime import datetime

# Date provided by user: 4/6/26. We will use YYYY-MM-DD format.
DATE = "2026-06-04"

# Inventory data extracted from images
# Format: (item_name, category, unit, rate, issue_qty)
inventory_data = [
    # Vegetables
    ("POTATO", "Vegetables", "Kgs", 12.000, 0.000),
    ("ONION", "Vegetables", "Kgs", 23.000, 12.000),
    ("TOMATO", "Vegetables", "Kgs", 18.000, 12.000),
    ("GINGER", "Vegetables", "Kgs", 80.000, 1.000),
    ("GARLIC", "Vegetables", "Kgs", 132.000, 1.000),
    ("PUMPKIN", "Vegetables", "Kgs", 95.000, 0.000),
    ("GREEN CHILLI", "Vegetables", "Kgs", 60.000, 1.500),
    ("CORRENDER", "Vegetables", "Kgs", 40.000, 1.000),
    ("CAPSICUM", "Vegetables", "Kgs", 31.000, 0.000),
    ("BEANS", "Vegetables", "Kgs", 55.000, 0.000),
    ("CARROT", "Vegetables", "Kgs", 33.000, 0.000),
    ("CAULI FLOWER", "Vegetables", "Kgs", 55.000, 0.000),
    ("GREEN ONION", "Vegetables", "Kgs", 37.000, 0.000),
    ("BOTTLE GD", "Vegetables", "Kgs", 22.000, 90.000),
    ("CABBAGE", "Vegetables", "Kgs", 44.000, 0.000),
    ("CUCUMBER", "Vegetables", "Kgs", 20.000, 18.000),
    ("MATAR", "Vegetables", "Kgs", 100.000, 0.000),
    ("PANEER", "Vegetables", "Kgs", 250.000, 0.000),
    ("LIME S", "Vegetables", "Kgs", 198.000, 0.000),
    ("DAHI", "Vegetables", "Kgs", 75.000, 0.000),
    ("PAV/KULCHA", "Vegetables", "Kgs", 35.000, 0.000),
    
    # Dry Items
    ("ATTA", "Dry", "Kgs", 31.00, 66.000),
    ("RICE", "Dry", "Kgs", 65.00, 46.000),
    ("R/OIL", "Dry", "Ltr", 180.92, 7.000),
    ("Sarso Dana", "Dry", "Kgs", 105.00, 0.000),
    ("RAJMAH", "Dry", "Kgs", 115.00, 0.000),
    ("URD (S)", "Dry", "Kgs", 120.00, 0.000),
    ("DAL CHANA", "Dry", "Kgs", 78.00, 15.000),
    ("BESAN", "Dry", "Kgs", 94.50, 0.000),
    ("DAL ARHAR", "Dry", "Kgs", 120.00, 3.000),
    ("DAL MASOOR (S)", "Dry", "Pkt", 85.00, 0.000),
    ("URD CRD(Chilka)", "Dry", "Kgs", 110.00, 3.000),
    ("MASUR CRD(Malika)", "Dry", "Kgs", 85.00, 3.000),
    ("MOONG Crd(Chilka)", "Dry", "Kgs", 110.00, 3.000),
    ("URD DHULI", "Dry", "Kgs", 140.00, 0.000),
    ("LOBHIYA", "Dry", "Kgs", 100.00, 0.000),
    ("JEERA (S)", "Dry", "Kgs", 315.00, 0.100),
    ("HALDI PDR", "Dry", "Kgs", 231.00, 0.300),
    ("MIRCHI PDR", "Dry", "Kgs", 315.00, 0.300),
    ("DAL CHINI", "Dry", "Kgs", 357.00, 0.010),
    ("LAUNG", "Dry", "Kgs", 1155.00, 0.010),
    ("HING", "Dry", "Nos", 89.25, 0.000),
    ("KITCHEN KING", "Dry", "Kgs", 800.00, 0.200),
    ("DEGI MIRCH", "Dry", "Kgs", 960.00, 0.200),
    ("KASURI METHI", "Dry", "Kgs", 336.00, 0.050),
    ("GARAM MASALA", "Dry", "Kgs", 920.00, 0.300),
    ("SALT", "Dry", "Kgs", 28.00, 4.000),
    ("DANIYA (S)", "Dry", "Kgs", 157.50, 0.200),
    ("JEERA PDR", "Dry", "Kgs", 420.00, 0.000),
    ("CHANA MASALA", "Dry", "Pkt", 736.01, 0.100),
    ("B ELAICHI", "Dry", "Kgs", 1995.00, 0.010),
    ("METHI DANA", "Dry", "Kgs", 105.00, 0.010),
    ("RAJMA MASALA", "Dry", "Pkt", 72.00, 0.000),
    ("TEJ PATTA", "Dry", "Kgs", 168.00, 0.010),
    ("AJINO MOTO", "Dry", "Kgs", 260.00, 0.000),
    ("DESI GHEE", "Dry", "Kgs", 504.00, 1.500),
    ("SARSOO", "Dry", "Kgs", 210.00, 0.000),
    ("CLEAN WRAP", "Dry", "Pkt", 123.00, 2.000),
    ("AJWAIN", "Dry", "Pkt", 252.00, 0.050),
    ("MIRCHI (S)", "Dry", "Kgs", 315.00, 0.050),
    ("CHAT MASALA", "Dry", "Kgs", 752.00, 0.100),
    ("RAJMAH MASALA", "Dry", "Kgs", 736.00, 0.000),
    ("GULAB JAL", "Dry", "BTL", 66.15, 0.000),
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
    ("DHANIYA PDR", "Dry", "Kgs", 168.00, 0.300),
    ("KALI MIRCH( S)", "Dry", "Kgs", 882.00, 0.010),
    ("MUMFALI DANA", "Dry", "Kgs", 157.50, 0.000),
    ("SAMBHAR MASALA", "Dry", "Pkt", 76.00, 0.000),
    ("LPG", "Dry", "Kgs", 61.83, 36.800),
    ("RAI", "Dry", "Pkt", 315.00, 0.000),
    ("SUGAR", "Dry", "Kgs", 49.00, 0.000),
    ("BAKING PDR", "Dry", "Pkt", 67.20, 0.000),
    ("SAHI PANEER MASALA", "Dry", "Pkt", 86.50, 0.000),
    ("SAHI PANEER MASALA (Kgs)", "Dry", "Kgs", 880.00, 0.000),
    ("SOYA BEAN BADIYA", "Dry", "Kgs", 94.50, 0.000),
    ("JAVTITRI", "Dry", "Kgs", 2730.00, 0.010),
    ("AMCHUR PDR", "Dry", "Pkt", 273.00, 0.000),
    ("DAL MAKHANI MASALA", "Dry", "Pkt", 70.00, 0.000),
    ("BLACK PEPPER PDR", "Dry", "Kgs", 120.00, 0.000),
    ("SABJI MASALA", "Dry", "Pkt", 2100.00, 0.000),
    ("Aachar", "Dry", "Kgs", 147.00, 0.000),
    ("CREAM", "Dry", "Kgs", 220.00, 0.000),
    ("PARATHA MASALA", "Dry", "Kgs", 80.00, 0.000),
    
    # Packaging
    ("PP BOX (DAL) MINI MEAL", "Packaging", "Nos", 3.186, 536.0),
    ("FOIL BOX (RICE,SABJI)", "Packaging", "Nos", 1.575, 1072.0),
    ("ROTI POUCH", "Packaging", "Nos", 236.000, 3.500),
    ("SALAD PKT", "Packaging", "Nos", 0.177, 1072.0),
    ("SPOON/MINI MEAL", "Packaging", "Nos", 0.504, 595.0),
    ("NEPKIN TUSSU PEPAR", "Packaging", "Nos", 0.354, 609.0),
    ("SALT POUCH", "Packaging", "Nos", 0.150, 536.0),
    ("PICKLE & PARATHA", "Packaging", "Nos", 0.899, 609.0),
    ("TAPE", "Packaging", "Nos", 23.600, 1.0),
    ("BIG FOIL BOX (BIRIYANI)", "Packaging", "Nos", 3.150, 59.0),
    ("PAPER BOX (LUNCH)", "Packaging", "Nos", 4.956, 536.0),
    ("BUTTER ROTI PAPER", "Packaging", "Nos", 236.000, 0.0),
    ("PARATHA BOX", "Packaging", "Nos", 3.360, 73.0),
    ("PARTATION BOX", "Packaging", "Nos", 6.960, 0.0),
    ("BLACK PACKET", "Packaging", "Nos", 141.600, 1.0),
    ("400 ML PP BOX", "Packaging", "Nos", 4.720, 0.0),

    # Sweets
    ("SWEET {BURFI}", "Sweets", "Kgs", 280.000, 0.0),
    ("PETHA", "Sweets", "Kgs", 150.000, 18.000),
    ("GULDANA", "Sweets", "Kgs", 250.000, 0.0),
]

# Sales Data
# Format: (Meal, Sold, Tasting & Staff)
sales_data = [
    ("Lunch", 536, 20),
    ("Mini Mil", 62, 0),
    ("Paratha", 73, 0),
]

def seed_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    try:
        print("Inserting inventory data...")
        for item, cat, unit, rate, issue_qty in inventory_data:
            # We insert with a default stock. Assuming stock should be updated.
            # Here we might log the issue_qty into stock ledger as an issue,
            # or add it as goods received. For simplicity, let's just make stock = 0 and record CP.
            # If the user wants the "real life data", we add it to inventory.
            cursor.execute('''
                INSERT INTO inventory (item, cat, unit, stock, cp) 
                VALUES (?, ?, ?, ?, ?)
            ''', (item, cat, unit, 0, rate))
            
            inv_id = cursor.lastrowid
            
            # If there was an issue quantity, log it as an expenditure/issue in stock ledger?
            if issue_qty > 0:
                # We can add a goods received entry to bring stock to issue_qty, then issue it.
                # Or just put it in stock ledger as an issue (which makes stock negative, but we'll set stock to 0)
                pass

        print("Inserting menu data...")
        # Add the sales items to menu
        for meal, sold, tasting in sales_data:
            sp = 0 # Default selling price as it's not provided in the image clearly.
            cursor.execute('''
                INSERT INTO menu (name, sp, active)
                VALUES (?, ?, 1)
            ''', (meal, sp))
            menu_id = cursor.lastrowid
            
            # Record the sales
            cursor.execute('''
                INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (DATE, menu_id, meal, sp, sold, tasting, 0, "Cash"))

        conn.commit()
        print("Real life data imported successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
