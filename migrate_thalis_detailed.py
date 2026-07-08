import sqlite3

def migrate():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()

    thali_mappings = [
        ("Panchratna thali", "Panchratna Thali (Lauki Dal Chana Sabji, Panchratna Dal, Rice, Roti, Salad, Dry Petha)"),
        ("Aloo shimla thali", "Aloo Shimla Thali (Aloo Shimla Mirch, Kadhi Pakora, Rice, Roti, Salad, Badana)"),
        ("Kadhai paneer thali", "Kadhai Paneer Thali (Kadhai Paneer, Dal Rajma, Rice, Roti, Salad, Besan Barfi)"),
        ("Aloo soyabean thali", "Aloo Soyabean Thali (Aloo Soyabean, Kala Chana, Rice, Roti, Salad, Dry Petha)"),
        ("Shahi paneer thali", "Shahi Paneer Thali (Shahi Paneer, Dal Tadka, Rice, Roti, Salad, Besan Barfi)"),
    ]

    for old_name, new_name in thali_mappings:
        print(f"\n--- Migrating '{old_name}' -> '{new_name}' ---")
        
        # 1. Update menu table
        cursor.execute("UPDATE menu SET name = ? WHERE name = ?", (new_name, old_name))
        if cursor.rowcount > 0:
            print(f"  Updated menu item name in 'menu' table.")

        # 2. Update sales table (replaces the thali name inside Lunch(old_name))
        cursor.execute("SELECT id, meal FROM sales WHERE meal LIKE ?", (f"%{old_name}%",))
        sales_rows = cursor.fetchall()
        for row in sales_rows:
            row_id, old_meal = row
            new_meal = old_meal.replace(old_name, new_name)
            cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row_id))
            print(f"  Updated sales id {row_id}: '{old_meal}' -> '{new_meal}'")

        # 3. Update samples table (replaces the thali name inside Lunch(old_name))
        cursor.execute("SELECT id, meal FROM samples WHERE meal LIKE ?", (f"%{old_name}%",))
        samples_rows = cursor.fetchall()
        for row in samples_rows:
            row_id, old_meal = row
            new_meal = old_meal.replace(old_name, new_name)
            cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row_id))
            print(f"  Updated samples id {row_id}: '{old_meal}' -> '{new_meal}'")

        # 4. Update expenditure table (replaces thali name in notes)
        cursor.execute("SELECT id, notes FROM expenditure WHERE notes LIKE ?", (f"%{old_name}%",))
        exp_rows = cursor.fetchall()
        for row in exp_rows:
            row_id, old_notes = row
            new_notes = old_notes.replace(old_name, new_name)
            cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, row_id))
            print(f"  Updated expenditure id {row_id}: '{old_notes}' -> '{new_notes}'")

    conn.commit()
    conn.close()
    print("\nDatabase migration for detailed Lunch Thalis completed successfully!")

if __name__ == '__main__':
    migrate()
