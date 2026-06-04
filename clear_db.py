import sqlite3

def reset_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    # List of tables to clear
    tables_to_clear = [
        'inventory',
        'menu',
        'recipes',
        'goods_received',
        'batch_prep',
        'expenditure',
        'sales',
        'waste_tracker',
        'stock_ledger',
        'daily_menu'
    ]
    
    try:
        # Disable foreign keys temporarily if needed, though simple deletes usually work if done safely
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        for table in tables_to_clear:
            cursor.execute(f"DELETE FROM {table};")
            # Reset auto-increment counter
            cursor.execute("DELETE FROM sqlite_sequence WHERE name=?;", (table,))
            print(f"Cleared table: {table}")
            
        conn.commit()
        cursor.execute("PRAGMA foreign_keys = ON;")
        print("Database reset successful. Users and roles preserved.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    reset_db()
