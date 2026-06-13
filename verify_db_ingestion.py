import sqlite3

def run_verifications():
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    DATE = "2026-04-30"
    errors = []

    print("=== STARTING DATABASE INTEGRITY VERIFICATION FOR 30 APR 2026 ===")

    # Map of 30 April rates to override the current inventory.cp values for historical calculations
    rates_30_apr = {
        "POTATO": 12.0, "ONION": 22.0, "TOMATO": 30.0, "GINGER": 65.0, "GARLIC": 132.0,
        "PEAS GREEN": 95.0, "GREEN CHILLI": 55.0, "CORRENDER": 40.0, "CAPSICUM": 18.0,
        "BEANS": 55.0, "CARROT": 33.0, "CAULI FLOWER": 55.0, "GREEN ONION": 37.0,
        "BOTTLE GD": 15.0, "CABBAGE": 44.0, "CUCUMBER": 15.0, "MATAR": 100.0,
        "PANEER": 250.0, "LIME S": 198.0, "DAHI": 75.0, "PAV/KULCHA": 35.0
    }

    # Helper function to get ledger issues sum for a set of item IDs
    def get_ledger_issue_val(inv_ids):
        if not inv_ids:
            return 0.0
        placeholders = ",".join("?" for _ in inv_ids)
        rows = cursor.execute(f'''
            SELECT sl.qty_change, i.item, i.cp
            FROM stock_ledger sl
            JOIN inventory i ON i.id = sl.inv_id
            WHERE sl.date = ? AND sl.transaction_type = 'Batch_Prep' AND sl.inv_id IN ({placeholders})
        ''', [DATE] + list(inv_ids)).fetchall()
        return sum(-row['qty_change'] * rates_30_apr.get(row['item'].upper(), row['cp']) for row in rows)

    # Helper function to get stock value at 30 April for a set of item IDs (sum of ledger changes up to that date)
    def get_historical_stock_val(inv_ids):
        if not inv_ids:
            return 0.0
        placeholders = ",".join("?" for _ in inv_ids)
        rows = cursor.execute(f'''
            SELECT i.item, i.cp, SUM(sl.qty_change) as hist_stock
            FROM stock_ledger sl
            JOIN inventory i ON i.id = sl.inv_id
            WHERE sl.date <= ? AND sl.inv_id IN ({placeholders})
            GROUP BY i.id
        ''', [DATE] + list(inv_ids)).fetchall()
        return sum(row['hist_stock'] * rates_30_apr.get(row['item'].upper(), row['cp']) for row in rows)

    # 1. Verification of Dry Items
    rows_dry = cursor.execute("SELECT id FROM inventory WHERE cat='Dry'").fetchall()
    dry_ids = [row['id'] for row in rows_dry]
    print(f"Dry Items count: {len(rows_dry)} (Expected: 73)")
    if len(rows_dry) != 73:
        errors.append(f"Dry items count mismatch: {len(rows_dry)} vs 73")

    dry_issue_val = get_ledger_issue_val(dry_ids)
    dry_bcf_val = get_historical_stock_val(dry_ids)

    print(f"Dry Items Issue Value: {dry_issue_val:.2f} (Expected: 12279.82)")
    print(f"Dry Items BCF Value: {dry_bcf_val:.2f} (Expected: 238550.10)")

    if abs(dry_issue_val - 12279.82) > 2.00:
        errors.append(f"Dry items issue value mismatch: {dry_issue_val:.2f} vs 12279.82")
    if abs(dry_bcf_val - 238550.10) > 2.00:
        errors.append(f"Dry items BCF value mismatch: {dry_bcf_val:.2f} vs 238550.10")

    # 2. Verification of Packaging Items (stored under category 'Misc' in inventory)
    rows_pkg = cursor.execute("SELECT id FROM inventory WHERE cat='Misc' AND item NOT LIKE 'SWEET%' AND item != 'PETHA'").fetchall()
    pkg_ids = [row['id'] for row in rows_pkg]
    print(f"Packaging Items count: {len(rows_pkg)} (Expected: 16)")
    if len(rows_pkg) != 16:
        errors.append(f"Packaging items count mismatch: {len(rows_pkg)} vs 16")

    pkg_issue_val = get_ledger_issue_val(pkg_ids)
    pkg_bcf_val = get_historical_stock_val(pkg_ids)

    print(f"Packaging Items Issue Value: {pkg_issue_val:.2f} (Expected: 8623.94)")
    print(f"Packaging Items BCF Value: {pkg_bcf_val:.2f} (Expected: 68021.78)")

    if abs(pkg_issue_val - 8623.94) > 2.00:
        errors.append(f"Packaging items issue value mismatch: {pkg_issue_val:.2f} vs 8623.94")
    if abs(pkg_bcf_val - 68021.78) > 2.00:
        errors.append(f"Packaging items BCF value mismatch: {pkg_bcf_val:.2f} vs 68021.78")

    # 3. Verification of Sweets (also under cat='Misc' but name filtered)
    rows_sw = cursor.execute("SELECT id FROM inventory WHERE cat='Misc' AND (item LIKE 'SWEET%' OR item = 'PETHA')").fetchall()
    sw_ids = [row['id'] for row in rows_sw]
    print(f"Sweets count: {len(rows_sw)} (Expected: 2)")
    if len(rows_sw) != 2:
        errors.append(f"Sweets count mismatch: {len(rows_sw)} vs 2")

    sw_issue_val = get_ledger_issue_val(sw_ids)
    sw_bcf_val = get_historical_stock_val(sw_ids)

    print(f"Sweets Issue Value: {sw_issue_val:.2f} (Expected: 1800.00)")
    print(f"Sweets BCF Value: {sw_bcf_val:.2f} (Expected: 4560.00)")

    if abs(sw_issue_val - 1800.00) > 0.05:
        errors.append(f"Sweets issue value mismatch: {sw_issue_val:.2f} vs 1800.00")
    if abs(sw_bcf_val - 4560.00) > 0.05:
        errors.append(f"Sweets BCF value mismatch: {sw_bcf_val:.2f} vs 4560.00")

    # 4. Verification of Fresh Items (cat='Fresh')
    rows_fresh = cursor.execute("SELECT id FROM inventory WHERE cat='Fresh'").fetchall()
    fresh_ids = [row['id'] for row in rows_fresh]
    print(f"Fresh Items count: {len(rows_fresh)} (Expected: 21)")
    if len(rows_fresh) != 21:
        errors.append(f"Fresh items count mismatch: {len(rows_fresh)} vs 21")

    fresh_issue_val = get_ledger_issue_val(fresh_ids)
    fresh_bcf_val = get_historical_stock_val(fresh_ids)

    print(f"Fresh Items Issue Value: {fresh_issue_val:.2f} (Expected: 5738.20)")
    print(f"Fresh Items BCF Value: {fresh_bcf_val:.2f} (Expected: 2262.01)")

    if abs(fresh_issue_val - 5738.20) > 0.05:
        errors.append(f"Fresh items issue value mismatch: {fresh_issue_val:.2f} vs 5738.20")
    if abs(fresh_bcf_val - 2262.01) > 0.05:
        errors.append(f"Fresh items BCF value mismatch: {fresh_bcf_val:.2f} vs 2262.01")

    # 5. Verification of Sales & Menu
    rows_sales = cursor.execute("SELECT s.*, m.cogs as m_cogs FROM sales s JOIN menu m ON m.id = s.menu_id WHERE s.date = ?", (DATE,)).fetchall()
    total_rev = sum(row['sold'] * row['sp'] for row in rows_sales)
    total_cogs = sum(row['cogs'] for row in rows_sales)
    total_profit = total_rev - total_cogs
    total_prep = cursor.execute("SELECT SUM(qty_prepared) FROM batch_prep WHERE date = ?", (DATE,)).fetchone()[0] or 0
    total_sold = sum(row['sold'] for row in rows_sales)

    print(f"Total Sales Revenue: {total_rev:.2f} (Expected: 47255.00)")
    print(f"Total Sales COGS: {total_cogs:.2f} (Expected: 32935.00)")
    print(f"Total Sales Profit: {total_profit:.2f} (Expected: 14320.00)")
    print(f"Total Packets Prepared: {total_prep} (Expected: 1133)")
    print(f"Total Packets Sold: {total_sold} (Expected: 1124)")

    if abs(total_rev - 47255.00) > 0.01:
        errors.append(f"Sales revenue mismatch: {total_rev:.2f} vs 47255.00")
    if abs(total_cogs - 32935.00) > 0.01:
        errors.append(f"Sales COGS mismatch: {total_cogs:.2f} vs 32935.00")
    if abs(total_profit - 14320.00) > 0.01:
        errors.append(f"Sales profit mismatch: {total_profit:.2f} vs 14320.00")

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

    print("\n=== VERIFICATION SUMMARY FOR 30 APR 2026 ===")
    if errors:
        print("❌ FAILED with the following errors:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("✅ ALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_verifications()
