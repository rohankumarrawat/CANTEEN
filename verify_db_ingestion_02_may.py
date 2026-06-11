import sqlite3

DATE = "2026-05-02"

def run_verifications():
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    errors = []

    print("=== STARTING DATABASE INTEGRITY VERIFICATION FOR 02 MAY 2026 ===")

    # Helper function to get ledger issues sum for a set of item IDs
    def get_ledger_issue_val(inv_ids):
        if not inv_ids:
            return 0.0
        placeholders = ",".join("?" for _ in inv_ids)
        rows = cursor.execute(f'''
            SELECT sl.qty_change, i.cp
            FROM stock_ledger sl
            JOIN inventory i ON i.id = sl.inv_id
            WHERE sl.date = ? AND sl.transaction_type = 'Batch_Prep' AND sl.inv_id IN ({placeholders})
        ''', [DATE] + list(inv_ids)).fetchall()
        return sum(-row['qty_change'] * row['cp'] for row in rows)

    # Helper function to get current stock value for a set of item IDs
    def get_stock_val(inv_ids):
        if not inv_ids:
            return 0.0
        placeholders = ",".join("?" for _ in inv_ids)
        rows = cursor.execute(f'''
            SELECT stock, cp
            FROM inventory
            WHERE id IN ({placeholders})
        ''', list(inv_ids)).fetchall()
        return sum(row['stock'] * row['cp'] for row in rows)

    # 1. Verification of Dry Items
    rows_dry = cursor.execute("SELECT id FROM inventory WHERE cat='Dry'").fetchall()
    dry_ids = [row['id'] for row in rows_dry]
    print(f"Dry Items count: {len(rows_dry)} (Expected: 73)")
    if len(rows_dry) != 73:
        errors.append(f"Dry items count mismatch: {len(rows_dry)} vs 73")

    dry_issue_val = get_ledger_issue_val(dry_ids)
    dry_bcf_val = get_stock_val(dry_ids)

    print(f"Dry Items Issue Value: {dry_issue_val:.2f} (Expected: 3956.03)")
    print(f"Dry Items BCF Value: {dry_bcf_val:.2f} (Expected: 234594.07)")

    if abs(dry_issue_val - 3956.03) > 2.00:
        errors.append(f"Dry items issue value mismatch: {dry_issue_val:.2f} vs 3956.03")
    if abs(dry_bcf_val - 234594.07) > 2.00:
        errors.append(f"Dry items BCF value mismatch: {dry_bcf_val:.2f} vs 234594.07")

    # 2. Verification of Packaging Items (Misc cat, excluding Burfi/Petha)
    rows_pkg = cursor.execute("SELECT id FROM inventory WHERE cat='Misc' AND item NOT LIKE 'SWEET%' AND item != 'PETHA'").fetchall()
    pkg_ids = [row['id'] for row in rows_pkg]
    print(f"Packaging Items count: {len(rows_pkg)} (Expected: 16)")
    if len(rows_pkg) != 16:
        errors.append(f"Packaging items count mismatch: {len(rows_pkg)} vs 16")

    pkg_issue_val = get_ledger_issue_val(pkg_ids)
    pkg_bcf_val = get_stock_val(pkg_ids)

    print(f"Packaging Items Issue Value: {pkg_issue_val:.2f} (Expected: 2379.06)")
    print(f"Packaging Items BCF Value: {pkg_bcf_val:.2f} (Expected: 65642.72)")

    if abs(pkg_issue_val - 2379.06) > 2.00:
        errors.append(f"Packaging items issue value mismatch: {pkg_issue_val:.2f} vs 2379.06")
    if abs(pkg_bcf_val - 65642.72) > 2.00:
        errors.append(f"Packaging items BCF value mismatch: {pkg_bcf_val:.2f} vs 65642.72")

    # 3. Verification of Sweets
    rows_sw = cursor.execute("SELECT id FROM inventory WHERE cat='Misc' AND (item LIKE 'SWEET%' OR item = 'PETHA')").fetchall()
    sw_ids = [row['id'] for row in rows_sw]
    print(f"Sweets count: {len(rows_sw)} (Expected: 2)")
    if len(rows_sw) != 2:
        errors.append(f"Sweets count mismatch: {len(rows_sw)} vs 2")

    sw_issue_val = get_ledger_issue_val(sw_ids)
    sw_bcf_val = get_stock_val(sw_ids)

    print(f"Sweets Issue Value: {sw_issue_val:.2f} (Expected: 700.00)")
    print(f"Sweets BCF Value: {sw_bcf_val:.2f} (Expected: 3860.00)")

    if abs(sw_issue_val - 700.00) > 0.05:
        errors.append(f"Sweets issue value mismatch: {sw_issue_val:.2f} vs 700.00")
    if abs(sw_bcf_val - 3860.00) > 0.05:
        errors.append(f"Sweets BCF value mismatch: {sw_bcf_val:.2f} vs 3860.00")

    # 4. Verification of Fresh Items
    rows_fresh = cursor.execute("SELECT id FROM inventory WHERE cat='Fresh'").fetchall()
    fresh_ids = [row['id'] for row in rows_fresh]
    print(f"Fresh Items count: {len(rows_fresh)} (Expected: 21)")
    if len(rows_fresh) != 21:
        errors.append(f"Fresh items count mismatch: {len(rows_fresh)} vs 21")

    fresh_issue_val = get_ledger_issue_val(fresh_ids)
    fresh_bcf_val = get_stock_val(fresh_ids)

    print(f"Fresh Items Issue Value: {fresh_issue_val:.2f} (Expected: 1153.03)")
    print(f"Fresh Items BCF Value: {fresh_bcf_val:.2f} (Expected: 9873.00)")

    if abs(fresh_issue_val - 1153.03) > 0.05:
        errors.append(f"Fresh items issue value mismatch: {fresh_issue_val:.2f} vs 1153.03")
    if abs(fresh_bcf_val - 9873.00) > 0.05:
        errors.append(f"Fresh items BCF value mismatch: {fresh_bcf_val:.2f} vs 9873.00")

    # 5. Verification of Sales & Menu
    rows_sales = cursor.execute("SELECT s.*, m.cogs as m_cogs FROM sales s JOIN menu m ON m.id = s.menu_id WHERE s.date = ?", (DATE,)).fetchall()
    total_rev = sum(row['sold'] * row['sp'] for row in rows_sales)
    total_cogs = sum(row['cogs'] for row in rows_sales)
    total_profit = total_rev - total_cogs
    total_prep = cursor.execute("SELECT SUM(qty_prepared) FROM batch_prep WHERE date = ?", (DATE,)).fetchone()[0] or 0
    total_sold = sum(row['sold'] for row in rows_sales)

    print(f"Total Sales Revenue: {total_rev:.2f} (Expected: 10700.00)")
    print(f"Total Sales COGS: {total_cogs:.2f} (Expected: 8188.00)")
    print(f"Total Sales Profit: {total_profit:.2f} (Expected: 2512.00)")
    print(f"Total Packets Prepared: {total_prep} (Expected: 159)")
    print(f"Total Packets Sold: {total_sold} (Expected: 158)")

    if abs(total_rev - 10700.00) > 0.01:
        errors.append(f"Sales revenue mismatch: {total_rev:.2f} vs 10700.00")
    if abs(total_cogs - 8188.00) > 0.01:
        errors.append(f"Sales COGS mismatch: {total_cogs:.2f} vs 8188.00")
    if abs(total_profit - 2512.00) > 0.01:
        errors.append(f"Sales profit mismatch: {total_profit:.2f} vs 2512.00")

    # 6. Check stock ledger balance check
    print("Checking stock ledger consistency...")
    ledger_errors = 0
    items = cursor.execute("SELECT * FROM inventory").fetchall()
    for item in items:
        # Sum of qty_change in ledger
        ledger_sum = cursor.execute("SELECT SUM(qty_change) FROM stock_ledger WHERE inv_id=?", (item['id'],)).fetchone()[0] or 0.0
        if abs(ledger_sum - item['stock']) > 0.001:
            ledger_errors += 1
            print(f"  Mismatch in ledger sum for '{item['item']}': Ledger={ledger_sum:.3f}, Stock={item['stock']:.3f}")

    if ledger_errors > 0:
        errors.append(f"Found {ledger_errors} items with inconsistent stock ledger balances.")

    conn.close()

    print("\n=== VERIFICATION SUMMARY FOR 02 MAY 2026 ===")
    if errors:
        print("❌ FAILED with the following errors:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("✅ ALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_verifications()
