import tkinter as tk
import customtkinter as ctk

app = ctk.CTk()

main_cont = ctk.CTkFrame(app)
main_cont.pack()

MEAL_SLOTS = ["Lunch", "Paratha", "Mini Meal"]
type_colors = {"Lunch": "#2C4A2A", "Paratha": "#0F766E", "Mini Meal": "#7C3AED"}

def make_slot_card(parent, meal_type):
    print(f"Making slot for {meal_type}")
    slot_card = ctk.CTkFrame(parent, fg_color="white", corner_radius=8, border_width=1)
    slot_card.pack(fill="x", pady=3)
    sh = ctk.CTkFrame(slot_card, fg_color=type_colors[meal_type], corner_radius=0, height=28)
    sh.pack(fill="x")
    sh.pack_propagate(False)
    lbl = ctk.CTkLabel(sh, text=meal_type)
    lbl.pack(side="left")

for m in MEAL_SLOTS:
    make_slot_card(main_cont, m)

app.update()
for child in main_cont.winfo_children():
    print(child)
