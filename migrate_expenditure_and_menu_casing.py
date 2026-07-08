import sqlite3
import re

def migrate():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    # 1. Spelling and capitalization mapping for items and menus
    name_mapping = {
        "Aloo shimla thali (aloo shimla Mirch, kadhi Pakora, Rice, Roti, Salad, badana)":
            "Aloo Shimla Thali (Aloo Shimla Mirch, Kadhi Pakora, Rice, Roti, Salad, Badana)",
        "Aloo soyabean thali (aloo Soyabean, kala Chana, Rice, Roti, Salad, dry petha)":
            "Aloo Soyabean Thali (Aloo Soyabean, Kala Chana, Rice, Roti, Salad, Dry Petha)",
        "Kadhai paneer thali (kadhai Paneer, dal Rajma, Rice, Roti, Salad, besan barfi)":
            "Kadhai Paneer Thali (Kadhai Paneer, Dal Rajma, Rice, Roti, Salad, Besan Barfi)",
        "Kadhi chawal": "Kadhi Chawal",
        "Lahori zeera": "Lahori Zeera",
        "Panchratna thali (lauki dal chana Sabji, panchratna Dal, Rice, Roti, Salad, dry petha)":
            "Panchratna Thali (Lauki Dal Chana Sabji, Panchratna Dal, Rice, Roti, Salad, Dry Petha)",
        "Shahi paneer thali (shahi Paneer, dal Tadka, Rice, Roti, Salad, besan barfi)":
            "Shahi Paneer Thali (Shahi Paneer, Dal Tadka, Rice, Roti, Salad, Besan Barfi)",
        "Tori kaddu thali (Tori, Kaddu, dal Chana, Chapati, rice)":
            "Tori Kaddu Thali (Tori, Kaddu, Dal Chana, Chapati, Rice)",
        "Dal chana parantha": "Dal Chana Parantha",
        "Fried aloo parantha": "Fried Aloo Parantha",
        "Mix veg parantha": "Mix Veg Parantha",
        "Mixed veg parantha": "Mixed Veg Parantha",
        "Plum cake": "Plum Cake",
        "Matar kulcha": "Matar Kulcha",
        "Pav bhaji": "Pav Bhaji",
        "Chhaach": "Chach",
        "CHHAACH": "Chach",
        "chhaach": "Chach",
        "DAHI": "Dahi",
        "dahi": "Dahi",
        "LASSI": "Lassi",
        "lassi": "Lassi",
        "Amul": "Amul Kool",
        "AMUL": "Amul Kool",
        "amul": "Amul Kool"
    }

    # Helper function to standardize item names
    def standardize_name(old_name):
        if not old_name:
            return old_name
        stripped = old_name.strip()
        # Direct match check
        for k, v in name_mapping.items():
            if stripped.lower() == k.lower():
                return v
        return stripped

    # 2. Update menu table item names
    menu_rows = cursor.execute("SELECT id, name FROM menu").fetchall()
    menu_updated = 0
    for r_id, name in menu_rows:
        new_name = standardize_name(name)
        if name != new_name:
            cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (new_name, r_id))
            menu_updated += 1
            print(f"Menu name update: '{name}' -> '{new_name}'")
    print(f"Updated {menu_updated} rows in menu table.")

    # 3. Update inventory table item names
    inv_rows = cursor.execute("SELECT id, item FROM inventory").fetchall()
    inv_updated = 0
    for r_id, item in inv_rows:
        new_item = standardize_name(item)
        if item != new_item:
            cursor.execute("UPDATE inventory SET item = ? WHERE id = ?", (new_item, r_id))
            inv_updated += 1
            print(f"Inventory item update: '{item}' -> '{new_item}'")
    print(f"Updated {inv_updated} rows in inventory table.")

    # 4. Update sales table meal names
    sales_rows = cursor.execute("SELECT id, meal FROM sales").fetchall()
    sales_updated = 0
    for r_id, meal in sales_rows:
        new_meal = standardize_name(meal)
        if meal != new_meal:
            cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, r_id))
            sales_updated += 1
    print(f"Updated {sales_updated} rows in sales table.")

    # 5. Update samples table meal names
    samples_rows = cursor.execute("SELECT id, meal FROM samples").fetchall()
    samples_updated = 0
    for r_id, meal in samples_rows:
        new_meal = standardize_name(meal)
        if meal != new_meal:
            cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, r_id))
            samples_updated += 1
    print(f"Updated {samples_updated} rows in samples table.")

    # 6. Normalize expenditure table notes
    exp_rows = cursor.execute("SELECT id, notes FROM expenditure").fetchall()
    exp_updated = 0
    for r_id, notes in exp_rows:
        notes_str = notes or ""
        # Look for "Auto-expenditure for {item} batch..."
        m = re.search(r"Auto-expenditure for (.+?) batch", notes_str, re.IGNORECASE)
        if m:
            item_part = m.group(1).strip()
            # Standardize item name
            std_item = standardize_name(item_part)
            if std_item.lower() == 'chhaach':
                std_item = 'Chach'
            new_notes = f"Auto-Expenditure for {std_item} Batch"
            if notes_str != new_notes:
                cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, r_id))
                exp_updated += 1
                print(f"Expenditure notes update: '{notes_str}' -> '{new_notes}'")
        else:
            # Check direct replacements for non-auto batch notes
            for old, new in name_mapping.items():
                if old in notes_str:
                    new_notes = notes_str.replace(old, new)
                    if notes_str != new_notes:
                        cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, r_id))
                        exp_updated += 1
                        print(f"Expenditure notes replace: '{notes_str}' -> '{new_notes}'")
                        notes_str = new_notes

    print(f"Updated {exp_updated} rows in expenditure table.")
    
    conn.commit()
    conn.close()
    print("Spelling and casing migration completed successfully.")

if __name__ == '__main__':
    migrate()
