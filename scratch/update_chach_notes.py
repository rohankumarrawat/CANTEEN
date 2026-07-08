import os
import glob
import sqlite3

def main():
    # 1. Update the database records
    db_path = "canteen.db"
    if os.path.exists(db_path):
        print("Connecting to canteen.db...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current records
        cursor.execute("SELECT id, date, meal, qty, notes, given_to FROM samples WHERE notes LIKE '%CHACH FOR STAFF%'")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows to update in samples table:")
        for r in rows:
            print(f"  - ID {r[0]}: date={r[1]}, meal={r[2]}, qty={r[3]}, notes={r[4]}, given_to={r[5]}")
            
        # Execute update
        cursor.execute("UPDATE samples SET notes = REPLACE(notes, 'STAFF', 'LADIES') WHERE notes LIKE '%CHACH FOR STAFF%'")
        conn.commit()
        print(f"Successfully updated {cursor.rowcount} rows in database.")
        
        # Check again
        cursor.execute("SELECT id, date, meal, qty, notes, given_to FROM samples WHERE notes LIKE '%CHACH FOR LADIES%'")
        updated_rows = cursor.fetchall()
        print(f"Now {len(updated_rows)} rows have 'CHACH FOR LADIES' notes in database.")
        conn.close()
    else:
        print("canteen.db not found!")

    # 2. Update the seed files
    seed_files = glob.glob("seed_*.py")
    print(f"Found {len(seed_files)} seed files. Scanning for 'CHACH FOR STAFF'...")
    
    updated_files_count = 0
    for file_path in seed_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "CHACH FOR STAFF" in content:
            new_content = content.replace("CHACH FOR STAFF", "CHACH FOR LADIES")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  - Updated: {file_path}")
            updated_files_count += 1
            
    print(f"Successfully updated {updated_files_count} seed files.")

if __name__ == "__main__":
    main()
