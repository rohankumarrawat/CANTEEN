import sqlite3
import os

DB_PATH = 'canteen.db'

def run():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    for d in ['2026-06-03', '2026-05-27', '2026-05-20', '2026-05-13', '2026-05-06']:
        rows = conn.execute('''
            SELECT sl.qty_change, i.item, i.cp, (-sl.qty_change * i.cp) as val
            FROM stock_ledger sl
            JOIN inventory i ON i.id = sl.inv_id
            WHERE sl.date = ? AND sl.transaction_type = 'Batch_Prep' AND sl.inv_id IN (
                SELECT id FROM inventory WHERE item IN (
                    'Kadhai Paneer Masala', 'Chaat Masala', 'Rajmah Masala', 'Rajmah Masala(Expensive)',
                    'Gulab Jal', 'Chana Masala', 'Chana Masala(Expensive)', 'Kala Chana', 'Kala Chana(Expensive)',
                    'Rice(Idlee)', 'Red Chilli Sauce', 'Green Chilli Sause', 'Tomato Sauce', 'Matar Paneer Masala',
                    'Pav Bhaji Masala', 'Matar (Frozen)', 'Food Colour', 'Food Colour(Expensive)', 'Kevada Water',
                    'Biryani Masala', 'Elaichi Small Gr'
                )
            )
        ''', (d,)).fetchall()
        print(f'=== {d} ===')
        for r in rows:
            print(dict(r))
    conn.close()

if __name__ == '__main__':
    run()
