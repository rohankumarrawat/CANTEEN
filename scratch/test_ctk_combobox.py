import customtkinter as ctk

try:
    app = ctk.CTk()
    cb = ctk.CTkComboBox(app, values=["A", "B", "C"])
    cb.set("A")
    val = cb.get()
    print("SUCCESS:", val)
except Exception as e:
    print("FAILED:", e)
