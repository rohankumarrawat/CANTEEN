from app import CanteenApp
import traceback
import sys

try:
    app = CanteenApp()
    app._uname.delete(0, 'end')
    app._uname.insert(0, "admin")
    app._pwd.delete(0, 'end')
    app._pwd.insert(0, "admin123")
    app._do_login()

    if hasattr(app, "_go"):
        app._go("waste")
    else:
        app._navigate("waste")
    app.update()
    # It renders the page
    print("Waste Page loaded")
    
    if hasattr(app, "_go"):
        app._go("batch")
    else:
        app._navigate("batch")
    app.update()
    print("Batch Page loaded")

    app.destroy()
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
