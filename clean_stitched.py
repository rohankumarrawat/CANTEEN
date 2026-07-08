ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
lbl(hbar, "  🍽  Create Daily Menu", size=14, weight="bold", color=WHITE).pack(side="left", padx=10)
ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
fg_color="transparent", hover_color=ARMY_HVR,
text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
command=lambda: overlay.destroy()).pack(side="right", padx=8)

# Footer (packed before content to stay at bottom)
foot = ctk.CTkFrame(modal, fg_color=WHITE, border_width=1,
border_color=BORDER, corner_radius=0, height=60)
foot.pack(fill="x", side="bottom"); foot.pack_propagate(False)

# Content area
content = ctk.CTkScrollableFrame(modal, fg_color="transparent")
content.pack(fill="both", expand=True, padx=16, pady=10)

# ── Date picker row ───────────────────────────────────────────────
date_row = ctk.CTkFrame(content, fg_color=BG_BLU, corner_radius=10,
border_width=1, border_color="#BFDBFE")
date_row.pack(fill="x", pady=(0,12))

lbl(date_row, "📅  Select Date", size=12, weight="bold",
color=BLUE).pack(anchor="w", padx=14, pady=(10,4))

date_input_row = ctk.CTkFrame(date_row, fg_color="transparent")
date_input_row.pack(fill="x", padx=14, pady=(0,10))

date_entry = ctk.CTkEntry(date_input_row, height=40, width=180,
font=ctk.CTkFont(size=14, weight="bold"),
border_color=BORDER, justify="center")
date_entry.pack(side="left", padx=(0,12))
date_entry.insert(0, today_str)

day_label = lbl(date_input_row, "", size=13, weight="bold", color=ARMY_BG)
day_label.pack(side="left", padx=8)

# ── Meal slot rows container ──────────────────────────────────────
slots_container = ctk.CTkFrame(content, fg_color="transparent")
slots_container.pack(fill="x")

# State for each slot
slot_widgets = {}  # meal_type → {dropdown, qty_entry, samp_entry, preview_lbl, preview_frame}

def _update_slot_preview(meal_type):
sw = slot_widgets.get(meal_type)
if not sw: return

sel = sw["dropdown"].get()
if sel.startswith("⭐ "):
sel = sel[2:]

m = menu_state["menu_by_name"].get(sel)
pf = sw["preview_frame"]
pl = sw["preview_lbl"]

if not m:
pf.pack_forget()
return

mid = m["id"]
details = menu_state["recipe_detail"].get(mid, [])
try:
qty = int(sw["qty_entry"].get() or 0)
except ValueError:
qty = 0

if details and qty > 0:
lines = [f"⚡ Auto-calc for {qty} plates of {sel}:"]
for d in details[:8]:
total = d["qpu"] * qty
lines.append(f"  {d['item']}: {total:.2f} {d['unit']} "
f"({d['qpu']:.3f}/plate × {qty})")
if len(details) > 8:
lines.append(f"  +{len(details)-8} more")
# Show total cost
total_cost = sum(d["qpu"] * qty * d["cp"] for d in details)
lines.append(f"\n  💰 Total raw cost: ₹{total_cost:,.0f}")
pl.configure(text="\n".join(lines))
pf.pack(fill="x", pady=(8,0))
elif details and qty == 0:
pl.configure(text=f"⚡ {sel} has {len(details)} ingredients — "
"enter plates to see breakdown")
pf.pack(fill="x", pady=(8,0))
elif not details:
pl.configure(text="⚠️ No ingredient recipes for this item — "
"it has no recipes linked")
pf.pack(fill="x", pady=(8,0))

def _on_new_item_created(m_type, new_name):
with get_db() as conn:
r_menus = conn.execute(
for r in r_recipes:
r_detail.setdefault(r["menu_id"], []).append({
"item": r["item"], "qpu": r["qty_per_unit"],
"unit": r["unit"], "cp": r["cp"], "inv_id": r["inv_id"]
})
menu_state["recipe_detail"] = r_detail

# Now update all dropdown menus with the new values
for m_t, sw in slot_widgets.items():
curr_sel = sw["dropdown"].get()

# Rebuild dropdown values
try:
d = _dt.date.fromisoformat(date_entry.get().strip())
dow = d.strftime("%A")
except:
dow = "Monday"

scheduled_name = sched_map.get(dow, {}).get(m_t, "")

dropdown_values = ["— Skip —", "＋ New Item"]
if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
dropdown_values.insert(1, f"⭐ {scheduled_name}")
for mn in menu_state["menu_names"]:
if mn != scheduled_name:
dropdown_values.append(mn)

sw["dropdown"].configure(values=dropdown_values)

if m_t == m_type:
sw["dropdown"].set(new_name)
m_item = menu_state["menu_by_name"].get(new_name)
if m_item:
ds = m_item.get("default_samples", 0) or 0
if ds > 0:
sw["samp_entry"].delete(0, "end")
sw["samp_entry"].insert(0, str(ds))
else:
if curr_sel in dropdown_values:
sw["dropdown"].set(curr_sel)
else:
sw["dropdown"].set("— Skip —")

_update_slot_preview(m_type)

def _on_dd_change(val, mt):
if val == "＋ New Item":
slot_widgets[mt]["dropdown"].set("— Skip —")
_update_slot_preview(mt)
self._modal_add_menu(
target_date=date_entry.get().strip(),
callback=lambda new_name, m_type=mt: _on_new_item_created(m_type, new_name)
)
else:
_update_slot_preview(mt)

def _build_slots():
"""Build meal slot rows based on the selected date."""
for w in slots_container.winfo_children():
w.destroy()
slot_widgets.clear()

date_str = date_entry.get().strip()
try:
d = _dt.date.fromisoformat(date_str)
dow = d.strftime("%A")
day_label.configure(text=f"{dow}  •  {d.strftime('%d %B %Y')}")
except Exception:
day_label.configure(text="⚠️ Invalid date format (use YYYY-MM-DD)")
return

band(slots_cont
ti = type_icons.get(meal_type, "🍽")

sh = ctk.CTkFrame(slot_card, fg_color=tc, corner_radius=0, height=34)
sh.pack(fill="x"); sh.pack_propagate(False)
lbl(sh, f"  {ti}  {meal_type}", size=12, weight="bold",
color=WHITE).pack(side="left", padx=8)
if scheduled_name:
lbl(sh, f"Scheduled: {scheduled_name}", size=9,
color="#CCCCCC").pack(side="right", padx=12)

body = ctk.CTkFrame(slot_card, fg_color="transparent")
body.pack(fill="x", padx=14, pady=10)

r1 = ctk.CTkFrame(body, fg_color="transparent")
r1.pack(fill="x")
r1.grid_columnconfigure(0, weight=4)
r1.grid_columnconfigure(1, weight=2)
r1.grid_columnconfigure(2, weight=1)

dd_frame = ctk.CTkFrame(r1, fg_color="transparent")
dd_frame.grid(row=0, column=0, sticky="nsew", padx=(0,8))
lbl(dd_frame, "Menu Item", size=10, weight="bold",
color=ARMY_BG).pack(anchor="w")
dd = ctk.CTkOptionMenu(
dd_frame, values=dropdown_values,
font=ctk.CTkFont(size=12), height=40,
fg_color=ARMY_BG, button_color=ARMY_HVR, text_color=WHITE)

if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
dd.set(f"⭐ {scheduled_name}")
else:
dd.set("— Skip —")
dd.pack(fill="x", pady=(4,0))

qty_frame = ctk.CTkFrame(r1, fg_color="transparent")
qty_frame.grid(row=0, column=1, sticky="nsew", padx=(0,8))
lbl(qty_frame, "Plates", size=10, weight="bold",
color=ARMY_BG).pack(anchor="w")
qty_e = ctk.CTkEntry(qty_frame, height=40, corner_radius=10,
placeholder_text="0",
font=ctk.CTkFont(size=14, weight="bold"),
border_color=BORDER, justify="center")
qty_e.pack(fill="x", pady=(4,0))

samp_frame = ctk.CTkFrame(r1, fg_color="transparent")
samp_frame.grid(row=0, column=2, sticky="nsew")
lbl(samp_frame, "🎁 Samples", size=10, color=TEAL).pack(anchor="w")
samp_e = ctk.CTkEntry(samp_frame, height=40, corner_radius=10,
placeholder_text="0",
font=ctk.CTkFont(size=12, weight="bold"),
border_color=TEAL, justify="center",
fg_color="#F0FDFA")
samp_e.pack(fill="x", pady=(4,0))

if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
ds = menu_state["menu_by_name"][scheduled_name].get("default_samples", 0) or 0
if ds > 0:
sam
"preview_lbl": preview_lbl,
}

qty_e.bind("<KeyRelease>", lambda e, mt=meal_type: _update_slot_preview(mt))
dd.configure(command=lambda val, mt=meal_type: _on_dd_change(val, mt))

if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
self.after(100, lambda mt=meal_type: _update_slot_preview(mt))

_build_slots()

date_entry.bind("<Return>", lambda e: _build_slots())
date_entry.bind("<FocusOut>", lambda e: _build_slots())

def _save_daily():
date_str = date_entry.get().strip()
try:
_dt.date.fromisoformat(date_str)
except Exception:
self._popup("⚠️ Invalid Date", "Use YYYY-MM-DD format."); return

saved = 0; logs = []

with get_db() as conn:
for meal_type, sw in slot_widgets.items():
sel = sw["dropdown"].get()

if sel == "— Skip —":
continue

if sel.startswith("⭐ "):
sel = sel[2:]

m = menu_state["menu_by_name"].get(sel)
if not m:
continue

mid = m["id"]
sp = m["sp"]
try:
qty = int(sw["qty_entry"].get() or 0)
except ValueError:
self._popup("⚠️ Invalid", f"Enter a valid number for {meal_type} plates.")
return
if qty <= 0:
continue

samp_qty = 0
try:
samp_qty = max(0, int(sw["samp_entry"].get() or 0))
except ValueError:
samp_qty = 0

# 1. batch_prep
conn.execute(
"INSERT INTO batch_prep (date, menu_id, qty_prepared, samples) "
"VALUES (?,?,?,?)",
(date_str, mid, qty, samp_qty))

# 2. Auto-deduct stock + log expenditure
details = menu_state["recipe_detail"].get(mid, [])
total_raw_cost = 0.0
for d in details:
deduct = d["qpu"] * qty
conn.execute(
"UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id=?",
(deduct, d["inv_id"]))
conn.execute(
"INSERT INTO stock_ledger "
"(date, inv_id, transaction_type, qty_change, notes) "
"VALUES (?,?,?,?,?)",
(date_str, d["inv_id"], "DAILY_MENU", -deduct,
f"Daily menu: {sel} ({meal_type}) x{qty}"))
total_raw_cost += deduct *
(date_str, round(total_raw_cost, 2), "Raw Material",
f"Auto-expenditure for {sel} batch x{qty}"))

# 3. Samples table
if samp_qty > 0:
cogs_per = m["cogs"] if m["cogs"] else 0
conn.execute(
"INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
"VALUES (?,?,?,?,?,?,?,?)",
(date_str, mid, meal_type, sp, samp_qty,
round(cogs_per * samp_qty, 2), "General",
f"Auto from daily menu: {sel}"))

logs.append(f"{meal_type}: {sel} x{qty}")
saved += 1

if saved > 0:
self._toast(f"✅ Daily menu saved  •  " + " | ".join(logs))
overlay.destroy()
self._live_refresh("batch")
else:
self._popup("⚠️ Nothing to save",
"Enter plates for at least one meal, or select items from dropdowns.")

btn(foot, "← Cancel", lambda: overlay.destroy(),
fg=STRIPE, hv=BORDER, h=42, w=120).pack(side="left", padx=16, pady=10)
btn(foot, "✅  Save Daily Menu", _save_daily,
fg=GREEN, hv=DGREEN, h=42, w=220).pack(side="right", padx=16, pady=10)

def _save_batch(self):
today = datetime.now().strftime("%Y-%m-%d")
saved = 0; deduct_log = []; sample_log = []
with get_db() as conn:
for mid2, e in self._be.items():
