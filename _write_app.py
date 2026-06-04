"""Helper: writes the new Indian-Army-themed app.py"""
import os

NEW_CONTENT = r'''"""
Canteen Inventory & Sales Management System
Indian Army — Demo Application  |  Python + CustomTkinter + SQLite

DATA STORAGE
────────────
All data is saved in a local SQLite database file:
    canteen.db   ← same folder as this script
Tables: inventory, sales
The file is created automatically on first launch.
"""

import customtkinter as ctk
from datetime import datetime
import sqlite3
import os

# ── Database Setup ─────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canteen.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS inventory (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                item     TEXT NOT NULL,
                cat      TEXT NOT NULL,
                unit     TEXT NOT NULL,
                stock    REAL NOT NULL DEFAULT 0,
                min_lvl  REAL NOT NULL DEFAULT 0,
                opening  REAL NOT NULL DEFAULT 0,
                received REAL NOT NULL DEFAULT 0,
                updated  TEXT DEFAULT CURRENT_DATE
            );
            CREATE TABLE IF NOT EXISTS sales (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                date    TEXT NOT NULL DEFAULT CURRENT_DATE,
                meal    TEXT NOT NULL,
                sp      REAL NOT NULL,
                sold    INTEGER NOT NULL DEFAULT 0,
                cogs    REAL NOT NULL DEFAULT 0,
                payment TEXT NOT NULL DEFAULT 'Cash'
            );
        """)
        if conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO inventory (item,cat,unit,stock,min_lvl,opening,received) VALUES (?,?,?,?,?,?,?)",
                [
                    ("Rice",        "Dry",       "Kg",  45.0, 20.0, 55.0, 10.0),
                    ("Dal (Toor)",  "Dry",       "Kg",   3.5,  5.0,  8.0,  0.0),
                    ("Wheat Flour", "Dry",       "Kg",  30.0, 15.0, 35.0,  5.0),
                    ("Sugar",       "Dry",       "Kg",   1.2,  3.0,  4.0,  0.0),
                    ("Cooking Oil", "Dry",       "Ltr",  8.0,  5.0, 10.0,  2.0),
                    ("Tomatoes",    "Fresh",     "Kg",   4.0,  2.0,  6.0,  2.0),
                    ("Onions",      "Fresh",     "Kg",   6.5,  3.0,  8.0,  2.0),
                    ("Milk",        "Dairy",     "Ltr",  0.8,  5.0,  5.0,  0.0),
                    ("Paneer",      "Dairy",     "Kg",   2.0,  1.0,  3.0,  0.0),
                    ("Lunch Boxes", "Packaging", "Pcs", 50.0,100.0,100.0,  0.0),
                ]
            )
        today = datetime.now().strftime("%Y-%m-%d")
        if conn.execute("SELECT COUNT(*) FROM sales WHERE date=?", (today,)).fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO sales (date,meal,sp,sold,cogs,payment) VALUES (?,?,?,?,?,?)",
                [
                    (today, "Standard Lunch", 80,  45, 2700, "Cash"),
                    (today, "VIP Thali",      150, 12, 1200, "UPI"),
                    (today, "Tea",            10,  80,  400, "Cash"),
                    (today, "Snacks",         30,  25,  500, "Card"),
                ]
            )

init_db()

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Indian Army Color Palette ──────────────────────────────────────────────────
SAFFRON   = "#FF9933"   # Indian flag saffron
IND_GREEN = "#138808"   # Indian flag green
GOLD      = "#C9A84C"   # Military brass / gold
GOLD_LT   = "#EDD97A"   # Light gold for on-dark text

ARMY_BG   = "#1F3320"   # Dark army green  (sidebar / bands)
ARMY_HVR  = "#2C4A2A"   # Hover state
ARMY_SEP  = "#2E4830"   # Separator lines

DARK   = "#1E293B"
MID    = "#64748B"
LIGHT  = "#F0F4EE"      # Subtle green-tinted background
WHITE  = "#FFFFFF"
BORDER = "#DDE8DD"
STRIPE = "#F4F9F4"

RED    = "#DC2626"
DRED   = "#B91C1C"
GREEN  = "#059669"
DGREEN = "#047857"
BLUE   = "#2563EB"
DBLUE  = "#1D4ED8"
PURPLE = "#7C3AED"

# ── Widget helpers ─────────────────────────────────────────────────────────────
def card(parent, **kw):
    d = dict(fg_color=WHITE, corner_radius=14, border_width=1, border_color=BORDER)
    d.update(kw)
    return ctk.CTkFrame(parent, **d)

def label(parent, text, size=13, weight="normal", color=DARK, **kw):
    return ctk.CTkLabel(parent, text=text,
                        font=ctk.CTkFont(size=size, weight=weight),
                        text_color=color, **kw)

def tricolor(parent, h=5):
    """Horizontal Indian tricolor stripe."""
    bar = ctk.CTkFrame(parent, fg_color="transparent", height=h)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    for c in (SAFFRON, WHITE, IND_GREEN):
        ctk.CTkFrame(bar, fg_color=c, width=9999).pack(side="left", fill="y", expand=True)

def army_band(parent, text):
    """Dark-green header band used across cards."""
    hdr = ctk.CTkFrame(parent, fg_color=ARMY_BG, corner_radius=0, height=44)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    label(hdr, f"  {text}", size=12, weight="bold", color=GOLD_LT).pack(side="left", padx=4, pady=10)

# ══════════════════════════════════════════════════════════════════════════════
class CanteenApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Indian Army Canteen Management System")
        self.geometry("1300x800")
        self.minsize(1100, 680)
        self.configure(fg_color=LIGHT)
        self._show_login()

    # ── Login ──────────────────────────────────────────────────────────────────
    def _show_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color="#EEF4EE")

        # Fullwidth tricolor at very top of window
        top_strip = ctk.CTkFrame(self, height=8, fg_color="transparent")
        top_strip.pack(fill="x", side="top")
        top_strip.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(top_strip, fg_color=c).pack(side="left", fill="y", expand=True)

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        box = ctk.CTkFrame(outer, fg_color=WHITE, corner_radius=24,
                           border_width=2, border_color=BORDER)
        box.pack()

        # Army-green header inside card
        hdr = ctk.CTkFrame(box, fg_color=ARMY_BG, corner_radius=0, height=118, width=424)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tricolor(hdr, 4)
        label(hdr, "🇮🇳  INDIAN ARMY", size=11, weight="bold", color=GOLD_LT).pack(pady=(12, 0))
        label(hdr, "CANTEEN MANAGEMENT SYSTEM", size=19, weight="bold", color=WHITE).pack(pady=(2, 0))
        label(hdr, "Service Before Self  •  सेवा परमो धर्म", size=10, color=GOLD).pack(pady=(2, 12))

        label(box, "Staff / Officer Login", size=15, weight="bold", color=ARMY_BG).pack(pady=(26, 20))

        label(box, "Username", size=12, weight="bold", color="#374151", anchor="w").pack(padx=44, fill="x", pady=(0, 4))
        self._uname = ctk.CTkEntry(box, width=340, height=46, corner_radius=10,
                                   placeholder_text="Enter username",
                                   font=ctk.CTkFont(size=14), border_color="#CBD5E1")
        self._uname.pack(padx=40, pady=(0, 14))
        self._uname.insert(0, "manager")

        label(box, "Password", size=12, weight="bold", color="#374151", anchor="w").pack(padx=44, fill="x", pady=(0, 4))
        self._pwd = ctk.CTkEntry(box, width=340, height=46, corner_radius=10,
                                 placeholder_text="Enter password", show="●",
                                 font=ctk.CTkFont(size=14), border_color="#CBD5E1")
        self._pwd.pack(padx=40, pady=(0, 22))
        self._pwd.insert(0, "1234")
        self._pwd.bind("<Return>", lambda e: self._do_login())

        ctk.CTkButton(box, text="🔐   Login to System", width=340, height=52,
                      corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=self._do_login).pack(padx=40, pady=(0, 14))

        self._login_err = label(box, "", size=12, color=RED)
        self._login_err.pack()

        foot = ctk.CTkFrame(box, height=5, fg_color="transparent", width=424)
        foot.pack(fill="x", pady=(14, 0))
        foot.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(foot, fg_color=c).pack(side="left", fill="y", expand=True)
        label(box, "जय हिन्द  •  Demo v1.0", size=11, color="#94A3B8").pack(pady=(8, 22))

    def _do_login(self):
        if self._uname.get().strip() == "manager" and self._pwd.get() == "1234":
            self._show_main()
        else:
            self._login_err.configure(text="⚠  Invalid credentials. Try  manager / 1234")

    # ── Main Shell ─────────────────────────────────────────────────────────────
    def _show_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=LIGHT)

        # Sidebar
        self._sidebar = ctk.CTkFrame(self, fg_color=ARMY_BG, width=252, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)
        tricolor(self._sidebar, 5)

        logo_f = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        logo_f.pack(fill="x", padx=18, pady=(14, 0))
        label(logo_f, "🇮🇳", size=34).pack(side="left", padx=(0, 10))
        txt_f = ctk.CTkFrame(logo_f, fg_color="transparent")
        txt_f.pack(side="left")
        label(txt_f, "INDIAN ARMY", size=12, weight="bold", color=GOLD).pack(anchor="w")
        label(txt_f, "Canteen System", size=10, color="#8AA88A").pack(anchor="w")

        ctk.CTkFrame(self._sidebar, height=1, fg_color=ARMY_SEP).pack(fill="x", padx=18, pady=12)

        unit = ctk.CTkFrame(self._sidebar, fg_color="#162818", corner_radius=10)
        unit.pack(padx=14, fill="x", pady=(0, 14))
        label(unit, "⭐  Unit / Establishment", size=10, color=GOLD).pack(padx=14, pady=(10, 2), anchor="w")
        label(unit, "56 APO Field Canteen", size=12, weight="bold", color=WHITE).pack(padx=14, anchor="w")
        label(unit, "Est. 1947  •  Serving with Pride", size=9, color="#8AA88A").pack(padx=14, pady=(0, 10), anchor="w")

        ctk.CTkFrame(self._sidebar, height=1, fg_color=ARMY_SEP).pack(fill="x", padx=18, pady=(0, 8))

        nav_items = [
            ("📊   Dashboard",    "dashboard"),
            ("💰   Sales Entry",  "sales"),
            ("📦   Inventory",    "inventory"),
            ("📋   Daily Report", "report"),
        ]
        self._nav_btns = {}
        for lbl_txt, page in nav_items:
            b = ctk.CTkButton(self._sidebar, text=lbl_txt, anchor="w", height=46,
                              font=ctk.CTkFont(size=14), fg_color="transparent",
                              hover_color=ARMY_HVR, text_color="#9DB89D",
                              corner_radius=10,
                              command=lambda p=page: self._navigate(p))
            b.pack(padx=14, pady=3, fill="x")
            self._nav_btns[page] = b

        ctk.CTkFrame(self._sidebar, height=1, fg_color=ARMY_SEP).pack(
            fill="x", padx=18, side="bottom", pady=(10, 6))
        ctk.CTkButton(self._sidebar, text="⬅   Logout", height=42, anchor="w",
                      fg_color="transparent", hover_color=ARMY_HVR, text_color="#5A7A5A",
                      font=ctk.CTkFont(size=13), corner_radius=10,
                      command=self._show_login).pack(padx=14, pady=(0, 12), fill="x", side="bottom")

        usr = ctk.CTkFrame(self._sidebar, fg_color="#162818", corner_radius=12)
        usr.pack(padx=14, side="bottom", fill="x", pady=(0, 8))
        label(usr, "👤  Canteen Manager", size=12, weight="bold", color=WHITE).pack(padx=14, pady=(12, 2), anchor="w")
        label(usr, "manager@IndianArmy.mil", size=9, color="#6A8A6A").pack(padx=14, pady=(0, 12), anchor="w")

        # Content area
        right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        tricolor(right, 5)
        self._content = ctk.CTkFrame(right, fg_color=LIGHT, corner_radius=0)
        self._content.pack(fill="both", expand=True)

        self._navigate("dashboard")

    def _navigate(self, page):
        for p, b in self._nav_btns.items():
            if p == page:
                b.configure(fg_color=SAFFRON, text_color=ARMY_BG)
            else:
                b.configure(fg_color="transparent", text_color="#9DB89D")
        for w in self._content.winfo_children(): w.destroy()
        {"dashboard": self._page_dashboard,
         "sales":     self._page_sales,
         "inventory": self._page_inventory,
         "report":    self._page_report}[page]()

    def _page_header(self, title, subtitle=""):
        hf = ctk.CTkFrame(self._content, fg_color="transparent")
        hf.pack(fill="x", padx=30, pady=(22, 0))
        ctk.CTkFrame(hf, fg_color=SAFFRON, width=5, corner_radius=3).pack(
            side="left", fill="y", padx=(0, 12))
        label(hf, title, size=25, weight="bold", color=ARMY_BG).pack(side="left", pady=4)
        if subtitle:
            label(hf, subtitle, size=12, color=MID).pack(side="right", pady=8)
        return hf

    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    def _page_dashboard(self):
        self._page_header("Dashboard",
                          f"🇮🇳  {datetime.now().strftime('%d %B %Y  —  %A')}")

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            rows     = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
            inv_rows = conn.execute("SELECT * FROM inventory").fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in rows)
        total_cost = sum(r["cogs"] for r in rows)
        net_profit = total_rev - total_cost
        meals_sold = sum(r["sold"] for r in rows)
        low_items  = [i for i in inv_rows if i["stock"] < i["min_lvl"]]

        # ── Stat cards ────────────────────────────────────────────────────────
        cf = ctk.CTkFrame(self._content, fg_color="transparent")
        cf.pack(fill="x", padx=30, pady=16)
        for i, (lbl_t, val, color, icon) in enumerate([
                ("Total Revenue",    f"₹ {total_rev:,.0f}",  SAFFRON,   "💰"),
                ("Total COGS",       f"₹ {total_cost:,.0f}", PURPLE,    "🧾"),
                ("Net Profit",       f"₹ {net_profit:,.0f}", IND_GREEN, "📈"),
                ("Meals Served",     str(meals_sold),         BLUE,      "🍛"),
                ("Low Stock Alerts", str(len(low_items)),     RED,       "⚠️"),
        ]):
            c = ctk.CTkFrame(cf, fg_color=WHITE, corner_radius=14,
                             border_width=2, border_color=color + "44")
            c.grid(row=0, column=i, padx=5, sticky="nsew")
            cf.grid_columnconfigure(i, weight=1)
            ctk.CTkFrame(c, fg_color=color, height=4, corner_radius=0).pack(fill="x")
            label(c, icon, size=26).pack(pady=(14, 4), padx=16, anchor="w")
            label(c, val, size=20, weight="bold", color=color).pack(padx=16, anchor="w")
            label(c, lbl_t, size=11, color=MID).pack(padx=16, pady=(2, 16), anchor="w")

        # ── Bottom: sales table + alerts ──────────────────────────────────────
        bot = ctk.CTkFrame(self._content, fg_color="transparent")
        bot.pack(fill="both", expand=True, padx=30, pady=(0, 24))
        bot.grid_columnconfigure(0, weight=3)
        bot.grid_columnconfigure(1, weight=2)

        sc = card(bot)
        sc.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        army_band(sc, "📊  Today's Sales Breakdown")

        th = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0)
        th.pack(fill="x")
        for j, col in enumerate(["Meal", "Qty", "Rate", "Revenue", "Payment"]):
            label(th, col, size=11, weight="bold", color=MID).grid(
                row=0, column=j, padx=14, pady=8, sticky="w")
            th.grid_columnconfigure(j, weight=1)

        for idx, row in enumerate(rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg, corner_radius=0)
            rf.pack(fill="x")
            pi = {"Cash": "💵", "UPI": "📱", "Card": "💳"}.get(row["payment"], "💰")
            for j, val in enumerate([row["meal"], str(row["sold"]),
                                      f"₹{row['sp']:.0f}",
                                      f"₹{row['sp']*row['sold']:,.0f}",
                                      f"{pi} {row['payment']}"]):
                label(rf, val, size=12).grid(row=0, column=j, padx=14, pady=9, sticky="w")
                rf.grid_columnconfigure(j, weight=1)

        tr = ctk.CTkFrame(sc, fg_color="#FFF7ED", corner_radius=0)
        tr.pack(fill="x", pady=(2, 0))
        for j, (v, c2) in enumerate(zip(
                ["TOTAL", str(meals_sold), "", f"₹{total_rev:,.0f}", ""],
                [SAFFRON, SAFFRON, DARK, SAFFRON, DARK])):
            label(tr, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=14, pady=9, sticky="w")
            tr.grid_columnconfigure(j, weight=1)

        db_f = ctk.CTkFrame(sc, fg_color="#F0F4EE", corner_radius=0)
        db_f.pack(fill="x")
        label(db_f, f"💾  Stored in: canteen.db  (SQLite — {DB_PATH})",
              size=9, color="#94A3B8").pack(padx=14, pady=5, anchor="w")

        # Alerts card
        ac = card(bot)
        ac.grid(row=0, column=1, sticky="nsew")
        ahdr = ctk.CTkFrame(ac, fg_color=DRED, corner_radius=0, height=44)
        ahdr.pack(fill="x")
        ahdr.pack_propagate(False)
        label(ahdr, f"  ⚠️  Low Stock Alerts  ({len(low_items)} items)",
              size=12, weight="bold", color=WHITE).pack(side="left", padx=4, pady=10)

        isc = ctk.CTkScrollableFrame(ac, fg_color="transparent")
        isc.pack(fill="both", expand=True, padx=12, pady=12)
        if not low_items:
            label(isc, "✅  All items sufficiently stocked.", size=13, color=IND_GREEN).pack(pady=20)
        else:
            for item in low_items:
                rf2 = ctk.CTkFrame(isc, fg_color="#FEF2F2", corner_radius=10,
                                   border_width=1, border_color="#FECACA")
                rf2.pack(fill="x", pady=4)
                label(rf2, f"  {item['item']}", size=13, weight="bold",
                      color="#991B1B").pack(padx=10, pady=(10, 2), anchor="w")
                sf2 = ctk.CTkFrame(rf2, fg_color="transparent")
                sf2.pack(padx=10, pady=(0, 10), fill="x")
                label(sf2, f"Have: {item['stock']} {item['unit']}",
                      size=11, color=RED).pack(side="left")
                label(sf2, f"Min: {item['min_lvl']} {item['unit']}",
                      size=11, color=MID).pack(side="right")

        ctk.CTkButton(ac, text="🛒  Generate Shopping List",
                      height=44, corner_radius=0,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=RED, hover_color=DRED,
                      command=lambda: self._popup("🛒  Shopping List",
                          "\n".join(f"• {i['item']}  →  need {i['min_lvl']-i['stock']:.1f} {i['unit']}"
                                    for i in low_items) or "All stock sufficient!")
                      ).pack(fill="x", side="bottom")

    # ══════════════════════════════════════════════════════════════════════════
    # SALES ENTRY
    # ══════════════════════════════════════════════════════════════════════════
    def _page_sales(self):
        self._page_header("💰  Daily Sales Entry",
                          datetime.now().strftime("Date: %d %B %Y"))
        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=30, pady=(16, 24))

        sc = card(wrap)
        sc.pack(fill="x", pady=(0, 16))
        army_band(sc, "🍽  Meal Preparation & Sales Count")
        label(sc, "Enter quantities prepared, sold and wastage. Stock is auto-deducted on Save.",
              size=12, color=MID).pack(padx=20, pady=(12, 8), anchor="w")

        th = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0)
        th.pack(fill="x")
        for j, (col, wt) in enumerate(zip(
                ["Meal Item", "Qty Prepared", "Qty Sold", "Wastage"], [2, 1, 1, 1])):
            label(th, col, size=11, weight="bold", color=MID).grid(
                row=0, column=j, padx=16, pady=9, sticky="w")
            th.grid_columnconfigure(j, weight=wt)

        meals = ["Standard Lunch", "VIP Thali", "Tea",
                 "Snacks", "Breakfast", "Evening Snacks"]
        self._entries = {}
        for idx, meal in enumerate(meals):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg, corner_radius=0)
            rf.pack(fill="x")
            icon = ("🍛" if "Lunch" in meal or "Thali" in meal
                    else "☕" if "Tea" in meal
                    else "🌅" if "Break" in meal else "🍿")
            label(rf, f"  {icon}  {meal}", size=13, weight="bold").grid(
                row=0, column=0, padx=16, pady=11, sticky="w")
            rf.grid_columnconfigure(0, weight=2)
            entries = []
            for j, (ph, bc) in enumerate(
                    [("0", BORDER), ("0", BORDER), ("0", "#FCA5A5")], start=1):
                e = ctk.CTkEntry(rf, width=112, height=38, corner_radius=8,
                                 placeholder_text=ph,
                                 font=ctk.CTkFont(size=13), border_color=bc)
                e.grid(row=0, column=j, padx=16, pady=9, sticky="w")
                rf.grid_columnconfigure(j, weight=1)
                entries.append(e)
            self._entries[meal] = entries

        pc = card(wrap)
        pc.pack(fill="x", pady=(0, 16))
        army_band(pc, "💳  Payment Collection Breakdown")
        pay_f = ctk.CTkFrame(pc, fg_color="transparent")
        pay_f.pack(padx=20, fill="x", pady=16)
        for i, (mode, color, icon, bg_c) in enumerate([
                ("Cash", IND_GREEN, "💵", "#F0FDF4"),
                ("UPI",  PURPLE,    "📱", "#FAF5FF"),
                ("Card", BLUE,      "💳", "#EFF6FF")]):
            b = ctk.CTkFrame(pay_f, fg_color=bg_c, corner_radius=12,
                             border_width=1, border_color=color + "44")
            b.grid(row=0, column=i, padx=6, sticky="nsew")
            pay_f.grid_columnconfigure(i, weight=1)
            label(b, f"{icon}  {mode}", size=13, weight="bold",
                  color=color).pack(padx=16, pady=(16, 4), anchor="w")
            label(b, "Amount (₹)", size=10, color=MID).pack(padx=16, anchor="w")
            ctk.CTkEntry(b, height=44, placeholder_text="0.00",
                         corner_radius=8, font=ctk.CTkFont(size=16),
                         border_color=color).pack(padx=16, pady=(4, 16), fill="x")

        bf = ctk.CTkFrame(wrap, fg_color="transparent")
        bf.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(bf,
                      text="✅  Save & Auto-Deduct Stock  (→ canteen.db)",
                      height=54, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=IND_GREEN, hover_color=DGREEN,
                      command=lambda: self._popup(
                          "✅  Saved to Database!",
                          f"Sales recorded in  canteen.db\n"
                          "Inventory auto-deducted based on recipes.\n\n"
                          f"📁  {DB_PATH}")
                      ).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ctk.CTkButton(bf, text="📋  Preview Report",
                      height=54, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._navigate("report")
                      ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    # ══════════════════════════════════════════════════════════════════════════
    # INVENTORY
    # ══════════════════════════════════════════════════════════════════════════
    def _page_inventory(self):
        hf = self._page_header("📦  Inventory Ledger",
                               datetime.now().strftime("%d %B %Y"))
        ff = ctk.CTkFrame(hf, fg_color="transparent")
        ff.pack(side="right")
        for cat in ["All", "Dry", "Fresh", "Dairy", "Packaging"]:
            ctk.CTkButton(ff, text=cat, width=82, height=32, corner_radius=8,
                          font=ctk.CTkFont(size=12),
                          fg_color=ARMY_BG if cat == "All" else "#E8EFE8",
                          text_color=WHITE if cat == "All" else "#374151",
                          hover_color=ARMY_HVR,
                          command=lambda c=cat: self._filter_inv(c)
                          ).pack(side="left", padx=3)

        bf2 = ctk.CTkFrame(self._content, fg_color="transparent")
        bf2.pack(fill="x", padx=30, pady=(12, 0))
        ctk.CTkButton(bf2, text="+ Add Received Stock",
                      height=40, width=200, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=IND_GREEN, hover_color=DGREEN,
                      command=lambda: self._popup(
                          "Add Stock",
                          f"Stock receipt saved to:\ncanteen.db  (inventory table)\n"
                          "(Full entry form available in production build.)")
                      ).pack(side="left")
        ctk.CTkButton(bf2, text="🔧  Manual Adjustment",
                      height=40, width=180, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=PURPLE, hover_color="#6D28D9",
                      command=lambda: self._popup(
                          "Manual Adjustment",
                          "Admin-only feature.\nAdjustment + reason saved to canteen.db.")
                      ).pack(side="left", padx=10)

        tc = card(self._content, corner_radius=14)
        tc.pack(fill="both", expand=True, padx=30, pady=14)

        cols = ["Item", "Category", "Unit", "Opening",
                "Received", "Used", "Closing Stock", "Status"]
        wts  = [3, 1, 1, 1, 1, 1, 2, 2]
        thead = ctk.CTkFrame(tc, fg_color=ARMY_BG, corner_radius=0)
        thead.pack(fill="x")
        for j, (col, wt) in enumerate(zip(cols, wts)):
            label(thead, col, size=11, weight="bold", color=GOLD_LT).grid(
                row=0, column=j, padx=14, pady=10, sticky="w")
            thead.grid_columnconfigure(j, weight=wt)

        self._inv_scroll = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_scroll.pack(fill="both", expand=True)

        with get_db() as conn:
            data = conn.execute("SELECT * FROM inventory").fetchall()
        self._render_inv_rows(list(data))

    def _filter_inv(self, cat):
        for w in self._inv_scroll.winfo_children(): w.destroy()
        with get_db() as conn:
            if cat == "All":
                data = conn.execute("SELECT * FROM inventory").fetchall()
            else:
                data = conn.execute(
                    "SELECT * FROM inventory WHERE cat=?", (cat,)).fetchall()
        self._render_inv_rows(list(data))

    def _render_inv_rows(self, data):
        wts = [3, 1, 1, 1, 1, 1, 2, 2]
        cat_icons = {"Dry": "🌾", "Fresh": "🥦", "Dairy": "🥛", "Packaging": "📦"}
        for idx, item in enumerate(data):
            is_low = item["stock"] < item["min_lvl"]
            used   = item["opening"] + item["received"] - item["stock"]
            bg     = "#FFF5F5" if is_low else (WHITE if idx % 2 == 0 else STRIPE)
            rf = ctk.CTkFrame(self._inv_scroll, fg_color=bg, corner_radius=0)
            rf.pack(fill="x")
            ci = cat_icons.get(item["cat"], "•")
            vals   = [f"  {item['item']}", f"{ci} {item['cat']}", item["unit"],
                      f"{item['opening']:.1f}", f"+{item['received']:.1f}", f"{used:.1f}",
                      f"{item['stock']:.1f} {item['unit']}",
                      "⚠️  LOW STOCK" if is_low else "✓  OK"]
            colors = [DARK, MID, MID, DARK,
                      IND_GREEN if item["received"] > 0 else MID,
                      PURPLE, RED if is_low else IND_GREEN,
                      RED if is_low else IND_GREEN]
            bolds  = [True, False, False, False, False, False, True, True]
            for j, (v, c, bo) in enumerate(zip(vals, colors, bolds)):
                label(rf, v, size=12,
                      weight="bold" if bo else "normal", color=c).grid(
                          row=0, column=j, padx=14, pady=10, sticky="w")
                rf.grid_columnconfigure(j, weight=wts[j])

    # ══════════════════════════════════════════════════════════════════════════
    # DAILY REPORT
    # ══════════════════════════════════════════════════════════════════════════
    def _page_report(self):
        hf = self._page_header("📋  Daily Operations Report",
                               datetime.now().strftime("%d %B %Y"))
        ctk.CTkButton(hf, text="🖨  Export PDF",
                      height=40, width=160, corner_radius=8,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._popup(
                          "PDF Exported",
                          "Canteen_Report_" + datetime.now().strftime("%d%m%Y") + ".pdf\n"
                          f"Saved to: {os.path.dirname(DB_PATH)}")
                      ).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=(16, 24))

        rc = card(scroll)
        rc.pack(fill="x", pady=(0, 14))

        # Report header with tricolor
        rhdr = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=100)
        rhdr.pack(fill="x")
        rhdr.pack_propagate(False)
        tricolor(rhdr, 5)
        ih = ctk.CTkFrame(rhdr, fg_color="transparent")
        ih.pack(expand=True)
        label(ih, "🇮🇳  INDIAN ARMY — CANTEEN DAILY REPORT",
              size=17, weight="bold", color=WHITE).pack(pady=(10, 2))
        label(ih, f"Date: {datetime.now().strftime('%d %B %Y')}   "
              "•   Unit: 56 APO Field Canteen   •   Confidential",
              size=11, color=GOLD).pack(pady=(0, 12))

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            s_rows = conn.execute(
                "SELECT * FROM sales WHERE date=?", (today,)).fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in s_rows)
        total_cogs = sum(r["cogs"] for r in s_rows)
        net_profit = total_rev - total_cogs
        meals_tot  = sum(r["sold"] for r in s_rows)

        def sec_title(txt):
            sf3 = ctk.CTkFrame(rc, fg_color="transparent")
            sf3.pack(fill="x", padx=24, pady=(16, 8))
            ctk.CTkFrame(sf3, fg_color=SAFFRON, width=4,
                         corner_radius=2).pack(side="left", fill="y", padx=(0, 10))
            label(sf3, txt, size=13, weight="bold", color=ARMY_BG).pack(side="left")

        sec_title("1.  Meal Sales Summary")
        th = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=0)
        th.pack(fill="x", padx=24)
        for j, col in enumerate(["Meal Item", "Sold", "Rate (₹)",
                                  "Revenue (₹)", "Payment"]):
            label(th, col, size=11, weight="bold", color=MID).grid(
                row=0, column=j, padx=14, pady=9, sticky="w")
            th.grid_columnconfigure(j, weight=1)

        for idx, row in enumerate(s_rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf2 = ctk.CTkFrame(rc, fg_color=bg, corner_radius=0)
            rf2.pack(fill="x", padx=24)
            pi = {"Cash": "💵", "UPI": "📱", "Card": "💳"}.get(row["payment"], "💰")
            for j, val in enumerate([
                    row["meal"], str(row["sold"]),
                    f"{row['sp']:.0f}",
                    f"{row['sp']*row['sold']:,.0f}",
                    f"{pi} {row['payment']}"]):
                label(rf2, val, size=12).grid(
                    row=0, column=j, padx=14, pady=9, sticky="w")
                rf2.grid_columnconfigure(j, weight=1)

        tot_row = ctk.CTkFrame(rc, fg_color="#FFF7ED", corner_radius=0)
        tot_row.pack(fill="x", padx=24, pady=(2, 0))
        for j, (v, c2) in enumerate(zip(
                ["TOTAL", str(meals_tot), "", f"{total_rev:,.0f}", ""],
                [SAFFRON, SAFFRON, DARK, SAFFRON, DARK])):
            label(tot_row, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=14, pady=10, sticky="w")
            tot_row.grid_columnconfigure(j, weight=1)

        sec_title("2.  Financial Summary")
        for lbl_txt, val, color in [
                ("Total Revenue (Sales Income)", f"₹ {total_rev:,.0f}",  IND_GREEN),
                ("Total COGS (Ingredient Cost)", f"₹ {total_cogs:,.0f}", RED),
                ("Net Daily Profit",             f"₹ {net_profit:,.0f}", SAFFRON)]:
            fr = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=10)
            fr.pack(padx=24, fill="x", pady=4)
            label(fr, f"  {lbl_txt}", size=12).pack(side="left", padx=14, pady=14)
            label(fr, val, size=16, weight="bold", color=color).pack(
                side="right", padx=18)

        sec_title("3.  Payment Mode Breakdown")
        pf2 = ctk.CTkFrame(rc, fg_color="transparent")
        pf2.pack(padx=24, fill="x", pady=(0, 4))
        cash_a = sum(r["sp"] * r["sold"] for r in s_rows if r["payment"] == "Cash")
        upi_a  = sum(r["sp"] * r["sold"] for r in s_rows if r["payment"] == "UPI")
        card_a = sum(r["sp"] * r["sold"] for r in s_rows if r["payment"] == "Card")
        for i, (mode, amt, color, bg_c) in enumerate([
                ("💵  Cash", f"₹ {cash_a:,.0f}", IND_GREEN, "#F0FDF4"),
                ("📱  UPI",  f"₹ {upi_a:,.0f}",  PURPLE,    "#FAF5FF"),
                ("💳  Card", f"₹ {card_a:,.0f}",  BLUE,      "#EFF6FF")]):
            b = ctk.CTkFrame(pf2, fg_color=bg_c, corner_radius=12,
                             border_width=1, border_color=color + "44")
            b.grid(row=0, column=i, padx=6, sticky="nsew")
            pf2.grid_columnconfigure(i, weight=1)
            label(b, mode, size=12, weight="bold", color=color).pack(
                padx=16, pady=(14, 4), anchor="w")
            label(b, amt, size=18, weight="bold", color=color).pack(
                padx=16, pady=(0, 14), anchor="w")

        sec_title("4.  Official Sign-off")
        sig_f = ctk.CTkFrame(rc, fg_color="transparent")
        sig_f.pack(padx=24, fill="x", pady=(0, 24))
        for i, (role, name, rank) in enumerate([
                ("Prepared By",  "Canteen Manager",     "JCO / OR"),
                ("Checked By",   "Supervision Officer", "Subedar"),
                ("Approved By",  "Officer-in-Charge",   "Captain / Lt")]):
            b = ctk.CTkFrame(sig_f, fg_color="#F9FAFB", corner_radius=12,
                             border_width=1, border_color=BORDER)
            b.grid(row=0, column=i, padx=8, sticky="nsew")
            sig_f.grid_columnconfigure(i, weight=1)
            label(b, role, size=10, weight="bold", color=MID).pack(
                padx=18, pady=(16, 44), anchor="w")
            ctk.CTkFrame(b, height=2, fg_color=ARMY_BG).pack(fill="x", padx=18)
            label(b, name, size=12, weight="bold", color=ARMY_BG).pack(
                padx=18, pady=(6, 2), anchor="w")
            label(b, rank, size=10, color=MID).pack(
                padx=18, pady=(0, 14), anchor="w")

        # Tricolor footer strip
        foot = ctk.CTkFrame(rc, height=6, fg_color="transparent")
        foot.pack(fill="x")
        foot.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(foot, fg_color=c).pack(side="left", fill="y", expand=True)
        label(rc, "जय हिन्द  •  जय जवान  •  जय किसान",
              size=11, color=MID).pack(pady=(8, 16))

    # ── Popup (with mini tricolor) ─────────────────────────────────────────────
    def _popup(self, title, message):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("490x290")
        win.resizable(False, False)
        win.grab_set()
        win.lift()
        win.configure(fg_color=WHITE)

        ts = ctk.CTkFrame(win, height=5, fg_color="transparent")
        ts.pack(fill="x")
        ts.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ts, fg_color=c).pack(side="left", fill="y", expand=True)

        icon = "✅" if any(x in title for x in ["Saved", "Export", "List"]) else "ℹ️"
        label(win, icon, size=38).pack(pady=(20, 6))
        label(win, message, size=12, color=DARK,
              justify="center", wraplength=440).pack(pady=(0, 18))
        ctk.CTkButton(win, text="OK", width=130, height=42, corner_radius=10,
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=win.destroy).pack()
        label(win, "जय हिन्द", size=10, color=MID).pack(pady=(10, 16))


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CanteenApp()
    app.mainloop()
'''

out = os.path.join(os.path.dirname(__file__), "app.py")
with open(out, "w", encoding="utf-8") as f:
    f.write(NEW_CONTENT)
print(f"Written {len(NEW_CONTENT)} chars to {out}")
