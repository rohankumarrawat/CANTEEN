import sqlite3

expenditures = [
    # 30 April 2026
    ("2026-04-30", 25521.0, "Raw Materials", "Auto-expenditure for LUNCH batch"),
    ("2026-04-30", 2048.0, "Raw Materials", "Auto-expenditure for PARATHA batch"),
    ("2026-04-30", 2151.0, "Raw Materials", "Auto-expenditure for DAHI batch"),
    ("2026-04-30", 1755.0, "Raw Materials", "Auto-expenditure for CHACH batch"),
    ("2026-04-30", 873.0, "Raw Materials", "Auto-expenditure for MINI batch"),
    ("2026-04-30", 110.0, "Raw Materials", "Auto-expenditure for AMUL batch"),
    ("2026-04-30", 135.0, "Raw Materials", "Auto-expenditure for LAHARI JEERA batch"),
    ("2026-04-30", 342.0, "Raw Materials", "Auto-expenditure for LASSI batch"),
    
    # 02 May 2026
    ("2026-05-02", 7712.0, "Raw Materials", "Auto-expenditure for LUNCH batch"),
    ("2026-05-02", 476.0, "Raw Materials", "Auto-expenditure for MINI batch"),
]

def insert_exps():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    
    try:
        # Clear any existing auto-expenditures for these dates to prevent duplication
        cursor.execute("DELETE FROM expenditure WHERE date IN ('2026-04-30', '2026-05-02')")
        
        for date, amount, category, notes in expenditures:
            cursor.execute('''
                INSERT INTO expenditure (date, amount, category, notes)
                VALUES (?, ?, ?, ?)
            ''', (date, amount, category, notes))
            
        conn.commit()
        print("🎉 Daily expenditures successfully inserted for 30 Apr and 02 May!")
        
    except Exception as e:
        print(f"Error inserting expenditures: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    insert_exps()
