import sqlite3

def run_verification():
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=== Verification for 11 May 2026 ===")
    date_11_may = "2026-05-11"
    
    # 1. Check samples count excluding 'Migrated from wastage' and 'Staff'
    all_samp = cursor.execute("SELECT * FROM samples WHERE date=?", (date_11_may,)).fetchall()
    compl_samp = [s for s in all_samp if s['notes'] != 'Migrated from wastage' and s['given_to'].lower() != 'staff']
    staff_samp = [s for s in all_samp if s['notes'] != 'Migrated from wastage' and s['given_to'].lower() == 'staff']
    
    print(f"Total samples in DB: {len(all_samp)}")
    print(f"Complimentary samples (excluding migrated): {sum(s['qty'] for s in compl_samp)}")
    print(f"Staff samples (excluding migrated): {sum(s['qty'] for s in staff_samp)}")
    
    # Check individual items
    for s in compl_samp:
        print(f"  - Item: {s['meal']}, Qty: {s['qty']}, Given to: {s['given_to']}, Notes: {s['notes']}")
    
    # 2. Check financial metrics for 11 May
    s_rows = cursor.execute("SELECT * FROM sales WHERE date=?", (date_11_may,)).fetchall()
    e_sum_rows = cursor.execute("SELECT category, SUM(amount) AS t FROM expenditure WHERE date=? GROUP BY category", (date_11_may,)).fetchall()
    w_row = cursor.execute("SELECT COALESCE(SUM(cost_lost),0) AS t FROM waste_tracker WHERE date=?", (date_11_may,)).fetchone()
    
    rev = sum(r["sp"]*r["sold"] for r in s_rows)
    exp = sum(r["t"] or 0 for r in e_sum_rows)
    waste = int(w_row["t"] or 0)
    net = rev - exp - waste
    
    print(f"Revenue: Rs. {rev}")
    print(f"Expenditure: Rs. {exp}")
    print(f"Wastage Cost: Rs. {waste}")
    print(f"Net Profit: Rs. {net}")

    print("\n=== Verification for 05 May 2026 ===")
    date_5_may = "2026-05-05"
    
    # 1. Check Lunch wastage
    lunch_sales = cursor.execute("SELECT * FROM sales WHERE date=? AND meal LIKE 'Lunch%'", (date_5_may,)).fetchone()
    if lunch_sales:
        print(f"Lunch Sold: {lunch_sales['sold']}")
        print(f"Lunch Wastage: {lunch_sales['wastage']}")
    else:
        print("Lunch sales record not found!")
        
    # 2. Check financial metrics for 5 May
    s_rows_5 = cursor.execute("SELECT * FROM sales WHERE date=?", (date_5_may,)).fetchall()
    e_sum_rows_5 = cursor.execute("SELECT category, SUM(amount) AS t FROM expenditure WHERE date=? GROUP BY category", (date_5_may,)).fetchall()
    w_row_5 = cursor.execute("SELECT COALESCE(SUM(cost_lost),0) AS t FROM waste_tracker WHERE date=?", (date_5_may,)).fetchone()
    
    rev_5 = sum(r["sp"]*r["sold"] for r in s_rows_5)
    exp_5 = sum(r["t"] or 0 for r in e_sum_rows_5)
    waste_5 = int(w_row_5["t"] or 0)
    net_5 = rev_5 - exp_5 - waste_5
    
    print(f"Revenue: Rs. {rev_5}")
    print(f"Expenditure: Rs. {exp_5}")
    print(f"Wastage Cost: Rs. {waste_5}")
    print(f"Net Profit: Rs. {net_5}")

    conn.close()

if __name__ == "__main__":
    run_verification()
