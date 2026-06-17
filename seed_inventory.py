import sqlite3
import random

def seed_realistic_inventory():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, item, cat, unit FROM inventory")
        items = cursor.fetchall()
        
        for inv_id, name, cat, unit in items:
            name_lower = name.lower()
            
            # Determine realistic ranges based on category and item name
            if cat == 'Packaging':
                min_lvl = random.choice([500, 1000])
                stock = min_lvl + random.randint(200, 2000)
                opening = stock - random.randint(0, int(stock/2))
                received = stock - opening + random.randint(50, 200) # simulated
            elif cat == 'Vegetables':
                min_lvl = random.choice([10, 15, 20])
                # Herbs/small veggies
                if any(x in name_lower for x in ['chilli', 'ginger', 'garlic', 'coriander']):
                    min_lvl = 2
                    stock = random.uniform(3.0, 8.0)
                else:
                    stock = min_lvl + random.uniform(5.0, 40.0)
                opening = max(0, stock - random.uniform(0, stock/2))
                received = stock - opening + random.uniform(0, 10)
            elif cat == 'Dry':
                if 'atta' in name_lower or 'rice' in name_lower or 'lpg' in name_lower:
                    min_lvl = 50
                    stock = random.uniform(60.0, 250.0)
                elif 'dal' in name_lower or 'rajmah' in name_lower or 'chana' in name_lower or 'oil' in name_lower or 'ghee' in name_lower or 'sugar' in name_lower:
                    min_lvl = 10
                    stock = random.uniform(15.0, 60.0)
                else:
                    # Spices / small dry items
                    min_lvl = random.choice([0.5, 1.0, 2.0])
                    stock = min_lvl + random.uniform(0.5, 5.0)
                opening = max(0, stock - random.uniform(0, stock/2))
                received = stock - opening + random.uniform(0, stock/3)
            elif cat == 'Sweets':
                min_lvl = 5
                stock = random.uniform(10.0, 30.0)
                opening = max(0, stock - random.uniform(0, stock/2))
                received = stock - opening + random.uniform(0, 5)
            else:
                min_lvl = 5
                stock = random.uniform(10.0, 50.0)
                opening = max(0, stock - random.uniform(0, stock/2))
                received = stock - opening + random.uniform(0, 10)
            
            # Rounding for cleanliness
            if unit == 'Nos':
                stock = round(stock)
                min_lvl = round(min_lvl)
                opening = round(opening)
                received = round(received)
            else:
                stock = round(stock, 3)
                min_lvl = round(min_lvl, 3)
                opening = round(opening, 3)
                received = round(received, 3)
                
            cursor.execute('''
                UPDATE inventory 
                SET stock = ?, min_lvl = ?, opening = ?, received = ?
                WHERE id = ?
            ''', (stock, min_lvl, opening, received, inv_id))
            
        conn.commit()
        print("Realistic stock levels applied to all items successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    seed_realistic_inventory()
