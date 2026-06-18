import sqlite3

def run_migration():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    # 1. Update Burfi to Barfi in inventory table
    cursor.execute("UPDATE inventory SET item = 'Barfi' WHERE item = 'Burfi'")
    print(f"Updated Burfi to Barfi: {cursor.rowcount} rows affected.")
    
    # 2. Standardize units in inventory table
    unit_map = {
        'KGS': 'Kgs',
        'kgs': 'Kgs',
        'NOS': 'Nos',
        'PKT': 'Pkt',
        'BTL': 'Btl',
        'LTR': 'Ltr',
        'PCS': 'Pcs'
    }
    for old, new in unit_map.items():
        cursor.execute("UPDATE inventory SET unit = ? WHERE unit = ?", (new, old))
        print(f"Standardized unit '{old}' -> '{new}': {cursor.rowcount} rows affected.")
        
    # 3. Update Chach notes in samples table
    chach_map = {
        '07 X CHACH FOR LADIES': '07 × Chach for Ladies / Staff (Chach – 07 nos.)',
        '06 X CHACH FOR LADIES': '06 × Chach for Ladies',
        '05 X CHACH FOR LADIES': '05 × Chach for Ladies'
    }
    for old, new in chach_map.items():
        cursor.execute("UPDATE samples SET notes = ? WHERE notes = ?", (new, old))
        print(f"Updated sample notes '{old}' -> '{new}': {cursor.rowcount} rows affected.")
        
    conn.commit()
    conn.close()
    print("Database report fixes migration complete!")

if __name__ == '__main__':
    run_migration()
