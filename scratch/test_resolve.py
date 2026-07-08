import re
import datetime as _dt
import sqlite3

def test_resolve():
    # Setup mocks matching app.py implementation
    MEAL_TYPE_MAP = {
        "LUNCH": "Lunch",
        "MINI": "Mini Meal",
        "MINI MEAL": "Mini Meal",
        "PARATHA": "Paratha"
    }
    
    # Connect to canteen.db to load the actual mapping from daily_menu
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    
    sched_name_map = {}
    for row in conn.execute("SELECT dm.day, dm.meal_type, m.name FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
        sched_name_map[(row["day"], row["meal_type"])] = row["name"]
    
    item_type_map = {}
    for row in conn.execute("SELECT DISTINCT m.name, dm.meal_type FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
        item_type_map[row["name"].lower().strip()] = row["meal_type"]
        
    conn.close()

    def _resolve_meal_name(date_str, meal_str):
        m_str = meal_str.strip()
        
        # 1. Check if it already has a prefix in parentheses, e.g. "Mini meal(Pav bhaji)" or "Lunch(...)"
        prefix_match = re.match(r'^(lunch|mini\s*meal|paratha)\s*\((.*?)\)\s*$', m_str, re.IGNORECASE)
        if prefix_match:
            prefix = prefix_match.group(1).lower()
            content = prefix_match.group(2).strip()
            if prefix == "lunch":
                prefix = "Lunch"
            elif "mini" in prefix:
                prefix = "Mini Meal"
            else:
                prefix = "Paratha"
            display_content = content if "," in content else content.title()
            return f"{prefix}({display_content})"
            
        # 2. Check if the string matches a category name directly (like "LUNCH")
        try:
            d = _dt.date.fromisoformat(date_str)
            dow = d.strftime("%A")
            mtype = MEAL_TYPE_MAP.get(m_str.upper())
            if mtype:
                specific = sched_name_map.get((dow, mtype))
                if specific:
                    return f"{mtype}({specific})"
                return mtype
        except Exception:
            pass
            
        # 3. Check if it's one of the known daily menu items or classify based on content rules
        clean_str = m_str.lower()
        mtype = item_type_map.get(clean_str)
        if not mtype:
            # Name-based classification rules for historical items not in the template weekly schedule
            if clean_str in ["amul kool", "brownie", "chach", "dahi", "lahori zeera", "lassi", "plum cake"]:
                mtype = None
            elif "paratha" in clean_str or "parantha" in clean_str:
                mtype = "Paratha"
            elif "," in clean_str or "thali" in clean_str:
                mtype = "Lunch"
            elif clean_str in ["pav bhaji", "rajma rice", "rajmah rice", "veg biryani", "veg biriyani", "kadhi chawal", "matar kulcha", "tamarind rice"]:
                mtype = "Mini Meal"
        
        if mtype:
            display_content = m_str if "," in m_str else m_str.title()
            return f"{mtype}({display_content})"
            
        return m_str.title() if "," not in m_str else m_str

    # Run test cases
    test_cases = [
        ("2026-05-30", "Tori, Kaddu, Dal Masoor, Chapati, Rice, Salad, Badana", "Lunch(Tori, Kaddu, Dal Masoor, Chapati, Rice, Salad, Badana)"),
        ("2026-05-30", "Mini meal(Pav bhaji)", "Mini Meal(Pav Bhaji)"),
        ("2026-05-30", "Pav Bhaji", "Mini Meal(Pav Bhaji)"),
        ("2026-05-30", "Amul Kool", "Amul Kool"),
        ("2026-05-30", "Lunch", "Lunch(Tori, Kaddu, Dal Masoor, Chapati, Rice, Salad, Badana)"),
        ("2026-05-30", "mixed veg paratha", "Paratha(Mixed Veg Paratha)"),
        ("2026-05-30", "Lauki Dal Chana Sabji, Panchratna Dal, Rice, Roti, Salad, Dry Petha", "Lunch(Lauki Dal Chana Sabji, Panchratna Dal, Rice, Roti, Salad, Dry Petha)"),
    ]

    for date_str, meal_str, expected in test_cases:
        res = _resolve_meal_name(date_str, meal_str)
        assert res == expected, f"Failed for {meal_str!r}: got {res!r}, expected {expected!r}"
        print(f"SUCCESS: {meal_str!r} -> {res!r}")

if __name__ == '__main__':
    test_resolve()
