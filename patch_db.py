import sqlite3

def patch_database():
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()

    try:
        # 1. ROTI POUCH (inv_id = 76)
        # Update opening balance and early issues from thousands to units
        cursor.execute("UPDATE stock_ledger SET qty_change = 12600.0 WHERE inv_id = 76 AND qty_change = 12.6")
        cursor.execute("UPDATE stock_ledger SET qty_change = -3500.0 WHERE inv_id = 76 AND qty_change = -3.5")
        cursor.execute("UPDATE stock_ledger SET qty_change = -800.0 WHERE inv_id = 76 AND qty_change = -0.8")

        # 2. BUTTER ROTI PAPER (inv_id = 85)
        # Update opening balance, received, and issues from thousands to units
        cursor.execute("UPDATE stock_ledger SET qty_change = 450.0 WHERE inv_id = 85 AND qty_change = 0.45")
        cursor.execute("UPDATE stock_ledger SET qty_change = -50.0 WHERE inv_id = 85 AND qty_change = -0.05")
        cursor.execute("UPDATE stock_ledger SET qty_change = -100.0 WHERE inv_id = 85 AND qty_change = -0.1")
        cursor.execute("UPDATE stock_ledger SET qty_change = 1000.0 WHERE inv_id = 85 AND qty_change = 1.0")
        cursor.execute("UPDATE stock_ledger SET qty_change = -150.0 WHERE inv_id = 85 AND qty_change = -0.15")

        # Update the inventory table for BUTTER ROTI PAPER to have stock in units (1700) and correct CP (0.236)
        cursor.execute("UPDATE inventory SET stock = 1700.0, cp = 0.236 WHERE id = 85")

        # Insert BUTTER ROTI PAPER reconciliation entry if not already present
        cursor.execute("SELECT id FROM stock_ledger WHERE inv_id = 85 AND notes LIKE '%reconciliation%'")
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                VALUES ('2026-05-11', 85, 'Batch_Prep', -150.0, 'Manual register math reconciliation (BUTTER ROTI PAPER BCF error)')
            ''')

        # 3. ELAICHI SMALL GR (inv_id = 54)
        # Check if correction ledger entry already exists
        cursor.execute("SELECT id FROM stock_ledger WHERE inv_id = 54 AND notes LIKE '%correction%'")
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes)
                VALUES ('2026-05-12', 54, 'Received', 0.010, 'Manual register math correction (ilaychi BCF error)')
            ''')

        # 4. Merge Duplicate Masalas
        # A. CHAT MASALA (id: 40 is duplicate of id: 114)
        # Redirect all ledger entries and goods received from 114 to 40
        cursor.execute("UPDATE stock_ledger SET inv_id = 40 WHERE inv_id = 114")
        cursor.execute("UPDATE goods_received SET inv_id = 40 WHERE inv_id = 114")
        
        # B. RAJMAH MASALA (id: 41 is duplicate of id: 115)
        # Redirect all ledger entries and goods received from 115 to 41
        cursor.execute("UPDATE stock_ledger SET inv_id = 41 WHERE inv_id = 115")
        cursor.execute("UPDATE goods_received SET inv_id = 41 WHERE inv_id = 115")
        
        # DELETE duplicate items first so we can rename id 40 and 41 without uniqueness violations
        cursor.execute("DELETE FROM inventory WHERE id IN (114, 115)")

        # Rename id 40 and 41 and set correct stock & CP
        cursor.execute("UPDATE inventory SET item = 'Chat Masala', stock = 0.9, cp = 752.0, updated = '2026-05-13' WHERE id = 40")
        cursor.execute("UPDATE inventory SET item = 'Rajma Masala (Kgs)', stock = 2.0, cp = 736.0, updated = '2026-05-13' WHERE id = 41")

        # Delete duplicate 'Opening' entries created on May 4 for id 40 and 41
        cursor.execute("DELETE FROM stock_ledger WHERE date = '2026-05-04' AND transaction_type = 'Opening' AND inv_id IN (40, 41)")

        conn.commit()
        print("🎉 Database patched, duplicate masalas merged and opening balances corrected successfully!")
    except Exception as e:
        print(f"Error patching database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    patch_database()
