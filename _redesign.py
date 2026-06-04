"""Writer script — overwrites app.py with redesigned version."""
code = r'''"""
Canteen Inventory & Sales Management System
Indian Army — Demo Application  |  Python + CustomTkinter + SQLite
"""

import customtkinter as ctk
from datetime import datetime
import sqlite3, os

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canteen.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL, cat TEXT NOT NULL, unit TEXT NOT NULL,
                stock REAL NOT NULL DEFAULT 0, min_lvl REAL NOT NULL DEFAULT 0,
                opening REAL NOT NULL DEFAULT 0, received REAL NOT NULL DEFAULT 0,
                updated TEXT DEFAULT CURRENT_DATE
            );
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                meal TEXT NOT NULL, sp REAL NOT NULL,
                sold INTEGER NOT NULL DEFAULT 0, cogs REAL NOT NULL DEFAULT 0,
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

# ── Theme ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Color Palette ─────────────────────────────────────────────────────────────
SAFFRON   = "#FF9933"
IND_GREEN = "#138808"
GOLD      = "#C9A84C"
GOLD_LT   = "#EDD97A"

ARMY_BG  = "#1F3320"
ARMY_HVR = "#2C4A2A"
ARMY_SEP = "#2E4830"

DARK   = "#1E293B"
MID    = "#64748B"
LIGHT  = "#F1F5F1"
WHITE  = "#FFFFFF"
BORDER = "#E2EAE2"
STRIPE = "#F8FAF8"

GREEN  = "#059669";  DGREEN  = "#047857"
RED    = "#DC2626";  DRED    = "#B91C1C"
BLUE   = "#2563EB";  DBLUE   = "#1D4ED8"
PURPLE = "#7C3AED"

# Safe 6-digit tint colors (no alpha — Tkinter-safe)
T_SAFFRON = "#FFD4A8"
T_GREEN   = "#A7F3D0"
T_BLUE    = "#BFDBFE"
T_PURPLE  = "#DDD6FE"
T_RED     = "#FECACA"

BG_SAFFRON = "#FFF7ED"
BG_GREEN   = "#F0FDF4"
BG_BLUE    = "#EFF6FF"
BG_PURPLE  = "#FAF5FF"
BG_RED     = "#FEF2F2"

# ── Helpers ───────────────────────────────────────────────────────────────────
def card(parent, **kw):
    d = dict(fg_color=WHITE, corner_radius=16, border_width=1, border_color=BORDER)
    d.update(kw)
    return ctk.CTkFrame(parent, **d)

def lbl(parent, text, size=13, weight="normal", color=DARK, **kw):
    return ctk.CTkLabel(parent, text=text,
                        font=ctk.CTkFont(size=size, weight=weight),
                        text_color=color, **kw)

def tricolor(parent, h=5):
    bar = ctk.CTkFrame(parent, fg_color="transparent", height=h)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    for c in (SAFFRON, WHITE, IND_GREEN):
        ctk.CTkFrame(bar, fg_color=c).pack(side="left", fill="both", expand=True)

def section_band(parent, text, height=48):
    """Army-green card header with saffron left accent and gold text."""
    hdr = ctk.CTkFrame(parent, fg_color=ARMY_BG, corner_radius=0, height=height)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkFrame(hdr, fg_color=SAFFRON, width=5, corner_radius=0).pack(side="left", fill="y")
    lbl(hdr, f"  {text}", size=12, weight="bold", color=GOLD_LT).pack(
        side="left", padx=10, pady=10)

# ═════════════════════════════════════════════════════════════════════════════
class CanteenApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Indian Army Canteen Management System")
        self.geometry("1340x820")
        self.minsize(1100, 700)
        self.configure(fg_color=LIGHT)
        self._show_login()

    # ── Login ─────────────────────────────────────────────────────────────────
    def _show_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color="#EDF3ED")

        strip = ctk.CTkFrame(self, height=7, fg_color="transparent")
        strip.pack(fill="x", side="top")
        strip.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(strip, fg_color=c).pack(side="left", fill="both", expand=True)

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        box = ctk.CTkFrame(outer, fg_color=WHITE, corner_radius=24,
                           border_width=2, border_color=BORDER)
        box.pack()

        hdr = ctk.CTkFrame(box, fg_color=ARMY_BG, corner_radius=0, height=138, width=440)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tricolor(hdr, 4)
        lbl(hdr, "🇮🇳  INDIAN ARMY", size=11, weight="bold", color=GOLD_LT).pack(pady=(14, 0))
        lbl(hdr, "CANTEEN MANAGEMENT SYSTEM", size=19, weight="bold", color=WHITE).pack(pady=(4, 0))
        lbl(hdr, "सेवा परमो धर्म  •  Service Before Self", size=10, color=GOLD).pack(pady=(4, 14))

        lbl(box, "Staff / Officer Login", size=15, weight="bold",
            color=ARMY_BG).pack(pady=(28, 20))

        for field_lbl, attr, ph, show in [
            ("Username", "_uname", "Enter username", ""),
            ("Password", "_pwd",   "Enter password", "●"),
        ]:
            lbl(box, field_lbl, size=12, weight="bold",
                color="#374151", anchor="w").pack(padx=46, fill="x", pady=(0, 4))
            e = ctk.CTkEntry(box, width=350, height=48, corner_radius=10,
                             placeholder_text=ph, show=show,
                             font=ctk.CTkFont(size=14), border_color="#CBD5E1")
            e.pack(padx=42, pady=(0, 14))
            setattr(self, attr, e)

        self._uname.insert(0, "manager")
        self._pwd.insert(0, "1234")
        self._pwd.bind("<Return>", lambda e: self._do_login())

        ctk.CTkButton(box, text="🔐  Login to System", width=350, height=54,
                      corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=self._do_login).pack(padx=42, pady=(0, 14))

        self._login_err = lbl(box, "", size=12, color=RED)
        self._login_err.pack()

        foot_strip = ctk.CTkFrame(box, height=5, fg_color="transparent", width=440)
        foot_strip.pack(fill="x", pady=(14, 0))
        foot_strip.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(foot_strip, fg_color=c).pack(side="left", fill="both", expand=True)
        lbl(box, "जय हिन्द  •  Demo v2.0  •  SQLite Powered",
            size=10, color="#94A3B8").pack(pady=(8, 22))

    def _do_login(self):
        if self._uname.get().strip() == "manager" and self._pwd.get() == "1234":
            self._show_main()
        else:
            self._login_err.configure(text="⚠  Invalid credentials. Use  manager / 1234")

    # ── Main Shell ────────────────────────────────────────────────────────────
    def _show_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=LIGHT)

        # Sidebar
        sb = ctk.CTkFrame(self, fg_color=ARMY_BG, width=264, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        self._sidebar = sb
        tricolor(sb, 5)

        lg = ctk.CTkFrame(sb, fg_color="transparent")
        lg.pack(fill="x", padx=18, pady=(16, 4))
        lbl(lg, "🇮🇳", size=36).pack(side="left", padx=(0, 12))
        tf = ctk.CTkFrame(lg, fg_color="transparent")
        tf.pack(side="left")
        lbl(tf, "INDIAN ARMY", size=13, weight="bold", color=GOLD).pack(anchor="w")
        lbl(tf, "Canteen Management", size=10, color="#8AA88A").pack(anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(fill="x", padx=18, pady=12)

        uc = ctk.CTkFrame(sb, fg_color="#162818", corner_radius=12)
        uc.pack(padx=14, fill="x", pady=(0, 16))
        lbl(uc, "⭐  Unit / Establishment", size=10, color=GOLD).pack(padx=14, pady=(10, 2), anchor="w")
        lbl(uc, "56 APO Field Canteen", size=12, weight="bold", color=WHITE).pack(padx=14, anchor="w")
        lbl(uc, "Est. 1947  •  Serving with Pride", size=9, color="#8AA88A").pack(
            padx=14, pady=(2, 10), anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(fill="x", padx=18, pady=(0, 10))

        self._nav_btns = {}
        for icon_txt, page in [
            ("📊   Dashboard",    "dashboard"),
            ("💰   Sales Entry",  "sales"),
            ("📦   Inventory",    "inventory"),
            ("📋   Daily Report", "report"),
        ]:
            b = ctk.CTkButton(sb, text=icon_txt, anchor="w", height=50,
                              font=ctk.CTkFont(size=14), fg_color="transparent",
                              hover_color=ARMY_HVR, text_color="#9DB89D",
                              corner_radius=10,
                              command=lambda p=page: self._navigate(p))
            b.pack(padx=14, pady=3, fill="x")
            self._nav_btns[page] = b

        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(
            fill="x", padx=18, side="bottom", pady=(10, 6))
        ctk.CTkButton(sb, text="⬅  Logout", height=44, anchor="w",
                      fg_color="transparent", hover_color=ARMY_HVR,
                      text_color="#688068", font=ctk.CTkFont(size=13),
                      corner_radius=10,
                      command=self._show_login).pack(padx=14, pady=(0, 12), fill="x", side="bottom")

        usr = ctk.CTkFrame(sb, fg_color="#162818", corner_radius=12)
        usr.pack(padx=14, side="bottom", fill="x", pady=(0, 10))
        lbl(usr, "👤  Canteen Manager", size=12, weight="bold",
            color=WHITE).pack(padx=14, pady=(12, 2), anchor="w")
        lbl(usr, "manager@IndianArmy.mil", size=9,
            color="#6A8A6A").pack(padx=14, pady=(0, 12), anchor="w")

        right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        tricolor(right, 5)
        self._content = ctk.CTkFrame(right, fg_color=LIGHT, corner_radius=0)
        self._content.pack(fill="both", expand=True)

        self._navigate("dashboard")

    def _navigate(self, page):
        for p, b in self._nav_btns.items():
            if p == page:
                b.configure(fg_color=SAFFRON, text_color=ARMY_BG,
                            font=ctk.CTkFont(size=14, weight="bold"))
            else:
                b.configure(fg_color="transparent", text_color="#9DB89D",
                            font=ctk.CTkFont(size=14))
        for w in self._content.winfo_children(): w.destroy()
        {"dashboard": self._page_dashboard,
         "sales":     self._page_sales,
         "inventory": self._page_inventory,
         "report":    self._page_report}[page]()

    def _page_header(self, title, subtitle=""):
        hf = ctk.CTkFrame(self._content, fg_color="transparent")
        hf.pack(fill="x", padx=28, pady=(20, 0))
        acc = ctk.CTkFrame(hf, fg_color=SAFFRON, width=5, corner_radius=3)
        acc.pack(side="left", fill="y", padx=(0, 14))
        txt_col = ctk.CTkFrame(hf, fg_color="transparent")
        txt_col.pack(side="left", fill="y", pady=4)
        lbl(txt_col, title, size=24, weight="bold", color=ARMY_BG).pack(anchor="w")
        if subtitle:
            lbl(txt_col, subtitle, size=11, color=MID).pack(anchor="w", pady=(2, 0))
        return hf

    # ═════════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ═════════════════════════════════════════════════════════════════════════
    def _page_dashboard(self):
        today_str = datetime.now().strftime("%A, %d %B %Y")
        self._page_header("Dashboard", f"🇮🇳  {today_str}  ·  56 APO Field Canteen")

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            rows     = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
            inv_rows = conn.execute("SELECT * FROM inventory").fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in rows)
        total_cost = sum(r["cogs"] for r in rows)
        net_profit = total_rev - total_cost
        meals_sold = sum(r["sold"] for r in rows)
        low_items  = [i for i in inv_rows if i["stock"] < i["min_lvl"]]

        # ── KPI Cards ─────────────────────────────────────────────────────────
        cf = ctk.CTkFrame(self._content, fg_color="transparent")
        cf.pack(fill="x", padx=28, pady=(18, 0))
        cf.grid_rowconfigure(0, weight=1)

        kpi = [
            ("💰", "Total Revenue",   f"₹ {total_rev:,.0f}",  SAFFRON, BG_SAFFRON, T_SAFFRON),
            ("🧾", "Total COGS",      f"₹ {total_cost:,.0f}", PURPLE,  BG_PURPLE,  T_PURPLE),
            ("📈", "Net Profit",      f"₹ {net_profit:,.0f}", GREEN,   BG_GREEN,   T_GREEN),
            ("🍛", "Meals Served",    str(meals_sold),         BLUE,    BG_BLUE,    T_BLUE),
            ("⚠️", "Low Stock Items", str(len(low_items)),     RED,     BG_RED,     T_RED),
        ]
        for i, (icon, title, value, color, bg, border) in enumerate(kpi):
            c = ctk.CTkFrame(cf, fg_color=WHITE, corner_radius=16,
                             border_width=1, border_color=border)
            c.grid(row=0, column=i, padx=5, sticky="nsew")
            cf.grid_columnconfigure(i, weight=1)

            ctk.CTkFrame(c, fg_color=color, height=4, corner_radius=0).pack(fill="x")

            inner = ctk.CTkFrame(c, fg_color="transparent")
            inner.pack(fill="both", padx=16, pady=14)

            # Icon in colored bubble
            icon_f = ctk.CTkFrame(inner, fg_color=bg, corner_radius=12, width=48, height=48)
            icon_f.pack(anchor="w")
            icon_f.pack_propagate(False)
            lbl(icon_f, icon, size=20).place(relx=0.5, rely=0.5, anchor="center")

            lbl(inner, value, size=22, weight="bold", color=color).pack(
                anchor="w", pady=(10, 1))
            lbl(inner, title, size=11, color=MID).pack(anchor="w", pady=(0, 4))

        # ── Bottom: sales table + alerts ──────────────────────────────────────
        bot = ctk.CTkFrame(self._content, fg_color="transparent")
        bot.pack(fill="both", expand=True, padx=28, pady=16)
        bot.grid_columnconfigure(0, weight=6)
        bot.grid_columnconfigure(1, weight=4)
        bot.grid_rowconfigure(0, weight=1)

        # Sales card
        sc = card(bot, corner_radius=16)
        sc.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        section_band(sc, "📊  Today's Sales Breakdown")

        th = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0)
        th.pack(fill="x", padx=2)
        col_wts = [3, 1, 1, 2, 2]
        for j, (col, wt) in enumerate(zip(
                ["Meal Item", "Qty", "Rate", "Revenue", "Payment"], col_wts)):
            lbl(th, col, size=11, weight="bold", color=MID).grid(
                row=0, column=j, padx=14, pady=9, sticky="w")
            th.grid_columnconfigure(j, weight=wt)

        for idx, row in enumerate(rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg, corner_radius=0)
            rf.pack(fill="x", padx=2)
            pi = {"Cash": "💵", "UPI": "📱", "Card": "💳"}.get(row["payment"], "💰")
            for j, (val, wt) in enumerate(zip(
                    [row["meal"], str(row["sold"]), f"₹{row['sp']:.0f}",
                     f"₹{row['sp']*row['sold']:,.0f}", f"{pi} {row['payment']}"],
                    col_wts)):
                lbl(rf, val, size=12).grid(row=0, column=j, padx=14, pady=10, sticky="w")
                rf.grid_columnconfigure(j, weight=wt)

        tr = ctk.CTkFrame(sc, fg_color="#FFF7ED", corner_radius=0)
        tr.pack(fill="x", padx=2, pady=(2, 0))
        for j, (v, c2, wt) in enumerate(zip(
                ["TOTAL", str(meals_sold), "", f"₹{total_rev:,.0f}", ""],
                [SAFFRON, MID, DARK, SAFFRON, DARK],
                col_wts)):
            lbl(tr, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=14, pady=10, sticky="w")
            tr.grid_columnconfigure(j, weight=wt)

        footer_f = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0)
        footer_f.pack(fill="x", padx=2)
        lbl(footer_f, "💾  SQLite · canteen.db  (persistent local storage)",
            size=9, color="#94A3B8").pack(padx=14, pady=6, anchor="w")

        # Alerts card
        ac = card(bot, corner_radius=16)
        ac.grid(row=0, column=1, sticky="nsew")

        ahdr = ctk.CTkFrame(ac, fg_color=DRED, corner_radius=0, height=48)
        ahdr.pack(fill="x")
        ahdr.pack_propagate(False)
        ctk.CTkFrame(ahdr, fg_color=SAFFRON, width=5, corner_radius=0).pack(side="left", fill="y")
        lbl(ahdr, f"  ⚠️  Low Stock  ({len(low_items)} items)",
            size=12, weight="bold", color=WHITE).pack(side="left", padx=10, pady=10)

        isc = ctk.CTkScrollableFrame(ac, fg_color="transparent")
        isc.pack(fill="both", expand=True, padx=10, pady=10)

        if not low_items:
            lbl(isc, "✅  All items sufficiently stocked.",
                size=12, color=GREEN).pack(pady=28)
        else:
            for item in low_items:
                rf2 = ctk.CTkFrame(isc, fg_color=BG_RED, corner_radius=10,
                                   border_width=1, border_color=T_RED)
                rf2.pack(fill="x", pady=4)
                lbl(rf2, f"  {item['item']}", size=13, weight="bold",
                    color="#991B1B").pack(padx=10, pady=(10, 2), anchor="w")
                sf2 = ctk.CTkFrame(rf2, fg_color="transparent")
                sf2.pack(padx=10, pady=(0, 10), fill="x")
                lbl(sf2, f"Have: {item['stock']} {item['unit']}",
                    size=11, color=RED).pack(side="left")
                lbl(sf2, f"Min: {item['min_lvl']} {item['unit']}",
                    size=11, color=MID).pack(side="right")

        ctk.CTkButton(ac, text="🛒  Generate Shopping List",
                      height=44, corner_radius=0,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=RED, hover_color=DRED,
                      command=lambda: self._popup(
                          "🛒  Shopping List",
                          "\n".join(
                              f"• {i['item']}  →  need {i['min_lvl']-i['stock']:.1f} {i['unit']}"
                              for i in low_items) or "All stock sufficient!")
                      ).pack(fill="x", side="bottom")

    # ═════════════════════════════════════════════════════════════════════════
    # SALES ENTRY
    # ═════════════════════════════════════════════════════════════════════════
    def _page_sales(self):
        self._page_header("💰  Daily Sales Entry",
                          datetime.now().strftime("📅  %d %B %Y"))
        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=28, pady=(16, 24))

        sc = card(wrap, corner_radius=16)
        sc.pack(fill="x", pady=(0, 16))
        section_band(sc, "🍽  Meal Preparation & Sales Count")
        lbl(sc, "  Enter quantities prepared, sold and wastage for each meal item.",
            size=12, color=MID).pack(padx=16, pady=(10, 6), anchor="w")

        th = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0)
        th.pack(fill="x")
        for j, (col, wt) in enumerate(zip(
                ["Meal Item", "Qty Prepared", "Qty Sold", "Wastage"], [3, 1, 1, 1])):
            lbl(th, col, size=11, weight="bold", color=MID).grid(
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
            lbl(rf, f"  {icon}  {meal}", size=13, weight="bold",
                color=DARK).grid(row=0, column=0, padx=16, pady=11, sticky="w")
            rf.grid_columnconfigure(0, weight=3)
            entries = []
            for j, (ph, bc) in enumerate(
                    [("0", BORDER), ("0", BORDER), ("0", T_RED)], start=1):
                e = ctk.CTkEntry(rf, width=110, height=38, corner_radius=8,
                                 placeholder_text=ph,
                                 font=ctk.CTkFont(size=13), border_color=bc)
                e.grid(row=0, column=j, padx=16, pady=9, sticky="w")
                rf.grid_columnconfigure(j, weight=1)
                entries.append(e)
            self._entries[meal] = entries

        pc = card(wrap, corner_radius=16)
        pc.pack(fill="x", pady=(0, 16))
        section_band(pc, "💳  Payment Collection Breakdown")
        pay_f = ctk.CTkFrame(pc, fg_color="transparent")
        pay_f.pack(padx=20, fill="x", pady=18)
        pay_f.grid_rowconfigure(0, weight=1)

        for i, (mode, color, icon, bg_c, border_c) in enumerate([
                ("Cash", GREEN,  "💵", BG_GREEN,  T_GREEN),
                ("UPI",  PURPLE, "📱", BG_PURPLE, T_PURPLE),
                ("Card", BLUE,   "💳", BG_BLUE,   T_BLUE)]):
            b = ctk.CTkFrame(pay_f, fg_color=bg_c, corner_radius=14,
                             border_width=1, border_color=border_c)
            b.grid(row=0, column=i, padx=6, sticky="nsew")
            pay_f.grid_columnconfigure(i, weight=1)
            hrow = ctk.CTkFrame(b, fg_color="transparent")
            hrow.pack(fill="x", padx=16, pady=(16, 4))
            ib = ctk.CTkFrame(hrow, fg_color=color, corner_radius=8, width=36, height=36)
            ib.pack(side="left", padx=(0, 10))
            ib.pack_propagate(False)
            lbl(ib, icon, size=16, color=WHITE).place(relx=0.5, rely=0.5, anchor="center")
            lbl(hrow, mode, size=14, weight="bold", color=color).pack(side="left", pady=6)
            lbl(b, "Amount (₹)", size=10, color=MID).pack(padx=16, anchor="w")
            ctk.CTkEntry(b, height=46, placeholder_text="0.00",
                         corner_radius=10, font=ctk.CTkFont(size=17),
                         border_color=border_c).pack(padx=16, pady=(4, 18), fill="x")

        bf = ctk.CTkFrame(wrap, fg_color="transparent")
        bf.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(bf, text="✅  Save & Auto-Deduct Stock",
                      height=54, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=lambda: self._popup(
                          "✅  Saved to Database!",
                          "Sales recorded in canteen.db\n"
                          "Inventory auto-deducted based on recipes.")
                      ).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ctk.CTkButton(bf, text="📋  Preview Report",
                      height=54, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._navigate("report")
                      ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    # ═════════════════════════════════════════════════════════════════════════
    # INVENTORY
    # ═════════════════════════════════════════════════════════════════════════
    def _page_inventory(self):
        hf = self._page_header("📦  Inventory Ledger",
                               datetime.now().strftime("📅  %d %B %Y"))
        ff = ctk.CTkFrame(hf, fg_color="transparent")
        ff.pack(side="right", anchor="e")
        self._filter_btns = {}
        for cat in ["All", "Dry", "Fresh", "Dairy", "Packaging"]:
            b = ctk.CTkButton(ff, text=cat, width=80, height=32, corner_radius=8,
                              font=ctk.CTkFont(size=12),
                              fg_color=ARMY_BG if cat == "All" else STRIPE,
                              text_color=WHITE if cat == "All" else DARK,
                              hover_color=ARMY_HVR,
                              command=lambda c=cat: self._filter_inv(c))
            b.pack(side="left", padx=3)
            self._filter_btns[cat] = b

        bf2 = ctk.CTkFrame(self._content, fg_color="transparent")
        bf2.pack(fill="x", padx=28, pady=(12, 0))
        ctk.CTkButton(bf2, text="+ Add Received Stock",
                      height=40, width=200, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=lambda: self._popup(
                          "Add Stock",
                          "Stock receipt saved to canteen.db\n"
                          "(Full entry form in production build.)")
                      ).pack(side="left")
        ctk.CTkButton(bf2, text="🔧  Manual Adjustment",
                      height=40, width=180, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=PURPLE, hover_color="#6D28D9",
                      command=lambda: self._popup(
                          "Manual Adjustment",
                          "Admin-only.\nAdjustment + reason saved to canteen.db.")
                      ).pack(side="left", padx=10)

        tc = card(self._content, corner_radius=16)
        tc.pack(fill="both", expand=True, padx=28, pady=14)

        cols = ["Item", "Category", "Unit", "Opening",
                "Received", "Used", "Closing Stock", "Status"]
        wts  = [3, 1, 1, 1, 1, 1, 2, 2]
        thead = ctk.CTkFrame(tc, fg_color=ARMY_BG, corner_radius=0)
        thead.pack(fill="x")
        for j, (col, wt) in enumerate(zip(cols, wts)):
            lbl(thead, col, size=11, weight="bold", color=GOLD_LT).grid(
                row=0, column=j, padx=14, pady=11, sticky="w")
            thead.grid_columnconfigure(j, weight=wt)

        self._inv_scroll = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_scroll.pack(fill="both", expand=True)

        with get_db() as conn:
            data = conn.execute("SELECT * FROM inventory").fetchall()
        self._render_inv_rows(list(data))

    def _filter_inv(self, cat):
        for c, b in self._filter_btns.items():
            b.configure(fg_color=ARMY_BG if c == cat else STRIPE,
                        text_color=WHITE if c == cat else DARK)
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
            bg     = BG_RED if is_low else (WHITE if idx % 2 == 0 else STRIPE)
            rf = ctk.CTkFrame(self._inv_scroll, fg_color=bg, corner_radius=0)
            rf.pack(fill="x")
            ci = cat_icons.get(item["cat"], "•")
            vals  = [f"  {item['item']}", f"{ci} {item['cat']}", item["unit"],
                     f"{item['opening']:.1f}", f"+{item['received']:.1f}", f"{used:.1f}",
                     f"{item['stock']:.1f} {item['unit']}",
                     "⚠️  LOW STOCK" if is_low else "✓  OK"]
            colors = [DARK, MID, MID, DARK,
                      GREEN if item["received"] > 0 else MID,
                      PURPLE, RED if is_low else GREEN,
                      RED if is_low else GREEN]
            bolds = [True, False, False, False, False, False, True, True]
            for j, (v, c, bo) in enumerate(zip(vals, colors, bolds)):
                lbl(rf, v, size=12, weight="bold" if bo else "normal", color=c).grid(
                    row=0, column=j, padx=14, pady=10, sticky="w")
                rf.grid_columnconfigure(j, weight=wts[j])

    # ═════════════════════════════════════════════════════════════════════════
    # DAILY REPORT
    # ═════════════════════════════════════════════════════════════════════════
    def _page_report(self):
        hf = self._page_header("📋  Daily Operations Report",
                               datetime.now().strftime("📅  %d %B %Y"))
        ctk.CTkButton(hf, text="🖨  Export PDF",
                      height=38, width=150, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._popup(
                          "PDF Exported",
                          "Canteen_Report_" + datetime.now().strftime("%d%m%Y") + ".pdf\n"
                          f"Saved to: {os.path.dirname(DB_PATH)}")
                      ).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=(14, 24))

        rc = card(scroll, corner_radius=16)
        rc.pack(fill="x", pady=(0, 14))

        rhdr = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=112)
        rhdr.pack(fill="x")
        rhdr.pack_propagate(False)
        tricolor(rhdr, 5)
        ih = ctk.CTkFrame(rhdr, fg_color="transparent")
        ih.pack(expand=True)
        lbl(ih, "🇮🇳  INDIAN ARMY — CANTEEN DAILY REPORT",
            size=17, weight="bold", color=WHITE).pack(pady=(10, 3))
        lbl(ih, f"Date: {datetime.now().strftime('%d %B %Y')}   "
            "•   56 APO Field Canteen   •   Confidential",
            size=11, color=GOLD).pack(pady=(0, 14))

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            s_rows = conn.execute(
                "SELECT * FROM sales WHERE date=?", (today,)).fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in s_rows)
        total_cogs = sum(r["cogs"] for r in s_rows)
        net_profit = total_rev - total_cogs
        meals_tot  = sum(r["sold"] for r in s_rows)

        def sec_title(txt):
            sf = ctk.CTkFrame(rc, fg_color="transparent")
            sf.pack(fill="x", padx=24, pady=(18, 8))
            ctk.CTkFrame(sf, fg_color=SAFFRON, width=4, corner_radius=2).pack(
                side="left", fill="y", padx=(0, 10))
            lbl(sf, txt, size=13, weight="bold", color=ARMY_BG).pack(side="left")

        sec_title("1.  Meal Sales Summary")
        th = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=0)
        th.pack(fill="x", padx=24)
        for j, col in enumerate(["Meal Item", "Sold", "Rate (₹)", "Revenue (₹)", "Payment"]):
            lbl(th, col, size=11, weight="bold", color=MID).grid(
                row=0, column=j, padx=14, pady=9, sticky="w")
            th.grid_columnconfigure(j, weight=1)

        for idx, row in enumerate(s_rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf2 = ctk.CTkFrame(rc, fg_color=bg, corner_radius=0)
            rf2.pack(fill="x", padx=24)
            pi = {"Cash": "💵", "UPI": "📱", "Card": "💳"}.get(row["payment"], "💰")
            for j, val in enumerate([row["meal"], str(row["sold"]),
                    f"{row['sp']:.0f}", f"{row['sp']*row['sold']:,.0f}",
                    f"{pi} {row['payment']}"]):
                lbl(rf2, val, size=12).grid(row=0, column=j, padx=14, pady=9, sticky="w")
                rf2.grid_columnconfigure(j, weight=1)

        tot_row = ctk.CTkFrame(rc, fg_color="#FFF7ED", corner_radius=0)
        tot_row.pack(fill="x", padx=24, pady=(2, 0))
        for j, (v, c2) in enumerate(zip(
                ["TOTAL", str(meals_tot), "", f"{total_rev:,.0f}", ""],
                [SAFFRON, MID, DARK, SAFFRON, DARK])):
            lbl(tot_row, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=14, pady=10, sticky="w")
            tot_row.grid_columnconfigure(j, weight=1)

        sec_title("2.  Financial Summary")
        for desc, val, color in [
                ("Total Revenue (Sales Income)", f"₹ {total_rev:,.0f}",  GREEN),
                ("Total COGS (Ingredient Cost)", f"₹ {total_cogs:,.0f}", RED),
                ("Net Daily Profit",             f"₹ {net_profit:,.0f}", SAFFRON)]:
            fr = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=10)
            fr.pack(padx=24, fill="x", pady=4)
            lbl(fr, f"  {desc}", size=12).pack(side="left", padx=14, pady=14)
            lbl(fr, val, size=16, weight="bold", color=color).pack(side="right", padx=18)

        sec_title("3.  Payment Mode Breakdown")
        pf2 = ctk.CTkFrame(rc, fg_color="transparent")
        pf2.pack(padx=24, fill="x", pady=(0, 4))
        pf2.grid_rowconfigure(0, weight=1)
        cash_a = sum(r["sp"] * r["sold"] for r in s_rows if r["payment"] == "Cash")
        upi_a  = sum(r["sp"] * r["sold"] for r in s_rows if r["payment"] == "UPI")
        card_a = sum(r["sp"] * r["sold"] for r in s_rows if r["payment"] == "Card")
        for i, (mode, amt, color, bg_c, border_c) in enumerate([
                ("💵  Cash", f"₹ {cash_a:,.0f}", GREEN,  BG_GREEN,  T_GREEN),
                ("📱  UPI",  f"₹ {upi_a:,.0f}",  PURPLE, BG_PURPLE, T_PURPLE),
                ("💳  Card", f"₹ {card_a:,.0f}",  BLUE,   BG_BLUE,   T_BLUE)]):
            b = ctk.CTkFrame(pf2, fg_color=bg_c, corner_radius=14,
                             border_width=1, border_color=border_c)
            b.grid(row=0, column=i, padx=6, sticky="nsew")
            pf2.grid_columnconfigure(i, weight=1)
            lbl(b, mode, size=13, weight="bold", color=color).pack(
                padx=18, pady=(16, 4), anchor="w")
            lbl(b, amt, size=20, weight="bold", color=color).pack(
                padx=18, pady=(0, 16), anchor="w")

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
            lbl(b, role, size=10, weight="bold", color=MID).pack(
                padx=18, pady=(16, 48), anchor="w")
            ctk.CTkFrame(b, height=2, fg_color=ARMY_BG).pack(fill="x", padx=18)
            lbl(b, name, size=12, weight="bold", color=ARMY_BG).pack(
                padx=18, pady=(6, 2), anchor="w")
            lbl(b, rank, size=10, color=MID).pack(padx=18, pady=(0, 14), anchor="w")

        foot = ctk.CTkFrame(rc, height=6, fg_color="transparent")
        foot.pack(fill="x", pady=(16, 0))
        foot.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(foot, fg_color=c).pack(side="left", fill="both", expand=True)
        lbl(rc, "जय हिन्द  •  जय जवान  •  जय किसान",
            size=11, color=MID).pack(pady=(8, 16))

    # ── Popup ──────────────────────────────────────────────────────────────────
    def _popup(self, title, message):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("480x280")
        win.resizable(False, False)
        win.grab_set()
        win.lift()
        win.configure(fg_color=WHITE)

        ts = ctk.CTkFrame(win, height=5, fg_color="transparent")
        ts.pack(fill="x")
        ts.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ts, fg_color=c).pack(side="left", fill="both", expand=True)

        icon = "✅" if any(x in title for x in ["Saved", "Export", "List"]) else "ℹ️"
        lbl(win, icon, size=36).pack(pady=(20, 6))
        lbl(win, message, size=12, color=DARK, justify="center",
            wraplength=420).pack(pady=(0, 18))
        ctk.CTkButton(win, text="Close", width=130, height=42, corner_radius=10,
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=win.destroy).pack()
        lbl(win, "जय हिन्द", size=10, color=MID).pack(pady=(10, 16))


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CanteenApp()
    app.mainloop()
'''

import os
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
with open(dest, "w") as f:
    f.write(code)
print(f"Written {len(code)} chars to {dest}")
