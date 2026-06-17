"""
Canteen Inventory & Sales Management System - ENHANCED VERSION
Indian Army — Advanced Management  |  Python + CustomTkinter + SQLite

ENHANCEMENTS:
✓ Stock Management (Add, Remove, Track, Alerts)
✓ User Management (Add, Remove, Roles, Permissions)  
✓ Waste Manager (Dedicated section with tracking)
✓ Daily Report (Comprehensive analysis by period)
✓ Batch Preparation (Simple 2-section prep tracking)
✓ Sales (Simple: Select item + number sold)
✓ Financial Records (Money tracking, reconciliation)
✓ Stock Deduction (Automatic based on recipes)
"""

import customtkinter as ctk
from datetime import datetime, timedelta
import sqlite3, os, math, hashlib
import tkinter as tk

# ── Database ───────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canteen.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def _has_column(conn, table, column):
    info = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(col[1] == column for col in info)

def init_db():
    if os.path.exists(DB_PATH):
        conn = get_db()
        try:
            legacy_inventory = not _has_column(conn, "inventory", "cp")
            legacy_sales = not _has_column(conn, "sales", "menu_id") or not _has_column(conn, "sales", "wastage")
        finally:
            conn.close()
        if legacy_inventory or legacy_sales:
            os.remove(DB_PATH)

    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS roles (
                role TEXT PRIMARY KEY,
                label TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                pw_hash TEXT NOT NULL,
                name TEXT NOT NULL DEFAULT '',
                rank TEXT NOT NULL DEFAULT '',
                contact TEXT DEFAULT '',
                active INTEGER DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS user_roles (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                role TEXT NOT NULL REFERENCES roles(role) ON DELETE CASCADE,
                PRIMARY KEY(user_id, role)
            );
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL UNIQUE,
                cat TEXT NOT NULL,
                unit TEXT NOT NULL,
                stock REAL NOT NULL DEFAULT 0,
                min_lvl REAL NOT NULL DEFAULT 0,
                opening REAL NOT NULL DEFAULT 0,
                received REAL NOT NULL DEFAULT 0,
                cp REAL NOT NULL DEFAULT 0,
                updated TEXT DEFAULT CURRENT_DATE
            );
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                sp REAL NOT NULL DEFAULT 0,
                active INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER NOT NULL REFERENCES menu(id) ON DELETE CASCADE,
                inv_id INTEGER NOT NULL REFERENCES inventory(id) ON DELETE CASCADE,
                qty_per_unit REAL NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS goods_received (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                inv_id INTEGER NOT NULL REFERENCES inventory(id),
                qty REAL NOT NULL,
                total_cost REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS batch_prep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                menu_id INTEGER NOT NULL REFERENCES menu(id),
                qty_prepared INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS expenditure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                notes TEXT
            );
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                menu_id INTEGER NOT NULL REFERENCES menu(id),
                meal TEXT NOT NULL,
                sp REAL NOT NULL,
                sold INTEGER NOT NULL DEFAULT 0,
                wastage INTEGER NOT NULL DEFAULT 0,
                cogs REAL NOT NULL DEFAULT 0,
                payment TEXT NOT NULL DEFAULT 'Cash'
            );
            CREATE TABLE IF NOT EXISTS waste_tracker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                item TEXT NOT NULL,
                qty_wasted REAL NOT NULL,
                reason TEXT,
                cost_lost REAL,
                recorded_by TEXT
            );
            CREATE TABLE IF NOT EXISTS stock_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                inv_id INTEGER NOT NULL REFERENCES inventory(id),
                transaction_type TEXT,
                qty_change REAL NOT NULL,
                notes TEXT
            );
        """)

        conn.executemany(
            "INSERT OR IGNORE INTO roles (role,label) VALUES (?,?)",
            [
                ("admin","System Admin"),
                ("manager","Canteen Manager"),
                ("officer","Officer (Read-Only)"),
                ("waste_mgr","Waste Manager"),
            ])

        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            for username, password, role, name, rank in [
                ("admin",   "admin123",   "admin",     "System Administrator", "Admin"),
                ("manager", "manager123", "manager",   "Canteen Manager",      "JCO"),
                ("officer", "officer123", "officer",   "Officer-in-Charge",    "Captain"),
                ("waste",   "waste123",   "waste_mgr", "Waste Manager",        "Havildar"),
            ]:
                cur = conn.execute(
                    "INSERT INTO users (username,pw_hash,name,rank) VALUES (?,?,?,?)",
                    (username, _hash(password), name, rank))
                conn.execute("INSERT INTO user_roles (user_id,role) VALUES (?,?)",
                             (cur.lastrowid, role))

        conn.executemany(
            "INSERT OR IGNORE INTO inventory (item,cat,unit,stock,min_lvl,opening,received,cp) VALUES (?,?,?,?,?,?,?,?)",
            [
                ("Rice", "Staple", "kg", 75, 20, 75, 20, 40),
                ("Roti Dough", "Staple", "kg", 25, 10, 25, 5, 20),
                ("Seasonal Vegetables", "Produce", "kg", 40, 15, 40, 20, 30),
                ("Salad Ingredients", "Produce", "kg", 18, 6, 18, 12, 15),
                ("Sweets", "Misc", "kg", 10, 4, 10, 5, 80),
                ("Panchratna Dal Mix", "Dry", "kg", 12, 4, 12, 6, 120),
                ("Kadhi Base", "Dry", "kg", 14, 5, 14, 8, 120),
                ("Pakoda Mix", "Dry", "kg", 8, 3, 8, 5, 80),
                ("Rajma", "Dry", "kg", 18, 5, 18, 10, 150),
                ("Kala Chana", "Dry", "kg", 15, 5, 15, 8, 140),
                ("Chana Dal", "Dry", "kg", 16, 5, 16, 8, 130),
                ("Paneer", "Dairy", "kg", 12, 4, 12, 6, 260),
                ("Mix Veg", "Produce", "kg", 22, 7, 22, 10, 40),
                ("Matar", "Dry", "kg", 12, 4, 12, 8, 120),
                ("Kulcha", "Bakery", "pcs", 100, 30, 100, 40, 25),
                ("Veg Manchurian", "Prepared", "kg", 10, 3, 10, 6, 220),
                ("Fried Rice Mix", "Prepared", "kg", 15, 5, 15, 8, 110),
                ("Biryani Mix", "Prepared", "kg", 14, 5, 14, 7, 130),
            ])

        conn.executemany(
            "INSERT OR IGNORE INTO menu (name,sp,active) VALUES (?,?,1)",
            [
                ("Panchratna Dal Thali", 70),
                ("Kadhi Pakoda Thali", 70),
                ("Rajma Thali", 70),
                ("Kala Chana Thali", 70),
                ("Chana Dal Paneer Thali", 70),
                ("Veg Manchurian & Fried Rice", 50),
                ("Kadhi chawal", 50),
                ("Rajma Rice", 50),
                ("Veg biryani", 50),
                ("Matar Kulcha", 50),
            ])

        menu_ids = {row[1]: row[0] for row in conn.execute("SELECT id,name FROM menu").fetchall()}
        inv_ids = {row[1]: row[0] for row in conn.execute("SELECT id,item FROM inventory").fetchall()}

        recipe_rows = [
            ("Panchratna Dal Thali", "Panchratna Dal Mix", 0.22),
            ("Panchratna Dal Thali", "Rice", 0.30),
            ("Panchratna Dal Thali", "Roti Dough", 0.20),
            ("Panchratna Dal Thali", "Seasonal Vegetables", 0.20),
            ("Panchratna Dal Thali", "Salad Ingredients", 0.12),
            ("Panchratna Dal Thali", "Sweets", 0.10),
            ("Kadhi Pakoda Thali", "Kadhi Base", 0.30),
            ("Kadhi Pakoda Thali", "Pakoda Mix", 0.15),
            ("Kadhi Pakoda Thali", "Rice", 0.30),
            ("Kadhi Pakoda Thali", "Roti Dough", 0.20),
            ("Kadhi Pakoda Thali", "Seasonal Vegetables", 0.18),
            ("Kadhi Pakoda Thali", "Salad Ingredients", 0.12),
            ("Kadhi Pakoda Thali", "Sweets", 0.10),
            ("Rajma Thali", "Rajma", 0.25),
            ("Rajma Thali", "Mix Veg", 0.22),
            ("Rajma Thali", "Rice", 0.30),
            ("Rajma Thali", "Roti Dough", 0.20),
            ("Rajma Thali", "Seasonal Vegetables", 0.12),
            ("Rajma Thali", "Sweets", 0.10),
            ("Kala Chana Thali", "Kala Chana", 0.25),
            ("Kala Chana Thali", "Mix Veg", 0.22),
            ("Kala Chana Thali", "Rice", 0.30),
            ("Kala Chana Thali", "Roti Dough", 0.20),
            ("Kala Chana Thali", "Seasonal Vegetables", 0.12),
            ("Kala Chana Thali", "Sweets", 0.10),
            ("Chana Dal Paneer Thali", "Chana Dal", 0.25),
            ("Chana Dal Paneer Thali", "Paneer", 0.12),
            ("Chana Dal Paneer Thali", "Rice", 0.30),
            ("Chana Dal Paneer Thali", "Roti Dough", 0.20),
            ("Chana Dal Paneer Thali", "Seasonal Vegetables", 0.12),
            ("Chana Dal Paneer Thali", "Sweets", 0.10),
            ("Veg Manchurian & Fried Rice", "Veg Manchurian", 0.22),
            ("Veg Manchurian & Fried Rice", "Fried Rice Mix", 0.40),
            ("Veg Manchurian & Fried Rice", "Salad Ingredients", 0.08),
            ("Kadhi chawal", "Kadhi Base", 0.35),
            ("Kadhi chawal", "Rice", 0.40),
            ("Kadhi chawal", "Salad Ingredients", 0.08),
            ("Rajma Rice", "Rajma", 0.25),
            ("Rajma Rice", "Rice", 0.40),
            ("Rajma Rice", "Salad Ingredients", 0.08),
            ("Veg biryani", "Biryani Mix", 0.45),
            ("Veg biryani", "Salad Ingredients", 0.10),
            ("Matar Kulcha", "Matar", 0.20),
            ("Matar Kulcha", "Kulcha", 2.00),
            ("Matar Kulcha", "Salad Ingredients", 0.08),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO recipes (menu_id,inv_id,qty_per_unit) VALUES (?,?,?)",
            [(menu_ids[name], inv_ids[item], qty) for name,item,qty in recipe_rows if name in menu_ids and item in inv_ids])

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
ORANGE = "#F97316"

T_SAF = "#FFD4A8"; BG_SAF = "#FFF7ED"
T_GRN = "#A7F3D0"; BG_GRN = "#F0FDF4"
T_BLU = "#BFDBFE"; BG_BLU = "#EFF6FF"
T_PUR = "#DDD6FE"; BG_PUR = "#FAF5FF"
T_RED = "#FECACA"; BG_RED = "#FEF2F2"

PAD = 24

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
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkFrame(hdr, fg_color=SAFFRON, width=4, corner_radius=0).pack(
        side="left", fill="y")
    lbl(hdr, f"  {text}", size=12, weight="bold", color=tc).pack(
        side="left", padx=8)

def trow(parent, cols_vals, col_weights, colors=None, bolds=None,
         bg=WHITE, row_h=38, pady=9, padx=16):
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
        self.title("Indian Army Canteen Management System - ENHANCED")
        self.geometry("1360x840")
        self.minsize(1100, 700)
        self.configure(fg_color=LIGHT)
        self._show_login()

    # ── Login ──────────────────────────────────────────────────────────────────
    def _show_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=ARMY_BG)

        bg_canvas = tk.Canvas(self, bg="#1F3320", highlightthickness=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def _draw_bg(event=None):
            bg_canvas.delete("all")
            W = bg_canvas.winfo_width()  or 1360
            H = bg_canvas.winfo_height() or 840
            for x in range(-H, W + H, 110):
                bg_canvas.create_polygon(
                    x, 0, x+55, 0, x+55+H, H, x+H, H,
                    fill="#253D27", outline="")
            for x in range(-H + 62, W + H, 110):
                bg_canvas.create_polygon(
                    x, 0, x+30, 0, x+30+H, H, x+H, H,
                    fill="#192A1C", outline="")

        bg_canvas.bind("<Configure>", _draw_bg)
        self.after(30, _draw_bg)

        top = ctk.CTkFrame(self, fg_color="transparent", height=8)
        top.place(x=0, y=0, relwidth=1)
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
        lbl(hdr, "Enhanced Version - Full Feature",
            size=10, color=GOLD).pack(pady=(3, 12))

        lbl(box, "Staff / Officer Login", size=15, weight="bold",
            color=ARMY_BG).pack(pady=(26, 16))

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
        self._pwd.insert(0, "manager123")
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
        lbl(box, "जय हिन्द  •  Enhanced v4.0  •  SQLite Powered",
            size=10, color="#94A3B8").pack(pady=(8, 22))

    def _do_login(self):
        username = self._uname.get().strip()
        password = self._pwd.get()
        if not username or not password:
            self._login_err.configure(text="⚠  Enter both username and password.")
            return
        with get_db() as conn:
            user = conn.execute(
                "SELECT id, username, name, rank FROM users WHERE username=? AND pw_hash=? AND active=1",
                (username, _hash(password))).fetchone()
            if not user:
                self._login_err.configure(
                    text="⚠  Invalid credentials or user inactive.")
                return
            roles = [r[0] for r in conn.execute(
                "SELECT role FROM user_roles WHERE user_id=?", (user["id"],)).fetchall()]
            if not roles:
                self._login_err.configure(text="⚠  No role assigned to this user.")
                return
            self._current_user = user
            self._current_roles = roles
            self._current_role = ("admin" if "admin" in roles else
                                  "manager" if "manager" in roles else
                                  "waste_mgr" if "waste_mgr" in roles else
                                  roles[0])
        self._show_main()

    # ── Main Shell ─────────────────────────────────────────────────────────────
    def _show_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=LIGHT)

        sb = ctk.CTkFrame(self, fg_color=ARMY_BG, width=258, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        self._sidebar = sb
        tricolor(sb, 5)

        lg = ctk.CTkFrame(sb, fg_color="transparent")
        lg.pack(fill="x", padx=16, pady=(14, 8))
        lbl(lg, "🇮🇳", size=30).pack(side="left", padx=(0, 10))
        tf = ctk.CTkFrame(lg, fg_color="transparent")
        tf.pack(side="left")
        lbl(tf, "INDIAN ARMY", size=12, weight="bold", color=GOLD).pack(anchor="w")
        lbl(tf, "Canteen Management", size=9, color="#7A9A7A").pack(anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=ARMY_SEP).pack(
            fill="x", padx=16, pady=(6, 10))

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
        nav_items = [("📊  Dashboard", "dashboard")]
        if self._current_role in ("admin", "manager"):
            nav_items += [
                ("💰  Sales Entry",  "sales"),
                ("🧑‍🍳  Batch Prep",   "batch"),
                ("📦  Inventory",    "inventory"),
            ]
        if self._current_role in ("admin", "waste_mgr"):
            nav_items += [("♻️  Waste Manager",  "waste")]
        if self._current_role in ("admin", "manager"):
            nav_items += [("📋  Daily Report", "report")]
        if self._current_role == "admin":
            nav_items += [
                ("🧾  Master Data",  "master"),
                ("👥  User Management",  "users"),
            ]

        for icon_txt, page in nav_items:
            b = ctk.CTkButton(sb, text=icon_txt, anchor="w", height=46,
                              font=ctk.CTkFont(size=13, weight="bold"),
                              fg_color="transparent",
                              hover_color=ARMY_HVR, text_color="#8AAA8A",
                              corner_radius=8,
                              command=lambda p=page: self._navigate(p))
            b.pack(padx=12, pady=2, fill="x")
            self._nav_btns[page] = b

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
        lbl(usr, f"👤  {self._current_user['name']}", size=11, weight="bold",
            color=WHITE).pack(padx=12, pady=(10, 1), anchor="w")
        lbl(usr, f"Role: {', '.join(self._current_roles)}", size=9,
            color="#5A7A5A").pack(padx=12, pady=(0, 10), anchor="w")

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
        pages = {
            "dashboard": self._page_dashboard,
            "sales":     self._page_sales,
            "batch":     self._page_batch,
            "inventory": self._page_inventory,
            "waste":     self._page_waste,
            "master":    self._page_master,
            "users":     self._page_users,
            "report":    self._page_report,
        }
        if page in pages:
            pages[page]()

    def _page_header(self, title, subtitle=""):
        hf = ctk.CTkFrame(self._content, fg_color=WHITE,
                          corner_radius=0, height=64)
        hf.pack(fill="x")
        hf.pack_propagate(False)
        ctk.CTkFrame(hf, fg_color=BORDER, height=1,
                     corner_radius=0).pack(side="bottom", fill="x")
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
            waste_rows = conn.execute(
                "SELECT * FROM waste_tracker WHERE date=?", (today,)).fetchall()

        total_rev  = sum(r["sp"] * r["sold"] for r in rows)
        total_cost = sum(r["cogs"] for r in rows)
        net_profit = total_rev - total_cost
        meals_sold = sum(r["sold"] for r in rows)
        low_items  = [i for i in inv_rows if i["stock"] < i["min_lvl"]]
        waste_cost = sum(w["cost_lost"] or 0 for w in waste_rows)

        KPI = [
            ("💰", "Total Revenue",  f"₹{total_rev:,.0f}",  SAFFRON, BG_SAF, T_SAF),
            ("🍛", "Meals Served",   str(meals_sold),       GREEN,   BG_GRN, T_GRN),
            ("📈", "Net Profit",     f"₹{net_profit:,.0f}", BLUE,    BG_BLU, T_BLU),
            ("♻️", "Wastage Cost",   f"₹{waste_cost:,.0f}", ORANGE,  BG_RED, T_RED),
            ("⚠️", "Low Stock",      str(len(low_items)),   RED,     BG_RED, T_RED),
        ]
        kr = ctk.CTkFrame(self._content, fg_color="transparent")
        kr.pack(fill="x", padx=PAD, pady=(18, 0))
        for i, (icon, title, val, color, bg, border) in enumerate(KPI):
            c = ctk.CTkFrame(kr, fg_color=WHITE, corner_radius=14,
                             border_width=1, border_color=border)
            c.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            kr.grid_columnconfigure(i, weight=1)

            ctk.CTkFrame(c, fg_color=color, height=4,
                         corner_radius=0).pack(fill="x")
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

        bot = ctk.CTkFrame(self._content, fg_color="transparent")
        bot.pack(fill="both", expand=True, padx=PAD, pady=(14, PAD))
        bot.grid_columnconfigure(0, weight=6)
        bot.grid_columnconfigure(1, weight=4)
        bot.grid_rowconfigure(0, weight=1)

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

        tot = ctk.CTkFrame(sc, fg_color=BG_SAF, corner_radius=0, height=38)
        tot.pack(fill="x")
        tot.pack_propagate(False)
        for j, (v, c2, wt) in enumerate(zip(
                ["TOTAL", str(meals_sold), "—", f"₹{total_rev:,.0f}", ""],
                [SAFFRON, MID, MID, SAFFRON, DARK], WTS)):
            lbl(tot, v, size=12, weight="bold", color=c2).grid(
                row=0, column=j, padx=16, sticky="w")
            tot.grid_columnconfigure(j, weight=wt)

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

    # ══════════════════════════════════════════════════════════════════════════
    # SIMPLE SALES ENTRY - Just select item + qty sold
    # ══════════════════════════════════════════════════════════════════════════
    def _page_sales(self):
        self._page_header("💰  Daily Sales Entry",
                          datetime.now().strftime("📅  %d %B %Y  •  Simple & Fast"))

        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(16, PAD))

        mc = card(wrap)
        mc.pack(fill="x", pady=(0, 16))
        band(mc, "🍽  Quick Sales Entry")
        lbl(mc, "  Select menu item and enter quantity sold. Stock & costs auto-deducted!",
            size=12, color=MID).pack(anchor="w", padx=16, pady=(10, 6))

        with get_db() as conn:
            meals = conn.execute(
                "SELECT id, name, sp FROM menu WHERE active=1 ORDER BY name").fetchall()

        self._simple_sales = {}
        COLS = [("Menu Item", 4), ("Sale Price", 1), ("Qty Sold", 1), ("Total", 1)]
        thead(mc, COLS, bg=STRIPE, tc=MID)

        for idx, meal in enumerate(meals):
            menu_id, name, sp = meal["id"], meal["name"], meal["sp"]
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(mc, fg_color=bg2, corner_radius=0, height=46)
            rf.pack(fill="x")
            rf.pack_propagate(False)

            icon = "🍛" if "Thali" in name or "Biryani" in name else "🍽️"
            lbl(rf, f"  {icon}  {name}", size=13, weight="bold",
                color=DARK).grid(row=0, column=0, padx=16, sticky="w", pady=5)
            lbl(rf, f"₹{sp:.0f}", size=12, weight="bold", color=MID).grid(
                row=0, column=1, sticky="w", pady=5)

            e_qty = ctk.CTkEntry(rf, height=32, width=60, corner_radius=8,
                                placeholder_text="0",
                                font=ctk.CTkFont(size=12),
                                border_color=BORDER)
            e_qty.grid(row=0, column=2, padx=10, sticky="ew", pady=5)
            rf.grid_columnconfigure(2, weight=1)

            lbl_total = lbl(rf, "₹0", size=12, weight="bold", color=GREEN)
            lbl_total.grid(row=0, column=3, sticky="w", padx=16, pady=5)

            def update_total(event=None, qty_entry=e_qty, lbl_t=lbl_total, price=sp):
                try:
                    q = int(qty_entry.get() or 0)
                    lbl_t.configure(text=f"₹{q*price:,.0f}")
                except:
                    lbl_t.configure(text="₹0")

            e_qty.bind("<KeyRelease>", update_total)
            self._simple_sales[menu_id] = (name, sp, e_qty)

        pc = card(wrap)
        pc.pack(fill="x", pady=(0, 16))
        band(pc, "💳  Payment Mode")
        pf = ctk.CTkFrame(pc, fg_color="transparent")
        pf.pack(fill="x", padx=20, pady=18)
        lbl(pf, "Payment Mode:", size=12, weight="bold", color=MID).grid(
            row=0, column=0, sticky="w")
        self._sales_payment_mode = ctk.CTkOptionMenu(
            pf, values=["Cash", "UPI", "Card"], command=lambda v: None)
        self._sales_payment_mode.set("Cash")
        self._sales_payment_mode.grid(row=0, column=1, padx=(12, 0), sticky="w")
        pf.grid_columnconfigure(1, weight=1)

        bf = ctk.CTkFrame(wrap, fg_color="transparent")
        bf.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(bf, text="✅  Save & Auto-Deduct Stock",
                      height=52, corner_radius=12,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=self._save_simple_sales
                      ).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ctk.CTkButton(bf, text="📋  View Report",
                      height=52, corner_radius=12,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=lambda: self._navigate("report")
                      ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    def _save_simple_sales(self):
        today = datetime.now().strftime("%Y-%m-%d")
        found = False
        payment_mode = self._sales_payment_mode.get() if hasattr(self, '_sales_payment_mode') else "Cash"

        with get_db() as conn:
            for menu_id, (meal, sp, qty_entry) in self._simple_sales.items():
                try:
                    sold = int(qty_entry.get() or 0)
                except ValueError:
                    self._popup("Invalid entry", "Please enter whole numbers only.")
                    return

                if sold <= 0:
                    continue

                found = True
                recipe_rows = conn.execute(
                    "SELECT inv_id, qty_per_unit FROM recipes WHERE menu_id=?",
                    (menu_id,)).fetchall()

                cost_per_unit = 0
                for recipe in recipe_rows:
                    inv = conn.execute(
                        "SELECT cp, stock FROM inventory WHERE id=?",
                        (recipe["inv_id"],)).fetchone()
                    if inv is None:
                        continue
                    cost_per_unit += recipe["qty_per_unit"] * inv["cp"]
                    deduction = recipe["qty_per_unit"] * sold
                    conn.execute(
                        "UPDATE inventory SET stock = stock - ? WHERE id=?",
                        (deduction, recipe["inv_id"]))

                conn.execute(
                    "INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment) VALUES (?,?,?,?,?,?,?,?)",
                    (today, menu_id, meal, sp, sold, 0, sold * cost_per_unit, payment_mode))

        if not found:
            self._popup("No sales entered", "Enter at least one quantity sold.")
            return

        self._popup("✅  Sales Saved!",
                    "Sales recorded and inventory auto-deducted based on recipes.")
        # Clear entries
        for menu_id, (meal, sp, qty_entry) in self._simple_sales.items():
            qty_entry.delete(0, "end")

    # ══════════════════════════════════════════════════════════════════════════
    # BATCH PREPARATION - 2 Section: Prep + Sales
    # ══════════════════════════════════════════════════════════════════════════
    def _page_batch(self):
        self._page_header("🧑‍🍳  Batch Preparation & Tracking",
                          datetime.now().strftime("📅  %d %B %Y"))

        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(16, PAD))

        # ── SECTION 1: BATCH PREPARATION ───────────────────────────────────────
        bc = card(wrap)
        bc.pack(fill="x", pady=(0, 16))
        band(bc, "SECTION 1: Batch Preparation")
        lbl(bc, "  Record quantities prepared. Stock will be auto-deducted.",
            size=12, color=MID).pack(anchor="w", padx=16, pady=(10, 6))

        with get_db() as conn:
            meals = conn.execute(
                "SELECT id, name FROM menu WHERE active=1 ORDER BY name").fetchall()

        self._batch_entries = {}
        COLS1 = [("Menu Item", 3), ("Qty to Prepare", 1)]
        thead(bc, COLS1, bg=STRIPE, tc=MID)

        for idx, meal in enumerate(meals):
            menu_id, name = meal["id"], meal["name"]
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(bc, fg_color=bg2, corner_radius=0, height=46)
            rf.pack(fill="x")
            rf.pack_propagate(False)

            lbl(rf, f"  {name}", size=13, weight="bold",
                color=DARK).grid(row=0, column=0, padx=16, sticky="w", pady=5)

            e = ctk.CTkEntry(rf, height=32, corner_radius=8,
                           placeholder_text="0",
                           font=ctk.CTkFont(size=12),
                           border_color=BORDER)
            e.grid(row=0, column=1, padx=16, sticky="ew", pady=5)
            rf.grid_columnconfigure(1, weight=1)

            self._batch_entries[menu_id] = (name, e)

        # ── SECTION 2: SALES ────────────────────────────────────────────────────
        sc = card(wrap)
        sc.pack(fill="x", pady=(0, 16))
        band(sc, "SECTION 2: Sales from Batch")
        lbl(sc, "  Record sales and wastage from the prepared batch.",
            size=12, color=MID).pack(anchor="w", padx=16, pady=(10, 6))

        self._batch_sales = {}
        COLS2 = [("Menu Item", 2), ("Qty Sold", 1), ("Wastage", 1), ("Payment", 1)]
        thead(sc, COLS2, bg=STRIPE, tc=MID)

        for idx, meal in enumerate(meals):
            menu_id, name = meal["id"], meal["name"]
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg2, corner_radius=0, height=46)
            rf.pack(fill="x")
            rf.pack_propagate(False)

            lbl(rf, f"  {name}", size=13, weight="bold",
                color=DARK).grid(row=0, column=0, padx=16, sticky="w", pady=5)

            e_sold = ctk.CTkEntry(rf, height=32, corner_radius=8,
                                placeholder_text="0",
                                font=ctk.CTkFont(size=11),
                                border_color=BORDER)
            e_sold.grid(row=0, column=1, padx=6, sticky="ew", pady=5)

            e_waste = ctk.CTkEntry(rf, height=32, corner_radius=8,
                                 placeholder_text="0",
                                 font=ctk.CTkFont(size=11),
                                 border_color=T_RED)
            e_waste.grid(row=0, column=2, padx=6, sticky="ew", pady=5)

            pm = ctk.CTkOptionMenu(rf, values=["Cash", "UPI", "Card"])
            pm.set("Cash")
            pm.grid(row=0, column=3, padx=6, sticky="ew", pady=5)

            for i in range(1, 4):
                rf.grid_columnconfigure(i, weight=1)

            self._batch_sales[menu_id] = (name, e_sold, e_waste, pm)

        bf = ctk.CTkFrame(wrap, fg_color="transparent")
        bf.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(bf, text="✅  Save Batch Prep & Sales",
                      height=52, corner_radius=12,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=self._save_batch_and_sales
                      ).pack(fill="x")

    def _save_batch_and_sales(self):
        today = datetime.now().strftime("%Y-%m-%d")
        found_prep = False
        found_sales = False

        with get_db() as conn:
            # Save batch preparations
            for menu_id, (name, qty_entry) in self._batch_entries.items():
                try:
                    prepared = int(qty_entry.get() or 0)
                except ValueError:
                    self._popup("Invalid entry", "Please enter whole numbers only.")
                    return

                if prepared <= 0:
                    continue

                found_prep = True
                conn.execute(
                    "INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                    (today, menu_id, prepared))

                recipe_rows = conn.execute(
                    "SELECT inv_id, qty_per_unit FROM recipes WHERE menu_id=?",
                    (menu_id,)).fetchall()

                for recipe in recipe_rows:
                    inv = conn.execute(
                        "SELECT cp FROM inventory WHERE id=?",
                        (recipe["inv_id"],)).fetchone()
                    if inv:
                        deduction = recipe["qty_per_unit"] * prepared
                        conn.execute(
                            "UPDATE inventory SET stock = stock - ? WHERE id=?",
                            (deduction, recipe["inv_id"]))

            # Save sales from batch
            for menu_id, (name, e_sold, e_waste, pm) in self._batch_sales.items():
                try:
                    sold = int(e_sold.get() or 0)
                    waste = int(e_waste.get() or 0)
                except ValueError:
                    self._popup("Invalid entry", "Please enter whole numbers only.")
                    return

                if sold <= 0 and waste <= 0:
                    continue

                found_sales = True
                menu_row = conn.execute(
                    "SELECT sp FROM menu WHERE id=?", (menu_id,)).fetchone()
                if not menu_row:
                    continue

                sp = menu_row["sp"]
                recipe_rows = conn.execute(
                    "SELECT inv_id, qty_per_unit FROM recipes WHERE menu_id=?",
                    (menu_id,)).fetchall()

                cost_per_unit = sum(
                    r["qty_per_unit"] * conn.execute(
                        "SELECT cp FROM inventory WHERE id=?", (r["inv_id"],)
                    ).fetchone()["cp"]
                    for r in recipe_rows
                )

                payment = pm.get()
                conn.execute(
                    "INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment) VALUES (?,?,?,?,?,?,?,?)",
                    (today, menu_id, name, sp, sold, waste, (sold + waste) * cost_per_unit, payment))

        if not found_prep and not found_sales:
            self._popup("No data entered", "Enter batch prep or sales data.")
            return

        msg = "Batch & Sales Saved! "
        if found_prep:
            msg += "✓ Batch prep recorded & stock deducted. "
        if found_sales:
            msg += "✓ Sales recorded."

        self._popup("✅  Saved Successfully!", msg)

        for menu_id, (name, qty_entry) in self._batch_entries.items():
            qty_entry.delete(0, "end")
        for menu_id, (name, e_sold, e_waste, pm) in self._batch_sales.items():
            e_sold.delete(0, "end")
            e_waste.delete(0, "end")

    # ══════════════════════════════════════════════════════════════════════════
    # WASTE MANAGER - Dedicated section
    # ══════════════════════════════════════════════════════════════════════════
    def _page_waste(self):
        self._page_header("♻️  Waste Management",
                          datetime.now().strftime("📅  %d %B %Y"))

        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(16, PAD))

        # Record waste form
        wc = card(wrap)
        wc.pack(fill="x", pady=(0, 16))
        band(wc, "Record Wastage")
        lbl(wc, "  Log food items wasted with reason and cost.",
            size=12, color=MID).pack(anchor="w", padx=16, pady=(10, 6))

        ff = ctk.CTkFrame(wc, fg_color="transparent")
        ff.pack(fill="x", padx=20, pady=16)

        # Item name
        lbl(ff, "Item Name", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0, 6))
        self._waste_item = ctk.CTkEntry(ff, height=40, corner_radius=10,
                                       placeholder_text="e.g., Rice, Vegetables, Dal",
                                       font=ctk.CTkFont(size=12))
        self._waste_item.pack(fill="x", pady=(0, 14))

        # Quantity
        lbl(ff, "Quantity Wasted (kg/pcs)", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0, 6))
        self._waste_qty = ctk.CTkEntry(ff, height=40, corner_radius=10,
                                      placeholder_text="e.g., 2.5",
                                      font=ctk.CTkFont(size=12))
        self._waste_qty.pack(fill="x", pady=(0, 14))

        # Reason
        lbl(ff, "Reason for Wastage", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0, 6))
        self._waste_reason = ctk.CTkOptionMenu(ff, values=[
            "Spoilage",
            "Preparation Error",
            "Plate Waste",
            "Burn/Over-cooked",
            "Storage Issue",
            "Customer Return",
            "Expiry",
            "Other"
        ])
        self._waste_reason.set("Spoilage")
        self._waste_reason.pack(fill="x", pady=(0, 14))

        # Cost
        lbl(ff, "Estimated Cost (₹)", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0, 6))
        self._waste_cost = ctk.CTkEntry(ff, height=40, corner_radius=10,
                                       placeholder_text="e.g., 150",
                                       font=ctk.CTkFont(size=12))
        self._waste_cost.pack(fill="x", pady=(0, 14))

        ctk.CTkButton(wc, text="✅  Record Waste",
                      height=48, corner_radius=12,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=ORANGE, hover_color="#EA580C",
                      command=self._save_waste
                      ).pack(fill="x", padx=20, pady=(0, 16))

        # Today's waste log
        lc = card(wrap)
        lc.pack(fill="both", expand=True, pady=(0, 0))
        band(lc, "Today's Waste Log")

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            waste_rows = conn.execute(
                "SELECT * FROM waste_tracker WHERE date=? ORDER BY id DESC",
                (today,)).fetchall()

        if not waste_rows:
            lbl(lc, "✅  No wastage recorded today.",
                size=12, color=GREEN).pack(pady=20)
        else:
            COLS = [("Item", 2), ("Qty", 1), ("Reason", 2), ("Cost", 1)]
            thead(lc, COLS, bg=STRIPE, tc=MID)

            total_waste_cost = 0
            for idx, waste in enumerate(waste_rows):
                bg2 = WHITE if idx % 2 == 0 else STRIPE
                total_waste_cost += waste["cost_lost"] or 0
                trow(lc,
                     [waste["item"], f"{waste['qty_wasted']:.1f}",
                      waste["reason"], f"₹{waste['cost_lost']:.0f}"],
                     [2, 1, 2, 1], bg=bg2)

            tot_waste = ctk.CTkFrame(lc, fg_color=BG_RED, corner_radius=0, height=38)
            tot_waste.pack(fill="x")
            tot_waste.pack_propagate(False)
            lbl(tot_waste, "TOTAL WASTAGE COST", size=12, weight="bold",
                color=RED).grid(row=0, column=0, padx=16, sticky="w")
            lbl(tot_waste, f"₹{total_waste_cost:,.0f}", size=14, weight="bold",
                color=RED).grid(row=0, column=3, padx=16, sticky="e")
            tot_waste.grid_columnconfigure(1, weight=1)
            tot_waste.grid_columnconfigure(2, weight=1)

    def _save_waste(self):
        item = self._waste_item.get().strip()
        try:
            qty = float(self._waste_qty.get())
            cost = float(self._waste_cost.get())
        except ValueError:
            self._popup("Invalid entry", "Enter numeric values for quantity and cost.")
            return

        if not item or qty <= 0 or cost < 0:
            self._popup("Invalid entry", "Fill all fields with valid values.")
            return

        reason = self._waste_reason.get()
        today = datetime.now().strftime("%Y-%m-%d")
        recorded_by = self._current_user["name"]

        with get_db() as conn:
            conn.execute(
                "INSERT INTO waste_tracker (date, item, qty_wasted, reason, cost_lost, recorded_by) VALUES (?,?,?,?,?,?)",
                (today, item, qty, reason, cost, recorded_by))

        self._popup("✅  Waste Recorded!", f"✓ {item} ({qty}) logged as {reason}")

        self._waste_item.delete(0, "end")
        self._waste_qty.delete(0, "end")
        self._waste_cost.delete(0, "end")
        self._waste_reason.set("Spoilage")

        self._navigate("waste")

    # ══════════════════════════════════════════════════════════════════════════
    # INVENTORY
    # ══════════════════════════════════════════════════════════════════════════
    def _page_inventory(self):
        hf = self._page_header("📦  Inventory Ledger",
                               datetime.now().strftime("📅  %d %B %Y"))

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

        ab = ctk.CTkFrame(self._content, fg_color="transparent")
        ab.pack(fill="x", padx=PAD, pady=(12, 0))
        ctk.CTkButton(ab, text="＋  Add Stock",
                      height=38, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN, width=170,
                      command=self._add_stock_dialog
                      ).pack(side="left")
        ctk.CTkButton(ab, text="✏️  Update Stock",
                      height=38, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=BLUE, hover_color=BG_BLU, width=170,
                      command=self._update_stock_dialog
                      ).pack(side="left", padx=10)
        ctk.CTkButton(ab, text="🗑  Remove Item",
                      height=38, corner_radius=8,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=RED, hover_color=DRED, width=170,
                      command=self._remove_stock_dialog
                      ).pack(side="left", padx=10)

        tc = card(self._content)
        tc.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        INV_COLS = [("Item", 4), ("Category", 2), ("Unit", 1),
                    ("Stock", 1), ("Min Level", 1), ("Status", 2)]
        INV_WTS = [w for _, w in INV_COLS]

        thead(tc, INV_COLS)

        self._inv_body = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_body.pack(fill="both", expand=True)
        self._inv_wts = INV_WTS

        with get_db() as conn:
            data = conn.execute("SELECT * FROM inventory ORDER BY cat, item").fetchall()
        self._render_inv_rows(list(data))

    def _filter_inv(self, cat):
        for c2, b in self._filter_btns.items():
            b.configure(fg_color=ARMY_BG if c2 == cat else STRIPE,
                        text_color=WHITE if c2 == cat else DARK)
        for w in self._inv_body.winfo_children():
            w.destroy()
        with get_db() as conn:
            if cat == "All":
                data = conn.execute("SELECT * FROM inventory ORDER BY cat, item").fetchall()
            else:
                data = conn.execute(
                    "SELECT * FROM inventory WHERE cat=? ORDER BY item", (cat,)).fetchall()
        self._render_inv_rows(list(data))

    def _render_inv_rows(self, data):
        cat_icon = {"Dry": "🌾", "Fresh": "🥦", "Dairy": "🥛", "Packaging": "📦"}
        for idx, item in enumerate(data):
            is_low = item["stock"] < item["min_lvl"]
            bg2 = BG_RED if is_low else (WHITE if idx % 2 == 0 else STRIPE)
            ci = cat_icon.get(item["cat"], "•")
            vals = [
                f"  {item['item']}",
                f"{ci}  {item['cat']}",
                item["unit"],
                f"{item['stock']:.1f}",
                f"{item['min_lvl']:.1f}",
                "⚠  LOW" if is_low else "✓  OK"
            ]
            clrs = [DARK, MID, MID, DARK, MID, RED if is_low else GREEN]
            blds = [True, False, False, False, False, True]
            trow(self._inv_body, vals, self._inv_wts,
                 colors=clrs, bolds=blds, bg=bg2, row_h=40)

    def _add_stock_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Received Stock")
        win.geometry("500x360")
        win.resizable(False, False)
        win.configure(fg_color=WHITE)

        with get_db() as conn:
            items = sorted([row["item"] for row in conn.execute(
                "SELECT DISTINCT item FROM inventory ORDER BY item").fetchall()])

        lbl(win, "Select Item", size=12, weight="bold", color=ARMY_BG).pack(pady=(20, 6), padx=24, anchor="w")
        item_menu = ctk.CTkOptionMenu(win, values=items)
        item_menu.set(items[0] if items else "")
        item_menu.pack(padx=24, fill="x", pady=(0, 14))

        lbl(win, "Quantity Received (kg/pcs)", size=12, weight="bold", color=ARMY_BG).pack(pady=(0, 6), padx=24, anchor="w")
        qty_entry = ctk.CTkEntry(win, height=40, corner_radius=10,
                                placeholder_text="e.g., 25.5",
                                font=ctk.CTkFont(size=12))
        qty_entry.pack(padx=24, fill="x", pady=(0, 14))

        lbl(win, "Cost per Unit (₹)", size=12, weight="bold", color=ARMY_BG).pack(pady=(0, 6), padx=24, anchor="w")
        cost_entry = ctk.CTkEntry(win, height=40, corner_radius=10,
                                 placeholder_text="e.g., 40",
                                 font=ctk.CTkFont(size=12))
        cost_entry.pack(padx=24, fill="x")

        def save_stock():
            try:
                qty = float(qty_entry.get())
                cost = float(cost_entry.get())
            except ValueError:
                self._popup("Invalid entry", "Enter numeric values.")
                return
            if qty <= 0 or cost < 0:
                self._popup("Invalid values", "Quantity must be positive.")
                return

            item = item_menu.get()
            with get_db() as conn:
                conn.execute(
                    "UPDATE inventory SET stock = stock + ?, received = received + ?, cp = ? WHERE item=?",
                    (qty, qty, cost, item))
                inv_id = conn.execute("SELECT id FROM inventory WHERE item=?", (item,)).fetchone()[0]
                conn.execute(
                    "INSERT INTO goods_received (date, inv_id, qty, total_cost) VALUES (?,?,?,?)",
                    (datetime.now().strftime("%Y-%m-%d"), inv_id, qty, qty * cost))

            self._popup("✅  Stock Added!", f"✓ {item}: +{qty} @ ₹{cost}/unit")
            win.destroy()
            self._navigate("inventory")

        ctk.CTkButton(win, text="✅  Save Receipt", fg_color=GREEN, hover_color=DGREEN,
                      height=48, font=ctk.CTkFont(size=12, weight="bold"),
                      command=save_stock).pack(pady=22, padx=24, fill="x")

    def _update_stock_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Update Stock Level")
        win.geometry("500x280")
        win.resizable(False, False)
        win.configure(fg_color=WHITE)

        with get_db() as conn:
            items = sorted([row["item"] for row in conn.execute(
                "SELECT DISTINCT item FROM inventory ORDER BY item").fetchall()])

        lbl(win, "Select Item", size=12, weight="bold", color=ARMY_BG).pack(pady=(20, 6), padx=24, anchor="w")
        item_menu = ctk.CTkOptionMenu(win, values=items)
        item_menu.set(items[0] if items else "")
        item_menu.pack(padx=24, fill="x", pady=(0, 14))

        lbl(win, "New Stock Level", size=12, weight="bold", color=ARMY_BG).pack(pady=(0, 6), padx=24, anchor="w")
        qty_entry = ctk.CTkEntry(win, height=40, corner_radius=10,
                                placeholder_text="e.g., 50",
                                font=ctk.CTkFont(size=12))
        qty_entry.pack(padx=24, fill="x")

        def update_level():
            try:
                qty = float(qty_entry.get())
            except ValueError:
                self._popup("Invalid entry", "Enter numeric value.")
                return
            if qty < 0:
                self._popup("Invalid value", "Stock cannot be negative.")
                return

            item = item_menu.get()
            with get_db() as conn:
                conn.execute(
                    "UPDATE inventory SET stock = ? WHERE item=?",
                    (qty, item))

            self._popup("✅  Stock Updated!", f"✓ {item}: {qty}")
            win.destroy()
            self._navigate("inventory")

        ctk.CTkButton(win, text="✅  Update", fg_color=BLUE, hover_color=BG_BLU,
                      height=48, font=ctk.CTkFont(size=12, weight="bold"),
                      command=update_level).pack(pady=22, padx=24, fill="x")

    def _remove_stock_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Remove Stock Item")
        win.geometry("500x280")
        win.resizable(False, False)
        win.configure(fg_color=WHITE)

        with get_db() as conn:
            items = sorted([row["item"] for row in conn.execute(
                "SELECT DISTINCT item FROM inventory ORDER BY item").fetchall()])

        lbl(win, "Select Item to Remove", size=12, weight="bold", color=ARMY_BG).pack(pady=(20, 6), padx=24, anchor="w")
        item_menu = ctk.CTkOptionMenu(win, values=items)
        item_menu.set(items[0] if items else "")
        item_menu.pack(padx=24, fill="x", pady=(0, 20))

        lbl(win, "⚠️  This will delete the inventory item permanently.", size=10, color=RED).pack(padx=24, anchor="w", pady=(0, 20))

        def remove_item():
            item = item_menu.get()
            with get_db() as conn:
                conn.execute("DELETE FROM inventory WHERE item=?", (item,))

            self._popup("✅  Item Removed!", f"✓ {item} deleted from inventory")
            win.destroy()
            self._navigate("inventory")

        ctk.CTkButton(win, text="🗑  Remove Item", fg_color=RED, hover_color=DRED,
                      height=48, font=ctk.CTkFont(size=12, weight="bold"),
                      command=remove_item).pack(pady=22, padx=24, fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # DAILY REPORT
    # ══════════════════════════════════════════════════════════════════════════
    def _page_report(self):
        hf = self._page_header("📋  Comprehensive Daily Report",
                               datetime.now().strftime("📅  %d %B %Y"))

        if not hasattr(self, '_report_period'):
            self._report_period = '7d'

        period_map = {'7d': 7, '15d': 15, '30d': 30, '90d': 90}
        days = period_map.get(self._report_period, 7)
        start_date = (datetime.now() - timedelta(days=days-1)).strftime('%Y-%m-%d')

        with get_db() as conn:
            s_rows = conn.execute(
                "SELECT * FROM sales WHERE date>=? ORDER BY date DESC", (start_date,)).fetchall()
            e_rows = conn.execute(
                "SELECT category, SUM(amount) AS total FROM expenditure WHERE date>=? GROUP BY category",
                (start_date,)).fetchall()
            w_rows = conn.execute(
                "SELECT SUM(cost_lost) AS total FROM waste_tracker WHERE date>=?", (start_date,)).fetchone()

        total_rev   = sum(r["sp"] * r["sold"] for r in s_rows)
        total_cogs  = sum(r["cogs"] for r in s_rows)
        gross_profit = total_rev - total_cogs
        total_exp   = sum(r["total"] or 0 for r in e_rows)
        waste_cost  = w_rows["total"] or 0
        net_profit  = gross_profit - total_exp - waste_cost
        meals_tot   = sum(r["sold"] for r in s_rows)
        cash_a      = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"] == "Cash")
        upi_a       = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"] == "UPI")
        card_a      = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"] == "Card")

        period_bar = ctk.CTkFrame(self._content, fg_color="transparent")
        period_bar.pack(fill="x", padx=PAD, pady=(12, 0))
        for code, label in [("7d", "1 Week"), ("15d", "Fortnight"),
                            ("30d", "Monthly"), ("90d", "Quarterly")]:
            btn = ctk.CTkButton(period_bar, text=label, width=120, height=36,
                                corner_radius=12,
                                fg_color=SAFFRON if self._report_period == code else STRIPE,
                                text_color=ARMY_BG if self._report_period == code else DARK,
                                hover_color=ARMY_HVR,
                                command=lambda p=code: self._set_report_period(p))
            btn.pack(side="left", padx=(0 if code == "7d" else 10, 0))

        kpi_bar = ctk.CTkFrame(self._content, fg_color="transparent")
        kpi_bar.pack(fill="x", padx=PAD, pady=(14, 0))
        kpi_bar.grid_rowconfigure(0, weight=1)
        for i, (icon, title, val, bg_c, bdr_c, tc) in enumerate([
                ("💰", "Total Revenue",    f"₹ {total_rev:,.0f}",  BG_GRN, T_GRN, GREEN),
                ("🍽", "Meals Served",     str(meals_tot),         BG_SAF, T_SAF, SAFFRON),
                ("📈", "Net Profit",       f"₹ {net_profit:,.0f}", BG_BLU, T_BLU, BLUE),
        ]):
            kc = card(kpi_bar, fg_color=bg_c, border_color=bdr_c)
            kc.grid(row=0, column=i, padx=(0 if i == 0 else 12), sticky="nsew")
            kpi_bar.grid_columnconfigure(i, weight=1)
            rf2 = ctk.CTkFrame(kc, fg_color="transparent")
            rf2.pack(fill="x", padx=20, pady=16)
            lbl(rf2, icon, size=30).pack(side="left", padx=(0, 14))
            info = ctk.CTkFrame(rf2, fg_color="transparent")
            info.pack(side="left")
            lbl(info, title, size=11, color=MID).pack(anchor="w")
            lbl(info, val,   size=22, weight="bold", color=tc).pack(anchor="w")

        scroll = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        rc = card(scroll, border_width=2)
        rc.pack(fill="x", pady=(0, 14))

        lh = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=90)
        lh.pack(fill="x")
        lh.pack_propagate(False)
        tricolor(lh, 5)
        lh_i = ctk.CTkFrame(lh, fg_color="transparent")
        lh_i.pack(fill="both", expand=True, padx=PAD, pady=8)
        lbl(lh_i, "🇮🇳  56 APO FIELD CANTEEN — INDIAN ARMY",
            size=11, weight="bold", color=GOLD_LT).pack(anchor="w")
        lbl(lh_i, "COMPREHENSIVE OPERATIONS REPORT",
            size=17, weight="bold", color=WHITE).pack(anchor="w", pady=(2, 0))
        lbl(lh_i, "Period: " + start_date + " to " + datetime.now().strftime("%Y-%m-%d"),
            size=10, color=GOLD).pack(anchor="w")

        # Sales section
        sc1 = ctk.CTkFrame(rc, fg_color="transparent")
        sc1.pack(fill="x", padx=PAD, pady=(20, 0))
        band(sc1, "Sales Summary", bg=ARMY_BG, tc=GOLD_LT, h=42)
        SALE_COLS = [("Date", 2), ("Meals", 1), ("Revenue", 2), ("COGS", 1), ("Profit", 1)]
        thead(sc1, SALE_COLS, bg=STRIPE, tc=MID)

        grouped_sales = {}
        for row in s_rows:
            date = row["date"]
            if date not in grouped_sales:
                grouped_sales[date] = {"meals": 0, "rev": 0, "cogs": 0}
            grouped_sales[date]["meals"] += row["sold"]
            grouped_sales[date]["rev"] += row["sp"] * row["sold"]
            grouped_sales[date]["cogs"] += row["cogs"]

        for idx, (date, data) in enumerate(sorted(grouped_sales.items(), reverse=True)):
            bg2 = WHITE if idx % 2 == 0 else STRIPE
            profit = data["rev"] - data["cogs"]
            trow(sc1,
                 [date, str(data["meals"]), f"₹{data['rev']:,.0f}",
                  f"₹{data['cogs']:,.0f}", f"₹{profit:,.0f}"],
                 [2, 1, 2, 1, 1], bg=bg2)

        tot_row = ctk.CTkFrame(sc1, fg_color=BG_SAF, corner_radius=0, height=38)
        tot_row.pack(fill="x")
        tot_row.pack_propagate(False)
        for j, (v, wt) in enumerate(zip(
                ["TOTAL", str(meals_tot), f"₹{total_rev:,.0f}",
                 f"₹{total_cogs:,.0f}", f"₹{gross_profit:,.0f}"],
                [2, 1, 2, 1, 1])):
            lbl(tot_row, v, size=12, weight="bold",
                color=SAFFRON if j in [0, 4] else MID).grid(
                row=0, column=j, padx=16, sticky="w")
            tot_row.grid_columnconfigure(j, weight=wt)

        # Financial summary
        fin_f = ctk.CTkFrame(rc, fg_color="transparent")
        fin_f.pack(fill="x", padx=PAD, pady=(20, 0))
        fin_f.grid_rowconfigure(0, weight=1)
        for i, (icon, desc, val, tc2, bg_c, bdr) in enumerate([
                ("💰", "Total Revenue",       f"₹ {total_rev:,.0f}",  GREEN,  BG_GRN, T_GRN),
                ("📦", "Total COGS",          f"₹ {total_cogs:,.0f}", RED,    BG_RED, T_RED),
                ("💥", "Waste Cost",          f"₹ {waste_cost:,.0f}", ORANGE, BG_RED, T_RED),
                ("📈", "NET PROFIT (After All)", f"₹ {net_profit:,.0f}", SAFFRON,BG_SAF, T_SAF)]):
            fc = card(fin_f, fg_color=bg_c, border_color=bdr)
            fc.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            fin_f.grid_columnconfigure(i, weight=1)
            lbl(fc, icon, size=22).pack(anchor="w", padx=18, pady=(14, 4))
            lbl(fc, desc, size=11, color=MID).pack(anchor="w", padx=18)
            lbl(fc, val,  size=18, weight="bold", color=tc2).pack(
                anchor="w", padx=18, pady=(2, 14))

        # Payment breakdown
        pm_f = ctk.CTkFrame(rc, fg_color="transparent")
        pm_f.pack(fill="x", padx=PAD, pady=(20, 0))
        pm_f.grid_rowconfigure(0, weight=1)
        for i, (mode, amt, pct, clr, bg_c, bdr) in enumerate([
                ("💵  Cash", f"₹ {cash_a:,.0f}",
                 f"{cash_a/total_rev*100:.0f}%" if total_rev else "0%",
                 GREEN, BG_GRN, T_GRN),
                ("📱  UPI",  f"₹ {upi_a:,.0f}",
                 f"{upi_a/total_rev*100:.0f}%" if total_rev else "0%",
                 PURPLE, BG_PUR, T_PUR),
                ("💳  Card", f"₹ {card_a:,.0f}",
                 f"{card_a/total_rev*100:.0f}%" if total_rev else "0%",
                 BLUE, BG_BLU, T_BLU)]):
            pc = card(pm_f, fg_color=bg_c, border_color=bdr)
            pc.grid(row=0, column=i, padx=(0 if i == 0 else 10), sticky="nsew")
            pm_f.grid_columnconfigure(i, weight=1)
            lbl(pc, mode, size=13, weight="bold", color=clr).pack(
                padx=18, pady=(14, 4), anchor="w")
            lbl(pc, amt,  size=22, weight="bold", color=clr).pack(
                padx=18, pady=(0, 2), anchor="w")
            lbl(pc, pct,  size=10, color=MID).pack(
                padx=18, pady=(0, 14), anchor="w")

        ft2 = ctk.CTkFrame(rc, fg_color="transparent", height=6)
        ft2.pack(fill="x", pady=(20, 0))
        ft2.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ft2, fg_color=c).pack(side="left", fill="both", expand=True)

        lbl(rc, "जय हिन्द  •  Report Generated: " + datetime.now().strftime("%d %b %Y, %I:%M %p"),
            size=11, color=MID).pack(pady=(8, 16))

    def _set_report_period(self, period):
        self._report_period = period
        self._navigate("report")

    # ══════════════════════════════════════════════════════════════════════════
    # MASTER DATA
    # ══════════════════════════════════════════════════════════════════════════
    def _page_master(self):
        hf = self._page_header("🧾  Master Data Management",
                               "View and manage core masters")

        scroll = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        mc = card(scroll)
        mc.pack(fill="x", pady=(0, 16))
        band(mc, "Inventory Master")
        cols = [("Item", 3), ("Category", 1), ("Unit", 1),
                ("Stock", 1), ("Min Level", 1)]
        thead(mc, cols, bg=STRIPE, tc=DARK)
        with get_db() as conn:
            rows = conn.execute(
                "SELECT item, cat, unit, stock, min_lvl FROM inventory ORDER BY cat, item").fetchall()
        for idx, row in enumerate(rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            trow(mc,
                 [row["item"], row["cat"], row["unit"],
                  f"{row['stock']:.1f}", f"{row['min_lvl']:.1f}"],
                 [3, 1, 1, 1, 1], bg=bg)

        mc2 = card(scroll)
        mc2.pack(fill="x", pady=(0, 0))
        band(mc2, "Menu Master")
        cols2 = [("Menu Item", 4), ("Sale Price", 1), ("Active", 1)]
        thead(mc2, cols2, bg=STRIPE, tc=DARK)
        with get_db() as conn:
            menu_rows = conn.execute(
                "SELECT name, sp, active FROM menu ORDER BY name").fetchall()
        for idx, row in enumerate(menu_rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            trow(mc2,
                 [row["name"], f"₹{row['sp']:.0f}",
                  "Yes" if row["active"] else "No"],
                 [4, 1, 1], bg=bg)

    # ══════════════════════════════════════════════════════════════════════════
    # USER MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════
    def _page_users(self):
        hf = self._page_header("👥  User Management",
                               "Create, edit, and manage user accounts")

        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        ab = ctk.CTkFrame(wrap, fg_color="transparent")
        ab.pack(fill="x", pady=(0, 16))
        ctk.CTkButton(ab, text="＋  Add New User",
                      height=40, corner_radius=10,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=self._add_user_dialog
                      ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(ab, text="🔄  Reset Password",
                      height=40, corner_radius=10,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=BLUE, hover_color=BG_BLU,
                      command=self._reset_password_dialog
                      ).pack(side="left")

        uc = card(wrap)
        uc.pack(fill="both", expand=True)
        band(uc, "Users & Roles")
        cols = [("Username", 2), ("Name", 2), ("Rank", 1), ("Roles", 2), ("Status", 1)]
        thead(uc, cols, bg=STRIPE, tc=DARK)
        with get_db() as conn:
            rows = conn.execute(
                "SELECT u.id, u.username, u.name, u.rank, u.active, GROUP_CONCAT(r.role, ', ') AS roles "
                "FROM users u "
                "LEFT JOIN user_roles r ON r.user_id = u.id "
                "GROUP BY u.id ORDER BY u.username").fetchall()

        for idx, row in enumerate(rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            status_icon = "✅  Active" if row["active"] else "❌  Inactive"
            status_color = GREEN if row["active"] else RED
            trow(uc,
                 [row["username"], row["name"], row["rank"],
                  row["roles"] or "None", status_icon],
                 [2, 2, 1, 2, 1],
                 colors=[DARK, DARK, MID, MID, status_color],
                 bolds=[True, True, False, False, True],
                 bg=bg)

    def _add_user_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Add New User")
        win.geometry("520x480")
        win.resizable(False, False)
        win.configure(fg_color=WHITE)

        fields = {}
        for field, attr, ph in [
            ("Username", "_new_uname", "e.g., jco_smith"),
            ("Full Name", "_new_name", "e.g., JCO Smith"),
            ("Rank", "_new_rank", "e.g., JCO, OR, Subedar"),
            ("Contact", "_new_contact", "e.g., 9876543210"),
            ("Password", "_new_pwd", "e.g., SecurePass123"),
        ]:
            lbl(win, field, size=11, weight="bold", color=ARMY_BG).pack(pady=(12, 4), padx=24, anchor="w")
            e = ctk.CTkEntry(win, height=40, corner_radius=10,
                            placeholder_text=ph,
                            font=ctk.CTkFont(size=11),
                            show="●" if "Password" in field else "")
            e.pack(padx=24, fill="x")
            fields[attr] = e

        lbl(win, "Role", size=11, weight="bold", color=ARMY_BG).pack(pady=(12, 4), padx=24, anchor="w")
        role_menu = ctk.CTkOptionMenu(win, values=["manager", "officer", "waste_mgr"])
        role_menu.set("manager")
        role_menu.pack(padx=24, fill="x")

        def save_user():
            username = fields["_new_uname"].get().strip()
            name = fields["_new_name"].get().strip()
            rank = fields["_new_rank"].get().strip()
            contact = fields["_new_contact"].get().strip()
            password = fields["_new_pwd"].get()
            role = role_menu.get()

            if not all([username, name, rank, password]):
                self._popup("Missing fields", "Fill all required fields.")
                return

            with get_db() as conn:
                try:
                    cur = conn.execute(
                        "INSERT INTO users (username, pw_hash, name, rank, contact) VALUES (?,?,?,?,?)",
                        (username, _hash(password), name, rank, contact))
                    user_id = cur.lastrowid
                    conn.execute("INSERT INTO user_roles (user_id, role) VALUES (?,?)",
                                (user_id, role))
                except sqlite3.IntegrityError:
                    self._popup("Error", "Username already exists!")
                    return

            self._popup("✅  User Created!", f"✓ {username} ({role}) created successfully")
            win.destroy()
            self._navigate("users")

        ctk.CTkButton(win, text="✅  Create User", fg_color=GREEN, hover_color=DGREEN,
                      height=48, font=ctk.CTkFont(size=12, weight="bold"),
                      command=save_user).pack(pady=22, padx=24, fill="x")

    def _reset_password_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Reset Password")
        win.geometry("500x280")
        win.resizable(False, False)
        win.configure(fg_color=WHITE)

        with get_db() as conn:
            users = [row["username"] for row in conn.execute(
                "SELECT username FROM users ORDER BY username").fetchall()]

        lbl(win, "Select User", size=12, weight="bold", color=ARMY_BG).pack(pady=(20, 6), padx=24, anchor="w")
        user_menu = ctk.CTkOptionMenu(win, values=users)
        user_menu.set(users[0] if users else "")
        user_menu.pack(padx=24, fill="x", pady=(0, 14))

        lbl(win, "New Password", size=12, weight="bold", color=ARMY_BG).pack(pady=(0, 6), padx=24, anchor="w")
        pwd_entry = ctk.CTkEntry(win, height=40, corner_radius=10,
                                placeholder_text="Enter new password", show="●",
                                font=ctk.CTkFont(size=12))
        pwd_entry.pack(padx=24, fill="x")

        def reset_pwd():
            username = user_menu.get()
            new_pwd = pwd_entry.get()
            if not new_pwd or len(new_pwd) < 6:
                self._popup("Weak password", "Password must be at least 6 characters.")
                return

            with get_db() as conn:
                conn.execute(
                    "UPDATE users SET pw_hash=? WHERE username=?",
                    (_hash(new_pwd), username))

            self._popup("✅  Password Reset!", f"✓ {username}'s password updated")
            win.destroy()

        ctk.CTkButton(win, text="✅  Reset", fg_color=BLUE, hover_color=BG_BLU,
                      height=48, font=ctk.CTkFont(size=12, weight="bold"),
                      command=reset_pwd).pack(pady=22, padx=24, fill="x")

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
                            ["Saved", "Export", "Created", "Reset", "Removed"]) else "ℹ️"
        lbl(win, icon2, size=36).pack(pady=(20, 6))
        lbl(win, message, size=12, color=DARK, justify="center",
            wraplength=420).pack(pady=(0, 18))
        ctk.CTkButton(win, text="Close", width=120, height=40,
                      corner_radius=10, fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=win.destroy).pack()
        lbl(win, "जय हिन्द", size=10, color=MID).pack(pady=(8, 16))

if __name__ == "__main__":
    app = CanteenApp()
    app.mainloop()
