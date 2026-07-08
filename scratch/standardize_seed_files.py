import glob
import os

def main():
    seed_files = glob.glob("seed_*.py")
    print(f"Found {len(seed_files)} seed files to standardize.")
    
    replacements = {
        'formatted_meal_name = f"{mtype}({specific_name})"': 'formatted_meal_name = f"{mtype} ({specific_name})"',
        'formatted_meal_name = f\'{mtype}({specific_name})\'': 'formatted_meal_name = f"{mtype} ({specific_name})"',
        '"Pav bhaji"': '"Pav Bhaji"',
        "'Pav bhaji'": "'Pav Bhaji'",
        '"Dal Chana parantha"': '"Dal Chana Parantha"',
        "'Dal Chana parantha'": "'Dal Chana Parantha'",
        '"Fried aloo parantha"': '"Fried Aloo Parantha"',
        "'Fried aloo parantha'": "'Fried Aloo Parantha'",
        '"Kadhi chawal"': '"Kadhi Chawal"',
        "'Kadhi chawal'": "'Kadhi Chawal'",
        '"Mix veg parantha"': '"Mix Veg Parantha"',
        "'Mix veg parantha'": "'Mix Veg Parantha'",
        '"Mixed veg parantha"': '"Mixed Veg Parantha"',
        "'Mixed veg parantha'": "'Mixed Veg Parantha'",
        '"Plum cake"': '"Plum Cake"',
        "'Plum cake'": "'Plum Cake'",
        '"Rajma rice"': '"Rajma Rice"',
        "'Rajma rice'": "'Rajma Rice'",
        '"Tamarind rice"': '"Tamarind Rice"',
        "'Tamarind rice'": "'Tamarind Rice'",
        '"Veg biryani"': '"Veg Biryani"',
        "'Veg biryani'": "'Veg Biryani'"
    }
    
    updated_files = 0
    for file_path in seed_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        modified = False
        new_content = content
        for old_str, new_str in replacements.items():
            if old_str in new_content:
                new_content = new_content.replace(old_str, new_str)
                modified = True
                
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  - Standardized: {file_path}")
            updated_files += 1
            
    print(f"Successfully standardized {updated_files} seed files!")

if __name__ == "__main__":
    main()
