import sqlite3
import os

DB_PATH = "/Users/rohan/Desktop/canteen/canteen.db"

def test_menu_rename():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # 1. Clean up or setup test menu items
    conn.execute("DELETE FROM menu WHERE name IN ('TEST_MENU_OLD', 'TEST_MENU_NEW', 'TEST_MENU_DUP')")
    conn.execute("DELETE FROM waste_tracker WHERE reason IN ('Production waste - TEST_MENU_OLD', 'Production waste - TEST_MENU_NEW', 'Batch update - TEST_MENU_OLD', 'Batch update - TEST_MENU_NEW')")
    
    # Insert test data
    conn.execute("INSERT INTO menu (name, sp, active) VALUES ('TEST_MENU_OLD', 50.0, 1)")
    mid_old = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    
    conn.execute("INSERT INTO menu (name, sp, active) VALUES ('TEST_MENU_DUP', 60.0, 1)")
    mid_dup = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    
    # Insert waste_tracker entries for TEST_MENU_OLD
    conn.execute("INSERT INTO waste_tracker (date, item, qty_wasted, reason, cost_lost, recorded_by) VALUES (?, ?, ?, ?, ?, ?)",
                 ("2026-06-17", "Salt", 1.0, "Production waste - TEST_MENU_OLD", 10.0, "Test"))
    conn.execute("INSERT INTO waste_tracker (date, item, qty_wasted, reason, cost_lost, recorded_by) VALUES (?, ?, ?, ?, ?, ?)",
                 ("2026-06-17", "Sugar", 0.5, "Batch update - TEST_MENU_OLD", 15.0, "Test"))
    
    conn.commit()
    print("Setup test menu items and waste tracker entries successfully.")
    
    # 2. Test duplicate check (case-insensitive)
    new_name_dup = "test_menu_dup"
    dup = conn.execute("SELECT id FROM menu WHERE LOWER(name) = LOWER(?) AND id != ?", (new_name_dup, mid_old)).fetchone()
    if dup:
        print(f"✅ Duplicate check passed: successfully blocked renaming to existing menu '{new_name_dup}' (mid={dup['id']})")
    else:
        print("❌ Duplicate check failed: duplicate not detected")
        assert False
        
    # 3. Perform actual rename
    new_name = "TEST_MENU_NEW"
    
    # Update menu name
    conn.execute("UPDATE menu SET name=? WHERE id=?", (new_name, mid_old))
    
    # Migrate historical waste tracker references
    conn.execute(
        "UPDATE waste_tracker SET reason = ? WHERE reason = ?",
        (f"Production waste - {new_name}", f"Production waste - TEST_MENU_OLD")
    )
    conn.execute(
        "UPDATE waste_tracker SET reason = ? WHERE reason = ?",
        (f"Batch update - {new_name}", f"Batch update - TEST_MENU_OLD")
    )
    
    conn.commit()
    
    # Verify updates
    updated_menu = conn.execute("SELECT name FROM menu WHERE id=?", (mid_old,)).fetchone()
    print(f"Updated menu name: {updated_menu['name']}")
    assert updated_menu['name'] == "TEST_MENU_NEW"
    
    # Verify waste tracker reason migration
    wastes = conn.execute("SELECT reason FROM waste_tracker WHERE reason LIKE '%TEST_MENU_NEW%'").fetchall()
    reasons = [w["reason"] for w in wastes]
    print(f"Migrated waste tracker reasons: {reasons}")
    assert len(reasons) == 2
    assert "Production waste - TEST_MENU_NEW" in reasons
    assert "Batch update - TEST_MENU_NEW" in reasons
    
    # Clean up
    conn.execute("DELETE FROM menu WHERE name IN ('TEST_MENU_OLD', 'TEST_MENU_NEW', 'TEST_MENU_DUP')")
    conn.execute("DELETE FROM waste_tracker WHERE reason IN ('Production waste - TEST_MENU_OLD', 'Production waste - TEST_MENU_NEW', 'Batch update - TEST_MENU_OLD', 'Batch update - TEST_MENU_NEW')")
    conn.commit()
    conn.close()
    print("✅ All DB logic assertions passed!")

if __name__ == "__main__":
    test_menu_rename()
