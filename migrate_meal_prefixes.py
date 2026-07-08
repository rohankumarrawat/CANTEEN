import sqlite3
import re

def standardize_meal_name(meal):
    s = meal.strip()
    while True:
        s_lower = s.lower()
        if s_lower.startswith("lunch("):
            if s.endswith(")"):
                s = s[6:-1].strip()
                continue
        if s_lower.startswith("mini meal("):
            if s.endswith(")"):
                s = s[10:-1].strip()
                continue
        if s_lower.startswith("paratha("):
            if s.endswith(")"):
                s = s[8:-1].strip()
                continue
        break
        
    s_lower = s.lower()
    if "panchratna" in s_lower:
        return "Lunch(Panchratna Thali (Lauki Dal Chana Sabji, Panchratna Dal, Rice, Roti, Salad, Dry Petha))"
    if "aloo shimla" in s_lower:
        return "Lunch(Aloo Shimla Thali (Aloo Shimla Mirch, Kadhi Pakora, Rice, Roti, Salad, Badana))"
    if "kadhai paneer" in s_lower:
        return "Lunch(Kadhai Paneer Thali (Kadhai Paneer, Dal Rajma, Rice, Roti, Salad, Besan Barfi))"
    if "soyabean" in s_lower:
        return "Lunch(Aloo Soyabean Thali (Aloo Soyabean, Kala Chana, Rice, Roti, Salad, Dry Petha))"
    if "shahi paneer" in s_lower:
        return "Lunch(Shahi Paneer Thali (Shahi Paneer, Dal Tadka, Rice, Roti, Salad, Besan Barfi))"
    if "tori kaddu" in s_lower:
        return "Lunch(Tori Kaddu Thali (Tori, Kaddu, Dal Chana, Chapati, Rice))"
    if "mix veg par" in s_lower or "mixed veg par" in s_lower:
        return "Paratha(Mix Veg Paratha)"
    if "fried aloo par" in s_lower or "fried aalo par" in s_lower:
        return "Paratha(Fried Aloo Paratha)"
    if "dal chana par" in s_lower:
        return "Paratha(Dal Chana Paratha)"
    if "rajma rice" in s_lower or "rajmah rice" in s_lower:
        return "Mini Meal(Rajma Rice)"
    if "veg biryani" in s_lower or "veg biriyani" in s_lower:
        return "Mini Meal(Veg Biryani)"
    if "tamarind rice" in s_lower:
        return "Mini Meal(Tamarind Rice)"
    if "kadhi chawal" in s_lower:
        return "Mini Meal(Kadhi Chawal)"
    if "matar kulcha" in s_lower:
        return "Mini Meal(Matar Kulcha)"
    if "pav bhaji" in s_lower:
        return "Mini Meal(Pav Bhaji)"
        
    if s.lower() in ["dahi", "chach", "amul kool", "lassi", "brownie", "plum cake", "lahori zeera"]:
        return " ".join(w.capitalize() for w in s.split())
    if s.lower() == "paratha":
        return "Paratha"
    return s

def migrate():
    conn = sqlite3.connect("canteen.db")
    cursor = conn.cursor()

    # 1. Standardize menu table names and merge duplicates
    print("Grouping and merging menu items...")
    menu_rows = cursor.execute("SELECT id, name FROM menu").fetchall()
    groups = {}
    for menu_id, name in menu_rows:
        std_name = standardize_meal_name(name)
        groups.setdefault(std_name, []).append((menu_id, name))

    for std_name, items in groups.items():
        if len(items) > 1:
            # We have duplicates! Merge them.
            items.sort(key=lambda x: x[0])
            primary_id, primary_name = items[0]
            print(f"\nMerging duplicates for '{std_name}' (Primary ID: {primary_id}):")
            for dup_id, dup_name in items[1:]:
                print(f"  Duplicate ID {dup_id} ('{dup_name}') -> primary ID {primary_id}")
                cursor.execute("UPDATE recipes SET menu_id = ? WHERE menu_id = ?", (primary_id, dup_id))
                cursor.execute("UPDATE sales SET menu_id = ? WHERE menu_id = ?", (primary_id, dup_id))
                cursor.execute("UPDATE batch_prep SET menu_id = ? WHERE menu_id = ?", (primary_id, dup_id))
                cursor.execute("UPDATE daily_menu SET menu_id = ? WHERE menu_id = ?", (primary_id, dup_id))
                cursor.execute("UPDATE samples SET menu_id = ? WHERE menu_id = ?", (primary_id, dup_id))
                cursor.execute("DELETE FROM menu WHERE id = ?", (dup_id,))
            cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (std_name, primary_id))
        else:
            primary_id, name = items[0]
            if name != std_name:
                cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (std_name, primary_id))
                print(f"Updated menu item ID {primary_id}: '{name}' -> '{std_name}'")

    # 2. Update sales meal column
    print("\nUpdating sales meal column...")
    rows = cursor.execute("SELECT id, meal FROM sales").fetchall()
    for row_id, old_meal in rows:
        new_meal = standardize_meal_name(old_meal)
        if old_meal != new_meal:
            cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row_id))
            print(f"  Sales ID {row_id}: '{old_meal}' -> '{new_meal}'")

    # 3. Update samples meal column
    print("\nUpdating samples meal column...")
    rows = cursor.execute("SELECT id, meal FROM samples").fetchall()
    for row_id, old_meal in rows:
        new_meal = standardize_meal_name(old_meal)
        if old_meal != new_meal:
            cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row_id))
            print(f"  Samples ID {row_id}: '{old_meal}' -> '{new_meal}'")

    # 4. Update expenditure notes
    print("\nUpdating expenditure notes...")
    rows = cursor.execute("SELECT id, notes FROM expenditure").fetchall()
    for row_id, old_notes in rows:
        if old_notes:
            new_notes = old_notes
            for term in ["Panchratna thali", "Panchratna Thali", "Aloo shimla thali", "Aloo Shimla Thali",
                         "Kadhai paneer thali", "Kadhai Paneer thali", "Kadhai Paneer Thali",
                         "Aloo soyabean thali", "Aloo Soyabean Thali",
                         "Shahi paneer thali", "Shahi Paneer thali", "Shahi Paneer Thali",
                         "Tori kaddu thali", "Tori Kaddu Thali", "Pav bhaji", "Pav Bhaji",
                         "Veg biryani", "Veg Biryani", "Rajma Rice", "Rajma rice"]:
                if term in old_notes:
                    std_term = standardize_meal_name(term)
                    new_notes = new_notes.replace(term, std_term)
            if old_notes != new_notes:
                cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, row_id))
                print(f"  Expenditure ID {row_id}: '{old_notes}' -> '{new_notes}'")

    conn.commit()
    conn.close()
    print("\nMeal prefixes migration completed successfully!")

if __name__ == "__main__":
    migrate()
