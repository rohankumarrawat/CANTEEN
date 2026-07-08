import sqlite3

def run_migration():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()

    # 1. Merge "Foil silver" (ID 122) into "Silver foil" (ID 121)
    row_121 = cursor.execute("SELECT * FROM inventory WHERE id=121").fetchone()
    row_122 = cursor.execute("SELECT * FROM inventory WHERE id=122").fetchone()
    
    if row_122:
        print("Merging 'Foil silver' (ID 122) into 'Silver foil' (ID 121)...")
        cursor.execute("UPDATE recipes SET inv_id=121 WHERE inv_id=122")
        cursor.execute("UPDATE goods_received SET inv_id=121 WHERE inv_id=122")
        cursor.execute("UPDATE stock_ledger SET inv_id=121 WHERE inv_id=122")
        if row_121:
            stock_121 = row_121[7] if len(row_121) > 7 else 0.0
            stock_122 = row_122[7] if len(row_122) > 7 else 0.0
            new_stock = stock_121 + stock_122
            cursor.execute("UPDATE inventory SET stock=? WHERE id=121", (new_stock,))
        cursor.execute("DELETE FROM inventory WHERE id=122")
        print("Merge completed successfully!")

    # 2. General Category Updates in inventory
    cursor.execute("UPDATE inventory SET cat='Milk Based Product' WHERE cat='Milk'")
    cursor.execute("UPDATE inventory SET cat='Packing Material' WHERE cat='Packaging Material' OR cat='Prepared'")
    cursor.execute("UPDATE inventory SET cat='Misc' WHERE cat='Bakery' OR cat='Bakey'")
    
    # 3. Comprehensive corrections map: {current_name_lower: (new_name, new_category)}
    corrections = {
        "aachar": ("Achar", "Dry"),
        "ajinomoto": ("Ajinomoto", "Dry"),
        "ajwain": ("Ajwain", "Dry"),
        "amchur powder": ("Amchur Powder", "Dry"),
        "atta": ("Atta", "Dry"),
        "badi elaichi": ("Badi Elaichi", "Dry"),
        "baking powder": ("Baking Powder", "Dry"),
        "besan": ("Besan", "Dry"),
        "biryani masala": ("Biryani Masala", "Dry"),
        "black pepper powder": ("Black Pepper Powder", "Dry"),
        "chana masala": ("Chana Masala", "Dry"),
        "chana masala (pkt)": ("Chana Masala (Pkt)", "Dry"),
        "chana masala (pkt) 2": ("Chana Masala (Pkt) 2", "Dry"),
        "chat masala": ("Chaat Masala", "Dry"),
        "chat masala (pkt)": ("Chaat Masala (Pkt)", "Dry"),
        "clean wrap": ("Cling Wrap", "Packing Material"),
        "corn flour": ("Corn Flour", "Dry"),
        "cream": ("Cream", "Dry"),
        "dal arhar": ("Dal Arhar", "Dry"),
        "dal chana": ("Dal Chana", "Dry"),
        "dal chini": ("Dalchini", "Dry"),
        "dal makhani masala": ("Dal Makhani Masala", "Dry"),
        "dal masoor (s)": ("Dal Masoor (S)", "Dry"),
        "degi mirch": ("Degi Mirch", "Dry"),
        "desi ghee": ("Desi Ghee", "Dry"),
        "dhaniya (s)": ("Dhaniya (S)", "Dry"),
        "dhaniya powder": ("Dhaniya Powder", "Dry"),
        "elaichi small gr": ("Elaichi Small Gr", "Dry"),
        "eno": ("Eno", "Dry"),
        "food colour": ("Food Colour", "Dry"),
        "garam masala": ("Garam Masala", "Dry"),
        "gud": ("Gud", "Dry"),
        "gulab jal": ("Gulab Jal", "Dry"),
        "haldi powder": ("Haldi Powder", "Dry"),
        "hing": ("Hing", "Dry"),
        "imli": ("Imli", "Dry"),
        "imli (expensive)": ("Imli (Expensive)", "Dry"),
        "javitri": ("Javitri", "Dry"),
        "jeera (s)": ("Jeera (S)", "Dry"),
        "jeera powder": ("Jeera Powder", "Dry"),
        "kala chana": ("Kala Chana", "Dry"),
        "kali mirch (s)": ("Kali Mirch (S)", "Dry"),
        "kali mirch pdr": ("Kali Mirch Powder", "Dry"),
        "kasuri methi": ("Kasuri Methi", "Dry"),
        "kewra water": ("Kewra Water", "Dry"),
        "khus khus": ("Khus Khus", "Dry"),
        "kitchen king": ("Kitchen King", "Dry"),
        "lpg": ("LPG", "Dry"),
        "laung": ("Laung", "Dry"),
        "lobia": ("Lobia", "Dry"),
        "maida": ("Maida", "Dry"),
        "masoor dal (malika)": ("Masoor Dal (Malka)", "Dry"),
        "matar (tf)": ("Matar (Frozen)", "Dry"),
        "matar paneer masala": ("Matar Paneer Masala", "Dry"),
        "methi dana": ("Methi Dana", "Dry"),
        "mirchi (s)": ("Mirchi (S)", "Dry"),
        "mirchi powder": ("Mirchi Powder", "Dry"),
        "moong dal chilka": ("Moong Dal Chilka", "Dry"),
        "moongphali dana": ("Moongphali Dana", "Dry"),
        "paratha masala": ("Paratha Masala", "Dry"),
        "pav bhaji masala": ("Pav Bhaji Masala", "Dry"),
        "r/oil": ("Refined Oil", "Dry"),
        "rai": ("Rai", "Dry"),
        "rajma": ("Rajma", "Dry"),
        "rajma masala": ("Rajma Masala", "Dry"),
        "rajma masala (kgs)": ("Rajma Masala (Kgs)", "Dry"),
        "red chilli sauce": ("Red Chilli Sauce", "Dry"),
        "rice": ("Rice", "Dry"),
        "rice (cheaper)": ("Rice (Cheaper)", "Dry"),
        "sabji masala": ("Sabji Masala", "Dry"),
        "sabudana": ("Sabudana", "Dry"),
        "salt": ("Salt", "Dry"),
        "sambhar masala": ("Sambhar Masala", "Dry"),
        "sarso dana": ("Sarson Dana", "Dry"),
        "sarson": ("Sarson", "Dry"),
        "shahi paneer masala (kgs)": ("Shahi Paneer Masala (Kgs)", "Dry"),
        "shahi paneer masala (pkt)": ("Shahi Paneer Masala (Pkt)", "Dry"),
        "soya bean badiya": ("Soya Bean Badiya", "Dry"),
        "soya sauce": ("Soya Sauce", "Dry"),
        "star phool masala": ("Star Phool Masala", "Dry"),
        "sugar": ("Sugar", "Dry"),
        "tej patta": ("Tej Patta", "Dry"),
        "urad (s)": ("Urad (S)", "Dry"),
        "urad dal chilka": ("Urad Dal Chilka", "Dry"),
        "urad dhuli": ("Urad Dhuli", "Dry"),
        "vinegar": ("Vinegar", "Dry"),
        "beans": ("Beans", "Fresh"),
        "bottle gd": ("Bottle Gourd", "Fresh"),
        "cabbage": ("Cabbage", "Fresh"),
        "capsicum": ("Capsicum", "Fresh"),
        "carrot": ("Carrot", "Fresh"),
        "cauli flower": ("Cauliflower", "Fresh"),
        "coriander": ("Coriander", "Fresh"),
        "cucumber": ("Cucumber", "Fresh"),
        "garlic": ("Garlic", "Fresh"),
        "ginger": ("Ginger", "Fresh"),
        "green chilli": ("Green Chilli", "Fresh"),
        "green onion": ("Green Onion", "Fresh"),
        "kulcha": ("Kulcha", "Fresh"),
        "lime s": ("Lemon", "Fresh"),
        "matar": ("Matar", "Fresh"),
        "onion": ("Onion", "Fresh"),
        "pav": ("Pav", "Fresh"),
        "pav/kulcha": ("Pav / Kulcha", "Fresh"),
        "peas green": ("Green Peas", "Fresh"),
        "potato": ("Potato", "Fresh"),
        "pumpkin": ("Pumpkin", "Fresh"),
        "tomato": ("Tomato", "Fresh"),
        "tori": ("Tori", "Fresh"),
        "amul kool": ("Amul Kool", "Milk Based Product"),
        "brownie": ("Brownie", "Milk Based Product"),
        "chach": ("Chach", "Milk Based Product"),
        "dahi": ("Dahi", "Milk Based Product"),
        "lahori zeera": ("Lahori Zeera", "Milk Based Product"),
        "lassi": ("Lassi", "Milk Based Product"),
        "paneer": ("Paneer", "Milk Based Product"),
        "plum cake": ("Plum Cake", "Milk Based Product"),
        "sweet (burfi)": ("Burfi", "Milk Based Product"),
        "petha": ("Petha", "Milk Based Product"),
        "guldana": ("Guldana", "Milk Based Product"),
        "400 ml pp box": ("400ml PP Box", "Packing Material"),
        "big foil box (biryani)": ("Big Foil Box (Biryani)", "Packing Material"),
        "black packet": ("Black Packet", "Packing Material"),
        "butter roti paper": ("Butter Roti Paper", "Packing Material"),
        "foil box (rice, sabji)": ("Foil Box (Rice, Sabji)", "Packing Material"),
        "napkin tissue paper": ("Napkin Tissue Paper", "Packing Material"),
        "pp box (dal) mini meal": ("PP Box (Dal) Mini Meal", "Packing Material"),
        "paper box (lunch)": ("Paper Box (Lunch)", "Packing Material"),
        "paratha box": ("Paratha Box", "Packing Material"),
        "partition box": ("Partition Box", "Packing Material"),
        "pickle & paratha": ("Pickle & Paratha", "Packing Material"),
        "roti pouch": ("Roti Pouch", "Packing Material"),
        "salad pkt": ("Salad Pkt", "Packing Material"),
        "salt pouch": ("Salt Pouch", "Packing Material"),
        "silver foil": ("Silver Foil", "Packing Material"),
        "spoon/mini meal": ("Spoon / Mini Meal", "Packing Material"),
        "tape": ("Tape", "Packing Material"),
    }

    # Fetch all items in DB currently
    all_db_items = cursor.execute("SELECT id, item, cat FROM inventory").fetchall()
    
    for i_id, name, cat in all_db_items:
        lower_name = name.strip().lower()
        if lower_name in corrections:
            new_name, new_cat = corrections[lower_name]
            cursor.execute(
                "UPDATE inventory SET item=?, cat=? WHERE id=?",
                (new_name, new_cat, i_id)
            )
            print(f"Updated item: '{name}' -> '{new_name}' (Category: {new_cat})")
        else:
            new_name = name.strip().title()
            cursor.execute(
                "UPDATE inventory SET item=? WHERE id=?",
                (new_name, i_id)
            )
            print(f"Capitalized item: '{name}' -> '{new_name}'")

    conn.commit()
    conn.close()
    print("Database categories and spellings migration finished successfully!")

if __name__ == '__main__':
    run_migration()
