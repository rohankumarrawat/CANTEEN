import os
import re
import subprocess
from datetime import datetime

months = {"apr": 4, "may": 5, "jun": 6}

def parse_filename_date(filename):
    m = re.match(r"^seed_(\d+)_(apr|may|jun)\.py$", filename)
    if m:
        day = int(m.group(1))
        month_str = m.group(2)
        month = months[month_str]
        return datetime(2026, month, day)
    return None

def main():
    files = os.listdir(".")
    seed_files = []
    for f in files:
        dt = parse_filename_date(f)
        if dt:
            seed_files.append((dt, f))
    
    # Sort chronologically by date
    seed_files.sort(key=lambda x: x[0])
    
    print(f"Found {len(seed_files)} seed files to run.")
    
    python_bin = os.path.join(".venv", "bin", "python")
    if not os.path.exists(python_bin):
        python_bin = "python"  # Fallback
        
    for dt, f in seed_files:
        print(f"Running {f} for date {dt.strftime('%Y-%m-%d')}...")
        res = subprocess.run([python_bin, f], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Error running {f}:")
            print(res.stderr)
            exit(1)
        else:
            lines = res.stdout.strip().split("\n")
            if lines:
                print(f"  {lines[-1]}")
                
    print("🎉 All database seed files executed successfully!")

if __name__ == "__main__":
    main()
