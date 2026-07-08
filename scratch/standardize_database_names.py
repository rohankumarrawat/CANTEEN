import sqlite3
import re

def standardize_name(name):
    # Mapping of lowercase names to standardized Title Case names
    std_map = {
        "dal chana parantha": "Dal Chana Parantha",
        "fried aloo parantha": "Fried Aloo Parantha",
        "kadhi chawal": "Kadhi Chawal",
        "mix veg parantha": "Mix Veg Parantha",
        "mixed veg parantha": "Mixed Veg Parantha",
        "pav bhaji": "Pav Bhajji (Fried Aloo)",
        "pav bhajji (fried aloo)": "Pav Bhajji (Fried Aloo)",
        "plum cake": "Plum Cake",
        "rajma rice": "Rajmah Rice",
        "rajmah rice": "Rajmah Rice",
        "tamarind rice": "Tamarind Rice",
        "veg biryani": "Veg Biryani",
        "broweni": "Brownie",
        "brownie": "Brownie",
        "paratha": "Paratha",
        "dahi": "Dahi",
        "chach": "Chach",
        "amul kool": "Amul Kool",
        "lahori zeera": "Lahori Zeera",
        "lassi": "Lassi",
        "matar kulcha": "Matar Kulcha",
        "tori kaddu thali (tori, kaddu, dal chana, chapati, rice)": "Tori / Kadoo Sabzi Thali (Tori / Kadoo Sabzi, Dal Masur, Rice, Roti & Salad, Badana)",
        "tori / kadoo sabzi thali (tori / kadoo sabzi, dal masur, rice, roti & salad, badana)": "Tori / Kadoo Sabzi Thali (Tori / Kadoo Sabzi, Dal Masur, Rice, Roti & Salad, Badana)",
        "kadhai paneer thali (kadhai paneer, dal rajma, rice, roti, salad, besan barfi)": "Kadhai Paneer Thali (Kadhai Paneer, Dal Rajmah, Rice, Roti & Salad, Besan Barfi)",
        "kadhai paneer thali (kadhai paneer, dal rajmah, rice, roti & salad, besan barfi)": "Kadhai Paneer Thali (Kadhai Paneer, Dal Rajmah, Rice, Roti & Salad, Besan Barfi)",
        "shahi paneer thali (shahi paneer, dal tadka, rice, roti, salad, besan barfi)": "Shahi Paneer Thali (Shahi Paneer, Dal Tadka, Rice, Roti & Salad, Besan Barfi)",
        "shahi paneer thali (shahi paneer, dal tadka, rice, roti & salad, besan barfi)": "Shahi Paneer Thali (Shahi Paneer, Dal Tadka, Rice, Roti & Salad, Besan Barfi)",
        "aloo shimla thali (aloo shimla mirch, kadhi pakora, rice, roti, salad, badana)": "Aloo Shimla Thali (Aloo Shimla Mirch, Kadhi Pakora, Rice, Roti & Salad, Badana)",
        "aloo shimla thali (aloo shimla mirch, kadhi pakora, rice, roti & salad, badana)": "Aloo Shimla Thali (Aloo Shimla Mirch, Kadhi Pakora, Rice, Roti & Salad, Badana)",
        "aloo soyabean thali (aloo soyabean, kala chana, rice, roti, salad, dry petha)": "Aloo Soyabean Thali (Aloo Soyabean, Kala Chana, Rice, Roti & Salad, Dry Petha)",
        "aloo soyabean thali (aloo soyabean, kala chana, rice, roti & salad, dry petha)": "Aloo Soyabean Thali (Aloo Soyabean, Kala Chana, Rice, Roti & Salad, Dry Petha)",
        "panchratna thali (lauki dal chana sabji, panchratna dal, rice, roti, salad, dry petha)": "Panchratna Thali (Lauki Dal Chana Sabji, Panchratna Dal, Rice & Roti, Salad, Dry Petha)",
        "panchratna thali (lauki dal chana sabji, panchratna dal, rice & roti, salad, dry petha)": "Panchratna Thali (Lauki Dal Chana Sabji, Panchratna Dal, Rice & Roti, Salad, Dry Petha)"
    }
    
    clean_name = name.strip()
    lower_name = clean_name.lower()
    if lower_name in std_map:
        return std_map[lower_name]
    return clean_name

def clean_meal_string(meal_str):
    # Regex to capture MealType(SpecificName) or MealType (SpecificName)
    # Be careful to handle nesting parentheses (like Tori Kaddu Thali (Tori, Kaddu...))
    match = re.match(r"^([^\(]+)(?:\((.*)\))?$", meal_str.strip())
    if not match:
        return standardize_name(meal_str)
        
    mtype = match.group(1).strip()
    specific = match.group(2).strip() if match.group(2) else None
    
    # Standardize meal type and specific name separately
    mtype_std = standardize_name(mtype)
    if specific:
        specific_std = standardize_name(specific)
        return f"{mtype_std} ({specific_std})"
    else:
        return mtype_std

def main():
    db_path = "canteen.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Update menu table
    print("Standardizing menu table names...")
    cursor.execute("SELECT id, name FROM menu")
    menu_rows = cursor.fetchall()
    for row_id, old_name in menu_rows:
        new_name = standardize_name(old_name)
        if old_name != new_name:
            print(f"  - Menu ID {row_id}: '{old_name}' -> '{new_name}'")
            cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (new_name, row_id))
            
    # 2. Update sales table
    print("Standardizing sales table meal strings...")
    cursor.execute("SELECT id, meal FROM sales")
    sales_rows = cursor.fetchall()
    sales_updated = 0
    for row_id, old_meal in sales_rows:
        new_meal = clean_meal_string(old_meal)
        if old_meal != new_meal:
            cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row_id))
            sales_updated += 1
    print(f"  - Updated {sales_updated} rows in sales table.")
            
    # 3. Update samples table
    print("Standardizing samples table meal strings...")
    cursor.execute("SELECT id, meal FROM samples")
    samples_rows = cursor.fetchall()
    samples_updated = 0
    for row_id, old_meal in samples_rows:
        new_meal = clean_meal_string(old_meal)
        if old_meal != new_meal:
            cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row_id))
            samples_updated += 1
    print(f"  - Updated {samples_updated} rows in samples table.")
    
    conn.commit()
    conn.close()
    print("🎉 Database standardizations finished successfully!")

if __name__ == "__main__":
    main()
