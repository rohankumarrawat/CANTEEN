import sys
import os
import tkinter as tk

# Set Cwd to parent dir so it finds app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import CanteenApp

def test_pdf():
    print("Initializing CanteenApp (headless mode)...")
    app = CanteenApp()
    
    # Run login to initialize session
    app._uname.insert(0, "admin")
    app._pwd.insert(0, "admin123")
    app._do_login()
    app.update()
    
    # Export PDF report for the range 30 Apr 2026 to 08 Jun 2026
    start_date = "2026-04-30"
    end_date = "2026-06-08"
    print(f"Exporting PDF for period {start_date} to {end_date}...")
    
    try:
        app._export_pdf_report(start_date, end_date)
        print("🎉 PDF exported successfully!")
    except Exception as e:
        print(f"❌ Error during PDF export: {e}")
        import traceback
        traceback.print_exc()
        
    app.destroy()

if __name__ == "__main__":
    test_pdf()
