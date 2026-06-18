import sqlite3

def run_migration():
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    upi_data = {
        '2026-06-04': 11855, '2026-06-03': 10385, '2026-06-02': 13745, '2026-06-01': 14385,
        '2026-05-30': 5710,  '2026-05-29': 12485, '2026-05-27': 10870, '2026-05-26': 10920, '2026-05-25': 13379,
        '2026-05-23': 6015,  '2026-05-22': 14665, '2026-05-21': 10655, '2026-05-20': 11000, '2026-05-19': 12845,
        '2026-05-18': 11985, '2026-05-16': 6470,  '2026-05-15': 15735, '2026-05-14': 16930, '2026-05-13': 12060,
        '2026-05-12': 13185, '2026-05-11': 12730, '2026-05-09': 5890,  '2026-05-08': 15385, '2026-05-07': 15480,
        '2026-05-06': 11345, '2026-05-05': 10890, '2026-05-04': 13540, '2026-05-02': 4760,  '2026-04-30': 12820
    }
    
    print("Starting proportional UPI allocation migration...")
    
    for date, upi_target in upi_data.items():
        # Fetch all sales rows on this date
        rows = cursor.execute("SELECT id, sp, sold, payment FROM sales WHERE date=?", (date,)).fetchall()
        if not rows:
            print(f"⚠️ Warning: No sales found for date {date}")
            continue
            
        row_revenues = [r["sp"] * r["sold"] for r in rows]
        total_rev = sum(row_revenues)
        
        if total_rev < upi_target:
            raise ValueError(f"Error on {date}: Target UPI ({upi_target}) exceeds Total Revenue ({total_rev})")
            
        # 1. Proportional integer assignment
        upi_allocations = []
        for rev in row_revenues:
            if total_rev > 0:
                upi_allocations.append(round(rev * upi_target / total_rev))
            else:
                upi_allocations.append(0)
                
        # 2. Adjust remainder to match target exactly
        allocated_sum = sum(upi_allocations)
        diff = upi_target - allocated_sum
        
        if diff > 0:
            # We need to add diff to the rows that have headroom (allocated upi < row revenue)
            # Sort indices by headroom (rev - allocated) descending
            indices = sorted(range(len(rows)), key=lambda idx: row_revenues[idx] - upi_allocations[idx], reverse=True)
            for d_idx in range(diff):
                target_idx = indices[d_idx % len(indices)]
                upi_allocations[target_idx] += 1
        elif diff < 0:
            # We need to subtract abs(diff) from the rows that have positive allocated upi
            # Sort indices by allocated upi descending
            indices = sorted(range(len(rows)), key=lambda idx: upi_allocations[idx], reverse=True)
            for d_idx in range(abs(diff)):
                target_idx = indices[d_idx % len(indices)]
                upi_allocations[target_idx] -= 1
                
        # 3. Apply updates to DB
        new_total_upi = sum(upi_allocations)
        if new_total_upi != upi_target:
            raise RuntimeError(f"Rounding correction failed for {date}: sum={new_total_upi}, target={upi_target}")
            
        for idx, row in enumerate(rows):
            row_id = row["id"]
            row_rev = row_revenues[idx]
            row_upi = upi_allocations[idx]
            row_cash = row_rev - row_upi
            
            if row_upi < 0 or row_cash < 0:
                raise ValueError(f"Negative values generated on {date} row {row_id}: Cash={row_cash}, UPI={row_upi}")
                
            pmt_str = f"Cash: {int(row_cash)}, UPI: {int(row_upi)}, Card: 0"
            cursor.execute(
                "UPDATE sales SET payment=?, cash_amt=?, upi_amt=?, card_amt=? WHERE id=?",
                (pmt_str, float(row_cash), float(row_upi), 0.0, row_id)
            )
            
        print(f"✅ Date {date}: Allocated UPI = ₹{upi_target}, Cash = ₹{total_rev - upi_target} (Total = ₹{total_rev})")
        
    conn.commit()
    conn.close()
    print("Proportional UPI allocation migration complete!")

if __name__ == '__main__':
    run_migration()
