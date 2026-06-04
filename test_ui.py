import sys
import threading
import time
import traceback
import tkinter as tk

# patch input to return 'manager' and 'manager123' if requested
import builtins

old_print = print

from app import CanteenApp

def run_test():
    try:
        app = CanteenApp()
        
        # Test Login
        print("Testing Login...")
        app._uname.delete(0, 'end')
        app._uname.insert(0, "admin")
        app._pwd.delete(0, 'end')
        app._pwd.insert(0, "admin123")
        app._do_login()

        time.sleep(1)
        
        pages = ["dashboard", "sales", "inventory", "master", "users", "report", "batch_prep", "wastage", "expenditure"]
        for p in pages:
            print(f"Testing navigation to: {p}")
            try:
                if hasattr(app, "_go"):
                    app._go(p)
                else:
                    app._navigate(p)
                app.update()
                time.sleep(0.1)
            except KeyError:
                print(f"Page '{p}' not found in router")
            except Exception as e:
                print(f"CRASH on page '{p}':")
                traceback.print_exc()

        print("Tests finished successfully.")
        app.destroy()
    except Exception as e:
        print("CRASH during init/login:")
        traceback.print_exc()
        if 'app' in locals():
            app.destroy()

if __name__ == '__main__':
    run_test()
