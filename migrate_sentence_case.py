import sqlite3
import re

def sentence_case(s):
    if not s:
        return s
    tokens = re.split(r'(\s+|[()/{}])', s)
    result = []
    is_first = True
    for t in tokens:
        if t.isalnum():
            # Special acronyms/units to keep uppercase:
            if t.upper() in ["LPG", "PP", "ML", "BBF", "BCF", "UPI"]:
                result.append(t.upper())
            else:
                if is_first:
                    result.append(t.capitalize())
                    is_first = False
                else:
                    result.append(t.lower())
        else:
            result.append(t)
    return "".join(result)

def migrate():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Update inventory table
    inventory_items = cursor.execute("SELECT id, item FROM inventory").fetchall()
    for row in inventory_items:
        old_name = row["item"]
        new_name = sentence_case(old_name)
        if old_name != new_name:
            print(f"Inventory: '{old_name}' -> '{new_name}'")
            cursor.execute("UPDATE inventory SET item = ? WHERE id = ?", (new_name, row["id"]))

    # 2. Update menu table
    menu_items = cursor.execute("SELECT id, name FROM menu").fetchall()
    for row in menu_items:
        old_name = row["name"]
        new_name = sentence_case(old_name)
        if old_name != new_name:
            print(f"Menu: '{old_name}' -> '{new_name}'")
            cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (new_name, row["id"]))

    # 3. Update sales table (meal column)
    sales_records = cursor.execute("SELECT id, meal FROM sales").fetchall()
    for row in sales_records:
        old_meal = row["meal"]
        m = re.match(r"^([^(]+)\(([^)]+)\)$", old_meal)
        if m:
            prefix = m.group(1)
            meal_name = m.group(2)
            new_meal = f"{sentence_case(prefix)}({sentence_case(meal_name)})"
        else:
            new_meal = sentence_case(old_meal)
        if old_meal != new_meal:
            print(f"Sales Meal: '{old_meal}' -> '{new_meal}'")
            cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row["id"]))

    # 4. Update samples table (meal column)
    samples_records = cursor.execute("SELECT id, meal FROM samples").fetchall()
    for row in samples_records:
        old_meal = row["meal"]
        m = re.match(r"^([^(]+)\(([^)]+)\)$", old_meal)
        if m:
            prefix = m.group(1)
            meal_name = m.group(2)
            new_meal = f"{sentence_case(prefix)}({sentence_case(meal_name)})"
        else:
            new_meal = sentence_case(old_meal)
        if old_meal != new_meal:
            print(f"Samples Meal: '{old_meal}' -> '{new_meal}'")
            cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row["id"]))

    # 5. Update expenditure table (notes column)
    exp_records = cursor.execute("SELECT id, notes FROM expenditure").fetchall()
    for row in exp_records:
        old_notes = row["notes"]
        if old_notes:
            m = re.match(r"^(Auto-expenditure for )([A-Za-z0-9 ]+)( batch)$", old_notes, re.IGNORECASE)
            if m:
                prefix = m.group(1)
                meal_token = m.group(2)
                suffix = m.group(3)
                if meal_token.upper() == "MINI":
                    new_token = "Mini meal"
                else:
                    new_token = sentence_case(meal_token)
                new_notes = f"{prefix}{new_token}{suffix}"
            else:
                new_notes = sentence_case(old_notes)
            
            if old_notes != new_notes:
                print(f"Expenditure Note: '{old_notes}' -> '{new_notes}'")
                cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, row["id"]))

    conn.commit()
    conn.close()
    print("Migration finished!")

if __name__ == '__main__':
    migrate()
