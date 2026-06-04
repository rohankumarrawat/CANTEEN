"""
Canteen Inventory & Sales Management System — v5.0
Indian Army | 56 APO Field Canteen
Python + CustomTkinter + SQLite + ReportLab PDF
"""

import customtkinter as ctk
from datetime import datetime, timedelta
import sqlite3, os, math, hashlib, shutil, threading
import tkinter as tk
from tkinter import filedialog, messagebox

# ── Try importing ReportLab for PDF ───────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors as RL_COLORS
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, PageBreak, HRFlowable)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "canteen.db")
BCK_DIR  = os.path.join(BASE_DIR, "backups")
os.makedirs(BCK_DIR, exist_ok=True)

# ── Database helpers ───────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _hash(pw): return hashlib.sha256(pw.encode()).hexdigest()

def _has_col(conn, table, col):
    return any(r[1] == col for r in conn.execute(f"PRAGMA table_info({table})"))

def init_db():
    with get_db() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS roles (role TEXT PRIMARY KEY, label TEXT NOT NULL);
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
                category TEXT NOT NULL DEFAULT 'General',
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
            CREATE TABLE IF NOT EXISTS daily_menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                menu_id INTEGER REFERENCES menu(id),
                UNIQUE(day, meal_type)
            );
        """)

        c.executemany("INSERT OR IGNORE INTO roles (role,label) VALUES (?,?)", [
            ("admin","System Admin"), ("manager","Canteen Manager"),
            ("officer","Officer (Read-Only)"), ("waste_mgr","Waste Manager"),
        ])

        if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            for un, pw, role, name, rank in [
                ("admin","admin123","admin","System Administrator","Admin"),
                ("manager","manager123","manager","Canteen Manager","JCO"),
                ("officer","officer123","officer","Officer-in-Charge","Captain"),
            ]:
                cur = c.execute("INSERT INTO users (username,pw_hash,name,rank) VALUES (?,?,?,?)",
                                (un, _hash(pw), name, rank))
                c.execute("INSERT INTO user_roles (user_id,role) VALUES (?,?)", (cur.lastrowid, role))

        c.executemany(
            "INSERT OR IGNORE INTO inventory (item,cat,unit,stock,min_lvl,opening,received,cp) VALUES (?,?,?,?,?,?,?,?)",
            [
                ("Rice","Dry","kg",75,20,75,20,40),
                ("Roti Dough","Dry","kg",25,10,25,5,20),
                ("Seasonal Vegetables","Fresh","kg",40,15,40,20,30),
                ("Salad Ingredients","Fresh","kg",18,6,18,12,15),
                ("Sweets","Dry","kg",10,4,10,5,80),
                ("Panchratna Dal Mix","Dry","kg",12,4,12,6,120),
                ("Kadhi Base","Dry","kg",14,5,14,8,120),
                ("Pakoda Mix","Dry","kg",8,3,8,5,80),
                ("Rajma","Dry","kg",18,5,18,10,150),
                ("Kala Chana","Dry","kg",15,5,15,8,140),
                ("Chana Dal","Dry","kg",16,5,16,8,130),
                ("Paneer","Dairy","kg",12,4,12,6,260),
                ("Mix Veg","Fresh","kg",22,7,22,10,40),
                ("Matar","Dry","kg",12,4,12,8,120),
                ("Kulcha","Bakery","pcs",100,30,100,40,25),
                ("Veg Manchurian","Prepared","kg",10,3,10,6,220),
                ("Fried Rice Mix","Prepared","kg",15,5,15,8,110),
                ("Biryani Mix","Prepared","kg",14,5,14,7,130),
            ])
        c.executemany("INSERT OR IGNORE INTO menu (name,sp,active) VALUES (?,?,1)", [
            ("Panchratna Dal Thali",70), ("Kadhi Pakoda Thali",70),
            ("Rajma Thali",70), ("Kala Chana Thali",70),
            ("Chana Dal Paneer Thali",70), ("Veg Manchurian & Fried Rice",50),
            ("Kadhi Chawal",50), ("Rajma Rice",50),
            ("Veg Biryani",50), ("Matar Kulcha",50),
        ])
        mid = {r[1]: r[0] for r in c.execute("SELECT id,name FROM menu")}
        iid = {r[1]: r[0] for r in c.execute("SELECT id,item FROM inventory")}
        recipes = [
            ("Panchratna Dal Thali","Panchratna Dal Mix",0.22),
            ("Panchratna Dal Thali","Rice",0.30),("Panchratna Dal Thali","Roti Dough",0.20),
            ("Panchratna Dal Thali","Seasonal Vegetables",0.20),
            ("Panchratna Dal Thali","Salad Ingredients",0.12),("Panchratna Dal Thali","Sweets",0.10),
            ("Kadhi Pakoda Thali","Kadhi Base",0.30),("Kadhi Pakoda Thali","Pakoda Mix",0.15),
            ("Kadhi Pakoda Thali","Rice",0.30),("Kadhi Pakoda Thali","Roti Dough",0.20),
            ("Kadhi Pakoda Thali","Seasonal Vegetables",0.18),
            ("Kadhi Pakoda Thali","Salad Ingredients",0.12),("Kadhi Pakoda Thali","Sweets",0.10),
            ("Rajma Thali","Rajma",0.25),("Rajma Thali","Mix Veg",0.22),
            ("Rajma Thali","Rice",0.30),("Rajma Thali","Roti Dough",0.20),
            ("Rajma Thali","Seasonal Vegetables",0.12),("Rajma Thali","Sweets",0.10),
            ("Kala Chana Thali","Kala Chana",0.25),("Kala Chana Thali","Mix Veg",0.22),
            ("Kala Chana Thali","Rice",0.30),("Kala Chana Thali","Roti Dough",0.20),
            ("Kala Chana Thali","Seasonal Vegetables",0.12),("Kala Chana Thali","Sweets",0.10),
            ("Chana Dal Paneer Thali","Chana Dal",0.25),("Chana Dal Paneer Thali","Paneer",0.12),
            ("Chana Dal Paneer Thali","Rice",0.30),("Chana Dal Paneer Thali","Roti Dough",0.20),
            ("Chana Dal Paneer Thali","Seasonal Vegetables",0.12),("Chana Dal Paneer Thali","Sweets",0.10),
            ("Veg Manchurian & Fried Rice","Veg Manchurian",0.22),
            ("Veg Manchurian & Fried Rice","Fried Rice Mix",0.40),
            ("Veg Manchurian & Fried Rice","Salad Ingredients",0.08),
            ("Kadhi Chawal","Kadhi Base",0.35),("Kadhi Chawal","Rice",0.40),
            ("Kadhi Chawal","Salad Ingredients",0.08),
            ("Rajma Rice","Rajma",0.25),("Rajma Rice","Rice",0.40),
            ("Rajma Rice","Salad Ingredients",0.08),
            ("Veg Biryani","Biryani Mix",0.45),("Veg Biryani","Salad Ingredients",0.10),
            ("Matar Kulcha","Matar",0.20),("Matar Kulcha","Kulcha",2.00),
            ("Matar Kulcha","Salad Ingredients",0.08),
        ]
        c.executemany("INSERT OR IGNORE INTO recipes (menu_id,inv_id,qty_per_unit) VALUES (?,?,?)",
                      [(mid[n], iid[i], q) for n,i,q in recipes if n in mid and i in iid])

init_db()

# ── Theme & Palette ────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

SAFFRON   = "#FF9933"
IND_GREEN = "#138808"
GOLD      = "#C9A84C"
GOLD_LT   = "#EDD97A"
ARMY_BG   = "#1F3320"
ARMY_HVR  = "#2C4A2A"
ARMY_SEP  = "#2E4830"
DARK      = "#1E293B"
MID       = "#64748B"
LIGHT     = "#F1F5F1"
WHITE     = "#FFFFFF"
BORDER    = "#DDE8DD"
STRIPE    = "#F5FAF5"
GREEN     = "#059669"; DGREEN = "#047857"
RED       = "#DC2626"; DRED   = "#B91C1C"
BLUE      = "#2563EB"; DBLUE  = "#1D4ED8"
PURPLE    = "#7C3AED"
ORANGE    = "#F97316"
TEAL      = "#0D9488"
T_SAF     = "#FFD4A8"; BG_SAF = "#FFF7ED"
T_GRN     = "#A7F3D0"; BG_GRN = "#F0FDF4"
T_BLU     = "#BFDBFE"; BG_BLU = "#EFF6FF"
T_PUR     = "#DDD6FE"; BG_PUR = "#FAF5FF"
T_RED     = "#FECACA"; BG_RED = "#FEF2F2"
T_TEA     = "#99F6E4"; BG_TEA = "#F0FDFA"
PAD       = 22

# ── Shared widgets ─────────────────────────────────────────────────────────────
def card(parent, **kw):
    d = dict(fg_color=WHITE, corner_radius=14, border_width=1, border_color=BORDER)
    d.update(kw)
    return ctk.CTkFrame(parent, **d)

def lbl(parent, text, size=13, weight="normal", color=DARK, **kw):
    return ctk.CTkLabel(parent, text=text,
                        font=ctk.CTkFont(size=size, weight=weight),
                        text_color=color, **kw)

def btn(parent, text, cmd, fg=ARMY_BG, hv=ARMY_HVR, h=40, w=None, **kw):
    b = ctk.CTkButton(parent, text=text, command=cmd, fg_color=fg, hover_color=hv,
                      height=h, corner_radius=10,
                      font=ctk.CTkFont(size=12, weight="bold"), **kw)
    if w: b.configure(width=w)
    return b

def entry(parent, ph="", show="", h=40, **kw):
    return ctk.CTkEntry(parent, placeholder_text=ph, show=show, height=h,
                        corner_radius=10, font=ctk.CTkFont(size=12),
                        border_color=BORDER, **kw)

def sep(parent, color=ARMY_SEP, h=1, **kw):
    return ctk.CTkFrame(parent, fg_color=color, height=h, corner_radius=0, **kw)

def tricolor(parent, h=5):
    bar = ctk.CTkFrame(parent, fg_color="transparent", height=h)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    for c in (SAFFRON, WHITE, IND_GREEN):
        ctk.CTkFrame(bar, fg_color=c).pack(side="left", fill="both", expand=True)

def band(parent, text, bg=ARMY_BG, tc=GOLD_LT, h=44, side_btn=None):
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkFrame(hdr, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
    lbl(hdr, f"  {text}", size=12, weight="bold", color=tc).pack(side="left", padx=8)
    if side_btn:
        side_btn(hdr)
    return hdr

def thead(parent, col_defs, bg=ARMY_BG, tc=GOLD_LT, h=36, padx=14):
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    for j, (name, wt) in enumerate(col_defs):
        lbl(hdr, name, size=10, weight="bold", color=tc).grid(
            row=0, column=j, padx=padx, pady=0, sticky="w")
        hdr.grid_columnconfigure(j, weight=wt)
    return hdr

def trow(parent, cols_vals, col_weights, colors=None, bolds=None,
         bg=WHITE, row_h=38, pady=8, padx=14):
    n   = len(cols_vals)
    clr = colors or [DARK] * n
    bld = bolds  or [False] * n
    rf  = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=row_h)
    rf.pack(fill="x")
    rf.pack_propagate(False)
    for j, (v, wt, c, b) in enumerate(zip(cols_vals, col_weights, clr, bld)):
        lbl(rf, str(v), size=11, weight="bold" if b else "normal", color=c).grid(
            row=0, column=j, padx=padx, pady=pady, sticky="w")
        rf.grid_columnconfigure(j, weight=wt)
    return rf

# ══════════════════════════════════════════════════════════════════════════════
class CanteenApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Indian Army — Canteen Management System v5.0")
        self.geometry("1400x860")
        self.minsize(1100, 700)
        self.configure(fg_color=LIGHT)
        self._report_period = "today"
        self._inv_filter    = "All"
        self._exp_filter    = "All"
        self._show_login()

    # ══════════════════════════════════════════════════════════════════════════
    # LOGIN
    # ══════════════════════════════════════════════════════════════════════════
    def _show_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=ARMY_BG)

        cv = tk.Canvas(self, bg="#1F3320", highlightthickness=0)
        cv.place(x=0, y=0, relwidth=1, relheight=1)

        def _draw(event=None):
            if not cv.winfo_exists(): return
            cv.delete("all")
            W = cv.winfo_width() or 1400; H = cv.winfo_height() or 860
            for x in range(-H, W+H, 110):
                cv.create_polygon(x,0, x+55,0, x+55+H,H, x+H,H, fill="#253D27", outline="")
            for x in range(-H+62, W+H, 110):
                cv.create_polygon(x,0, x+30,0, x+30+H,H, x+H,H, fill="#192A1C", outline="")
            cx, cy = W//2, H//2
            R = min(W,H)//4
            cy -= R//2
            cv.create_oval(cx-R,cy-R,cx+R,cy+R, outline="#3D5A2A", width=3)
            for i in range(24):
                a = math.radians(i*15-90)
                cv.create_line(cx+int(20*math.cos(a)), cy+int(20*math.sin(a)),
                               cx+int((R-12)*math.cos(a)), cy+int((R-12)*math.sin(a)),
                               fill="#3D5A2A", width=2)

        cv.bind("<Configure>", _draw)
        self.after(30, _draw)

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

        hdr = ctk.CTkFrame(box, fg_color=ARMY_BG, corner_radius=0, height=136, width=460)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tricolor(hdr, 4)
        lbl(hdr, "🇮🇳  INDIAN ARMY", size=11, weight="bold", color=GOLD_LT).pack(pady=(12,0))
        lbl(hdr, "CANTEEN MANAGEMENT SYSTEM", size=18, weight="bold", color=WHITE).pack(pady=(3,0))
        lbl(hdr, "56 APO Field Canteen  •  सेवा परमो धर्म", size=10, color=GOLD).pack(pady=(3,12))

        lbl(box, "Staff / Officer Login", size=15, weight="bold", color=ARMY_BG).pack(pady=(24,14))

        for field, attr, ph, show in [
            ("Username", "_uname", "Enter username", ""),
            ("Password", "_pwd",   "Enter password", "●"),
        ]:
            rf = ctk.CTkFrame(box, fg_color="transparent")
            rf.pack(fill="x", padx=44, pady=(0,12))
            lbl(rf, field, size=12, weight="bold", color="#374151").pack(anchor="w", pady=(0,5))
            e = ctk.CTkEntry(rf, height=46, corner_radius=10,
                             placeholder_text=ph, show=show,
                             font=ctk.CTkFont(size=14), border_color="#CBD5E1")
            e.pack(fill="x")
            setattr(self, attr, e)

        self._uname.insert(0, "admin")
        self._pwd.insert(0, "admin123")
        self._pwd.bind("<Return>", lambda e: self._do_login())

        ctk.CTkButton(box, text="🔐  Login to System", height=52, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=ARMY_BG, hover_color=ARMY_HVR,
                      command=self._do_login).pack(padx=44, pady=(6,12), fill="x")

        self._login_err = lbl(box, "", size=12, color=RED)
        self._login_err.pack()

        foot = ctk.CTkFrame(box, fg_color="transparent", height=5, width=460)
        foot.pack(fill="x", pady=(14,0)); foot.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(foot, fg_color=c).pack(side="left", fill="both", expand=True)
        lbl(box, "जय हिन्द  •  v5.0  •  SQLite + PDF", size=10, color="#94A3B8").pack(pady=(8,22))

    def _do_login(self):
        un = self._uname.get().strip()
        pw = self._pwd.get()
        if not un or not pw:
            self._login_err.configure(text="⚠  Enter both username and password.")
            return
        with get_db() as conn:
            user = conn.execute(
                "SELECT id,username,name,rank FROM users WHERE username=? AND pw_hash=? AND active=1",
                (un, _hash(pw))).fetchone()
            if not user:
                self._login_err.configure(text="⚠  Invalid credentials or account inactive.")
                return
            roles = [r[0] for r in conn.execute(
                "SELECT role FROM user_roles WHERE user_id=?", (user["id"],))]
            if not roles:
                self._login_err.configure(text="⚠  No role assigned."); return
            self._user  = user
            self._roles = roles
            self._role  = ("admin" if "admin" in roles else
                           "manager" if "manager" in roles else roles[0])
        self._build_main()

    # ══════════════════════════════════════════════════════════════════════════
    # SHELL
    # ══════════════════════════════════════════════════════════════════════════
    def _build_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=LIGHT)

        # Sidebar
        sb = ctk.CTkFrame(self, fg_color=ARMY_BG, width=264, corner_radius=0)
        sb.pack(side="left", fill="y"); sb.pack_propagate(False)
        self._sb = sb
        tricolor(sb, 5)

        lg = ctk.CTkFrame(sb, fg_color="transparent")
        lg.pack(fill="x", padx=16, pady=(14,8))
        lbl(lg, "🇮🇳", size=30).pack(side="left", padx=(0,10))
        tf = ctk.CTkFrame(lg, fg_color="transparent"); tf.pack(side="left")
        lbl(tf, "INDIAN ARMY", size=12, weight="bold", color=GOLD).pack(anchor="w")
        lbl(tf, "Canteen Management", size=9, color="#7A9A7A").pack(anchor="w")

        sep(sb).pack(fill="x", padx=16, pady=(6,10))

        uc = ctk.CTkFrame(sb, fg_color="#1A2F1C", corner_radius=10)
        uc.pack(padx=12, fill="x", pady=(0,12))
        lbl(uc, "⭐  Unit / Establishment", size=9, color=GOLD).pack(padx=12, pady=(9,1), anchor="w")
        lbl(uc, "56 APO Field Canteen", size=12, weight="bold", color=WHITE).pack(padx=12, anchor="w")
        lbl(uc, "Est. 1947  •  Serving with Pride", size=9, color="#7A9A7A").pack(padx=12, pady=(1,9), anchor="w")

        sep(sb).pack(fill="x", padx=16, pady=(0,6))
        lbl(sb, "  NAVIGATION", size=9, weight="bold", color="#4A6A4A").pack(anchor="w", padx=16, pady=(2,4))

        r = self._role
        nav = [("📊  Dashboard", "dashboard")]
        if r in ("admin","manager"):
            nav += [
                ("💰  Sales Entry",   "sales"),
                ("🧑‍🍳  Batch Prep",    "batch"),
                ("📦  Inventory",     "inventory"),
                ("💸  Expenditure",   "expenditure"),
                ("♻️  Waste",          "waste"),
            ]
        nav += [("📋  Daily Report", "report")]
        if r == "admin":
            nav += [
                ("🧾  Master Data",   "master"),
                ("👥  Users",         "users"),
                ("💾  Backup & Restore", "backup"),
            ]

        self._nav_btns = {}
        for txt, pg in nav:
            b = ctk.CTkButton(sb, text=txt, anchor="w", height=44,
                              font=ctk.CTkFont(size=12, weight="bold"),
                              fg_color="transparent", hover_color=ARMY_HVR,
                              text_color="#8AAA8A", corner_radius=8,
                              command=lambda p=pg: self._go(p))
            b.pack(padx=12, pady=2, fill="x")
            self._nav_btns[pg] = b

        sep(sb).pack(fill="x", padx=16, side="bottom", pady=(8,6))
        ctk.CTkButton(sb, text="⬅  Logout", height=38, anchor="w",
                      fg_color="transparent", hover_color=ARMY_HVR,
                      text_color="#5A7A5A", font=ctk.CTkFont(size=12, weight="bold"),
                      corner_radius=8, command=self._show_login).pack(
                          padx=12, pady=(0,8), fill="x", side="bottom")

        usr = ctk.CTkFrame(sb, fg_color="#1A2F1C", corner_radius=10)
        usr.pack(padx=12, side="bottom", fill="x", pady=(0,8))
        lbl(usr, f"👤  {self._user['name']}", size=11, weight="bold",
            color=WHITE).pack(padx=12, pady=(10,1), anchor="w")
        lbl(usr, f"Role: {', '.join(self._roles)}", size=9,
            color="#5A7A5A").pack(padx=12, pady=(0,10), anchor="w")

        right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        tricolor(right, 5)
        self._area = ctk.CTkFrame(right, fg_color=LIGHT, corner_radius=0)
        self._area.pack(fill="both", expand=True)

        self._go("dashboard")

    def _go(self, page):
        for p, b in self._nav_btns.items():
            b.configure(fg_color=SAFFRON if p == page else "transparent",
                        text_color=ARMY_BG if p == page else "#8AAA8A")
        for w in self._area.winfo_children(): w.destroy()
        {
            "dashboard":   self._pg_dashboard,
            "sales":       self._pg_sales,
            "batch":       self._pg_batch,
            "inventory":   self._pg_inventory,
            "expenditure": self._pg_expenditure,
            "waste":       self._pg_waste,
            "report":      self._pg_report,
            "master":      self._pg_master,
            "users":       self._pg_users,
            "backup":      self._pg_backup,
        }.get(page, self._pg_dashboard)()

    def _hdr(self, title, sub=""):
        hf = ctk.CTkFrame(self._area, fg_color=WHITE, corner_radius=0, height=64)
        hf.pack(fill="x"); hf.pack_propagate(False)
        sep(hf, BORDER).pack(side="bottom", fill="x")
        ctk.CTkFrame(hf, fg_color=SAFFRON, width=5, corner_radius=0).pack(side="left", fill="y")
        inner = ctk.CTkFrame(hf, fg_color="transparent")
        inner.pack(side="left", fill="y", padx=PAD)
        lbl(inner, title, size=19, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(12,0))
        if sub: lbl(inner, sub, size=10, color=MID).pack(anchor="w")
        return hf

    def _popup(self, title, message, color=GREEN):
        win = ctk.CTkToplevel(self)
        win.title(title); win.geometry("480x240")
        win.resizable(False, False); win.grab_set(); win.lift()
        win.configure(fg_color=WHITE)
        ts = ctk.CTkFrame(win, fg_color="transparent", height=5); ts.pack(fill="x"); ts.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ts, fg_color=c).pack(side="left", fill="both", expand=True)
        is_ok = any(x in title for x in ["✅","Saved","Created","Reset","Done","Backup","Restored"])
        lbl(win, "✅" if is_ok else "ℹ️", size=36).pack(pady=(18,4))
        lbl(win, message, size=12, color=DARK, justify="center", wraplength=420).pack(pady=(0,16))
        btn(win, "Close", win.destroy, fg=ARMY_BG, hv=ARMY_HVR, h=40).pack(padx=60, fill="x")
        lbl(win, "जय हिन्द", size=10, color=MID).pack(pady=(8,16))

    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_dashboard(self):
        self._hdr("Dashboard",
                  f"🇮🇳  {datetime.now().strftime('%A, %d %B %Y')}  ·  56 APO Field Canteen")
        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            sales = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
            inv   = conn.execute("SELECT * FROM inventory").fetchall()
            waste = conn.execute("SELECT * FROM waste_tracker WHERE date=?", (today,)).fetchall()
            exp   = conn.execute("SELECT SUM(amount) FROM expenditure WHERE date=?", (today,)).fetchone()[0] or 0

        rev    = sum(r["sp"]*r["sold"] for r in sales)
        cogs   = sum(r["cogs"] for r in sales)
        profit = rev - cogs - exp
        meals  = sum(r["sold"] for r in sales)
        low    = [i for i in inv if i["stock"] < i["min_lvl"]]
        wcost  = sum(w["cost_lost"] or 0 for w in waste)

        KPI = [
            ("💰", "Revenue",     f"₹{rev:,.0f}",    SAFFRON, BG_SAF, T_SAF),
            ("🍛", "Meals Served", str(meals),         GREEN,   BG_GRN, T_GRN),
            ("📈", "Net Profit",  f"₹{profit:,.0f}",  BLUE,    BG_BLU, T_BLU),
            ("💸", "Expenditure", f"₹{exp:,.0f}",     PURPLE,  BG_PUR, T_PUR),
            ("♻️", "Waste Cost",  f"₹{wcost:,.0f}",   ORANGE,  BG_SAF, T_SAF),
            ("⚠️", "Low Stock",   str(len(low)),       RED,     BG_RED, T_RED),
        ]
        kr = ctk.CTkFrame(self._area, fg_color="transparent")
        kr.pack(fill="x", padx=PAD, pady=(16,0))
        for i, (icon, title, val, color, bg, border) in enumerate(KPI):
            c = ctk.CTkFrame(kr, fg_color=WHITE, corner_radius=12, border_width=1, border_color=border)
            c.grid(row=0, column=i, padx=(0 if i==0 else 8), sticky="nsew")
            kr.grid_columnconfigure(i, weight=1)
            ctk.CTkFrame(c, fg_color=color, height=3, corner_radius=0).pack(fill="x")
            rf = ctk.CTkFrame(c, fg_color="transparent"); rf.pack(fill="x", padx=14, pady=12)
            ib = ctk.CTkFrame(rf, fg_color=bg, corner_radius=8, width=40, height=40)
            ib.pack(side="left"); ib.pack_propagate(False)
            lbl(ib, icon, size=18).place(relx=0.5, rely=0.5, anchor="center")
            vf = ctk.CTkFrame(rf, fg_color="transparent"); vf.pack(side="left", padx=(10,0))
            lbl(vf, val,   size=18, weight="bold", color=color).pack(anchor="w")
            lbl(vf, title, size=9,  color=MID).pack(anchor="w")

        bot = ctk.CTkFrame(self._area, fg_color="transparent")
        bot.pack(fill="both", expand=True, padx=PAD, pady=(14,PAD))
        bot.grid_columnconfigure(0, weight=6); bot.grid_columnconfigure(1, weight=4)
        bot.grid_rowconfigure(0, weight=1)

        # Sales table
        sc = card(bot); sc.grid(row=0, column=0, padx=(0,10), sticky="nsew")
        band(sc, "📊  Today's Sales — Quick View")
        COLS = [("Meal Item",3),("Sold",1),("Rate",1),("Revenue",2),("Payment",1)]
        thead(sc, COLS)
        sf = ctk.CTkScrollableFrame(sc, fg_color="transparent")
        sf.pack(fill="both", expand=True)
        for ix, r in enumerate(sales):
            pi = {"Cash":"💵","UPI":"📱","Card":"💳"}.get(r["payment"],"💰")
            trow(sf,[r["meal"],str(r["sold"]),f"₹{r['sp']:.0f}",
                     f"₹{r['sp']*r['sold']:,.0f}",f"{pi} {r['payment']}"],
                 [3,1,1,2,1],
                 colors=[DARK,MID,MID,GREEN,MID],bolds=[True,False,False,True,False],
                 bg=WHITE if ix%2==0 else STRIPE)
        totf = ctk.CTkFrame(sc, fg_color=BG_SAF, corner_radius=0, height=36)
        totf.pack(fill="x"); totf.pack_propagate(False)
        for j,(v,wt) in enumerate(zip(["TOTAL",str(meals),"—",f"₹{rev:,.0f}",""],
                                      [3,1,1,2,1])):
            lbl(totf, v, size=11, weight="bold",
                color=SAFFRON if j in [0,3] else MID).grid(row=0,column=j,padx=14,sticky="w")
            totf.grid_columnconfigure(j, weight=wt)

        # Alerts
        ac = card(bot); ac.grid(row=0, column=1, sticky="nsew")
        band(ac, f"⚠️  Low Stock Alerts  ({len(low)} items)", bg=DRED, tc=WHITE)
        sf2 = ctk.CTkScrollableFrame(ac, fg_color="transparent")
        sf2.pack(fill="both", expand=True, padx=8, pady=8)
        if not low:
            lbl(sf2, "✅  All items sufficiently stocked.", size=12, color=GREEN).pack(pady=24)
        else:
            for item in low:
                rf2 = ctk.CTkFrame(sf2, fg_color=BG_RED, corner_radius=10, border_width=1, border_color=T_RED)
                rf2.pack(fill="x", pady=3)
                lbl(rf2, f"  {item['item']}", size=12, weight="bold", color="#991B1B").pack(padx=10, pady=(8,2), anchor="w")
                bf2 = ctk.CTkFrame(rf2, fg_color="transparent"); bf2.pack(padx=10, pady=(0,8), fill="x")
                lbl(bf2, f"Stock: {item['stock']:.1f} {item['unit']}", size=10, color=RED).pack(side="left")
                lbl(bf2, f"Min: {item['min_lvl']:.1f}", size=10, color=MID).pack(side="right")
        btn(ac, "🛒  Shopping List", lambda: self._popup(
            "🛒 Shopping List",
            "\n".join(f"• {i['item']}  →  need {i['min_lvl']-i['stock']:.1f} {i['unit']}" for i in low)
            or "All stock sufficient!"),
            fg=DRED, hv=RED, h=38).pack(fill="x", side="bottom")

    # ══════════════════════════════════════════════════════════════════════════
    # SALES ENTRY — per-item update, today's sales shown below
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_sales(self):
        hf = self._hdr("💰  Daily Sales Entry",
                       datetime.now().strftime("📅  %d %B %Y  •  Select item & enter sold qty"))
        # Export day report button in header
        btn(hf, "📋  Export Day PDF", lambda: self._export_pdf_report(
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%Y-%m-%d")),
            fg=ARMY_BG, hv=ARMY_HVR, h=32).pack(side="right", padx=PAD)

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(14,PAD))

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            meals = conn.execute("SELECT id,name,sp FROM menu WHERE active=1 ORDER BY name").fetchall()
            today_sales = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
        today_map = {r["menu_id"]: r for r in today_sales}

        # ── Quick-entry grid ──────────────────────────────────────────────────
        mc = card(wrap); mc.pack(fill="x", pady=(0,14))
        band(mc, "🍽  Quick Item Sales Entry  — enter qty per item, hit Save")
        lbl(mc, "  Each item saves independently. Stock & COGS auto-deducted.",
            size=11, color=MID).pack(anchor="w", padx=14, pady=(8,4))

        COLS = [("Menu Item",4),("Price",1),("Qty Sold",1),("Revenue Est.",1),("Payment",1),("Action",1)]
        thead(mc, COLS, bg=STRIPE, tc=MID)

        self._sq = {}  # menu_id -> (name,sp,e_qty,e_pm)
        for ix, meal in enumerate(meals):
            mid2, name2, sp2 = meal["id"], meal["name"], meal["sp"]
            already = today_map.get(mid2)
            bg2 = WHITE if ix%2==0 else STRIPE
            rf = ctk.CTkFrame(mc, fg_color=bg2, corner_radius=0, height=46)
            rf.pack(fill="x"); rf.pack_propagate(False)

            lbl(rf, f"  {'🍛' if 'Thali' in name2 or 'Biryani' in name2 else '🍽'}  {name2}",
                size=12, weight="bold", color=DARK).grid(row=0, column=0, padx=14, sticky="w", pady=4)
            lbl(rf, f"₹{sp2:.0f}", size=11, color=MID).grid(row=0, column=1, sticky="w")

            e_qty = ctk.CTkEntry(rf, height=30, width=60, corner_radius=8,
                                 placeholder_text="0", font=ctk.CTkFont(size=12),
                                 border_color=BORDER)
            if already: e_qty.insert(0, str(already["sold"]))
            e_qty.grid(row=0, column=2, padx=8, sticky="ew", pady=4)
            rf.grid_columnconfigure(2, weight=1)

            lbl_rev = lbl(rf, f"₹{(already['sold']*sp2 if already else 0):,.0f}",
                          size=11, weight="bold", color=GREEN)
            lbl_rev.grid(row=0, column=3, sticky="w", padx=8)

            pm = ctk.CTkOptionMenu(rf, values=["Cash","UPI","Card"], width=90,
                                   font=ctk.CTkFont(size=11))
            pm.set(already["payment"] if already else "Cash")
            pm.grid(row=0, column=4, padx=6, sticky="ew", pady=4)
            rf.grid_columnconfigure(4, weight=1)

            def _save_one(m_id=mid2, m_name=name2, m_sp=sp2, eq=e_qty, epm=pm):
                self._save_one_sale(m_id, m_name, m_sp, eq, epm)
                self._go("sales")                       # refresh

            def _upd_rev(event=None, eq=e_qty, lr=lbl_rev, sp=sp2):
                try:    lr.configure(text=f"₹{int(eq.get() or 0)*sp:,.0f}")
                except: lr.configure(text="₹0")

            e_qty.bind("<KeyRelease>", _upd_rev)

            b_save = ctk.CTkButton(rf, text="Save", width=60, height=28,
                                   corner_radius=8, fg_color=GREEN, hover_color=DGREEN,
                                   font=ctk.CTkFont(size=11, weight="bold"),
                                   command=_save_one)
            b_save.grid(row=0, column=5, padx=8, sticky="e")
            rf.grid_columnconfigure(5, weight=1)

            if already:
                # Highlight already-saved row
                rf.configure(border_color=T_GRN, border_width=1)
                lbl(rf, "✓", size=11, weight="bold", color=GREEN).grid(
                    row=0, column=5, padx=2, sticky="e")

            self._sq[mid2] = (name2, sp2, e_qty, pm)

        # Save all at once button
        bf = ctk.CTkFrame(wrap, fg_color="transparent"); bf.pack(fill="x", pady=(6,0))
        btn(bf, "✅  Save All Sales at Once", self._save_all_sales,
            fg=ARMY_BG, hv=ARMY_HVR, h=48).pack(fill="x")

        # ── Today's sales summary ─────────────────────────────────────────────
        if today_sales:
            sc = card(wrap); sc.pack(fill="x", pady=(16,0))
            band(sc, f"📊  Today's Recorded Sales  ({today})")
            COLS2 = [("Meal",4),("Sold",1),("Wastage",1),("COGS",1),("Revenue",1),("Payment",1)]
            thead(sc, COLS2, bg=STRIPE, tc=MID)
            tot_rev = tot_cogs = 0
            for ix, r in enumerate(today_sales):
                rev2 = r["sp"]*r["sold"]
                tot_rev += rev2; tot_cogs += r["cogs"]
                trow(sc,[r["meal"],str(r["sold"]),str(r["wastage"]),
                         f"₹{r['cogs']:,.0f}",f"₹{rev2:,.0f}",r["payment"]],
                     [4,1,1,1,1,1], bg=WHITE if ix%2==0 else STRIPE)
            totf = ctk.CTkFrame(sc, fg_color=BG_GRN, corner_radius=0, height=36)
            totf.pack(fill="x"); totf.pack_propagate(False)
            for j,(v,wt) in enumerate(zip(
                    ["TOTAL","","",f"₹{tot_cogs:,.0f}",f"₹{tot_rev:,.0f}",""],
                    [4,1,1,1,1,1])):
                lbl(totf,v,size=11,weight="bold",
                    color=GREEN if j in[3,4] else MID).grid(row=0,column=j,padx=14,sticky="w")
                totf.grid_columnconfigure(j, weight=wt)

    def _save_one_sale(self, menu_id, meal, sp, eq, epm):
        try:    sold = int(eq.get() or 0)
        except: self._popup("⚠️ Invalid", "Enter a whole number."); return
        if sold <= 0: self._popup("⚠️ No qty", "Enter quantity > 0."); return
        today = datetime.now().strftime("%Y-%m-%d")
        payment = epm.get()
        with get_db() as conn:
            # Remove existing record for this same item today (update semantics)
            conn.execute("DELETE FROM sales WHERE date=? AND menu_id=?", (today, menu_id))
            recipes = conn.execute("SELECT inv_id,qty_per_unit FROM recipes WHERE menu_id=?",
                                   (menu_id,)).fetchall()
            cpu = 0
            for rc in recipes:
                inv = conn.execute("SELECT cp,stock FROM inventory WHERE id=?", (rc["inv_id"],)).fetchone()
                if inv:
                    cpu += rc["qty_per_unit"] * inv["cp"]
                    conn.execute("UPDATE inventory SET stock = stock - ? WHERE id=?",
                                 (rc["qty_per_unit"]*sold, rc["inv_id"]))
            conn.execute("INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) VALUES (?,?,?,?,?,?,?,?)",
                         (today, menu_id, meal, sp, sold, 0, sold*cpu, payment))
        self._popup("✅ Saved!", f"{meal} — {sold} sold @ ₹{sp}, Revenue ₹{sp*sold:,.0f}")

    def _save_all_sales(self):
        today = datetime.now().strftime("%Y-%m-%d")
        payment = "Cash"
        saved = 0
        with get_db() as conn:
            for mid2, (name2, sp2, eq, pm) in self._sq.items():
                try:    sold = int(eq.get() or 0)
                except: continue
                if sold <= 0: continue
                payment = pm.get()
                conn.execute("DELETE FROM sales WHERE date=? AND menu_id=?", (today, mid2))
                recipes = conn.execute("SELECT inv_id,qty_per_unit FROM recipes WHERE menu_id=?",
                                       (mid2,)).fetchall()
                cpu = 0
                for rc in recipes:
                    inv = conn.execute("SELECT cp FROM inventory WHERE id=?", (rc["inv_id"],)).fetchone()
                    if inv:
                        cpu += rc["qty_per_unit"] * inv["cp"]
                        conn.execute("UPDATE inventory SET stock=stock-? WHERE id=?",
                                     (rc["qty_per_unit"]*sold, rc["inv_id"]))
                conn.execute("INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) VALUES (?,?,?,?,?,?,?,?)",
                             (today, mid2, name2, sp2, sold, 0, sold*cpu, payment))
                saved += 1
        if saved == 0:
            self._popup("⚠️ Nothing saved", "Enter at least one qty > 0."); return
        self._popup("✅ All Sales Saved!", f"{saved} items recorded. Stock & COGS updated.")
        self._go("sales")

    # ══════════════════════════════════════════════════════════════════════════
    # BATCH PREP
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_batch(self):
        self._hdr("🧑‍🍳  Batch Preparation",
                  datetime.now().strftime("📅  %d %B %Y  •  Record prep qty to auto-deduct stock"))
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(14,PAD))

        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            meals = conn.execute("SELECT id,name FROM menu WHERE active=1 ORDER BY name").fetchall()
            batches_today = conn.execute(
                "SELECT bp.menu_id, SUM(bp.qty_prepared) as total, m.name "
                "FROM batch_prep bp JOIN menu m ON m.id=bp.menu_id "
                "WHERE bp.date=? GROUP BY bp.menu_id", (today,)).fetchall()

        batch_map = {b["menu_id"]: b["total"] for b in batches_today}

        # Form
        bc = card(wrap); bc.pack(fill="x", pady=(0,14))
        band(bc, "📝  Enter Batch Quantities  — stock auto-deducted on save")
        lbl(bc, "  Enter how many units of each meal were prepared today.",
            size=11, color=MID).pack(anchor="w", padx=14, pady=(8,4))

        COLS = [("Meal Item",4),("Qty to Prepare",2),("Already Prepared Today",2)]
        thead(bc, COLS, bg=STRIPE, tc=MID)

        self._be = {}  # menu_id -> entry
        for ix, meal in enumerate(meals):
            mid2, nm = meal["id"], meal["name"]
            bg2 = WHITE if ix%2==0 else STRIPE
            rf = ctk.CTkFrame(bc, fg_color=bg2, corner_radius=0, height=46)
            rf.pack(fill="x"); rf.pack_propagate(False)
            lbl(rf, f"  {nm}", size=12, weight="bold", color=DARK).grid(
                row=0, column=0, padx=14, sticky="w", pady=4)
            e = ctk.CTkEntry(rf, height=30, corner_radius=8,
                             placeholder_text="0", font=ctk.CTkFont(size=12),
                             border_color=BORDER)
            e.grid(row=0, column=1, padx=10, sticky="ew", pady=4)
            rf.grid_columnconfigure(1, weight=2)
            already = batch_map.get(mid2, 0)
            ac_color = GREEN if already > 0 else MID
            lbl(rf, f"{already} units" if already else "None today",
                size=11, color=ac_color, weight="bold" if already else "normal").grid(
                row=0, column=2, padx=14, sticky="w")
            rf.grid_columnconfigure(0,weight=4); rf.grid_columnconfigure(2,weight=2)
            self._be[mid2] = e

        bf = ctk.CTkFrame(wrap, fg_color="transparent"); bf.pack(fill="x", pady=(8,0))
        btn(bf, "✅  Save Batch & Auto-Deduct Stock", self._save_batch,
            fg=GREEN, hv=DGREEN, h=48).pack(fill="x")

        # Today's batch log
        if batches_today:
            lc = card(wrap); lc.pack(fill="x", pady=(16,0))
            band(lc, f"📊  Today's Batch Log  ({today})")
            COLS2 = [("Meal Item",4),("Total Prepared",2)]
            thead(lc, COLS2, bg=STRIPE, tc=MID)
            for ix, b in enumerate(batches_today):
                trow(lc, [b["name"], f"{b['total']} units"],
                     [4,2], colors=[DARK, GREEN], bolds=[True,True],
                     bg=WHITE if ix%2==0 else STRIPE)

    def _save_batch(self):
        today = datetime.now().strftime("%Y-%m-%d")
        saved = 0
        with get_db() as conn:
            for mid2, e in self._be.items():
                try:    qty = int(e.get() or 0)
                except: self._popup("⚠️ Invalid", "Whole numbers only."); return
                if qty <= 0: continue
                conn.execute("INSERT INTO batch_prep (date,menu_id,qty_prepared) VALUES (?,?,?)",
                             (today, mid2, qty))
                for rc in conn.execute("SELECT inv_id,qty_per_unit FROM recipes WHERE menu_id=?",
                                       (mid2,)):
                    conn.execute("UPDATE inventory SET stock=stock-?,received=received WHERE id=?",
                                 (rc["qty_per_unit"]*qty, rc["inv_id"]))
                saved += 1
        if saved == 0:
            self._popup("⚠️ Nothing saved", "Enter at least one qty > 0."); return
        self._popup("✅ Batch Saved!", f"{saved} meal(s) recorded. Inventory deducted.")
        self._go("batch")

    # ══════════════════════════════════════════════════════════════════════════
    # INVENTORY — full CRUD with category tabs & edit-in-dialog
    # ══════════════════════════════════════════════════════════════════════════
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

        # Action bar
        ab = ctk.CTkFrame(self._area, fg_color="transparent")
        ab.pack(fill="x", padx=PAD, pady=(10,0))
        btn(ab, "＋  Add New Item",    self._dlg_inv_add,    fg=GREEN,   hv=DGREEN, h=36).pack(side="left")
        btn(ab, "📥  Receive Stock",   self._dlg_inv_receive, fg=TEAL,    hv=ARMY_BG, h=36).pack(side="left", padx=8)
        btn(ab, "✏️  Edit Item",        self._dlg_inv_edit,   fg=BLUE,    hv=DBLUE,   h=36).pack(side="left")
        btn(ab, "🗑  Delete Item",      self._dlg_inv_del,    fg=RED,     hv=DRED,    h=36).pack(side="left", padx=8)

        # Table
        tc = card(self._area)
        tc.pack(fill="both", expand=True, padx=PAD, pady=(10,PAD))
        INV_COLS = [("Item",4),("Category",2),("Unit",1),("Opening",1),
                    ("Received",1),("Stock",1),("Min",1),("Status",1)]
        thead(tc, INV_COLS)
        self._inv_sf = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_sf.pack(fill="both", expand=True)
        self._inv_wts = [w for _,w in INV_COLS]
        self._inv_loadrows()

    def _inv_setcat(self, cat):
        self._inv_filter = cat
        for c, b in self._inv_fb.items():
            b.configure(fg_color=ARMY_BG if c==cat else STRIPE,
                        text_color=WHITE if c==cat else DARK)
        for w in self._inv_sf.winfo_children(): w.destroy()
        self._inv_loadrows()

    def _inv_loadrows(self):
        with get_db() as conn:
            if self._inv_filter == "All":
                data = conn.execute("SELECT * FROM inventory ORDER BY cat,item").fetchall()
            else:
                data = conn.execute("SELECT * FROM inventory WHERE cat=? ORDER BY item",
                                    (self._inv_filter,)).fetchall()
        ci = {"Dry":"🌾","Fresh":"🥦","Dairy":"🥛","Bakery":"🥐","Prepared":"🍲"}
        for ix, item in enumerate(data):
            low = item["stock"] < item["min_lvl"]
            bg2 = BG_RED if low else (WHITE if ix%2==0 else STRIPE)
            trow(self._inv_sf,
                 [f"  {item['item']}", f"{ci.get(item['cat'],'•')} {item['cat']}",
                  item["unit"], f"{item['opening']:.1f}", f"{item['received']:.1f}",
                  f"{item['stock']:.1f}", f"{item['min_lvl']:.1f}",
                  "⚠ LOW" if low else "✓ OK"],
                 self._inv_wts,
                 colors=[DARK,MID,MID,MID,MID,
                         RED if low else GREEN, MID,
                         RED if low else GREEN],
                 bolds=[True,False,False,False,False,True,False,True],
                 bg=bg2, row_h=40)

    def _dlg_inv_add(self):
        win = ctk.CTkToplevel(self)
        win.title("Add New Inventory Item"); win.geometry("540x480")
        win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win, "＋  Create New Inventory Item", h=44)
        fields = {}
        for lbl_t, ph, attr in [
            ("Item Name","e.g., Mustard Oil","name"),
            ("Category (Dry/Fresh/Dairy/Bakery/Prepared)","e.g., Dry","cat"),
            ("Unit (kg/ltr/pcs)","e.g., kg","unit"),
            ("Opening Stock","e.g., 20","stock"),
            ("Minimum Level","e.g., 5","min_lvl"),
            ("Cost Price per Unit (₹)","e.g., 90","cp"),
        ]:
            lbl(win, lbl_t, size=11, weight="bold", color=ARMY_BG).pack(anchor="w", padx=24, pady=(10,3))
            e = entry(win, ph=ph, h=38); e.pack(fill="x", padx=24)
            fields[attr] = e

        def save():
            try:
                nm   = fields["name"].get().strip()
                cat  = fields["cat"].get().strip()
                unit = fields["unit"].get().strip()
                stk  = float(fields["stock"].get() or 0)
                mn   = float(fields["min_lvl"].get() or 0)
                cp   = float(fields["cp"].get() or 0)
            except ValueError:
                self._popup("⚠️ Invalid","Enter numeric values."); return
            if not nm or not cat or not unit:
                self._popup("⚠️ Missing","Fill all fields."); return
            with get_db() as conn:
                try:
                    conn.execute("INSERT INTO inventory (item,cat,unit,stock,min_lvl,opening,cp) VALUES (?,?,?,?,?,?,?)",
                                 (nm, cat, unit, stk, mn, stk, cp))
                except sqlite3.IntegrityError:
                    self._popup("⚠️ Duplicate","Item already exists."); return
            self._popup("✅ Added!", f"{nm} added to inventory.")
            win.destroy(); self._go("inventory")

        btn(win, "✅  Save Item", save, fg=GREEN, hv=DGREEN, h=46).pack(padx=24, pady=18, fill="x")

    def _dlg_inv_receive(self):
        win = ctk.CTkToplevel(self)
        win.title("Receive Stock"); win.geometry("500x340")
        win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win, "📥  Receive / Add Stock", h=44)

        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        lbl(win,"Select Item",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(16,4))
        iom = ctk.CTkOptionMenu(win, values=items); iom.set(items[0] if items else "")
        iom.pack(fill="x", padx=24, pady=(0,12))
        lbl(win,"Quantity Received",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(0,4))
        e_qty = entry(win, ph="e.g., 25.5", h=38); e_qty.pack(fill="x",padx=24,pady=(0,12))
        lbl(win,"New Cost Price (₹) — leave blank to keep existing",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(0,4))
        e_cp = entry(win, ph="e.g., 42", h=38); e_cp.pack(fill="x",padx=24)

        def save():
            try:    qty = float(e_qty.get())
            except: self._popup("⚠️ Invalid","Enter numeric quantity."); return
            if qty <= 0: self._popup("⚠️ Invalid","Qty must be > 0."); return
            item = iom.get()
            cp_val = e_cp.get().strip()
            with get_db() as conn:
                inv_id = conn.execute("SELECT id,cp FROM inventory WHERE item=?", (item,)).fetchone()
                new_cp = float(cp_val) if cp_val else inv_id["cp"]
                conn.execute("UPDATE inventory SET stock=stock+?,received=received+?,cp=? WHERE item=?",
                             (qty, qty, new_cp, item))
                conn.execute("INSERT INTO goods_received (date,inv_id,qty,total_cost) VALUES (?,?,?,?)",
                             (datetime.now().strftime("%Y-%m-%d"), inv_id["id"], qty, qty*new_cp))
            self._popup("✅ Stock Received!", f"{item}: +{qty} units @ ₹{new_cp}/unit")
            win.destroy(); self._go("inventory")

        btn(win,"✅  Confirm Receipt",save,fg=TEAL,hv=ARMY_BG,h=46).pack(padx=24,pady=18,fill="x")

    def _dlg_inv_edit(self):
        win = ctk.CTkToplevel(self)
        win.title("Edit Inventory Item"); win.geometry("520x420")
        win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win, "✏️  Edit / Update Inventory Item", h=44)

        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        selected_var = tk.StringVar(value=items[0] if items else "")
        lbl(win,"Select Item",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(14,4))
        iom = ctk.CTkOptionMenu(win, values=items, variable=selected_var)
        iom.pack(fill="x", padx=24, pady=(0,10))

        fields = {}
        for lbl_t, attr, ph in [
            ("New Stock Level","stock","e.g., 50"),
            ("New Min Level","min_lvl","e.g., 10"),
            ("New Cost Price (₹)","cp","e.g., 45"),
        ]:
            lbl(win,lbl_t,size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(6,3))
            e = entry(win, ph=ph, h=38); e.pack(fill="x",padx=24)
            fields[attr] = e

        def save():
            item = iom.get()
            updates = {}
            for attr, e in fields.items():
                v = e.get().strip()
                if v:
                    try: updates[attr] = float(v)
                    except: self._popup("⚠️ Invalid","Numeric values only."); return
            if not updates:
                self._popup("⚠️ Nothing to update","Fill at least one field."); return
            set_clause = ", ".join(f"{k}=?" for k in updates)
            with get_db() as conn:
                conn.execute(f"UPDATE inventory SET {set_clause} WHERE item=?",
                             (*updates.values(), item))
            self._popup("✅ Updated!", f"{item} updated.")
            win.destroy(); self._go("inventory")

        btn(win,"✅  Save Changes",save,fg=BLUE,hv=DBLUE,h=46).pack(padx=24,pady=18,fill="x")

    def _dlg_inv_del(self):
        win = ctk.CTkToplevel(self)
        win.title("Delete Inventory Item"); win.geometry("480x260")
        win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win, "🗑  Delete Inventory Item", bg=DRED, tc=WHITE, h=44)

        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        lbl(win,"Select Item to Delete",size=12,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(18,6))
        iom = ctk.CTkOptionMenu(win, values=items); iom.set(items[0] if items else "")
        iom.pack(fill="x",padx=24,pady=(0,10))
        lbl(win,"⚠️  This permanently removes the item and its recipes.",size=10,color=RED).pack(padx=24,anchor="w")

        def delete():
            item = iom.get()
            with get_db() as conn:
                conn.execute("DELETE FROM inventory WHERE item=?", (item,))
            self._popup("✅ Deleted!", f"{item} removed."); win.destroy(); self._go("inventory")

        btn(win,"🗑  Delete Permanently",delete,fg=RED,hv=DRED,h=46).pack(padx=24,pady=16,fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # EXPENDITURE
    # ══════════════════════════════════════════════════════════════════════════
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

        e_date = entry(ff, ph="YYYY-MM-DD", h=38); e_date.insert(0, today)
        e_date.grid(row=1,column=0,sticky="ew",pady=(0,8))
        cat_menu = ctk.CTkOptionMenu(ff, values=CATS, font=ctk.CTkFont(size=11))
        cat_menu.set(CATS[0]); cat_menu.grid(row=1,column=1,padx=(20,0),sticky="ew",pady=(0,8))
        e_amt = entry(ff, ph="e.g., 1500", h=38)
        e_amt.grid(row=1,column=2,padx=(20,0),sticky="ew",pady=(0,8))

        lbl(ff,"Notes (optional)",size=11,weight="bold",color=ARMY_BG).grid(row=2,column=0,columnspan=3,sticky="w",pady=(0,4))
        e_notes = entry(ff, ph="e.g., Supplier: Sharma Stores", h=38)
        e_notes.grid(row=3,column=0,columnspan=3,sticky="ew")

        for i in range(3): ff.grid_columnconfigure(i, weight=1)

        def save_exp():
            try:    amt = float(e_amt.get())
            except: self._popup("⚠️ Invalid","Enter numeric amount."); return
            if amt <= 0: self._popup("⚠️ Invalid","Amount must be > 0."); return
            exp_date = e_date.get().strip() or today
            cat = cat_menu.get(); notes = e_notes.get().strip()
            with get_db() as conn:
                conn.execute("INSERT INTO expenditure (date,amount,category,notes) VALUES (?,?,?,?)",
                             (exp_date, amt, cat, notes or None))
            self._popup("✅ Expenditure Saved!", f"₹{amt:,.0f} under {cat}")
            e_amt.delete(0,"end"); e_notes.delete(0,"end")
            self._go("expenditure")

        btn(fc,"✅  Save Expenditure",save_exp,fg=GREEN,hv=DGREEN,h=44).pack(padx=18,pady=(0,16),fill="x")

        # ── Category Filter ───────────────────────────────────────────────────
        catf = ctk.CTkFrame(wrap, fg_color="transparent"); catf.pack(fill="x", pady=(0,10))
        all_cats = ["All"] + CATS
        self._exp_filter = getattr(self,"_exp_filter","All")
        for cat in all_cats:
            b = ctk.CTkButton(catf, text=cat, height=28, corner_radius=8,
                              font=ctk.CTkFont(size=10, weight="bold"),
                              fg_color=ARMY_BG if cat==self._exp_filter else STRIPE,
                              text_color=WHITE if cat==self._exp_filter else DARK,
                              hover_color=ARMY_HVR,
                              command=lambda c=cat: self._exp_setcat(c))
            b.pack(side="left", padx=2)

        # ── Expenditure Table ─────────────────────────────────────────────────
        ec = card(wrap); ec.pack(fill="both", expand=True)
        band(ec, "📋  Expenditure Ledger")
        COLS = [("Date",2),("Category",3),("Amount",2),("Notes",4),("Del",1)]
        thead(ec, COLS, bg=STRIPE, tc=MID)

        with get_db() as conn:
            if self._exp_filter == "All":
                rows = conn.execute("SELECT * FROM expenditure ORDER BY date DESC,id DESC").fetchall()
            else:
                rows = conn.execute("SELECT * FROM expenditure WHERE category=? ORDER BY date DESC",
                                    (self._exp_filter,)).fetchall()

        total = sum(r["amount"] for r in rows)
        esf = ctk.CTkScrollableFrame(ec, fg_color="transparent")
        esf.pack(fill="both", expand=True)
        for ix, r in enumerate(rows):
            bg2 = WHITE if ix%2==0 else STRIPE
            rf = ctk.CTkFrame(esf, fg_color=bg2, corner_radius=0, height=38)
            rf.pack(fill="x"); rf.pack_propagate(False)
            for j,(v,wt) in enumerate(zip(
                    [r["date"],r["category"],f"₹{r['amount']:,.0f}",r["notes"] or "—"],
                    [2,3,2,4])):
                lbl(rf,v,size=11,color=DARK if j<2 else MID,
                    weight="bold" if j==2 else "normal").grid(row=0,column=j,padx=14,sticky="w")
                rf.grid_columnconfigure(j,weight=wt)
            del_btn = ctk.CTkButton(rf, text="🗑", width=28, height=26,
                                    fg_color=STRIPE, hover_color=T_RED,
                                    text_color=RED, corner_radius=6,
                                    font=ctk.CTkFont(size=11),
                                    command=lambda rid=r["id"]: self._del_exp(rid))
            del_btn.grid(row=0,column=4,padx=8,sticky="e")
            rf.grid_columnconfigure(4,weight=1)

        totf = ctk.CTkFrame(ec, fg_color=BG_RED, corner_radius=0, height=36)
        totf.pack(fill="x"); totf.pack_propagate(False)
        lbl(totf, "TOTAL", size=11, weight="bold", color=RED).grid(row=0,column=0,padx=14,sticky="w")
        lbl(totf, f"₹{total:,.0f}", size=13, weight="bold", color=RED).grid(row=0,column=2,padx=14,sticky="w")
        totf.grid_columnconfigure(0,weight=2); totf.grid_columnconfigure(1,weight=3)
        totf.grid_columnconfigure(2,weight=2); totf.grid_columnconfigure(3,weight=4)

    def _exp_setcat(self, cat):
        self._exp_filter = cat; self._go("expenditure")

    def _del_exp(self, rid):
        with get_db() as conn:
            conn.execute("DELETE FROM expenditure WHERE id=?", (rid,))
        self._go("expenditure")

    # ══════════════════════════════════════════════════════════════════════════
    # WASTE
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_waste(self):
        self._hdr("♻️  Waste Management",
                  datetime.now().strftime("📅  %d %B %Y"))
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(14,PAD))

        wc = card(wrap); wc.pack(fill="x", pady=(0,14))
        band(wc, "📝  Record Wastage")
        ff = ctk.CTkFrame(wc, fg_color="transparent"); ff.pack(fill="x", padx=18, pady=14)

        for i,(lbl_t,attr,ph) in enumerate([
            ("Item Name","_wi","e.g., Rice, Vegetables"),
            ("Qty Wasted","_wq","e.g., 2.5"),
            ("Estimated Cost (₹)","_wc","e.g., 150"),
        ]):
            lbl(ff,lbl_t,size=11,weight="bold",color=ARMY_BG).grid(row=0,column=i,sticky="w",padx=(0 if i==0 else 16,0),pady=(0,4))
            e = entry(ff,ph=ph,h=38)
            e.grid(row=1,column=i,sticky="ew",padx=(0 if i==0 else 16,0))
            setattr(self, attr, e)
            ff.grid_columnconfigure(i, weight=1)

        lbl(ff,"Reason",size=11,weight="bold",color=ARMY_BG).grid(row=2,column=0,columnspan=2,sticky="w",pady=(10,4))
        self._wr = ctk.CTkOptionMenu(ff, values=["Spoilage","Preparation Error","Plate Waste",
            "Burn/Over-cooked","Storage Issue","Customer Return","Expiry","Other"])
        self._wr.set("Spoilage"); self._wr.grid(row=3,column=0,columnspan=3,sticky="ew")

        btn(wc,"✅  Record Waste",self._save_waste,fg=ORANGE,hv="#EA580C",h=44).pack(padx=18,pady=(0,14),fill="x")

        # Today's log
        lc = card(wrap); lc.pack(fill="both", expand=True)
        band(lc, "📋  Today's Waste Log")
        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            wr = conn.execute("SELECT * FROM waste_tracker WHERE date=? ORDER BY id DESC",(today,)).fetchall()
        if not wr:
            lbl(lc,"✅  No wastage recorded today.",size=12,color=GREEN).pack(pady=22)
        else:
            COLS = [("Item",3),("Qty",1),("Reason",2),("Cost",1),("By",2)]
            thead(lc, COLS, bg=STRIPE, tc=MID)
            total_wc = 0
            for ix, w in enumerate(wr):
                total_wc += w["cost_lost"] or 0
                trow(lc,[w["item"],f"{w['qty_wasted']:.1f}",w["reason"],
                         f"₹{w['cost_lost']:.0f}",w["recorded_by"] or "—"],
                     [3,1,2,1,2], bg=WHITE if ix%2==0 else STRIPE)
            tot = ctk.CTkFrame(lc, fg_color=BG_RED, height=36, corner_radius=0)
            tot.pack(fill="x"); tot.pack_propagate(False)
            lbl(tot,"TOTAL WASTE COST",size=11,weight="bold",color=RED).grid(row=0,column=0,padx=14,sticky="w")
            lbl(tot,f"₹{total_wc:,.0f}",size=13,weight="bold",color=RED).grid(row=0,column=3,padx=14,sticky="e")
            tot.grid_columnconfigure(1,weight=1); tot.grid_columnconfigure(2,weight=1)

    def _save_waste(self):
        try:
            qty  = float(self._wq.get())
            cost = float(self._wc.get())
        except ValueError:
            self._popup("⚠️ Invalid","Numeric values for qty and cost."); return
        item = self._wi.get().strip()
        if not item or qty <= 0:
            self._popup("⚠️ Invalid","Item name and qty are required."); return
        with get_db() as conn:
            conn.execute("INSERT INTO waste_tracker (date,item,qty_wasted,reason,cost_lost,recorded_by) VALUES (?,?,?,?,?,?)",
                         (datetime.now().strftime("%Y-%m-%d"), item, qty,
                          self._wr.get(), cost, self._user["name"]))
        self._popup("✅ Waste Recorded!", f"{item} ({qty}) — {self._wr.get()}")
        self._go("waste")

    # ══════════════════════════════════════════════════════════════════════════
    # DAILY REPORT — date picker + PDF export
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_report(self):
        today = datetime.now().strftime("%Y-%m-%d")
        hf = self._hdr("📋  Daily Operations Report",
                       "Select date range  •  Export to PDF")

        # Period toggles
        pbar = ctk.CTkFrame(hf, fg_color="transparent"); pbar.pack(side="right", padx=PAD)
        for code, lbl_t in [("today","Today"),("7d","7 Days"),("30d","Month"),("90d","Quarter")]:
            ctk.CTkButton(pbar, text=lbl_t, width=80, height=30, corner_radius=8,
                          font=ctk.CTkFont(size=11, weight="bold"),
                          fg_color=SAFFRON if self._report_period==code else STRIPE,
                          text_color=ARMY_BG if self._report_period==code else DARK,
                          hover_color=ARMY_HVR,
                          command=lambda p=code: self._set_rperiod(p)).pack(side="left",padx=2)

        # Compute date range
        if self._report_period == "today":
            start = end = today
        elif self._report_period == "7d":
            start = (datetime.now()-timedelta(days=6)).strftime("%Y-%m-%d"); end = today
        elif self._report_period == "30d":
            start = (datetime.now()-timedelta(days=29)).strftime("%Y-%m-%d"); end = today
        else:
            start = (datetime.now()-timedelta(days=89)).strftime("%Y-%m-%d"); end = today

        with get_db() as conn:
            s_rows = conn.execute("SELECT * FROM sales WHERE date>=? AND date<=? ORDER BY date DESC",
                                  (start,end)).fetchall()
            e_rows = conn.execute("SELECT category,SUM(amount) AS t FROM expenditure WHERE date>=? AND date<=? GROUP BY category",
                                  (start,end)).fetchall()
            w_row  = conn.execute("SELECT COALESCE(SUM(cost_lost),0) AS t FROM waste_tracker WHERE date>=? AND date<=?",
                                  (start,end)).fetchone()
            inv    = conn.execute("SELECT * FROM inventory ORDER BY cat,item").fetchall()

        rev   = sum(r["sp"]*r["sold"] for r in s_rows)
        cogs  = sum(r["cogs"] for r in s_rows)
        meals = sum(r["sold"] for r in s_rows)
        waste = int(w_row["t"] or 0)
        exp   = sum(r["t"] or 0 for r in e_rows)
        gp    = rev - cogs
        net   = gp - exp - waste
        cash_a = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"]=="Cash")
        upi_a  = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"]=="UPI")
        card_a = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"]=="Card")

        scroll = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=PAD, pady=(12,PAD))

        # Export button
        ebf = ctk.CTkFrame(scroll, fg_color="transparent"); ebf.pack(fill="x", pady=(0,12))
        btn(ebf, "📄  Export as PDF", lambda: self._export_pdf_report(start, end),
            fg=ARMY_BG, hv=ARMY_HVR, h=42).pack(side="right")

        # Report letterhead
        rc = card(scroll, border_width=2); rc.pack(fill="x", pady=(0,14))
        lh = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=90)
        lh.pack(fill="x"); lh.pack_propagate(False)
        tricolor(lh, 4)
        li = ctk.CTkFrame(lh, fg_color="transparent"); li.pack(fill="both", expand=True, padx=PAD, pady=6)
        lbl(li,"🇮🇳  56 APO FIELD CANTEEN — INDIAN ARMY",size=11,weight="bold",color=GOLD_LT).pack(anchor="w")
        lbl(li,"DAILY OPERATIONS REPORT",size=18,weight="bold",color=WHITE).pack(anchor="w",pady=(2,0))
        lbl(li,f"Period: {start} to {end}",size=10,color=GOLD).pack(anchor="w")

        # KPI cards
        kf = ctk.CTkFrame(rc, fg_color="transparent"); kf.pack(fill="x", padx=PAD, pady=(20,0))
        kf.grid_rowconfigure(0, weight=1)
        for i,(icon,t,v,tc,bg_c,br) in enumerate([
            ("💰","Revenue",f"₹{rev:,.0f}",GREEN,BG_GRN,T_GRN),
            ("🍽","Meals",str(meals),SAFFRON,BG_SAF,T_SAF),
            ("♻️","Waste Cost",f"₹{waste:,.0f}",ORANGE,BG_SAF,T_SAF),
            ("💸","Expenditure",f"₹{exp:,.0f}",PURPLE,BG_PUR,T_PUR),
            ("📈","Net Profit",f"₹{net:,.0f}",net>=0 and BLUE or RED,BG_BLU,T_BLU),
        ]):
            kc = card(kf, fg_color=bg_c, border_color=br)
            kc.grid(row=0,column=i,padx=(0 if i==0 else 10),sticky="nsew")
            kf.grid_columnconfigure(i, weight=1)
            lbl(kc,icon,size=22).pack(anchor="w",padx=16,pady=(12,2))
            lbl(kc,t,size=10,color=MID).pack(anchor="w",padx=16)
            lbl(kc,v,size=17,weight="bold",color=tc).pack(anchor="w",padx=16,pady=(2,12))

        # Meal Sales Table
        self._rept_section(rc, "Meal Sales Summary",
            [("Date",2),("Meal",4),("Sold",1),("Wastage",1),("COGS",2),("Revenue",2),("Payment",1)],
            [[r["date"],r["meal"],str(r["sold"]),str(r["wastage"]),
              f"₹{r['cogs']:,.0f}",f"₹{r['sp']*r['sold']:,.0f}",r["payment"]]
             for r in s_rows],
            [2,4,1,1,2,2,1])

        # Payment breakdown
        pmf = ctk.CTkFrame(rc, fg_color="transparent"); pmf.pack(fill="x", padx=PAD, pady=(20,0))
        pmf.grid_rowconfigure(0,weight=1)
        for i,(mode,amt,clr,bg_c,br) in enumerate([
            ("💵 Cash",cash_a,GREEN,BG_GRN,T_GRN),
            ("📱 UPI",upi_a,PURPLE,BG_PUR,T_PUR),
            ("💳 Card",card_a,BLUE,BG_BLU,T_BLU),
        ]):
            pc = card(pmf,fg_color=bg_c,border_color=br)
            pc.grid(row=0,column=i,padx=(0 if i==0 else 10),sticky="nsew")
            pmf.grid_columnconfigure(i,weight=1)
            lbl(pc,mode,size=13,weight="bold",color=clr).pack(padx=16,pady=(14,4),anchor="w")
            lbl(pc,f"₹{amt:,.0f}",size=20,weight="bold",color=clr).pack(padx=16,pady=(0,2),anchor="w")
            pct = f"{amt/rev*100:.0f}%" if rev else "0%"
            lbl(pc,pct,size=10,color=MID).pack(padx=16,pady=(0,14),anchor="w")

        # Expenditure breakdown
        if e_rows:
            self._rept_section(rc,"Expenditure Summary",
                [("Category",4),("Amount",2)],
                [[r["category"],f"₹{r['t']:,.0f}"] for r in e_rows],
                [4,2])

        # Inventory closing stock
        self._rept_section(rc,"Inventory Closing Stock",
            [("Item",4),("Category",2),("Unit",1),("Opening",1),("Received",1),("Stock",1),("Status",1)],
            [[i["item"],i["cat"],i["unit"],f"{i['opening']:.1f}",f"{i['received']:.1f}",
              f"{i['stock']:.1f}","⚠ LOW" if i["stock"]<i["min_lvl"] else "✓ OK"]
             for i in inv],
            [4,2,1,1,1,1,1])

        # Signature block
        sf = ctk.CTkFrame(rc, fg_color="transparent"); sf.pack(fill="x", padx=PAD, pady=(20,16))
        sf.grid_rowconfigure(0,weight=1)
        for i,(role,name) in enumerate([
            ("Prepared By","Canteen Manager (JCO)"),
            ("Checked By","Supervision Officer"),
            ("Approved By","Officer-in-Charge"),
        ]):
            sc = card(sf); sc.grid(row=0,column=i,padx=(0 if i==0 else 14),sticky="nsew")
            sf.grid_columnconfigure(i,weight=1)
            lbl(sc,role,size=10,color=MID,weight="bold").pack(padx=14,pady=(12,2),anchor="w")
            lbl(sc,name,size=11,color=DARK).pack(padx=14,anchor="w")
            lbl(sc,"Signature: ________________________",size=10,color=MID).pack(padx=14,pady=(8,4),anchor="w")
            lbl(sc,f"Date: {end}",size=10,color=MID).pack(padx=14,pady=(0,12),anchor="w")

        ft = ctk.CTkFrame(rc, fg_color="transparent", height=6); ft.pack(fill="x"); ft.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ft, fg_color=c).pack(side="left", fill="both", expand=True)
        lbl(rc,"जय हिन्द  •  CONFIDENTIAL — For Official Use Only  •  " +
            datetime.now().strftime("Generated: %d %b %Y %I:%M %p"),
            size=9, color=MID).pack(pady=(8,14))

    def _rept_section(self, parent, title, cols, rows, wts):
        band(parent, title, bg=ARMY_BG, tc=GOLD_LT, h=40)
        thead(parent, cols, bg=STRIPE, tc=MID)
        for ix, r in enumerate(rows):
            trow(parent, r, wts, bg=WHITE if ix%2==0 else STRIPE)

    def _set_rperiod(self, p):
        self._report_period = p; self._go("report")

    # ── PDF Export ──────────────────────────────────────────────────────────
    def _export_pdf_report(self, start, end):
        if not PDF_AVAILABLE:
            self._popup("⚠️ PDF Error",
                        "ReportLab is not installed.\nRun: pip install reportlab")
            return

        fname = f"DailyReport_{start}_to_{end}.pdf"
        out   = os.path.join(BASE_DIR, fname)

        with get_db() as conn:
            s_rows = conn.execute("SELECT * FROM sales WHERE date>=? AND date<=? ORDER BY date DESC",
                                  (start,end)).fetchall()
            e_rows = conn.execute("SELECT * FROM expenditure WHERE date>=? AND date<=? ORDER BY date DESC",
                                  (start,end)).fetchall()
            w_rows = conn.execute("SELECT * FROM waste_tracker WHERE date>=? AND date<=?",
                                  (start,end)).fetchall()
            inv    = conn.execute("SELECT * FROM inventory ORDER BY cat,item").fetchall()

        rev    = sum(r["sp"]*r["sold"] for r in s_rows)
        cogs   = sum(r["cogs"] for r in s_rows)
        meals  = sum(r["sold"] for r in s_rows)
        waste  = sum(w["cost_lost"] or 0 for w in w_rows)
        exp    = sum(r["amount"] for r in e_rows)
        net    = rev - cogs - exp - waste

        # ReportLab colours
        OliveGreen = RL_COLORS.HexColor("#1F3320")
        Gold       = RL_COLORS.HexColor("#C9A84C")
        Saffron    = RL_COLORS.HexColor("#FF9933")
        TableHdr   = RL_COLORS.HexColor("#253D27")
        AltRow     = RL_COLORS.HexColor("#F5FAF5")
        BgGreen    = RL_COLORS.HexColor("#F0FDF4")
        BgOrange   = RL_COLORS.HexColor("#FFF7ED")

        W_A4, H_A4 = A4
        styles = getSampleStyleSheet()

        def S(name, **kw): return ParagraphStyle(name, **kw)
        TITLE = S("T", fontName="Helvetica-Bold", fontSize=18, textColor=RL_COLORS.white, alignment=TA_CENTER)
        SUB   = S("S", fontName="Helvetica",      fontSize=10, textColor=Gold, alignment=TA_CENTER)
        SEC   = S("H", fontName="Helvetica-Bold", fontSize=12, textColor=OliveGreen)
        BODY  = S("B", fontName="Helvetica",      fontSize=9,  textColor=RL_COLORS.black, leading=14)
        TH    = S("TH",fontName="Helvetica-Bold", fontSize=9,  textColor=RL_COLORS.white, alignment=TA_CENTER)
        TD    = S("TD",fontName="Helvetica",      fontSize=8,  textColor=RL_COLORS.black, alignment=TA_CENTER)
        TDL   = S("TDL",fontName="Helvetica",     fontSize=8,  textColor=RL_COLORS.black)

        def pdf_table(headers, rows_data, col_widths):
            hrow = [Paragraph(h, TH) for h in headers]
            data = [hrow] + [[Paragraph(str(v), TD) for v in row] for row in rows_data]
            t = Table(data, colWidths=col_widths, repeatRows=1)
            cmds = [
                ("BACKGROUND",    (0,0), (-1,0),  TableHdr),
                ("FONTNAME",      (0,0), (-1,-1), "Helvetica"),
                ("FONTSIZE",      (0,0), (-1,-1), 8),
                ("ALIGN",         (0,0), (-1,-1), "CENTER"),
                ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
                ("TOPPADDING",    (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("ROWBACKGROUNDS",(0,1), (-1,-1), [RL_COLORS.white, AltRow]),
                ("GRID",          (0,0), (-1,-1), 0.3, RL_COLORS.HexColor("#CCCCBB")),
                ("LINEABOVE",     (0,0), (-1,0),  1.5, Gold),
                ("LINEBELOW",     (0,-1),(-1,-1), 1.5, Gold),
            ]
            t.setStyle(TableStyle(cmds)); return t

        story = []

        # Letterhead
        lh_data = [[Paragraph("🇮🇳  INDIAN ARMY — 56 APO FIELD CANTEEN", TITLE)]]
        lh_t = Table(lh_data, colWidths=[W_A4 - 4*cm])
        lh_t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), OliveGreen),
            ("TOPPADDING", (0,0), (-1,-1), 16),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ]))
        story.append(lh_t)
        story.append(Paragraph(f"DAILY OPERATIONS REPORT  |  Period: {start} to {end}", SUB))
        story.append(Spacer(1, 0.4*cm))

        # KPI summary
        kpi_d = [
            [Paragraph("Total Revenue", TH), Paragraph(f"₹ {rev:,.0f}", TD),
             Paragraph("Total COGS",   TH), Paragraph(f"₹ {cogs:,.0f}", TD),
             Paragraph("Net Profit",   TH), Paragraph(f"₹ {net:,.0f}",  TD)],
        ]
        kpi_t = Table(kpi_d, colWidths=[3*cm, 3.5*cm, 3*cm, 3.5*cm, 3*cm, 3.5*cm])
        kpi_t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,0), OliveGreen), ("BACKGROUND", (2,0),(2,0), OliveGreen),
            ("BACKGROUND",    (4,0), (4,0), OliveGreen),
            ("TOPPADDING",    (0,0), (-1,-1), 10), ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("BOX",           (0,0), (-1,-1), 1, Gold),
        ]))
        story.append(kpi_t)
        story.append(Spacer(1, 0.5*cm))

        # Sales
        story.append(Paragraph("Meal Sales Summary", SEC))
        story.append(Spacer(1, 0.15*cm))
        if s_rows:
            story.append(pdf_table(
                ["Date","Meal Item","Sold","Wastage","Rate","Revenue","Payment"],
                [[r["date"],r["meal"],str(r["sold"]),str(r["wastage"]),
                  f"Rs.{r['sp']:.0f}",f"Rs.{r['sp']*r['sold']:,.0f}",r["payment"]]
                 for r in s_rows],
                [2*cm, 5*cm, 1.5*cm, 2*cm, 1.5*cm, 2.5*cm, 2*cm]))
        else:
            story.append(Paragraph("No sales recorded for this period.", BODY))
        story.append(Spacer(1, 0.5*cm))

        # Expenditure
        story.append(Paragraph("Expenditure", SEC)); story.append(Spacer(1, 0.15*cm))
        if e_rows:
            story.append(pdf_table(
                ["Date","Category","Amount","Notes"],
                [[r["date"],r["category"],f"Rs.{r['amount']:,.0f}",r["notes"] or "—"] for r in e_rows],
                [2*cm, 5*cm, 2.5*cm, 7*cm]))
        else:
            story.append(Paragraph("No expenditure recorded.", BODY))
        story.append(Spacer(1, 0.5*cm))

        # Inventory
        story.append(Paragraph("Inventory Closing Stock", SEC)); story.append(Spacer(1, 0.15*cm))
        story.append(pdf_table(
            ["Item","Category","Unit","Opening","Received","Closing","Status"],
            [[i["item"],i["cat"],i["unit"],f"{i['opening']:.1f}",f"{i['received']:.1f}",
              f"{i['stock']:.1f}","LOW" if i["stock"]<i["min_lvl"] else "OK"]
             for i in inv],
            [4*cm, 2.5*cm, 1.5*cm, 2*cm, 2*cm, 2*cm, 2*cm]))
        story.append(Spacer(1, 0.5*cm))

        # Signature
        sig_d = [[
            Paragraph("Prepared By\nCanteen Manager (JCO)\n\nSignature: _______________\n\nDate: "+end, BODY),
            Paragraph("Checked By\nSupervision Officer\n\nSignature: _______________\n\nDate: "+end, BODY),
            Paragraph("Approved By\nOfficer-in-Charge (Captain)\n\nSignature: _______________\n\nDate: "+end, BODY),
        ]]
        sig_t = Table(sig_d, colWidths=[(W_A4-4*cm)/3]*3)
        sig_t.setStyle(TableStyle([
            ("BOX",           (0,0), (-1,-1), 0.5, OliveGreen),
            ("INNERGRID",     (0,0), (-1,-1), 0.5, OliveGreen),
            ("TOPPADDING",    (0,0), (-1,-1), 12),
            ("BOTTOMPADDING", (0,0), (-1,-1), 12),
            ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ]))
        story.append(sig_t)
        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("CONFIDENTIAL — For Official Use Only  |  जय हिन्द",
                                S("FT", fontName="Helvetica-Oblique", fontSize=8,
                                  textColor=RL_COLORS.grey, alignment=TA_CENTER)))

        # Build
        def on_page(canv, doc):
            canv.saveState()
            canv.setFillColor(OliveGreen)
            canv.rect(0, 0, W_A4, 0.7*cm, fill=1, stroke=0)
            canv.setFillColor(Gold)
            canv.setFont("Helvetica", 7)
            canv.drawCentredString(W_A4/2, 0.22*cm,
                "INDIAN ARMY  |  56 APO FIELD CANTEEN  |  CONFIDENTIAL")
            canv.drawRightString(W_A4 - 1*cm, 0.22*cm, f"Page {doc.page}")
            canv.restoreState()

        doc = SimpleDocTemplate(out, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=1.5*cm)
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

        self._popup("✅ PDF Exported!", f"Report saved to:\n{fname}")
        try:
            import subprocess; subprocess.Popen(["open", out])
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════════════════
    # MASTER DATA — Menu + Inventory tabs
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_master(self):
        self._hdr("🧾  Master Data", "Manage menus, recipes, inventory items")
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(12,PAD))

        # Menu master
        mc = card(wrap); mc.pack(fill="x", pady=(0,14))
        def _add_menu_btn(p):
            btn(p,"＋ Add Menu Item",self._dlg_add_menu,fg=GREEN,hv=DGREEN,h=30,w=160).pack(side="right",padx=12)
        band(mc,"🍽  Menu Master — Active Items", side_btn=_add_menu_btn)
        COLS = [("Menu Item",4),("Sale Price",1),("Active",1),("Edit",1)]
        thead(mc, COLS, bg=STRIPE, tc=MID)
        with get_db() as conn:
            menus = conn.execute("SELECT * FROM menu ORDER BY name").fetchall()
        for ix, m in enumerate(menus):
            rf = ctk.CTkFrame(mc, fg_color=WHITE if ix%2==0 else STRIPE, corner_radius=0, height=40)
            rf.pack(fill="x"); rf.pack_propagate(False)
            lbl(rf,f"  {m['name']}",size=12,weight="bold",color=DARK).grid(row=0,column=0,padx=14,sticky="w")
            lbl(rf,f"₹{m['sp']:.0f}",size=11,color=MID).grid(row=0,column=1,sticky="w")
            status_lbl = "✓ Yes" if m["active"] else "✗ No"
            lbl(rf,status_lbl,size=11,
                color=GREEN if m["active"] else RED,weight="bold").grid(row=0,column=2,sticky="w")
            ctk.CTkButton(rf,text="✏️ Edit",width=64,height=26,corner_radius=6,
                          fg_color=BLUE,hover_color=DBLUE,font=ctk.CTkFont(size=10,weight="bold"),
                          command=lambda mid=m["id"],nm=m["name"],sp=m["sp"],ac=m["active"]:
                              self._dlg_edit_menu(mid,nm,sp,ac)).grid(row=0,column=3,padx=8,sticky="e")
            rf.grid_columnconfigure(0,weight=4); rf.grid_columnconfigure(1,weight=1)
            rf.grid_columnconfigure(2,weight=1); rf.grid_columnconfigure(3,weight=1)

    def _dlg_add_menu(self):
        win = ctk.CTkToplevel(self); win.title("Add Menu Item")
        win.geometry("460x240"); win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win,"＋  Add New Menu Item",h=44)
        lbl(win,"Item Name",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(16,4))
        e_name = entry(win,ph="e.g., Veg Pulao",h=38); e_name.pack(fill="x",padx=24)
        lbl(win,"Selling Price (₹)",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(12,4))
        e_sp = entry(win,ph="e.g., 60",h=38); e_sp.pack(fill="x",padx=24)
        def save():
            nm = e_name.get().strip()
            try: sp = float(e_sp.get())
            except: self._popup("⚠️ Invalid","Numeric price."); return
            if not nm: self._popup("⚠️ Missing","Enter item name."); return
            with get_db() as conn:
                try: conn.execute("INSERT INTO menu (name,sp) VALUES (?,?)", (nm,sp))
                except sqlite3.IntegrityError: self._popup("⚠️ Duplicate","Item exists."); return
            self._popup("✅ Added!", f"{nm} added."); win.destroy(); self._go("master")
        btn(win,"✅  Add Item",save,fg=GREEN,hv=DGREEN,h=44).pack(padx=24,pady=14,fill="x")

    def _dlg_edit_menu(self, mid, name, sp, active):
        win = ctk.CTkToplevel(self); win.title("Edit Menu Item")
        win.geometry("460x260"); win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win,f"✏️  Edit: {name}",h=44)
        lbl(win,"Selling Price (₹)",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(16,4))
        e_sp = entry(win,ph="e.g., 70",h=38); e_sp.insert(0,str(sp)); e_sp.pack(fill="x",padx=24)
        lbl(win,"Status",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(12,4))
        status_v = ctk.CTkOptionMenu(win,values=["Active","Inactive"])
        status_v.set("Active" if active else "Inactive"); status_v.pack(fill="x",padx=24)
        def save():
            try: new_sp = float(e_sp.get())
            except: self._popup("⚠️ Invalid","Numeric price."); return
            new_ac = 1 if status_v.get()=="Active" else 0
            with get_db() as conn:
                conn.execute("UPDATE menu SET sp=?,active=? WHERE id=?",(new_sp,new_ac,mid))
            self._popup("✅ Updated!",f"{name} updated."); win.destroy(); self._go("master")
        btn(win,"✅  Save",save,fg=BLUE,hv=DBLUE,h=44).pack(padx=24,pady=14,fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # USER MANAGEMENT — Create/Edit/Toggle, with role picker
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_users(self):
        self._hdr("👥  User Management", "Create  •  Edit  •  Assign Roles  •  Activate / Deactivate")
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(12,PAD))

        ab = ctk.CTkFrame(wrap, fg_color="transparent"); ab.pack(fill="x", pady=(0,14))
        btn(ab,"＋  Add New User",  self._dlg_add_user,  fg=GREEN, hv=DGREEN, h=38).pack(side="left")
        btn(ab,"🔄  Reset Password",self._dlg_reset_pwd, fg=BLUE,  hv=DBLUE,  h=38).pack(side="left",padx=8)
        btn(ab,"🔑  Toggle Active",  self._dlg_toggle_user,fg=TEAL,hv=ARMY_BG,h=38).pack(side="left")

        uc = card(wrap); uc.pack(fill="both", expand=True)
        band(uc,"👥  All Users & Role Permissions")
        COLS = [("Username",2),("Full Name",2),("Rank",1),("Roles",2),("Status",1),("Contact",2)]
        thead(uc, COLS, bg=STRIPE, tc=MID)
        with get_db() as conn:
            users = conn.execute(
                "SELECT u.id,u.username,u.name,u.rank,u.active,u.contact, "
                "GROUP_CONCAT(r.role,', ') AS roles FROM users u "
                "LEFT JOIN user_roles r ON r.user_id=u.id "
                "GROUP BY u.id ORDER BY u.username").fetchall()
        for ix, u in enumerate(users):
            bg2 = WHITE if ix%2==0 else STRIPE
            st_icon = "✅ Active" if u["active"] else "❌ Inactive"
            st_color = GREEN if u["active"] else RED
            trow(uc,[u["username"],u["name"],u["rank"],
                     u["roles"] or "None", st_icon, u["contact"] or "—"],
                 [2,2,1,2,1,2],
                 colors=[DARK,DARK,MID,MID,st_color,MID],
                 bolds=[True,True,False,False,True,False], bg=bg2)

    def _dlg_add_user(self):
        win = ctk.CTkToplevel(self); win.title("Add New User")
        win.geometry("520x520"); win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win,"＋  Create New User Account",h=44)
        fields = {}
        for lbl_t, attr, ph, pw in [
            ("Username","_nu","e.g., jco_smith",False),
            ("Full Name","_nn","e.g., JCO Ramesh Smith",False),
            ("Rank","_nr","e.g., JCO, Havildar, Captain",False),
            ("Contact","_nc","e.g., 9876543210",False),
            ("Password","_np","Minimum 6 characters",True),
        ]:
            lbl(win,lbl_t,size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(12,3))
            e = ctk.CTkEntry(win,height=38,corner_radius=10,placeholder_text=ph,
                             show="●" if pw else "",font=ctk.CTkFont(size=12),border_color=BORDER)
            e.pack(fill="x",padx=24); fields[attr] = e

        lbl(win,"Role (Permissions)",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(12,3))
        role_m = ctk.CTkOptionMenu(win,values=["manager","officer","waste_mgr"])
        role_m.set("manager"); role_m.pack(fill="x",padx=24)

        def save():
            un = fields["_nu"].get().strip(); nm = fields["_nn"].get().strip()
            rk = fields["_nr"].get().strip(); ct = fields["_nc"].get().strip()
            pw = fields["_np"].get()
            if not all([un,nm,rk,pw]):
                self._popup("⚠️ Missing","Fill all required fields."); return
            if len(pw) < 6:
                self._popup("⚠️ Weak Password","At least 6 characters."); return
            with get_db() as conn:
                try:
                    cur = conn.execute("INSERT INTO users (username,pw_hash,name,rank,contact) VALUES (?,?,?,?,?)",
                                       (un,_hash(pw),nm,rk,ct))
                    conn.execute("INSERT INTO user_roles (user_id,role) VALUES (?,?)",
                                 (cur.lastrowid, role_m.get()))
                except sqlite3.IntegrityError:
                    self._popup("⚠️ Duplicate","Username already exists."); return
            self._popup("✅ User Created!",f"{un} ({role_m.get()}) created.")
            win.destroy(); self._go("users")

        btn(win,"✅  Create User",save,fg=GREEN,hv=DGREEN,h=46).pack(padx=24,pady=16,fill="x")

    def _dlg_reset_pwd(self):
        win = ctk.CTkToplevel(self); win.title("Reset Password")
        win.geometry("480x260"); win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win,"🔄  Reset User Password",h=44)
        with get_db() as conn:
            users = [r["username"] for r in conn.execute("SELECT username FROM users ORDER BY username")]
        lbl(win,"Select User",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(16,4))
        um = ctk.CTkOptionMenu(win,values=users); um.set(users[0] if users else ""); um.pack(fill="x",padx=24,pady=(0,12))
        lbl(win,"New Password",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(0,4))
        e_pw = ctk.CTkEntry(win,height=38,corner_radius=10,placeholder_text="Min 6 chars",
                            show="●",font=ctk.CTkFont(size=12)); e_pw.pack(fill="x",padx=24)
        def save():
            pw = e_pw.get()
            if len(pw) < 6: self._popup("⚠️ Weak","At least 6 characters."); return
            with get_db() as conn:
                conn.execute("UPDATE users SET pw_hash=? WHERE username=?",(_hash(pw),um.get()))
            self._popup("✅ Password Reset!",f"{um.get()}'s password updated."); win.destroy()
        btn(win,"✅  Reset",save,fg=BLUE,hv=DBLUE,h=44).pack(padx=24,pady=16,fill="x")

    def _dlg_toggle_user(self):
        win = ctk.CTkToplevel(self); win.title("Toggle Active Status")
        win.geometry("480x240"); win.resizable(False,False); win.configure(fg_color=WHITE)
        band(win,"🔑  Activate / Deactivate User",h=44)
        with get_db() as conn:
            users = [(r["username"],r["active"]) for r in conn.execute(
                "SELECT username,active FROM users ORDER BY username")]
        un_list = [u[0] for u in users]
        lbl(win,"Select User",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(16,4))
        um = ctk.CTkOptionMenu(win,values=un_list); um.set(un_list[0] if un_list else ""); um.pack(fill="x",padx=24,pady=(0,10))
        lbl(win,"New Status",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",padx=24,pady=(0,4))
        sm = ctk.CTkOptionMenu(win,values=["Active","Inactive"]); sm.set("Active"); sm.pack(fill="x",padx=24)
        def save():
            new_ac = 1 if sm.get()=="Active" else 0
            with get_db() as conn:
                conn.execute("UPDATE users SET active=? WHERE username=?",(new_ac,um.get()))
            self._popup("✅ Updated!",f"{um.get()} is now {sm.get()}."); win.destroy(); self._go("users")
        btn(win,"✅  Update",save,fg=TEAL,hv=ARMY_BG,h=44).pack(padx=24,pady=14,fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # BACKUP & RESTORE
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_backup(self):
        self._hdr("💾  Database Backup & Restore",
                  f"Backups folder: {BCK_DIR}")
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(14,PAD))

        # Backup actions
        ac = card(wrap); ac.pack(fill="x", pady=(0,16))
        band(ac,"💾  Create Backup")
        inf = ctk.CTkFrame(ac, fg_color="transparent"); inf.pack(fill="x", padx=18, pady=12)
        lbl(inf,f"Current DB: {DB_PATH}",size=11,color=MID).pack(anchor="w")
        lbl(inf,f"Backup dir: {BCK_DIR}",size=11,color=MID).pack(anchor="w",pady=(2,0))
        lbl(inf,"Each backup is a timestamped copy of canteen.db.",size=11,color=MID).pack(anchor="w",pady=(2,0))

        bf2 = ctk.CTkFrame(ac, fg_color="transparent"); bf2.pack(fill="x", padx=18, pady=(0,16))
        btn(bf2,"💾  Backup Now",self._do_backup,fg=GREEN,hv=DGREEN,h=44).pack(side="left")
        btn(bf2,"📂  Open Backup Folder",lambda: self._open_folder(BCK_DIR),
            fg=ARMY_BG,hv=ARMY_HVR,h=44).pack(side="left",padx=10)

        # Restore
        rc = card(wrap); rc.pack(fill="x", pady=(0,16))
        band(rc,"🔄  Restore from Backup", bg=DRED, tc=WHITE)
        lbl(rc,"⚠️  Restoring replaces the current database with the selected backup.",
            size=11,color=RED).pack(anchor="w",padx=18,pady=(10,4))

        backups = sorted(
            [f for f in os.listdir(BCK_DIR) if f.endswith(".db")], reverse=True)

        if not backups:
            lbl(rc,"No backups found. Create one first.",size=12,color=MID).pack(pady=14)
        else:
            bf3 = ctk.CTkFrame(rc, fg_color="transparent"); bf3.pack(fill="x", padx=18, pady=(4,12))
            lbl(bf3,"Select Backup",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(0,4))
            bm = ctk.CTkOptionMenu(bf3,values=backups); bm.set(backups[0])
            bm.pack(fill="x",pady=(0,12))
            btn(bf3,"🔄  Restore Selected Backup",
                lambda: self._do_restore(bm.get()),
                fg=RED,hv=DRED,h=44).pack(fill="x")

        # Backup log
        lc = card(wrap); lc.pack(fill="both", expand=True)
        band(lc,"📋  Backup History")
        if not backups:
            lbl(lc,"No backups yet.",size=12,color=MID).pack(pady=18)
        else:
            COLS = [("Filename",5),("Size",2),("Created",3)]
            thead(lc, COLS, bg=STRIPE, tc=MID)
            for ix, bf_name in enumerate(backups):
                fpath = os.path.join(BCK_DIR, bf_name)
                sz = os.path.getsize(fpath)
                ctime = datetime.fromtimestamp(os.path.getctime(fpath)).strftime("%d %b %Y  %H:%M")
                trow(lc,[bf_name,f"{sz//1024} KB",ctime],[5,2,3],
                     bg=WHITE if ix%2==0 else STRIPE)

    def _do_backup(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(BCK_DIR, f"canteen_backup_{ts}.db")
        shutil.copy2(DB_PATH, dest)
        self._popup("✅ Backup Created!", f"Saved as:\ncanteen_backup_{ts}.db")
        self._go("backup")

    def _do_restore(self, fname):
        src = os.path.join(BCK_DIR, fname)
        if not messagebox.askyesno("Confirm Restore",
                                   f"Restore from:\n{fname}\n\nThis will OVERWRITE the current database!\nAll unsaved changes will be lost."):
            return
        shutil.copy2(src, DB_PATH)
        init_db()   # re-apply any missing schema
        self._popup("✅ Restored!", f"Database restored from:\n{fname}\n\nPlease restart the app for full effect.")

    def _open_folder(self, path):
        try:
            import subprocess; subprocess.Popen(["open", path])
        except Exception:
            pass

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CanteenApp()
    app.mainloop()
