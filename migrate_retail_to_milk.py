import sqlite3

def run_migration():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    # 1. Target retail items and their defaults for inventory
    retail_items = [
        ("Lahori Zeera", "Milk Based Product", "Btl", 0.0, 5.0, 0.0, 8.0),
        ("Chach",        "Milk Based Product", "Pkt", 0.0, 5.0, 0.0, 8.0),
        ("Amul Kool",    "Milk Based Product", "Pkt", 0.0, 5.0, 0.0, 20.0),
        ("Lassi",        "Milk Based Product", "Pkt", 0.0, 5.0, 0.0, 16.0),
        ("Brownie",      "Milk Based Product", "Pcs", 0.0, 5.0, 0.0, 30.0),
        ("Plum Cake",    "Milk Based Product", "Pcs", 0.0, 5.0, 0.0, 15.0),
        ("Burfi",        "Milk Based Product", "Kgs", 0.0, 5.0, 0.0, 280.0),
        ("Petha",        "Milk Based Product", "Kgs", 0.0, 5.0, 0.0, 150.0),
        ("Paneer",       "Milk Based Product", "Kgs", 0.0, 5.0, 0.0, 250.0),
        ("Dahi",         "Milk Based Product", "Kgs", 0.0, 5.0, 0.0, 75.0),
        ("Guldana",      "Milk Based Product", "Kgs", 0.0, 5.0, 0.0, 250.0)
    ]
    
    print("Migrating/Inserting retail items to 'Milk Based Product' category...")
    
    for item, cat, unit, stock, min_lvl, opening, cp in retail_items:
        # Check if the item already exists (case-insensitive check)
        cursor.execute("SELECT id, item, cat, unit, cp FROM inventory WHERE item = ? COLLATE NOCASE", (item,))
        row = cursor.fetchone()
        
        if row:
            row_id, existing_name, existing_cat, existing_unit, existing_cp = row
            # Update the category and standard name if it exists
            cursor.execute(
                "UPDATE inventory SET item = ?, cat = ? WHERE id = ?",
                (item, cat, row_id)
            )
            print(f"Updated existing item: '{existing_name}' (ID {row_id}) -> Category '{cat}'")
        else:
            # Insert the new item
            cursor.execute(
                "INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, cp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item, cat, unit, stock, min_lvl, opening, cp)
            )
            print(f"Inserted new retail item: '{item}' with Category '{cat}'")
            
    conn.commit()
    
    # Verify the results
    cursor.execute("SELECT item, cat FROM inventory WHERE cat = 'Milk Based Product'")
    results = cursor.fetchall()
    print("\nVerified Milk Based Product items:")
    for r in results:
        print(f" - {r[0]}: {r[1]}")
        
    conn.close()

if __name__ == '__main__':
    run_migration()
