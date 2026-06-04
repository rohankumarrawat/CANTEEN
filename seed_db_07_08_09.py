import sqlite3

# We will process 3 days of data: 7th May, 8th May, and 9th May
days_data = [
    {
        "date": "2026-05-07",
        "sales": [("Lunch", 523, 20), ("Mini Mil", 62, 0), ("Paratha", 73, 0)],
        "rates": {
            "POTATO": 10.0, "ONION": 23.0, "TOMATO": 18.0, "GINGER": 135.0, 
            "GREEN CHILLI": 55.0
        }
    },
    {
        "date": "2026-05-08",
        "sales": [("Lunch", 540, 20), ("Mini Mil", 62, 0), ("Paratha", 73, 0)],
        "rates": {
            "POTATO": 10.0, "ONION": 23.0, "TOMATO": 18.0, "GINGER": 135.0, 
            "GREEN CHILLI": 60.0, "PAV/KULCHA": 30.0
            # Also adding PEAS GREEN since it appeared on the 8th sheet
        },
        "new_items": [("PEAS GREEN", "Vegetables", "Kgs", 95.0)]
    },
    {
        "date": "2026-05-09",
        "sales": [("Lunch", 142, 12), ("Mini Mil", 18, 0), ("Paratha", 0, 0)],
        "rates": {
            "POTATO": 10.0, "ONION": 22.0, "TOMATO": 16.0, "GINGER": 65.0, 
            "GREEN CHILLI": 60.0, "PUMPKIN": 15.0, "CORRENDER": 20.0, 
            "CAPSICUM": 22.0, "BOTTLE GD": 12.0, "DAHI": 75.0, "PAV/KULCHA": 35.0
        }
    }
]

def update_db():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    try:
        for day in days_data:
            date = day["date"]
            print(f"Processing data for {date}...")
            
            # Update rates
            for item, rate in day.get("rates", {}).items():
                cursor.execute("UPDATE inventory SET cp = ? WHERE item = ?", (rate, item))
                
            # Add new items if any
            for item, cat, unit, rate in day.get("new_items", []):
                cursor.execute("SELECT id FROM inventory WHERE item = ?", (item,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO inventory (item, cat, unit, stock, cp) 
                        VALUES (?, ?, ?, 0, ?)
                    ''', (item, cat, unit, rate))
            
            # Insert Sales
            for meal, sold, tasting in day["sales"]:
                # Ensure menu item exists
                cursor.execute("SELECT id FROM menu WHERE name = ?", (meal,))
                row = cursor.fetchone()
                if row:
                    menu_id = row[0]
                else:
                    cursor.execute("INSERT INTO menu (name, sp, active) VALUES (?, 0, 1)", (meal,))
                    menu_id = cursor.lastrowid
                
                # Insert the sale record
                cursor.execute('''
                    INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment)
                    VALUES (?, ?, ?, 0, ?, ?, 0, 'Cash')
                ''', (date, menu_id, meal, sold, tasting))
                
        conn.commit()
        print("Data for 7th, 8th, and 9th May added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_db()
