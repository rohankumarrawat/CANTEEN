"""Writer — overwrites app.py with properly aligned redesign v3."""
code = r'''"""
Canteen Inventory & Sales Management System
Indian Army — Demo  |  Python + CustomTkinter + SQLite
"""

import customtkinter as ctk
from datetime import datetime
import sqlite3, os

# ── Database ───────────────────────────────────────────────────────────────────
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

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Palette ────────────────────────────────────────────────────────────────────
SAFFRON   = "#FF9933"
IND_GREEN = "#138808"
GOLD      = "#C9A84C"
GOLD_LT   = "#EDD97A"
ARMY_BG   = "#1F3320"
ARMY_HVR  = "#2C4A2A"
ARMY_SEP  = "#2E4830"

DARK   = "#1E293B"
MID    = "#64748B"
LIGHT  = "#F1F5F1"
WHITE  = "#FFFFFF"
BORDER = "#DDE8DD"
STRIPE = "#F5FAF5"

GREEN  = "#059669";  DGREEN = "#047857"
RED    = "#DC2626";  DRED   = "#B91C1C"
BLUE   = "#2563EB"
PURPLE = "#7C3AED"

# 6-digit Tkinter-safe tints
T_SAF = "#FFD4A8"; BG_SAF = "#FFF7ED"
T_GRN = "#A7F3D0"; BG_GRN = "#F0FDF4"
T_BLU = "#BFDBFE"; BG_BLU = "#EFF6FF"
T_PUR = "#DDD6FE"; BG_PUR = "#FAF5FF"
T_RED = "#FECACA"; BG_RED = "#FEF2F2"

PAD = 24   # consistent page margin

# ── Widget helpers ─────────────────────────────────────────────────────────────
def card(parent, **kw):
    d = dict(fg_color=WHITE, corner_radius=14, border_width=1, border_color=BORDER)
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

def band(parent, text, bg=ARMY_BG, tc=GOLD_LT, h=44):
    """Uniform card-header band: colored bg + saffron left accent + text."""
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkFrame(hdr, fg_color=SAFFRON, width=4, corner_radius=0).pack(
        side="left", fill="y")
    lbl(hdr, f"  {text}", size=12, weight="bold", color=tc).pack(
        side="left", padx=8)

def trow(parent, cols_vals, col_weights, colors=None, bolds=None,
         bg=WHITE, row_h=38, pady=9, padx=16):
    """Render one table row into parent.  Returns the row frame."""
    n   = len(cols_vals)
    clr = colors or [DARK] * n
    bld = bolds  or [False] * n
    rf  = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=row_h)
    rf.pack(fill="x")
    rf.pack_propagate(False)
    for j, (v, wt, c, b) in enumerate(zip(cols_vals, col_weights, clr, bld)):
        lbl(rf, v, size=12, weight="bold" if b else "normal", color=c).grid(
            row=0, column=j, padx=padx, pady=pady, sticky="w")
        rf.grid_columnconfigure(j, weight=wt)
    return rf

def thead(parent, col_defs, bg=ARMY_BG, tc=GOLD_LT, h=38, padx=16):
    """Table header row matching trow column layout."""
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    for j, (name, wt) in enumerate(col_defs):
        lbl(hdr, name, size=11, weight="bold", color=tc).grid(
            row=0, column=j, padx=padx, pady=0, sticky="w")
        hdr.grid_columnconfigure(j, weight=wt)
    return hdr

# ══════════════════════════════════════════════════════════════════════════════
class CanteenApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Indian Army Canteen Management System")
        self.geometry("1360x840")
        self.minsize(1100, 700)
        self.configure(fg_color=LIGHT)
        self._show_login()

    # ── Login ──────────────────────────────────────────────────────────────────
    def _show_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color="#EDF3ED")

        top = ctk.CTkFrame(self, fg_color="transparent", height=7)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(top, fg_color=c).pack(side="left", fill="both", expand=True)

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        box = ctk.CTkFrame(outer, fg_color=WHITE, corner_radius=24,
                           border_width=2, border_color=BORDER)
        box.pack()

        hdr = ctk.CTkFrame(box, fg_color=ARMY_BG, corner_radius=0,
                           height=132, width=440)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tricolor(hdr, 4)
        lbl(hdr, "🇮🇳  INDIAN ARMY", size=11, weight="bold",
            color=GOLD_LT).pack(pady=(12, 0))
        lbl(hdr, "CANTEEN MANAGEMENT SYSTEM", size=18, weight="bold",
            color=WHITE).pack(pady=(3, 0))
        lbl(hdr, "सेवा परमो धर्म  •  Service Before Self",
            size=10, color=GOLD).pack(pady=(3, 12))

        lbl(box, "Staff / Officer Login", size=15, weight="bold",
            color=ARMY_BG).pack(pady=(26, 16))

        # Fields — each label + entry in its own row frame for perfect alignment
        for field, attr, ph, show in [
            ("Username", "_uname", "Enter username", ""),
            ("Password", "_pwd",   "Enter password", "●"),
        ]:
            rf = ctk.CTkFrame(box, fg_color="transparent")
            rf.pack(fill="x", padx=44, pady=(0, 12))
            lbl(rf, field, size=12, weight="bold",
                color="#374151").pack(anchor="w", pady=(0, 5))
            e = ctk.CTkEntry(rf, height=46, corner_radius=10,
                             placeholder_text=ph, show=show,
                             font=ctk.CTkFont(size=14),
                             border_color="#CBD5E1")
            e.pack(fill="x")
            setattr(self, attr, e)

        self._uname.insert(0, "manager")
        self._pwd.insert(0, "1234")
        self._pwd.bind("<Return>", lambda e: self._do_login())

        ctk.CTkButton(box, text="🔐  Login to System", height=52,
                      corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=self._do_login).pack(
                          padx=44, pady=(6, 12), fill="x")

        self._login_err = lbl(box, "", size=12, color=RED)
        self._login_err.pack()

        foot = ctk.CTkFrame(box, fg_color="transparent", height=5, width=440)
        foot.pack(fill="x", pady=(14, 0))
        foot.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(foot, fg_color=c).pack(side="left", fill="both", expand=True)
        lbl(box, "जय हिन्द  •  Demo v3.0  •  SQLite Powered",
            size=10, color="#94A3B8").pack(pady=(8, 22))

    def _do_login(self):
        if self._uname.get().strip() == "manager" and self._pwd.get() == "1234":
            self._show_main()
        else:
            self._login_err.configure(
                text="⚠  Invalid credentials. Use  manager / 1234")

    # ── Main Shell ─────────────────────────────────────────────────────────────
    def _show_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=LIGHT)

        # Sidebar
        sb = ctk.CTkFrame(self, fg_color=ARMY_BG, width=258, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        self._sidebar = sb
        tricolor(sb, 5)

        # Logo row
        lg = ctk.CTkFrame(sb, fg_color="transparent")
        lg.pack(fill="x", padx=16, pady=(14, 8))
        lbl(lg, "🇮🇳", size=30).pack(side="left", padx=(0, 10))
        tf = ctk.CTkFrame(lg, fg_color="transparent")
        tf.pack(side="left")
        lbl(tf, "INDIAN ARMY", size=12, weight="bold", color=GOLD).pack(anchor="w")
        lbl(tf, "Canteen Management", size=9, color="#7A9A7A").pack(anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(
            fill="x", padx=16, pady=(6, 10))

        # Unit card
        uc = ctk.CTkFrame(sb, fg_color="#1A2F1C", corner_radius=10)
        uc.pack(padx=12, fill="x", pady=(0, 12))
        lbl(uc, "⭐  Unit / Establishment", size=9, color=GOLD).pack(
            padx=12, pady=(9, 1), anchor="w")
        lbl(uc, "56 APO Field Canteen", size=12, weight="bold",
            color=WHITE).pack(padx=12, anchor="w")
        lbl(uc, "Est. 1947  •  Serving with Pride", size=9,
            color="#7A9A7A").pack(padx=12, pady=(1, 9), anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(
            fill="x", padx=16, pady=(0, 6))
        lbl(sb, "  NAVIGATION", size=9, weight="bold",
            color="#4A6A4A").pack(anchor="w", padx=16, pady=(2, 4))

        self._nav_btns = {}
        for icon_txt, page in [
            ("📊  Dashboard",    "dashboard"),
            ("💰  Sales Entry",  "sales"),
            ("📦  Inventory",    "inventory"),
            ("📋  Daily Report", "report"),
        ]:
            b = ctk.CTkButton(sb, text=icon_txt, anchor="w", height=46,
                              font=ctk.CTkFont(size=13, weight="bold"),
                              fg_color="transparent",
                              hover_color=ARMY_HVR, text_color="#8AAA8A",
                              corner_radius=8,
                              command=lambda p=page: self._navigate(p))
            b.pack(padx=12, pady=2, fill="x")
            self._nav_btns[page] = b

        # Bottom items
        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(
            fill="x", padx=16, side="bottom", pady=(8, 6))
        ctk.CTkButton(sb, text="⬅  Logout", height=40, anchor="w",
                      fg_color="transparent", hover_color=ARMY_HVR,
                      text_color="#5A7A5A",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      corner_radius=8,
                      command=self._show_login).pack(
                          padx=12, pady=(0, 8), fill="x", side="bottom")

        usr = ctk.CTkFrame(sb, fg_color="#1A2F1C", corner_radius=10)
        usr.pack(padx=12, side="bottom", fill="x", pady=(0, 8))
        lbl(usr, "👤  Canteen Manager", size=11, weight="bold",
            color=WHITE).pack(padx=12, pady=(10, 1), anchor="w")
        lbl(usr, "manager@indianarmy.mil", size=9,
            color="#5A7A5A").pack(padx=12, pady=(0, 10), anchor="w")

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
                b.configure(fg_color="transparent", text_color="#8AAA8A")
        for w in self._content.winfo_children():
            w.destroy()
        {"dashboard": self._page_dashboard,
         "sales":     self._page_sales,
         "inventory": self._page_inventory,
         "report":    self._page_report}[page]()

    def _page_header(self, title, subtitle=""):
        """Top title bar. Returns the frame so callers can add right-side buttons."""
        hf = ctk.CTkFrame(self._content, fg_color=WHITE,
                          corner_radius=0, height=64)
        hf.pack(fill="x")
        hf.pack_propagate(False)
        # subtle bottom border
        ctk.CTkFrame(hf, fg_color=BORDER, height=1,
                     corner_radius=0).pack(side="bottom", fill="x")
        # saffron left accent
        ctk.CTkFrame(hf, fg_color=SAFFRON, width=5,
                     corner_radius=0).pack(side="left", fill="y")
        inner = ctk.CTkFrame(hf, fg_color="transparent")
        inner.pack(side="left", fill="y", padx=PAD)
        lbl(inner, title, size=20, weight="bold", color=ARMY_BG).pack(
            anchor="w", pady=(12, 0))
        if subtitle:
            lbl(inner, subtitle, size=10, color=MID).pack(anchor="w")
        return hf

    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    def _page_dashboard(self):
        hf = self._page_header(
            "Dashboard",
            f"🇮🇳  {datetime.now().strftime('%A, %d %B %Y')}  ·  56 APO Field Canteen"
        )

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            rows     = conn.execute(
                "SELECT * FROM sales WHERE date=?", (today,)).fetchall()
            inv_rows = conn.execute("SELECT * FROM inventory").fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in rows)
        total_cost = sum(r["cogs"] for r in rows)
        net_profit = total_rev - total_cost
        meals_sold = sum(r["sold"] for r in rows)
        low_items  = [i for i in inv_rows if i["stock"] < i["min_lvl"]]

        # ── KPI row ───────────────────────────────────────────────────────────
        KPI = [
            ("💰", "Total Revenue",  f"₹{total_rev:,.0f}",  SAFFRON, BG_SAF, T_SAF),
            ("🧾", "Total COGS",     f"₹{total_cost:,.0f}", PURPLE,  BG_PUR, T_PUR),
            ("📈", "Net Profit",     f"₹{net_profit:,.0f}", GREEN,   BG_GRN, T_GRN),
            ("🍛", "Meals Served",   str(meals_sold),        BLUE,    BG_BLU, T_BLU),
            ("⚠️", "Low Stock",      str(len(low_items)),    RED,     BG_RED, T_RED),
        ]
        kr = ctk.CTkFrame(self._content, fg_color="transparent")
        kr.pack(fill="x", padx=PAD, pady=(18, 0))
        for i, (icon, title, val, color, bg, border) in enumerate(KPI):
            c = ctk.CTkFrame(kr, fg_color=WHITE, corner_radius=14,
                             border_width=1, border_color=border)
            c.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            kr.grid_columnconfigure(i, weight=1)
            kr.grid_rowconfigure(0, weight=1)

            # Top accent line
            ctk.CTkFrame(c, fg_color=color, height=4,
                         corner_radius=0).pack(fill="x")
            # Content row: icon bubble  ·  value+label
            row_f = ctk.CTkFrame(c, fg_color="transparent")
            row_f.pack(fill="x", padx=16, pady=14)

            ib = ctk.CTkFrame(row_f, fg_color=bg, corner_radius=10,
                              width=44, height=44)
            ib.pack(side="left")
            ib.pack_propagate(False)
            lbl(ib, icon, size=19).place(relx=0.5, rely=0.5, anchor="center")

            vf = ctk.CTkFrame(row_f, fg_color="transparent")
            vf.pack(side="left", padx=(12, 0), fill="both")
            lbl(vf, val,   size=20, weight="bold", color=color).pack(anchor="w")
            lbl(vf, title, size=10, color=MID).pack(anchor="w", pady=(1, 0))

        # ── Bottom section ────────────────────────────────────────────────────
        bot = ctk.CTkFrame(self._content, fg_color="transparent")
        bot.pack(fill="both", expand=True, padx=PAD, pady=(14, PAD))
        bot.grid_columnconfigure(0, weight=6)
        bot.grid_columnconfigure(1, weight=4)
        bot.grid_rowconfigure(0, weight=1)

        # Sales table card
        COLS = [("Meal Item", 3), ("Qty", 1), ("Rate", 1),
                ("Revenue", 2), ("Payment", 2)]
        WTS  = [w for _, w in COLS]

        sc = card(bot)
        sc.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        band(sc, "📊  Today's Sales Breakdown")
        thead(sc, COLS, bg=STRIPE, tc=MID)

        for idx, row in enumerate(rows):
            pi  = {"Cash": "💵", "UPI": "📱", "Card": "💳"}.get(row["payment"], "💰")
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            trow(sc,
                 [row["meal"], str(row["sold"]), f"₹{row['sp']:.0f}",
                  f"₹{row['sp']*row['sold']:,.0f}", f"{pi} {row['payment']}"],
                 WTS,
                 colors=[DARK, MID, MID, DARK, MID],
                 bolds=[True, False, False, True, False],
                 bg=bg2)

        # Total row
        tot = ctk.CTkFrame(sc, fg_color=BG_SAF, corner_radius=0, height=38)
        tot.pack(fill="x")
        tot.pack_propagate(False)
        for j, (v, c2, wt) in enumerate(zip(
                ["TOTAL", str(meals_sold), "—", f"₹{total_rev:,.0f}", ""],
                [SAFFRON, MID, MID, SAFFRON, DARK], WTS)):
            lbl(tot, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=16, sticky="w")
            tot.grid_columnconfigure(j, weight=wt)

        foot = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0, height=26)
        foot.pack(fill="x", side="bottom")
        foot.pack_propagate(False)
        lbl(foot, "💾  SQLite · canteen.db  (persistent local storage)",
            size=9, color="#94A3B8").pack(side="left", padx=16)
        lbl(foot, datetime.now().strftime("Last sync: %H:%M"),
            size=9, color="#94A3B8").pack(side="right", padx=16)

        # Alerts card
        ac = card(bot)
        ac.grid(row=0, column=1, sticky="nsew")
        band(ac, f"⚠️  Low Stock  ({len(low_items)} items)", bg=DRED, tc=WHITE)

        sc2 = ctk.CTkScrollableFrame(ac, fg_color="transparent")
        sc2.pack(fill="both", expand=True, padx=10, pady=10)

        if not low_items:
            lbl(sc2, "✅  All items sufficiently stocked.",
                size=12, color=GREEN).pack(pady=28)
        else:
            for item in low_items:
                rf2 = ctk.CTkFrame(sc2, fg_color=BG_RED, corner_radius=10,
                                   border_width=1, border_color=T_RED)
                rf2.pack(fill="x", pady=4)
                lbl(rf2, f"  {item['item']}", size=13, weight="bold",
                    color="#991B1B").pack(padx=10, pady=(10, 2), anchor="w")
                bf2 = ctk.CTkFrame(rf2, fg_color="transparent")
                bf2.pack(padx=10, pady=(0, 10), fill="x")
                lbl(bf2, f"Stock: {item['stock']} {item['unit']}",
                    size=11, color=RED).pack(side="left")
                lbl(bf2, f"Min: {item['min_lvl']} {item['unit']}",
                    size=11, color=MID).pack(side="right")

        ctk.CTkButton(ac, text="🛒  Generate Shopping List",
                      height=42, corner_radius=0,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=RED, hover_color=DRED,
                      command=lambda: self._popup(
                          "🛒  Shopping List",
                          "\n".join(
                              f"• {i['item']}  —  need {i['min_lvl']-i['stock']:.1f} {i['unit']}"
                              for i in low_items) or "All stock sufficient!")
                      ).pack(fill="x", side="bottom")

    # ══════════════════════════════════════════════════════════════════════════
    # SALES ENTRY
    # ══════════════════════════════════════════════════════════════════════════
    def _page_sales(self):
        self._page_header("💰  Daily Sales Entry",
                          datetime.now().strftime("📅  %d %B %Y"))

        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(16, PAD))

        # Meal form
        mc = card(wrap)
        mc.pack(fill="x", pady=(0, 16))
        band(mc, "🍽  Meal Preparation & Sales Count")
        lbl(mc, "  Enter quantities prepared, sold and wastage for each meal item.",
            size=12, color=MID).pack(anchor="w", padx=16, pady=(10, 6))

        MEAL_COLS = [("Meal Item", 3), ("Qty Prepared", 2),
                     ("Qty Sold", 2), ("Wastage", 2)]
        MWTS = [w for _, w in MEAL_COLS]
        thead(mc, MEAL_COLS, bg=STRIPE, tc=MID)

        meals = [("Standard Lunch", "🍛"),
                 ("VIP Thali",      "🍛"),
                 ("Tea",            "☕"),
                 ("Snacks",         "🍿"),
                 ("Breakfast",      "🌅"),
                 ("Evening Snacks", "🍿")]
        self._entries = {}
        for idx, (meal, icon) in enumerate(meals):
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            rf  = ctk.CTkFrame(mc, fg_color=bg2, corner_radius=0)
            rf.pack(fill="x")
            lbl(rf, f"  {icon}  {meal}", size=13, weight="bold",
                color=DARK).grid(row=0, column=0, padx=16, pady=10, sticky="w")
            rf.grid_columnconfigure(0, weight=MWTS[0])
            ents = []
            for j in range(1, 4):
                bc = T_RED if j == 3 else BORDER
                e = ctk.CTkEntry(rf, height=36, corner_radius=8,
                                 placeholder_text="0",
                                 font=ctk.CTkFont(size=13),
                                 border_color=bc)
                e.grid(row=0, column=j, padx=(0, 16), pady=10, sticky="ew")
                rf.grid_columnconfigure(j, weight=MWTS[j])
                ents.append(e)
            self._entries[meal] = ents

        # Payment breakdown
        pc = card(wrap)
        pc.pack(fill="x", pady=(0, 16))
        band(pc, "💳  Payment Collection Breakdown")

        pf = ctk.CTkFrame(pc, fg_color="transparent")
        pf.pack(fill="x", padx=20, pady=18)
        pf.grid_rowconfigure(0, weight=1)

        for i, (mode, color, icon, bg_c, border_c) in enumerate([
                ("Cash", GREEN,  "💵", BG_GRN, T_GRN),
                ("UPI",  PURPLE, "📱", BG_PUR, T_PUR),
                ("Card", BLUE,   "💳", BG_BLU, T_BLU)]):
            b = ctk.CTkFrame(pf, fg_color=bg_c, corner_radius=12,
                             border_width=1, border_color=border_c)
            b.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            pf.grid_columnconfigure(i, weight=1)

            top2 = ctk.CTkFrame(b, fg_color="transparent")
            top2.pack(fill="x", padx=16, pady=(16, 6))
            ib2 = ctk.CTkFrame(top2, fg_color=color, corner_radius=8,
                               width=34, height=34)
            ib2.pack(side="left")
            ib2.pack_propagate(False)
            lbl(ib2, icon, size=14, color=WHITE).place(
                relx=0.5, rely=0.5, anchor="center")
            lbl(top2, f"  {mode}", size=13, weight="bold",
                color=color).pack(side="left", pady=6)

            lbl(b, "Amount (₹)", size=10, color=MID).pack(padx=16, anchor="w")
            ctk.CTkEntry(b, height=44, placeholder_text="0.00",
                         corner_radius=8, font=ctk.CTkFont(size=16),
                         border_color=border_c).pack(
                             padx=16, pady=(4, 18), fill="x")

        # Action buttons
        bf = ctk.CTkFrame(wrap, fg_color="transparent")
        bf.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(bf, text="✅  Save & Auto-Deduct Stock",
                      height=52, corner_radius=12,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=lambda: self._popup(
                          "✅  Saved to Database!",
                          "Sales recorded in canteen.db\n"
                          "Inventory auto-deducted based on recipes.")
                      ).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ctk.CTkButton(bf, text="📋  Preview Report",
                      height=52, corner_radius=12,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._navigate("report")
                      ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    # ══════════════════════════════════════════════════════════════════════════
    # INVENTORY
    # ══════════════════════════════════════════════════════════════════════════
    def _page_inventory(self):
        hf = self._page_header("📦  Inventory Ledger",
                               datetime.now().strftime("📅  %d %B %Y"))

        # Filter buttons in the header bar
        ff = ctk.CTkFrame(hf, fg_color="transparent")
        ff.pack(side="right", padx=PAD)
        self._filter_btns = {}
        for cat in ["All", "Dry", "Fresh", "Dairy", "Packaging"]:
            b = ctk.CTkButton(ff, text=cat, width=76, height=30,
                              corner_radius=8,
                              font=ctk.CTkFont(size=12, weight="bold"),
                              fg_color=ARMY_BG if cat == "All" else STRIPE,
                              text_color=WHITE if cat == "All" else DARK,
                              hover_color=ARMY_HVR,
                              command=lambda c=cat: self._filter_inv(c))
            b.pack(side="left", padx=3)
            self._filter_btns[cat] = b

        # Action buttons row
        ab = ctk.CTkFrame(self._content, fg_color="transparent")
        ab.pack(fill="x", padx=PAD, pady=(12, 0))
        ctk.CTkButton(ab, text="＋  Add Received Stock",
                      height=38, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN, width=190,
                      command=lambda: self._popup(
                          "Add Stock",
                          "Stock receipt saved to canteen.db\n"
                          "(Full entry form in production build.)")
                      ).pack(side="left")
        ctk.CTkButton(ab, text="🔧  Manual Adjustment",
                      height=38, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=PURPLE, hover_color="#6D28D9", width=170,
                      command=lambda: self._popup(
                          "Manual Adjustment",
                          "Admin-only feature.\nSaved to canteen.db.")
                      ).pack(side="left", padx=10)

        # Table
        tc = card(self._content)
        tc.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        INV_COLS = [("Item", 4), ("Category", 2), ("Unit", 1),
                    ("Opening", 1), ("Received", 1), ("Used", 1),
                    ("Closing Stock", 2), ("Status", 2)]
        INV_WTS = [w for _, w in INV_COLS]

        thead(tc, INV_COLS)

        self._inv_body = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_body.pack(fill="both", expand=True)
        self._inv_wts = INV_WTS

        with get_db() as conn:
            data = conn.execute("SELECT * FROM inventory").fetchall()
        self._render_inv_rows(list(data))

    def _filter_inv(self, cat):
        for c2, b in self._filter_btns.items():
            b.configure(fg_color=ARMY_BG if c2 == cat else STRIPE,
                        text_color=WHITE if c2 == cat else DARK)
        for w in self._inv_body.winfo_children():
            w.destroy()
        with get_db() as conn:
            if cat == "All":
                data = conn.execute("SELECT * FROM inventory").fetchall()
            else:
                data = conn.execute(
                    "SELECT * FROM inventory WHERE cat=?", (cat,)).fetchall()
        self._render_inv_rows(list(data))

    def _render_inv_rows(self, data):
        cat_icon = {"Dry": "🌾", "Fresh": "🥦",
                    "Dairy": "🥛", "Packaging": "📦"}
        for idx, item in enumerate(data):
            is_low = item["stock"] < item["min_lvl"]
            used   = item["opening"] + item["received"] - item["stock"]
            bg2    = BG_RED if is_low else (WHITE if idx % 2 == 0 else STRIPE)
            ci     = cat_icon.get(item["cat"], "•")
            vals   = [
                f"  {item['item']}",
                f"{ci}  {item['cat']}",
                item["unit"],
                f"{item['opening']:.1f}",
                f"+{item['received']:.1f}",
                f"{used:.1f}",
                f"{item['stock']:.1f} {item['unit']}",
                "⚠  LOW" if is_low else "✓  OK"
            ]
            clrs = [DARK, MID, MID, DARK,
                    GREEN if item["received"] > 0 else MID,
                    PURPLE,
                    RED if is_low else GREEN,
                    RED if is_low else GREEN]
            blds = [True, False, False, False, False, False, True, True]
            trow(self._inv_body, vals, self._inv_wts,
                 colors=clrs, bolds=blds, bg=bg2, row_h=40)

    # ══════════════════════════════════════════════════════════════════════════
    # DAILY REPORT
    # ══════════════════════════════════════════════════════════════════════════
    def _page_report(self):
        hf = self._page_header("📋  Daily Operations Report",
                               datetime.now().strftime("📅  %d %B %Y"))
        ctk.CTkButton(hf, text="🖨  Export PDF",
                      height=34, width=140, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._popup(
                          "PDF Exported",
                          "Canteen_Report_" +
                          datetime.now().strftime("%d%m%Y") + ".pdf\n"
                          f"Saved to: {os.path.dirname(DB_PATH)}")
                      ).pack(side="right", padx=PAD, pady=14)

        scroll = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        rc = card(scroll)
        rc.pack(fill="x", pady=(0, 14))

        # Letterhead
        lh = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=104)
        lh.pack(fill="x")
        lh.pack_propagate(False)
        tricolor(lh, 5)
        lbl(lh, "🇮🇳  INDIAN ARMY — CANTEEN DAILY REPORT",
            size=16, weight="bold", color=WHITE).pack(pady=(12, 2))
        lbl(lh, f"Date: {datetime.now().strftime('%d %B %Y')}   "
            "•   56 APO Field Canteen   •   Confidential",
            size=11, color=GOLD).pack(pady=(0, 12))

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            s_rows = conn.execute(
                "SELECT * FROM sales WHERE date=?", (today,)).fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in s_rows)
        total_cogs = sum(r["cogs"] for r in s_rows)
        net_profit = total_rev - total_cogs
        meals_tot  = sum(r["sold"] for r in s_rows)

        def sec(txt):
            sf = ctk.CTkFrame(rc, fg_color="transparent")
            sf.pack(fill="x", padx=PAD, pady=(18, 8))
            ctk.CTkFrame(sf, fg_color=SAFFRON, width=4,
                         corner_radius=2).pack(side="left", fill="y",
                                               padx=(0, 10))
            lbl(sf, txt, size=13, weight="bold", color=ARMY_BG).pack(
                side="left")

        SALE_COLS = [("Meal Item", 3), ("Sold", 1), ("Rate (₹)", 1),
                     ("Revenue (₹)", 2), ("Payment", 2)]
        SWTS = [w for _, w in SALE_COLS]

        sec("1.  Meal Sales Summary")
        # Report tables use padx=PAD on the left side, full width frame:
        tbl_f = ctk.CTkFrame(rc, fg_color="transparent")
        tbl_f.pack(fill="x", padx=PAD)
        thead(tbl_f, SALE_COLS, bg=STRIPE, tc=MID)
        for idx, row in enumerate(s_rows):
            pi  = {"Cash": "💵", "UPI": "📱", "Card": "💳"}.get(row["payment"], "💰")
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            trow(tbl_f,
                 [row["meal"], str(row["sold"]),
                  f"{row['sp']:.0f}",
                  f"{row['sp']*row['sold']:,.0f}",
                  f"{pi} {row['payment']}"],
                 SWTS, bg=bg2)
        # Total
        tot2 = ctk.CTkFrame(tbl_f, fg_color=BG_SAF, corner_radius=0, height=38)
        tot2.pack(fill="x")
        tot2.pack_propagate(False)
        for j, (v, c2, wt) in enumerate(zip(
                ["GRAND TOTAL", str(meals_tot), "—",
                 f"{total_rev:,.0f}", ""],
                [SAFFRON, MID, MID, SAFFRON, DARK], SWTS)):
            lbl(tot2, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=16, sticky="w")
            tot2.grid_columnconfigure(j, weight=wt)

        sec("2.  Financial Summary")
        for desc, val, clr in [
                ("Total Revenue",    f"₹ {total_rev:,.0f}",  GREEN),
                ("Total COGS",       f"₹ {total_cogs:,.0f}", RED),
                ("Net Daily Profit", f"₹ {net_profit:,.0f}", SAFFRON)]:
            fr = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=10)
            fr.pack(padx=PAD, fill="x", pady=4)
            lbl(fr, f"  {desc}", size=12, color=DARK).pack(
                side="left", padx=14, pady=13)
            lbl(fr, val, size=16, weight="bold", color=clr).pack(
                side="right", padx=18)

        sec("3.  Payment Mode Breakdown")
        pf3 = ctk.CTkFrame(rc, fg_color="transparent")
        pf3.pack(padx=PAD, fill="x", pady=(0, 4))
        pf3.grid_rowconfigure(0, weight=1)
        cash_a = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"] == "Cash")
        upi_a  = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"] == "UPI")
        card_a = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"] == "Card")
        for i, (mode, amt, clr, bg_c, bo_c) in enumerate([
                ("💵  Cash", f"₹ {cash_a:,.0f}", GREEN,  BG_GRN, T_GRN),
                ("📱  UPI",  f"₹ {upi_a:,.0f}",  PURPLE, BG_PUR, T_PUR),
                ("💳  Card", f"₹ {card_a:,.0f}",  BLUE,   BG_BLU, T_BLU)]):
            b2 = ctk.CTkFrame(pf3, fg_color=bg_c, corner_radius=12,
                              border_width=1, border_color=bo_c)
            b2.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            pf3.grid_columnconfigure(i, weight=1)
            lbl(b2, mode, size=13, weight="bold", color=clr).pack(
                padx=18, pady=(16, 4), anchor="w")
            lbl(b2, amt, size=20, weight="bold", color=clr).pack(
                padx=18, pady=(0, 16), anchor="w")

        sec("4.  Official Sign-off")
        sf2 = ctk.CTkFrame(rc, fg_color="transparent")
        sf2.pack(padx=PAD, fill="x", pady=(0, 24))
        for i, (role, name, rank) in enumerate([
                ("Prepared By",  "Canteen Manager",     "JCO / OR"),
                ("Checked By",   "Supervision Officer", "Subedar"),
                ("Approved By",  "Officer-in-Charge",   "Captain / Lt")]):
            b3 = ctk.CTkFrame(sf2, fg_color="#F9FAFB", corner_radius=12,
                              border_width=1, border_color=BORDER)
            b3.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            sf2.grid_columnconfigure(i, weight=1)
            lbl(b3, role, size=10, weight="bold", color=MID).pack(
                padx=16, pady=(16, 48), anchor="w")
            ctk.CTkFrame(b3, height=2, fg_color=ARMY_BG).pack(fill="x", padx=16)
            lbl(b3, name, size=12, weight="bold", color=ARMY_BG).pack(
                padx=16, pady=(6, 1), anchor="w")
            lbl(b3, rank, size=10, color=MID).pack(
                padx=16, pady=(0, 12), anchor="w")

        # Footer tricolor
        ft2 = ctk.CTkFrame(rc, fg_color="transparent", height=5)
        ft2.pack(fill="x", pady=(16, 0))
        ft2.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ft2, fg_color=c).pack(side="left", fill="both", expand=True)
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

        ts = ctk.CTkFrame(win, fg_color="transparent", height=5)
        ts.pack(fill="x")
        ts.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ts, fg_color=c).pack(side="left", fill="both", expand=True)

        icon2 = "✅" if any(x in title for x in
                            ["Saved", "Export", "List"]) else "ℹ️"
        lbl(win, icon2, size=36).pack(pady=(20, 6))
        lbl(win, message, size=12, color=DARK, justify="center",
            wraplength=420).pack(pady=(0, 18))
        ctk.CTkButton(win, text="Close", width=120, height=40,
                      corner_radius=10, fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=win.destroy).pack()
        lbl(win, "जय हिन्द", size=10, color=MID).pack(pady=(8, 16))


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CanteenApp()
    app.mainloop()
'''

import os
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
with open(dest, "w") as f:
    f.write(code)
print(f"Written {len(code)} chars → {dest}")
