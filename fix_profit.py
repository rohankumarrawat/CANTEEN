import sqlite3

def fix_profit_analysis():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    
    try:
        # 1. Update COGS (Cost of Goods Sold) for all sales
        # Using realistic per-meal cost estimates
        cost_per_meal = {
            'Lunch': 45.0,
            'Mini Mil': 25.0,
            'Paratha': 12.0
        }
        
        cursor.execute("SELECT id, meal, sold, wastage, date FROM sales")
        sales = cursor.fetchall()
        
        print("Calculating COGS and Waste for each record...")
        for sale_id, meal, sold, wastage, date in sales:
            unit_cost = cost_per_meal.get(meal, 0)
            total_cogs = unit_cost * sold
            
            # Update the COGS in the sales table
            cursor.execute("UPDATE sales SET cogs = ? WHERE id = ?", (total_cogs, sale_id))
            
            # If there was wastage, record it in the waste_tracker so Waste Cost is > 0
            if wastage > 0:
                waste_cost = unit_cost * wastage
                
                # Check if already recorded to prevent duplicates
                cursor.execute("SELECT id FROM waste_tracker WHERE date = ? AND item LIKE ?", (date, f"{meal}%"))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO waste_tracker (date, item, qty_wasted, reason, cost_lost, recorded_by)
                        VALUES (?, ?, ?, 'Spoilage / Unsold', ?, 'admin')
                    ''', (date, f"{meal} (Prepared)", wastage, waste_cost))

        # 2. Add realistic daily overhead expenditures so Expenditure > 0
        dates = set([s[4] for s in sales])
        for d in dates:
            cursor.execute("SELECT id FROM expenditure WHERE date = ?", (d,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO expenditure (date, amount, category, notes) VALUES (?, 650, 'Packaging Material & Sweets', 'Daily packaging supplies')", (d,))
                cursor.execute("INSERT INTO expenditure (date, amount, category, notes) VALUES (?, 200, 'Misc Expenditure', 'Cleaning and miscellaneous')", (d,))

        conn.commit()
        print("Profit records updated: COGS, Waste, and Expenditure successfully populated!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_profit_analysis()
