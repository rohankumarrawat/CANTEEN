import sqlite3

def run_migration():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    # Check if custom_name column already exists in batch_prep
    cursor.execute("PRAGMA table_info(batch_prep)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'custom_name' not in columns:
        print("Adding 'custom_name' column to 'batch_prep' table...")
        cursor.execute("ALTER TABLE batch_prep ADD COLUMN custom_name TEXT")
        conn.commit()
        print("Column added successfully!")
    else:
        print("Column 'custom_name' already exists in 'batch_prep' table.")
        
    conn.close()

if __name__ == '__main__':
    run_migration()
