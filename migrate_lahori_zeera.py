import sqlite3

def run_migration():
    db_path = "canteen.db"
    print(f"Connecting to database: {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Update inventory.item
        cursor.execute("SELECT COUNT(*) FROM inventory WHERE item = 'Lahori Zeera'")
        inv_count = cursor.fetchone()[0]
        cursor.execute("UPDATE inventory SET item = 'Lahori Zeera' WHERE item = 'Lahori Zeera'")
        print(f"Updated {inv_count} rows in 'inventory' table.")
        
        # 2. Update menu.name
        cursor.execute("SELECT COUNT(*) FROM menu WHERE name = 'Lahori Zeera'")
        menu_count = cursor.fetchone()[0]
        cursor.execute("UPDATE menu SET name = 'Lahori Zeera' WHERE name = 'Lahori Zeera'")
        print(f"Updated {menu_count} rows in 'menu' table.")
        
        # 3. Update expenditure.notes
        cursor.execute("SELECT COUNT(*) FROM expenditure WHERE notes LIKE '%Lahori Zeera%' OR notes LIKE '%LAHORI ZEERA%'")
        exp_count = cursor.fetchone()[0]
        cursor.execute("UPDATE expenditure SET notes = REPLACE(notes, 'Lahori Zeera', 'Lahori Zeera') WHERE notes LIKE '%Lahori Zeera%'")
        cursor.execute("UPDATE expenditure SET notes = REPLACE(notes, 'LAHORI ZEERA', 'LAHORI ZEERA') WHERE notes LIKE '%LAHORI ZEERA%'")
        print(f"Updated {exp_count} rows in 'expenditure' table.")
        
        # 4. Update sales.meal
        cursor.execute("SELECT COUNT(*) FROM sales WHERE meal LIKE '%Lahori Zeera%' OR meal LIKE '%LAHORI ZEERA%'")
        sales_count = cursor.fetchone()[0]
        cursor.execute("UPDATE sales SET meal = REPLACE(meal, 'Lahori Zeera', 'Lahori Zeera') WHERE meal LIKE '%Lahori Zeera%'")
        cursor.execute("UPDATE sales SET meal = REPLACE(meal, 'LAHORI ZEERA', 'LAHORI ZEERA') WHERE meal LIKE '%LAHORI ZEERA%'")
        print(f"Updated {sales_count} rows in 'sales' table.")
        
        # 5. Update samples.meal and notes
        cursor.execute("SELECT COUNT(*) FROM samples WHERE meal LIKE '%Lahori Zeera%' OR meal LIKE '%LAHORI ZEERA%' OR notes LIKE '%Lahori Zeera%' OR notes LIKE '%LAHORI ZEERA%'")
        samples_count = cursor.fetchone()[0]
        cursor.execute("UPDATE samples SET meal = REPLACE(meal, 'Lahori Zeera', 'Lahori Zeera') WHERE meal LIKE '%Lahori Zeera%'")
        cursor.execute("UPDATE samples SET meal = REPLACE(meal, 'LAHORI ZEERA', 'LAHORI ZEERA') WHERE meal LIKE '%LAHORI ZEERA%'")
        cursor.execute("UPDATE samples SET notes = REPLACE(notes, 'Lahori Zeera', 'Lahori Zeera') WHERE notes LIKE '%Lahori Zeera%'")
        cursor.execute("UPDATE samples SET notes = REPLACE(notes, 'LAHORI ZEERA', 'LAHORI ZEERA') WHERE notes LIKE '%LAHORI ZEERA%'")
        print(f"Updated {samples_count} rows in 'samples' table.")
        
        conn.commit()
        print("🎉 Database migration completed successfully!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error during database migration: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
