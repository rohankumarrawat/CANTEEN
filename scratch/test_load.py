import sys
sys.path.append("/Users/rohan/Desktop/canteen")
import tkinter as tk
import customtkinter as ctk
import datetime
from app import CanteenApp

def test():
    app = CanteenApp()
    wrap = ctk.CTkFrame(app)
    app._master_daily_menu(wrap)
    
    # We must trigger it using the GUI button because _load_data is nested
    root_f = wrap.winfo_children()[0]
    right_f = root_f.winfo_children()[1]
    date_card = right_f.winfo_children()[0]
    
    # The Load button is the last child of date_card
    load_btn = date_card.winfo_children()[-1]
    
    # Set the date entry to '2026-06-16'
    date_entry = date_card.winfo_children()[2]
    date_entry.delete(0, 'end')
    date_entry.insert(0, '2026-06-16')
    
    # Click the load button
    load_btn.invoke()
    
    app.update()

test()
