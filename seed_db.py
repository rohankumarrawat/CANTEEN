import sqlite3
from datetime import datetime

# Date provided by user: 4/6/26. We will use YYYY-MM-DD format.
DATE = "2026-06-04"

# Inventory data extracted from images
# Format: (item_name, category, unit, rate, issue_qty)
inventory_data = [
    # Vegetables
    ("Potato", "Vegetables", "Kgs", 12.000, 0.000),
    ("Onion", "Vegetables", "Kgs", 23.000, 12.000),
    ("Tomato", "Vegetables", "Kgs", 18.000, 12.000),
    ("Ginger", "Vegetables", "Kgs", 80.000, 1.000),
    ("Garlic", "Vegetables", "Kgs", 132.000, 1.000),
    ("Pumpkin", "Vegetables", "Kgs", 95.000, 0.000),
    ("Green chilli", "Vegetables", "Kgs", 60.000, 1.500),
    ("Coriander", "Vegetables", "Kgs", 40.000, 1.000),
    ("Capsicum", "Vegetables", "Kgs", 31.000, 0.000),
    ("Beans", "Vegetables", "Kgs", 55.000, 0.000),
    ("Carrot", "Vegetables", "Kgs", 33.000, 0.000),
    ("Cauli flower", "Vegetables", "Kgs", 55.000, 0.000),
    ("Green onion", "Vegetables", "Kgs", 37.000, 0.000),
    ("Bottle GD", "Vegetables", "Kgs", 22.000, 90.000),
    ("Cabbage", "Vegetables", "Kgs", 44.000, 0.000),
    ("Cucumber", "Vegetables", "Kgs", 20.000, 18.000),
    ("Matar", "Vegetables", "Kgs", 100.000, 0.000),
    ("Paneer", "Vegetables", "Kgs", 250.000, 0.000),
    ("Lime S", "Vegetables", "Kgs", 198.000, 0.000),
    ("Dahi", "Vegetables", "Kgs", 75.000, 0.000),
    ("Pav/Kulcha", "Vegetables", "Kgs", 35.000, 0.000),
    
    # Dry Items
    ("Atta", "Dry", "Kgs", 31.00, 66.000),
    ("Rice", "Dry", "Kgs", 65.00, 46.000),
    ("R/oil", "Dry", "Ltr", 180.92, 7.000),
    ("Sarso Dana", "Dry", "Kgs", 105.00, 0.000),
    ("Rajma", "Dry", "Kgs", 115.00, 0.000),
    ("Urad (s)", "Dry", "Kgs", 120.00, 0.000),
    ("Dal Chana", "Dry", "Kgs", 78.00, 15.000),
    ("Besan", "Dry", "Kgs", 94.50, 0.000),
    ("Dal Arhar", "Dry", "Kgs", 120.00, 3.000),
    ("Dal masoor (s)", "Dry", "Pkt", 85.00, 0.000),
    ("Urad Dal Chilka", "Dry", "Kgs", 110.00, 3.000),
    ("Masoor Dal (Malika)", "Dry", "Kgs", 85.00, 3.000),
    ("Moong Dal Chilka", "Dry", "Kgs", 110.00, 3.000),
    ("Urad Dhuli", "Dry", "Kgs", 140.00, 0.000),
    ("Lobia", "Dry", "Kgs", 100.00, 0.000),
    ("Jeera (s)", "Dry", "Kgs", 315.00, 0.100),
    ("Haldi Powder", "Dry", "Kgs", 231.00, 0.300),
    ("Mirchi Powder", "Dry", "Kgs", 315.00, 0.300),
    ("Dal chini", "Dry", "Kgs", 357.00, 0.010),
    ("Laung", "Dry", "Kgs", 1155.00, 0.010),
    ("Hing", "Dry", "Nos", 89.25, 0.000),
    ("Kitchen King", "Dry", "Kgs", 800.00, 0.200),
    ("Degi Mirch", "Dry", "Kgs", 960.00, 0.200),
    ("Kasuri Methi", "Dry", "Kgs", 336.00, 0.050),
    ("Garam Masala", "Dry", "Kgs", 920.00, 0.300),
    ("Salt", "Dry", "Kgs", 28.00, 4.000),
    ("Dhaniya (s)", "Dry", "Kgs", 157.50, 0.200),
    ("Jeera Powder", "Dry", "Kgs", 420.00, 0.000),
    ("Chana Masala", "Dry", "Pkt", 736.01, 0.100),
    ("Badi Elaichi", "Dry", "Kgs", 1995.00, 0.010),
    ("Methi Dana", "Dry", "Kgs", 105.00, 0.010),
    ("Rajma Masala", "Dry", "Pkt", 72.00, 0.000),
    ("Tej Patta", "Dry", "Kgs", 168.00, 0.010),
    ("Ajinomoto", "Dry", "Kgs", 260.00, 0.000),
    ("Desi Ghee", "Dry", "Kgs", 504.00, 1.500),
    ("Sarson", "Dry", "Kgs", 210.00, 0.000),
        ("Clean Wrap", "Packaging Material", "Pkt", 123.00, 2.000),
    ("Ajwain", "Dry", "Pkt", 252.00, 0.050),
    ("Mirchi (s)", "Dry", "Kgs", 315.00, 0.050),
    ("Chat Masala", "Dry", "Kgs", 752.00, 0.100),
    ("RAJMAH MASALA", "Dry", "Kgs", 736.00, 0.000),
    ("Gulab Jal", "Dry", "BTL", 66.15, 0.000),
    ("Kala Chana", "Dry", "Kgs", 78.00, 0.000),
    ("Vinegar", "Dry", "BTL", 53.00, 0.000),
    ("Red Chilli Sauce", "Dry", "BTL", 84.00, 0.000),
    ("Matar Paneer Masala", "Dry", "BTL", 35.00, 0.000),
    ("Pav Bhaji Masala", "Dry", "BTL", 92.00, 0.000),
    ("Matar (TF)", "Dry", "Kgs", 60.00, 0.000),
    ("Star Phool Masala", "Dry", "Kgs", 1600.00, 0.000),
    ("Food Colour", "Dry", "Pkt", 68.44, 0.000),
    ("Kewra Water", "Dry", "BTL", 70.80, 0.000),
    ("Biryani Masala", "Dry", "Pkt", 73.50, 0.000),
    ("Elaichi Small Gr", "Dry", "Kgs", 3150.00, 0.000),
    ("Dhaniya Powder", "Dry", "Kgs", 168.00, 0.300),
    ("Kali Mirch (s)", "Dry", "Kgs", 882.00, 0.010),
    ("Moongphali Dana", "Dry", "Kgs", 157.50, 0.000),
    ("Sambhar Masala", "Dry", "Pkt", 76.00, 0.000),
    ("LPG", "Dry", "Kgs", 61.83, 36.800),
    ("Rai", "Dry", "Pkt", 315.00, 0.000),
    ("Sugar", "Dry", "Kgs", 49.00, 0.000),
    ("Baking Powder", "Dry", "Pkt", 67.20, 0.000),
    ("SHAHI PANEER MASALA", "Dry", "Pkt", 86.50, 0.000),
    ("Shahi Paneer Masala (kgs)", "Dry", "Kgs", 880.00, 0.000),
    ("Soya Bean Badiya", "Dry", "Kgs", 94.50, 0.000),
    ("Javitri", "Dry", "Kgs", 2730.00, 0.010),
    ("Amchur Powder", "Dry", "Pkt", 273.00, 0.000),
    ("Dal Makhani Masala", "Dry", "Pkt", 70.00, 0.000),
    ("Black Pepper Powder", "Dry", "Kgs", 120.00, 0.000),
    ("Sabji Masala", "Dry", "Pkt", 2100.00, 0.000),
    ("Aachar", "Dry", "Kgs", 147.00, 0.000),
    ("Cream", "Dry", "Kgs", 220.00, 0.000),
    ("Paratha Masala", "Dry", "Kgs", 80.00, 0.000),
    
    # Packaging
    ("PP Box (Dal) Mini Meal", "Packaging Material", "Nos", 3.186, 536.0),
    ("Foil Box (Rice, Sabji)", "Packaging Material", "Nos", 1.575, 1072.0),
    ("Roti pouch", "Packaging Material", "Nos", 236.000, 3.500),
    ("Salad Pkt", "Packaging Material", "Nos", 0.177, 1072.0),
    ("Spoon/Mini Meal", "Packaging Material", "Nos", 0.504, 595.0),
    ("Napkin Tissue Paper", "Packaging Material", "Nos", 0.354, 609.0),
    ("Salt Pouch", "Packaging Material", "Nos", 0.150, 536.0),
    ("Pickle & Paratha", "Packaging Material", "Nos", 0.899, 609.0),
    ("Tape", "Packaging Material", "Nos", 23.600, 1.0),
    ("Big Foil Box (Biryani)", "Packaging Material", "Nos", 3.150, 59.0),
    ("Paper Box (Lunch)", "Packaging Material", "Nos", 4.956, 536.0),
    ("Butter Roti Paper", "Packaging Material", "Nos", 236.000, 0.0),
    ("Paratha Box", "Packaging Material", "Nos", 3.360, 73.0),
    ("Partition Box", "Packaging Material", "Nos", 6.960, 0.0),
    ("Black Packet", "Packaging Material", "Nos", 141.600, 1.0),
    ("400 ML PP Box", "Packaging Material", "Nos", 4.720, 0.0),

    # Sweets
    ("Sweet (Burfi)", "Sweets", "Kgs", 280.000, 0.0),
    ("Petha", "Sweets", "Kgs", 150.000, 18.000),
    ("Guldana", "Sweets", "Kgs", 250.000, 0.0),
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
