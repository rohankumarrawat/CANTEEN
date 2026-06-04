from app import CanteenApp
import traceback

try:
    app = CanteenApp()
    app._uname.delete(0, 'end')
    app._uname.insert(0, "admin")
    app._pwd.delete(0, 'end')
    app._pwd.insert(0, "admin123")
    app._do_login()

    keys = ["dashboard", "sales", "batch", "inventory", "waste", "master", "users", "report"]
    for k in keys:
        try:
            print(f"Loading {k}...")
            if hasattr(app, "_go"):
                app._go(k)
            else:
                app._navigate(k)
            app.update_idletasks()
        except Exception as e:
            print(f"Crash on {k}:")
            traceback.print_exc()

    print("Success")
except Exception as e:
    traceback.print_exc()
