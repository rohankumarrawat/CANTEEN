"""
Add Batch_Prep usage entries for July 8 so the Ingredient Breakdown shows,
while keeping stock BCF levels unchanged by compensating the Opening baseline.
"""
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))
DATE = "2026-07-08"

# All items with Issue > 0 on July 8 (from the daily expenditure sheets)
# Format: (item_name_in_db, issue_qty)
issued_items = [
    ("Atta",                        50.000),
    ("Rice",                        35.000),
    ("Refined Oil (Expensive)",     11.500),
    ("Sarson Dana",                  0.020),
    ("Rajma",                       13.000),
    ("Rajma (Expensive)",            4.000),
    ("Jeera (s)",                    0.200),
    ("Haldi Powder",                 0.100),
    ("Haldi Powder(Expensive)",      0.100),
    ("Mirchi Powder",                0.200),
    ("Dalchini",                     0.020),
    ("Hing",                         1.000),
    ("Kitchen King",                 0.200),
    ("Deggi Mirch",                  0.200),
    ("Kasuri methi (Expensive)",     0.050),
    ("Garam Masala",                 0.200),
    ("Salt",                         2.000),
    ("Jeera Powder",                 0.200),
    ("Methi Dana(Expensive)",        0.050),
    ("Tej Patta(Expensive)",         0.020),
    ("Ajwain",                       0.050),
    ("Dhaniya Powder(Expensive)",    0.200),
    ("Shahi Paneer Masala (kgs)",    2.000),
    ("Imli (Expensive)",             0.100),
    ("Desi Ghee",                    1.000),
    ("Cream",                        1.000),
    # Packaging
    ("PP Box (Dal) Mini Meal",     800.000),
    ("Foil Box (Rice, Sabji)",     400.000),
    ("Roti Pouch",                2300.000),
    ("Salad Pkt",                  800.000),
    ("Spoon / Mini Meal",          440.000),
    ("Napkin Tissue Paper",        472.000),
    ("Salt Pouch",                 400.000),
    ("Pickle & Paratha",           472.000),
    ("Tape",                         1.000),
    ("Big Foil Box (Biryani)",      40.000),
    ("Paper Box (Lunch)",          400.000),
    ("Butter Roti Paper",          150.000),
    ("Paratha Box",                 72.000),
    ("Silver Foil",                  0.500),
    # Sweets
    ("Barfi",                       12.000),
    # Fresh
    ("Potato",                      10.000),
    ("Onion",                       14.000),
    ("Tomato",                       6.490),
    ("Tomato 'R'",                   9.000),
    ("Ginger",                       1.000),
    ("Garlic (Expensive)",           1.550),
    ("Green Chilli (Expensive)",     2.000),
    ("Coriander (Expensive)",        1.000),
    ("Capsicum",                    17.715),
    ("Beans",                        1.000),
    ("Carrot",                       1.000),
    ("Cauliflower",                  1.500),
    ("Cucumber (Expensive)",        12.000),
    ("LPG",                         26.900),
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print(f"Adding Batch_Prep entries for {len(issued_items)} items on July 8...")
added = 0
skipped = []

try:
    for item_name, issue_qty in issued_items:
        row = cursor.execute(
            "SELECT id FROM inventory WHERE item = ? COLLATE NOCASE", (item_name,)
        ).fetchone()

        if not row:
            skipped.append(item_name)
            continue

        inv_id = row[0]

        # 1. Add Batch_Prep entry on July 8
        cursor.execute("""
            INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
            VALUES (?, ?, 'Batch_Prep', ?, 'Material used for production')
        """, (DATE, inv_id, -issue_qty))

        # 2. Compensate by increasing the Opening baseline so net stock stays at BCF
        opening = cursor.execute("""
            SELECT id FROM stock_ledger
            WHERE inv_id = ? AND transaction_type = 'Opening'
            ORDER BY date LIMIT 1
        """, (inv_id,)).fetchone()

        if opening:
            cursor.execute(
                "UPDATE stock_ledger SET qty_change = ROUND(qty_change + ?, 4) WHERE id = ?",
                (issue_qty, opening[0])
            )
        else:
            cursor.execute("""
                INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                VALUES ('2026-04-30', ?, 'Opening', ?, 'Baseline opening stock')
            """, (inv_id, issue_qty))

        # 3. Update inventory.opening
        cursor.execute(
            "UPDATE inventory SET opening = ROUND(opening + ?, 4) WHERE id = ?",
            (issue_qty, inv_id)
        )
        added += 1

    conn.commit()
    print(f"\n✅ Done: {added} Batch_Prep entries added.")
    if skipped:
        print(f"⚠️  Skipped (not found in DB): {skipped}")

    # Verify stock unchanged for a couple of items
    for check in ["Atta", "Rice", "Rajma"]:
        s = cursor.execute("SELECT stock FROM inventory WHERE item = ?", (check,)).fetchone()[0]
        print(f"   {check} stock: {s}")

except Exception as e:
    conn.rollback()
    print(f"❌ ERROR: {e}")
    raise
finally:
    conn.close()
