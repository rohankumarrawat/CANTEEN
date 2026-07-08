import sqlite3
import glob
import re
import os

def parse_items_from_seeds():
    seed_files = glob.glob('/Users/rohan/Desktop/canteen/seed_*.py')
    seed_items = set()
    
    # We want to match strings that look like inventory item names.
    # In seed_db.py: ("Potato", "Vegetables", "Kgs", 12.000, 0.000) or ("Urad (s)", "Dry", "Kgs", 120.00, 0.000)
    # In daily seed files: ('Potato', 'Kgs', ...)
    for path in seed_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to find tuples like ('Item Name', 'Unit', ...) or ("Item Name", "Unit", ...)
        # We can also search for anything quoted that starts with capital letters and is followed by unit like Kgs, Ltr, Nos, Pkt, Kg, Nos, Nos.
        # Let's extract items from:
        # 1. inventory_data list in seed_db.py
        # 2. Daily updates list: (item, unit, opening, received, consumed, rate, cogs, closing, value)
        # Let's write a simpler regex or parse them by matching common patterns.
        # Or even better, let's execute the seed scripts in a sandbox or parse their AST!
        # Actually, let's just find all double or single quoted strings in lines that have Kgs, Ltr, Nos, Pkt, Kg.
        for line in content.split('\n'):
            matches = re.findall(r"['\"]([^'\"]+)['\"]", line)
            for m in matches:
                # If the line has indicators of inventory record (e.g. rate, kgs, etc)
                if any(x in line for x in ['Kgs', 'Ltr', 'Nos', 'Pkt', 'Kg', 'Nos', 'Btl', 'PKT']):
                    # Filter out units, categories
                    if m not in ['Kgs', 'Ltr', 'Nos', 'Pkt', 'Kg', 'Btl', 'Pkt', 'Dry', 'Vegetables', 'Package material', 'Sweets', 'Milk', 'Misc', 'Nos']:
                        # Skip things like column headers or comments
                        if not any(x in m for x in ['item_name', 'category', 'unit', 'rate', 'issue_qty', 'Auto-expenditure', 'Lunch', 'Mini meal', 'Paratha', 'Mini Mil', 'Complimentary', 'Sweets', 'Vegetables', 'Milk', 'Misc', 'Package material']):
                            seed_items.add(m)
    return seed_items

def main():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    conn.row_factory = sqlite3.Row
    db_items = {row['item'] for row in conn.execute("SELECT item FROM inventory").fetchall()}
    conn.close()
    
    seed_items = parse_items_from_seeds()
    
    print(f"Total unique items in DB: {len(db_items)}")
    print(f"Total unique items extracted from seeds: {len(seed_items)}")
    
    print("\n--- Items in Seeds but NOT in DB ---")
    not_in_db = sorted(list(seed_items - db_items))
    for item in not_in_db:
        print(f"  {item}")
        
    print("\n--- Items in DB but NOT in Seeds ---")
    not_in_seeds = sorted(list(db_items - seed_items))
    for item in not_in_seeds:
        print(f"  {item}")

if __name__ == '__main__':
    main()
