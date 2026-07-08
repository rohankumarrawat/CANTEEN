# Script to insert July 8 expenditure records
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

DATE = "2026-07-08"

expenditures = [
    (23543.0, "Raw Materials", "Auto-expenditure for LUNCH batch"),
    (2486.0, "Raw Materials", "Auto-expenditure for Paratha batch"),
    (1308.0, "Raw Materials", "Auto-expenditure for MINI MEAL batch"),
    (2151.0, "Raw Materials", "Auto-expenditure for DAHI batch"),
    (1737.0, "Raw Materials", "Auto-expenditure for CHACH batch"),
    (90.0, "Raw Materials", "Auto-expenditure for AMUL COOL batch"),
    (36.0, "Raw Materials", "Auto-expenditure for LAHORI ZEE batch")
]

print("Inserting July 8 expenditure records...")
try:
    # Delete any existing expenditure records first to prevent duplicates
    cursor.execute("DELETE FROM expenditure WHERE date = ?", (DATE,))
    deleted = cursor.rowcount
    print(f"Cleared {deleted} existing expenditure records for July 8.")

    for amount, category, notes in expenditures:
        cursor.execute('''
            INSERT INTO expenditure (date, amount, category, notes)
            VALUES (?, ?, ?, ?)
        ''', (DATE, amount, category, notes))
        
    conn.commit()
    print(f"✅ Successfully inserted {len(expenditures)} expenditure records for July 8.")
    
    # Verify the sum
    total_exp = cursor.execute("SELECT SUM(amount) FROM expenditure WHERE date = ?", (DATE,)).fetchone()[0]
    print(f"Total Expenditure on July 8 is now: {total_exp}")

except Exception as e:
    conn.rollback()
    print(f"❌ ERROR: {e}")
    raise
finally:
    conn.close()
