import sqlite3

def run_migration():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    # Get IDs of both items
    cursor.execute("SELECT id FROM menu WHERE name = 'Mix Veg Paratha'")
    row_mix = cursor.fetchone()
    cursor.execute("SELECT id FROM menu WHERE name = 'Mixed Veg Paratha'")
    row_mixed = cursor.fetchone()
    
    if not row_mix or not row_mixed:
        print("Mix Veg Paratha or Mixed Veg Paratha not found. Maybe already merged?")
        conn.close()
        return
        
    mix_id = row_mix[0]
    mixed_id = row_mixed[0]
    
    print(f"Merging 'Mix Veg Paratha' (ID {mix_id}) into 'Mixed Veg Paratha' (ID {mixed_id})...")
    
    # 1. Update daily_menu
    cursor.execute("UPDATE daily_menu SET menu_id = ? WHERE menu_id = ?", (mixed_id, mix_id))
    print(f"Updated daily_menu rows: {cursor.rowcount}")
    
    # 2. Update sales
    cursor.execute("UPDATE sales SET menu_id = ?, meal = 'Mixed Veg Paratha' WHERE menu_id = ?", (mixed_id, mix_id))
    print(f"Updated sales rows: {cursor.rowcount}")
    
    # 3. Update batch_prep
    cursor.execute("UPDATE batch_prep SET menu_id = ? WHERE menu_id = ?", (mixed_id, mix_id))
    print(f"Updated batch_prep rows: {cursor.rowcount}")
    
    # 4. Update recipes
    cursor.execute("UPDATE recipes SET menu_id = ? WHERE menu_id = ?", (mixed_id, mix_id))
    print(f"Updated recipes rows: {cursor.rowcount}")
    
    # 5. Delete from menu
    cursor.execute("DELETE FROM menu WHERE id = ?", (mix_id,))
    print(f"Deleted duplicate menu item 'Mix Veg Paratha' from menu table.")
    
    conn.commit()
    conn.close()
    print("Merge migration completed successfully!")

if __name__ == '__main__':
    run_migration()
