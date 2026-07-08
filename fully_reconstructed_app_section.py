font=ctk.CTkFont(size=12, weight="bold"),

bar.pack(fill="x", pady=(14,4))
btn(bar, "✅  Save All Batches", self._save_batch,
fg=GREEN, hv=DGREEN, h=48).pack(fill="x")

# ── Log table ─────────────────────────────────────────────────────────
if batches_today:
lc = card(wrap); lc.pack(fill="x", pady=(14,0))
band(lc, f"📊  Today's Batch Log  •  {today_disp}")
COLS2 = [("Meal Item",4),("Total Prepared",2)]
thead(lc, COLS2, bg=STRIPE, tc=MID)
for ix, b in enumerate(batches_today):
trow(lc, [b["name"], f"{b['total']} units"],
[4,2], colors=[DARK, GREEN], bolds=[True,True],
bg=WHITE if ix%2==0 else STRIPE)

def _save_batch(self):
today = datetime.now().strftime("%Y-%m-%d")
saved = 0; deduct_log = []; sample_log = []
with get_db() as conn:
for mid2, e in self._be.items():
try:    qty = int(e.get() or 0)
- For each meal slot (Lunch, Paratha, Mini Meal):
• Dropdown of known items (pre-filled from daily_menu schedule)
• Plates + Samples inputs
• Auto-ingredient preview for known items
- Save: auto-deducts stock, creates expenditure, batch_prep, samples
- '+ New Item' option opens full wizard on top, and returns new item pre-selected!
"""
import datetime as _dt

today_str = datetime.now().strftime("%Y-%m-%d")
MEAL_SLOTS = ["Lunch", "Paratha", "Mini Meal"]

with get_db() as conn:
all_menus = conn.execute(
"SELECT id, name, sp, cogs, default_samples "
"FROM menu WHERE active=1 ORDER BY name"
).fetchall()
sched_rows = conn.execute(
"SELECT dm.day, dm.meal_type, m.name, m.id as menu_id "
"FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"
).fetchall()
all_recipes = conn.execute(
"SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
"FROM recipes r JOIN inventory i ON i.id=r.inv_id"
).fetchall()

# Build lookups
menu_by_name = {m["name"]: m for m in all_menus}
menu_by_id   
- Pick date → shows day of week
body = ctk.CTkFrame(mc, fg_color="transparent")
body.pack(fill="x", padx=12, pady=10)

# Ingredient pills
if has_recipe:
pf = ctk.CTkFrame(body, fg_color="transparent")
pf.pack(fill="x", pady=(0,6))
for ing_txt in recipe_map[mid2][:3]:
ctk.CTkLabel(pf, text=f"🥄 {ing_txt}", height=20,
corner_radius=6, fg_color=BG_SAF,
font=ctk.CTkFont(size=9),
text_color=ARMY_BG).pack(side="left", padx=(0,4))
else:
lbl(body, "No ingredients mapped", size=9, color=MID).pack(anchor="w", pady=(0,4))

# ── Input row: Qty + Samples side by side ──────────────────────
input_row = ctk.CTkFrame(body, fg_color="transparent")
input_row.pack(fill="x", pady=(0,2))
input_row.grid_columnconfigure(0, weight=3)
input_row.grid_columnconfigure(1, weight=1)

# Qty to Prepare
qty_f = ctk.CTkFrame(input_row, fg_color="transparent")
qty_f.grid(row=0, column=0, sticky="nsew", padx=(0,4))
lbl(qty_f, "Qty to Prepare", size=10, color=MID).pack(anchor="w")
e = ctk.CTkEntry(qty_f, height=40, corner_radius=10,
placeholder_text="0",

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
corner_radius=8, border_width=1,
border_color="#BBF7D0")
# Start hidden; shown when user types a qty
_preview_visible = [False]
_preview_lbl = lbl(preview_frame,
"Type qty above to see ingredient breakdown",
size=9, color=MID, wraplength=280)
_preview_lbl.pack(padx=8, pady=6, anchor="w")

def _update_preview(event, mid=mid2, plbl=_preview_lbl,
pf2=preview_frame, pv=_preview_visible,
qty_entry=e):
try:
qty = int(qty_entry.get() or 0)
except ValueError:
qty = 0
if qty > 0:
details = recipe_detail.get(mid, [])
lines = [f"⚡ Auto-calc for {qty} plates:"]
for d in details[:6]:
total = d["qpu"] * qty
lines.append(f"  {d['item']}: {total:.2f} {d['unit']} ({d['qpu']:.3f}/plate)")
if len(details) > 6:
lines.append(f"  +{len(details)-6} more ingredients")
plbl.configure(text="\n".join(lines), text_color=ARMY_BG)
if not pv[0]:
pf2.pack(fill="x", pady=(6,0))
pv[0] = True
else:
if pv[0]:
pf2.pack_forget()
# Section header
band(slots_container,
f"
color=BLUE).pack(anchor="w", padx=14, pady=(10,4))

date_input_row = ctk.CTkFrame(date_row, fg_color="transparent")
date_input_row.pack(fill="x", padx=14, pady=(0,10))

date_entry = ctk.CTkEntry(date_input_row, height=40, width=180,
font=ctk.CTkFont(size=14, weight="bold"),
border_color=BORDER, justify="center")
date_entry.pack(side="left", padx=(0,12))
date_entry.insert(0, today_str)

font=ctk.CTkFont(size=11, weight="bold"),
command=lambda c=code: _select_type(c))
b.pack(side="left", padx=3)
type_btns[code] = b

# ── Dynamic form ──────────────────────────────────────────────────────
def _refresh_form():
for w in form_frame.winfo_children():
w.destroy()
fields.clear()
def _modal_daily_menu(self):
"""
Smart Daily Menu Creator modal:
- Pick date → shows day of week
- For each meal slot (Lunch, Paratha, Mini Meal):
• Dropdown of known items (pre-filled from daily_menu schedule)
• Plates + Samples inputs
• Auto-ingredient preview for known items
- Save: auto-deducts stock, creates expenditure, batch_prep, samples
- '+ New Item' option opens full wizard on top, and returns new item pre-selected!
"""
import datetime as _dt

today_str = datetime.now().strftime("%Y-%m-%d")
MEAL_SLOTS = ["Lunch", "Paratha", "Mini Meal"]

with get_db() as conn:
all_menus = conn.execute(
"SELECT id, name, sp, cogs, default_samples "
"FROM menu WHERE active=1 ORDER BY name"
).fetchall()
sched_rows = conn.execute(
"SELECT dm.day, dm.meal_type, m.name, m.id as menu_id "
"FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"
).fetchall()
all_recipes = conn.execute(
"SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
"FROM recipes r JOIN inventory i ON i.id=r.inv_id"
).fetchall()

# Build lookups
menu_by_name = {m["name"]: m for m in all_menus}
menu_by_id   
modal = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
border_width=2, border_color=ARMY_BG,
width=900, height=680)
modal.place(relx=0.5, rely=0.5, anchor="center")
modal.pack_propagate(False)

# Header
hbar = ctk.CTkFrame(modal, fg_color=ARMY_BG, corner_radius=0, height=54)
hbar.pack(fill="x"); hbar.pack_propagate(False)
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
slot_widgets[mt]["dropdown"].set("— Skip —")
_update_slot_preview(mt)
"enter plates to see breakdown")
if not _vis[0]:
_pf.pack(fill="x", pady=(8,0))
_vis[0] = True
elif not details:
_pl.configure(text="⚠️ No ingredient recipes for this item — "
"use '＋ New Item' to create with ingredients")
if not _vis[0]:
_pf.pack(fill="x", pady=(8,0))
_vis[0] = True

qty_e.bind("<KeyRelease>", _update_preview)
dd.configure(command=lambda val, up=_update_preview: up())

# Trigger initial preview if pre-selected
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
date_str = date_entry.get().strip()
try:
_dt.date.fromisoformat(date_str)
except Exception:
self._popup("⚠️ Invalid Date", "Use YYYY-MM-DD format."); return

saved = 0; logs = []
new_item_requested = False

with get_db() as conn:
for meal_type, sw in slot_widgets.items():
sel = sw["dropdown"].get()

# Skip
if sel == "— Skip —":
continue

# New Item → close modal, open wizard
if sel == "＋ New Item":
new_item_requested = True
continue

# Strip star prefix
if sel.startswith("⭐ "):
sel = sel[2:]

m = menu_by_name.get(sel)
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
if se:
try:    samp_qty = int(se.get() or 0)
except: samp_qty = 0
if samp_qty < 0: samp_qty = 0

# Resolve generic menu_id to today's specific one
spec_mid, spec_name = self._resolve_specific_menu_id_and_name(conn, mid2, today, "")
if not spec_name:
row = conn.execute("SELECT name, sp FROM menu WHERE id=?", (spec_mid,)).fetchone()
spec_name = row["name"] if row else ""
sp = row["sp"] if row else 0
else:
row = conn.execute("SELECT sp FROM menu WHERE id=?", (spec_mid,)).fetchone()
sp = row["sp"] if row else 0

# Save batch_prep with samples column
conn.execute(
"INSERT INTO batch_prep (date, menu_id, qty_prepared, samples) "
"VALUES (?,?,?,?)",
(today, spec_mid, qty, samp_qty))

# Auto-insert into samples table if samples > 0
if samp_qty > 0:
# Determine meal type from daily_menu or heuristic
import datetime as _dt
try:
dow = _dt.date.fromisoformat(today).strftime("%A")
dm_row = conn.execute(
"SELECT meal_type FROM daily_menu WHERE menu_id=? AND day=?",
(spec_mid, dow)).fetchone()
meal_type = dm_row["meal_type"] if dm_row else "Lunch"
except Exception:
dd_frame, values=dropdown_values,
font=ctk.CTkFont(size=12), height=40,

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
conn.execute(
"INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
"VALUES (?,?,?,?,?,?,?,?)",
(date_str, mid, meal_type, sp, samp_qty,
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
samp_e.insert(0, str(ds))

preview_f = ctk.CTkFrame(body, fg_color="#F0FDF4",
corner_radius=8, border_width=1,
border_color="#BBF7D0")
preview_lbl = lbl(preview_f, "", size=9, color=ARMY_BG, wraplength=800)
preview_lbl.pack(padx=8, pady=6, anchor="w")

slot_widgets[meal_type] = {
"dropdown": dd,
"qty_entry": qty_e,
"samp_entry": samp_e,
"preview_frame": preview_f,
"preview_lbl": preview_lbl,
}

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
if total_raw_cost > 0:
conn.execute(
"INSERT INTO expenditure (date, amount, category, notes) "
"VALUES (?,?,?,?)",
(date_str, round(total_raw_cost, 2), "Raw Material",
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
self._toast(summary)
self._live_refresh("batch")

# ==============================================================================
# INVENTORY — full CRUD with category tabs & edit-in-dialog
# ==============================================================================
def _pg_inventory(self):
hf = self._hdr("📦  Stock / Inventory",
datetime.now().strftime("📅  %d %B %Y  •  Live stock levels"))

# Category filter tabs
ff = ctk.CTkFrame(hf, fg_color="transparent"); ff.pack(side="right", padx=PAD)
cats = ["All","Dry","Fresh","Dairy","Bakery","Prepared"]
self._inv_fb = {}
for cat in cats:
b = ctk.CTkButton(ff, text=cat, width=72, height=28,
corner_radius=8, font=ctk.CTkFont(size=11, weight="bold"),
fg_color=ARMY_BG if cat==self._inv_filter else STRIPE,
text_color=WHITE if cat==self._inv_filter else DARK,
hover_color=ARMY_HVR,
command=lambda c=cat: self._inv_setcat(c))
b.pack(side="left", padx=2)
self._inv_fb[cat] = b

# Search bar
sb = ctk.CTkFrame(self._area, fg_color="transparent")
sb.pack(fill="x", padx=PAD, pady=(8,0))
self._inv_search = ctk.CTkEntry(sb, placeholder_text="\U0001f50d  Search inventory items...",
height=34, corner_radius=10)
self._inv_search.pack(fill="x")
self._inv_search.bind("<KeyRelease>", lambda e: self._debounce("_inv_search_job", self._inv_filter_search))
(today, rc["inv_id"], "BATCH_PREP", -deduct,
f"Batch: {spec_name} x{qty}"))
total_raw_cost += deduct * (rc["cp"] or 0)
deduct_log.append(f"{rc['item']} -{deduct:.2f}{rc['unit']}")

# Auto-expenditure for batch raw material cost
if total_raw_cost > 0:
conn.execute(
"INSERT INTO expenditure (date, amount, category, notes) "
"VALUES (?,?,?,?)",
(today, round(total_raw_cost, 2), "Raw Material",
f"Auto-expenditure for {spec_name} batch x{qty}"))

saved += 1

if saved == 0:
self._popup("⚠️ Nothing saved", "Enter at least one qty > 0."); return
summary = f"✅ {saved} batch(es) saved"
if sample_log:
summary += "  |  🎁 Samples: " + ", ".join(sample_log[:3])
if deduct_log:

# ==============================================================================
# INVENTORY — full CRUD with category tabs & edit-in-dialog
# ==============================================================================
def _pg_inventory(self):
def _pg_inventory(self):
hf = self._hdr("📦  Stock / Inventory",
datetime.now().strftime("📅  %d %B %Y  •  Live stock levels"))

# Category filter tabs
ff = ctk.CTkFrame(hf, fg_color="transparent"); ff.pack(side="right", padx=PAD)
cats = ["All","Dry","Fresh","Milk","Package material","Misc"]
self._inv_fb = {}
for cat in cats:
b = ctk.CTkButton(ff, text=cat, width=72, height=28,
corner_radius=8, font=ctk.CTkFont(size=11, weight="bold"),
fg_color=ARMY_BG if cat==self._inv_filter else STRIPE,
text_color=WHITE if cat==self._inv_filter else DARK,
hover_color=ARMY_HVR,
command=lambda c=cat: self._inv_setcat(c))
b.pack(side="left", padx=2)

# Search bar
sb = ctk.CTkFrame(self._area, fg_color="transparent")
sb.pack(fill="x", padx=PAD, pady=(8,0))
self._inv_search = ctk.CTkEntry(sb, placeholder_text="\U0001f50d  Search inventory items...",
height=34, corner_radius=10)
self._inv_search.pack(fill="x")
self._inv_search.bind("<KeyRelease>", lambda e: self._debounce("_inv_search_job", self._inv_filter_search))

def _pg_expenditure(self):
today = datetime.now().strftime("%Y-%m-%d")
hf = self._hdr("💸  Expenditure Manager",
f"Track all cash outflows  •  Today: {today}")

wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
wrap.pack(fill="both", expand=True, padx=PAD, pady=(14,PAD))

CATS = ["Dry Ration","Fresh Vegetables","Dairy","Packaging Material & Sweets",
"Misc Expenditure","Repair","Property","Other"]

# ── Add Expenditure Form ──────────────────────────────────────────────
fc = card(wrap); fc.pack(fill="x", pady=(0,14))
band(fc, "➕  Record New Expenditure")
ff = ctk.CTkFrame(fc, fg_color="transparent"); ff.pack(fill="x", padx=18, pady=14)

lbl(ff,"Date",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=0,sticky="w",pady=(0,4))
lbl(ff,"Category",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=1,sticky="w",padx=(20,0),pady=(0,4))
lbl(ff,"Amount (₹)",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=2,sticky="w",padx=(20,0),pady=(0,4))

self._exp_deduct = ctk.BooleanVar(value=False)
cdc = ctk.CTkCheckBox(fc, text="Link to Inventory (Add this purchase to stock)", 
variable=self._exp_deduct, text_color=ARMY_BG, font=ctk.CTkFont(size=11, weight="bol
lbl(cf, col, size=10, weight="bold", color=GOLD_LT).pack(anchor="w", padx=10, pady=8)

self._inv_sf = ctk.CTkScrollableFrame(tc, fg_color="transparent")
self._inv_sf.pack(fill="both", expand=True)
self._inv_hdr = INV_HDR
self._inv_loadrows()

]

for (val, bold, color), w in zip(vals, widths):
cf = ctk.CTkFrame(rf, fg_color="transparent", width=w)
cf.pack(side="left", fill="y"); cf.pack_propagate(False)
lbl(cf, str(val), size=11,
weight="bold" if bold else "normal",
color=color).pack(anchor="w", padx=10, pady=6)

def _dlg_inv_add(self):
body, card, close = self._show_modal("＋  Add New Inventory Item", 540, 520)
fields = {}
CATEGORIES = ["Dry", "Fresh", "Dairy", "Bakery", "Prepared", "Misc"]

# ── CSV-order hint ────────────────────────────────────────────────────
hint = ctk.CTkFrame(body, fg_color=BG_GRN, corner_radius=8)
hint.pack(fill="x", pady=(0, 10))
lbl(hint, "Fields match the CSV import format:",
size=9, weight="bold", color=ARMY_BG).pack(anchor="w", padx=10, pady=(5, 1))
lbl(hint, "item → category → unit → opening_stock → min_level → cost_price",
size=9, color=MID).pack(anchor="w", padx=10, pady=(0, 5))

# ── Item Name ─────────────────────────────────────────────────────────
lbl(body, "Item Name", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4, 3))
e_name = entry(body, ph="e.g., Mustard Oil", h=38); e_name.pack(fill="x")
fields["name"] = e_name

# ── Category ────────────────
e_unit = entry(body, ph="e.g., kg", h=38); e_unit.pack(fill="x")
fields["unit"] = e_unit

# ── Opening Stock + Min Level (side by side) ──────────────────────────
rf = ctk.CTkFrame(body, fg_color="transparent"); rf.pack(fill="x", pady=(8, 0))
rf.grid_columnconfigure(0, weight=1); rf.grid_columnconfigure(1, weight=1)

(eq, eq, new_cp, it))
conn.execute("INSERT INTO goods_received (date,inv_id,qty,total_cost) VALUES (?,?,?,?)",
(exp_date, row["id"], eq, amt))
def _inv_render_rows(self, data, search_q=""):
"""Destroy old rows and paint filtered rows — always runs on main thread."""
if not hasattr(self, "_inv_sf") or not self._inv_sf.winfo_exists():
return

# Apply in-memory filter
if search_q:
data = [d for d in data if search_q in d["item"].lower()]

# Clear existing rows
for w in self._inv_sf.winfo_children():
w.destroy()

ci = {"Dry":"🌾","Fresh":"🥦","Milk":"🥛","Bakery":"🥐","Package material":"📦"}
widths = [w for _, w in self._inv_hdr]

for ix, item in enumerate(data):
low = item["stock"] < item["min_lvl"]
bg2 = "#FEE2E2" if low else (WHITE if ix % 2 == 0 else STRIPE)

rf = ctk.CTkFrame(self._inv_sf, fg_color=bg2, corner_radius=0, height=40)
rf.pack(fill="x"); rf.pack_propagate(False)

cat_icon = ci.get(item["cat"], "•")
vals = [
(f"  {item['item']}",        True,  DARK),
(f"{cat_icon} {item['cat']}", False, MID),
(item["unit"],               False, MID),
(f"{item['opening']:.1f}",   False, MID),
(f"{item['received']:.1f}",  False, MID),
(f"{item['stock']:.1f}",     True,  RED if low else GREEN),
(f"{item['min_lvl']:.1f}",   False, MID),
("⚠ LOW" if low else "✓ OK", True,  RED if low else GREEN),
]

for (val, bold, color), w in zip(vals, widths):
cf = ctk.CTkFrame(rf, fg_color="transparent", width=w)
cf.pack(side="left", fill="y"); cf.pack_propagate(False)
lbl(cf, str(val), size=11,
weight="bold" if bold else "normal",
color=color).pack(anchor="w", padx=10, pady=6)

def _dlg_inv_add(self):
body, card, close = self._show_modal("＋  Add New Inventory Item", 540, 520)
fields = {}
CATEGORIES = ["Dry", "Fresh", "Milk", "Bakery", "Package material", "Misc"]

# ── CSV-order hint ────────────────────────────────────────────────────
hint = ctk.CTkFrame(body, fg_color=BG_GRN, corner_radius=8)
hint.pack(fill="x", pady=(0, 10))
lbl(hint, "Fields match the CSV import format:",
size=9, weight="bold", color=ARMY_BG).pack(anchor="w", padx=10, pady=(5, 1))
lbl(hint, "item → category → unit → opening_stock → min_level → cost_price",
size=9, color=MID).pack(anchor="w", padx=10, pady=(0, 5))

# ── Item Name ─────────────────────────────────────────────────────────
lbl(body, "Item Name", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4, 3))
e_name = entry(body, ph="e.g., Mustard Oil", h=38); e_name.pack(fill="x")
fields["name"] = e_name

# ── Category ─────────────────────────────────────────────────────────
fields["unit"] = e_unit

# ── Opening Stock + Min Level (side by side) ──────────────────────────
rf = ctk.CTkFrame(body, fg_color="transparent"); rf.pack(fill="x", pady=(8, 0))
rf.grid_columnconfigure(0, weight=1); rf.grid_columnconfigure(1, weight=1)

lbl(rf, "Opening Stock", size=11, weight="bold",
color=ARMY_BG).grid(row=0, column=0, sticky="w", pady=(0, 3))
e_stock = entry(rf, ph="e.g., 20", h=38)
e_stock.grid(row=1, column=0, sticky="ew", padx=(0, 8))
fields["stock"] = e_stock

lbl(rf, "Min Level Alert", size=11, weight="bold",
color=ARMY_BG).grid(row=0, column=1, sticky="w", pady=(0, 3))
e_min = entry(rf, ph="e.g., 5", h=38)
e_min.grid(row=1, column=1, sticky="ew")
fields["min_lvl"] = e_min

# ── Cost Price ────────────────────────────────────────────────────────
lbl(body, "Cost Price per Unit (₹)", size=11, weight="bold",
color=ARMY_BG).pack(anchor="w", pady=(8, 3))
e_cp = entry(body, ph="e.g., 90", h=38); e_cp.pack(fill="x")
fields["cp"] = e_cp

def save():
try:
nm   = fields["name"].get().strip()
unit = fields["unit"].get().strip()
stk  = float(fields["stock"].get() or 0)
mn   = float(fields["min_lvl"].get() or 0)
cp   = float(fields["cp"].get() or 0)
def _master_daily_menu(self, wrap):
"""
Date-wise daily menu creation & viewing.
- All 3 meal slots always visible (Lunch, Paratha, Mini Meal)
- + Add New Dish: unlimited extra items (Chaach, Amul Kool, Brownie, etc.)
- Known items: just enter plates+samples → auto-deduct stock
- New items: open add-menu wizard and return
"""
import datetime as _dt
today_str = datetime.now().strftime("%Y-%m-%d")
MEAL_SLOTS = ["Lunch", "Paratha", "Mini Meal"]

# ── Date picker bar ────────────────────────────────────────────────────
date_card = card(wrap); date_card.pack(fill="x", pady=(0, 10))
band(date_card, "📅  Select Date  —  View or Create Daily Menu",
bg=ARMY_BG, tc=GOLD_LT, h=38)

dr = ctk.CTkFrame(date_card, fg_color="transparent")
dr.pack(fill="x", padx=14, pady=(10, 4))
lbl(dr, "Date (YYYY-MM-DD):", size=11, weight="bold", color=ARMY_BG
).pack(side="left", padx=(0, 10))
date_var   = ctk.StringVar(value=today_str)
date_entry = ctk.CTkEntry(dr, textvariable=date_var, height=40, width=170,
font=ctk.CTkFont(size=14, weight="bold"),
border_color=BORDER, justify="center")
date_entry.pack(side="left"
# NOTE: no expand=True here so the scrollable parent frame (wrap) can scroll
content_area = ctk.CTkFrame(wrap, fg_color="transparent")
content_area.pack(fill="x")

# Shared mutable state
slot_widgets  = {}   # meal_type / key → widget dict
extra_counter = [0]  # counter for unique extra-slot keys

def _get_menu_data():
with get_db() as conn:
all_menus   = [dict(m) for m in conn.execute(
"SELECT id, name, sp, cogs, default_samples "
"FROM menu WHERE active=1 ORDER BY name"
).fetchall()]
sched_rows  = [dict(s) for s in conn.execute(
"SELECT dm.day, dm.meal_type, m.name "
"FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"
).fetchall()]
all_recipes = [dict(r) for r in conn.execute(
"SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
"FROM recipes r JOIN inventory i ON i.id=r.inv_id"
).fetchall()]
menu_by_name  = {m["name"]: m for m in all_menus}
menu_names    = [m["name"] for m in all_menus]
sched_map     = {}
for s in sched_rows:
sched_map.setdefault(s["day"], {})[s["meal_type"]] = s["name"]
recipe_detail = {}
for r in all_recipes:
recipe_detail.setdefault(r["menu_id"], []).append({
"item": r["item"], "qpu": r["qty_per_unit"],
"unit": r["unit"], "cp":  r["cp"], "inv_id": r["inv_id"]
})
return {
"menu_by_name": menu_by_name, "menu_names": menu_names,
"recipe_detail": recipe_detail, "sched_map": sched_map,
"all_menus": all_menus,
}

def _load_date(*_):
for w in content_area.winfo_children(): w.destroy()
slot_widgets.clear()
extra_counter[0] = 0

date_str = date_var.get().strip()
try:
d   = _dt.date.fromisoformat(date_str)
dow = d.strftime("%A")
day_lbl.configure(text=f"{dow}  •  {d.strftime('%d %B %Y')}")
except Exception:
day_lbl.configure(text="⚠️  Use YYYY-MM-DD")
status_lbl.configure(text="", text_color=GREEN)
