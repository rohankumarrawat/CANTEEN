import sqlite3

DATE = "2026-05-13"

def run_verifications():
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    errors = []

    print("=== STARTING DATABASE INTEGRITY VERIFICATION FOR 13 MAY 2026 ===")

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
    print(f"Dry Items count in DB: {len(rows_dry)} (Expected: 75)")

    dry_issue_val = get_ledger_issue_val(dry_ids)
    dry_bcf_val = get_stock_val(dry_ids)

    # Note: the mathematically calculated sum of dry items rows is 12666.95 for issues and 143552.58 for BCF.
    # The sheet's written totals are 13810.17 and 141992.16 (manual addition errors).
    print(f"Dry Items Calculated Issue Value: {dry_issue_val:.2f} (Expected: 12666.95)")
    print(f"Dry Items Calculated BCF Value: {dry_bcf_val:.2f} (Expected: 143552.58)")

    if abs(dry_issue_val - 12666.95) > 1.00:
        errors.append(f"Dry items issue value mismatch: {dry_issue_val:.2f} vs 12666.95")
    if abs(dry_bcf_val - 143552.58) > 1.00:
        errors.append(f"Dry items BCF value mismatch: {dry_bcf_val:.2f} vs 143552.58")

    # 2. Verification of Packaging Items (Misc cat, excluding Burfi/Petha/Guldana)
    rows_pkg = cursor.execute("SELECT id FROM inventory WHERE cat='Misc' AND item NOT IN ('Sweet (Burfi)', 'Petha', 'Guldana')").fetchall()
    pkg_ids = [row['id'] for row in rows_pkg]
    print(f"Packaging Items count: {len(rows_pkg)}")

    pkg_issue_val = get_ledger_issue_val(pkg_ids)
    pkg_bcf_val = get_stock_val(pkg_ids)

    print(f"Packaging Items Issue Value: {pkg_issue_val:.2f} (Expected: 8050.92)")
    print(f"Packaging Items BCF Value: {pkg_bcf_val:.2f} (Expected: 54520.67)")

    if abs(pkg_issue_val - 8050.92) > 1.00:
        errors.append(f"Packaging items issue value mismatch: {pkg_issue_val:.2f} vs 8050.92")
    if abs(pkg_bcf_val - 54520.67) > 1.00:
        errors.append(f"Packaging items BCF value mismatch: {pkg_bcf_val:.2f} vs 54520.67")

    # 3. Verification of Sweets
    rows_sw = cursor.execute("SELECT id FROM inventory WHERE cat='Misc' AND item IN ('Sweet (Burfi)', 'Petha', 'Guldana')").fetchall()
    sw_ids = [row['id'] for row in rows_sw]
    print(f"Sweets count: {len(rows_sw)} (Expected: 3)")

    sw_issue_val = get_ledger_issue_val(sw_ids)
    sw_bcf_val = get_stock_val(sw_ids)

    print(f"Sweets Issue Value: {sw_issue_val:.2f} (Expected: 3360.00)")
    print(f"Sweets BCF Value: {sw_bcf_val:.2f} (Expected: 2810.00)")

    if abs(sw_issue_val - 3360.00) > 0.05:
        errors.append(f"Sweets issue value mismatch: {sw_issue_val:.2f} vs 3360.00")
    if abs(sw_bcf_val - 2810.00) > 0.05:
        errors.append(f"Sweets BCF value mismatch: {sw_bcf_val:.2f} vs 2810.00")

    # 4. Verification of Fresh Items
    rows_fresh = cursor.execute("SELECT id FROM inventory WHERE cat='Fresh'").fetchall()
    fresh_ids = [row['id'] for row in rows_fresh]
    print(f"Fresh Items count: {len(rows_fresh)} (Expected: 21)")

    fresh_issue_val = get_ledger_issue_val(fresh_ids)
    fresh_bcf_val = get_stock_val(fresh_ids)

    print(f"Fresh Items Issue Value: {fresh_issue_val:.2f} (Expected: 2465.00)")
    print(f"Fresh Items BCF Value: {fresh_bcf_val:.2f} (Expected: 4867.84)")

    if abs(fresh_issue_val - 2465.00) > 0.05:
        errors.append(f"Fresh items issue value mismatch: {fresh_issue_val:.2f} vs 2465.00")
    if abs(fresh_bcf_val - 4867.84) > 0.05:
        errors.append(f"Fresh items BCF value mismatch: {fresh_bcf_val:.2f} vs 4867.84")

    # 5. Verification of Sales & Menu
    rows_sales = cursor.execute("SELECT s.*, m.cogs as m_cogs FROM sales s JOIN menu m ON m.id = s.menu_id WHERE s.date = ?", (DATE,)).fetchall()
    total_rev = sum(row['sold'] * row['sp'] for row in rows_sales)
    total_cogs = sum(row['cogs'] for row in rows_sales)
    total_profit = total_rev - total_cogs
    total_prep = cursor.execute("SELECT SUM(qty_prepared) FROM batch_prep WHERE date = ?", (DATE,)).fetchone()[0] or 0
    total_sold = sum(row['sold'] for row in rows_sales)

    print(f"Total Sales Revenue: {total_rev:.2f} (Expected: 41130.00)")
    print(f"Total Sales COGS/EXPDR: {total_cogs:.2f} (Expected: 31933.00)")
    print(f"Total Sales Profit: {total_profit:.2f} (Expected: 9197.00)")
    print(f"Total Packets Prepared: {total_prep} (Expected: 981)")
    print(f"Total Packets Sold: {total_sold} (Expected: 973)")

    if abs(total_rev - 41130.00) > 0.01:
        errors.append(f"Sales revenue mismatch: {total_rev:.2f} vs 41130.00")
    if abs(total_cogs - 31933.00) > 0.01:
        errors.append(f"Sales COGS/EXPDR mismatch: {total_cogs:.2f} vs 31933.00")
    if abs(total_profit - 9197.00) > 0.01:
        errors.append(f"Sales profit mismatch: {total_profit:.2f} vs 9197.00")

    # 6. Check stock ledger consistency
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

    print("\n=== VERIFICATION SUMMARY FOR 13 MAY 2026 ===")
    if errors:
        print("❌ FAILED with the following errors:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("✅ ALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_verifications()
