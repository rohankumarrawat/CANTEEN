"""
Delete all data from 2026-06-05 to 2026-06-08 (inclusive)
and restore inventory stock levels by reversing the stock_ledger deductions.
"""
import sqlite3, shutil, os, datetime

DB = os.path.join(os.path.dirname(__file__), '..', 'canteen.db')
DB = os.path.abspath(DB)

# 1. Backup first
backup = DB + f".bak_before_delete_jun5_8_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(DB, backup)
print(f"✅ Backup saved: {backup}")

START = '2026-06-05'
END   = '2026-06-08'

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

try:
    # 2. Restore inventory stock — add back the qty that was deducted (qty_change < 0)
    #    and remove the qty that was added as 'Received' or 'Opening' (qty_change > 0)
    ledger_rows = conn.execute(
        "SELECT inv_id, qty_change FROM stock_ledger WHERE date >= ? AND date <= ?",
        (START, END)
    ).fetchall()

    restore_map = {}  # inv_id -> net qty to add back
    for r in ledger_rows:
        restore_map[r["inv_id"]] = restore_map.get(r["inv_id"], 0.0) - r["qty_change"]

    for inv_id, restore_qty in restore_map.items():
        conn.execute(
            "UPDATE inventory SET stock = ROUND(stock + ?, 4) WHERE id = ?",
            (restore_qty, inv_id)
        )
        print(f"  📦 inv_id={inv_id}: stock adjusted by +{restore_qty:.4f}")

    # 3. Delete from all tables
    tables = [
        'sales',
        'batch_prep',
        'expenditure',
        'samples',
        'stock_ledger',
        'waste_tracker',
        'goods_received',
    ]
    for t in tables:
        try:
            cur = conn.execute(
                f"DELETE FROM {t} WHERE date >= ? AND date <= ?", (START, END)
            )
            print(f"  🗑  {t}: {cur.rowcount} rows deleted")
        except Exception as e:
            print(f"  ⚠️  {t}: {e}")

    conn.commit()
    print("\n✅ Done — all Jun 5–8 data deleted and stock restored.")

except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e} — rolled back, no changes made.")
    raise

finally:
    conn.close()
