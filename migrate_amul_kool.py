import sqlite3

def migrate():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    # 1. Update menu
    cursor.execute("UPDATE menu SET name = 'Amul Kool' WHERE name = 'Amul Kool'")
    print(f"Updated {cursor.rowcount} rows in menu table.")
    
    # 2. Update inventory
    cursor.execute("UPDATE inventory SET item = 'Amul Kool' WHERE item = 'Amul Kool'")
    print(f"Updated {cursor.rowcount} rows in inventory table.")
    
    # 3. Update sales
    cursor.execute("UPDATE sales SET meal = 'Amul Kool' WHERE meal = 'Amul Kool'")
    print(f"Updated {cursor.rowcount} rows in sales table.")
    
    # 4. Update samples
    cursor.execute("UPDATE samples SET meal = 'Amul Kool' WHERE meal = 'Amul Kool'")
    print(f"Updated {cursor.rowcount} rows in samples table (meal).")
    
    cursor.execute("UPDATE samples SET notes = REPLACE(notes, 'AMUL KOOL', 'AMUL KOOL') WHERE notes LIKE '%AMUL KOOL%'")
    print(f"Updated {cursor.rowcount} rows in samples table (notes, uppercase).")
    
    cursor.execute("UPDATE samples SET notes = REPLACE(notes, 'Amul Kool', 'Amul Kool') WHERE notes LIKE '%Amul Kool%'")
    print(f"Updated {cursor.rowcount} rows in samples table (notes, titlecase).")
    
    # 5. Update expenditure
    cursor.execute("UPDATE expenditure SET notes = REPLACE(notes, 'AMUL KOOL', 'AMUL KOOL') WHERE notes LIKE '%AMUL KOOL%'")
    print(f"Updated {cursor.rowcount} rows in expenditure table (notes, uppercase).")
    
    cursor.execute("UPDATE expenditure SET notes = REPLACE(notes, 'Amul Kool', 'Amul Kool') WHERE notes LIKE '%Amul Kool%'")
    print(f"Updated {cursor.rowcount} rows in expenditure table (notes, titlecase).")
    
    conn.commit()
    conn.close()
    print("Database migration completed successfully.")

if __name__ == '__main__':
    migrate()
