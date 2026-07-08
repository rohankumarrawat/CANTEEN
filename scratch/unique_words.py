import sqlite3
import re

def get_unique_words():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT item FROM inventory")
    items = [r[0] for r in cursor.fetchall()]
    conn.close()
    
    words = set()
    for item in items:
        # Remove parentheses, numbers, symbols, and split by space or slash
        cleaned = re.sub(r'[\(\)\{\}\d\-\.\,\&\/]', ' ', item)
        for w in cleaned.split():
            words.add(w.lower())
            
    print("Unique words in inventory item names:")
    for w in sorted(list(words)):
        print(f"  {w}")

if __name__ == '__main__':
    get_unique_words()
