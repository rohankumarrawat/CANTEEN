import sqlite3
import re

def standardize_text(s, mapping):
    if not s:
        return s
    
    # 1. Exact case-insensitive match (highest priority)
    for target, replacement in mapping.items():
        if s.strip().lower() == target.strip().lower():
            return replacement

    # 2. Substring replacements with word boundaries where applicable
    for target, replacement in mapping.items():
        # Only use word boundary if target starts/ends with alphanumeric characters
        start_boundary = r'\b' if target[0].isalnum() else ''
        end_boundary = r'\b' if target[-1].isalnum() else ''
        pattern = re.compile(start_boundary + re.escape(target) + end_boundary, re.IGNORECASE)
        s = pattern.sub(replacement, s)
        
    # 3. Handle Thali names casing:
    # All thali meal names and their ingredient details inside parentheses will be fully title-cased.
    # Pattern: "... Thali (..., ..., ...)"
    m = re.match(r"^([^(]+)\(([^)]+)\)$", s)
    if m:
        prefix = m.group(1).strip()
        contents = m.group(2).strip()
        if "thali" in prefix.lower():
            # Title Case the prefix and items inside parentheses
            prefix_title = " ".join(w.capitalize() for w in prefix.split())
            items = [item.strip() for item in contents.split(",")]
            items_title = []
            for item in items:
                # Capitalize each word in the ingredient
                item_words = []
                for word in item.split():
                    if word.upper() in ["TF", "LPG", "PP", "ML", "BBF", "BCF", "UPI"]:
                        item_words.append(word.upper())
                    else:
                        item_words.append(word.capitalize())
                items_title.append(" ".join(item_words))
            s = f"{prefix_title} ({', '.join(items_title)})"
            
    return s

def migrate():
    db_path = "/Users/rohan/Desktop/canteen/canteen.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Define exact case-insensitive mapping
    item_mapping = {
        "Dal arhar": "Dal Arhar",
        "Desi ghee": "Desi Ghee",
        "Mungphali dana": "Moongphali Dana",
        "Moongphali dana": "Moongphali Dana",
        "Matar tf": "Matar (TF)",
        "Matar TF": "Matar (TF)",
        "Matar tinned/frozen": "Matar (TF)",
        "B elaichi": "Badi Elaichi",
        "B ELAICHI": "Badi Elaichi",
        "Badi elaichi": "Badi Elaichi",
        "Lahori zeera": "Lahori Zeera",
        "Lahari jeera": "Lahori Zeera",
        "Lahari Jeera": "Lahori Zeera",
        "Matar paneer masala": "Matar Paneer Masala",
        "Masur crd(malika)": "Masoor Dal (Malika)",
        "Masoor dal (malika)": "Masoor Dal (Malika)",
        "Moong crd(chilka)": "Moong Dal Chilka",
        "Moong dal chilka": "Moong Dal Chilka",
        "Urd (s)": "Urad (s)",
        "Urad (s)": "Urad (s)",
        "Urd crd(chilka)": "Urad Dal Chilka",
        "Urad dal chilka": "Urad Dal Chilka",
        "Urd dhuli": "Urad Dhuli",
        "Urad dhuli": "Urad Dhuli",
        "Amchur pdr": "Amchur Powder",
        "Amchur powder": "Amchur Powder",
        "Mirchi pdr": "Mirchi Powder",
        "Mirchi powder": "Mirchi Powder",
        "Jeera pdr": "Jeera Powder",
        "Jeera powder": "Jeera Powder",
        "Haldi pdr": "Haldi Powder",
        "Haldi powder": "Haldi Powder",
        "Dhaniya pdr": "Dhaniya Powder",
        "Dhaniya powder": "Dhaniya Powder",
        "Baking pdr": "Baking Powder",
        "Baking powder": "Baking Powder",
        "Black pepper pdr": "Black Pepper Powder",
        "Black pepper powder": "Black Pepper Powder",
        "Khas khas": "Khus Khus",
        "Sarsoo": "Sarson",
        "Lobhiya": "Lobia",
        "Rajmah": "Rajma",
        "Matar kulcha": "Matar Kulcha",
        "Dal chana": "Dal Chana",
        "Paratha masala": "Paratha Masala",
        "Chat masala": "Chat Masala",
        "Chat masala (pkt)": "Chat Masala (Pkt)",
        "Rajma masala": "Rajma Masala",
        "Rajma masala (kgs)": "Rajma Masala (Kgs)",
        "Shahi paneer masala": "Shahi Paneer Masala",
        "Shahi paneer masala (kgs)": "Shahi Paneer Masala (Kgs)",
        "Soya bean badiya": "Soya Bean Badiya",
        "Kala chana": "Kala Chana",
        "Degi mirch": "Degi Mirch",
        "Kitchen king": "Kitchen King",
        "Garam masala": "Garam Masala",
        "Kasuri methi": "Kasuri Methi",
        "Chana masala": "Chana Masala",
        "Methi dana": "Methi Dana",
        "Tej patta": "Tej Patta",
        "Tej Patta": "Tej Patta",
        "Gulab jal": "Gulab Jal",
        "Red chilli sauce": "Red Chilli Sauce",
        "Pav bhaji masala": "Pav Bhaji Masala",
        "Star phool masala": "Star Phool Masala",
        "Food colour": "Food Colour",
        "Kewra water": "Kewra Water",
        "Biryani masala": "Biryani Masala",
        "Elaichi small gr": "Elaichi Small Gr",
        "Kali mirch (s)": "Kali Mirch (s)",
        "Sambhar masala": "Sambhar Masala",
        "Dal makhani masala": "Dal Makhani Masala",
        "Sabji masala": "Sabji Masala",
        "Butter roti paper": "Butter Roti Paper",
        "Paper box (lunch)": "Paper Box (Lunch)",
        "Napkin tissue paper": "Napkin Tissue Paper",
        "Salad pkt": "Salad Pkt",
        "Foil box (rice, sabji)": "Foil Box (Rice, Sabji)",
        "Foil box (rice,sabji)": "Foil Box (Rice, Sabji)",
        "PP box (dal) mini meal": "PP Box (Dal) Mini Meal",
        "Spoon/mini meal": "Spoon/Mini Meal",
        "Salt pouch": "Salt Pouch",
        "Pickle & paratha": "Pickle & Paratha",
        "Big foil box (biryani)": "Big Foil Box (Biryani)",
        "Paratha box": "Paratha Box",
        "Partition box": "Partition Box",
        "Black packet": "Black Packet",
        "400 ML PP box": "400 ML PP Box",
        "Sweet {burfi}": "Sweet (Burfi)",
        "Sweet (burfi)": "Sweet (Burfi)",
        "SWEET (BURFI)": "Sweet (Burfi)",
        "Petha": "Petha",
        "Guldana": "Guldana",
        "Lime S": "Lime S",
        "Pav/Kulcha": "Pav/Kulcha",
        "R/oil": "R/oil",
        "Sarso Dana": "Sarso Dana",
        "Dal chini": "Dal chini",
        "Ajinomoto": "Ajinomoto",
        "Clean wrap": "Clean Wrap",
        "Ajwain": "Ajwain",
        "Mirchi (s)": "Mirchi (s)",
        "Javitri": "Javitri",
        "Aachar": "Aachar",
        "Cream": "Cream",
        "Potato": "Potato",
        "Onion": "Onion",
        "Tomato": "Tomato",
        "Ginger": "Ginger",
        "Garlic": "Garlic",
        "Pumpkin": "Pumpkin",
        "Green chilli": "Green Chilli",
        "Green Chilli": "Green Chilli",
        "Coriander": "Coriander",
        "Capsicum": "Capsicum",
        "Beans": "Beans",
        "Carrot": "Carrot",
        "Cauli flower": "Cauli Flower",
        "Cauli Flower": "Cauli Flower",
        "Green onion": "Green Onion",
        "Green Onion": "Green Onion",
        "Bottle gd": "Bottle Gd",
        "Bottle Gd": "Bottle Gd",
        "Cabbage": "Cabbage",
        "Cucumber": "Cucumber",
        "Matar": "Matar",
        "Paneer": "Paneer",
        "Dahi": "Dahi",
        "Atta": "Atta",
        "Rice": "Rice",
        "Besan": "Besan",
        "Dal masoor (s)": "Dal Masoor (s)",
        "Laung": "Laung",
        "Hing": "Hing",
        "Salt": "Salt",
        "LPG": "LPG",
        "Rai": "Rai",
        "Sugar": "Sugar",
        "Silver foil": "Silver Foil",
        "Foil silver": "Foil Silver",
        "Tori": "Tori",
        "Eno": "Eno",
        "Imli": "Imli",
        "Rice (cheaper)": "Rice (Cheaper)",
        "Imli (expensive)": "Imli (Expensive)",
        "Kulcha": "Kulcha",
        "Pav": "Pav",
        "Sabudana": "Sabudana",
        "Kali mirch pdr": "Kali Mirch Powder",
        "Kali mirch powder": "Kali Mirch Powder",
        "Maida": "Maida",
        "Soya sauce": "Soya Sauce",
        "Chach": "Chach",
        "Amul Kool": "Amul Kool",
        "Lassi": "Lassi",
        "Brownie": "Brownie",
        "Plum cake": "Plum Cake",
        
        # Original database unclean names mapping
        "Kevada water": "Kewra Water",
        "Kevada Water": "Kewra Water",
        "Biriyani masala": "Biryani Masala",
        "Biriyani Masala": "Biryani Masala",
        "ilaychi small Gr": "Elaichi Small Gr",
        "Ilaychi small gr": "Elaichi Small Gr",
        "Mumfali dana": "Moongphali Dana",
        "Mumfali Dana": "Moongphali Dana",
        "Sahi paneer masala": "Shahi Paneer Masala",
        "Sahi Paneer masala": "Shahi Paneer Masala",
        "Sahi Paneer masala (kgs)": "Shahi Paneer Masala (Kgs)",
        "Sahi Paneer masala (pkt)": "Shahi Paneer Masala (Pkt)",
        "Emli": "Imli",
        "Emli (expensive)": "Imli (Expensive)",
        "Saya sauce": "Soya Sauce",
        "Saya Sauce": "Soya Sauce",
        "Corrender": "Coriander",
        "Nepkin tussu pepar": "Napkin Tissue Paper",
        "Nepkin Tussu Pepar": "Napkin Tissue Paper",
        "Big foil box (biriyani)": "Big Foil Box (Biryani)",
        "Partation box": "Partition Box",
        "Ajino moto": "Ajinomoto",
        "Ajino Moto": "Ajinomoto",
        "Javtitri": "Javitri",
        "Daniya (s)": "Dhaniya (s)"
    }

    # Unit Title Casing Mapping
    unit_mapping = {
        "kgs": "Kgs",
        "KGS": "Kgs",
        "nos": "Nos",
        "NOS": "Nos",
        "pkt": "Pkt",
        "PKT": "Pkt",
        "btl": "Btl",
        "BTL": "Btl",
        "pcs": "Pcs",
        "PCS": "Pcs",
        "ltr": "Ltr",
        "LTR": "Ltr",
    }

    # 1. Update retail item categories to Milk
    retail_items = ["Sweet (Burfi)", "Dahi", "Paneer"]
    for item in retail_items:
        cursor.execute("UPDATE inventory SET cat = 'Milk' WHERE item = ? COLLATE NOCASE", (item,))

    # 2. Insert new retail items under Milk category if missing
    new_retail_items = [
        ("Lahori Zeera", "Milk", "Btl", 0.0, 5.0, 0.0, 8.0),
        ("Chach",        "Milk", "Pkt", 0.0, 5.0, 0.0, 8.0),
        ("Amul Kool",         "Milk", "Pkt", 0.0, 5.0, 0.0, 20.0),
        ("Lassi",        "Milk", "Pkt", 0.0, 5.0, 0.0, 16.0),
        ("Brownie",      "Milk", "Pcs", 0.0, 5.0, 0.0, 30.0),
        ("Plum Cake",    "Milk", "Pcs", 0.0, 5.0, 0.0, 15.0)
    ]
    for item, cat, unit, stock, min_lvl, opening, cp in new_retail_items:
        cursor.execute("SELECT item FROM inventory WHERE item=? COLLATE NOCASE", (item,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, cp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item, cat, unit, stock, min_lvl, opening, cp)
            )
        else:
            cursor.execute("UPDATE inventory SET cat='Milk' WHERE item=? COLLATE NOCASE", (item,))

    # 3. Update units in inventory
    rows = cursor.execute("SELECT id, unit FROM inventory").fetchall()
    for row in rows:
        unit = row["unit"]
        new_unit = unit_mapping.get(unit, unit)
        if new_unit == unit:
            new_unit = unit.title()
        if unit != new_unit:
            cursor.execute("UPDATE inventory SET unit = ? WHERE id = ?", (new_unit, row["id"]))

    # 4. Update item names in inventory
    rows = cursor.execute("SELECT id, item FROM inventory").fetchall()
    for row in rows:
        old_name = row["item"]
        new_name = standardize_text(old_name, item_mapping)
        if old_name != new_name:
            cursor.execute("UPDATE inventory SET item = ? WHERE id = ?", (new_name, row["id"]))
            print(f"Inventory Name: '{old_name}' -> '{new_name}'")

    # Update category for package material items
    package_items = [
        "PP Box (Dal) Mini Meal",
        "Foil Box (Rice, Sabji)",
        "Roti pouch",
        "Salad Pkt",
        "Spoon/Mini Meal",
        "Napkin Tissue Paper",
        "Salt Pouch",
        "Pickle & Paratha",
        "Tape",
        "Big Foil Box (Biryani)",
        "Paper Box (Lunch)",
        "Butter Roti Paper",
        "Paratha Box",
        "Partition Box",
        "Black Packet",
        "400 ML PP Box",
        "Silver Foil",
        "Foil Silver"
    ]
    for item in package_items:
        cursor.execute("UPDATE inventory SET cat = 'Packaging Material' WHERE item = ? COLLATE NOCASE", (item,))

    # Update expenditure and inventory category names
    cursor.execute("UPDATE inventory SET cat = 'Packaging Material' WHERE cat = 'Package material'")
    cursor.execute("UPDATE expenditure SET category = 'Packaging Material' WHERE category = 'Package material'")
    cursor.execute("UPDATE expenditure SET category = 'Misc (Civ. Payment)' WHERE category = 'Misc(Civ payment)'")


    # 5. Update menu table
    rows = cursor.execute("SELECT id, name FROM menu").fetchall()
    for row in rows:
        old_name = row["name"]
        new_name = standardize_text(old_name, item_mapping)
        if old_name != new_name:
            cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (new_name, row["id"]))
            print(f"Menu Name: '{old_name}' -> '{new_name}'")

    # 6. Update sales table
    rows = cursor.execute("SELECT id, meal FROM sales").fetchall()
    for row in rows:
        old_meal = row["meal"]
        new_meal = standardize_text(old_meal, item_mapping)
        if old_meal != new_meal:
            cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row["id"]))
            print(f"Sales Meal: '{old_meal}' -> '{new_meal}'")

    # 7. Update samples table
    rows = cursor.execute("SELECT id, meal, notes FROM samples").fetchall()
    for row in rows:
        old_meal = row["meal"]
        new_meal = standardize_text(old_meal, item_mapping)
        if old_meal != new_meal:
            cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row["id"]))
            print(f"Samples Meal: '{old_meal}' -> '{new_meal}'")
        
        old_notes = row["notes"]
        if old_notes:
            new_notes = standardize_text(old_notes, item_mapping)
            if old_notes != new_notes:
                cursor.execute("UPDATE samples SET notes = ? WHERE id = ?", (new_notes, row["id"]))
                print(f"Samples Notes: '{old_notes}' -> '{new_notes}'")

    # 8. Update expenditure table
    rows = cursor.execute("SELECT id, notes FROM expenditure").fetchall()
    for row in rows:
        old_notes = row["notes"]
        if old_notes:
            new_notes = standardize_text(old_notes, item_mapping)
            if old_notes != new_notes:
                cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, row["id"]))
                print(f"Expenditure Notes: '{old_notes}' -> '{new_notes}'")

    # 9. Update waste_tracker table
    rows = cursor.execute("SELECT id, item FROM waste_tracker").fetchall()
    for row in rows:
        old_item = row["item"]
        new_item = standardize_text(old_item, item_mapping)
        if old_item != new_item:
            cursor.execute("UPDATE waste_tracker SET item = ? WHERE id = ?", (new_item, row["id"]))
            print(f"Waste Tracker: '{old_item}' -> '{new_item}'")

    conn.commit()
    conn.close()
    print("Database spelling and casing standardization complete!")

if __name__ == "__main__":
    migrate()
