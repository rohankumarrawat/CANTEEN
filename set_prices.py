import sqlite3

def update_realistic_prices():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    # Realistic prices for an army/institutional canteen
    prices = {
        'Lunch': 60.0,
        'Mini Mil': 35.0,
        'Paratha': 20.0
    }
    
    try:
        print("Setting realistic selling prices in the menu...")
        for meal_name, sp in prices.items():
            # Update menu table
            cursor.execute("UPDATE menu SET sp = ? WHERE name = ?", (sp, meal_name))
            
            # Update historical sales records
            cursor.execute("UPDATE sales SET sp = ? WHERE meal = ?", (sp, meal_name))
            
        conn.commit()
        print("Prices updated successfully! Revenue will now calculate correctly.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_realistic_prices()
