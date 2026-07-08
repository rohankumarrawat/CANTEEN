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
    
    app._load_data('2026-06-16')
    app._build_create_mode('2026-06-16', 'Tuesday')
    
    root_f = wrap.winfo_children()[0]
    right_f = root_f.winfo_children()[1]
    slots_outer = right_f.winfo_children()[2]
    
    inner = slots_outer._parent_canvas.winfo_children()[0]
    
    for i, child in enumerate(inner.winfo_children()):
        print(f"Child {i}: {child}")
        if isinstance(child, ctk.CTkFrame):
            print(f"  bg: {child.cget('fg_color')}")
            for j, sub in enumerate(child.winfo_children()):
                if isinstance(sub, ctk.CTkFrame) and hasattr(sub, 'cget'):
                    print(f"    sub {j}: {sub} bg={sub.cget('fg_color')}")
                    for k, subsub in enumerate(sub.winfo_children()):
                        if isinstance(subsub, ctk.CTkLabel):
                            print(f"      subsub {k}: text='{subsub.cget('text')}'")
                elif isinstance(sub, ctk.CTkLabel):
                    print(f"    sub {j}: {sub} text='{sub.cget('text')}'")
                else:
                    print(f"    sub {j}: {sub}")

test()
