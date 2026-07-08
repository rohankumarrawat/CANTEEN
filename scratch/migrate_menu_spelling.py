import sqlite3
import re
import datetime as _dt

def migrate():
    db_path = 'canteen.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Load initial mapping from daily_menu to determine meal types
    sched_name_map = {}
    for row in conn.execute("SELECT dm.day, dm.meal_type, m.name FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
        sched_name_map[(row["day"], row["meal_type"])] = row["name"]
    
    item_type_map = {}
    for row in conn.execute("SELECT DISTINCT m.name, dm.meal_type FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
        item_type_map[row["name"].lower().strip()] = row["meal_type"]

    # Spelling / Capitalization Corrections for menu items
    rename_map = {
        "tamarind rice": "Tamarind Rice",
        "rajma rice": "Rajma Rice",
        "veg biryani": "Veg Biryani",
        "mixed veg parantha": "Mixed Veg Paratha",
        "mix veg parantha": "Mixed Veg Paratha",
        "mix veg paratha": "Mixed Veg Paratha",
        "fried aloo parantha": "Fried Aloo Paratha",
        "dal chana parantha": "Dal Chana Paratha",
        "tori/ kaddu, dal masur, chapati, rice & salad badana": "Tori, Kaddu, Dal Masoor, Chapati, Rice, Salad, Badana",
        "tori/kaddu, dal masoor, chapati, rice, salad, badana": "Tori, Kaddu, Dal Masoor, Chapati, Rice, Salad, Badana",
        "tori, kaddu, dal chana, chapati, rice": "Tori, Kaddu, Dal Masoor, Chapati, Rice, Salad, Badana"
    }

    def standardize_db_meal_name(meal_str, date_str):
        m_str = meal_str.strip()
        
        # 1. Parse existing prefix in parentheses
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
                
            # Clean the content name
            cleaned_content = rename_map.get(content.lower(), content)
            if "," in cleaned_content:
                items = [item.strip() for item in cleaned_content.split(",")]
                items_clean = []
                for item in items:
                    items_clean.append(rename_map.get(item.lower(), item).title() if len(item) > 2 else item)
                display_content = ", ".join(items_clean)
            else:
                display_content = rename_map.get(cleaned_content.lower(), cleaned_content).title()
                
            return f"{prefix}({display_content})"
            
        # 2. Check if the string matches a category name directly (like "LUNCH")
        MEAL_TYPE_MAP = {
            "LUNCH": "Lunch",
            "MINI": "Mini Meal",
            "MINI MEAL": "Mini Meal",
            "PARATHA": "Paratha"
        }
        mtype = MEAL_TYPE_MAP.get(m_str.upper())
        if mtype:
            try:
                d = _dt.date.fromisoformat(date_str)
                dow = d.strftime("%A")
                specific = sched_name_map.get((dow, mtype))
                if specific:
                    cleaned_specific = rename_map.get(specific.lower(), specific)
                    return f"{mtype}({cleaned_specific})"
            except Exception:
                pass
            return mtype
            
        # 3. Clean the name directly
        cleaned_m_str = rename_map.get(m_str.lower(), m_str)
        if "," in cleaned_m_str:
            items = [item.strip() for item in cleaned_m_str.split(",")]
            items_clean = []
            for item in items:
                items_clean.append(rename_map.get(item.lower(), item).title() if len(item) > 2 else item)
            m_str = ", ".join(items_clean)
        else:
            m_str = rename_map.get(cleaned_m_str.lower(), cleaned_m_str).title()
            
        # Determine category
        clean_str = m_str.lower()
        mtype = item_type_map.get(clean_str)
        if not mtype:
            if clean_str in ["amul kool", "brownie", "chach", "dahi", "lahori zeera", "lassi", "plum cake"]:
                mtype = None
            elif "paratha" in clean_str or "parantha" in clean_str:
                mtype = "Paratha"
            elif "," in clean_str or "thali" in clean_str:
                mtype = "Lunch"
            elif clean_str in ["pav bhaji", "rajma rice", "rajmah rice", "veg biryani", "veg biriyani", "kadhi chawal", "matar kulcha", "tamarind rice"]:
                mtype = "Mini Meal"
                
        if mtype:
            return f"{mtype}({m_str})"
            
        return m_str

    try:
        # Step A. Standardize existing menu item names and merge duplicate entries
        print("Standardizing menu table...")
        menu_items = cursor.execute("SELECT id, name FROM menu").fetchall()
        
        name_to_id = {}
        for row in menu_items:
            mid = row["id"]
            old_name = row["name"]
            
            # Compute standardized name
            new_name = rename_map.get(old_name.lower(), old_name)
            if "," not in new_name:
                new_name = new_name.title()
            else:
                items = [item.strip() for item in new_name.split(",")]
                items_clean = []
                for item in items:
                    items_clean.append(rename_map.get(item.lower(), item).title() if len(item) > 2 else item)
                new_name = ", ".join(items_clean)
                
            clean_new_name = new_name.lower().strip()
            
            # Check if this standardized name already exists (or will exist) under another ID
            if clean_new_name in name_to_id:
                primary_id = name_to_id[clean_new_name]
                print(f"  Conflict/Duplicate found: ID {mid} ('{old_name}') standardizes to '{new_name}', which matches ID {primary_id}. Merging directly...")
                
                # Update references in all other tables
                cursor.execute("UPDATE daily_menu SET menu_id = ? WHERE menu_id = ?", (primary_id, mid))
                cursor.execute("UPDATE sales SET menu_id = ? WHERE menu_id = ?", (primary_id, mid))
                cursor.execute("UPDATE batch_prep SET menu_id = ? WHERE menu_id = ?", (primary_id, mid))
                cursor.execute("UPDATE samples SET menu_id = ? WHERE menu_id = ?", (primary_id, mid))
                cursor.execute("UPDATE recipes SET menu_id = ? WHERE menu_id = ?", (primary_id, mid))
                
                # Delete the duplicate from menu table
                cursor.execute("DELETE FROM menu WHERE id = ?", (mid,))
            else:
                # No conflict, update the name in menu table
                if old_name != new_name:
                    cursor.execute("UPDATE menu SET name = ? WHERE id = ?", (new_name, mid))
                    print(f"  Updated Menu ID {mid}: '{old_name}' -> '{new_name}'")
                name_to_id[clean_new_name] = mid

        # Re-fetch new sched_name_map and item_type_map after menu standardizations
        sched_name_map = {}
        for row in conn.execute("SELECT dm.day, dm.meal_type, m.name FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
            sched_name_map[(row["day"], row["meal_type"])] = row["name"]
        
        item_type_map = {}
        for row in conn.execute("SELECT DISTINCT m.name, dm.meal_type FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
            item_type_map[row["name"].lower().strip()] = row["meal_type"]

        # Step B. Standardize meal names in sales table
        print("\nStandardizing sales table meal column...")
        sales_rows = cursor.execute("SELECT id, date, meal FROM sales").fetchall()
        sales_updated_count = 0
        for row in sales_rows:
            old_meal = row["meal"]
            new_meal = standardize_db_meal_name(old_meal, row["date"])
            if old_meal != new_meal:
                cursor.execute("UPDATE sales SET meal = ? WHERE id = ?", (new_meal, row["id"]))
                sales_updated_count += 1
        print(f"  Updated {sales_updated_count} rows in sales table.")

        # Step C. Standardize meal names in samples table
        print("\nStandardizing samples table meal column...")
        samples_rows = cursor.execute("SELECT id, date, meal FROM samples").fetchall()
        samples_updated_count = 0
        for row in samples_rows:
            old_meal = row["meal"]
            new_meal = standardize_db_meal_name(old_meal, row["date"])
            if old_meal != new_meal:
                cursor.execute("UPDATE samples SET meal = ? WHERE id = ?", (new_meal, row["id"]))
                samples_updated_count += 1
        print(f"  Updated {samples_updated_count} rows in samples table.")

        # Step D. Standardize expenditure notes
        print("\nStandardizing expenditure table notes...")
        exp_rows = cursor.execute("SELECT id, notes FROM expenditure").fetchall()
        exp_updated_count = 0
        for row in exp_rows:
            old_notes = row["notes"] or ""
            new_notes = old_notes
            for old_name, new_name in rename_map.items():
                pattern = re.compile(re.escape(old_name), re.IGNORECASE)
                new_notes = pattern.sub(new_name, new_notes)
            if old_notes != new_notes:
                cursor.execute("UPDATE expenditure SET notes = ? WHERE id = ?", (new_notes, row["id"]))
                exp_updated_count += 1
        print(f"  Updated {exp_updated_count} rows in expenditure table.")

        conn.commit()
        print("\n🎉 Spelling and capitalization standardization complete!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
