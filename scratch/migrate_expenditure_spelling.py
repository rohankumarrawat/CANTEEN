import sqlite3

def migrate():
    conn = sqlite3.connect("canteen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    rows = cursor.execute("SELECT id, category, notes FROM expenditure").fetchall()
    updated_count = 0

    for r in rows:
        rid = r["id"]
        cat = r["category"]
        notes = r["notes"] or ""
        
        new_cat = cat
        if cat == "Raw Materials":
            new_cat = "Raw Material"

        new_notes = notes
        if "Auto-expenditure" in notes or "Auto-Expenditure" in notes:
            # Normalize to "Auto-Expenditure"
            new_notes = notes.replace("Auto-expenditure", "Auto-Expenditure")
            # Capitalize "Batch"
            new_notes = new_notes.replace("batch", "Batch")
            # Fix spellings and capitalizations of meal names
            new_notes = new_notes.replace("Lahori zeera", "Lahori Zeera")
            new_notes = new_notes.replace("Mini meal", "Mini Meal")
            new_notes = new_notes.replace("Plum cake", "Plum Cake")
            new_notes = new_notes.replace("Chach", "Chhaach")

        if new_cat != cat or new_notes != notes:
            cursor.execute(
                "UPDATE expenditure SET category = ?, notes = ? WHERE id = ?",
                (new_cat, new_notes, rid)
            )
            updated_count += 1

    conn.commit()
    print(f"Updated {updated_count} expenditure rows.")
    conn.close()

if __name__ == "__main__":
    migrate()
