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

# ── Matplotlib for dashboard charts ───────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    CHART_OK = True
except ImportError:
    CHART_OK = False

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
import sys

if getattr(sys, "frozen", False):
    # Running as a PyInstaller bundle: put the database NEXT TO the .exe
    # so it persists across runs and is not wiped from the temp folder.
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as a normal Python script
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
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL DEFAULT CURRENT_DATE,
                menu_id INTEGER REFERENCES menu(id),
                meal TEXT NOT NULL,
                sp REAL NOT NULL DEFAULT 0,
                qty INTEGER NOT NULL DEFAULT 0,
                cost REAL NOT NULL DEFAULT 0,
                given_to TEXT DEFAULT 'General',
                notes TEXT
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

        # Migrations
        if not _has_col(c, "users", "contact"):
            c.execute("ALTER TABLE users ADD COLUMN contact TEXT DEFAULT ''")
        if not _has_col(c, "users", "active"):
            c.execute("ALTER TABLE users ADD COLUMN active INTEGER DEFAULT 1")
        # Store original raw/made/waste so edits can compute deltas
        if not _has_col(c, "recipes", "total_raw"):
            c.execute("ALTER TABLE recipes ADD COLUMN total_raw REAL DEFAULT 0")
        if not _has_col(c, "recipes", "total_made"):
            c.execute("ALTER TABLE recipes ADD COLUMN total_made REAL DEFAULT 0")
        if not _has_col(c, "recipes", "total_waste"):
            c.execute("ALTER TABLE recipes ADD COLUMN total_waste REAL DEFAULT 0")
        # Store cost-of-goods-sold per plate for profit display
        if not _has_col(c, "menu", "cogs"):
            c.execute("ALTER TABLE menu ADD COLUMN cogs REAL DEFAULT 0")

        # ── Samples migration: move misclassified wastage rows into samples table ──
        # Items prepared but sold=0 (AMUL, LAHARI JEERA, LASSI etc.) were stored
        # as wastage. Move them to the samples table and zero out wastage.
        sample_meal_candidates = c.execute(
            "SELECT id, date, menu_id, meal, sp, wastage, cogs FROM sales "
            "WHERE sold = 0 AND wastage > 0"
        ).fetchall()
        for row in sample_meal_candidates:
            # Check there is no existing samples row for this date+meal already
            exists = c.execute(
                "SELECT id FROM samples WHERE date=? AND meal=? COLLATE NOCASE",
                (row[1], row[3])
            ).fetchone()
            if not exists:
                c.execute(
                    "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                    "VALUES (?,?,?,?,?,?,'General','Migrated from wastage')",
                    (row[1], row[2], row[3], row[4], row[5], row[6])
                )
            # Zero out wastage on the sales row
            c.execute("UPDATE sales SET wastage=0 WHERE id=?", (row[0],))

        # Performance indexes (CREATE IF NOT EXISTS is idempotent)
        c.executescript("""
            CREATE INDEX IF NOT EXISTS idx_inventory_cat  ON inventory(cat);
            CREATE INDEX IF NOT EXISTS idx_inventory_item ON inventory(item);
            CREATE INDEX IF NOT EXISTS idx_sales_date     ON sales(date);
            CREATE INDEX IF NOT EXISTS idx_stock_ledger_date ON stock_ledger(date);
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

        # No auto-seed: inventory, menu and recipes are entered by users only

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
    bar = ctk.CTkFrame(parent, fg_color="transparent", height=h, corner_radius=0)
    bar.pack(fill="x")
    
    ctk.CTkFrame(bar, fg_color=SAFFRON, corner_radius=0).place(relx=0.0, rely=0, relwidth=0.3334, relheight=1)
    ctk.CTkFrame(bar, fg_color=WHITE, corner_radius=0).place(relx=0.3333, rely=0, relwidth=0.3334, relheight=1)
    ctk.CTkFrame(bar, fg_color=IND_GREEN, corner_radius=0).place(relx=0.6666, rely=0, relwidth=0.3334, relheight=1)

def band(parent, text, bg=ARMY_BG, tc=GOLD_LT, h=44, side_btn=None):
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    ctk.CTkFrame(hdr, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
    lbl(hdr, f"  {text}", size=12, weight="bold", color=tc).pack(side="left", padx=8)
    if side_btn:
        side_btn(hdr)
    return hdr

def thead(parent, col_defs, bg=ARMY_BG, tc=GOLD_LT, h=36, padx=8):
    hdr = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=h)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    uid = abs(hash(tuple(wt for _, wt in col_defs)))
    for j, (name, wt) in enumerate(col_defs):
        cell = ctk.CTkFrame(hdr, fg_color="transparent", corner_radius=0)
        cell.grid(row=0, column=j, padx=0, pady=0, sticky="nsew")
        lbl(cell, name, size=10, weight="bold", color=tc).pack(
            anchor="w", padx=padx, pady=0)
        cell.grid_columnconfigure(0, weight=1)
        hdr.grid_columnconfigure(j, weight=wt, uniform=f"grp_{uid}")
    hdr.grid_rowconfigure(0, weight=1)
    return hdr

def trow(parent, cols_vals, col_weights, colors=None, bolds=None,
         bg=WHITE, row_h=38, pady=0, padx=8):
    n   = len(cols_vals)
    clr = colors or [DARK] * n
    bld = bolds  or [False] * n
    rf  = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0, height=row_h)
    rf.pack(fill="x")
    rf.pack_propagate(False)
    uid = abs(hash(tuple(col_weights)))
    for j, (v, wt, c, b) in enumerate(zip(cols_vals, col_weights, clr, bld)):
        cell = ctk.CTkFrame(rf, fg_color="transparent", corner_radius=0)
        cell.grid(row=0, column=j, padx=0, pady=0, sticky="nsew")
        # Clip long text with ellipsis to prevent overflow
        text = str(v)
        lbl(cell, text, size=11, weight="bold" if b else "normal", color=c).pack(
            anchor="w", padx=padx, pady=9)
        cell.grid_columnconfigure(0, weight=1)
        rf.grid_columnconfigure(j, weight=wt, uniform=f"grp_{uid}")
    rf.grid_rowconfigure(0, weight=1)
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

    # ==============================================================================
    # LOGIN
    # ==============================================================================
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
            # Only draw the diagonal stripes, remove the Ashok Chakra

        cv.bind("<Configure>", _draw)
        self.after(30, _draw)


        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")
        box = ctk.CTkFrame(outer, fg_color=WHITE, corner_radius=24,
                           border_width=2, border_color=BORDER)
        box.pack()

        hdr = ctk.CTkFrame(box, fg_color=ARMY_BG, corner_radius=0, height=150, width=460)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tricolor(hdr, 4)
        lbl(hdr, "🇮🇳  INDIAN ARMY", size=11, weight="bold", color=GOLD_LT).pack(pady=(10,0))
        lbl(hdr, "CANTEEN MANAGEMENT SYSTEM", size=18, weight="bold", color=WHITE).pack(pady=(3,0))
        lbl(hdr, "AWWA LUNCH PROJECT..", size=14, weight="bold", color=GOLD).pack(pady=(3,0))
        lbl(hdr, "“ Sehat, Swad aur Samman ”", size=10, color="#E2E8F0").pack(pady=(2,10))

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

        sep(box, BORDER).pack(fill="x", pady=(14,0))
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

    # ==============================================================================
    # SHELL
    # ==============================================================================
    def _build_main(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color=LIGHT)

        # Sidebar
        sb = ctk.CTkFrame(self, fg_color=ARMY_BG, width=264, corner_radius=0)
        sb.pack(side="left", fill="y"); sb.pack_propagate(False)
        self._sb = sb
        
        # Saffron top band matches sidebar exactly
        ctk.CTkFrame(sb, fg_color=SAFFRON, corner_radius=0, height=5).pack(fill="x")

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
        lbl(uc, "AWWA LUNCH PROJECT..", size=12, weight="bold", color=WHITE).pack(padx=12, anchor="w")
        lbl(uc, "“ Sehat, Swad aur Samman ”", size=9, color="#7A9A7A").pack(padx=12, pady=(1,9), anchor="w")

        sep(sb).pack(fill="x", padx=16, pady=(0,6))


        lbl(sb, "  NAVIGATION", size=9, weight="bold", color="#4A6A4A").pack(anchor="w", padx=16, pady=(2,4))

        r = self._role
        nav = [("📊  Dashboard", "dashboard")]
        if r in ("admin","manager"):
            nav += [
                ("💰  Sales Entry",   "sales"),
                ("📦  Inventory",     "inventory"),
                ("💸  Expenditure",   "expenditure"),
                ("♻️  Waste",          "waste"),
            ]
        nav += [("📋  Daily Report", "report")]
        if r == "admin":
            nav += [
                ("🧾  Master Data",   "master"),
                ("👥  Users",         "users"),
                ("✏️  Edit Records",   "edit_datewise"),
                ("💾  Backup & Restore", "backup"),
            ]

        self._nav_btns = {}
        
        # Use a scrollable frame so the nav list doesn't push the bottom section off-screen
        nav_scroll = ctk.CTkScrollableFrame(sb, fg_color="transparent")
        nav_scroll.pack(fill="both", expand=True, padx=4)
        
        for txt, pg in nav:
            b = ctk.CTkButton(nav_scroll, text=txt, anchor="w", height=44,
                              font=ctk.CTkFont(size=12, weight="bold"),
                              fg_color="transparent", hover_color=ARMY_HVR,
                              text_color="#8AAA8A", corner_radius=8,
                              command=lambda p=pg: self._go(p))
            b.pack(padx=8, pady=2, fill="x")
            self._nav_btns[pg] = b

        # ── User Profile & Logout (Bottom) ────────────────────────────────────
        usr = ctk.CTkFrame(sb, fg_color="#162818", corner_radius=10)
        usr.pack(padx=12, side="bottom", fill="x", pady=(12,12))
        
        info_f = ctk.CTkFrame(usr, fg_color="transparent")
        info_f.pack(fill="x", padx=12, pady=(10, 4))
        lbl(info_f, f"👤  {self._user['name']}", size=11, weight="bold",
            color=WHITE).pack(anchor="w")
        lbl(info_f, f"Role: {', '.join(self._roles)}", size=9,
            color="#7A9A7A").pack(anchor="w", pady=(2,0))
            
        sep(usr, "#2A3F2C").pack(fill="x", padx=10, pady=4)
        
        ctk.CTkButton(usr, text="⬅  Logout", height=32, anchor="w",
                      fg_color="transparent", hover_color="#2A3F2C",
                      text_color=SAFFRON, font=ctk.CTkFont(size=11, weight="bold"),
                      corner_radius=6, command=self._show_login).pack(
                          padx=8, pady=(0,8), fill="x")

        right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        
        # White and Green top band for main area
        top_wg = ctk.CTkFrame(right, fg_color="transparent", height=5, corner_radius=0)
        top_wg.pack(fill="x"); top_wg.pack_propagate(False)
        ctk.CTkFrame(top_wg, fg_color=WHITE, corner_radius=0).pack(side="left", fill="both", expand=True)
        ctk.CTkFrame(top_wg, fg_color=IND_GREEN, corner_radius=0).pack(side="left", fill="both", expand=True)
        
        self._area = ctk.CTkFrame(right, fg_color=LIGHT, corner_radius=0)
        self._area.pack(fill="both", expand=True)

        self._go("dashboard")

    def _go(self, page):
        for p, b in self._nav_btns.items():
            b.configure(fg_color=SAFFRON if p == page else "transparent",
                        text_color=ARMY_BG if p == page else "#8AAA8A")
        for w in self._area.winfo_children(): w.destroy()
        # Clear inventory cache on page switch so re-entry always fetches fresh data
        if hasattr(self, "_inv_data_cache"):
            del self._inv_data_cache
        {
            "dashboard":      self._pg_dashboard,
            "sales":          self._pg_sales,
            "batch":          self._pg_batch,
            "inventory":      self._pg_inventory,
            "expenditure":    self._pg_expenditure,
            "waste":          self._pg_waste,
            "report":         self._pg_report,
            "master":         self._pg_master,
            "users":          self._pg_users,
            "import":         self._pg_import,
            "import_datewise":self._pg_import_datewise,
            "edit_datewise":  self._pg_edit_datewise,
            "backup":         self._pg_backup,
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

    def _confirm(self, title, message):
        """Show a Yes / No dialog; returns True if user clicks Yes."""
        result = [False]
        win = ctk.CTkToplevel(self)
        win.title(title); win.geometry("480x260")
        win.resizable(False, False); win.grab_set(); win.lift()
        win.configure(fg_color=WHITE)
        ts = ctk.CTkFrame(win, fg_color="transparent", height=5); ts.pack(fill="x"); ts.pack_propagate(False)
        for c in (SAFFRON, WHITE, IND_GREEN):
            ctk.CTkFrame(ts, fg_color=c).pack(side="left", fill="both", expand=True)
        lbl(win, "⚠️", size=36).pack(pady=(18,4))
        lbl(win, message, size=12, color=DARK, justify="center", wraplength=420).pack(pady=(0,16))
        bf = ctk.CTkFrame(win, fg_color="transparent"); bf.pack(fill="x", padx=40)
        def _yes():
            result[0] = True; win.destroy()
        btn(bf, "Yes, Delete", _yes, fg=RED, hv="#B91C1C", h=40, w=180).pack(side="left", padx=(0,8))
        btn(bf, "Cancel", win.destroy, fg=STRIPE, hv=BORDER, h=40, w=180, text_color=DARK).pack(side="left")
        win.wait_window()
        return result[0]

    # ── Live banner (auto-dismiss, no separate window) ─────────────────────
    def _toast(self, msg, duration_ms=2400, color=GREEN):
        """Show a brief success toast at the top-right of _area."""
        f = ctk.CTkFrame(self._area, fg_color=color, corner_radius=10,
                         border_width=0, height=42)
        f.place(relx=1.0, x=-16, rely=0.0, y=72, anchor="ne")
        ctk.CTkLabel(f, text=f"  ✅  {msg}  ",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=WHITE).pack(padx=12, pady=8)
        self.after(duration_ms, lambda: f.destroy() if f.winfo_exists() else None)

    # ── Refresh the current sidebar page (re-draw content completely) ──────
    def _live_refresh(self, page):
        """Destroy and rebuild the current page so totals update live."""
        for w in self._area.winfo_children(): w.destroy()
        {
            "dashboard":     self._pg_dashboard,
            "sales":         self._pg_sales,
            "batch":         self._pg_batch,
            "inventory":     self._pg_inventory,
            "expenditure":   self._pg_expenditure,
            "waste":         self._pg_waste,
            "report":        self._pg_report,
            "master":        self._pg_master,
            "users":         self._pg_users,
            "edit_datewise": self._pg_edit_datewise,
            "backup":        self._pg_backup,
        }.get(page, self._pg_dashboard)()

    # ── In-app modal overlay ────────────────────────────────────────────
    def _show_modal(self, title, width=520, height=460):
        """
        Render a modern in-app modal card over the content area.
        Returns (body_frame, close_fn).
        """
        # dark overlay
        overlay = tk.Frame(self._area, bg="#1E293B")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)

        # card
        card = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                            border_width=2, border_color=ARMY_BG,
                            width=width, height=height)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # header bar
        hbar = ctk.CTkFrame(card, fg_color=ARMY_BG, corner_radius=0, height=52)
        hbar.pack(fill="x"); hbar.pack_propagate(False)
        ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
        lbl(hbar, f"  {title}", size=13, weight="bold", color=WHITE).pack(side="left", padx=8)

        def close():
            overlay.destroy()

        ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                      fg_color="transparent", hover_color=ARMY_HVR,
                      text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                      command=close).pack(side="right", padx=8)

        # scrollable body
        body = ctk.CTkScrollableFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=18, pady=12)

        return body, card, close

    # ==============================================================================
    # DASHBOARD — with charts
    # ==============================================================================
    def _pg_dashboard(self):
        self._hdr("Dashboard",
                  f"\U0001F1EE\U0001F1F3  {datetime.now().strftime('%A, %d %B %Y')}  \u00b7  AWWA LUNCH PROJECT..")
        today = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")
        with get_db() as conn:
            sales = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
            inv   = conn.execute("SELECT * FROM inventory").fetchall()
            waste = conn.execute("SELECT * FROM waste_tracker WHERE date=?", (today,)).fetchall()
            samp  = conn.execute("SELECT * FROM samples WHERE date=?", (today,)).fetchall()
            exp   = conn.execute("SELECT SUM(amount) FROM expenditure WHERE date=?", (today,)).fetchone()[0] or 0
            # 7-day trend data
            week_data = conn.execute(
                "SELECT date, SUM(sp*sold) as rev, SUM(sold) as meals "
                "FROM sales WHERE date >= ? GROUP BY date ORDER BY date",
                ((datetime.now()-timedelta(days=6)).strftime("%Y-%m-%d"),)).fetchall()
            cat_data = conn.execute(
                "SELECT cat, SUM(stock) as total FROM inventory GROUP BY cat").fetchall()

        rev    = sum(r["sp"]*r["sold"] for r in sales)
        meals  = sum(r["sold"] for r in sales)
        wcost  = sum(w["cost_lost"] or 0 for w in waste)
        scost  = sum(s["cost"] or 0 for s in samp)
        sqty   = sum(s["qty"] for s in samp)
        low    = [i for i in inv if i["stock"] < i["min_lvl"]]
        # Profit = Revenue - Expenditure - WasteCost (samples cost already in Expenditure)
        profit = rev - exp - wcost

        # Main scrollable body for dashboard
        scroll = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # KPI cards ------------------------------------------------------------
        KPI = [
            ("\U0001f4b0", "Revenue",        f"\u20b9{rev:,.0f}",   SAFFRON, BG_SAF, T_SAF),
            ("\U0001f35b", "Meals Served",    str(meals),          GREEN,   BG_GRN, T_GRN),
            ("\U0001f4c8", "Net Profit",      f"\u20b9{profit:,.0f}", BLUE,    BG_BLU, T_BLU),
            ("\U0001f4b8", "Expenditure",     f"\u20b9{exp:,.0f}",    PURPLE,  BG_PUR, T_PUR),
            ("\u267b\ufe0f", "Waste Cost",    f"\u20b9{wcost:,.0f}",  ORANGE,  BG_SAF, T_SAF),
            ("\U0001f381", f"Samples ({sqty})", f"\u20b9{scost:,.0f}", TEAL,  BG_TEA, T_TEA),
            ("\u26a0\ufe0f", "Low Stock",     str(len(low)),       RED,     BG_RED, T_RED),
        ]
        # Two rows: 4 KPIs top row, 3 KPIs bottom row
        kr = ctk.CTkFrame(scroll, fg_color="transparent")
        kr.pack(fill="x", padx=PAD, pady=(14,0))
        top_kpis = KPI[:4]
        bot_kpis = KPI[4:]
        for i, (icon, title, val, color, bg, border) in enumerate(top_kpis):
            c = ctk.CTkFrame(kr, fg_color=WHITE, corner_radius=12, border_width=1, border_color=border)
            c.grid(row=0, column=i, padx=(0 if i==0 else 6), pady=(0,6), sticky="nsew")
            kr.grid_columnconfigure(i, weight=1)
            ctk.CTkFrame(c, fg_color=color, height=3, corner_radius=0).pack(fill="x")
            rf = ctk.CTkFrame(c, fg_color="transparent"); rf.pack(fill="x", padx=12, pady=10)
            ib = ctk.CTkFrame(rf, fg_color=bg, corner_radius=8, width=36, height=36)
            ib.pack(side="left"); ib.pack_propagate(False)
            lbl(ib, icon, size=16).place(relx=0.5, rely=0.5, anchor="center")
            vf = ctk.CTkFrame(rf, fg_color="transparent"); vf.pack(side="left", padx=(8,0))
            lbl(vf, val,   size=16, weight="bold", color=color).pack(anchor="w")
            lbl(vf, title, size=9,  color=MID).pack(anchor="w")
        for i, (icon, title, val, color, bg, border) in enumerate(bot_kpis):
            c = ctk.CTkFrame(kr, fg_color=WHITE, corner_radius=12, border_width=1, border_color=border)
            c.grid(row=1, column=i, padx=(0 if i==0 else 6), sticky="nsew")
            ctk.CTkFrame(c, fg_color=color, height=3, corner_radius=0).pack(fill="x")
            rf = ctk.CTkFrame(c, fg_color="transparent"); rf.pack(fill="x", padx=12, pady=10)
            ib = ctk.CTkFrame(rf, fg_color=bg, corner_radius=8, width=36, height=36)
            ib.pack(side="left"); ib.pack_propagate(False)
            lbl(ib, icon, size=16).place(relx=0.5, rely=0.5, anchor="center")
            vf = ctk.CTkFrame(rf, fg_color="transparent"); vf.pack(side="left", padx=(8,0))
            lbl(vf, val,   size=16, weight="bold", color=color).pack(anchor="w")
            lbl(vf, title, size=9,  color=MID).pack(anchor="w")

        # ── Charts row ────────────────────────────────────────────────────────
        if CHART_OK:
            chart_row = ctk.CTkFrame(scroll, fg_color="transparent")
            chart_row.pack(fill="x", padx=PAD, pady=(12,0))
            chart_row.grid_columnconfigure(0, weight=3)
            chart_row.grid_columnconfigure(1, weight=2)

            # Revenue trend line chart
            cf1 = ctk.CTkFrame(chart_row, fg_color=WHITE, corner_radius=12,
                               border_width=1, border_color=BORDER)
            cf1.grid(row=0, column=0, padx=(0,8), sticky="nsew")
            lbl(cf1, "  \U0001f4c8  7-Day Revenue Trend", size=11, weight="bold",
                color=ARMY_BG).pack(anchor="w", padx=12, pady=(10,0))

            fig1 = Figure(figsize=(5, 2.2), dpi=100, facecolor="#FFFFFF")
            ax1 = fig1.add_subplot(111)
            if week_data:
                dates = [r["date"][-5:] for r in week_data]  # MM-DD
                revs  = [r["rev"] for r in week_data]
                ax1.fill_between(range(len(dates)), revs, alpha=0.15, color="#138808")
                ax1.plot(range(len(dates)), revs, color="#138808", linewidth=2.5, marker="o",
                         markersize=5, markerfacecolor="#FF9933")
                ax1.set_xticks(range(len(dates))); ax1.set_xticklabels(dates, fontsize=7)
                ax1.set_ylabel("\u20b9", fontsize=8)
                for i2, v in enumerate(revs):
                    ax1.annotate(f"\u20b9{v:,.0f}", (i2, v), textcoords="offset points",
                                 xytext=(0,8), ha="center", fontsize=6, color="#138808")
            else:
                ax1.text(0.5, 0.5, "No sales data yet", ha="center", va="center",
                         fontsize=10, color="#94A3B8", transform=ax1.transAxes)
            ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
            ax1.tick_params(labelsize=7)
            fig1.tight_layout(pad=1.5)
            canvas1 = FigureCanvasTkAgg(fig1, master=cf1)
            canvas1.draw(); canvas1.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(4,8))

            # Stock category donut
            cf2 = ctk.CTkFrame(chart_row, fg_color=WHITE, corner_radius=12,
                               border_width=1, border_color=BORDER)
            cf2.grid(row=0, column=1, sticky="nsew")
            lbl(cf2, "  \U0001f4e6  Stock by Category", size=11, weight="bold",
                color=ARMY_BG).pack(anchor="w", padx=12, pady=(10,0))

            fig2 = Figure(figsize=(2.8, 2.2), dpi=100, facecolor="#FFFFFF")
            ax2 = fig2.add_subplot(111)
            if cat_data:
                cats = [r["cat"] for r in cat_data if r["total"] > 0]
                vals = [r["total"] for r in cat_data if r["total"] > 0]
                
                if sum(vals) > 0:
                    colors_pie = ["#FF9933","#138808","#3B82F6","#8B5CF6","#F59E0B","#EF4444"]
                    wedges, texts, autotexts = ax2.pie(
                        vals, labels=cats, autopct="%1.0f%%", startangle=90,
                        colors=colors_pie[:len(cats)], pctdistance=0.75,
                        textprops={"fontsize": 7})
                    for at in autotexts: at.set_fontsize(6); at.set_color("white")
                    centre = plt.Circle((0,0), 0.55, fc="white"); ax2.add_artist(centre)
                else:
                    ax2.text(0.5, 0.5, "No positive stock", ha="center", va="center",
                             fontsize=10, color="#94A3B8", transform=ax2.transAxes)
            else:
                ax2.text(0.5, 0.5, "No stock", ha="center", va="center",
                         fontsize=10, color="#94A3B8", transform=ax2.transAxes)
            fig2.tight_layout(pad=0.5)
            canvas2 = FigureCanvasTkAgg(fig2, master=cf2)
            canvas2.draw(); canvas2.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=(0,8))
        else:
            fb = ctk.CTkFrame(scroll, fg_color=WHITE, corner_radius=12,
                              border_width=1, border_color=BORDER, height=180)
            fb.pack(fill="x", padx=PAD, pady=(12,0))
            lbl(fb, "Charts unavailable (matplotlib missing)", size=12, color=MID).pack(expand=True)

        # ── Bottom: Sales table + Alerts ──────────────────────────────────────
        bot = ctk.CTkFrame(scroll, fg_color="transparent", height=350)
        bot.pack(fill="x", padx=PAD, pady=(10,PAD))
        bot.pack_propagate(False)
        bot.grid_columnconfigure(0, weight=6)
        bot.grid_columnconfigure(1, weight=4)
        bot.grid_rowconfigure(0, weight=1)

        # Sales table
        sc = card(bot)
        sc.grid(row=0, column=0, padx=(0,8), sticky="nsew")
        band(sc, "📊  Today’s Sales")
        COLS = [("Meal",3),("Sold",1),("Revenue",2),("Payment",1)]
        thead(sc, COLS)
        sf = ctk.CTkScrollableFrame(sc, fg_color="transparent")
        sf.pack(fill="both", expand=True)
        for ix, r in enumerate(sales):
            pi = {"Cash":"💵","UPI":"📱","Card":"💳"}.get(r["payment"],"💰")
            trow(sf,[r["meal"],str(r["sold"]),
                     f"₹{r['sp']*r['sold']:,.0f}",f"{pi} {r['payment']}"],
                  [3,1,2,1],
                  colors=[DARK,MID,GREEN,MID],bolds=[True,False,True,False],
                  bg=WHITE if ix%2==0 else STRIPE)
        totf = ctk.CTkFrame(sc, fg_color=BG_SAF, corner_radius=0, height=34)
        totf.pack(fill="x"); totf.pack_propagate(False)
        lbl(totf, f"  TOTAL: {meals} meals  •  ₹{rev:,.0f}", size=11,
            weight="bold", color=SAFFRON).pack(side="left", padx=10)

        # Alerts
        ac = card(bot)
        ac.grid(row=0, column=1, sticky="nsew")
        
        ahdr = ctk.CTkFrame(ac, fg_color=DRED if low else IND_GREEN,
                            corner_radius=0, height=44)
        ahdr.pack(fill="x"); ahdr.pack_propagate(False)
        ctk.CTkFrame(ahdr, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
        lbl(ahdr, f"  ⚠️  Low Stock  ({len(low)} item{'s' if len(low) != 1 else ''})",
            size=12, weight="bold", color=WHITE).pack(side="left", padx=8)

        # Symmetrical spacer to match thethead in Sales table
        sub_hdr = ctk.CTkFrame(ac, fg_color=WHITE, height=36)
        sub_hdr.pack(fill="x")
        sub_hdr.pack_propagate(False)
        lbl(sub_hdr, "Items requiring replenishment", size=10, color=MID).pack(side="left", padx=14, pady=8)

        asc = ctk.CTkScrollableFrame(ac, fg_color="transparent")
        asc.pack(fill="both", expand=True)

        if not low:
            ok = ctk.CTkFrame(asc, fg_color=BG_GRN, corner_radius=10,
                               border_width=1, border_color=T_GRN)
            ok.pack(fill="x", pady=4, padx=8)
            lbl(ok, "✅  All items well stocked",
                size=12, weight="bold", color=GREEN).pack(pady=16, padx=12)
        else:
            for item in low:
                pct  = (item["stock"] / item["min_lvl"] * 100) if item["min_lvl"] else 0
                scol = "#991B1B" if pct < 30 else "#9A3412"
                sbg  = BG_RED   if pct < 30 else "#FFF7ED"
                sbd  = T_RED    if pct < 30 else T_SAF
                box = ctk.CTkFrame(asc, fg_color=sbg, corner_radius=10,
                                   border_width=1, border_color=sbd)
                box.pack(fill="x", pady=(0, 6), padx=8)
                tr = ctk.CTkFrame(box, fg_color="transparent")
                tr.pack(fill="x", padx=10, pady=(8, 1))
                lbl(tr, f"⚠  {item['item']}", size=12, weight="bold", color=scol).pack(side="left")
                lbl(tr, item["cat"], size=9, color=MID).pack(side="right")
                br = ctk.CTkFrame(box, fg_color="transparent")
                br.pack(fill="x", padx=10, pady=(0, 4))
                lbl(br, f"Stock: {item['stock']:.1f} {item['unit']}",
                    size=10, weight="bold", color=RED).pack(side="left")
                lbl(br, f"Min: {item['min_lvl']:.1f} {item['unit']}",
                    size=10, color=MID).pack(side="right")
                pb = ctk.CTkFrame(box, fg_color="#E5E7EB", corner_radius=4, height=5)
                pb.pack(fill="x", padx=10, pady=(0, 8)); pb.pack_propagate(False)
                fill = min(max(pct / 100, 0.02), 1.0)
                ctk.CTkFrame(pb, fg_color=RED if pct < 50 else ORANGE,
                             corner_radius=4, height=5
                             ).place(relx=0, rely=0, relwidth=fill, relheight=1)

        # Symmetrical footer to match the Sales table footer
        totf2 = ctk.CTkFrame(ac, fg_color=BG_RED if low else BG_GRN, corner_radius=0, height=34)
        totf2.pack(fill="x"); totf2.pack_propagate(False)
        lbl(totf2, f"  STATUS: {len(low)} items low" if low else "  STATUS: All stocked", size=11,
            weight="bold", color=RED if low else GREEN).pack(side="left", padx=10)

    # -- Core stock deduction engine (single source of truth) ------------------
    # ==============================================================================
    # BATCH PREP — modern card layout
    # ==============================================================================
    # SALES ENTRY
    # ==============================================================================
    def _pg_sales(self):
        today      = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")

        hf = self._hdr("🍽️  Sales Entry", f"📅  {today_disp}")
        btn(hf, "📄  Export PDF", lambda: self._export_pdf_report(today, today),
            fg=ARMY_BG, hv=ARMY_HVR, h=32).pack(side="right", padx=PAD)
        btn(hf, "📅  Past Entry", lambda: self._dlg_backdated_entry("sales"),
            fg=SAFFRON, hv="#D97706", h=32).pack(side="right")

        with get_db() as conn:
            meals       = conn.execute("SELECT id,name,sp FROM menu WHERE active=1 ORDER BY name").fetchall()
            today_sales = conn.execute("SELECT * FROM sales WHERE date=? ORDER BY id", (today,)).fetchall()

        # Aggregate totals per menu item (multiple records = multiple transactions)
        today_totals = {}
        for r in today_sales:
            mid = r["menu_id"]
            if mid not in today_totals:
                today_totals[mid] = {"sold": 0, "revenue": 0.0, "entries": 0}
            today_totals[mid]["sold"]    += r["sold"]
            today_totals[mid]["revenue"] += r["sp"] * r["sold"]
            today_totals[mid]["entries"] += 1

        tot_rev  = sum(r["sp"]*r["sold"] for r in today_sales)
        tot_sold = sum(r["sold"] for r in today_sales)

        # ── Summary strip ──────────────────────────────────────────────────────
        sf = ctk.CTkFrame(self._area, fg_color=ARMY_BG, corner_radius=0, height=56)
        sf.pack(fill="x", padx=PAD, pady=(10,0)); sf.pack_propagate(False)
        for icon, label, val, clr in [
            ("🍽", "Total Sold",   f"{tot_sold}",           SAFFRON),
            ("💰", "Revenue",      f"₹{tot_rev:,.0f}",       "#4ADE80"),
            ("📊", "Transactions", f"{len(today_sales)}", WHITE),
        ]:
            cf = ctk.CTkFrame(sf, fg_color="transparent"); cf.pack(side="left", padx=24, expand=True)
            lbl(cf, f"{icon}  {label}", size=10, color="#94A3B8").pack(anchor="w")
            lbl(cf, val, size=18, weight="bold", color=clr).pack(anchor="w")

        # ── Search bar ────────────────────────────────────────────────────────
        search_bar = ctk.CTkFrame(self._area, fg_color="transparent")
        search_bar.pack(fill="x", padx=PAD, pady=(8,0))
        self._sale_search = ctk.CTkEntry(search_bar,
                                         placeholder_text="🔍  Search meals...",
                                         height=34, corner_radius=10)
        self._sale_search.pack(fill="x")
        self._sale_search.bind("<KeyRelease>", lambda e: self._debounce("_sale_search_job", self._filter_sale_cards))

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(8, PAD))

        self._sq = {}
        self._sale_cards = []
        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        self._sale_grid = grid
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        for ix, meal in enumerate(meals):
            mid2, name2, sp2 = meal["id"], meal["name"], meal["sp"]
            agg       = today_totals.get(mid2)
            has_sales = agg is not None
            is_thali  = any(x in name2 for x in ["Thali","Biryani","Rice"])

            mc = ctk.CTkFrame(grid, fg_color=WHITE, corner_radius=14,
                              border_width=2,
                              border_color=T_GRN if has_sales else BORDER)
            mc.grid(row=ix//3, column=ix%3, padx=6, pady=6, sticky="nsew")

            # Top badge
            top = ctk.CTkFrame(mc, fg_color=ARMY_BG if is_thali else TEAL,
                               corner_radius=0, height=36)
            top.pack(fill="x"); top.pack_propagate(False)
            lbl(top, f"  {'🍛' if is_thali else '🍽️'}  {name2}",
                size=11, weight="bold", color=WHITE).pack(side="left", padx=8)
            lbl(top, f"₹{sp2:.0f}", size=12, weight="bold",
                color=SAFFRON).pack(side="right", padx=12)

            # Today's running total badge
            if has_sales:
                si = ctk.CTkFrame(mc, fg_color=BG_GRN, corner_radius=0, height=22)
                si.pack(fill="x"); si.pack_propagate(False)
                entries_txt = f"{agg['entries']} batch" if agg['entries'] == 1 else f"{agg['entries']} batches"
                lbl(si,
                    f"  ✅  Today: {agg['sold']} sold • {entries_txt} • ₹{agg['revenue']:,.0f}",
                    size=9, weight="bold", color=GREEN).pack(side="left", padx=6)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="x", padx=12, pady=10)

            # Entry always starts blank (new transaction each time)
            lbl(body, "Add New Sale Qty", size=10, color=MID).pack(anchor="w")
            e_qty = ctk.CTkEntry(body, height=40, corner_radius=10,
                                 placeholder_text="0",
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 border_color=BORDER, justify="center")
            e_qty.pack(fill="x", pady=(4,8))

            rev_lbl = lbl(body, "Revenue: ₹0", size=11, weight="bold", color=GREEN)
            rev_lbl.pack(anchor="w")

            def _upd(event=None, eq=e_qty, rl=rev_lbl, sp=sp2):
                try:    rl.configure(text=f"Revenue: ₹{int(eq.get() or 0)*sp:,.0f}")
                except: rl.configure(text="Revenue: ₹0")
            e_qty.bind("<KeyRelease>", _upd)

            pm = ctk.CTkOptionMenu(body, values=["Cash","UPI","Card"],
                                   width=120, height=30,
                                   font=ctk.CTkFont(size=11))
            pm.set("Cash")
            pm.pack(fill="x", pady=(8,4))

            def _save(m_id=mid2, m_name=name2, m_sp=sp2, eq=e_qty, epm=pm):
                self._save_one_sale(m_id, m_name, m_sp, eq, epm)

            # Button always says "Add Sale" — never replaces existing records
            ctk.CTkButton(mc, text="➕  Add Sale",
                          height=36, corner_radius=10,
                          fg_color=GREEN, hover_color=DGREEN,
                          font=ctk.CTkFont(size=12, weight="bold"),
                          command=_save).pack(fill="x", padx=12, pady=(0,12))

            self._sq[mid2] = (name2, sp2, e_qty, pm)
            self._sale_cards.append((name2.lower(), mc))

        # ── Save All bar ───────────────────────────────────────────────────────
        bar = ctk.CTkFrame(wrap, fg_color="transparent")
        bar.pack(fill="x", pady=(14,4))
        btn(bar, "💾  Save All Items at Once", self._save_all_sales,
            fg=ARMY_BG, hv=ARMY_HVR, h=48).pack(fill="x")

        # ── Today's sales log ─────────────────────────────────────────────────
        if today_sales:
            sc = card(wrap); sc.pack(fill="x", pady=(14,0))
            band(sc, f"📊  Today's Sales Log  •  {today_disp}")
            COLS2 = [("Meal",4),("Sold",1),("COGS",1),("Revenue",1),("Payment",1),("Ingredients Deducted",3)]
            thead(sc, COLS2, bg=STRIPE, tc=MID)
            tot_cogs = 0
            with get_db() as conn:
                for ix, r in enumerate(today_sales):
                    rev2 = r["sp"]*r["sold"]; tot_cogs += r["cogs"]
                    ledger_rows = conn.execute(
                        "SELECT sl.qty_change, i.item, i.unit "
                        "FROM stock_ledger sl JOIN inventory i ON i.id=sl.inv_id "
                        "WHERE sl.notes LIKE ? AND sl.date=?",
                        (f"Sale:{r['id']}%", r["date"])).fetchall()
                    if ledger_rows:
                        parts = [f"{lr['item']} {-lr['qty_change']:.2f}{lr['unit']}"
                                 for lr in ledger_rows[:2]]
                        if len(ledger_rows) > 2:
                            parts.append(f"+{len(ledger_rows)-2} more")
                        deduct_cell = ", ".join(parts)
                    else:
                        deduct_cell = "⚠ No recipe"
                    trow(sc,[r["meal"],str(r["sold"]),
                             f"₹{r['cogs']:,.0f}",f"₹{rev2:,.0f}",r["payment"],deduct_cell],
                         [4,1,1,1,1,3], bg=WHITE if ix%2==0 else STRIPE)
            totf = ctk.CTkFrame(sc, fg_color=BG_GRN, corner_radius=0, height=38)
            totf.pack(fill="x"); totf.pack_propagate(False)
            lbl(totf, "  TOTAL", size=11, weight="bold", color=GREEN).grid(
                row=0, column=0, padx=14, sticky="w")
            lbl(totf, f"₹{tot_cogs:,.0f}", size=11, weight="bold",
                color=GREEN).grid(row=0, column=2, sticky="w", padx=14)
            lbl(totf, f"₹{tot_rev:,.0f}", size=13, weight="bold",
                color=GREEN).grid(row=0, column=3, sticky="w", padx=14)
            for i,w in enumerate([4,1,1,1,1,3]):
                totf.grid_columnconfigure(i, weight=w)

    def _filter_sale_cards(self):
        q = self._sale_search.get().lower().strip()
        for name, card in self._sale_cards:
            if q in name:
                card.grid()
            else:
                card.grid_remove()

    def _apply_stock_deduction(self, conn, menu_id, qty_sold, sale_id, today):
        """Calculate COGS per portion sold.
        
        NOTE: Inventory stock is NOT deducted here.
        Ingredients are already fully deducted when the menu/batch is created.
        This function only computes the cost-of-goods-sold (COGS) for profit
        tracking and logs the sale event to the stock_ledger for audit purposes.
        """
        recipes = conn.execute(
            "SELECT r.inv_id, r.qty_per_unit "
            "FROM recipes r WHERE r.menu_id=?", (menu_id,)).fetchall()
        cpu        = 0.0
        deductions = []
        for rc in recipes:
            inv = conn.execute(
                "SELECT id, item, unit, cp, stock FROM inventory WHERE id=?",
                (rc["inv_id"],)).fetchone()
            if not inv:
                continue
            inv_id       = inv["id"]
            item_name    = inv["item"]
            unit         = inv["unit"]
            qty_per_unit = rc["qty_per_unit"]
            total_used   = qty_per_unit * qty_sold
            cpu         += qty_per_unit * (inv["cp"] or 0)

            # Audit-only log — stock NOT deducted again here.
            # Ingredients were already deducted at menu/batch creation.
            conn.execute(
                "INSERT INTO stock_ledger "
                "(date, inv_id, transaction_type, qty_change, notes) "
                "VALUES (?, ?, 'Sale_COGS', 0, ?)",
                (today, inv_id,
                 f"Sale:{sale_id} | {item_name} "
                 f"({qty_per_unit:.4f} {unit}/portion x {qty_sold} portions | "
                 f"COGS only — stock deducted at batch creation)"))

            deductions.append({
                "item":           item_name,
                "unit":           unit,
                "qty_per_unit":   qty_per_unit,
                "total_deducted": total_used,
                "stock_before":   inv["stock"],
                "stock_after":    inv["stock"],  # unchanged
            })
        return cpu, deductions, []

    def _save_one_sale(self, menu_id, meal, sp, eq, epm):
        """Always creates a NEW sale record. Never edits existing."""
        try:
            sold = int(eq.get() or 0)
        except:
            self._popup("⚠️ Invalid Entry", "Please enter a whole number for quantity sold.")
            return
        if sold <= 0:
            self._popup("⚠️ No Quantity", "Enter a quantity greater than 0.")
            return

        today   = datetime.now().strftime("%Y-%m-%d")
        payment = epm.get()

        with get_db() as conn:
            # Always INSERT a brand-new sale record
            cur = conn.execute(
                "INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) "
                "VALUES (?,?,?,?,?,0,0.0,?)",
                (today, menu_id, meal, sp, sold, payment))
            new_sale_id = cur.lastrowid

            # Deduct stock for this qty
            cpu, deductions, warnings = self._apply_stock_deduction(
                conn, menu_id, sold, new_sale_id, today)

            # Update COGS
            conn.execute(
                "UPDATE sales SET cogs=? WHERE id=?",
                (sold * cpu, new_sale_id))

        if warnings:
            self._popup("⚠️ Low Stock", "\n".join(warnings[:5]))

        if deductions:
            parts = [f"{d['item']}: -{d['total_deducted']:.2f}{d['unit']}"
                     for d in deductions[:3]]
            if len(deductions) > 3:
                parts.append(f"+{len(deductions)-3} more")
            deduct_str = " | Deducted: " + ", ".join(parts)
        else:
            deduct_str = " | ⚠ No recipe linked — stock NOT deducted"

        self._toast(
            f"{meal} — {sold} sold • ₹{sp*sold:,.0f} • COGS ₹{sold*cpu:,.0f}"
            f"{deduct_str}",
            duration_ms=4000)
        self._live_refresh("sales")

    def _save_all_sales(self):
        """Saves each item with qty>0 as a brand-new sale record. Never edits existing."""
        today         = datetime.now().strftime("%Y-%m-%d")
        saved         = 0
        all_warnings  = []
        total_deducts = 0

        with get_db() as conn:
            for mid2, (name2, sp2, eq, pm) in self._sq.items():
                try:
                    sold = int(eq.get() or 0)
                except:
                    continue
                if sold <= 0:
                    continue
                payment = pm.get()

                # Always INSERT a new record — never update existing ones
                cur = conn.execute(
                    "INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) "
                    "VALUES (?,?,?,?,?,0,0.0,?)",
                    (today, mid2, name2, sp2, sold, payment))
                new_sale_id = cur.lastrowid

                # Deduct stock for this qty
                cpu, deductions, warnings = self._apply_stock_deduction(
                    conn, mid2, sold, new_sale_id, today)

                # Update COGS
                conn.execute(
                    "UPDATE sales SET cogs=? WHERE id=?",
                    (sold * cpu, new_sale_id))

                all_warnings.extend(warnings)
                total_deducts += len(deductions)
                saved += 1

        if saved == 0:
            self._popup("⚠️ Nothing Saved", "Enter at least one quantity > 0.")
            return

        if all_warnings:
            warn_body = f"{saved} sale(s) saved.\n\nLow-stock warnings:\n" + "\n".join(all_warnings[:8])
            if len(all_warnings) > 8:
                warn_body += f"\n... and {len(all_warnings)-8} more"
            self._popup("⚠️ Stock Warnings", warn_body)

        self._toast(
            f"✅ {saved} new transaction(s) added — "
            f"{total_deducts} ingredient deductions recorded",
            duration_ms=3500)
        self._live_refresh("sales")

    # ==============================================================================
    def _pg_batch(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")
        hf = self._hdr("🧑‍🍳  Batch Preparation", f"📅  {today_disp}")
        btn(hf, "📅  Past Entry", lambda: self._dlg_backdated_entry("batch"),
            fg=SAFFRON, hv="#D97706", h=32).pack(side="right", padx=PAD)

        with get_db() as conn:
            meals = conn.execute("SELECT id,name,sp FROM menu WHERE active=1 ORDER BY name").fetchall()
            batches_today = conn.execute(
                "SELECT bp.menu_id, SUM(bp.qty_prepared) as total, m.name "
                "FROM batch_prep bp JOIN menu m ON m.id=bp.menu_id "
                "WHERE bp.date=? GROUP BY bp.menu_id", (today,)).fetchall()
            all_recipes = conn.execute(
                "SELECT r.menu_id, i.item, r.qty_per_unit, i.unit "
                "FROM recipes r JOIN inventory i ON i.id=r.inv_id").fetchall()

        batch_map = {b["menu_id"]: b["total"] for b in batches_today}
        recipe_map = {}
        for r in all_recipes:
            recipe_map.setdefault(r["menu_id"], []).append(
                f"{r['item']} ({r['qty_per_unit']:.2f} {r['unit']})")
        tot_prepared = sum(b["total"] for b in batches_today)

        # ── Summary strip ─────────────────────────────────────────────────────
        sf = ctk.CTkFrame(self._area, fg_color=ARMY_BG, corner_radius=0, height=56)
        sf.pack(fill="x", padx=PAD, pady=(10,0)); sf.pack_propagate(False)
        for icon, label, val, clr in [
            ("🧑‍🍳", "Meals Today", f"{len(batches_today)}", SAFFRON),
            ("📦", "Total Prepared", f"{tot_prepared} units", "#4ADE80"),
            ("📋", "Active Items", f"{len(meals)}", WHITE),
        ]:
            cf = ctk.CTkFrame(sf, fg_color="transparent"); cf.pack(side="left", padx=24, expand=True)
            lbl(cf, f"{icon}  {label}", size=10, color="#94A3B8").pack(anchor="w")
            lbl(cf, val, size=18, weight="bold", color=clr).pack(anchor="w")

        # ── Controls ──────────────────────────────────────────────────────────
        ctrl = ctk.CTkFrame(self._area, fg_color="transparent")
        ctrl.pack(fill="x", padx=PAD, pady=(10,0))
        self._batch_deduct = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(ctrl, text="Auto-deduct stock on save",
                        variable=self._batch_deduct, text_color=ARMY_BG,
                        font=ctk.CTkFont(size=11, weight="bold"),
                        checkbox_width=20, checkbox_height=20
                       ).pack(side="left")

        # ── Search + Cards grid ────────────────────────────────────────────────
        search_bar = ctk.CTkFrame(self._area, fg_color="transparent")
        search_bar.pack(fill="x", padx=PAD, pady=(8,0))
        self._batch_search = ctk.CTkEntry(search_bar, placeholder_text="\U0001f50d  Search meals...",
                                          height=34, corner_radius=10)
        self._batch_search.pack(fill="x")
        self._batch_search.bind("<KeyRelease>", lambda e: self._debounce("_batch_search_job", self._filter_batch_cards))

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(8,PAD))

        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        self._batch_grid = grid
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        self._be = {}
        self._batch_cards = []
        for ix, meal in enumerate(meals):
            mid2, nm = meal["id"], meal["name"]
            already = batch_map.get(mid2, 0)
            has_recipe = mid2 in recipe_map
            is_thali = any(x in nm for x in ["Thali","Biryani","Rice"])

            mc = ctk.CTkFrame(grid, fg_color=WHITE, corner_radius=14,
                              border_width=2,
                              border_color=T_GRN if already else BORDER)
            mc.grid(row=ix//3, column=ix%3, padx=6, pady=6, sticky="nsew")

            # Top badge
            top = ctk.CTkFrame(mc, fg_color=ARMY_BG if is_thali else TEAL,
                               corner_radius=0, height=34)
            top.pack(fill="x"); top.pack_propagate(False)
            lbl(top, f"  {'🍛' if is_thali else '🍽'}  {nm}",
                size=11, weight="bold", color=WHITE).pack(side="left", padx=6)

            # Already prepared
            if already:
                si = ctk.CTkFrame(mc, fg_color=BG_GRN, corner_radius=0, height=22)
                si.pack(fill="x"); si.pack_propagate(False)
                lbl(si, f"  ✅  Already prepared: {already} units",
                    size=9, weight="bold", color=GREEN).pack(side="left", padx=6)

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

            # Qty input
            lbl(body, "Qty to Prepare", size=10, color=MID).pack(anchor="w")
            e = ctk.CTkEntry(body, height=40, corner_radius=10,
                             placeholder_text="0",
                             font=ctk.CTkFont(size=16, weight="bold"),
                             border_color=BORDER, justify="center")
            e.pack(fill="x", pady=(4,4))
            self._be[mid2] = e
            self._batch_cards.append((nm.lower(), mc))

        # ── Save bar ──────────────────────────────────────────────────────────
        bar = ctk.CTkFrame(wrap, fg_color="transparent")
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
        saved = 0; deduct_log = []
        with get_db() as conn:
            for mid2, e in self._be.items():
                try:    qty = int(e.get() or 0)
                except: self._popup("⚠️ Invalid", "Whole numbers only."); return
                if qty <= 0: continue

                conn.execute(
                    "INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                    (today, mid2, qty))

                if getattr(self, "_batch_deduct", None) and self._batch_deduct.get():
                    for rc in conn.execute(
                        "SELECT r.inv_id, r.qty_per_unit, i.item, i.unit "
                        "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
                        "WHERE r.menu_id=?", (mid2,)):
                        deduct = rc["qty_per_unit"] * qty
                        conn.execute(
                            "UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id=?",
                            (deduct, rc["inv_id"]))
                        deduct_log.append(f"{rc['item']} -{deduct:.2f}{rc['unit']}")
                saved += 1

        if saved == 0:
            self._popup("⚠️ Nothing saved", "Enter at least one qty > 0."); return
        summary = f"✅ {saved} batch(es) saved"
        if deduct_log:
            summary += "  |  Stock deducted: " + ", ".join(deduct_log[:4])
            if len(deduct_log) > 4: summary += f" +{len(deduct_log)-4} more"
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

        # Action bar
        ab = ctk.CTkFrame(self._area, fg_color="transparent")
        ab.pack(fill="x", padx=PAD, pady=(8,0))
        btn(ab, "＋  Add New Item",    self._dlg_inv_add,    fg=GREEN,   hv=DGREEN, h=36).pack(side="left")
        btn(ab, "📥  Receive Stock",   self._dlg_inv_receive, fg=TEAL,    hv=ARMY_BG, h=36).pack(side="left", padx=8)
        btn(ab, "✏️  Edit Item",        self._dlg_inv_edit,   fg=BLUE,    hv=DBLUE,   h=36).pack(side="left")
        btn(ab, "🗑  Delete Item",      self._dlg_inv_del,    fg=RED,     hv=DRED,    h=36).pack(side="left", padx=8)
        btn(ab, "📅  Past Stock",       lambda: self._dlg_backdated_entry("stock"),
            fg=SAFFRON, hv="#D97706", h=36).pack(side="left")

        # Table — fixed-width columns so header & rows align
        tc = card(self._area)
        tc.pack(fill="both", expand=True, padx=PAD, pady=(10,PAD))

        # Header row (widths MUST match cell widths in _inv_loadrows)
        hdr = ctk.CTkFrame(tc, fg_color=ARMY_BG, corner_radius=0, height=36)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        INV_HDR = [("Item", 195), ("Category", 100), ("Unit", 60),
                   ("Opening", 80), ("Received", 85), ("Stock", 80),
                   ("Min Lvl", 75), ("Status", 75)]
        for col, w in INV_HDR:
            cf = ctk.CTkFrame(hdr, fg_color="transparent", width=w)
            cf.pack(side="left", fill="y"); cf.pack_propagate(False)
            lbl(cf, col, size=10, weight="bold", color=GOLD_LT).pack(anchor="w", padx=10, pady=8)

        self._inv_sf = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_sf.pack(fill="both", expand=True)
        self._inv_hdr = INV_HDR
        self._inv_loadrows()

    def _inv_setcat(self, cat):
        self._inv_filter = cat
        for c, b in self._inv_fb.items():
            b.configure(fg_color=ARMY_BG if c==cat else STRIPE,
                        text_color=WHITE if c==cat else DARK)
        # Reload from DB then re-render with current search query
        q = self._inv_search.get().strip().lower() if hasattr(self, "_inv_search") else ""
        self._inv_loadrows(search_q=q, reload_db=True)

    def _inv_loadrows(self, search_q="", reload_db=False):
        """Load inventory rows with debounced search and threaded DB fetch.
        
        - reload_db=True  → fetch fresh data from DB in a background thread
        - reload_db=False → filter the in-memory cache only (instant, no DB hit)
        """
        # If we have a fresh cache and no DB reload needed, filter in-memory immediately
        if not reload_db and hasattr(self, "_inv_data_cache"):
            self._inv_render_rows(self._inv_data_cache, search_q)
            return

        # Otherwise fetch from DB in a background thread
        cat_filter = self._inv_filter

        def _fetch():
            with get_db() as conn:
                if cat_filter == "All":
                    data = conn.execute(
                        "SELECT * FROM inventory ORDER BY cat, item").fetchall()
                else:
                    data = conn.execute(
                        "SELECT * FROM inventory WHERE cat=? ORDER BY item",
                        (cat_filter,)).fetchall()
            # Convert to plain dicts so we can use them off the Row object
            data = [dict(d) for d in data]
            # Schedule render back on main thread
            if self.winfo_exists():
                self.after(0, lambda: self._inv_on_data_ready(data, search_q))

        threading.Thread(target=_fetch, daemon=True).start()

    def _inv_on_data_ready(self, data, search_q):
        """Called on the main thread after DB fetch completes."""
        self._inv_data_cache = data          # store for in-memory searches
        self._inv_render_rows(data, search_q)

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

        ci = {"Dry":"🌾","Fresh":"🥦","Dairy":"🥛","Bakery":"🥐","Prepared":"🍲"}
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

        # ── Category ─────────────────────────────────────────────────────────
        lbl(body, "Category", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(8, 3))
        cat_menu = ctk.CTkOptionMenu(body, values=CATEGORIES, font=ctk.CTkFont(size=12), height=36)
        cat_menu.set("Dry"); cat_menu.pack(fill="x")

        # ── Unit ──────────────────────────────────────────────────────────────
        lbl(body, "Unit  (kg / ltr / pcs / gm)", size=11, weight="bold",
            color=ARMY_BG).pack(anchor="w", pady=(8, 3))
        e_unit = entry(body, ph="e.g., kg", h=38); e_unit.pack(fill="x")
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
                cat  = cat_menu.get()
            except ValueError:
                self._popup("⚠️ Invalid", "Enter numeric values for stock/min/cost."); return
            if not nm or not unit:
                self._popup("⚠️ Missing", "Item name and unit are required."); return
            with get_db() as conn:
                try:
                    conn.execute(
                        "INSERT INTO inventory (item,cat,unit,stock,min_lvl,opening,cp) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (nm, cat, unit, stk, mn, stk, cp))
                except sqlite3.IntegrityError:
                    self._popup("⚠️ Duplicate", f"'{nm}' already exists."); return
            self._popup("✅ Added!", f"{nm} ({cat}) added to inventory.")
            close(); self._go("inventory")

        btn(card, "✅  Add Item", save, fg=GREEN, hv=DGREEN, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")


    def _dlg_inv_receive(self):
        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        body, card, close = self._show_modal("📥  Receive / Add Stock", 520, 380)

        lbl(body, "Select Item (Searchable)", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        se = ctk.CTkEntry(body, placeholder_text="🔍 Type to search...", height=32); se.pack(fill="x", pady=(0,4))
        iom = ctk.CTkOptionMenu(body, values=items or ["(none)"], font=ctk.CTkFont(size=12))
        def filter_items(*args, e=se, i=iom, opts=items):
            q = e.get().lower(); fil = [x for x in opts if q in x.lower()]
            i.configure(values=fil or ["(none)"])
            if fil: i.set(fil[0])
        se.bind("<KeyRelease>", filter_items)
        iom.set(items[0] if items else ""); iom.pack(fill="x", pady=(0,10))

        lbl(body, "Quantity Received", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0,3))
        e_qty = entry(body, ph="e.g., 25.5", h=38); e_qty.pack(fill="x", pady=(0,10))

        lbl(body, "New Cost Price (₹)  •  leave blank to keep existing",
            size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0,3))
        e_cp = entry(body, ph="e.g., 42", h=38); e_cp.pack(fill="x")

        def save():
            try:    qty = float(e_qty.get())
            except: self._popup("⚠️ Invalid","Enter numeric quantity."); return
            if qty <= 0: self._popup("⚠️ Invalid","Qty must be > 0."); return
            item = iom.get();  cp_val = e_cp.get().strip()
            with get_db() as conn:
                row = conn.execute("SELECT id,cp FROM inventory WHERE item=?", (item,)).fetchone()
                new_cp = float(cp_val) if cp_val else row["cp"]
                conn.execute("UPDATE inventory SET stock=stock+?,received=received+?,cp=? WHERE item=?",
                             (qty, qty, new_cp, item))
                conn.execute("INSERT INTO goods_received (date,inv_id,qty,total_cost) VALUES (?,?,?,?)",
                             (datetime.now().strftime("%Y-%m-%d"), row["id"], qty, qty*new_cp))
            self._popup("✅ Stock Received!", f"{item}: +{qty} @ ₹{new_cp}/unit")
            close(); self._go("inventory")

        btn(card, "✅  Confirm Receipt", save, fg=TEAL, hv=ARMY_BG, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")

    def _dlg_inv_edit(self):
        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        body, card, close = self._show_modal("✏️  Edit Inventory Item", 520, 420)

        lbl(body, "Select Item (Searchable)", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        se = ctk.CTkEntry(body, placeholder_text="🔍 Type to search...", height=32); se.pack(fill="x", pady=(0,4))
        iom = ctk.CTkOptionMenu(body, values=items or ["(none)"], font=ctk.CTkFont(size=12))
        def filter_items(*args, e=se, i=iom, opts=items):
            q = e.get().lower(); fil = [x for x in opts if q in x.lower()]
            i.configure(values=fil or ["(none)"])
            if fil: i.set(fil[0])
        se.bind("<KeyRelease>", filter_items)
        iom.set(items[0] if items else ""); iom.pack(fill="x", pady=(0,12))

        fields = {}
        for lbl_t, attr, ph in [
            ("New Stock Level (leave blank to skip)", "stock",   "e.g., 50"),
            ("New Min Level  (leave blank to skip)",  "min_lvl", "e.g., 10"),
            ("New Cost Price ₹ (leave blank to skip)","cp",      "e.g., 45"),
        ]:
            lbl(body, lbl_t, size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
            e = entry(body, ph=ph, h=38); e.pack(fill="x", pady=(0,4))
            fields[attr] = e

        def save():
            item = iom.get(); updates = {}
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
            close(); self._go("inventory")

        btn(card, "✅  Save Changes", save, fg=BLUE, hv=DBLUE, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")

    def _dlg_inv_del(self):
        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        if not items:
            self._popup("⚠️ Empty", "No inventory items to delete."); return

        body, card, close = self._show_modal("🗑  Delete Inventory Item", 500, 320)

        lbl(body, "Select Item to Delete", size=12, weight="bold",
            color=ARMY_BG).pack(anchor="w", pady=(4,6))
        se = ctk.CTkEntry(body, placeholder_text="🔍 Type to search...", height=34)
        se.pack(fill="x", pady=(0,6))
        iom = ctk.CTkOptionMenu(body, values=items, font=ctk.CTkFont(size=12), height=38)
        iom.set(items[0]); iom.pack(fill="x", pady=(0,10))

        def filter_items(*args):
            q = se.get().lower()
            fil = [x for x in items if q in x.lower()]
            iom.configure(values=fil or ["(none)"])
            if fil: iom.set(fil[0])
        se.bind("<KeyRelease>", filter_items)

        warn = ctk.CTkFrame(body, fg_color=BG_RED, corner_radius=8)
        warn.pack(fill="x", pady=(0, 12))
        lbl(warn, "⚠️  Permanently removes the item and all its recipe links.",
            size=10, color=RED).pack(padx=12, pady=8)

        def delete():
            item = iom.get()
            if item in ("", "(none)"):
                return
            if not self._confirm("Confirm Delete",
                                 f"Permanently delete '{item}' and all recipe links?"):
                return
            with get_db() as conn:
                inv_row = conn.execute("SELECT id FROM inventory WHERE item=?", (item,)).fetchone()
                if inv_row:
                    conn.execute("DELETE FROM recipes WHERE inv_id=?", (inv_row["id"],))
                    conn.execute("DELETE FROM stock_ledger WHERE inv_id=?", (inv_row["id"],))
                    conn.execute("DELETE FROM goods_received WHERE inv_id=?", (inv_row["id"],))
                    conn.execute("DELETE FROM inventory WHERE id=?", (inv_row["id"],))
            self._toast(f"🗑 '{item}' deleted from inventory")
            close(); self._go("inventory")

        btn(body, "🗑  Delete Permanently", delete, fg=RED, hv=DRED, h=46).pack(fill="x")

    # ==============================================================================
    # HISTORICAL / BACKDATED ENTRY  (Stock • Batch Prep • Sales for any date)
    # ==============================================================================
    def _dlg_backdated_entry(self, default_type="sales"):
        """
        Modal dialog to record Stock Received, Batch Prep, or Sales
        for any past (or current) date.  All relevant tables are updated
        with the chosen date so reports stay consistent.
        """
        with get_db() as conn:
            inv_items  = [r["item"] for r in
                          conn.execute("SELECT item FROM inventory ORDER BY item")]
            inv_cp     = {r["item"]: (r["id"], r["cp"] or 0, r["stock"] or 0)
                          for r in conn.execute("SELECT item,id,cp,stock FROM inventory")}
            menu_rows  = conn.execute(
                "SELECT id,name,sp FROM menu WHERE active=1 ORDER BY name").fetchall()

        menu_names = [m["name"] for m in menu_rows]
        menu_map   = {m["name"]: {"id": m["id"], "sp": m["sp"]} for m in menu_rows}

        body, card_w, close = self._show_modal(
            "📅  Historical / Backdated Entry", width=580, height=580)

        # ── Date ──────────────────────────────────────────────────────────────
        lbl(body, "Entry Date  (YYYY-MM-DD)",
            size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        e_date = entry(body, ph="e.g. 2026-06-01", h=38)
        e_date.pack(fill="x", pady=(0,10))
        e_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # ── Type selector ─────────────────────────────────────────────────────
        lbl(body, "Entry Type",
            size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0,4))
        type_var  = ctk.StringVar(value=default_type)
        type_btns = {}
        tf = ctk.CTkFrame(body, fg_color="transparent"); tf.pack(fill="x", pady=(0,12))
        TYPES = [("stock", "📦  Stock Received", TEAL),
                 ("batch", "🧑‍🍳  Batch Prep",   ARMY_BG),
                 ("sales", "🍽  Sales",           GREEN)]

        form_frame = ctk.CTkFrame(body, fg_color="transparent")
        form_frame.pack(fill="x")
        fields = {}

        def _select_type(code):
            type_var.set(code)
            for c2, b2 in type_btns.items():
                _, _, clr2 = next(x for x in TYPES if x[0] == c2)
                b2.configure(fg_color=clr2 if c2 == code else STRIPE,
                             text_color=WHITE if c2 == code else DARK)
            _refresh_form()

        for code, label, clr in TYPES:
            b = ctk.CTkButton(tf, text=label, width=165, height=34, corner_radius=8,
                              fg_color=clr if code == default_type else STRIPE,
                              text_color=WHITE if code == default_type else DARK,
                              hover_color=ARMY_HVR,
                              font=ctk.CTkFont(size=11, weight="bold"),
                              command=lambda c=code: _select_type(c))
            b.pack(side="left", padx=3)
            type_btns[code] = b

        # ── Dynamic form ──────────────────────────────────────────────────────
        def _refresh_form():
            for w in form_frame.winfo_children():
                w.destroy()
            fields.clear()
            t = type_var.get()

            if t == "stock":
                # ── Mode toggle: Single Item vs Bulk CSV ──────────────────────
                mode_var = ctk.StringVar(value="single")
                mtf = ctk.CTkFrame(form_frame, fg_color="transparent")
                mtf.pack(fill="x", pady=(4, 8))
                s_btn = ctk.CTkButton(mtf, text="📋  Single Item", width=148, height=30,
                                      corner_radius=7,
                                      fg_color=TEAL, text_color=WHITE,
                                      hover_color=ARMY_HVR,
                                      font=ctk.CTkFont(size=11, weight="bold"),
                                      command=lambda: _set_mode("single"))
                s_btn.pack(side="left", padx=(0, 6))
                c_btn = ctk.CTkButton(mtf, text="📂  Bulk CSV Upload", width=148, height=30,
                                      corner_radius=7,
                                      fg_color=STRIPE, text_color=DARK,
                                      hover_color=ARMY_HVR,
                                      font=ctk.CTkFont(size=11, weight="bold"),
                                      command=lambda: _set_mode("csv"))
                c_btn.pack(side="left")
                fields["mode_var"] = mode_var
                fields["s_btn"] = s_btn
                fields["c_btn"] = c_btn

                inner = ctk.CTkFrame(form_frame, fg_color="transparent")
                inner.pack(fill="x")
                fields["inner"] = inner

                def _set_mode(m):
                    mode_var.set(m)
                    s_btn.configure(fg_color=TEAL if m == "single" else STRIPE,
                                    text_color=WHITE if m == "single" else DARK)
                    c_btn.configure(fg_color=TEAL if m == "csv" else STRIPE,
                                    text_color=WHITE if m == "csv" else DARK)
                    for w in inner.winfo_children():
                        w.destroy()
                    if m == "single":
                        _build_single(inner)
                    else:
                        _build_csv(inner)

                def _build_single(p):
                    # Is this item NEW or EXISTING?
                    item_mode_var = ctk.StringVar(value="existing")
                    mf = ctk.CTkFrame(p, fg_color="transparent"); mf.pack(fill="x", pady=(0, 8))
                    eb = ctk.CTkButton(mf, text="📦  Update Existing", width=148, height=28,
                                       corner_radius=6, fg_color=TEAL, text_color=WHITE,
                                       font=ctk.CTkFont(size=10, weight="bold"), hover_color=ARMY_HVR,
                                       command=lambda: _set_item_mode("existing"))
                    eb.pack(side="left", padx=(0, 6))
                    nb = ctk.CTkButton(mf, text="✦  Add New Item", width=148, height=28,
                                       corner_radius=6, fg_color=STRIPE, text_color=DARK,
                                       font=ctk.CTkFont(size=10, weight="bold"), hover_color=ARMY_HVR,
                                       command=lambda: _set_item_mode("new"))
                    nb.pack(side="left")
                    fields["item_mode"] = item_mode_var

                    item_form = ctk.CTkFrame(p, fg_color="transparent"); item_form.pack(fill="x")

                    def _set_item_mode(m):
                        item_mode_var.set(m)
                        eb.configure(fg_color=TEAL if m=="existing" else STRIPE,
                                     text_color=WHITE if m=="existing" else DARK)
                        nb.configure(fg_color=TEAL if m=="new" else STRIPE,
                                     text_color=WHITE if m=="new" else DARK)
                        for w in item_form.winfo_children(): w.destroy()
                        if m == "existing":
                            _form_existing(item_form)
                        else:
                            _form_new(item_form)

                    CATS = ["Dry", "Fresh", "Dairy", "Bakery", "Prepared", "Misc"]

                    def _form_existing(fp):
                        lbl(fp, "Inventory Item", size=11, weight="bold",
                            color=ARMY_BG).pack(anchor="w", pady=(0, 3))
                        se2 = ctk.CTkEntry(fp, placeholder_text="🔍 Search...", height=32)
                        se2.pack(fill="x", pady=(0, 4))
                        iom2 = ctk.CTkOptionMenu(fp, values=inv_items or ["(none)"],
                                                 font=ctk.CTkFont(size=12), height=36)
                        if inv_items: iom2.set(inv_items[0])
                        iom2.pack(fill="x", pady=(0, 8))
                        def _fi2(*a, e=se2, i=iom2, opts=inv_items):
                            q = e.get().lower()
                            fil = [x for x in opts if q in x.lower()]
                            i.configure(values=fil or ["(none)"])
                            if fil: i.set(fil[0])
                        se2.bind("<KeyRelease>", _fi2)
                        fields["item_om"] = iom2

                        qr = ctk.CTkFrame(fp, fg_color="transparent"); qr.pack(fill="x")
                        qr.grid_columnconfigure(0, weight=1); qr.grid_columnconfigure(1, weight=1)
                        lbl(qr, "Qty Received", size=11, weight="bold",
                            color=ARMY_BG).grid(row=0, column=0, sticky="w", pady=(0, 3))
                        eq2 = entry(qr, ph="e.g. 10.0", h=38)
                        eq2.grid(row=1, column=0, sticky="ew", padx=(0, 8))
                        fields["qty"] = eq2
                        lbl(qr, "Cost Price ₹/unit (optional)", size=11, weight="bold",
                            color=ARMY_BG).grid(row=0, column=1, sticky="w", pady=(0, 3))
                        ecp2 = entry(qr, ph="leave blank to keep current", h=38)
                        ecp2.grid(row=1, column=1, sticky="ew")
                        fields["cp"] = ecp2

                        lbl(fp, "Notes (optional)", size=11, weight="bold",
                            color=ARMY_BG).pack(anchor="w", pady=(8, 3))
                        en2 = entry(fp, ph="e.g. Monthly ration received", h=38)
                        en2.pack(fill="x")
                        fields["notes"] = en2

                    def _form_new(fp):
                        lbl(fp, "Item Name  (must not already exist)", size=11, weight="bold",
                            color=ARMY_BG).pack(anchor="w", pady=(0, 3))
                        e_nm = entry(fp, ph="e.g., Mustard Oil", h=38); e_nm.pack(fill="x", pady=(0, 6))
                        fields["new_name"] = e_nm

                        r1 = ctk.CTkFrame(fp, fg_color="transparent"); r1.pack(fill="x")
                        r1.grid_columnconfigure(0, weight=1); r1.grid_columnconfigure(1, weight=1)
                        lbl(r1, "Category", size=11, weight="bold",
                            color=ARMY_BG).grid(row=0, column=0, sticky="w", pady=(0, 3))
                        cat_om = ctk.CTkOptionMenu(r1, values=CATS,
                                                   font=ctk.CTkFont(size=11), height=34)
                        cat_om.set("Dry")
                        cat_om.grid(row=1, column=0, sticky="ew", padx=(0, 8))
                        fields["new_cat"] = cat_om
                        lbl(r1, "Unit  (kg / ltr / pcs)", size=11, weight="bold",
                            color=ARMY_BG).grid(row=0, column=1, sticky="w", pady=(0, 3))
                        e_unit = entry(r1, ph="e.g., kg", h=34)
                        e_unit.grid(row=1, column=1, sticky="ew")
                        fields["new_unit"] = e_unit

                        r2 = ctk.CTkFrame(fp, fg_color="transparent"); r2.pack(fill="x", pady=(6, 0))
                        r2.grid_columnconfigure(0, weight=1); r2.grid_columnconfigure(1, weight=1)
                        lbl(r2, "Opening Stock (qty)", size=11, weight="bold",
                            color=ARMY_BG).grid(row=0, column=0, sticky="w", pady=(0, 3))
                        e_stk = entry(r2, ph="e.g., 50", h=38)
                        e_stk.grid(row=1, column=0, sticky="ew", padx=(0, 8))
                        fields["new_stock"] = e_stk
                        lbl(r2, "Min Level Alert", size=11, weight="bold",
                            color=ARMY_BG).grid(row=0, column=1, sticky="w", pady=(0, 3))
                        e_min = entry(r2, ph="e.g., 5", h=38)
                        e_min.grid(row=1, column=1, sticky="ew")
                        fields["new_min"] = e_min

                        lbl(fp, "Cost Price ₹/unit", size=11, weight="bold",
                            color=ARMY_BG).pack(anchor="w", pady=(8, 3))
                        e_cp2 = entry(fp, ph="e.g., 90", h=38); e_cp2.pack(fill="x")
                        fields["new_cp"] = e_cp2

                    _form_existing(item_form)   # default

                def _build_csv(p):
                    # Format info box
                    info = ctk.CTkFrame(p, fg_color=BG_GRN, corner_radius=8)
                    info.pack(fill="x", pady=(0, 8))
                    lbl(info, "CSV Format — same as Import Data page:",
                        size=10, weight="bold", color=ARMY_BG).pack(anchor="w", padx=10, pady=(6, 2))
                    lbl(info, "item, qty_received, category, unit, min_level, cost_price, notes",
                        size=9, color=DARK).pack(anchor="w", padx=10)
                    lbl(info, "Example:  RICE, 50, Dry, kg, 10, 45.00, Weekly ration",
                        size=9, color=MID).pack(anchor="w", padx=10)
                    lbl(info, "• category, unit, min_level, cost_price, notes → optional",
                        size=9, color=MID).pack(anchor="w", padx=10)
                    lbl(info, "• Existing item → qty ADDED to stock",
                        size=9, weight="bold", color=TEAL).pack(anchor="w", padx=10)
                    lbl(info, "• New item (not in inventory) → CREATED if category+unit present",
                        size=9, weight="bold", color=ARMY_BG).pack(anchor="w", padx=10, pady=(0, 6))

                    # File picker row
                    pf2 = ctk.CTkFrame(p, fg_color="transparent")
                    pf2.pack(fill="x", pady=(0, 6))
                    path_var = ctk.StringVar(value="No file selected")
                    ctk.CTkLabel(pf2, textvariable=path_var,
                                 font=ctk.CTkFont(size=9), text_color=MID,
                                 anchor="w").pack(side="left", fill="x", expand=True)

                    def _pick():
                        import tkinter.filedialog as fd
                        fp = fd.askopenfilename(
                            title="Select Stock CSV",
                            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
                        if fp:
                            path_var.set(fp)
                            fields["csv_path"] = fp
                            _preview(fp)

                    btn(pf2, "📂  Choose File", _pick,
                        fg=TEAL, hv=ARMY_BG, h=32, w=130).pack(side="right")

                    # Preview card
                    prev = ctk.CTkFrame(p, fg_color=STRIPE, corner_radius=8)
                    prev.pack(fill="x")
                    fields["csv_path"] = ""
                    fields["csv_rows"] = []
                    fields["prev_card"] = prev

                    def _preview(fp):
                        import csv as csv_mod
                        for w in prev.winfo_children():
                            w.destroy()
                        rows_ok, rows_bad = [], []
                        VALID_CATS = {"dry","fresh","dairy","bakery","prepared","misc"}
                        try:
                            with open(fp, newline="", encoding="utf-8-sig") as f:
                                reader = csv_mod.DictReader(f)
                                hdrs = [h.strip().lower()
                                        for h in (reader.fieldnames or [])]
                                reader.fieldnames = hdrs
                                inv_upper = {x.upper(): x for x in inv_items}
                                for row in reader:
                                    raw_item = (row.get("item") or "").strip()
                                    if not raw_item:
                                        continue
                                    qty_s = (row.get("qty_received")
                                             or row.get("qty") or "").strip()
                                    cat_s = (row.get("category") or row.get("cat") or "").strip()
                                    unit_s= (row.get("unit") or "").strip()
                                    min_s = (row.get("min_level") or row.get("min") or "").strip()
                                    cp_s  = (row.get("cost_price")
                                             or row.get("cp") or "").strip()
                                    nt_s  = (row.get("notes")
                                             or row.get("note") or "").strip()
                                    try:
                                        qty_f = float(qty_s)
                                    except Exception:
                                        rows_bad.append(f"Bad qty: '{raw_item}'")
                                        continue
                                    if qty_f <= 0:
                                        rows_bad.append(f"Zero qty: '{raw_item}'")
                                        continue
                                    matched      = inv_upper.get(raw_item.upper())
                                    can_create   = (not matched
                                                    and bool(cat_s) and bool(unit_s))
                                    rows_ok.append({
                                        "item":       matched or raw_item,
                                        "qty":        qty_f,
                                        "cat":        cat_s,
                                        "unit":       unit_s,
                                        "min":        float(min_s) if min_s else 0,
                                        "cp":         cp_s,
                                        "notes":      nt_s,
                                        "exists":     matched is not None,
                                        "can_create": can_create
                                    })
                            fields["csv_rows"] = rows_ok
                            upd = sum(1 for r in rows_ok if r["exists"])
                            new = sum(1 for r in rows_ok if not r["exists"] and r["can_create"])
                            skp = sum(1 for r in rows_ok if not r["exists"] and not r["can_create"])
                            bad = len(rows_bad)
                            summary = (f"  ↑ {upd} update   ✦ {new} new"
                                       + (f"   ✗ {skp} skip" if skp else "")
                                       + (f"   ⚠ {bad} bad qty" if bad else ""))
                            lbl(prev, summary, size=10, weight="bold",
                                color=GREEN if (upd + new) > 0 else RED
                                ).pack(anchor="w", padx=10, pady=(6, 2))
                            for r in rows_ok[:8]:
                                if r["exists"]:
                                    flag, clr = "↑ update", DARK
                                elif r["can_create"]:
                                    flag, clr = f"✦ NEW ({r['cat']}/{r['unit']})", TEAL
                                else:
                                    flag, clr = "✗ skip — add category+unit", RED
                                lbl(prev,
                                    f"  {r['item'][:26]:26s}  +{r['qty']}"
                                    + (f"  @₹{r['cp']}" if r["cp"] else "")
                                    + f"  [{flag}]",
                                    size=9, color=clr).pack(anchor="w", padx=10)
                            if len(rows_ok) > 8:
                                lbl(prev, f"  … {len(rows_ok) - 8} more rows",
                                    size=9, color=MID).pack(anchor="w", padx=10)
                            for b in rows_bad[:3]:
                                lbl(prev, f"  ⚠ {b}", size=9,
                                    color=RED).pack(anchor="w", padx=10)
                            if rows_bad:
                                lbl(prev, "  (rows with bad/zero qty are skipped)",
                                    size=8, color=MID).pack(anchor="w", padx=10, pady=(0, 6))
                        except Exception as ex:
                            fields["csv_rows"] = []
                            lbl(prev, f"  ❌ Could not read CSV: {ex}",
                                size=9, color=RED).pack(anchor="w", padx=10, pady=6)

                _build_single(inner)   # default to single-item mode


            elif t == "batch":
                lbl(form_frame, "Menu Item", size=11, weight="bold",
                    color=ARMY_BG).pack(anchor="w", pady=(4,3))
                mom = ctk.CTkOptionMenu(form_frame, values=menu_names or ["(none)"],
                                        font=ctk.CTkFont(size=12), height=36)
                if menu_names: mom.set(menu_names[0])
                mom.pack(fill="x", pady=(0,8))
                fields["menu_om"] = mom

                lbl(form_frame, "Qty Prepared (portions)", size=11, weight="bold",
                    color=ARMY_BG).pack(anchor="w", pady=(0,3))
                e_qty = entry(form_frame, ph="e.g. 100", h=38)
                e_qty.pack(fill="x", pady=(0,8))
                fields["qty"] = e_qty

                dv = ctk.BooleanVar(value=True)
                ctk.CTkCheckBox(form_frame, text="Deduct raw material stock",
                                variable=dv, text_color=ARMY_BG,
                                font=ctk.CTkFont(size=11)).pack(anchor="w", pady=(0,4))
                fields["deduct"] = dv

                ev = ctk.BooleanVar(value=True)
                ctk.CTkCheckBox(form_frame, text="Log raw material cost as Expenditure",
                                variable=ev, text_color=ARMY_BG,
                                font=ctk.CTkFont(size=11)).pack(anchor="w")
                fields["log_exp"] = ev

            elif t == "sales":
                lbl(form_frame, "Menu Item", size=11, weight="bold",
                    color=ARMY_BG).pack(anchor="w", pady=(4,3))
                mom = ctk.CTkOptionMenu(form_frame, values=menu_names or ["(none)"],
                                        font=ctk.CTkFont(size=12), height=36)
                if menu_names: mom.set(menu_names[0])
                mom.pack(fill="x", pady=(0,8))
                fields["menu_om"] = mom

                rf = ctk.CTkFrame(form_frame, fg_color="transparent"); rf.pack(fill="x")
                rf.grid_columnconfigure(0, weight=1); rf.grid_columnconfigure(1, weight=1)
                lbl(rf, "Qty Sold", size=11, weight="bold",
                    color=ARMY_BG).grid(row=0, column=0, sticky="w", pady=(0,3))
                e_qty = entry(rf, ph="e.g. 50", h=38)
                e_qty.grid(row=1, column=0, sticky="ew", padx=(0,8), pady=(0,8))
                fields["qty"] = e_qty

                m_name = mom.get()
                default_sp = str(int(menu_map[m_name]["sp"])) if m_name in menu_map else ""
                lbl(rf, "Selling Price ₹/plate", size=11, weight="bold",
                    color=ARMY_BG).grid(row=0, column=1, sticky="w", pady=(0,3))
                e_sp = entry(rf, ph="e.g. 45", h=38)
                e_sp.grid(row=1, column=1, sticky="ew", pady=(0,8))
                if default_sp: e_sp.insert(0, default_sp)
                fields["sp"] = e_sp

                lbl(form_frame, "Payment Method", size=11, weight="bold",
                    color=ARMY_BG).pack(anchor="w", pady=(0,3))
                pm = ctk.CTkOptionMenu(form_frame, values=["Cash","UPI","Card"],
                                       font=ctk.CTkFont(size=12), height=36)
                pm.pack(fill="x")
                fields["payment"] = pm

        _refresh_form()

        # ── Save ──────────────────────────────────────────────────────────────
        def _save():
            date_str = e_date.get().strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                self._popup("⚠️ Invalid Date",
                            "Use format YYYY-MM-DD\ne.g. 2026-06-01"); return

            t = type_var.get()

            # ── Stock Received ────────────────────────────────────────────────
            if t == "stock":
                mode = fields.get("mode_var") and fields["mode_var"].get() or "single"
                CATS_VALID = ["Dry", "Fresh", "Dairy", "Bakery", "Prepared", "Misc"]

                def _do_stock_update(conn, item_name, qty, cp_str, notes_str):
                    """Add qty to an EXISTING item. Returns (ok, msg)."""
                    row = conn.execute(
                        "SELECT id, stock, cp FROM inventory WHERE item=? COLLATE NOCASE",
                        (item_name,)).fetchone()
                    if not row:
                        return False, f"'{item_name}' not found"
                    new_stock = (row["stock"] or 0) + qty
                    new_cp    = float(cp_str) if cp_str else (row["cp"] or 0)
                    conn.execute(
                        "UPDATE inventory SET stock=?, cp=?, updated=? WHERE id=?",
                        (new_stock, new_cp, date_str, row["id"]))
                    conn.execute(
                        "INSERT INTO stock_ledger "
                        "(date, inv_id, transaction_type, qty_change, notes) "
                        "VALUES (?,?,'Received',?,?)",
                        (date_str, row["id"], qty, notes_str))
                    conn.execute(
                        "INSERT INTO goods_received (date, inv_id, qty, total_cost) "
                        "VALUES (?,?,?,?)",
                        (date_str, row["id"], qty, qty * new_cp))
                    return True, f"{item_name} +{qty}"

                def _do_stock_create(conn, item_name, qty, cat, unit, min_lvl,
                                     cp_str, notes_str):
                    """CREATE a new inventory item then log stock receipt. Returns (ok, msg)."""
                    try:
                        cp_val = float(cp_str) if cp_str else 0.0
                        conn.execute(
                            "INSERT INTO inventory "
                            "(item, cat, unit, stock, min_lvl, opening, cp) "
                            "VALUES (?,?,?,?,?,?,?)",
                            (item_name, cat, unit, qty, min_lvl, qty, cp_val))
                        new_id = conn.execute(
                            "SELECT id FROM inventory WHERE item=? COLLATE NOCASE",
                            (item_name,)).fetchone()["id"]
                        conn.execute(
                            "INSERT INTO stock_ledger "
                            "(date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Opening',?,?)",
                            (date_str, new_id, qty, notes_str or f"New item via import — {date_str}"))
                        return True, f"{item_name} created ({cat}/{unit}) +{qty}"
                    except sqlite3.IntegrityError:
                        return False, f"'{item_name}' duplicate — skipped"

                if mode == "single":
                    item_mode = fields.get("item_mode") and fields["item_mode"].get() or "existing"

                    if item_mode == "existing":
                        item = fields.get("item_om") and fields["item_om"].get() or ""
                        if item in ("", "(none)"):
                            self._popup("⚠️ No Item", "Select an inventory item."); return
                        try:    qty = float(fields["qty"].get() or 0)
                        except: self._popup("⚠️ Invalid Qty", "Enter a numeric quantity."); return
                        if qty <= 0:
                            self._popup("⚠️ Zero Qty", "Quantity must be > 0."); return
                        cp_str = fields.get("cp") and fields["cp"].get().strip() or ""
                        notes  = (fields.get("notes") and fields["notes"].get().strip()
                                  or f"Stock received — {date_str}")
                        with get_db() as conn:
                            ok, msg = _do_stock_update(conn, item, qty, cp_str, notes)
                        if ok:
                            self._toast(f"✅ {msg}  ({date_str})")
                            close(); self._live_refresh("inventory")
                        else:
                            self._popup("⚠️ Not Found", msg)

                    else:  # new item
                        nm   = fields.get("new_name") and fields["new_name"].get().strip() or ""
                        cat  = fields.get("new_cat")  and fields["new_cat"].get() or ""
                        unit = fields.get("new_unit") and fields["new_unit"].get().strip() or ""
                        if not nm:
                            self._popup("⚠️ No Name", "Enter an item name."); return
                        if not unit:
                            self._popup("⚠️ No Unit", "Enter the unit (kg / ltr / pcs)."); return
                        try:    stk = float(fields["new_stock"].get() or 0)
                        except: self._popup("⚠️ Invalid Stock", "Enter numeric opening stock."); return
                        try:    mn  = float(fields["new_min"].get() or 0)
                        except: mn = 0
                        cp_str = fields.get("new_cp") and fields["new_cp"].get().strip() or ""
                        with get_db() as conn:
                            ok, msg = _do_stock_create(
                                conn, nm, stk, cat, unit, mn, cp_str, "")
                        if ok:
                            self._toast(f"✅ {msg}")
                            close(); self._live_refresh("inventory")
                        else:
                            self._popup("⚠️ Error", msg)

                else:  # CSV mode
                    rows = fields.get("csv_rows") or []
                    if not rows:
                        self._popup("⚠️ No Data",
                                    "Load a CSV file first and confirm the preview."); return
                    updated, created, skipped = 0, 0, []
                    with get_db() as conn:
                        for r in rows:
                            notes_r = r["notes"] or f"Bulk CSV import — {date_str}"
                            if r["exists"]:
                                ok, _ = _do_stock_update(
                                    conn, r["item"], r["qty"], r["cp"], notes_r)
                                if ok: updated += 1
                                else:  skipped.append(r["item"])
                            elif r["can_create"]:
                                cat_val = r["cat"] or "Dry"
                                ok, _ = _do_stock_create(
                                    conn, r["item"], r["qty"],
                                    cat_val, r["unit"], r["min"],
                                    r["cp"], notes_r)
                                if ok: created += 1
                                else:  skipped.append(r["item"])
                            else:
                                skipped.append(r["item"] + " (missing category/unit)")

                    msg = f"✅ CSV complete — {updated} updated, {created} new items created"
                    if skipped:
                        msg += f", {len(skipped)} skipped"
                    self._toast(msg, duration_ms=5000)
                    if skipped:
                        self._popup(
                            "⚠️ Items Skipped",
                            f"{len(skipped)} item(s) skipped:\n\n"
                            + "\n".join(skipped[:15])
                            + ("\n..." if len(skipped) > 15 else "")
                            + "\n\nFor new items, make sure 'category' and 'unit' "
                              "columns are filled in the CSV.")
                    close(); self._live_refresh("inventory")


            # ── Batch Prep ────────────────────────────────────────────────────
            elif t == "batch":
                menu_name = fields["menu_om"].get()
                if menu_name not in menu_map:
                    self._popup("⚠️ No Menu", "Select a valid menu item."); return
                try:    qty = int(fields["qty"].get() or 0)
                except: self._popup("⚠️ Invalid Qty", "Whole number required."); return
                if qty <= 0:
                    self._popup("⚠️ Zero Qty", "Quantity must be > 0."); return
                menu_id   = menu_map[menu_name]["id"]
                do_deduct = fields["deduct"].get()
                do_exp    = fields["log_exp"].get()

                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO batch_prep (date, menu_id, qty_prepared) "
                        "VALUES (?,?,?)", (date_str, menu_id, qty))

                    recipes = conn.execute(
                        "SELECT r.inv_id, r.qty_per_unit, i.item, i.unit, i.cp "
                        "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
                        "WHERE r.menu_id=?", (menu_id,)).fetchall()

                    total_raw_cost = 0.0
                    for rc in recipes:
                        used = rc["qty_per_unit"] * qty
                        total_raw_cost += used * (rc["cp"] or 0)
                        if do_deduct:
                            conn.execute(
                                "UPDATE inventory SET stock=MAX(0,stock-?) WHERE id=?",
                                (used, rc["inv_id"]))
                            conn.execute(
                                "INSERT INTO stock_ledger "
                                "(date, inv_id, transaction_type, qty_change, notes) "
                                "VALUES (?,?,'Batch_Prep',?,?)",
                                (date_str, rc["inv_id"], -used,
                                 f"Backdated batch: {menu_name} ×{qty} on {date_str}"))

                    if do_exp and total_raw_cost > 0:
                        conn.execute(
                            "INSERT INTO expenditure "
                            "(date, amount, category, notes) VALUES (?,?,?,?)",
                            (date_str, round(total_raw_cost, 2),
                             "Raw Material",
                             f"Batch: {menu_name} | {date_str}"))

                self._toast(
                    f"✅ Batch: {menu_name} ×{qty} logged for {date_str}"
                    + (f"  |  ₹{total_raw_cost:,.0f} expenditure" if do_exp else ""))
                close(); self._live_refresh("batch")

            # ── Sales ─────────────────────────────────────────────────────────
            elif t == "sales":
                menu_name = fields["menu_om"].get()
                if menu_name not in menu_map:
                    self._popup("⚠️ No Menu", "Select a valid menu item."); return
                try:    qty = int(fields["qty"].get() or 0)
                except: self._popup("⚠️ Invalid Qty", "Whole number required."); return
                if qty <= 0:
                    self._popup("⚠️ Zero Qty", "Quantity must be > 0."); return
                try:    sp = float(fields["sp"].get() or 0)
                except: self._popup("⚠️ Invalid Price", "Enter a numeric price."); return
                if sp <= 0:
                    self._popup("⚠️ Zero Price", "Selling price must be > 0."); return
                payment = fields["payment"].get()
                menu_id = menu_map[menu_name]["id"]

                with get_db() as conn:
                    cur = conn.execute(
                        "INSERT INTO sales "
                        "(date,menu_id,meal,sp,sold,wastage,cogs,payment) "
                        "VALUES (?,?,?,?,?,0,0.0,?)",
                        (date_str, menu_id, menu_name, sp, qty, payment))
                    new_sale_id = cur.lastrowid
                    # Compute COGS for audit (no stock deduction — batch already handles it)
                    cpu, _, _ = self._apply_stock_deduction(
                        conn, menu_id, qty, new_sale_id, date_str)
                    conn.execute(
                        "UPDATE sales SET cogs=? WHERE id=?",
                        (qty * cpu, new_sale_id))

                self._toast(
                    f"✅ Sale: {menu_name} ×{qty} @ ₹{sp:.0f} ({payment}) for {date_str}"
                    f"  |  Revenue ₹{sp*qty:,.0f}")
                close(); self._live_refresh("sales")

        btn(card_w, "✅  Save Entry", _save, fg=GREEN, hv=DGREEN, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")

    # ==============================================================================
    # EXPENDITURE
    # ==============================================================================
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
                              variable=self._exp_deduct, text_color=ARMY_BG, font=ctk.CTkFont(size=11, weight="bold"))
        cdc.pack(anchor="w", padx=18, pady=(0,10))
        
        invf = ctk.CTkFrame(fc, fg_color=BG_SAF, corner_radius=8)
        
        with get_db() as conn: inv_items = [r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")]
        lbl(invf, "Inventory Item", size=11, weight="bold", color=ARMY_BG).grid(row=0, column=0, sticky="w", padx=14, pady=(8,4))
        exp_iom = ctk.CTkOptionMenu(invf, values=inv_items or ["(none)"], font=ctk.CTkFont(size=11))
        exp_iom.grid(row=1, column=0, sticky="ew", padx=(14,8), pady=(0,8))
        lbl(invf, "Quantity Received", size=11, weight="bold", color=ARMY_BG).grid(row=0, column=1, sticky="w", padx=(8,14), pady=(8,4))
        exp_qty = entry(invf, ph="e.g. 50", h=32); exp_qty.grid(row=1, column=1, sticky="ew", padx=(8,14), pady=(0,8))
        invf.grid_columnconfigure(0, weight=2); invf.grid_columnconfigure(1, weight=1)
        
        def toggle_inv(*args):
            if self._exp_deduct.get(): invf.pack(fill="x", padx=18, pady=(0,14), after=cdc)
            else: invf.pack_forget()
        cdc.configure(command=toggle_inv)

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
            try: 
                eq = float(exp_qty.get() or 0) if self._exp_deduct.get() else 0
            except: 
                self._popup("⚠️ Invalid","Enter numeric qty"); return
            
            with get_db() as conn:
                conn.execute("INSERT INTO expenditure (date,amount,category,notes) VALUES (?,?,?,?)",
                             (exp_date, amt, cat, notes or None))
                if self._exp_deduct.get() and eq > 0:
                    it = exp_iom.get()
                    row = conn.execute("SELECT id,cp FROM inventory WHERE item=?", (it,)).fetchone()
                    new_cp = round(amt / eq, 2)  # actual cost-per-unit from this purchase
                    conn.execute("UPDATE inventory SET stock=stock+?,received=received+?,cp=? WHERE item=?",
                                 (eq, eq, new_cp, it))
                    conn.execute("INSERT INTO goods_received (date,inv_id,qty,total_cost) VALUES (?,?,?,?)",
                                 (exp_date, row["id"], eq, amt))
            self._popup("✅ Expenditure Saved!", f"₹{amt:,.0f} under {cat}")
            e_amt.delete(0,"end"); e_notes.delete(0,"end")
            self._toast(f"✅ ₹{amt:,.0f} under {cat}")
            self._live_refresh("expenditure")

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
                rows = conn.execute("SELECT * FROM expenditure ORDER BY date DESC, amount DESC, id DESC").fetchall()
            else:
                rows = conn.execute("SELECT * FROM expenditure WHERE category=? ORDER BY date DESC, amount DESC, id DESC",
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

    # ==============================================================================
    # WASTE — modern with stock selector
    # ==============================================================================
    def _pg_waste(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")
        self._hdr("\u267b\ufe0f  Waste Management", f"\U0001f4c5  {today_disp}")

        with get_db() as conn:
            inv_data = conn.execute("SELECT item, unit, cp FROM inventory ORDER BY item").fetchall()
            inv_items = sorted([f"{r['item']} ({r['unit']})" for r in inv_data])
            self._cost_map = {f"{r['item']} ({r['unit']})": r["cp"] for r in inv_data}
            wr = conn.execute("SELECT * FROM waste_tracker WHERE date=? ORDER BY id DESC",
                              (today,)).fetchall()

        total_wc = sum(w["cost_lost"] or 0 for w in wr)

        # Summary strip
        sf = ctk.CTkFrame(self._area, fg_color=ARMY_BG, corner_radius=0, height=52)
        sf.pack(fill="x", padx=PAD, pady=(10,0)); sf.pack_propagate(False)
        for icon, label, val, clr in [
            ("\U0001f5d1", "Entries Today", str(len(wr)), SAFFRON),
            ("\U0001f4b8", "Total Loss", f"\u20b9{total_wc:,.0f}", "#F87171"),
        ]:
            cf = ctk.CTkFrame(sf, fg_color="transparent"); cf.pack(side="left", padx=24, expand=True)
            lbl(cf, f"{icon}  {label}", size=10, color="#94A3B8").pack(anchor="w")
            lbl(cf, val, size=18, weight="bold", color=clr).pack(anchor="w")

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(10,PAD))

        # ── Record form ───────────────────────────────────────────────────────
        wc = card(wrap); wc.pack(fill="x", pady=(0,14))
        band(wc, "\U0001f4dd  Record Wastage")

        body = ctk.CTkFrame(wc, fg_color="transparent"); body.pack(fill="x", padx=18, pady=14)

        # Row 1: Item selection with search
        lbl(body, "Select Stock Item (Searchable)", size=11, weight="bold",
            color=ARMY_BG).pack(anchor="w", pady=(0,4))
        se = ctk.CTkEntry(body, placeholder_text="\U0001f50d  Type to search stock...", height=32)
        se.pack(fill="x", pady=(0,6))
        self._wi_om = ctk.CTkOptionMenu(body, values=inv_items or ["(none)"],
                                        font=ctk.CTkFont(size=12))
        self._wi_om.set(inv_items[0] if inv_items else "")
        self._wi_om.pack(fill="x", pady=(0,10))

        # Row 2: Qty + Cost side by side
        r2 = ctk.CTkFrame(body, fg_color="transparent"); r2.pack(fill="x", pady=(0,10))
        r2.grid_columnconfigure(0, weight=1); r2.grid_columnconfigure(1, weight=1)

        lbl(r2, "Qty Wasted", size=11, weight="bold", color=ARMY_BG).grid(
            row=0, column=0, sticky="w", pady=(0,4))
        self._wq = entry(r2, ph="e.g., 2.5", h=36)
        self._wq.grid(row=1, column=0, sticky="ew", padx=(0,8))

        lbl(r2, "Estimated Cost (\u20b9)", size=11, weight="bold", color=ARMY_BG).grid(
            row=0, column=1, sticky="w", padx=(8,0), pady=(0,4))
        self._wc = entry(r2, ph="e.g., 150", h=36)
        self._wc.grid(row=1, column=1, sticky="ew", padx=(8,0))

        def _calc_waste_cost(*args):
            try:
                qty = float(self._wq.get() or 0)
                item_label = self._wi_om.get()
                cp = getattr(self, "_cost_map", {}).get(item_label, 0)
                if qty > 0 and cp > 0:
                    est_cost = qty * cp
                    self._wc.delete(0, 'end')
                    self._wc.insert(0, f"{est_cost:.0f}")
                elif not self._wc.get():
                    self._wc.delete(0, 'end')
                    self._wc.insert(0, "0")
            except ValueError:
                pass
                
        self._wi_om.configure(command=lambda _: _calc_waste_cost())
        self._wq.bind("<KeyRelease>", _calc_waste_cost)

        def filter_waste_items(*args):
            q = se.get().lower()
            fil = [x for x in inv_items if q in x.lower()]
            self._wi_om.configure(values=fil or ["(none)"])
            if fil: 
                self._wi_om.set(fil[0])
                _calc_waste_cost()
        se.bind("<KeyRelease>", filter_waste_items)

        # Row 3: Reason
        lbl(body, "Reason", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(0,4))
        self._wr = ctk.CTkOptionMenu(body, values=[
            "Spoilage","Preparation Error","Plate Waste",
            "Burn/Over-cooked","Storage Issue","Expiry","Other"],
            font=ctk.CTkFont(size=12))
        self._wr.set("Spoilage"); self._wr.pack(fill="x", pady=(0,6))

        # Deduct checkbox
        self._waste_deduct = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(body, text="Also deduct from inventory stock",
                        variable=self._waste_deduct, text_color=ARMY_BG,
                        font=ctk.CTkFont(size=11, weight="bold"),
                        checkbox_width=20, checkbox_height=20).pack(anchor="w", pady=(4,0))

        btn(wc, "\u2705  Record Waste", self._save_waste,
            fg=ORANGE, hv="#EA580C", h=46).pack(padx=18, pady=(0,14), fill="x")

        # ── Today's log ──────────────────────────────────────────────────────
        lc = card(wrap); lc.pack(fill="both", expand=True)
        band(lc, f"\U0001f4cb  Today\u2019s Waste Log  \u2022  {today_disp}")
        if not wr:
            lbl(lc, "\u2705  No wastage recorded today.", size=12, color=GREEN).pack(pady=22)
        else:
            COLS = [("Item",3),("Qty",1),("Reason",2),("Cost",1),("By",2),("Del",1)]
            thead(lc, COLS, bg=STRIPE, tc=MID)
            for ix, w in enumerate(wr):
                bg2 = WHITE if ix%2==0 else STRIPE
                rf = ctk.CTkFrame(lc, fg_color=bg2, corner_radius=0, height=38)
                rf.pack(fill="x"); rf.pack_propagate(False)
                for j,(v,wt) in enumerate(zip(
                        [w["item"],f"{w['qty_wasted']:.1f}",w["reason"],
                         f"\u20b9{w['cost_lost']:.0f}",w["recorded_by"] or "\u2014"],
                        [3,1,2,1,2])):
                    lbl(rf,v,size=11,color=DARK if j==0 else MID,
                        weight="bold" if j==0 else "normal").grid(row=0,column=j,padx=14,sticky="w")
                    rf.grid_columnconfigure(j,weight=wt)
                del_btn = ctk.CTkButton(rf, text="\U0001f5d1", width=28, height=26,
                                        fg_color=STRIPE, hover_color=T_RED,
                                        text_color=RED, corner_radius=6,
                                        font=ctk.CTkFont(size=11),
                                        command=lambda wid=w["id"]: self._del_waste(wid))
                del_btn.grid(row=0,column=5,padx=8,sticky="e")
                rf.grid_columnconfigure(5,weight=1)
            tot = ctk.CTkFrame(lc, fg_color=BG_RED, height=34, corner_radius=0)
            tot.pack(fill="x"); tot.pack_propagate(False)
            lbl(tot, f"  TOTAL WASTE: \u20b9{total_wc:,.0f}", size=11,
                weight="bold", color=RED).pack(side="left", padx=10)

        # ── All Waste History ────────────────────────────────────────────────
        with get_db() as conn:
            all_wr = conn.execute("SELECT * FROM waste_tracker WHERE date!=? ORDER BY date DESC, id DESC",
                                  (today,)).fetchall()
        if all_wr:
            hc = card(wrap); hc.pack(fill="both", expand=True, pady=(14,0))
            band(hc, "\U0001f4c5  Previous Waste History")
            HCOLS = [("Date",2),("Item",3),("Qty",1),("Reason",2),("Cost",1),("Del",1)]
            thead(hc, HCOLS, bg=STRIPE, tc=MID)
            hsf = ctk.CTkScrollableFrame(hc, fg_color="transparent", height=200)
            hsf.pack(fill="both", expand=True)
            for ix, w in enumerate(all_wr):
                bg2 = WHITE if ix%2==0 else STRIPE
                rf = ctk.CTkFrame(hsf, fg_color=bg2, corner_radius=0, height=38)
                rf.pack(fill="x"); rf.pack_propagate(False)
                for j,(v,wt) in enumerate(zip(
                        [w["date"],w["item"],f"{w['qty_wasted']:.1f}",w["reason"],
                         f"\u20b9{w['cost_lost']:.0f}"],
                        [2,3,1,2,1])):
                    lbl(rf,v,size=11,color=DARK if j<=1 else MID,
                        weight="bold" if j<=1 else "normal").grid(row=0,column=j,padx=14,sticky="w")
                    rf.grid_columnconfigure(j,weight=wt)
                del_btn = ctk.CTkButton(rf, text="\U0001f5d1", width=28, height=26,
                                        fg_color=STRIPE, hover_color=T_RED,
                                        text_color=RED, corner_radius=6,
                                        font=ctk.CTkFont(size=11),
                                        command=lambda wid=w["id"]: self._del_waste(wid))
                del_btn.grid(row=0,column=5,padx=8,sticky="e")
                rf.grid_columnconfigure(5,weight=1)

    def _save_waste(self):
        try:
            qty  = float(self._wq.get())
            cost = float(self._wc.get())
        except ValueError:
            self._popup("\u26a0\ufe0f Invalid","Numeric values for qty and cost."); return
        raw = self._wi_om.get()
        item = raw.split(" (")[0].strip() if " (" in raw else raw.strip()
        if not item or qty <= 0:
            self._popup("\u26a0\ufe0f Invalid","Select item and enter qty > 0."); return
        with get_db() as conn:
            conn.execute(
                "INSERT INTO waste_tracker (date,item,qty_wasted,reason,cost_lost,recorded_by) "
                "VALUES (?,?,?,?,?,?)",
                (datetime.now().strftime("%Y-%m-%d"), item, qty,
                 self._wr.get(), cost, self._user["name"]))
            if getattr(self, "_waste_deduct", None) and self._waste_deduct.get():
                conn.execute("UPDATE inventory SET stock=stock-? WHERE item=?", (qty, item))
        self._toast(f"\u2705 Waste: {item} ({qty}) \u2014 {self._wr.get()}")
        self._live_refresh("waste")

    def _del_waste(self, wid):
        with get_db() as conn:
            rec = conn.execute("SELECT item, qty_wasted FROM waste_tracker WHERE id=?", (wid,)).fetchone()
            conn.execute("DELETE FROM waste_tracker WHERE id=?", (wid,))
            if rec:
                # Restore deducted stock when waste entry is deleted
                conn.execute("UPDATE inventory SET stock = MIN(stock + ?, opening + received) WHERE item=?",
                             (rec["qty_wasted"], rec["item"]))
        self._go("waste")

    # ==============================================================================
    # DAILY REPORT — date picker + PDF export
    # ==============================================================================
    def _pg_report(self):
        today = datetime.now().strftime("%Y-%m-%d")
        hf = self._hdr("📋  Daily Operations Report",
                       "Select date range  •  Export to PDF")

        # Period toggles
        pbar = ctk.CTkFrame(hf, fg_color="transparent"); pbar.pack(side="right", padx=PAD)
        
        # Custom Range entry
        spec_f = ctk.CTkFrame(pbar, fg_color="transparent")
        spec_f.pack(side="left", padx=(0, 15))
        
        start_entry = ctk.CTkEntry(spec_f, placeholder_text="Start: YYYY-MM-DD", width=115, height=30)
        start_entry.pack(side="left", padx=2)
        lbl(spec_f, "to", size=11, color=MID).pack(side="left", padx=2)
        end_entry = ctk.CTkEntry(spec_f, placeholder_text="End: YYYY-MM-DD", width=115, height=30)
        end_entry.pack(side="left", padx=2)
        
        if getattr(self, "_report_start_date", None):
            start_entry.insert(0, self._report_start_date)
        if getattr(self, "_report_end_date", None):
            end_entry.insert(0, self._report_end_date)
            
        def _set_custom():
            s = start_entry.get().strip()
            e = end_entry.get().strip()
            # If user only fills start, make end same as start for a single day report
            if s and not e: e = s
            if s and e:
                self._report_start_date = s
                self._report_end_date = e
                self._report_period = "custom"
                self._go("report")
        ctk.CTkButton(spec_f, text="View", width=50, height=30, fg_color=GREEN, hover_color=DGREEN,
                      command=_set_custom).pack(side="left", padx=(4,2))

        for code, lbl_t in [("today","Today"),("7d","7 Days"),("30d","Month"),("custom","Custom Range")]:
            ctk.CTkButton(pbar, text=lbl_t, width=80, height=30, corner_radius=8,
                          font=ctk.CTkFont(size=11, weight="bold"),
                          fg_color=SAFFRON if self._report_period==code else STRIPE,
                          text_color=ARMY_BG if self._report_period==code else DARK,
                          hover_color=ARMY_HVR,
                          command=lambda p=code: self._set_rperiod(p)).pack(side="left",padx=2)

        # Reload button
        ctk.CTkButton(pbar, text="🔄", width=36, height=30, corner_radius=8,
                      font=ctk.CTkFont(size=14),
                      fg_color=STRIPE, hover_color=ARMY_HVR, text_color=DARK,
                      command=lambda: self._go("report")).pack(side="left", padx=(6, 0))

        # Compute date range
        if self._report_period == "today":
            start = end = today
        elif self._report_period == "7d":
            start = (datetime.now()-timedelta(days=6)).strftime("%Y-%m-%d"); end = today
        elif self._report_period == "30d":
            start = (datetime.now()-timedelta(days=29)).strftime("%Y-%m-%d"); end = today
        elif self._report_period == "custom":
            start = getattr(self, "_report_start_date", today)
            end = getattr(self, "_report_end_date", today)
        else:
            start = (datetime.now()-timedelta(days=89)).strftime("%Y-%m-%d"); end = today

        # ── Loading spinner (shown while data loads) ─────────────────────────────────
        loading_frame = ctk.CTkFrame(self._area, fg_color="transparent")
        loading_frame.pack(fill="both", expand=True)
        spinner_lbl = lbl(loading_frame, "🔄", size=38, color=ARMY_BG)
        spinner_lbl.pack(expand=True)
        lbl(loading_frame, "Loading report data...", size=13, color=MID).pack()
        self._area.update_idletasks()  # ensure spinner renders before DB fetch

        # Spin animation (rotate through phases)
        _spin_chars = ["◴", "◷", "◶", "◵"]
        _spin_state = [0]
        def _animate_spin():
            if not spinner_lbl.winfo_exists(): return
            spinner_lbl.configure(text=_spin_chars[_spin_state[0] % 4])
            _spin_state[0] += 1
            self._spin_job = self.after(200, _animate_spin)
        _animate_spin()

        def _load_and_render():
            # Cancel spinner
            if hasattr(self, "_spin_job"):
                self.after_cancel(self._spin_job)
            if loading_frame.winfo_exists():
                loading_frame.destroy()
            self._render_report_inner(start, end)


        self.after(60, _load_and_render)

    def _render_report(self, start, end):
        """Separated render so loading frame can flash before DB read."""
        self._render_report_inner(start, end)

    def _render_report_inner(self, start, end):
        MEAL_TYPE_MAP = {"LUNCH": "Lunch", "MINI": "Mini Meal", "PARATHA": "Paratha"}
        with get_db() as conn:
            s_rows = conn.execute("SELECT * FROM sales WHERE date>=? AND date<=? ORDER BY date DESC",
                                  (start,end)).fetchall()
            # Summary for KPI total
            e_sum_rows = conn.execute("SELECT category,SUM(amount) AS t FROM expenditure WHERE date>=? AND date<=? GROUP BY category",
                                  (start,end)).fetchall()
            e_rows = conn.execute("SELECT * FROM expenditure WHERE date>=? AND date<=? ORDER BY date DESC, amount DESC, id DESC",
                                  (start,end)).fetchall()
            w_row  = conn.execute("SELECT COALESCE(SUM(cost_lost),0) AS t FROM waste_tracker WHERE date>=? AND date<=?",
                                  (start,end)).fetchone()
            # Build lookup: (day_name, meal_type) → specific menu name
            sched_name_map = {}
            for row in conn.execute("SELECT dm.day, dm.meal_type, m.name FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
                sched_name_map[(row["day"], row["meal_type"])] = row["name"]

        def _resolve_meal_name(date_str, meal_str):
            """Return specific name like 'Paratha (Aalo Paratha)' if found in daily_menu."""
            import datetime as _dt
            try:
                d = _dt.date.fromisoformat(date_str)
                dow = d.strftime("%A")  # 'Monday', 'Tuesday', …
                mtype = MEAL_TYPE_MAP.get(meal_str.upper())
                if mtype:
                    specific = sched_name_map.get((dow, mtype))
                    if specific:
                        return f"{mtype} ({specific})"
            except Exception:
                pass
            return meal_str

        with get_db() as conn:
            inv_query = """
                SELECT
                    i.item, i.cat, i.unit, i.min_lvl,
                    (SELECT COALESCE(SUM(qty_change), 0) FROM stock_ledger WHERE inv_id = i.id AND date < ?) AS opening,
                    (SELECT COALESCE(SUM(qty_change), 0) FROM stock_ledger WHERE inv_id = i.id AND date >= ? AND date <= ? AND transaction_type = 'Received') AS received,
                    (SELECT COALESCE(SUM(qty_change), 0) FROM stock_ledger WHERE inv_id = i.id AND date <= ?) AS stock
                FROM inventory i
                ORDER BY i.cat, i.item
            """
            inv = conn.execute(inv_query, (start, start, end, end)).fetchall()
            samp_rows = conn.execute(
                "SELECT * FROM samples WHERE date>=? AND date<=? ORDER BY date DESC",
                (start, end)).fetchall()
            # Ingredient-level cost grouped by inventory category (Dry/Fresh/Misc)
            ing_rows = conn.execute("""
                SELECT i.cat, i.item, i.unit, i.cp,
                       ABS(SUM(sl.qty_change)) AS qty_used,
                       ROUND(ABS(SUM(sl.qty_change)) * i.cp, 2) AS item_cost
                FROM stock_ledger sl
                JOIN inventory i ON i.id = sl.inv_id
                WHERE sl.date >= ? AND sl.date <= ? AND sl.qty_change < 0
                GROUP BY i.id, i.cat, i.item, i.unit, i.cp
                HAVING item_cost > 0
                ORDER BY i.cat, item_cost DESC
            """, (start, end)).fetchall()
            # Per-date ingredient usage (for the date-grouped range view)
            ing_by_date_rows = conn.execute("""
                SELECT sl.date, i.cat, i.item, i.unit, i.cp,
                       ABS(SUM(sl.qty_change)) AS qty_used,
                       ROUND(ABS(SUM(sl.qty_change)) * i.cp, 2) AS item_cost
                FROM stock_ledger sl
                JOIN inventory i ON i.id = sl.inv_id
                WHERE sl.date >= ? AND sl.date <= ? AND sl.qty_change < 0
                GROUP BY sl.date, i.id, i.cat, i.item, i.unit, i.cp
                HAVING item_cost > 0
                ORDER BY sl.date DESC, i.cat, item_cost DESC
            """, (start, end)).fetchall()
            gr_rows = conn.execute("""
                SELECT i.cat, i.item, i.unit, 
                       SUM(gr.qty) AS qty_received,
                       SUM(gr.total_cost) AS total_cost
                FROM goods_received gr
                JOIN inventory i ON i.id = gr.inv_id
                WHERE gr.date >= ? AND gr.date <= ?
                GROUP BY i.id, i.cat, i.item, i.unit
                HAVING total_cost > 0
                ORDER BY i.cat, total_cost DESC
            """, (start, end)).fetchall()


        rev   = sum(r["sp"]*r["sold"] for r in s_rows)
        meals = sum(r["sold"] for r in s_rows)
        waste = int(w_row["t"] or 0)
        exp   = sum(r["t"] or 0 for r in e_sum_rows)
        samp_qty  = sum(s["qty"] for s in samp_rows)
        samp_cost = sum(s["cost"] or 0 for s in samp_rows)
        net   = rev - exp - waste
        cash_a = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"]=="Cash")
        upi_a  = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"]=="UPI")
        card_a = sum(r["sp"]*r["sold"] for r in s_rows if r["payment"]=="Card")

        # Group ingredients by inventory category (Dry / Fresh / Misc)
        import collections as _col
        ing_by_cat = _col.OrderedDict()
        for row in ing_rows:
            cat = row["cat"]
            if cat not in ing_by_cat:
                ing_by_cat[cat] = []
            ing_by_cat[cat].append({
                "item": row["item"],
                "unit": row["unit"],
                "qty":  row["qty_used"],
                "cp":   row["cp"],
                "cost": row["item_cost"],
            })

        # Per-date ingredient usage grouped as {date: {cat: [{item, unit, qty, cost}]}}
        ing_by_date = _col.OrderedDict()
        for row in ing_by_date_rows:
            d   = row["date"]
            cat = row["cat"]
            if d not in ing_by_date:
                ing_by_date[d] = _col.OrderedDict()
            if cat not in ing_by_date[d]:
                ing_by_date[d][cat] = []
            ing_by_date[d][cat].append({
                "item": row["item"],
                "unit": row["unit"],
                "qty":  row["qty_used"],
                "cp":   row["cp"],
                "cost": row["item_cost"],
            })

        gr_by_cat = _col.OrderedDict()
        for row in gr_rows:
            cat = row["cat"]
            if cat not in gr_by_cat:
                gr_by_cat[cat] = []
            gr_by_cat[cat].append({
                "item": row["item"],
                "unit": row["unit"],
                "qty":  row["qty_received"],
                "cost": row["total_cost"],
                "rate": row["total_cost"] / row["qty_received"] if row["qty_received"] > 0 else 0
            })

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
        lbl(li,"🇮🇳  AWWA LUNCH PROJECT.. — INDIAN ARMY",size=11,weight="bold",color=GOLD_LT).pack(anchor="w")
        lbl(li,"DAILY OPERATIONS REPORT",size=18,weight="bold",color=WHITE).pack(anchor="w",pady=(2,0))
        lbl(li,f"Period: {start} to {end}",size=10,color=GOLD).pack(anchor="w")

        # KPI cards
        kf = ctk.CTkFrame(rc, fg_color="transparent"); kf.pack(fill="x", padx=PAD, pady=(20,0))
        kf.grid_rowconfigure(0, weight=1)
        for i,(icon,t,v,tc,bg_c,br) in enumerate([
            ("💰","Revenue",f"₹{rev:,.0f}",GREEN,BG_GRN,T_GRN),
            ("🍽","Meals",str(meals),SAFFRON,BG_SAF,T_SAF),
            ("♻️","Waste Cost",f"₹{waste:,.0f}",ORANGE,BG_SAF,T_SAF),
            ("🎁",f"Samples ({samp_qty})",f"₹{samp_cost:,.0f}",TEAL,BG_TEA,T_TEA),
            ("💸","Expenditure",f"₹{exp:,.0f}",PURPLE,BG_PUR,T_PUR),
            ("📈","Net Profit",f"₹{net:,.0f}",net>=0 and BLUE or RED,BG_BLU,T_BLU),
        ]):
            kc = card(kf, fg_color=bg_c, border_color=br)
            kc.grid(row=0,column=i,padx=(0 if i==0 else 10),sticky="nsew")
            kf.grid_columnconfigure(i, weight=1)
            lbl(kc,icon,size=22).pack(anchor="w",padx=16,pady=(12,2))
            lbl(kc,t,size=10,color=MID).pack(anchor="w",padx=16)
            lbl(kc,v,size=17,weight="bold",color=tc).pack(anchor="w",padx=16,pady=(2,12))

        # Meal Sales Table — show specific meal name (e.g. KADHI CHAWAL) from daily_menu
        if start == end:
            self._rept_section(rc, "Meal Sales Summary",
                [("Date",3),("Meal",5),("Sold",1),("Wastage",2),("COGS",2),("Revenue",2),("Payment",2)],
                [[r["date"],
                  _resolve_meal_name(r["date"], r["meal"]),
                  str(r["sold"]),str(r["wastage"]),
                  f"₹{r['cogs']:,.0f}",f"₹{r['sp']*r['sold']:,.0f}",r["payment"]]
                 for r in s_rows],
                [3,5,1,2,2,2,2])
        else:
            # Group sales by date
            import collections as _col
            import datetime as _dt
            sales_by_date = _col.OrderedDict()
            for r in s_rows:
                d = r["date"]
                if d not in sales_by_date:
                    sales_by_date[d] = []
                sales_by_date[d].append(r)

            # Group expenditures by date
            exp_by_date = _col.OrderedDict()
            for r in e_rows:
                d = r["date"]
                if d not in exp_by_date:
                    exp_by_date[d] = []
                exp_by_date[d].append(r)

            # Combine and sort all unique dates descending
            all_dates = sorted(list(set(sales_by_date.keys()) | set(exp_by_date.keys())), reverse=True)

            band(rc, "Operations Summary by Date (Meal Sales & Expenditures)", bg=ARMY_BG, tc=GOLD_LT, h=40)

            if not all_dates:
                band(rc, "No records found for this period", bg=STRIPE, tc=MID, h=36)
            else:
                for date_str in all_dates:
                    day_rows = sales_by_date.get(date_str, [])
                    day_exps = exp_by_date.get(date_str, [])

                    day_sold = sum(r["sold"] for r in day_rows)
                    day_rev = sum(r["sp"] * r["sold"] for r in day_rows)
                    day_exp = sum(e["amount"] for e in day_exps)

                    try:
                        d_obj = _dt.date.fromisoformat(date_str)
                        date_display = d_obj.strftime("%A, %d %b %Y")
                    except Exception:
                        date_display = date_str

                    # Date header sub-band (with day totals on the right)
                    dh = ctk.CTkFrame(rc, fg_color="#253D27", corner_radius=0, height=32)
                    dh.pack(fill="x")
                    dh.pack_propagate(False)
                    ctk.CTkFrame(dh, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
                    lbl(dh, f"  📅  {date_display}", size=11, weight="bold", color=GOLD_LT).pack(side="left", padx=8)

                    # Prepare summary text for the header
                    info_parts = []
                    if day_rows:
                        info_parts.append(f"Sold: {day_sold} (₹{day_rev:,.0f})")
                    if day_exps:
                        info_parts.append(f"Exp: ₹{day_exp:,.0f}")
                    lbl(dh, "  |  ".join(info_parts), size=10, color=SAFFRON).pack(side="right", padx=14)

                    # 1. Render Meal Sales Table
                    if day_rows:
                        thead(rc, [("Meal Item", 8), ("Sold", 1), ("Wastage", 2), ("COGS", 2), ("Revenue", 2), ("Payment", 2)], bg=STRIPE, tc=MID)
                        for ix, r in enumerate(day_rows):
                            trow(rc, [
                                _resolve_meal_name(r["date"], r["meal"]),
                                str(r["sold"]),
                                str(r["wastage"]),
                                f"₹{r['cogs']:,.0f}",
                                f"₹{r['sp']*r['sold']:,.0f}",
                                r["payment"]
                            ], [8,1,2,2,2,2], bg=WHITE if ix % 2 == 0 else STRIPE)

                    # 2. Render Expenditure Table
                    if day_exps:
                        lbl(rc, "   💸  Expenditures:", size=10, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(6,2))
                        thead(rc, [("Category", 3), ("Meal / Batch", 5), ("Amount", 2), ("Notes", 3)], bg=STRIPE, tc=MID)
                        import re as _re
                        for ix, e in enumerate(day_exps):
                            # Parse meal type out of auto-generated notes e.g. "Auto-expenditure for LUNCH batch"
                            raw_note = e["notes"] or ""
                            m = _re.search(r"Auto-expenditure for (\w+) batch", raw_note, _re.IGNORECASE)
                            if m:
                                meal_token = m.group(1).upper()
                                resolved   = _resolve_meal_name(date_str, meal_token)
                                batch_lbl  = resolved
                                note_txt   = "Auto batch"
                            else:
                                batch_lbl = raw_note or "—"
                                note_txt  = ""
                            trow(rc, [
                                e["category"],
                                batch_lbl,
                                f"₹{e['amount']:,.0f}",
                                note_txt or "—"
                            ], [3,5,2,3], bg=WHITE if ix % 2 == 0 else STRIPE)

                    # 3. Ingredients used this day (grouped by category)
                    day_ings = ing_by_date.get(date_str, {})
                    if day_ings:
                        lbl(rc, "   🧂  Ingredients Used:", size=10, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(6,2))
                        for cat_name, items in day_ings.items():
                            # Category sub-header
                            cat_hdr = ctk.CTkFrame(rc, fg_color="#E8F0E8", corner_radius=0, height=22)
                            cat_hdr.pack(fill="x")
                            cat_hdr.pack_propagate(False)
                            ctk.CTkFrame(cat_hdr, fg_color=SAFFRON, width=3, corner_radius=0).pack(side="left", fill="y")
                            cat_total = sum(it["cost"] for it in items)
                            lbl(cat_hdr, f"  {cat_name}", size=9, weight="bold", color=ARMY_BG).pack(side="left", padx=6)
                            lbl(cat_hdr, f"₹{cat_total:,.0f}", size=9, weight="bold", color=ARMY_BG).pack(side="right", padx=10)
                            # Items under this category
                            thead(rc, [("Item", 6), ("Qty Used", 2), ("Unit", 2), ("Rate/Unit", 2), ("Cost", 2)], bg=STRIPE, tc=MID)
                            for jx, it in enumerate(items):
                                trow(rc, [
                                    it["item"],
                                    f"{it['qty']:.2f}",
                                    it["unit"],
                                    f"₹{it['cp']:,.2f}",
                                    f"₹{it['cost']:,.2f}"
                                ], [6,2,2,2,2], bg=WHITE if jx % 2 == 0 else STRIPE)

                    # Small spacer between days
                    ctk.CTkFrame(rc, fg_color="transparent", height=10).pack(fill="x")

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

        # Expenditure — Dry / Fresh / Misc ingredient-level breakdown
        # Cat colours: Dry=SAFFRON, Fresh=TEAL, Misc=PURPLE
        CAT_CLR = {"Dry": ("#FF9933", "#253D27"), "Fresh": (TEAL, "#0E2C2B"),
                   "Misc": (PURPLE, "#1E1733")}
        if ing_by_cat:
            band(rc, "📊  Expenditure Breakdown — Ingredients by Category", bg=ARMY_BG, tc=GOLD_LT, h=40)
            ing_grand_total = sum(i["cost"] for items in ing_by_cat.values() for i in items)
            for cat, items in ing_by_cat.items():
                cat_total = sum(i["cost"] for i in items)
                accent, hdr_bg = CAT_CLR.get(cat, (SAFFRON, "#253D27"))
                # Category sub-header
                ch = ctk.CTkFrame(rc, fg_color=hdr_bg, corner_radius=0, height=34)
                ch.pack(fill="x")
                ch.pack_propagate(False)
                ctk.CTkFrame(ch, fg_color=accent, width=5, corner_radius=0).pack(side="left", fill="y")
                lbl(ch, f"  📂  {cat} Ration", size=12, weight="bold", color="#FFFFFF").pack(side="left", padx=8)
                lbl(ch, f"₹{cat_total:,.0f}", size=12, weight="bold", color=accent).pack(side="right", padx=14)
                # Column header
                thead(rc, [("Ingredient", 5), ("Unit", 2), ("Qty Used", 2), ("Rate/Unit", 2), ("Cost", 2)],
                      bg=STRIPE, tc=MID)
                # Ingredient rows
                for ix, item in enumerate(items):
                    clrs = [DARK, MID, DARK, MID, GREEN]
                    trow(rc,
                         [item["item"],
                          item["unit"],
                          f"{item['qty']:.2f}",
                          f"₹{item['cp']:.2f}",
                          f"₹{item['cost']:,.0f}"],
                         [5, 2, 2, 2, 2],
                         colors=clrs,
                         bg=WHITE if ix % 2 == 0 else STRIPE)
                # Category subtotal bar
                sub_rf = ctk.CTkFrame(rc, fg_color="#E8F5E9", corner_radius=0, height=34)
                sub_rf.pack(fill="x")
                sub_rf.pack_propagate(False)
                uid_sub = abs(hash(cat + "sub"))
                for j, (txt, wt, bold) in enumerate([
                    (f"{cat} Subtotal", 5, True),
                    (f"{len(items)} ingredients", 2, False),
                    ("", 2, False),
                    ("", 2, False),
                    (f"₹{cat_total:,.0f}", 2, True)
                ]):
                    cell = ctk.CTkFrame(sub_rf, fg_color="transparent", corner_radius=0)
                    cell.grid(row=0, column=j, padx=0, pady=0, sticky="nsew")
                    lbl(cell, txt, size=11, weight="bold" if bold else "normal",
                        color=ARMY_BG if bold else MID).pack(anchor="w", padx=8, pady=8)
                    cell.grid_columnconfigure(0, weight=1)
                    sub_rf.grid_columnconfigure(j, weight=wt, uniform=f"grp_{uid_sub}")
                sub_rf.grid_rowconfigure(0, weight=1)
            # Grand total footer
            gt_f = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=44)
            gt_f.pack(fill="x")
            gt_f.pack_propagate(False)
            lbl(gt_f, "  💸  Grand Total — All Ingredients", size=12, weight="bold", color=GOLD_LT).pack(side="left", padx=14)
            lbl(gt_f, f"₹{ing_grand_total:,.0f}", size=15, weight="bold", color=SAFFRON).pack(side="right", padx=16)
        # Inventory Purchases Breakdown
        if gr_by_cat:
            band(rc, "📦  Inventory Purchases Breakdown — Goods Received", bg=ARMY_BG, tc=GOLD_LT, h=40)
            gr_grand_total = sum(i["cost"] for items in gr_by_cat.values() for i in items)
            for cat, items in gr_by_cat.items():
                cat_total = sum(i["cost"] for i in items)
                accent, hdr_bg = CAT_CLR.get(cat, (SAFFRON, "#253D27"))
                # Category sub-header
                ch = ctk.CTkFrame(rc, fg_color=hdr_bg, corner_radius=0, height=34)
                ch.pack(fill="x")
                ch.pack_propagate(False)
                ctk.CTkFrame(ch, fg_color=accent, width=5, corner_radius=0).pack(side="left", fill="y")
                lbl(ch, f"  📂  {cat} Purchases", size=12, weight="bold", color="#FFFFFF").pack(side="left", padx=8)
                lbl(ch, f"₹{cat_total:,.0f}", size=12, weight="bold", color=accent).pack(side="right", padx=14)
                # Column header
                thead(rc, [("Item Name", 5), ("Unit", 2), ("Qty Received", 2), ("Rate/Unit", 2), ("Total Cost", 2)],
                      bg=STRIPE, tc=MID)
                # Rows
                for ix, item in enumerate(items):
                    clrs = [DARK, MID, DARK, MID, GREEN]
                    trow(rc,
                         [item["item"],
                          item["unit"],
                          f"{item['qty']:.2f}",
                          f"₹{item['rate']:.2f}",
                          f"₹{item['cost']:,.0f}"],
                         [5, 2, 2, 2, 2],
                         colors=clrs,
                         bg=WHITE if ix % 2 == 0 else STRIPE)
                # Category subtotal bar
                sub_rf = ctk.CTkFrame(rc, fg_color="#E8F5E9", corner_radius=0, height=34)
                sub_rf.pack(fill="x")
                sub_rf.pack_propagate(False)
                uid_sub = abs(hash(cat + "gr_sub"))
                for j, (txt, wt, bold) in enumerate([
                    (f"{cat} Purchases Subtotal", 5, True),
                    (f"{len(items)} items", 2, False),
                    ("", 2, False),
                    ("", 2, False),
                    (f"₹{cat_total:,.0f}", 2, True)
                ]):
                    cell = ctk.CTkFrame(sub_rf, fg_color="transparent", corner_radius=0)
                    cell.grid(row=0, column=j, padx=0, pady=0, sticky="nsew")
                    lbl(cell, txt, size=11, weight="bold" if bold else "normal",
                        color=ARMY_BG if bold else MID).pack(anchor="w", padx=8, pady=8)
                    cell.grid_columnconfigure(0, weight=1)
                    sub_rf.grid_columnconfigure(j, weight=wt, uniform=f"grp_{uid_sub}")
                sub_rf.grid_rowconfigure(0, weight=1)
            # Grand total footer
            gt_f = ctk.CTkFrame(rc, fg_color=ARMY_BG, corner_radius=0, height=44)
            gt_f.pack(fill="x")
            gt_f.pack_propagate(False)
            lbl(gt_f, "  📦  Grand Total — All Purchases", size=12, weight="bold", color=GOLD_LT).pack(side="left", padx=14)
            lbl(gt_f, f"₹{gr_grand_total:,.0f}", size=15, weight="bold", color=SAFFRON).pack(side="right", padx=16)

        if e_sum_rows:
            self._rept_section(rc, "Expenditure Summary",
                [("Category", 4), ("Amount", 2)],
                [[r["category"], f"₹{r['t']:,.0f}"] for r in e_sum_rows],
                [4, 2])

        # Samples section
        if samp_rows:
            self._rept_section(rc, "🎁  Sample Complimentary",
                [("Date",3),("Item",5),("Qty",1),("Rate ₹",2),("Cost ₹",2),("Given To",3)],
                [[s["date"],_resolve_meal_name(s["date"], s["meal"]),str(s["qty"]),
                  f"₹{s['sp']:.0f}",f"₹{s['cost']:,.0f}",s["given_to"] or "General"]
                 for s in samp_rows],
                [3,5,1,2,2,3])
        else:
            band(rc, "🎁  Sample Complimentary — None for this period", bg=STRIPE, tc=MID, h=36)

        # Inventory closing stock
        self._rept_section(rc,"Inventory Closing Stock",
            [("Item",4),("Category",2),("Unit",2),("Opening",2),("Received",2),("Stock",2),("Status",2)],
            [[i["item"],i["cat"],i["unit"],f"{i['opening']:.1f}",f"{i['received']:.1f}",
              f"{i['stock']:.1f}","⚠ LOW" if i["stock"]<i["min_lvl"] else "✓ OK"]
             for i in inv],
            [4,2,2,2,2,2,2])

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

        # Save reports to the user's Documents folder (always writable on Windows)
        # Creates subfolder: Documents\AWWA Canteen Reports\
        docs_dir = os.path.join(os.path.expanduser("~"), "Documents", "AWWA Canteen Reports")
        os.makedirs(docs_dir, exist_ok=True)
        out = os.path.join(docs_dir, fname)

        with get_db() as conn:
            s_rows = conn.execute("SELECT * FROM sales WHERE date>=? AND date<=? ORDER BY date DESC",
                                  (start,end)).fetchall()
            e_rows = conn.execute("SELECT * FROM expenditure WHERE date>=? AND date<=? ORDER BY date DESC, amount DESC, id DESC",
                                  (start,end)).fetchall()
            w_rows = conn.execute("SELECT * FROM waste_tracker WHERE date>=? AND date<=?",
                                  (start,end)).fetchall()
            inv_query = """
                SELECT 
                    i.item, i.cat, i.unit, i.min_lvl,
                    (SELECT COALESCE(SUM(qty_change), 0) FROM stock_ledger WHERE inv_id = i.id AND date < ?) AS opening,
                    (SELECT COALESCE(SUM(qty_change), 0) FROM stock_ledger WHERE inv_id = i.id AND date >= ? AND date <= ? AND transaction_type = 'Received') AS received,
                    (SELECT COALESCE(SUM(qty_change), 0) FROM stock_ledger WHERE inv_id = i.id AND date <= ?) AS stock
                FROM inventory i
                ORDER BY i.cat, i.item
            """
            inv = conn.execute(inv_query, (start, start, end, end)).fetchall()
            sched_name_map = {}
            for row in conn.execute("SELECT dm.day, dm.meal_type, m.name FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
                sched_name_map[(row["day"], row["meal_type"])] = row["name"]
            gr_rows = conn.execute("""
                SELECT i.cat, i.item, i.unit, 
                       SUM(gr.qty) AS qty_received,
                       SUM(gr.total_cost) AS total_cost
                FROM goods_received gr
                JOIN inventory i ON i.id = gr.inv_id
                WHERE gr.date >= ? AND gr.date <= ?
                GROUP BY i.id, i.cat, i.item, i.unit
                HAVING total_cost > 0
                ORDER BY i.cat, total_cost DESC
            """, (start, end)).fetchall()
            # Per-date ingredient usage for range-view PDF
            ing_by_date_rows = conn.execute("""
                SELECT sl.date, i.cat, i.item, i.unit, i.cp,
                       ABS(SUM(sl.qty_change)) AS qty_used,
                       ROUND(ABS(SUM(sl.qty_change)) * i.cp, 2) AS item_cost
                FROM stock_ledger sl
                JOIN inventory i ON i.id = sl.inv_id
                WHERE sl.date >= ? AND sl.date <= ? AND sl.qty_change < 0
                GROUP BY sl.date, i.id, i.cat, i.item, i.unit, i.cp
                HAVING item_cost > 0
                ORDER BY sl.date DESC, i.cat, item_cost DESC
            """, (start, end)).fetchall()

        MEAL_TYPE_MAP = {"LUNCH": "Lunch", "MINI": "Mini Meal", "PARATHA": "Paratha"}
        def _resolve_meal_name(date_str, meal_str):
            import datetime as _dt
            try:
                d = _dt.date.fromisoformat(date_str)
                dow = d.strftime("%A")
                mtype = MEAL_TYPE_MAP.get(meal_str.upper())
                if mtype:
                    specific = sched_name_map.get((dow, mtype))
                    if specific:
                        return f"{mtype} ({specific})"
            except Exception:
                pass
            return meal_str

        rev    = sum(r["sp"]*r["sold"] for r in s_rows)
        meals  = sum(r["sold"] for r in s_rows)
        waste  = sum(w["cost_lost"] or 0 for w in w_rows)
        exp    = sum(r["amount"] for r in e_rows)
        net    = rev - exp - waste   # matches dashboard: Revenue - Expenditure - WasteCost

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
        lh_data = [[Paragraph("🇮🇳  INDIAN ARMY — AWWA LUNCH PROJECT..", TITLE)]]
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
             Paragraph("Expenditure",   TH), Paragraph(f"₹ {exp:,.0f}", TD),
             Paragraph("Net Profit",    TH), Paragraph(f"₹ {net:,.0f}",  TD)],
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
            if start == end:
                story.append(pdf_table(
                    ["Date","Meal Item","Sold","Wastage","Rate","Revenue","Payment"],
                    [[r["date"],_resolve_meal_name(r["date"], r["meal"]),str(r["sold"]),str(r["wastage"]),
                      f"Rs.{r['sp']:.0f}",f"Rs.{r['sp']*r['sold']:,.0f}",r["payment"]]
                     for r in s_rows],
                    [2*cm, 5*cm, 1.5*cm, 2*cm, 1.5*cm, 2.5*cm, 2*cm]))
            else:
                # Group sales by date
                import collections as _col
                import datetime as _dt
                sales_by_date = _col.OrderedDict()
                for r in s_rows:
                    d = r["date"]
                    if d not in sales_by_date:
                        sales_by_date[d] = []
                    sales_by_date[d].append(r)

                # Group expenditures by date
                exp_by_date = _col.OrderedDict()
                for r in e_rows:
                    d = r["date"]
                    if d not in exp_by_date:
                        exp_by_date[d] = []
                    exp_by_date[d].append(r)

                # Combine and sort all unique dates descending
                all_dates = sorted(list(set(sales_by_date.keys()) | set(exp_by_date.keys())), reverse=True)

                DATE_SUBHDR = S("DS", fontName="Helvetica-Bold", fontSize=9, textColor=OliveGreen)
                for date_str in all_dates:
                    day_rows = sales_by_date.get(date_str, [])
                    day_exps = exp_by_date.get(date_str, [])

                    day_sold = sum(r["sold"] for r in day_rows)
                    day_rev = sum(r["sp"] * r["sold"] for r in day_rows)
                    day_exp = sum(e["amount"] for e in day_exps)

                    try:
                        d_obj = _dt.date.fromisoformat(date_str)
                        date_display = d_obj.strftime("%A, %d %b %Y")
                    except Exception:
                        date_display = date_str

                    # Header text
                    info_text = []
                    if day_rows:
                        info_text.append(f"Sold: {day_sold} (Rs.{day_rev:,.0f})")
                    if day_exps:
                        info_text.append(f"Exp: Rs.{day_exp:,.0f}")

                    story.append(Paragraph(f"📅 {date_display}  ({ ' | '.join(info_text) })", DATE_SUBHDR))
                    story.append(Spacer(1, 0.1*cm))

                    # 1. Meal Sales Table
                    if day_rows:
                        story.append(pdf_table(
                            ["Meal Item", "Sold", "Wastage", "Rate", "Revenue", "Payment"],
                            [[_resolve_meal_name(r["date"], r["meal"]), str(r["sold"]), str(r["wastage"]),
                              f"Rs.{r['sp']:.0f}", f"Rs.{r['sp']*r['sold']:,.0f}", r["payment"]]
                             for r in day_rows],
                            [7*cm, 1.5*cm, 2*cm, 1.5*cm, 2.5*cm, 2*cm]))
                        story.append(Spacer(1, 0.15*cm))

                    # 2. Expenditure Table
                    if day_exps:
                        story.append(Paragraph("Expenditures:", S("ES_SUB", fontName="Helvetica-Bold", fontSize=8, textColor=OliveGreen)))
                        story.append(Spacer(1, 0.05*cm))
                        import re as _re
                        exp_data = []
                        for e in day_exps:
                            raw_note = e["notes"] or ""
                            m2 = _re.search(r"Auto-expenditure for (\w+) batch", raw_note, _re.IGNORECASE)
                            if m2:
                                meal_token = m2.group(1).upper()
                                batch_lbl  = _resolve_meal_name(date_str, meal_token)
                                note_txt   = "Auto batch"
                            else:
                                batch_lbl = raw_note or "—"
                                note_txt  = raw_note or "—"
                            exp_data.append([e["category"], batch_lbl, f"Rs.{e['amount']:,.0f}", note_txt])
                        story.append(pdf_table(
                            ["Category", "Meal / Batch", "Amount", "Notes"],
                            exp_data,
                            [3*cm, 6*cm, 2.5*cm, 5*cm]))
                        story.append(Spacer(1, 0.15*cm))

                    # 3. Ingredients used this day (per-date, by category)
                    day_ings = ing_by_date.get(date_str, {})
                    if day_ings:
                        ING_SUB = S("ING_SUB", fontName="Helvetica-Bold", fontSize=8, textColor=OliveGreen)
                        story.append(Paragraph("Ingredients Used:", ING_SUB))
                        story.append(Spacer(1, 0.05*cm))
                        for cat_name, items in day_ings.items():
                            cat_total = sum(it["cost"] for it in items)
                            story.append(Paragraph(
                                f"  {cat_name}  (Rs.{cat_total:,.0f})",
                                S("IC", fontName="Helvetica-Bold", fontSize=7.5, textColor=OliveGreen)
                            ))
                            story.append(Spacer(1, 0.03*cm))
                            story.append(pdf_table(
                                ["Item", "Qty Used", "Unit", "Rate/Unit", "Cost"],
                                [[it["item"], f"{it['qty']:.2f}", it["unit"],
                                  f"Rs.{it['cp']:,.2f}", f"Rs.{it['cost']:,.2f}"]
                                 for it in items],
                                [6*cm, 2*cm, 2*cm, 2.5*cm, 2.5*cm]))
                            story.append(Spacer(1, 0.1*cm))

                    story.append(Spacer(1, 0.25*cm))
        else:
            story.append(Paragraph("No sales recorded for this period.", BODY))
        story.append(Spacer(1, 0.5*cm))

        # Expenditure - show global list only for single day report (since range groups them under date)
        if start == end:
            story.append(Paragraph("Expenditure", SEC)); story.append(Spacer(1, 0.15*cm))
            if e_rows:
                story.append(pdf_table(
                    ["Date","Category","Amount","Notes"],
                    [[r["date"],r["category"],f"Rs.{r['amount']:,.0f}",r["notes"] or "—"] for r in e_rows],
                    [2*cm, 5*cm, 2.5*cm, 7*cm]))
            else:
                story.append(Paragraph("No expenditure recorded.", BODY))
            story.append(Spacer(1, 0.5*cm))

        # Build gr_by_cat for PDF
        import collections as _col
        gr_by_cat = _col.OrderedDict()
        for row in gr_rows:
            cat = row["cat"]
            if cat not in gr_by_cat:
                gr_by_cat[cat] = []
            gr_by_cat[cat].append({
                "item": row["item"],
                "unit": row["unit"],
                "qty":  row["qty_received"],
                "cost": row["total_cost"],
                "rate": row["total_cost"] / row["qty_received"] if row["qty_received"] > 0 else 0
            })

        # Build ing_by_date for PDF
        ing_by_date = _col.OrderedDict()
        for row in ing_by_date_rows:
            d   = row["date"]
            cat = row["cat"]
            if d not in ing_by_date:
                ing_by_date[d] = _col.OrderedDict()
            if cat not in ing_by_date[d]:
                ing_by_date[d][cat] = []
            ing_by_date[d][cat].append({
                "item": row["item"],
                "unit": row["unit"],
                "qty":  row["qty_used"],
                "cp":   row["cp"],
                "cost": row["item_cost"],
            })

        # Inventory Purchases Breakdown in PDF
        story.append(Paragraph("Inventory Purchases Breakdown", SEC)); story.append(Spacer(1, 0.15*cm))
        if gr_rows:
            GR_SUBHDR = S("GRS", fontName="Helvetica-Bold", fontSize=9, textColor=OliveGreen)
            for cat, items in gr_by_cat.items():
                cat_total = sum(i["cost"] for i in items)
                story.append(Paragraph(f"📂 {cat} Purchases (Subtotal: Rs.{cat_total:,.0f})", GR_SUBHDR))
                story.append(Spacer(1, 0.08*cm))
                story.append(pdf_table(
                    ["Item Name", "Unit", "Qty Received", "Rate/Unit", "Total Cost"],
                    [[item["item"], item["unit"], f"{item['qty']:.1f}", f"Rs.{item['rate']:.2f}", f"Rs.{item['cost']:,.0f}"]
                     for item in items],
                    [6.5*cm, 1.5*cm, 2.5*cm, 3*cm, 3*cm]))
                story.append(Spacer(1, 0.25*cm))
        else:
            story.append(Paragraph("No inventory purchases recorded for this period.", BODY))
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
                "INDIAN ARMY  |  AWWA LUNCH PROJECT..  |  CONFIDENTIAL")
            canv.drawRightString(W_A4 - 1*cm, 0.22*cm, f"Page {doc.page}")
            canv.restoreState()

        doc = SimpleDocTemplate(out, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=1.5*cm)
        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

        self._popup("✅ PDF Exported!",
                    f"Report saved to:\n{out}\n\n"
                    f"(Documents → AWWA Canteen Reports)")
        # Auto-open the PDF using the correct command for the platform
        try:
            if sys.platform == "win32":
                os.startfile(out)                                    # Windows
            elif sys.platform == "darwin":
                import subprocess; subprocess.Popen(["open", out])  # macOS
            else:
                import subprocess; subprocess.Popen(["xdg-open", out])  # Linux
        except Exception:
            pass

    def _filter_batch_cards(self):
        q = self._batch_search.get().lower() if hasattr(self, "_batch_search") else ""
        for name, w in self._batch_cards:
            if q in name: w.grid()
            else: w.grid_remove()

    def _debounce(self, job_attr, fn, delay_ms=250):
        """Cancel any pending call stored in job_attr and schedule fn after delay_ms."""
        existing = getattr(self, job_attr, None)
        if existing:
            try:
                self.after_cancel(existing)
            except Exception:
                pass
        setattr(self, job_attr, self.after(delay_ms, fn))

    def _inv_filter_search(self):
        if not hasattr(self, "_inv_sf") or not hasattr(self, "_inv_hdr"): return
        q = self._inv_search.get().strip().lower() if hasattr(self, "_inv_search") else ""
        # Use in-memory cache for instant filtering; no DB hit needed
        self._inv_loadrows(search_q=q, reload_db=False)

    # ==============================================================================
    # MASTER DATA — Menu + Inventory tabs
    # ==============================================================================
    # ==============================================================================
    # MASTER DATA — tabbed: Menu | Daily Schedule | Users  (all in-app modals)
    # ==============================================================================
    def _pg_master(self):
        self._hdr("🧾  Master Data", "Menu • Daily Schedule • Users — all managed here")
        self._master_tab = getattr(self, "_master_tab", "menu")

        # ── Pill tab bar ──────────────────────────────────────────────────────
        tbar = ctk.CTkFrame(self._area, fg_color=WHITE, corner_radius=0,
                             height=52, border_width=1, border_color=BORDER)
        tbar.pack(fill="x", padx=PAD, pady=(10,0))
        tbar.pack_propagate(False)
        self._mtabs = {}
        tabs = [
            ("menu",     "🍽  Menu Items"),
            ("schedule", "📅  Daily Schedule"),
            ("users",    "👤  Users & Roles"),
        ]
        for code, label in tabs:
            active = code == self._master_tab
            b = ctk.CTkButton(
                tbar, text=label, height=38, corner_radius=0,
                fg_color=SAFFRON if active else "transparent",
                text_color=ARMY_BG if active else DARK,
                hover_color=STRIPE,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda c=code: self._switch_master_tab(c))
            b.pack(side="left", padx=0)
            self._mtabs[code] = b

        self._mwrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        self._mwrap.pack(fill="both", expand=True, padx=PAD, pady=(10, PAD))
        self._render_master_content()

    def _switch_master_tab(self, tab):
        self._master_tab = tab
        for c, b in self._mtabs.items():
            b.configure(fg_color=SAFFRON if c==tab else "transparent",
                        text_color=ARMY_BG if c==tab else DARK)
        for w in self._mwrap.winfo_children(): w.destroy()
        self._render_master_content()

    def _render_master_content(self):
        t = self._master_tab
        if t == "menu":       self._master_menu(self._mwrap)
        elif t == "schedule": self._master_schedule(self._mwrap)
        elif t == "users":    self._master_users(self._mwrap)

    # ── Menu Items tab ────────────────────────────────────────────────────────
    def _master_menu(self, wrap):
        """Menu Items tab with search + day filter."""
        DAYS_FILTER = ["All Days","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        # ── Filter bar ───────────────────────────────────────────────────────
        fb = ctk.CTkFrame(wrap, fg_color="transparent"); fb.pack(fill="x", pady=(0,8))
        lbl(fb, "🔍", size=14).pack(side="left", padx=(0,4))
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(fb, textvariable=search_var, placeholder_text="Search menu items…",
                                    width=220, height=34, font=ctk.CTkFont(size=12))
        search_entry.pack(side="left", padx=(0,10))
        day_filter_var = ctk.StringVar(value="All Days")
        day_opt = ctk.CTkOptionMenu(fb, variable=day_filter_var, values=DAYS_FILTER,
                                     width=140, height=34, font=ctk.CTkFont(size=12))
        day_opt.pack(side="left")
        lbl(fb, "📅 Day:", size=11, color=MID).pack(side="left", padx=(8,4))

        mc = card(wrap); mc.pack(fill="x", pady=(0,14))

        # Header band with Add button
        hband = band(mc, "🍽  Menu Master  •  Active Items")
        btn(hband, "＋  Add Item", self._modal_add_menu,
            fg=GREEN, hv=DGREEN, h=30, w=130).pack(side="right", padx=12)

        # Column headers
        hdr = ctk.CTkFrame(mc, fg_color=STRIPE, corner_radius=0, height=32)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        for col, w in [("Menu Item", 260), ("Type", 90), ("Day", 90), ("Price ₹", 70),
                       ("Cost / Profit / Waste", 185), ("Status", 70), ("Actions", 0)]:
            lbl(hdr, col, size=10, weight="bold", color=MID).pack(
                side="left", padx=10, pady=6)
            if w > 0:
                ctk.CTkFrame(hdr, fg_color="transparent", width=max(0, w - 90)
                             ).pack(side="left")

        # Rows — query menu with per-item cogs, wastage from waste_tracker
        with get_db() as conn:
            menus = conn.execute("SELECT * FROM menu ORDER BY active DESC, name").fetchall()
            # Sum wastage cost per menu item
            waste_map = {}
            for wr in conn.execute(
                "SELECT wt.reason, SUM(wt.cost_lost) as total_wc "
                "FROM waste_tracker wt GROUP BY wt.reason"
            ).fetchall():
                for prefix in ("Production waste - ", "Batch update - "):
                    if wr["reason"] and wr["reason"].startswith(prefix):
                        nm = wr["reason"][len(prefix):]
                        waste_map[nm] = waste_map.get(nm, 0) + (wr["total_wc"] or 0)
            # Build type & day lookup from daily_menu
            menu_type_map = {}   # menu_name → meal_type
            menu_day_map  = {}   # menu_name → list of days
            for row in conn.execute(
                "SELECT dm.meal_type, dm.day, m.name "
                "FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"):
                menu_type_map[row["name"]] = row["meal_type"]
                menu_day_map.setdefault(row["name"], []).append(row["day"])

        # ── filter + render rows ─────────────────────────────────────────────
        def render_rows(*_):
            # Remove old rows (but keep header)
            for child in list(mc.winfo_children()):
                if getattr(child, "_is_menu_row", False):
                    child.destroy()
            q   = search_var.get().strip().lower()
            day = day_filter_var.get()
            ix  = 0
            for m in menus:
                name = m["name"]
                # Apply search filter
                if q and q not in name.lower():
                    continue
                # Apply day filter
                if day != "All Days":
                    days_for_item = menu_day_map.get(name, [])
                    if day not in days_for_item:
                        continue

                bg2 = WHITE if ix % 2 == 0 else STRIPE
                is_thali = any(x in name for x in ["THALI","BIRYANI","RICE","Thali","Biryani","Rice"])
                icon = "🍱" if is_thali else "🍽"

                rf = ctk.CTkFrame(mc, fg_color=bg2, corner_radius=0, height=52)
                rf._is_menu_row = True
                rf.pack(fill="x"); rf.pack_propagate(False)

                # Name
                name_f = ctk.CTkFrame(rf, fg_color="transparent", width=260)
                name_f.pack(side="left", fill="y", padx=(10,0))
                name_f.pack_propagate(False)
                lbl(name_f, f"{icon}  {name}", size=11, weight="bold",
                    color=DARK if m["active"] else MID).pack(side="left", anchor="w", pady=4)

                # Type — from daily_menu; fallback to price heuristic
                mtype = menu_type_map.get(name)
                if not mtype:
                    if m["sp"] >= 70:   mtype = "Lunch"
                    elif m["sp"] >= 40: mtype = "Paratha"
                    else:               mtype = "Mini Meal"
                type_color = {"Lunch": BLUE, "Paratha": ORANGE, "Mini Meal": TEAL}.get(mtype, MID)
                cat_f = ctk.CTkFrame(rf, fg_color="transparent", width=90)
                cat_f.pack(side="left", fill="y"); cat_f.pack_propagate(False)
                lbl(cat_f, mtype, size=10, weight="bold", color=type_color).pack(anchor="w", pady=4)

                # Day
                day_f = ctk.CTkFrame(rf, fg_color="transparent", width=90)
                day_f.pack(side="left", fill="y"); day_f.pack_propagate(False)
                days_str = ", ".join(d[:3] for d in menu_day_map.get(name, []))
                lbl(day_f, days_str or "—", size=9, color=MID).pack(anchor="w", pady=4)

                # Price
                pr_f = ctk.CTkFrame(rf, fg_color="transparent", width=70)
                pr_f.pack(side="left", fill="y"); pr_f.pack_propagate(False)
                lbl(pr_f, f"₹{m['sp']:.0f}", size=12, weight="bold",
                    color=GREEN if m["active"] else MID).pack(anchor="w", pady=4)

                # Cost / Profit
                cogs_val   = m["cogs"] if m["cogs"] else 0.0
                profit_v   = m["sp"] - cogs_val
                margin_pct = (profit_v / m["sp"] * 100) if m["sp"] > 0 else 0
                wc_val     = waste_map.get(name, 0.0)
                pf_f = ctk.CTkFrame(rf, fg_color="transparent", width=185)
                pf_f.pack(side="left", fill="y"); pf_f.pack_propagate(False)
                if cogs_val > 0:
                    profit_color = GREEN if profit_v > 0 else RED
                    lbl(pf_f, f"Cost ₹{cogs_val:.1f}  |  Profit ₹{profit_v:.1f} ({margin_pct:.0f}%)",
                        size=9, weight="bold", color=profit_color).pack(anchor="w", pady=(2,0))
                    lbl(pf_f, f"Waste ₹{wc_val:.1f}",
                        size=9, color=ORANGE).pack(anchor="w", pady=(0,2))
                else:
                    lbl(pf_f, "No cost data", size=9, color=MID).pack(anchor="w", pady=4)

                # Status
                ac_f = ctk.CTkFrame(rf, fg_color="transparent", width=70)
                ac_f.pack(side="left", fill="y"); ac_f.pack_propagate(False)
                lbl(ac_f, "✓ Active" if m["active"] else "✗ Off", size=10, weight="bold",
                    color=GREEN if m["active"] else RED).pack(anchor="w", pady=4)

                # Actions
                af = ctk.CTkFrame(rf, fg_color="transparent")
                af.pack(side="right", padx=(0, 8), fill="y")
                ctk.CTkButton(af, text="🗑", width=30, height=28, corner_radius=6,
                              fg_color="#FEE2E2", hover_color="#FECACA", text_color=RED,
                              font=ctk.CTkFont(size=13),
                              command=lambda mid=m["id"],nm=name: self._delete_menu_item(mid, nm)
                              ).pack(side="right", padx=(4,0))
                tog_txt = "Deactivate" if m["active"] else "Activate"
                tog_clr = ORANGE if m["active"] else GREEN
                ctk.CTkButton(af, text=tog_txt, width=84, height=28, corner_radius=6,
                              fg_color=tog_clr,
                              hover_color=DGREEN if not m["active"] else "#EA580C",
                              text_color=WHITE, font=ctk.CTkFont(size=10, weight="bold"),
                              command=lambda mid=m["id"],ac=m["active"]:
                                  self._toggle_menu_item(mid, not ac)
                              ).pack(side="right", padx=(4,0))
                ctk.CTkButton(af, text="✏️", width=30, height=28, corner_radius=6,
                              fg_color=BG_BLU, hover_color=T_BLU, text_color=BLUE,
                              font=ctk.CTkFont(size=13),
                              command=lambda mid=m["id"],nm=name,sp=m["sp"],ac=m["active"]:
                                  self._modal_edit_menu(mid, nm, sp, ac)
                              ).pack(side="right", padx=(4,0))
                ctk.CTkButton(af, text="🔄", width=30, height=28, corner_radius=6,
                              fg_color="#FEF3C7", hover_color="#FDE68A", text_color="#92400E",
                              font=ctk.CTkFont(size=13),
                              command=lambda mid=m["id"],nm=name:
                                  self._modal_update_batch(mid, nm)
                              ).pack(side="right", padx=(4,0))
                ctk.CTkButton(af, text="🥗", width=30, height=28, corner_radius=6,
                              fg_color=BG_GRN, hover_color=T_GRN, text_color=GREEN,
                              font=ctk.CTkFont(size=13),
                              command=lambda mid=m["id"],nm=name:
                                  self._modal_edit_ingredients(mid, nm)
                              ).pack(side="right", padx=(4,0))
                ix += 1

        search_var.trace_add("write", render_rows)
        day_filter_var.trace_add("write", render_rows)
        render_rows()  # initial render



    def _delete_menu_item(self, menu_id, name):
        if self._confirm(
                "Delete Menu Item",
                f"Permanently delete '{name}'?\n\nThis will also remove all linked recipes."):
            with get_db() as conn:
                conn.execute("DELETE FROM recipes WHERE menu_id=?", (menu_id,))
                conn.execute("DELETE FROM batch_prep WHERE menu_id=?", (menu_id,))
                conn.execute("DELETE FROM sales WHERE menu_id=?", (menu_id,))
                conn.execute("DELETE FROM daily_menu WHERE menu_id=?", (menu_id,))
                conn.execute("DELETE FROM menu WHERE id=?", (menu_id,))
            self._toast(f"🗑  Deleted '{name}'")
            self._switch_master_tab("menu")

    def _toggle_menu_item(self, menu_id, new_active):
        with get_db() as conn:
            conn.execute("UPDATE menu SET active=? WHERE id=?", (1 if new_active else 0, menu_id))
        self._switch_master_tab("menu")

    def _modal_add_menu(self):
        """
        3-Step Wizard:
          Step 1  Menu item name
          Step 2  Per ingredient: Total Raw | Total Made | Total Waste | Serving per Plate
                  -> live cost per piece AND cost per plate
          Step 3  Selling price review + save
                  Saves: menu, recipes (qty_per_unit = per-plate), batch_prep,
                         waste_tracker, deducts inventory stock
        """
        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            inv_data = {r["item"]: {"cp": r["cp"], "stock": r["stock"], "unit": r["unit"]}
                        for r in conn.execute("SELECT item,cp,stock,unit FROM inventory ORDER BY item")}
        inv_items = sorted(inv_data.keys())

        wizard_step          = [1]
        ing_rows             = []
        snapshot_rows        = []   # plain dicts captured before widgets are cleared
        menu_name            = [""]
        total_cost_per_piece = [0.0]
        total_cost_per_plate = [0.0]
        batch_portions       = [0]

        overlay = tk.Frame(self._area, bg="#1E293B")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        modal_card = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                                  border_width=2, border_color=ARMY_BG, width=860, height=640)
        modal_card.place(relx=0.5, rely=0.5, anchor="center")
        modal_card.pack_propagate(False)

        hbar = ctk.CTkFrame(modal_card, fg_color=ARMY_BG, corner_radius=0, height=54)
        hbar.pack(fill="x", side="top"); hbar.pack_propagate(False)
        ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
        title_lbl = lbl(hbar, "  New Menu Item  Step 1 of 3", size=13, weight="bold", color=WHITE)
        title_lbl.pack(side="left", padx=10)
        ctk.CTkButton(hbar, text="X", width=34, height=34, corner_radius=8,
                      fg_color="transparent", hover_color=ARMY_HVR, text_color=GOLD_LT,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=lambda: overlay.destroy()).pack(side="right", padx=10)

        dot_bar = ctk.CTkFrame(modal_card, fg_color=STRIPE, corner_radius=0, height=36)
        dot_bar.pack(fill="x", side="top"); dot_bar.pack_propagate(False)
        step_labels = ["1 Name", "2 Raw/Made/Waste/Serving", "3 Price & Save"]
        dot_lbls = []
        inner_dot = ctk.CTkFrame(dot_bar, fg_color="transparent"); inner_dot.pack(expand=True)
        for i, sl in enumerate(step_labels):
            dl = lbl(inner_dot, sl, size=11, weight="bold", color=SAFFRON if i == 0 else MID)
            dl.pack(side="left", padx=12); dot_lbls.append(dl)

        # Footer packed BEFORE content so it always stays visible at bottom
        foot = ctk.CTkFrame(modal_card, fg_color=WHITE, border_width=1,
                            border_color=BORDER, corner_radius=0, height=60)
        foot.pack(fill="x", side="bottom"); foot.pack_propagate(False)
        # Content expands to fill remaining space between header and footer
        content = ctk.CTkFrame(modal_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        def _dots():
            s = wizard_step[0]
            for i, dl in enumerate(dot_lbls):
                if   i+1 == s: dl.configure(text_color=SAFFRON, font=ctk.CTkFont(size=11, weight="bold"))
                elif i+1  < s: dl.configure(text_color=GREEN,   font=ctk.CTkFont(size=11, weight="bold"))
                else:          dl.configure(text_color=MID,     font=ctk.CTkFont(size=11, weight="normal"))

        def _clear():
            for w in content.winfo_children(): w.destroy()
            for w in foot.winfo_children():    w.destroy()

        # ── STEP 1 ──────────────────────────────────────────────────────────
        def _step1():
            _clear(); wizard_step[0] = 1; _dots()
            title_lbl.configure(text="  New Menu Item  Step 1 of 3")
            inf = ctk.CTkFrame(content, fg_color=BG_BLU, corner_radius=10)
            inf.pack(fill="x", pady=(4,12))
            lbl(inf, "Enter the menu item name to get started.", size=12, color=BLUE
                ).pack(padx=14, pady=10, anchor="w")
            lbl(content, "Menu Item Name", size=12, weight="bold", color=ARMY_BG
                ).pack(anchor="w", pady=(0,4))
            e = entry(content, ph="e.g., Roti Thali / Veg Pulao", h=44)
            e.pack(fill="x")
            if menu_name[0]: e.insert(0, menu_name[0])
            lbl(content, "Use a clear name staff will recognise on the sales screen.",
                size=10, color=MID).pack(anchor="w", pady=(6,0))

            def _next():
                nm = e.get().strip()
                if not nm: self._popup("Warning", "Enter the menu item name."); return
                menu_name[0] = nm; wizard_step[0] = 2; _step2()

            btn(foot, "<- Cancel", lambda: overlay.destroy(), fg=STRIPE, hv=BORDER, h=42, w=120
                ).pack(side="left", padx=16, pady=10)
            btn(foot, "Next ->", _next, fg=ARMY_BG, hv=ARMY_HVR, h=42, w=160
                ).pack(side="right", padx=16, pady=10)

        # ── STEP 2 ──────────────────────────────────────────────────────────
        cost_lbl_ref   = [None]
        cb_vars        = {}       # item_name -> BooleanVar
        cb_widgets     = []       # list of (item_name, checkbox_widget)

        def _step2():
            _clear(); wizard_step[0] = 2; _dots()
            title_lbl.configure(text="  " + menu_name[0] + "  Step 2 of 3")

            # ── Calculation explanation banner ───────────────────────────────
            calc_info = ctk.CTkFrame(content, fg_color=BG_BLU, corner_radius=8,
                                     border_width=1, border_color="#BFDBFE")
            calc_info.pack(fill="x", pady=(0,6))
            lbl(calc_info, "📐  How calculations work", size=10, weight="bold",
                color=BLUE).pack(anchor="w", padx=10, pady=(6,2))
            lbl(calc_info,
                "Total Made = total plates served from this batch  •  "
                "Stock deducted = Total Raw  •  "
                "Waste logged = Total Waste × Cost/unit  •  "
                "Cost/plate = (Raw−Waste) × Cost/unit ÷ Total Made",
                size=9, color=BLUE, wraplength=820).pack(anchor="w", padx=10, pady=(0,6))

            # Two-column layout inside content
            two_col = ctk.CTkFrame(content, fg_color="transparent")
            two_col.pack(fill="both", expand=True)
            two_col.grid_columnconfigure(0, weight=2)
            two_col.grid_columnconfigure(1, weight=3)
            two_col.grid_rowconfigure(0, weight=1)

            # ── LEFT: Searchable checkbox picker ────────────────────────────
            left = ctk.CTkFrame(two_col, fg_color=STRIPE, corner_radius=10,
                                border_width=1, border_color=BORDER)
            left.grid(row=0, column=0, sticky="nsew", padx=(0,8))

            lbl(left, "📦  Select Ingredients", size=11, weight="bold",
                color=ARMY_BG).pack(anchor="w", padx=10, pady=(10,4))

            srch = ctk.CTkEntry(left, placeholder_text="🔍 Search...", height=30,
                                font=ctk.CTkFont(size=11))
            srch.pack(fill="x", padx=10, pady=(0,6))

            cb_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent", height=200)
            cb_scroll.pack(fill="both", expand=True, padx=6, pady=(0,8))

            # Build checkbox list
            cb_vars.clear(); cb_widgets.clear()
            for it in inv_items:
                var = ctk.BooleanVar(value=False)
                # Pre-check items already in ing_rows
                for r in ing_rows:
                    try:
                        if r["om"].get() == it: var.set(True)
                    except Exception: pass
                cb_vars[it] = var

                cb_f = ctk.CTkFrame(cb_scroll, fg_color="transparent")
                cb_f.pack(fill="x", pady=1)
                cb = ctk.CTkCheckBox(cb_f, text=it, variable=var,
                                     font=ctk.CTkFont(size=11), text_color=DARK,
                                     fg_color=ARMY_BG, hover_color=ARMY_HVR,
                                     checkbox_width=18, checkbox_height=18,
                                     command=lambda i=it: _on_check(i))
                cb.pack(anchor="w", padx=4)
                cb_widgets.append((it, cb, cb_f))

            def _filter_cb(*args):
                q = srch.get().lower()
                for name, cb_w, cb_frame in cb_widgets:
                    if q in name.lower():
                        cb_frame.pack(fill="x", pady=1)
                    else:
                        cb_frame.pack_forget()
            srch.bind("<KeyRelease>", _filter_cb)

            lbl(left, f"{len(inv_items)} items available", size=9,
                color=MID).pack(pady=(0,6))

            # ── RIGHT: Qty input rows ────────────────────────────────────────
            right = ctk.CTkFrame(two_col, fg_color="transparent")
            right.grid(row=0, column=1, sticky="nsew")

            lbl(right, "⚖️  Qty per Batch for Selected Ingredients",
                size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(2,2))

            # Column header
            hrow = ctk.CTkFrame(right, fg_color=ARMY_BG, corner_radius=6, height=26)
            hrow.pack(fill="x", pady=(0,4)); hrow.pack_propagate(False)
            for col_t in ["Ingredient", "Total Raw", "Total Made", "Total Waste", "Serve/Plate"]:
                lbl(hrow, col_t, size=9, weight="bold", color=GOLD_LT
                    ).pack(side="left", padx=4, expand=True)

            # Scrollable ingredients area — expands to fill available right-panel space
            ing_sf = ctk.CTkScrollableFrame(right, fg_color="transparent")
            ing_sf.pack(fill="both", expand=True)

            # Live cost panel
            cost_panel = ctk.CTkFrame(right, fg_color=BG_SAF, corner_radius=8,
                                      border_width=1, border_color=T_SAF)
            cost_panel.pack(fill="x", pady=(4,0))
            lbl(cost_panel, "💰 Live Cost Analysis", size=10, weight="bold",
                color=ORANGE).pack(anchor="w", padx=12, pady=(4,2))
            cost_lbl = lbl(cost_panel,
                           "Tick ingredients on the left to begin.",
                           size=10, color=MID, wraplength=380)
            cost_lbl.pack(anchor="w", padx=12, pady=(0,6))
            cost_lbl_ref[0] = cost_lbl

            def _auto_serve(row_dict):
                """Auto-fill Serve/Plate = Raw / Made (quantity per plate).
                e.g. 5 kg gas for 100 plates -> 5/100 = 0.05 kg per plate
                Only auto-fills if user has not manually edited the serve field.
                """
                try:    made = float(row_dict["made"].get())
                except: made = 0.0
                try:    raw  = float(row_dict["raw"].get())
                except: raw  = 0.0
                if made > 0 and raw > 0:
                    serve_val = round(raw / made, 4)
                    row_dict["serve"].delete(0, "end")
                    row_dict["serve"].insert(0, str(serve_val))

            def _recalc():
                """Recalculate cost using Serve/Plate = Made / Raw (editable)."""
                total_plate = 0.0; lines = []; max_p = 0
                for row in ing_rows:
                    iname = row["item"]
                    try:    raw   = float(row["raw"].get())
                    except: raw   = 0.0
                    try:    made  = float(row["made"].get())
                    except: made  = 0.0
                    try:    waste = float(row["waste"].get())
                    except: waste = 0.0
                    try:    serve = float(row["serve"].get())
                    except: serve = 0.0
                    if serve <= 0 and made > 0 and raw > 0:
                        serve = round(raw / made, 4)
                    if iname in inv_data and made > 0:
                        cp = inv_data[iname]["cp"]
                        usable = max(raw - waste, 0)
                        cost_per_plate = (usable * cp) / made
                        wc = waste * cp
                        total_plate += cost_per_plate
                        unit_str = inv_data[iname].get("unit", "")
                        lines.append(
                            f"  {iname}:  {serve:.4f} {unit_str}/plate  |  "
                            f"₹{cost_per_plate:.2f}/plate  |  "
                            f"waste ₹{wc:.1f}  |  deducts {raw} {unit_str}")
                        max_p = max(max_p, int(made))
                batch_portions[0] = max_p
                if lines:
                    cost_lbl_ref[0].configure(
                        text=f"  {max_p} plates  |  Total Cost/plate: ₹{total_plate:.2f}\n" +
                             "\n".join(lines) +
                             f"\n\n  ⭐ TOTAL cost/plate: ₹{total_plate:.2f}",
                        text_color=DARK)
                else:
                    cost_lbl_ref[0].configure(
                        text="Tick ingredients on the left to begin.", text_color=MID)
                total_cost_per_piece[0] = total_plate
                total_cost_per_plate[0] = total_plate

            def _add_row(item_name, prefill=None):
                """Add a compact 2-line card."""
                row_f = ctk.CTkFrame(ing_sf, fg_color=WHITE, corner_radius=8,
                                     border_color=BORDER)
                row_f.pack(fill="x", pady=(0,5), padx=2)

                # ── Top bar: name + unit ──────────────────────────────────────
                top = ctk.CTkFrame(row_f, fg_color=ARMY_BG, corner_radius=6, height=24)
                top.pack(fill="x", padx=4, pady=(4,2)); top.pack_propagate(False)
                unit_str = inv_data.get(item_name, {}).get("unit", "")
                lbl(top, f"  {item_name}  ({unit_str})",
                    size=10, weight="bold", color=GOLD_LT).pack(side="left", padx=6)

                # ── Bottom row: 4 labelled fields ─────────────────────────────
                bot = ctk.CTkFrame(row_f, fg_color="transparent")
                bot.pack(fill="x", padx=6, pady=(0,6))

                def _field(parent, label_text, readonly=False):
                    """Create a labelled compact entry."""
                    fc = ctk.CTkFrame(parent, fg_color="transparent")
                    fc.pack(side="left", padx=(0,6))
                    lbl(fc, label_text, size=8, color=MID).pack(anchor="w")
                    e = ctk.CTkEntry(fc, height=30, width=80,
                                     font=ctk.CTkFont(size=12), border_color=BORDER,
                                     corner_radius=6, justify="center",
                                     fg_color="#F0FDF4" if readonly else WHITE)
                    e.pack()
                    e.bind("<KeyRelease>", lambda _: _recalc())
                    return e

                raw_e   = _field(bot, "Total Raw")
                made_e  = _field(bot, "Total Made")
                waste_e = _field(bot, "Total Waste")
                # Serve/Plate = Made ÷ Raw, editable (light-blue = auto-filled)
                serve_fc = ctk.CTkFrame(bot, fg_color="transparent")
                serve_fc.pack(side="left", padx=(0,6))
                lbl(serve_fc, "Serve/Plate (auto)", size=8, color=BLUE).pack(anchor="w")
                serve_e = ctk.CTkEntry(serve_fc, height=30, width=80,
                                       font=ctk.CTkFont(size=12), border_color="#93C5FD",
                                       corner_radius=6, justify="center",
                                       fg_color="#EFF6FF")
                serve_e.pack()
                serve_e.bind("<KeyRelease>", lambda _: _recalc())

                # Hidden value holder
                om_val = ctk.StringVar(value=item_name)
                class _OM:
                    def get(self): return om_val.get()
                om = _OM()

                row_dict = {"om": om, "raw": raw_e, "made": made_e,
                            "waste": waste_e, "serve": serve_e, "frame": row_f,
                            "item": item_name}
                ing_rows.append(row_dict)

                # Auto-fill serve when raw or made changes
                def _on_raw_made(event, rd=row_dict):
                    _auto_serve(rd)
                    _recalc()

                raw_e.bind("<KeyRelease>",  lambda e, rd=row_dict: (_auto_serve(rd), _recalc()))
                made_e.bind("<KeyRelease>", lambda e, rd=row_dict: (_auto_serve(rd), _recalc()))

                if prefill:
                    raw_e.insert(0,   str(prefill.get("raw",   "")))
                    made_e.insert(0,  str(prefill.get("made",  "")))
                    waste_e.insert(0, str(prefill.get("waste", "")))
                    # Restore serve: use saved value or auto-calc
                    saved_serve = prefill.get("serve", "")
                    if saved_serve and str(saved_serve) not in ("", "1", "1.0"):
                        serve_e.insert(0, str(saved_serve))
                    else:
                        _auto_serve(row_dict)
                _recalc()
                return row_dict

            def _remove_row(item_name):
                for rd in list(ing_rows):
                    if rd.get("item") == item_name:
                        rd["frame"].destroy()
                        ing_rows.remove(rd)
                        break
                _recalc()

            def _on_check(item_name):
                if cb_vars[item_name].get():
                    # Add row if not already there
                    if not any(rd.get("item") == item_name for rd in ing_rows):
                        _add_row(item_name)
                else:
                    _remove_row(item_name)

            # Restore previous rows if coming back from step 3
            saved = []
            for r in ing_rows:
                try:
                    saved.append({"item": r["om"].get(), "raw": r["raw"].get(),
                                  "made": r["made"].get(), "waste": r["waste"].get(),
                                  "serve": r["serve"].get()})
                except Exception: pass
            ing_rows.clear()
            for s in saved:
                iname = s.get("item","")
                if iname in cb_vars:
                    cb_vars[iname].set(True)
                _add_row(iname, prefill=s)

            def _go_step3():
                snapshot_rows.clear()
                for row in ing_rows:
                    try:    raw   = float(row["raw"].get())
                    except: raw   = 0.0
                    try:    made  = float(row["made"].get())
                    except: made  = 0.0
                    try:    waste = float(row["waste"].get())
                    except: waste = 0.0
                    try:    serve = float(row["serve"].get())
                    except: serve = 1.0
                    if serve <= 0: serve = 1.0
                    snapshot_rows.append({
                        "name": row["om"].get(),
                        "raw": raw, "made": made,
                        "waste": waste, "serve": serve   # serve = Made/Raw ratio
                    })
                _step3()

            btn(foot, "<- Back", lambda: _step1(), fg=STRIPE, hv=BORDER, h=42, w=100
                ).pack(side="left", padx=16, pady=10)
            btn(foot, "Next ->", _go_step3, fg=ARMY_BG, hv=ARMY_HVR, h=42, w=160
                ).pack(side="right", padx=16, pady=10)

        # ── STEP 3 ──────────────────────────────────────────────────────────
        e_sp_ref = [None]

        def _step3():
            _clear(); wizard_step[0] = 3; _dots()
            title_lbl.configure(text="  " + menu_name[0] + "  Step 3 of 3")
            cost_piece = total_cost_per_piece[0]
            cost_plate = total_cost_per_plate[0]

            sc = ctk.CTkFrame(content, fg_color=BG_GRN, corner_radius=10,
                              border_width=1, border_color=T_GRN)
            sc.pack(fill="x", pady=(4,12))
            lbl(sc, menu_name[0], size=13, weight="bold", color=DGREEN
                ).pack(anchor="w", padx=14, pady=(10,2))
            ing_count = len([r for r in snapshot_rows if r.get("name","") not in ("","(none)","")])
            lbl(sc, "Ingredients: " + str(ing_count) + "  |  Batch: " + str(batch_portions[0]) + " portions",
                size=11, color=DARK).pack(anchor="w", padx=14)

            if cost_plate > 0:
                suggested = max(5, round(cost_plate * 1.3 / 5) * 5)
                lbl(sc,
                    "Cost/Piece: Rs." + str(round(cost_piece,2)) +
                    "   |   Cost/Plate: Rs." + str(round(cost_plate,2)),
                    size=12, weight="bold", color=TEAL).pack(anchor="w", padx=14, pady=(4,2))
                lbl(sc,
                    "Suggested Selling Price (30% margin on plate cost): Rs." + str(int(suggested)),
                    size=11, color=MID).pack(anchor="w", padx=14, pady=(0,10))
            elif cost_piece > 0:
                suggested = max(5, round(cost_piece * 1.3 / 5) * 5)
                lbl(sc,
                    "Cost/Piece: Rs." + str(round(cost_piece,2)) +
                    "   |   Suggested Price: Rs." + str(int(suggested)),
                    size=12, weight="bold", color=GREEN).pack(anchor="w", padx=14, pady=(4,10))
            else:
                suggested = 70
                lbl(sc, "No cost data. Set price manually.", size=11, color=MID
                    ).pack(anchor="w", padx=14, pady=(4,10))

            sep(content, color=BORDER, h=1).pack(fill="x", pady=8)
            lbl(content, "Selling Price per Plate (Rs.)", size=12, weight="bold", color=ARMY_BG
                ).pack(anchor="w", pady=(0,4))
            e_sp = entry(content, ph="e.g., " + str(suggested), h=46); e_sp.pack(fill="x")
            if cost_plate > 0 or cost_piece > 0:
                e_sp.insert(0, str(int(suggested)))
            e_sp_ref[0] = e_sp
            lbl(content, "Staff see this price on the sales screen. You can edit it anytime.",
                size=10, color=MID, wraplength=580).pack(anchor="w", pady=(4,0))

            # Ingredient summary table — wrapped in a scrollable frame so all rows are visible
            valid_rows = [r for r in snapshot_rows if r.get("name","") not in ("", "(none)", "")]
            if valid_rows:
                sep(content, color=BORDER, h=1).pack(fill="x", pady=(12,6))
                lbl(content, "Ingredient Summary", size=11, weight="bold", color=ARMY_BG
                    ).pack(anchor="w", pady=(0,4))
                # Sticky table header
                th = ctk.CTkFrame(content, fg_color=ARMY_BG, corner_radius=6, height=26)
                th.pack(fill="x"); th.pack_propagate(False)
                for col in ["Ingredient", "Raw", "Made", "Waste", "Serve/Plate", "Waste Cost", "Rs./plate"]:
                    lbl(th, col, size=10, weight="bold", color=GOLD_LT).pack(
                        side="left", expand=True, padx=5)
                # Scrollable body — max 220px tall so Save button is always visible
                tbl_sf = ctk.CTkScrollableFrame(content, fg_color="transparent", height=220)
                tbl_sf.pack(fill="x", expand=False, pady=(0,4))
                for ix, row in enumerate(valid_rows):
                    iname = row["name"]
                    raw   = row.get("raw",   0.0)
                    made  = row.get("made",  0.0)
                    wst   = row.get("waste", 0.0)
                    serve = row.get("serve", 1.0)
                    if serve <= 0: serve = 1.0
                    usable  = max(raw - wst, 0)
                    cp      = inv_data.get(iname, {}).get("cp", 0)
                    per_p   = (usable * cp / made) if made > 0 else 0
                    per_plt = per_p * serve
                    waste_c = wst * cp
                    bg2 = WHITE if ix % 2 == 0 else STRIPE
                    rf = ctk.CTkFrame(tbl_sf, fg_color=bg2, corner_radius=0, height=28)
                    rf.pack(fill="x"); rf.pack_propagate(False)
                    for val in [iname, str(round(raw,2)), str(int(made)),
                                str(round(wst,2)), str(round(serve,4)) + " qty",
                                "Rs." + str(round(waste_c,1)), "Rs." + str(round(per_plt,2))]:
                        lbl(rf, val, size=10, color=DARK).pack(side="left", expand=True, padx=5)

            # ── SAVE ────────────────────────────────────────────────────────
            def _save():
                nm = menu_name[0]
                try:    sp = float(e_sp_ref[0].get())
                except: self._popup("Invalid", "Enter a numeric selling price."); return
                if sp <= 0: self._popup("Invalid", "Price must be > 0."); return

                today_str = datetime.now().strftime("%Y-%m-%d")
                valid_ings = []
                for row in snapshot_rows:
                    iname = row.get("name", "")
                    if iname in ("", "(none)"): continue
                    raw   = row.get("raw",   0.0)
                    made  = row.get("made",  0.0)
                    wst   = row.get("waste", 0.0)
                    serve = row.get("serve", 0.0)
                    # serve = Raw / Made (quantity per plate)
                    if serve <= 0 and made > 0 and raw > 0:
                        serve = raw / made
                    if made > 0:
                        usable = max(raw - wst, 0)
                        # qty_per_unit = usable raw per plate = usable / Made
                        qpu    = usable / made
                        cp_val = inv_data.get(iname, {}).get("cp", 0)
                        valid_ings.append({
                            "name":       iname,
                            "raw":        raw,
                            "made":       made,
                            "waste":      wst,
                            "serve":      serve,
                            "qpu":        qpu,
                            "waste_cost": wst * cp_val
                        })

                with get_db() as conn:
                    try:
                        cur = conn.execute(
                            "INSERT INTO menu (name, sp, active) VALUES (?, ?, 1)", (nm, sp))
                        new_mid = cur.lastrowid
                    except sqlite3.IntegrityError:
                        self._popup("Duplicate", "'" + nm + "' already exists."); return

                    for ing in valid_ings:
                        irow = conn.execute(
                            "SELECT id FROM inventory WHERE item=?", (ing["name"],)).fetchone()
                        if not irow: continue
                        iid = irow["id"]

                        # 1. Recipe: qty per plate + store originals for delta edits
                        conn.execute(
                            "INSERT INTO recipes "
                            "(menu_id, inv_id, qty_per_unit, total_raw, total_made, total_waste) "
                            "VALUES (?,?,?,?,?,?)",
                            (new_mid, iid, ing["qpu"],
                             ing["raw"], ing["made"], ing["waste"]))

                        # 2. Deduct raw stock from inventory
                        conn.execute(
                            "UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id=?",
                            (ing["raw"], iid))

                        # 3. Log stock ledger
                        conn.execute(
                            "INSERT INTO stock_ledger "
                            "(date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,?,?,?)",
                            (today_str, iid, "MENU_SETUP", -ing["raw"],
                             f"New menu: {nm}"))

                        # 4. Log waste to waste_tracker
                        if ing["waste"] > 0:
                            conn.execute(
                                "INSERT INTO waste_tracker "
                                "(date, item, qty_wasted, reason, cost_lost, recorded_by) "
                                "VALUES (?,?,?,?,?,?)",
                                (today_str, ing["name"], ing["waste"],
                                 "Production waste - " + nm,
                                 ing["waste_cost"], "Menu Setup"))

                    # 5. Log batch_prep
                    max_made = max((ing["made"] for ing in valid_ings), default=0)
                    if max_made > 0:
                        conn.execute(
                            "INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                            (today_str, new_mid, int(max_made)))

                    # 6. Store COGS per plate in menu table
                    total_cogs = sum(
                        (max(ing["raw"] - ing["waste"], 0) *
                         inv_data.get(ing["name"], {}).get("cp", 0) / ing["made"])
                        for ing in valid_ings if ing["made"] > 0
                    )
                    conn.execute(
                        "UPDATE menu SET cogs=? WHERE id=?",
                        (round(total_cogs, 4), new_mid))

                    # Log total raw material cost as Expenditure so net profit
                    # immediately reflects the spend when the menu/batch is created.
                    # (Waste is tracked separately in waste_tracker.)
                    total_raw_cost = sum(
                        ing["raw"] * inv_data.get(ing["name"], {}).get("cp", 0)
                        for ing in valid_ings
                    )
                    if total_raw_cost > 0:
                        conn.execute(
                            "INSERT INTO expenditure (date, amount, category, notes) "
                            "VALUES (?,?,?,?)",
                            (today_str, round(total_raw_cost, 2),
                             "Raw Material",
                             f"Batch: {nm} | {today_str}"))
                msg = "Created '" + nm + "' @ ₹" + str(int(sp))
                if valid_ings:
                    wc_total  = sum(i["waste_cost"] for i in valid_ings)
                    profit    = sp - total_cogs
                    margin    = (profit / sp * 100) if sp > 0 else 0
                    msg += (f"  |  Cost ₹{total_cogs:.1f}  |  "
                            f"Profit ₹{profit:.1f} ({margin:.0f}%)  |  "
                            f"Waste ₹{wc_total:.1f}")
                self._toast(msg)
                overlay.destroy()
                self._switch_master_tab("menu")

            btn(foot, "<- Back", lambda: _step2(), fg=STRIPE, hv=BORDER, h=42, w=100
                ).pack(side="left",  padx=16, pady=10)
            btn(foot, "Create Menu Item", _save, fg=GREEN, hv=DGREEN, h=42, w=200
                ).pack(side="right", padx=16, pady=10)

        _step1()


    def _modal_edit_menu(self, mid, name, sp, active):
        body, card, close = self._show_modal(f"✏️  Edit Menu Item", 520, 400)

        # Item name header
        ni = ctk.CTkFrame(body, fg_color=ARMY_BG, corner_radius=10)
        ni.pack(fill="x", pady=(0,14))
        lbl(ni, f"  🍽  {name}", size=14, weight="bold", color=WHITE).pack(
            padx=14, pady=(10,2), anchor="w")
        lbl(ni, "  Edit selling price and status below",
            size=10, color=GOLD_LT).pack(padx=14, pady=(0,10), anchor="w")

        sep(body, color=BORDER, h=1).pack(fill="x", pady=(0,10))

        # Current info row
        info_row = ctk.CTkFrame(body, fg_color=STRIPE, corner_radius=8)
        info_row.pack(fill="x", pady=(0,12))
        lbl(info_row, f"  Current Price: ₹{sp:.0f}", size=11, color=MID
            ).pack(side="left", padx=14, pady=8)
        status_txt = "✓ Active" if active else "✗ Inactive"
        status_clr = GREEN if active else RED
        lbl(info_row, status_txt, size=11, weight="bold", color=status_clr
            ).pack(side="right", padx=14, pady=8)

        # New price
        lbl(body, "New Selling Price (₹)", size=11, weight="bold",
            color=ARMY_BG).pack(anchor="w", pady=(0,4))
        e_sp = entry(body, ph="e.g., 70", h=42)
        e_sp.insert(0, str(int(sp))); e_sp.pack(fill="x")

        # Status
        lbl(body, "Status", size=11, weight="bold",
            color=ARMY_BG).pack(anchor="w", pady=(12,4))
        status_m = ctk.CTkOptionMenu(body, values=["Active", "Inactive"],
                                     font=ctk.CTkFont(size=12), height=40,
                                     fg_color=ARMY_BG, button_color=ARMY_HVR,
                                     text_color=WHITE)
        status_m.set("Active" if active else "Inactive"); status_m.pack(fill="x")

        def save():
            try:    new_sp = float(e_sp.get())
            except: self._popup("⚠️ Invalid", "Enter a numeric price."); return
            if new_sp <= 0: self._popup("⚠️ Invalid", "Price must be > 0."); return
            new_ac = 1 if status_m.get() == "Active" else 0
            with get_db() as conn:
                conn.execute("UPDATE menu SET sp=?,active=? WHERE id=?", (new_sp, new_ac, mid))
            self._toast(f"'{name}' updated  •  ₹{new_sp:.0f}  •  {status_m.get()}")
            close(); self._switch_master_tab("menu")

        btn(card, "✅  Save Changes", save, fg=GREEN, hv=DGREEN, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")

    # ── Legacy aliases so other code doesn't break ─────────────────────────
    def _modal_edit_ingredients(self, mid, name):
        body, modal_card, close = self._show_modal(f"🥗  Ingredients: {name}", 600, 480)
        
        ic = card(body); ic.pack(fill="x", pady=(0,14))
        band(ic,"📋  Current Active Ingredients")
        COLS = [("Item",3),("Qty/Unit",2),("Remove",1)]
        thead(ic, COLS, bg=STRIPE, tc=MID)
        
        with get_db() as conn:
            inv = conn.execute("SELECT id, item, unit FROM inventory ORDER BY item").fetchall()
            recipes = conn.execute(
                "SELECT r.id as rid, i.item, i.unit, r.qty_per_unit FROM recipes r "
                "JOIN inventory i ON i.id = r.inv_id WHERE r.menu_id=?", (mid,)
            ).fetchall()
            
        def del_r(rid):
            with get_db() as conn: conn.execute("DELETE FROM recipes WHERE id=?", (rid,))
            self._toast("✅ Ingredient removed"); close(); self._modal_edit_ingredients(mid, name)
            
        if not recipes:
            lbl(ic,"No ingredients mapped yet.",size=11,color=MID).pack(pady=10)
        else:
            for ix, r in enumerate(recipes):
                rf = ctk.CTkFrame(ic, fg_color=WHITE if ix%2==0 else STRIPE, corner_radius=0, height=36)
                rf.pack(fill="x"); rf.pack_propagate(False)
                lbl(rf, r["item"], size=11, weight="bold", color=DARK).grid(row=0,column=0,padx=14,sticky="w")
                lbl(rf, f"{r['qty_per_unit']} {r['unit']}", size=11).grid(row=0,column=1,padx=14,sticky="w")
                b = ctk.CTkButton(rf, text="🗑", width=28, height=24, fg_color=STRIPE, hover_color=T_RED, text_color=RED,
                                  command=lambda rid=r["rid"]: del_r(rid))
                b.grid(row=0,column=2,padx=14,sticky="e")
                rf.grid_columnconfigure(0,weight=3); rf.grid_columnconfigure(1,weight=2); rf.grid_columnconfigure(2,weight=1)
                
        fc = card(body); fc.pack(fill="x")
        band(fc,"➕  Add Ingredient")
        ff = ctk.CTkFrame(fc, fg_color="transparent"); ff.pack(fill="x", padx=14, pady=10)
        
        lbl(ff,"Select Item (Searchable)",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(0,4))
        se = ctk.CTkEntry(ff, placeholder_text="🔍 Type to search...", height=32); se.pack(fill="x", pady=(0,6))
        
        inv_names = [i["item"] for i in inv]
        om = ctk.CTkOptionMenu(ff, values=inv_names or ["(none)"], font=ctk.CTkFont(size=12))
        om.set(inv_names[0] if inv_names else ""); om.pack(fill="x", pady=(0,10))
        
        def filter_items(*args):
            q = se.get().lower(); fil = [x for x in inv_names if q in x.lower()]
            om.configure(values=fil or ["(none)"])
            if fil: om.set(fil[0])
        se.bind("<KeyRelease>", filter_items)
        
        lbl(ff,"Quantity per meal",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(0,4))
        qe = entry(ff, ph="e.g. 0.150 for 150g (if unit is kg)", h=36); qe.pack(fill="x", pady=(0,10))
        
        def save_ing():
            item = om.get()
            try: q = float(qe.get())
            except: self._popup("⚠️ Invalid","Enter numeric qty"); return
            if q <= 0: return
            with get_db() as conn:
                iid = conn.execute("SELECT id FROM inventory WHERE item=?", (item,)).fetchone()["id"]
                conn.execute("INSERT INTO recipes (menu_id,inv_id,qty_per_unit) VALUES (?,?,?)", (mid, iid, q))
            self._toast(f"✅ Added {item}"); close(); self._modal_edit_ingredients(mid, name)
            
        btn(fc,"✅ Add Ingredient",save_ing,fg=GREEN,hv=DGREEN,h=38).pack(padx=14,pady=(0,14),fill="x")

    def _dlg_add_menu(self):        self._modal_add_menu()
    def _dlg_edit_menu(self,m,n,s,a): self._modal_edit_menu(m,n,s,a)

    def _modal_update_batch(self, menu_id, menu_name):
        """
        Update Batch modal: admin can adjust Raw / Made / Waste for each ingredient.
        Only the DELTA (new value minus stored original) is applied to stock.
        E.g.  original raw = 10 kg, new raw = 12 kg  =>  deduct only 2 kg from stock.
              original raw = 10 kg, new raw = 8  kg  =>  add back 2 kg to stock.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")

        with get_db() as conn:
            # Fetch current recipe rows with originals
            rows = conn.execute(
                "SELECT r.id as rid, i.item, i.unit, i.cp, i.stock, "
                "r.qty_per_unit, r.total_raw, r.total_made, r.total_waste "
                "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
                "WHERE r.menu_id=? ORDER BY i.item", (menu_id,)
            ).fetchall()
            menu_row = conn.execute(
                "SELECT name, sp FROM menu WHERE id=?", (menu_id,)).fetchone()

        if not rows:
            self._popup("No Ingredients",
                        f"'{menu_name}' has no ingredient recipes.\n"
                        "Use the 🥗 button to add ingredients first.")
            return

        overlay = tk.Frame(self._area, bg="#1E293B")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        modal_card = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                                  border_width=2, border_color=ARMY_BG, width=860, height=640)
        modal_card.place(relx=0.5, rely=0.5, anchor="center")
        modal_card.pack_propagate(False)

        # Header
        hbar = ctk.CTkFrame(modal_card, fg_color=ARMY_BG, corner_radius=0, height=54)
        hbar.pack(fill="x", side="top"); hbar.pack_propagate(False)
        ctk.CTkFrame(hbar, fg_color="#F59E0B", width=4).pack(side="left", fill="y")
        lbl(hbar, f"  🔄  Update Batch  •  {menu_name}",
            size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
        ctk.CTkButton(hbar, text="X", width=34, height=34, corner_radius=8,
                      fg_color="transparent", hover_color=ARMY_HVR, text_color=GOLD_LT,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=lambda: overlay.destroy()).pack(side="right", padx=10)

        # Footer packed first so it's always visible
        foot = ctk.CTkFrame(modal_card, fg_color=WHITE, border_width=1,
                            border_color=BORDER, corner_radius=0, height=60)
        foot.pack(fill="x", side="bottom"); foot.pack_propagate(False)

        content = ctk.CTkScrollableFrame(modal_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=10)

        # Info banner
        info = ctk.CTkFrame(content, fg_color="#FEF3C7", corner_radius=8,
                            border_width=1, border_color="#FDE68A")
        info.pack(fill="x", pady=(0,10))
        lbl(info, "⚠️  Delta Stock Adjustment", size=10, weight="bold",
            color="#92400E").pack(anchor="w", padx=12, pady=(6,2))
        lbl(info,
            "Enter the NEW total values. Only the difference from the original is applied to stock.\n"
            "Example: Original Raw = 10 kg, New Raw = 12 kg  →  2 kg deducted from stock.\n"
            "         Original Raw = 10 kg, New Raw = 8 kg   →  2 kg returned to stock.",
            size=9, color="#78350F", wraplength=800
        ).pack(anchor="w", padx=12, pady=(0,8))

        # Column header
        hrow = ctk.CTkFrame(content, fg_color=ARMY_BG, corner_radius=6, height=28)
        hrow.pack(fill="x", pady=(0,6)); hrow.pack_propagate(False)
        for col_t in ["Ingredient", "Orig Raw", "New Raw", "Orig Made", "New Made",
                      "Orig Waste", "New Waste", "Stock Now"]:
            lbl(hrow, col_t, size=9, weight="bold", color=GOLD_LT
                ).pack(side="left", expand=True, padx=4)

        # Build editable rows
        row_refs = []   # list of dicts with entry widget refs
        for ix, r in enumerate(rows):
            bg2 = WHITE if ix % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(content, fg_color=bg2, corner_radius=8,
                              border_width=1, border_color=BORDER)
            rf.pack(fill="x", pady=(0,5))

            # Top: ingredient name bar
            top = ctk.CTkFrame(rf, fg_color=ARMY_BG, corner_radius=6, height=22)
            top.pack(fill="x", padx=4, pady=(4,2)); top.pack_propagate(False)
            lbl(top, f"  {r['item']}  ({r['unit']})",
                size=10, weight="bold", color=GOLD_LT).pack(side="left", padx=6)
            stk = round(r["stock"], 3)
            stk_color = RED if stk < 2 else GREEN
            lbl(top, f"Stock: {stk} {r['unit']}",
                size=9, color=stk_color).pack(side="right", padx=8)

            # Bottom: fields row
            bot = ctk.CTkFrame(rf, fg_color="transparent")
            bot.pack(fill="x", padx=6, pady=(2,6))

            def _field_ro(parent, value, unit=""):
                """Read-only display cell."""
                fc = ctk.CTkFrame(parent, fg_color="transparent")
                fc.pack(side="left", padx=(0,4))
                lbl(fc, f"{value} {unit}", size=11, color=MID, weight="bold").pack()

            def _field_edit(parent, ph="0"):
                """Editable entry."""
                e = ctk.CTkEntry(parent, height=30, width=80, justify="center",
                                 font=ctk.CTkFont(size=12), border_color=BORDER,
                                 fg_color="#EFF6FF")
                e.pack(side="left", padx=(0,4))
                return e

            orig_raw   = r["total_raw"]   or 0.0
            orig_made  = r["total_made"]  or 0.0
            orig_waste = r["total_waste"] or 0.0

            _field_ro(bot, round(orig_raw,3),   r["unit"])
            new_raw_e  = _field_edit(bot, str(round(orig_raw,3)))
            _field_ro(bot, round(orig_made,3),  "plates")
            new_made_e = _field_edit(bot, str(round(orig_made,3)))
            _field_ro(bot, round(orig_waste,3), r["unit"])
            new_wst_e  = _field_edit(bot, str(round(orig_waste,3)))
            lbl(bot, f"  {stk} {r['unit']}",
                size=10, color=stk_color).pack(side="left", padx=4)

            # Pre-fill with current originals
            new_raw_e.insert(0,  str(round(orig_raw,3)))
            new_made_e.insert(0, str(round(orig_made,3)))
            new_wst_e.insert(0,  str(round(orig_waste,3)))

            row_refs.append({
                "rid":        r["rid"],
                "item":       r["item"],
                "unit":       r["unit"],
                "cp":         r["cp"],
                "orig_raw":   orig_raw,
                "orig_made":  orig_made,
                "orig_waste": orig_waste,
                "new_raw":    new_raw_e,
                "new_made":   new_made_e,
                "new_waste":  new_wst_e,
            })

        def _apply_updates():
            changes = []
            errors  = []
            for rd in row_refs:
                try:    nr = float(rd["new_raw"].get())
                except: errors.append(f"{rd['item']}: invalid Raw"); continue
                try:    nm = float(rd["new_made"].get())
                except: errors.append(f"{rd['item']}: invalid Made"); continue
                try:    nw = float(rd["new_waste"].get())
                except: errors.append(f"{rd['item']}: invalid Waste"); continue
                if nr < 0 or nm < 0 or nw < 0:
                    errors.append(f"{rd['item']}: values cannot be negative")
                    continue
                changes.append({
                    "rid":       rd["rid"],
                    "item":      rd["item"],
                    "cp":        rd["cp"],
                    "orig_raw":  rd["orig_raw"],
                    "orig_made": rd["orig_made"],
                    "orig_waste":rd["orig_waste"],
                    "new_raw":   nr,
                    "new_made":  nm,
                    "new_waste": nw,
                })

            if errors:
                self._popup("⚠️ Validation Errors", "\n".join(errors))
                return

            with get_db() as conn:
                for ch in changes:
                    delta_raw   = ch["new_raw"]   - ch["orig_raw"]
                    new_made    = ch["new_made"]
                    cp          = ch["cp"]

                    # Compute new qty_per_unit
                    if new_made > 0:
                        usable = max(ch["new_raw"] - ch["new_waste"], 0)
                        new_qpu = usable / new_made
                    else:
                        new_qpu = 0.0

                    # 1. Update recipe row with new totals & qpu
                    conn.execute(
                        "UPDATE recipes SET qty_per_unit=?, total_raw=?, "
                        "total_made=?, total_waste=? WHERE id=?",
                        (new_qpu, ch["new_raw"], ch["new_made"],
                         ch["new_waste"], ch["rid"]))

                    # 2. Apply delta to inventory stock
                    if delta_raw != 0:
                        conn.execute(
                            "UPDATE inventory SET stock = MAX(0, stock - ?) "
                            "WHERE item=?",
                            (delta_raw, ch["item"]))
                        conn.execute(
                            "INSERT INTO stock_ledger "
                            "(date, inv_id, transaction_type, qty_change, notes) "
                            "SELECT ?, id, ?, ?, ? FROM inventory WHERE item=?",
                            (today_str, "BATCH_UPDATE", -delta_raw,
                             f"Batch update: {menu_name} "
                             f"(orig {ch['orig_raw']}→new {ch['new_raw']})",
                             ch["item"]))

                    # 3. Log extra waste if waste increased
                    extra_waste = ch["new_waste"] - ch["orig_waste"]
                    if extra_waste > 0:
                        conn.execute(
                            "INSERT INTO waste_tracker "
                            "(date, item, qty_wasted, reason, cost_lost, recorded_by) "
                            "VALUES (?,?,?,?,?,?)",
                            (today_str, ch["item"], extra_waste,
                             f"Batch update - {menu_name}",
                             extra_waste * cp, "Admin Update"))

                    # 4. Update batch_prep
                    if new_made > 0:
                        existing = conn.execute(
                            "SELECT id FROM batch_prep WHERE menu_id=? AND date=?",
                            (menu_id, today_str)).fetchone()
                        if existing:
                            conn.execute(
                                "UPDATE batch_prep SET qty_prepared=? "
                                "WHERE menu_id=? AND date=?",
                                (int(new_made), menu_id, today_str))
                        else:
                            conn.execute(
                                "INSERT INTO batch_prep (date, menu_id, qty_prepared) "
                                "VALUES (?,?,?)",
                                (today_str, menu_id, int(new_made)))

                # 5. Recalculate and update COGS for the menu item
                all_recipes = conn.execute(
                    "SELECT r.total_raw, r.total_made, r.total_waste, i.cp "
                    "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
                    "WHERE r.menu_id=?", (menu_id,)
                ).fetchall()
                new_cogs = sum(
                    (max(r["total_raw"] - r["total_waste"], 0) * r["cp"] / r["total_made"])
                    for r in all_recipes if r["total_made"] > 0
                )
                sp_now = conn.execute(
                    "SELECT sp FROM menu WHERE id=?", (menu_id,)).fetchone()["sp"]
                conn.execute(
                    "UPDATE menu SET cogs=? WHERE id=?",
                    (round(new_cogs, 4), menu_id))

                # 6. Update raw material expenditure entry for this batch
                #    Delete old entry and insert updated total so Net Profit
                #    always reflects the current actual ingredient spend.
                new_raw_cost = sum(
                    r["total_raw"] * r["cp"] for r in all_recipes
                )
                note_pattern = f"Batch: {menu_name} | %"
                conn.execute(
                    "DELETE FROM expenditure WHERE category='Raw Material' "
                    "AND notes LIKE ?", (note_pattern,))
                if new_raw_cost > 0:
                    conn.execute(
                        "INSERT INTO expenditure (date, amount, category, notes) "
                        "VALUES (?,?,?,?)",
                        (today_str, round(new_raw_cost, 2),
                         "Raw Material",
                         f"Batch: {menu_name} | {today_str}"))

            # Build summary toast
            parts = []
            for ch in changes:
                d = ch["new_raw"] - ch["orig_raw"]
                if d > 0:   parts.append(f"{ch['item']} −{d:.2f} from stock")
                elif d < 0: parts.append(f"{ch['item']} +{abs(d):.2f} back to stock")
            profit_now = sp_now - new_cogs
            margin_now = (profit_now / sp_now * 100) if sp_now > 0 else 0
            toast_msg  = (f"🔄  {menu_name} updated  |  "
                          f"Cost ₹{new_cogs:.1f}  |  "
                          f"Profit ₹{profit_now:.1f} ({margin_now:.0f}%)")
            if parts: toast_msg += "  |  " + "  ".join(parts)
            self._toast(toast_msg)
            overlay.destroy()
            self._switch_master_tab("menu")

        btn(foot, "Cancel", lambda: overlay.destroy(),
            fg=STRIPE, hv=BORDER, h=42, w=100).pack(side="left", padx=16, pady=10)
        btn(foot, "🔄  Apply Changes & Update Stock", _apply_updates,
            fg="#D97706", hv="#B45309", h=42, w=260).pack(side="right", padx=16, pady=10)

    # ── Daily Schedule tab ────────────────────────────────────────────────────
    def _master_schedule(self, wrap):
        DAYS  = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        TYPES = ["Lunch","Paratha","Mini Meal"]
        with get_db() as conn:
            menu_names = [r["name"] for r in conn.execute(
                "SELECT name FROM menu WHERE active=1 ORDER BY name")]
            sched_rows = conn.execute(
                "SELECT dm.day, dm.meal_type, m.name "
                "FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id").fetchall()

        sched_map = {}
        for s in sched_rows:
            sched_map.setdefault(s["day"], {})[s["meal_type"]] = s["name"]

        # Form
        fc = card(wrap); fc.pack(fill="x", pady=(0,14))
        band(fc, "📅  Assign Daily Menu  •  Lunch | Paratha | Mini Meal")
        ff = ctk.CTkFrame(fc, fg_color="transparent"); ff.pack(fill="x", padx=18, pady=14)
        for i in range(3): ff.grid_columnconfigure(i, weight=1)

        lbl(ff,"Day",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=0,sticky="w",pady=(0,4))
        lbl(ff,"Meal Type",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=1,sticky="w",padx=(16,0),pady=(0,4))
        lbl(ff,"Menu Item",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=2,sticky="w",padx=(16,0),pady=(0,4))

        day_m  = ctk.CTkOptionMenu(ff, values=DAYS,  font=ctk.CTkFont(size=12))
        type_m = ctk.CTkOptionMenu(ff, values=TYPES, font=ctk.CTkFont(size=12))
        item_m = ctk.CTkOptionMenu(ff, values=menu_names or ["(add menu items first)"],
                                   font=ctk.CTkFont(size=12))
        day_m.set("Monday");  day_m.grid( row=1, column=0, sticky="ew", pady=(0,8))
        type_m.set("Lunch");  type_m.grid(row=1, column=1, sticky="ew", padx=(16,0), pady=(0,8))
        item_m.set(menu_names[0] if menu_names else "")
        item_m.grid(row=1, column=2, sticky="ew", padx=(16,0), pady=(0,8))

        def save_sched():
            day = day_m.get(); mtype = type_m.get(); mitem = item_m.get()
            with get_db() as conn:
                mid2 = conn.execute("SELECT id FROM menu WHERE name=?", (mitem,)).fetchone()
                if not mid2: self._popup("⚠️ Error","Menu item not found."); return
                conn.execute("INSERT OR REPLACE INTO daily_menu (day,meal_type,menu_id) VALUES (?,?,?)",
                             (day, mtype, mid2["id"]))
            self._toast(f"{day} {mtype} → {mitem}")
            self._switch_master_tab("schedule")

        btn(fc,"📅  Save Schedule",save_sched,fg=GREEN,hv=DGREEN,h=44).pack(padx=18,pady=(0,14),fill="x")

        # Weekly table
        sc = card(wrap); sc.pack(fill="both", expand=True, pady=(0,14))
        band(sc, "📅  Weekly Menu Schedule  •  AWWA Lunch Programme")
        thead(sc,[("Day",2),("Lunch — ₹70",3),("Paratha — ₹40",3),("Mini Meal — ₹50",3)],bg=STRIPE,tc=MID)
        for ix, day in enumerate(DAYS):
            lunch   = sched_map.get(day,{}).get("Lunch","—")
            paratha = sched_map.get(day,{}).get("Paratha","—")
            mini    = sched_map.get(day,{}).get("Mini Meal","—")
            bg2 = WHITE if ix%2==0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg2, corner_radius=0, height=44)
            rf.pack(fill="x"); rf.pack_propagate(False)
            lbl(rf, day, size=12, weight="bold", color=DARK if day not in ["Saturday","Sunday"] else MID).grid(
                row=0, column=0, padx=14, sticky="w")
            lbl(rf, lunch,   size=10, color=BLUE   if lunch!="—"   else MID).grid(row=0, column=1, padx=10, sticky="w")
            lbl(rf, paratha, size=10, color=ORANGE  if paratha!="—" else MID).grid(row=0, column=2, padx=10, sticky="w")
            lbl(rf, mini,    size=10, color=TEAL   if mini!="—"    else MID).grid(row=0, column=3, padx=10, sticky="w")
            rf.grid_columnconfigure(0,weight=2); rf.grid_columnconfigure(1,weight=3)
            rf.grid_columnconfigure(2,weight=3); rf.grid_columnconfigure(3,weight=3)

        # Clear control
        clf = ctk.CTkFrame(wrap, fg_color="transparent"); clf.pack(fill="x", pady=(4,10))
        lbl(clf,"Clear:",size=11,weight="bold",color=MID).pack(side="left",padx=(0,8))
        cd = ctk.CTkOptionMenu(clf,values=DAYS,width=120,font=ctk.CTkFont(size=11))
        cd.pack(side="left")
        ct2 = ctk.CTkOptionMenu(clf,values=["All","Lunch","Paratha","Mini Meal"],width=120,font=ctk.CTkFont(size=11))
        ct2.pack(side="left",padx=6)
        def do_clear():
            day=cd.get(); t=ct2.get()
            with get_db() as conn:
                if t=="All": conn.execute("DELETE FROM daily_menu WHERE day=?",(day,))
                else:         conn.execute("DELETE FROM daily_menu WHERE day=? AND meal_type=?",(day,t))
            self._switch_master_tab("schedule")
        btn(clf,"🗑 Clear",do_clear,fg=RED,hv=DRED,h=32).pack(side="left")

    # ── Users list tab ────────────────────────────────────────────────────────
    def _master_users(self, wrap):
        ab = ctk.CTkFrame(wrap, fg_color="transparent"); ab.pack(fill="x", pady=(0,14))
        btn(ab,"＋  Add User",     self._dlg_add_user,    fg=GREEN, hv=DGREEN, h=38).pack(side="left")
        btn(ab,"🔄  Reset Password",self._dlg_reset_pwd,  fg=BLUE,  hv=DBLUE,  h=38).pack(side="left",padx=8)
        btn(ab,"🔑  Toggle Active", self._dlg_toggle_user, fg=TEAL,  hv=ARMY_BG, h=38).pack(side="left")

        uc = card(wrap); uc.pack(fill="both", expand=True)
        band(uc, "👤  All User Accounts & Roles")
        COLS = [("Username",2),("Full Name",3),("Rank",1),("Roles",2),("Status",1),("Contact",2)]
        thead(uc, COLS, bg=STRIPE, tc=MID)
        with get_db() as conn:
            users = conn.execute(
                "SELECT u.id,u.username,u.name,u.rank,u.active,u.contact,"
                "GROUP_CONCAT(r.role,', ') AS roles FROM users u "
                "LEFT JOIN user_roles r ON r.user_id=u.id "
                "GROUP BY u.id ORDER BY u.username").fetchall()
        for ix, u in enumerate(users):
            bg2 = WHITE if ix%2==0 else STRIPE
            trow(uc,
                 [u["username"], u["name"], u["rank"],
                  u["roles"] or "None",
                  "✅ Active" if u["active"] else "❌ Inactive",
                  u["contact"] or "—"],
                 [2,3,1,2,1,2],
                 colors=[DARK,DARK,MID,MID,GREEN if u["active"] else RED,MID],
                 bolds=[True,True,False,False,True,False], bg=bg2)

    # ==============================================================================
    # USER MANAGEMENT — Create/Edit/Toggle, with role picker
    # ==============================================================================
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
        body, card, close = self._show_modal("＋  Create New User Account", 520, 530)
        fields = {}
        for lbl_t, attr, ph, pw in [
            ("Username",  "_nu","e.g., jco_smith",        False),
            ("Full Name", "_nn","e.g., JCO Ramesh Smith", False),
            ("Rank",      "_nr","e.g., JCO, Captain",     False),
            ("Contact",   "_nc","e.g., 9876543210",       False),
            ("Password",  "_np","Minimum 6 characters",   True),
        ]:
            lbl(body, lbl_t, size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(8,3))
            e = ctk.CTkEntry(body, height=38, corner_radius=10, placeholder_text=ph,
                             show="●" if pw else "", font=ctk.CTkFont(size=12), border_color=BORDER)
            e.pack(fill="x"); fields[attr] = e

        lbl(body,"Role (Permissions)",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(8,3))
        role_m = ctk.CTkOptionMenu(body, values=["manager","officer","waste_mgr"],
                                   font=ctk.CTkFont(size=12))
        role_m.set("manager"); role_m.pack(fill="x")

        def save():
            un = fields["_nu"].get().strip(); nm = fields["_nn"].get().strip()
            rk = fields["_nr"].get().strip(); ct = fields["_nc"].get().strip()
            pw = fields["_np"].get()
            if not all([un,nm,rk,pw]):
                self._popup("⚠️ Missing","Fill all required fields."); return
            if len(pw) < 6:
                self._popup("⚠️ Weak Password","Minimum 6 characters required."); return
            with get_db() as conn:
                try:
                    cur = conn.execute("INSERT INTO users (username,pw_hash,name,rank,contact) VALUES (?,?,?,?,?)",
                                       (un,_hash(pw),nm,rk,ct))
                    conn.execute("INSERT INTO user_roles (user_id,role) VALUES (?,?)",
                                 (cur.lastrowid, role_m.get()))
                except sqlite3.IntegrityError:
                    self._popup("⚠️ Duplicate","Username already exists!"); return
            self._popup("✅ User Created!", f"{un} ({role_m.get()}) created successfully.")
            close(); self._go("users")

        btn(card,"✅  Create User",save,fg=GREEN,hv=DGREEN,h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")

    def _dlg_reset_pwd(self):
        with get_db() as conn:
            users = [r["username"] for r in conn.execute("SELECT username FROM users ORDER BY username")]
        body, card, close = self._show_modal("🔄  Reset User Password", 500, 300)
        lbl(body,"Select User",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(4,3))
        um = ctk.CTkOptionMenu(body,values=users,font=ctk.CTkFont(size=12))
        um.set(users[0] if users else ""); um.pack(fill="x",pady=(0,12))
        lbl(body,"New Password",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(0,3))
        e_pw = ctk.CTkEntry(body,height=38,corner_radius=10,placeholder_text="Min 6 chars",
                            show="●",font=ctk.CTkFont(size=12),border_color=BORDER)
        e_pw.pack(fill="x")
        def save():
            pw = e_pw.get()
            if len(pw) < 6: self._popup("⚠️ Weak","At least 6 characters."); return
            with get_db() as conn:
                conn.execute("UPDATE users SET pw_hash=? WHERE username=?",(_hash(pw),um.get()))
            self._popup("✅ Password Reset!",f"{um.get()}'s password updated.")
            close()
        btn(card,"✅  Reset Password",save,fg=BLUE,hv=DBLUE,h=46).pack(
            padx=18,pady=12,fill="x",side="bottom")

    def _dlg_toggle_user(self):
        with get_db() as conn:
            un_list = [r["username"] for r in conn.execute("SELECT username FROM users ORDER BY username")]
        body, card, close = self._show_modal("🔑  Activate / Deactivate User", 500, 290)
        lbl(body,"Select User",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(4,3))
        um = ctk.CTkOptionMenu(body,values=un_list,font=ctk.CTkFont(size=12))
        um.set(un_list[0] if un_list else ""); um.pack(fill="x",pady=(0,12))
        lbl(body,"Set Status To",size=11,weight="bold",color=ARMY_BG).pack(anchor="w",pady=(0,3))
        sm = ctk.CTkOptionMenu(body,values=["Active","Inactive"],font=ctk.CTkFont(size=12))
        sm.set("Active"); sm.pack(fill="x")
        def save():
            new_ac = 1 if sm.get()=="Active" else 0
            with get_db() as conn:
                conn.execute("UPDATE users SET active=? WHERE username=?",(new_ac,um.get()))
            self._popup("✅ Updated!",f"{um.get()} is now {sm.get()}.")
            close(); self._go("users")
        btn(card,"✅  Update Status",save,fg=TEAL,hv=ARMY_BG,h=46).pack(
            padx=18,pady=12,fill="x",side="bottom")

    # ==============================================================================
    # ==============================================================================
    # IMPORT DATA — CSV import for Inventory & Menu
    # ==============================================================================
    # ==============================================================================
    # EDIT IMPORTED / PASTED DATA
    # ==============================================================================
    def _pg_edit_datewise(self):
        """Page to view and edit any imported (datewise) records by date."""
        self._hdr("✏️  Edit Imported Records",
                  "Select a date to view and edit Sales, Inventory & Expenditure records")

        # remember which date the user last selected so page refresh keeps it
        if not hasattr(self, "_edit_date"):
            self._edit_date = datetime.now().strftime("%Y-%m-%d")

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(10, PAD))

        # ── Date selector bar ─────────────────────────────────────────────────
        dc = card(wrap); dc.pack(fill="x", pady=(0, 14))
        df = ctk.CTkFrame(dc, fg_color="transparent")
        df.pack(fill="x", padx=18, pady=14)
        lbl(df, "📅  Select Date:", size=12, weight="bold", color=ARMY_BG).pack(side="left", padx=(0,10))
        date_var = ctk.StringVar(value=self._edit_date)
        date_e = ctk.CTkEntry(df, textvariable=date_var, placeholder_text="YYYY-MM-DD",
                               width=140, height=36, corner_radius=8)
        date_e.pack(side="left")

        def _load_date():
            d = date_var.get().strip()
            if not d:
                return
            self._edit_date = d
            _render_all(d)

        btn(df, "🔍  Load Records", _load_date, fg=ARMY_BG, hv=ARMY_HVR, h=36, w=140).pack(side="left", padx=10)

        # ── Content area (rebuilt on each Load) ───────────────────────────────
        content_host = ctk.CTkFrame(wrap, fg_color="transparent")
        content_host.pack(fill="both", expand=True)

        # ─────────────────────────────────────────────────────────────────────
        def _render_all(d):
            for w in content_host.winfo_children():
                w.destroy()
            _render_sales(d)
            _render_inventory(d)
            _render_expenditure(d)
            _render_samples(d)

        # ── HELPER: coloured action icon button ───────────────────────────────
        def _icon_btn(parent, text, cmd, fg, hv):
            return ctk.CTkButton(parent, text=text, width=30, height=28,
                                 corner_radius=6, fg_color=fg, hover_color=hv,
                                 font=ctk.CTkFont(size=13), command=cmd)

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 1 — SALES
        # ══════════════════════════════════════════════════════════════════════
        def _render_sales(d):
            sc = card(content_host); sc.pack(fill="x", pady=(0, 14))
            hb = band(sc, "💰  Sales Records")
            btn(hb, "＋  Add Sale", lambda: _modal_add_sale(d, lambda: _render_all(d)),
                fg=GREEN, hv=DGREEN, h=28, w=110).pack(side="right", padx=10)

            with get_db() as conn:
                rows = conn.execute(
                    "SELECT s.id, s.meal, s.sp, s.sold, s.wastage, s.cogs, s.payment "
                    "FROM sales s WHERE s.date=? ORDER BY s.id", (d,)).fetchall()

            if not rows:
                lbl(sc, "  No sales records for this date.", size=11, color=MID).pack(pady=12, anchor="w", padx=18)
                return

            # Header
            hf = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0, height=30)
            hf.pack(fill="x"); hf.pack_propagate(False)
            for txt, w in [("Meal",260),("Rate ₹",70),("Prepared",80),("Sold",60),
                           ("Wastage",70),("Expenditure ₹",110),("Payment",70),("Actions",0)]:
                lbl(hf, txt, size=9, weight="bold", color=MID).pack(side="left", padx=10)
                if w > 0:
                    ctk.CTkFrame(hf, fg_color="transparent", width=max(0,w-80)).pack(side="left")

            for ix, r in enumerate(rows):
                bg2 = WHITE if ix % 2 == 0 else STRIPE
                rf = ctk.CTkFrame(sc, fg_color=bg2, corner_radius=0, height=44)
                rf.pack(fill="x"); rf.pack_propagate(False)

                # wastage from batch_prep
                with get_db() as conn:
                    bp = conn.execute(
                        "SELECT qty_prepared FROM batch_prep WHERE date=? AND menu_id=("
                        "SELECT id FROM menu WHERE name=? COLLATE NOCASE LIMIT 1)",
                        (d, r["meal"])).fetchone()
                prep_qty = bp["qty_prepared"] if bp else (r["sold"] + r["wastage"])

                for val, w2 in [(r["meal"],260),(f"₹{r['sp']:.0f}",70),
                                (str(prep_qty),80),(str(r["sold"]),60),
                                (str(r["wastage"]),70),(f"₹{r['cogs']:,.0f}",110),
                                (r["payment"],70)]:
                    cf = ctk.CTkFrame(rf, fg_color="transparent", width=w2)
                    cf.pack(side="left", fill="y"); cf.pack_propagate(False)
                    lbl(cf, val, size=10, color=DARK).pack(anchor="w", padx=10, pady=4)

                af = ctk.CTkFrame(rf, fg_color="transparent")
                af.pack(side="right", padx=8, fill="y")

                _icon_btn(af, "🗑",
                          lambda rid=r["id"], nm=r["meal"]: _delete_sale(d, rid, nm, lambda: _render_all(d)),
                          "#FEE2E2", "#FECACA").pack(side="right", padx=(4,0))
                _icon_btn(af, "✏️",
                          lambda rid=r["id"], nm=r["meal"], sp=r["sp"], sold=r["sold"],
                                 wast=r["wastage"], cogs=r["cogs"], pmt=r["payment"], prep=prep_qty:
                              _modal_edit_sale(d, rid, nm, sp, prep, sold, wast, cogs, pmt, lambda: _render_all(d)),
                          BG_BLU, T_BLU).pack(side="right", padx=(4,0))

        # ──── Sales modal helpers ──────────────────────────────────────────────
        def _modal_edit_sale(d, sale_id, meal, sp, prep, sold, wastage, cogs, payment, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=540, height=500)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  ✏️  Edit Sale — {meal}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            fields = [
                ("Meal Name",       meal,           "meal_e"),
                ("Rate (₹)",        str(int(sp)),   "sp_e"),
                ("Qty Prepared",    str(prep),      "prep_e"),
                ("Qty Sold",        str(sold),      "sold_e"),
                ("Wastage",         str(wastage),   "waste_e"),
                ("Expenditure (₹)", str(int(cogs)), "cogs_e"),
            ]
            widgets = {}
            for label_txt, default, key in fields:
                row_f = ctk.CTkFrame(body, fg_color="transparent")
                row_f.pack(fill="x", pady=5)
                lbl(row_f, label_txt, size=11, weight="bold", color=DARK, width=140).pack(side="left")
                e = ctk.CTkEntry(row_f, height=36, corner_radius=8)
                e.insert(0, default)
                e.pack(side="left", fill="x", expand=True, padx=(8, 0))
                widgets[key] = e

            pm_var = ctk.StringVar(value=payment)
            pm_f = ctk.CTkFrame(body, fg_color="transparent")
            pm_f.pack(fill="x", pady=5)
            lbl(pm_f, "Payment Mode", size=11, weight="bold", color=DARK, width=140).pack(side="left")
            ctk.CTkOptionMenu(pm_f, values=["Cash", "UPI", "Card"], variable=pm_var,
                              height=36, corner_radius=8).pack(side="left", padx=(8,0))

            def _save():
                try:
                    new_meal = widgets["meal_e"].get().strip()
                    new_sp   = float(widgets["sp_e"].get())
                    new_prep = int(float(widgets["prep_e"].get()))
                    new_sold = int(float(widgets["sold_e"].get()))
                    new_wast = int(float(widgets["waste_e"].get()))
                    new_cogs = float(widgets["cogs_e"].get())
                    new_pmt  = pm_var.get()
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Please enter valid numbers.")
                    return

                with get_db() as conn:
                    conn.execute(
                        "UPDATE sales SET meal=?, sp=?, sold=?, wastage=?, cogs=?, payment=? WHERE id=?",
                        (new_meal, new_sp, new_sold, new_wast, new_cogs, new_pmt, sale_id))
                    # Update menu selling price if it changed
                    conn.execute(
                        "UPDATE menu SET sp=?, cogs=? WHERE name=? COLLATE NOCASE",
                        (new_sp, (new_cogs / new_prep) if new_prep > 0 else 0, new_meal))
                    # Sync batch_prep qty
                    conn.execute(
                        "UPDATE batch_prep SET qty_prepared=? WHERE date=? AND menu_id=("
                        "SELECT id FROM menu WHERE name=? COLLATE NOCASE LIMIT 1)",
                        (new_prep, d, new_meal))
                    # Sync expenditure for this sale on this date (Raw Materials)
                    conn.execute(
                        "UPDATE expenditure SET amount=? WHERE date=? AND notes LIKE ?",
                        (new_cogs, d, f"%{new_meal}%"))

                overlay.destroy()
                self._toast(f"✅ Sale '{new_meal}' updated")
                refresh_cb()

            btn(body, "💾  Save Changes", _save, fg=GREEN, hv=DGREEN, h=42).pack(fill="x", pady=(16, 0))

        def _modal_add_sale(d, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=540, height=480)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  ＋  Add Sale — {d}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            fields = [
                ("Meal Name",        "",    "meal_e"),
                ("Rate (₹)",         "70",  "sp_e"),
                ("Qty Prepared",     "0",   "prep_e"),
                ("Qty Sold",         "0",   "sold_e"),
                ("Expenditure (₹)",  "0",   "cogs_e"),
            ]
            widgets = {}
            for label_txt, default, key in fields:
                row_f = ctk.CTkFrame(body, fg_color="transparent")
                row_f.pack(fill="x", pady=5)
                lbl(row_f, label_txt, size=11, weight="bold", color=DARK, width=140).pack(side="left")
                e = ctk.CTkEntry(row_f, height=36, corner_radius=8)
                if default:
                    e.insert(0, default)
                e.pack(side="left", fill="x", expand=True, padx=(8, 0))
                widgets[key] = e

            pm_var = ctk.StringVar(value="Cash")
            pm_f = ctk.CTkFrame(body, fg_color="transparent")
            pm_f.pack(fill="x", pady=5)
            lbl(pm_f, "Payment Mode", size=11, weight="bold", color=DARK, width=140).pack(side="left")
            ctk.CTkOptionMenu(pm_f, values=["Cash", "UPI", "Card"], variable=pm_var,
                              height=36, corner_radius=8).pack(side="left", padx=(8,0))

            def _save_new():
                try:
                    new_meal = widgets["meal_e"].get().strip()
                    if not new_meal:
                        self._popup("⚠️ Missing", "Meal name is required."); return
                    new_sp   = float(widgets["sp_e"].get())
                    new_prep = int(float(widgets["prep_e"].get()))
                    new_sold = int(float(widgets["sold_e"].get()))
                    new_cogs = float(widgets["cogs_e"].get())
                    new_pmt  = pm_var.get()
                    new_wast = max(0, new_prep - new_sold)
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Please enter valid numbers.")
                    return

                cpu = (new_cogs / new_prep) if new_prep > 0 else 0
                with get_db() as conn:
                    m = conn.execute("SELECT id FROM menu WHERE name=? COLLATE NOCASE", (new_meal,)).fetchone()
                    if m:
                        menu_id = m[0]
                        conn.execute("UPDATE menu SET sp=?, cogs=? WHERE id=?", (new_sp, cpu, menu_id))
                    else:
                        cur = conn.execute("INSERT INTO menu (name, sp, active, cogs) VALUES (?,?,1,?)",
                                           (new_meal, new_sp, cpu))
                        menu_id = cur.lastrowid
                    conn.execute(
                        "INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment) "
                        "VALUES (?,?,?,?,?,?,?,?)",
                        (d, menu_id, new_meal, new_sp, new_sold, new_wast, new_cogs, new_pmt))
                    conn.execute("INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                                 (d, menu_id, new_prep))
                    conn.execute("INSERT INTO expenditure (date, amount, category, notes) VALUES (?,?,?,?)",
                                 (d, new_cogs, "Raw Materials", f"Auto-expenditure for {new_meal} batch"))

                overlay.destroy()
                self._toast(f"✅ Sale '{new_meal}' added")
                refresh_cb()

            btn(body, "💾  Add Sale", _save_new, fg=GREEN, hv=DGREEN, h=42).pack(fill="x", pady=(16, 0))

        def _delete_sale(d, sale_id, meal, refresh_cb):
            if self._confirm("Delete Sale", f"Delete sale record for '{meal}' on {d}?\nThis cannot be undone."):
                with get_db() as conn:
                    conn.execute("DELETE FROM sales WHERE id=?", (sale_id,))
                self._toast(f"🗑  Deleted sale '{meal}'")
                refresh_cb()

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 2 — INVENTORY
        # ══════════════════════════════════════════════════════════════════════
        def _render_inventory(d):
            ic = card(content_host); ic.pack(fill="x", pady=(0, 14))
            hb = band(ic, "📦  Inventory Records")
            btn(hb, "＋  Add Item", lambda: _modal_add_inv(d, lambda: _render_all(d)),
                fg=GREEN, hv=DGREEN, h=28, w=110).pack(side="right", padx=10)

            with get_db() as conn:
                rows = conn.execute(
                    "SELECT DISTINCT i.id, i.item, i.cat, i.unit, i.cp, i.stock,"
                    " COALESCE((SELECT qty_change FROM stock_ledger WHERE inv_id=i.id AND date=? AND transaction_type='Opening' LIMIT 1), 0) AS opening,"
                    " COALESCE((SELECT qty_change FROM stock_ledger WHERE inv_id=i.id AND date=? AND transaction_type='Received' LIMIT 1), 0) AS received,"
                    " COALESCE(ABS((SELECT qty_change FROM stock_ledger WHERE inv_id=i.id AND date=? AND transaction_type='Batch_Prep' LIMIT 1)), 0) AS issued"
                    " FROM inventory i"
                    " WHERE EXISTS (SELECT 1 FROM stock_ledger sl WHERE sl.inv_id=i.id AND sl.date=?)"
                    " ORDER BY i.cat, i.item",
                    (d, d, d, d)).fetchall()

            if not rows:
                lbl(ic, "  No inventory records linked to this date.", size=11, color=MID).pack(pady=12, anchor="w", padx=18)
                return

            # Header
            hf = ctk.CTkFrame(ic, fg_color=STRIPE, corner_radius=0, height=30)
            hf.pack(fill="x"); hf.pack_propagate(False)
            for txt, w in [("Item",200),("Cat",70),("Unit",50),("Rate ₹",70),
                           ("Opening",70),("Received",80),("Issued",70),("Closing",70),("Actions",0)]:
                lbl(hf, txt, size=9, weight="bold", color=MID).pack(side="left", padx=10)
                if w > 0:
                    ctk.CTkFrame(hf, fg_color="transparent", width=max(0,w-70)).pack(side="left")

            for ix, r in enumerate(rows):
                bg2 = WHITE if ix % 2 == 0 else STRIPE
                closing = r["opening"] + r["received"] - r["issued"]
                rf = ctk.CTkFrame(ic, fg_color=bg2, corner_radius=0, height=44)
                rf.pack(fill="x"); rf.pack_propagate(False)

                for val, w2 in [(r["item"],200),(r["cat"],70),(r["unit"],50),(f"₹{r['cp']:.2f}",70),
                                (f"{r['opening']:.2f}",70),(f"{r['received']:.2f}",80),
                                (f"{r['issued']:.2f}",70),(f"{closing:.2f}",70)]:
                    cf = ctk.CTkFrame(rf, fg_color="transparent", width=w2)
                    cf.pack(side="left", fill="y"); cf.pack_propagate(False)
                    lbl(cf, val, size=10, color=DARK).pack(anchor="w", padx=10, pady=4)

                af = ctk.CTkFrame(rf, fg_color="transparent")
                af.pack(side="right", padx=8, fill="y")
                _icon_btn(af, "🗑",
                          lambda iid=r["id"], nm=r["item"]: _delete_inv(d, iid, nm, lambda: _render_all(d)),
                          "#FEE2E2", "#FECACA").pack(side="right", padx=(4,0))
                _icon_btn(af, "✏️",
                          lambda iid=r["id"], nm=r["item"], cat=r["cat"], unit=r["unit"],
                                 cp=r["cp"], op=r["opening"], rec=r["received"], iss=r["issued"]:
                              _modal_edit_inv(d, iid, nm, cat, unit, cp, op, rec, iss, lambda: _render_all(d)),
                          BG_BLU, T_BLU).pack(side="right", padx=(4,0))

        # ──── Inventory modal helpers ──────────────────────────────────────────
        def _modal_edit_inv(d, inv_id, item, cat, unit, cp, opening, received, issued, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=560, height=530)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  ✏️  Edit Inventory — {item}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            fields = [
                ("Item Name",   item,          "name_e"),
                ("Category",    cat,           "cat_e"),
                ("Unit",        unit,          "unit_e"),
                ("Rate (₹)",    f"{cp:.2f}",   "cp_e"),
                ("Opening",     f"{opening:.3f}", "op_e"),
                ("Received",    f"{received:.3f}","rec_e"),
                ("Issued",      f"{issued:.3f}", "iss_e"),
            ]
            widgets = {}
            for label_txt, default, key in fields:
                row_f = ctk.CTkFrame(body, fg_color="transparent")
                row_f.pack(fill="x", pady=4)
                lbl(row_f, label_txt, size=11, weight="bold", color=DARK, width=100).pack(side="left")
                e = ctk.CTkEntry(row_f, height=36, corner_radius=8)
                e.insert(0, default)
                e.pack(side="left", fill="x", expand=True, padx=(8, 0))
                widgets[key] = e

            closing_lbl = lbl(body, f"Closing = {opening + received - issued:.3f}",
                              size=11, weight="bold", color=BLUE)
            closing_lbl.pack(anchor="w", pady=(4, 0))

            def _on_change(*_):
                try:
                    op  = float(widgets["op_e"].get())
                    rec = float(widgets["rec_e"].get())
                    iss = float(widgets["iss_e"].get())
                    closing_lbl.configure(text=f"Closing = {op + rec - iss:.3f}")
                except Exception:
                    pass

            for key in ("op_e", "rec_e", "iss_e"):
                widgets[key].bind("<KeyRelease>", _on_change)

            def _save():
                try:
                    new_name = widgets["name_e"].get().strip()
                    new_cat  = widgets["cat_e"].get().strip()
                    new_unit = widgets["unit_e"].get().strip()
                    new_cp   = float(widgets["cp_e"].get())
                    new_op   = float(widgets["op_e"].get())
                    new_rec  = float(widgets["rec_e"].get())
                    new_iss  = float(widgets["iss_e"].get())
                    new_bcf  = new_op + new_rec - new_iss
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Please enter valid numbers.")
                    return

                with get_db() as conn:
                    # Update inventory master (closing stock = new_bcf)
                    conn.execute(
                        "UPDATE inventory SET item=?, cat=?, unit=?, cp=?, stock=? WHERE id=?",
                        (new_name, new_cat, new_unit, new_cp, new_bcf, inv_id))

                    # Re-sync stock_ledger for this date
                    conn.execute("DELETE FROM stock_ledger WHERE inv_id=? AND date=?", (inv_id, d))
                    if new_op != 0:
                        conn.execute(
                            "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Opening',?,'Opening balance BBF')", (d, inv_id, new_op))
                    if new_rec > 0:
                        conn.execute(
                            "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Received',?,'Stock Received')", (d, inv_id, new_rec))
                    if new_iss > 0:
                        conn.execute(
                            "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Batch_Prep',?,'Material used for production')", (d, inv_id, -new_iss))

                overlay.destroy()
                self._toast(f"✅ Inventory '{new_name}' updated")
                refresh_cb()

            btn(body, "💾  Save Changes", _save, fg=GREEN, hv=DGREEN, h=42).pack(fill="x", pady=(12, 0))

        def _modal_add_inv(d, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=560, height=510)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  ＋  Add Inventory — {d}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            fields = [
                ("Item Name",  "",    "name_e"),
                ("Category",   "Dry", "cat_e"),
                ("Unit",       "Kgs", "unit_e"),
                ("Rate (₹)",   "0",   "cp_e"),
                ("Opening",    "0",   "op_e"),
                ("Received",   "0",   "rec_e"),
                ("Issued",     "0",   "iss_e"),
            ]
            widgets = {}
            for label_txt, default, key in fields:
                row_f = ctk.CTkFrame(body, fg_color="transparent")
                row_f.pack(fill="x", pady=4)
                lbl(row_f, label_txt, size=11, weight="bold", color=DARK, width=100).pack(side="left")
                e = ctk.CTkEntry(row_f, height=36, corner_radius=8)
                if default:
                    e.insert(0, default)
                e.pack(side="left", fill="x", expand=True, padx=(8, 0))
                widgets[key] = e

            def _save_new():
                try:
                    new_name = widgets["name_e"].get().strip()
                    if not new_name:
                        self._popup("⚠️ Missing", "Item name is required."); return
                    new_cat  = widgets["cat_e"].get().strip() or "Dry"
                    new_unit = widgets["unit_e"].get().strip() or "Kgs"
                    new_cp   = float(widgets["cp_e"].get())
                    new_op   = float(widgets["op_e"].get())
                    new_rec  = float(widgets["rec_e"].get())
                    new_iss  = float(widgets["iss_e"].get())
                    new_bcf  = new_op + new_rec - new_iss
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Please enter valid numbers.")
                    return

                with get_db() as conn:
                    existing = conn.execute("SELECT id FROM inventory WHERE item=? COLLATE NOCASE", (new_name,)).fetchone()
                    if existing:
                        inv_id = existing[0]
                        conn.execute("UPDATE inventory SET cat=?, unit=?, cp=?, stock=? WHERE id=?",
                                     (new_cat, new_unit, new_cp, new_bcf, inv_id))
                    else:
                        cur = conn.execute(
                            "INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated) "
                            "VALUES (?,?,?,?,0.0,?,?,?,?)",
                            (new_name, new_cat, new_unit, new_bcf, new_op, new_rec, new_cp, d))
                        inv_id = cur.lastrowid

                    conn.execute("DELETE FROM stock_ledger WHERE inv_id=? AND date=?", (inv_id, d))
                    if new_op != 0:
                        conn.execute(
                            "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Opening',?,'Opening balance BBF')", (d, inv_id, new_op))
                    if new_rec > 0:
                        conn.execute(
                            "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Received',?,'Stock Received')", (d, inv_id, new_rec))
                    if new_iss > 0:
                        conn.execute(
                            "INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,'Batch_Prep',?,'Material used for production')", (d, inv_id, -new_iss))

                overlay.destroy()
                self._toast(f"✅ Inventory '{new_name}' added")
                refresh_cb()

            btn(body, "💾  Add Item", _save_new, fg=GREEN, hv=DGREEN, h=42).pack(fill="x", pady=(12, 0))

        def _delete_inv(d, inv_id, item, refresh_cb):
            if self._confirm("Delete Inventory Record",
                             f"Remove all stock_ledger entries for '{item}' on {d}?\n"
                             f"(The inventory item itself is NOT deleted.)"):
                with get_db() as conn:
                    conn.execute("DELETE FROM stock_ledger WHERE inv_id=? AND date=?", (inv_id, d))
                self._toast(f"🗑  Removed ledger entries for '{item}' on {d}")
                refresh_cb()

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 3 — EXPENDITURE
        # ══════════════════════════════════════════════════════════════════════
        def _render_expenditure(d):
            ec = card(content_host); ec.pack(fill="x", pady=(0, 14))
            hb = band(ec, "💸  Expenditure Records")
            btn(hb, "＋  Add Entry", lambda: _modal_add_exp(d, lambda: _render_all(d)),
                fg=GREEN, hv=DGREEN, h=28, w=110).pack(side="right", padx=10)

            with get_db() as conn:
                rows = conn.execute(
                    "SELECT id, amount, category, notes FROM expenditure WHERE date=? ORDER BY id",
                    (d,)).fetchall()

            if not rows:
                lbl(ec, "  No expenditure records for this date.", size=11, color=MID).pack(pady=12, anchor="w", padx=18)
                return

            hf = ctk.CTkFrame(ec, fg_color=STRIPE, corner_radius=0, height=30)
            hf.pack(fill="x"); hf.pack_propagate(False)
            for txt, w in [("Category",150),("Amount ₹",100),("Notes",0),("Actions",0)]:
                lbl(hf, txt, size=9, weight="bold", color=MID).pack(side="left", padx=10)
                if w > 0:
                    ctk.CTkFrame(hf, fg_color="transparent", width=max(0,w-60)).pack(side="left")

            for ix, r in enumerate(rows):
                bg2 = WHITE if ix % 2 == 0 else STRIPE
                rf = ctk.CTkFrame(ec, fg_color=bg2, corner_radius=0, height=44)
                rf.pack(fill="x"); rf.pack_propagate(False)

                for val, w2 in [(r["category"],150),(f"₹{r['amount']:,.0f}",100),(str(r["notes"] or ""),0)]:
                    cf = ctk.CTkFrame(rf, fg_color="transparent", width=w2 if w2 else 300)
                    cf.pack(side="left", fill="y"); cf.pack_propagate(False)
                    lbl(cf, val, size=10, color=DARK).pack(anchor="w", padx=10, pady=4)

                af = ctk.CTkFrame(rf, fg_color="transparent")
                af.pack(side="right", padx=8, fill="y")
                _icon_btn(af, "🗑",
                          lambda eid=r["id"]: _delete_exp(eid, lambda: _render_all(d)),
                          "#FEE2E2", "#FECACA").pack(side="right", padx=(4,0))
                _icon_btn(af, "✏️",
                          lambda eid=r["id"], amt=r["amount"], cat=r["category"], notes=r["notes"]:
                              _modal_edit_exp(d, eid, amt, cat, notes, lambda: _render_all(d)),
                          BG_BLU, T_BLU).pack(side="right", padx=(4,0))

        def _modal_edit_exp(d, exp_id, amount, category, notes, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=520, height=380)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, "  ✏️  Edit Expenditure", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            row1 = ctk.CTkFrame(body, fg_color="transparent"); row1.pack(fill="x", pady=5)
            lbl(row1, "Category", size=11, weight="bold", color=DARK, width=100).pack(side="left")
            cat_e = ctk.CTkEntry(row1, height=36, corner_radius=8)
            cat_e.insert(0, category or "")
            cat_e.pack(side="left", fill="x", expand=True, padx=(8,0))

            row2 = ctk.CTkFrame(body, fg_color="transparent"); row2.pack(fill="x", pady=5)
            lbl(row2, "Amount (₹)", size=11, weight="bold", color=DARK, width=100).pack(side="left")
            amt_e = ctk.CTkEntry(row2, height=36, corner_radius=8)
            amt_e.insert(0, str(amount))
            amt_e.pack(side="left", fill="x", expand=True, padx=(8,0))

            row3 = ctk.CTkFrame(body, fg_color="transparent"); row3.pack(fill="x", pady=5)
            lbl(row3, "Notes", size=11, weight="bold", color=DARK, width=100).pack(side="left")
            notes_e = ctk.CTkEntry(row3, height=36, corner_radius=8)
            notes_e.insert(0, notes or "")
            notes_e.pack(side="left", fill="x", expand=True, padx=(8,0))

            def _save():
                try:
                    new_cat   = cat_e.get().strip() or "General"
                    new_amt   = float(amt_e.get())
                    new_notes = notes_e.get().strip()
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Amount must be a number."); return
                with get_db() as conn:
                    conn.execute(
                        "UPDATE expenditure SET category=?, amount=?, notes=? WHERE id=?",
                        (new_cat, new_amt, new_notes, exp_id))
                overlay.destroy()
                self._toast("✅ Expenditure updated")
                refresh_cb()

            btn(body, "💾  Save Changes", _save, fg=GREEN, hv=DGREEN, h=42).pack(fill="x", pady=(16,0))

        def _modal_add_exp(d, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=520, height=360)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=SAFFRON, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  ＋  Add Expenditure — {d}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            row1 = ctk.CTkFrame(body, fg_color="transparent"); row1.pack(fill="x", pady=5)
            lbl(row1, "Category", size=11, weight="bold", color=DARK, width=100).pack(side="left")
            cat_e = ctk.CTkEntry(row1, height=36, corner_radius=8)
            cat_e.insert(0, "Raw Materials")
            cat_e.pack(side="left", fill="x", expand=True, padx=(8,0))

            row2 = ctk.CTkFrame(body, fg_color="transparent"); row2.pack(fill="x", pady=5)
            lbl(row2, "Amount (₹)", size=11, weight="bold", color=DARK, width=100).pack(side="left")
            amt_e = ctk.CTkEntry(row2, height=36, corner_radius=8)
            amt_e.pack(side="left", fill="x", expand=True, padx=(8,0))

            row3 = ctk.CTkFrame(body, fg_color="transparent"); row3.pack(fill="x", pady=5)
            lbl(row3, "Notes", size=11, weight="bold", color=DARK, width=100).pack(side="left")
            notes_e = ctk.CTkEntry(row3, height=36, corner_radius=8)
            notes_e.pack(side="left", fill="x", expand=True, padx=(8,0))

            def _save_new():
                try:
                    new_cat   = cat_e.get().strip() or "General"
                    new_amt   = float(amt_e.get())
                    new_notes = notes_e.get().strip()
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Amount must be a number."); return
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO expenditure (date, amount, category, notes) VALUES (?,?,?,?)",
                        (d, new_amt, new_cat, new_notes))
                overlay.destroy()
                self._toast("✅ Expenditure added")
                refresh_cb()

            btn(body, "💾  Add Entry", _save_new, fg=GREEN, hv=DGREEN, h=42).pack(fill="x", pady=(16,0))

        def _delete_exp(exp_id, refresh_cb):
            if self._confirm("Delete Expenditure", "Delete this expenditure entry?\nThis cannot be undone."):
                with get_db() as conn:
                    conn.execute("DELETE FROM expenditure WHERE id=?", (exp_id,))
                self._toast("🗑  Expenditure deleted")
                refresh_cb()

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 4 — SAMPLES / COMPLIMENTARY ITEMS
        # ══════════════════════════════════════════════════════════════════════
        def _render_samples(d):
            sc = card(content_host); sc.pack(fill="x", pady=(0, 14))
            hb = band(sc, "🎁  Sample Complimentary", bg=ARMY_BG, tc=GOLD_LT)
            btn(hb, "＋  Add Sample", lambda: _modal_add_sample(d, lambda: _render_all(d)),
                fg=TEAL, hv="#0F766E", h=28, w=120).pack(side="right", padx=10)

            with get_db() as conn:
                rows = conn.execute(
                    "SELECT * FROM samples WHERE date=? ORDER BY id", (d,)).fetchall()

            if not rows:
                lbl(sc, "  No samples recorded for this date.", size=11, color=MID).pack(
                    pady=12, anchor="w", padx=18)
                return

            # Header
            hf = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=0, height=30)
            hf.pack(fill="x"); hf.pack_propagate(False)
            for txt, w in [("Item",220),("Qty",60),("Rate ₹",70),("Cost ₹",90),("Given To",130),("Notes",0),("Actions",0)]:
                lbl(hf, txt, size=9, weight="bold", color=MID).pack(side="left", padx=10)
                if w > 0:
                    ctk.CTkFrame(hf, fg_color="transparent", width=max(0,w-70)).pack(side="left")

            for ix, r in enumerate(rows):
                bg2 = WHITE if ix % 2 == 0 else STRIPE
                rf = ctk.CTkFrame(sc, fg_color=bg2, corner_radius=0, height=44)
                rf.pack(fill="x"); rf.pack_propagate(False)

                for val, w2 in [(r["meal"],220),(str(r["qty"]),60),(f"₹{r['sp']:.0f}",70),
                                (f"₹{r['cost']:,.0f}",90),(r["given_to"] or "General",130),
                                (str(r["notes"] or ""),0)]:
                    cf = ctk.CTkFrame(rf, fg_color="transparent", width=w2 if w2 else 200)
                    cf.pack(side="left", fill="y"); cf.pack_propagate(False)
                    lbl(cf, val, size=10, color=DARK).pack(anchor="w", padx=10, pady=4)

                af = ctk.CTkFrame(rf, fg_color="transparent")
                af.pack(side="right", padx=8, fill="y")
                _icon_btn(af, "🗑",
                          lambda sid=r["id"], nm=r["meal"]: _delete_sample(sid, nm, lambda: _render_all(d)),
                          "#FEE2E2", "#FECACA").pack(side="right", padx=(4,0))
                _icon_btn(af, "✏️",
                          lambda sid=r["id"], nm=r["meal"], sp=r["sp"], qty=r["qty"],
                                 cost=r["cost"], gt=r["given_to"], notes=r["notes"]:
                              _modal_edit_sample(d, sid, nm, sp, qty, cost, gt, notes, lambda: _render_all(d)),
                          BG_TEA, T_TEA).pack(side="right", padx=(4,0))

        def _modal_edit_sample(d, samp_id, meal, sp, qty, cost, given_to, notes, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=520, height=460)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=TEAL, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  🎁  Edit Sample — {meal}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            fields = [
                ("Item Name",    meal,              "meal_e"),
                ("Rate (₹)",     str(int(sp)),      "sp_e"),
                ("Qty (samples)",str(qty),          "qty_e"),
                ("Cost (₹)",     str(int(cost)),    "cost_e"),
                ("Given To",     given_to or "General", "gt_e"),
                ("Notes",        notes or "",       "notes_e"),
            ]
            widgets = {}
            for label_txt, default, key in fields:
                row_f = ctk.CTkFrame(body, fg_color="transparent")
                row_f.pack(fill="x", pady=4)
                lbl(row_f, label_txt, size=11, weight="bold", color=DARK, width=120).pack(side="left")
                e = ctk.CTkEntry(row_f, height=36, corner_radius=8)
                e.insert(0, default)
                e.pack(side="left", fill="x", expand=True, padx=(8, 0))
                widgets[key] = e

            def _save():
                try:
                    new_meal = widgets["meal_e"].get().strip()
                    new_sp   = float(widgets["sp_e"].get())
                    new_qty  = int(float(widgets["qty_e"].get()))
                    new_cost = float(widgets["cost_e"].get())
                    new_gt   = widgets["gt_e"].get().strip() or "General"
                    new_notes= widgets["notes_e"].get().strip()
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Please enter valid numbers."); return
                with get_db() as conn:
                    conn.execute(
                        "UPDATE samples SET meal=?, sp=?, qty=?, cost=?, given_to=?, notes=? WHERE id=?",
                        (new_meal, new_sp, new_qty, new_cost, new_gt, new_notes, samp_id))
                overlay.destroy()
                self._toast(f"✅ Sample '{new_meal}' updated")
                refresh_cb()

            btn(body, "💾  Save Changes", _save, fg=TEAL, hv="#0F766E", h=42).pack(fill="x", pady=(12, 0))

        def _modal_add_sample(d, refresh_cb):
            overlay = tk.Frame(self._area, bg="#1E293B")
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            mc = ctk.CTkFrame(overlay, fg_color=WHITE, corner_radius=20,
                              border_width=2, border_color=ARMY_BG, width=520, height=440)
            mc.place(relx=0.5, rely=0.5, anchor="center")
            mc.pack_propagate(False)

            hbar = ctk.CTkFrame(mc, fg_color=ARMY_BG, corner_radius=0, height=52)
            hbar.pack(fill="x"); hbar.pack_propagate(False)
            ctk.CTkFrame(hbar, fg_color=TEAL, width=4, corner_radius=0).pack(side="left", fill="y")
            lbl(hbar, f"  ＋  Add Sample — {d}", size=13, weight="bold", color=WHITE).pack(side="left", padx=10)
            ctk.CTkButton(hbar, text="✕", width=36, height=36, corner_radius=8,
                          fg_color="transparent", hover_color=ARMY_HVR,
                          text_color=GOLD_LT, font=ctk.CTkFont(size=14, weight="bold"),
                          command=overlay.destroy).pack(side="right", padx=8)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="both", expand=True, padx=24, pady=18)

            fields = [
                ("Item Name",    "",        "meal_e"),
                ("Rate (₹)",     "25",      "sp_e"),
                ("Qty (samples)","0",       "qty_e"),
                ("Cost (₹)",     "0",       "cost_e"),
                ("Given To",     "General", "gt_e"),
                ("Notes",        "",        "notes_e"),
            ]
            widgets = {}
            for label_txt, default, key in fields:
                row_f = ctk.CTkFrame(body, fg_color="transparent")
                row_f.pack(fill="x", pady=4)
                lbl(row_f, label_txt, size=11, weight="bold", color=DARK, width=120).pack(side="left")
                e = ctk.CTkEntry(row_f, height=36, corner_radius=8)
                if default:
                    e.insert(0, default)
                e.pack(side="left", fill="x", expand=True, padx=(8, 0))
                widgets[key] = e

            def _save_new():
                try:
                    new_meal = widgets["meal_e"].get().strip()
                    if not new_meal:
                        self._popup("⚠️ Missing", "Item name is required."); return
                    new_sp   = float(widgets["sp_e"].get())
                    new_qty  = int(float(widgets["qty_e"].get()))
                    new_cost = float(widgets["cost_e"].get())
                    new_gt   = widgets["gt_e"].get().strip() or "General"
                    new_notes= widgets["notes_e"].get().strip()
                except ValueError:
                    self._popup("⚠️ Invalid Input", "Please enter valid numbers."); return

                with get_db() as conn:
                    m = conn.execute("SELECT id FROM menu WHERE name=? COLLATE NOCASE", (new_meal,)).fetchone()
                    menu_id = m[0] if m else None
                    conn.execute(
                        "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                        "VALUES (?,?,?,?,?,?,?,?)",
                        (d, menu_id, new_meal, new_sp, new_qty, new_cost, new_gt, new_notes))
                overlay.destroy()
                self._toast(f"✅ Sample '{new_meal}' added")
                refresh_cb()

            btn(body, "💾  Add Sample", _save_new, fg=TEAL, hv="#0F766E", h=42).pack(fill="x", pady=(12, 0))

        def _delete_sample(samp_id, meal, refresh_cb):
            if self._confirm("Delete Sample", f"Delete sample record for '{meal}'?\nThis cannot be undone."):
                with get_db() as conn:
                    conn.execute("DELETE FROM samples WHERE id=?", (samp_id,))
                self._toast(f"🗑  Sample '{meal}' deleted")
                refresh_cb()

        # ── Initial render ────────────────────────────────────────────────────
        _render_all(self._edit_date)

    def _pg_import(self):
        import csv, io
        self._hdr("📥  Import Data",
                  "Import Inventory items or Menu items from a CSV file")

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(14, PAD))

        # ── Instructions card ─────────────────────────────────────────────────
        ic = card(wrap); ic.pack(fill="x", pady=(0, 14))
        band(ic, "📋  How to Import")
        body_i = ctk.CTkFrame(ic, fg_color="transparent")
        body_i.pack(fill="x", padx=18, pady=14)
        steps = [
            "1️⃣  Choose what to import: Inventory Items  OR  Menu Items",
            "2️⃣  Click 'Download Template' to get a pre-formatted CSV file",
            "3️⃣  Fill in your data in the CSV (open with Excel or Google Sheets)",
            "4️⃣  Click 'Choose File & Import' — data is added instantly",
        ]
        for s in steps:
            lbl(body_i, s, size=11, color=DARK).pack(anchor="w", pady=2)

        sep(body_i, BORDER).pack(fill="x", pady=(10, 6))
        lbl(body_i, "⚠  Duplicate item names are skipped automatically.",
            size=10, color=ORANGE).pack(anchor="w")

        # ── Import Type selector ──────────────────────────────────────────────
        tc = card(wrap); tc.pack(fill="x", pady=(0, 14))
        band(tc, "🔀  Select Import Type")
        tf = ctk.CTkFrame(tc, fg_color="transparent")
        tf.pack(fill="x", padx=18, pady=14)

        import_type = ctk.StringVar(value="inventory")
        ctk.CTkRadioButton(tf, text="📦  Inventory Items (item, category, unit, opening_stock, min_level, cost_price)",
                           variable=import_type, value="inventory",
                           font=ctk.CTkFont(size=11), text_color=DARK,
                           fg_color=GREEN).pack(anchor="w", pady=4)
        ctk.CTkRadioButton(tf, text="🍽  Menu Items (name, selling_price)",
                           variable=import_type, value="menu",
                           font=ctk.CTkFont(size=11), text_color=DARK,
                           fg_color=GREEN).pack(anchor="w", pady=4)

        # ── Template download ─────────────────────────────────────────────────
        def download_template():
            t = import_type.get()
            if t == "inventory":
                header = "item,category,unit,opening_stock,min_level,cost_price\n"
                sample = ("Atta,Dry,kg,50,10,35\n"
                          "Mustard Oil,Dry,ltr,20,5,120\n"
                          "Tomato,Fresh,kg,15,3,30\n")
                fname = "inventory_template.csv"
            else:
                header = "name,selling_price\n"
                sample = ("Dal Tadka Thali,80\n"
                          "Chole Bhature,60\n"
                          "Veg Pulao,55\n")
                fname = "menu_template.csv"
            path = filedialog.asksaveasfilename(
                defaultextension=".csv", initialfile=fname,
                filetypes=[("CSV Files", "*.csv")])
            if path:
                with open(path, "w") as f:
                    f.write(header + sample)
                self._toast(f"✅ Template saved: {os.path.basename(path)}")

        btn(tc, "⬇  Download CSV Template", download_template,
            fg=BLUE, hv=DBLUE, h=40).pack(padx=18, pady=(0, 14), fill="x")

        # ── Preview area ──────────────────────────────────────────────────────
        pc = card(wrap); pc.pack(fill="both", expand=True)
        band(pc, "👁  Preview & Import")
        pf = ctk.CTkFrame(pc, fg_color="transparent")
        pf.pack(fill="both", expand=True, padx=18, pady=14)

        preview_lbl = lbl(pf, "No file selected. Click below to choose a CSV file.",
                          size=11, color=MID)
        preview_lbl.pack(anchor="w", pady=(0, 10))

        prev_box = ctk.CTkScrollableFrame(pf, fg_color=STRIPE,
                                          corner_radius=8, height=180)
        prev_box.pack(fill="x", pady=(0, 12))
        lbl(prev_box, "  — preview will appear here —",
            size=10, color=MID).pack(pady=20)

        result_lbl = lbl(pf, "", size=11, color=GREEN)
        result_lbl.pack(anchor="w")

        def choose_and_import():
            path = filedialog.askopenfilename(
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
            if not path:
                return

            # Parse CSV
            try:
                with open(path, newline="", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
            except Exception as e:
                self._popup("⚠️ Read Error", str(e)); return

            if not rows:
                self._popup("⚠️ Empty File", "The CSV has no data rows."); return

            # Clear preview box
            for w in prev_box.winfo_children(): w.destroy()
            preview_lbl.configure(
                text=f"File: {os.path.basename(path)}  •  {len(rows)} rows found",
                text_color=DARK)

            # Show preview table
            t = import_type.get()
            if t == "inventory":
                cols = ["item","category","unit","opening_stock","min_level","cost_price"]
            else:
                cols = ["name","selling_price"]

            hdr_f = ctk.CTkFrame(prev_box, fg_color=ARMY_BG, corner_radius=0, height=28)
            hdr_f.pack(fill="x"); hdr_f.pack_propagate(False)
            for col in cols:
                lbl(hdr_f, col.replace("_"," ").title(), size=9,
                    weight="bold", color=GOLD_LT).pack(side="left", expand=True, fill="x", padx=8)

            for ix, row in enumerate(rows[:20]):
                rf = ctk.CTkFrame(prev_box, fg_color=WHITE if ix%2==0 else STRIPE,
                                  corner_radius=0, height=26)
                rf.pack(fill="x"); rf.pack_propagate(False)
                for col in cols:
                    val = row.get(col, row.get(col.replace("_"," "), "—"))
                    lbl(rf, str(val)[:20], size=9, color=DARK).pack(
                        side="left", expand=True, fill="x", padx=8)

            if len(rows) > 20:
                lbl(prev_box, f"  … and {len(rows)-20} more rows",
                    size=9, color=MID).pack(anchor="w", padx=8, pady=4)

            # Perform import
            imported = 0; skipped = 0
            with get_db() as conn:
                if t == "inventory":
                    for row in rows:
                        try:
                            nm  = str(row.get("item","")).strip()
                            cat = str(row.get("category","Dry")).strip()
                            unit = str(row.get("unit","kg")).strip()
                            stk = float(row.get("opening_stock", 0) or 0)
                            mn  = float(row.get("min_level", 0) or 0)
                            cp  = float(row.get("cost_price", 0) or 0)
                            if not nm: skipped += 1; continue
                            conn.execute(
                                "INSERT OR IGNORE INTO inventory "
                                "(item,cat,unit,stock,min_lvl,opening,received,cp) "
                                "VALUES (?,?,?,?,?,?,0,?)",
                                (nm, cat, unit, stk, mn, stk, cp))
                            if conn.execute("SELECT changes()").fetchone()[0]:
                                imported += 1
                            else:
                                skipped += 1
                        except Exception:
                            skipped += 1
                else:
                    for row in rows:
                        try:
                            nm = str(row.get("name","")).strip()
                            sp = float(row.get("selling_price", 0) or 0)
                            if not nm: skipped += 1; continue
                            conn.execute(
                                "INSERT OR IGNORE INTO menu (name,sp,active) VALUES (?,?,1)",
                                (nm, sp))
                            if conn.execute("SELECT changes()").fetchone()[0]:
                                imported += 1
                            else:
                                skipped += 1
                        except Exception:
                            skipped += 1

            msg = f"✅  {imported} rows imported"
            if skipped: msg += f"  •  {skipped} skipped (duplicates/errors)"
            result_lbl.configure(text=msg,
                                 text_color=GREEN if imported > 0 else ORANGE)
            self._toast(msg)

        btn(pf, "📂  Choose File & Import", choose_and_import,
            fg=GREEN, hv=DGREEN, h=46).pack(fill="x")

    def _pg_import_datewise(self):
        import csv, io
        self._hdr("📅  Import Datewise Statement",
                  "Import a full daily statement (Inventory + Sales) from a CSV file")

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(14, PAD))

        ic = card(wrap); ic.pack(fill="x", pady=(0, 14))
        band(ic, "📋  How to Import Datewise")
        body_i = ctk.CTkFrame(ic, fg_color="transparent")
        body_i.pack(fill="x", padx=18, pady=14)
        
        # Date selector for the import
        date_f = ctk.CTkFrame(body_i, fg_color="transparent")
        date_f.pack(fill="x", pady=(0, 10))
        lbl(date_f, "Select Date for Import (YYYY-MM-DD):", size=11, color=DARK, weight="bold").pack(side="left", padx=(0, 10))
        date_entry = ctk.CTkEntry(date_f, placeholder_text="YYYY-MM-DD", width=120)
        date_entry.pack(side="left")
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        steps = [
            "1️⃣  Enter the specific date above for this import.",
            "2️⃣  Click 'Download Template' to get the unified CSV structure.",
            "3️⃣  Fill the CSV with both Inventory rows and Sale rows.",
            "4️⃣  Click 'Choose File & Import'. This will automatically:",
            "      - Clear existing data for that specific date to prevent duplicates.",
            "      - Update Inventory stocks, log Received & Issue transactions.",
            "      - Log Sales, update COGS, and record Daily Expenditures.",
        ]
        for s in steps:
            lbl(body_i, s, size=11, color=DARK).pack(anchor="w", pady=2)

        # Template Download
        def dl_template():
            out_path = os.path.join(os.path.expanduser("~"), "Documents", "Datewise_Import_Template.csv")
            try:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(["Type", "Item Name", "Category", "Unit", "Opening", "Received", "Issue", "Closing", "Rate", "Prepared", "Sold", "Expenditure"])
                    w.writerow(["Inventory", "POTATO", "Fresh", "Kgs", "95.4", "0", "45.0", "50.4", "12.0", "", "", ""])
                    w.writerow(["Sale", "LUNCH", "", "", "", "", "", "", "70.0", "521", "520", "25521.0"])
                self._popup("✅ Template Saved", f"Saved to:\n{out_path}")
            except Exception as e:
                self._popup("❌ Error", f"Could not save template:\n{e}")

        # Processing Logic
        def do_import():
            d = date_entry.get().strip()
            if not d:
                self._popup("⚠️ Missing Date", "Please enter a valid date (YYYY-MM-DD).")
                return
            
            fpath = filedialog.askopenfilename(title="Select Datewise CSV",
                                               filetypes=[("CSV Files", "*.csv")])
            if not fpath: return

            try:
                with open(fpath, "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
            except Exception as e:
                self._popup("❌ File Error", f"Could not read CSV:\n{e}")
                return

            with get_db() as conn:
                try:
                    # Idempotent cleanup for this date
                    conn.execute("DELETE FROM sales WHERE date = ?", (d,))
                    conn.execute("DELETE FROM batch_prep WHERE date = ?", (d,))
                    conn.execute("DELETE FROM goods_received WHERE date = ?", (d,))
                    conn.execute("DELETE FROM expenditure WHERE date = ?", (d,))
                    conn.execute("DELETE FROM stock_ledger WHERE date = ?", (d,))

                    for r in rows:
                        rtype = r.get("Type", "").strip().lower()
                        item_name = r.get("Item Name", "").strip()
                        if not item_name or not rtype: continue

                        if rtype == "inventory":
                            cat = r.get("Category", "Dry")
                            unit = r.get("Unit", "Kgs")
                            try:
                                bbf = float(r.get("Opening", 0) or 0)
                                rec = float(r.get("Received", 0) or 0)
                                iss = float(r.get("Issue", 0) or 0)
                                bcf = float(r.get("Closing", 0) or 0)
                                rate = float(r.get("Rate", 0) or 0)
                            except: continue

                            # Update or Insert Inventory
                            cur = conn.execute("SELECT id, received FROM inventory WHERE item = ? COLLATE NOCASE", (item_name,))
                            row = cur.fetchone()
                            if row:
                                inv_id = row[0]
                                new_rec = (row[1] or 0.0) + rec
                                conn.execute("UPDATE inventory SET stock=?, cp=?, received=?, updated=? WHERE id=?",
                                             (bcf, rate, new_rec, d, inv_id))
                                # For existing items, always log Opening balance to stock_ledger
                                # so the daily report can compute correct closing stock for this date.
                                if bbf != 0:
                                    conn.execute("INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) VALUES (?,?,'Opening',?,'Opening balance BBF')",
                                                 (d, inv_id, bbf))
                            else:
                                cur = conn.execute("INSERT INTO inventory (item, cat, unit, stock, min_lvl, opening, received, cp, updated) VALUES (?,?,?,?,0.0,?,?,?,?)",
                                                   (item_name, cat, unit, bcf, bbf, rec, rate, d))
                                inv_id = cur.lastrowid
                                conn.execute("INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) VALUES (?,?,'Opening',?,'Opening balance BBF')",
                                             (d, inv_id, bbf))

                            if rec > 0:
                                conn.execute("INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) VALUES (?,?,'Received',?,'Stock Received')",
                                             (d, inv_id, rec))
                                conn.execute("INSERT INTO goods_received (date, inv_id, qty, total_cost) VALUES (?,?,?,?)",
                                             (d, inv_id, rec, rec * rate))
                            if iss > 0:
                                conn.execute("INSERT INTO stock_ledger (date, inv_id, transaction_type, qty_change, notes) VALUES (?,?,'Batch_Prep',?,'Material used for production')",
                                             (d, inv_id, -iss))

                        elif rtype == "sale":
                            try:
                                sp = float(r.get("Rate", 0) or 0)
                                prep = int(float(r.get("Prepared", 0) or 0))
                                sold = int(float(r.get("Sold", 0) or 0))
                                exp = float(r.get("Expenditure", 0) or 0)
                            except: continue

                            cur = conn.execute("SELECT id FROM menu WHERE name = ? COLLATE NOCASE", (item_name,))
                            m_row = cur.fetchone()
                            cpu = (exp / prep) if prep > 0 else 0
                            if m_row:
                                menu_id = m_row[0]
                                conn.execute("UPDATE menu SET cogs = ? WHERE id = ?", (cpu, menu_id))
                            else:
                                cur = conn.execute("INSERT INTO menu (name, sp, active, cogs) VALUES (?,?,1,?)",
                                                   (item_name, sp, cpu))
                                menu_id = cur.lastrowid
                            
                            wastage = prep - sold
                            conn.execute("INSERT INTO sales (date, menu_id, meal, sp, sold, wastage, cogs, payment) VALUES (?,?,?,?,?,?,?,'Cash')",
                                         (d, menu_id, item_name, sp, sold, wastage, exp))
                            conn.execute("INSERT INTO batch_prep (date, menu_id, qty_prepared) VALUES (?,?,?)",
                                         (d, menu_id, prep))
                            conn.execute("INSERT INTO expenditure (date, amount, category, notes) VALUES (?,?,'Raw Materials',?)",
                                         (d, exp, f"Auto-expenditure for {item_name} batch"))
                except Exception as e:
                    self._popup("❌ Import Failed", f"Database error during import:\n{e}")
                    return

            self._toast(f"✅ Datewise Import for {d} completed successfully!")
            self._go("dashboard")

        cf = card(wrap); cf.pack(fill="x", pady=10)
        btn(cf, "📥  Download Template", dl_template, fg=STRIPE, text_color=DARK, hv=BORDER, h=46).pack(fill="x", pady=(0, 10))
        btn(cf, "📂  Choose CSV File & Import", do_import, fg=GREEN, hv=DGREEN, h=46).pack(fill="x")

    # ==============================================================================
    # BACKUP & RESTORE
    # ==============================================================================
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
        if not self._confirm("Confirm Restore",
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
