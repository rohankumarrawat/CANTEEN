import sqlite3

def check_all_tables():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row['name'] for row in cursor.fetchall()]
    
    for table in tables:
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col['name'] for col in cursor.fetchall()]
        
        # Search each text column for 'Javtitri' or 'Javitri'
        for col in columns:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE CAST({col} AS TEXT) LIKE '%Javtitri%'")
                count_javtitri = cursor.fetchone()[0]
                
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE CAST({col} AS TEXT) LIKE '%Javitri%'")
                count_javitri = cursor.fetchone()[0]
                
                if count_javtitri > 0 or count_javitri > 0:
                    print(f"Table '{table}', Column '{col}': Javtitri={count_javtitri}, Javitri={count_javitri}")
            except Exception as e:
                # Some columns might not support LIKE or CAST, ignore those
                pass
                
    conn.close()

if __name__ == '__main__':
    check_all_tables()
