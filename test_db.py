import sqlite3

conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
conn.row_factory = sqlite3.Row

tables = ['roles', 'users', 'user_roles', 'inventory', 'menu', 'recipes', 
          'goods_received', 'batch_prep', 'expenditure', 'sales', 
          'waste_tracker', 'stock_ledger']

for t in tables:
    try:
        conn.execute(f"SELECT * FROM {t} LIMIT 1")
    except Exception as e:
        print(f"Error checking {t}: {e}")

print("All tables checked.")
