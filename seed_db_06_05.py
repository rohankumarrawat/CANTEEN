import sqlite3

DATE = "2026-05-06"

inventory_data = [
    # Vegetables (from 06-05-2026 image)
    ("Potato", "Vegetables", "Kgs", 12.000, 15.000),
    ("Onion", "Vegetables", "Kgs", 23.000, 14.000),
    ("Tomato", "Vegetables", "Kgs", 18.000, 12.000),
    ("Ginger", "Vegetables", "Kgs", 80.000, 1.000),
    ("Garlic", "Vegetables", "Kgs", 132.000, 2.000),
    ("Pumpkin", "Vegetables", "Kgs", 95.000, 0.000),
    ("Green chilli", "Vegetables", "Kgs", 55.000, 1.015),
    ("Coriander", "Vegetables", "Kgs", 40.000, 0.000),
    ("Capsicum", "Vegetables", "Kgs", 31.000, 0.000),
    ("Beans", "Vegetables", "Kgs", 59.000, 0.000),
    ("Carrot", "Vegetables", "Kgs", 33.000, 0.000),
    ("Cauli flower", "Vegetables", "Kgs", 55.000, 0.000),
    ("Green onion", "Vegetables", "Kgs", 37.000, 0.000),
    ("Bottle GD", "Vegetables", "Kgs", 22.000, 0.000),
    ("Cabbage", "Vegetables", "Kgs", 44.000, 0.000),
    ("Cucumber", "Vegetables", "Kgs", 20.000, 14.000),
    ("Matar", "Vegetables", "Kgs", 100.000, 10.000),
    ("Paneer", "Vegetables", "Kgs", 250.000, 13.000),
    ("Lime S", "Vegetables", "Kgs", 198.000, 0.000),
    ("Dahi", "Vegetables", "Kgs", 75.000, 0.000),
    ("Pav/Kulcha", "Vegetables", "Kgs", 35.000, 0.000),
    
    # Dry Items (from 06-05-2026 image)
    ("Atta", "Dry", "Kgs", 31.00, 52.000),
    ("Rice", "Dry", "Kgs", 65.00, 40.000),
    ("R/oil", "Dry", "Ltr", 180.92, 12.000),
    ("Sarso Dana", "Dry", "Kgs", 105.00, 0.000),
    ("Rajma", "Dry", "Kgs", 115.00, 18.000),
    ("Urad (s)", "Dry", "Kgs", 120.00, 0.000),
    ("Dal Chana", "Dry", "Kgs", 78.00, 0.000),
    ("Besan", "Dry", "Kgs", 94.50, 6.000),
    ("Dal Arhar", "Dry", "Kgs", 120.00, 0.000),
    ("Dal masoor (s)", "Dry", "Pkt", 85.00, 0.000),
    ("Urad Dal Chilka", "Dry", "Kgs", 110.00, 0.000),
    ("Masoor Dal (Malika)", "Dry", "Kgs", 85.00, 0.000),
    ("Moong Dal Chilka", "Dry", "Kgs", 110.00, 0.000),
    ("Urad Dhuli", "Dry", "Kgs", 140.00, 0.000),
    ("Lobia", "Dry", "Kgs", 100.00, 0.000),
    ("Jeera (s)", "Dry", "Kgs", 315.00, 0.300),
    ("Haldi Powder", "Dry", "Kgs", 231.00, 0.300),
    ("Mirchi Powder", "Dry", "Kgs", 315.00, 0.300),
    ("Dal chini", "Dry", "Kgs", 357.00, 0.010),
    ("Laung", "Dry", "Kgs", 1155.00, 0.010),
    ("Hing", "Dry", "Nos", 89.25, 0.000),
    ("Kitchen King", "Dry", "Kgs", 800.00, 0.200),
    ("Degi Mirch", "Dry", "Kgs", 960.00, 0.200),
    ("Kasuri Methi", "Dry", "Kgs", 336.00, 0.050),
    ("Garam Masala", "Dry", "Kgs", 920.00, 0.200),
    ("Salt", "Dry", "Kgs", 28.00, 3.000),
    ("Dhaniya (s)", "Dry", "Kgs", 157.50, 0.050),
    ("Jeera Powder", "Dry", "Kgs", 420.00, 0.400),
    ("Chana Masala", "Dry", "Pkt", 736.01, 0.000),
    ("Badi Elaichi", "Dry", "Kgs", 1995.00, 0.010),
    ("Methi Dana", "Dry", "Kgs", 105.00, 0.000),
    ("Rajma Masala", "Dry", "Pkt", 72.00, 4.000),
    ("Tej Patta", "Dry", "Kgs", 168.00, 0.010),
    ("Ajinomoto", "Dry", "Kgs", 260.00, 0.000),
    ("Desi Ghee", "Dry", "Kgs", 504.00, 1.000),
    ("Sarson", "Dry", "Kgs", 210.00, 0.000),
        ("Clean Wrap", "Package material", "Pkt", 450.00, 0.500),
    ("Ajwain", "Dry", "Pkt", 252.00, 0.050),
    ("Mirchi (s)", "Dry", "Kgs", 315.00, 0.050),
    ("Chat Masala", "Dry", "Kgs", 752.00, 0.100),
    ("RAJMAH MASALA", "Dry", "Kgs", 736.00, 0.000),
    ("Gulab Jal", "Dry", "BTL", 66.15, 0.000),
    ("Chana Masala", "Dry", "Pkt", 736.00, 0.000),
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
    ("Dhaniya Powder", "Dry", "Kgs", 168.00, 0.200),
    ("Kali Mirch (s)", "Dry", "Kgs", 882.00, 0.010),
    ("Moongphali Dana", "Dry", "Kgs", 157.50, 2.000),
    ("Sambhar Masala", "Dry", "Pkt", 76.00, 0.000),
    ("LPG", "Dry", "Kgs", 61.83, 20.600),
    ("Rai", "Dry", "Pkt", 315.00, 0.000),
    ("Sugar", "Dry", "Kgs", 49.00, 0.000),
    ("Baking Powder", "Dry", "Pkt", 67.20, 0.000),
    ("SHAHI PANEER MASALA", "Dry", "Pkt", 86.50, 4.000),
    ("Shahi Paneer Masala (kgs)", "Dry", "Kgs", 880.00, 0.000),
    ("Soya Bean Badiya", "Dry", "Kgs", 94.50, 0.000),
    ("Javitri", "Dry", "Kgs", 2730.00, 0.020),
    ("Amchur Powder", "Dry", "Pkt", 273.00, 0.000),
    ("Dal Makhani Masala", "Dry", "Pkt", 70.00, 0.000),
    ("Black Pepper Powder", "Dry", "Kgs", 120.00, 0.000),
    ("Sabji Masala", "Dry", "Pkt", 2100.00, 0.000),
    ("Aachar", "Dry", "Kgs", 147.00, 0.000),
    ("Cream", "Dry", "Kgs", 220.00, 0.500),
    ("Paratha Masala", "Dry", "Kgs", 80.00, 0.000),
    
    # Packaging
    ("PP Box (Dal) Mini Meal", "Package material", "Nos", 3.186, 411.0),
    ("Foil Box (Rice, Sabji)", "Package material", "Nos", 1.575, 822.0),
    ("Roti pouch", "Package material", "Nos", 236.000, 2.800),
    ("Salad Pkt", "Package material", "Nos", 0.177, 822.0),
    ("Spoon/Mini Meal", "Package material", "Nos", 0.504, 472.0),
    ("Napkin Tissue Paper", "Package material", "Nos", 0.354, 411.0),
    ("Salt Pouch", "Package material", "Nos", 0.150, 411.0),
    ("Pickle & Paratha", "Package material", "Nos", 0.899, 482.0),
    ("Tape", "Package material", "Nos", 23.600, 2.0),
    ("Big Foil Box (Biryani)", "Package material", "Nos", 3.150, 61.0),
    ("Paper Box (Lunch)", "Package material", "Nos", 4.956, 411.0),
    ("Butter Roti Paper", "Package material", "Nos", 236.000, 0.0),
    ("Paratha Box", "Package material", "Nos", 3.360, 71.0),
    ("Partition Box", "Package material", "Nos", 6.960, 0.0),
    ("Black Packet", "Package material", "Nos", 141.600, 1.0),
    ("400 ML PP Box", "Package material", "Nos", 4.720, 61.0),

    # Sweets
    ("Sweet (Burfi)", "Sweets", "Kgs", 280.000, 12.000),
    ("Petha", "Sweets", "Kgs", 150.000, 0.000),
    ("Guldana", "Sweets", "Kgs", 250.000, 0.000),
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
