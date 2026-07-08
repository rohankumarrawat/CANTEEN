import sqlite3

def migrate():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()

    old_name = "Tori kaddu thali"
    new_name = "Tori Kaddu Thali (Tori, Kaddu, Dal Chana, Chapati, Rice)"

    # 1. Update menu table
    cursor.execute("UPDATE menu SET name = ? WHERE name = ?", (new_name, old_name))
    print(f"Updated menu item name to: {new_name}")

    # 2. Update sales table
    cursor.execute("SELECT id, meal FROM sales WHERE meal LIKE ?", (f"%{old_name}%",))
    sales_rows = cursor.fetchall()
    for row in sales_rows:
        row_id, old_meal = row
        new_meal = old_meal.replace(old_name, new_name)
        cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row_id))
        print(f"Updated sales id {row_id}: '{old_meal}' -> '{new_meal}'")

    # 3. Update samples table
    cursor.execute("SELECT id, meal FROM samples WHERE meal LIKE ?", (f"%{old_name}%",))
    samples_rows = cursor.fetchall()
    for row in samples_rows:
        row_id, old_meal = row
        new_meal = old_meal.replace(old_name, new_name)
        cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row_id))
        print(f"Updated samples id {row_id}: '{old_meal}' -> '{new_meal}'")

    # 4. Update expenditure table
    cursor.execute("SELECT id, notes FROM expenditure WHERE notes LIKE ?", (f"%{old_name}%",))
    exp_rows = cursor.fetchall()
    for row in exp_rows:
        row_id, old_notes = row
        new_notes = old_notes.replace(old_name, new_name)
        cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, row_id))
        print(f"Updated expenditure id {row_id}: '{old_notes}' -> '{new_notes}'")

    conn.commit()
    conn.close()
    print("Database migration for Tori kaddu thali completed successfully!")

if __name__ == '__main__':
    migrate()
