"""
Canteen Inventory & Sales Management System
Demo Application — Python + CustomTkinter
"""

import customtkinter as ctk
from datetime import datetime
import random

# ── Theme ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Mock Data ──────────────────────────────────────────────────────────────────
INVENTORY = [
    {"item": "Rice",          "cat": "Dry",        "unit": "Kg",  "stock": 45.0, "min": 20.0, "opening": 55.0, "received": 10.0},
    {"item": "Dal (Toor)",    "cat": "Dry",        "unit": "Kg",  "stock":  3.5, "min":  5.0, "opening":  8.0, "received":  0.0},
    {"item": "Wheat Flour",   "cat": "Dry",        "unit": "Kg",  "stock": 30.0, "min": 15.0, "opening": 35.0, "received":  5.0},
    {"item": "Sugar",         "cat": "Dry",        "unit": "Kg",  "stock":  1.2, "min":  3.0, "opening":  4.0, "received":  0.0},
    {"item": "Cooking Oil",   "cat": "Dry",        "unit": "Ltr", "stock":  8.0, "min":  5.0, "opening": 10.0, "received":  2.0},
    {"item": "Tomatoes",      "cat": "Fresh",      "unit": "Kg",  "stock":  4.0, "min":  2.0, "opening":  6.0, "received":  2.0},
    {"item": "Onions",        "cat": "Fresh",      "unit": "Kg",  "stock":  6.5, "min":  3.0, "opening":  8.0, "received":  2.0},
    {"item": "Milk",          "cat": "Dairy",      "unit": "Ltr", "stock":  0.8, "min":  5.0, "opening":  5.0, "received":  0.0},
    {"item": "Paneer",        "cat": "Dairy",      "unit": "Kg",  "stock":  2.0, "min":  1.0, "opening":  3.0, "received":  0.0},
    {"item": "Lunch Boxes",   "cat": "Packaging",  "unit": "Pcs", "stock": 50,   "min": 100,  "opening": 100,  "received":  0  },
]

SALES = [
    {"meal": "Standard Lunch", "sp": 80,  "sold": 45, "cogs": 2700},
    {"meal": "VIP Thali",      "sp": 150, "sold": 12, "cogs": 1200},
    {"meal": "Tea",            "sp": 10,  "sold": 80, "cogs":  400},
    {"meal": "Snacks",         "sp": 30,  "sold": 25, "cogs":  500},
]

LOW_ITEMS = [i for i in INVENTORY if i["stock"] < i["min"]]

# ── Helpers ────────────────────────────────────────────────────────────────────
BLUE   = "#2563EB"
DBLUE  = "#1D4ED8"
GREEN  = "#059669"
DGREEN = "#047857"
RED    = "#DC2626"
PURPLE = "#7C3AED"
AMBER  = "#D97706"
DARK   = "#1E293B"
MID    = "#64748B"
LIGHT  = "#F1F5F9"
WHITE  = "#FFFFFF"
BORDER = "#E2E8F0"
STRIPE = "#F8FAFC"


def card(parent, **kwargs):
    defaults = dict(fg_color=WHITE, corner_radius=14, border_width=1, border_color=BORDER)
    defaults.update(kwargs)
    return ctk.CTkFrame(parent, **defaults)


def label(parent, text, size=13, weight="normal", color=DARK, **kwargs):
    return ctk.CTkLabel(parent, text=text,
                        font=ctk.CTkFont(size=size, weight=weight),
                        text_color=color, **kwargs)


def divider(parent):
    ctk.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", padx=30, pady=16)


# ══════════════════════════════════════════════════════════════════════════════
class CanteenApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Canteen Inventory & Sales System")
        self.geometry("1280x780")
        self.minsize(1100, 680)
        self.configure(fg_color=LIGHT)
        self._show_login()

    # ── Login ──────────────────────────────────────────────────────────────────
    def _show_login(self):
        for w in self.winfo_children():
            w.destroy()
        self.configure(fg_color="#EFF6FF")

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        box = card(outer, corner_radius=22)
        box.pack()

        label(box, "🍽️", size=54).pack(pady=(42, 4))
        label(box, "Canteen System", size=24, weight="bold").pack()
        label(box, "Inventory & Sales Management", size=13, color=MID).pack(pady=(2, 30))

        ctk.CTkFrame(box, height=1, fg_color=BORDER, width=340).pack(padx=40)

        label(box, "Username", size=12, weight="bold", color="#374151", anchor="w").pack(padx=44, fill="x", pady=(22, 3))
        self._uname = ctk.CTkEntry(box, width=340, height=46, corner_radius=10,
                                   placeholder_text="Enter username",
                                   font=ctk.CTkFont(size=14), border_color="#CBD5E1")
        self._uname.pack(padx=40, pady=(0, 14))
        self._uname.insert(0, "manager")

        label(box, "Password", size=12, weight="bold", color="#374151", anchor="w").pack(padx=44, fill="x", pady=(0, 3))
        self._pwd = ctk.CTkEntry(box, width=340, height=46, corner_radius=10,
                                 placeholder_text="Enter password", show="●",
                                 font=ctk.CTkFont(size=14), border_color="#CBD5E1")
        self._pwd.pack(padx=40, pady=(0, 22))
        self._pwd.insert(0, "1234")
        self._pwd.bind("<Return>", lambda e: self._do_login())

        ctk.CTkButton(box, text="Login  →", width=340, height=50, corner_radius=12,
                      font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=BLUE, hover_color=DBLUE,
                      command=self._do_login).pack(padx=40, pady=(0, 14))

        self._login_err = label(box, "", size=12, color=RED)
        self._login_err.pack()

        label(box, "Demo v1.0  •  Indian Army Canteen", size=11, color="#94A3B8").pack(pady=(10, 34))

    def _do_login(self):
        if self._uname.get().strip() == "manager" and self._pwd.get() == "1234":
            self._show_main()
        else:
            self._login_err.configure(text="⚠  Invalid credentials. Try manager / 1234")

    # ── Main Shell (Sidebar + Content) ─────────────────────────────────────────
    def _show_main(self):
        for w in self.winfo_children():
            w.destroy()
        self.configure(fg_color=LIGHT)

        # Sidebar
        self._sidebar = ctk.CTkFrame(self, fg_color="#0F172A", width=240, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        label(self._sidebar, "🍽️  Canteen", size=19, weight="bold", color=WHITE).pack(pady=(28, 2), padx=22, anchor="w")
        label(self._sidebar, "Management System", size=11, color="#64748B").pack(pady=(0, 22), padx=22, anchor="w")
        ctk.CTkFrame(self._sidebar, height=1, fg_color="#1E293B").pack(fill="x", padx=20, pady=(0, 18))

        nav_items = [
            ("📊   Dashboard",    "dashboard"),
            ("💰   Sales Entry",  "sales"),
            ("📦   Inventory",    "inventory"),
            ("📋   Daily Report", "report"),
        ]
        self._nav_btns = {}
        for lbl, page in nav_items:
            b = ctk.CTkButton(self._sidebar, text=lbl, anchor="w", height=46,
                              font=ctk.CTkFont(size=14), fg_color="transparent",
                              hover_color="#1E293B", text_color="#94A3B8",
                              corner_radius=10,
                              command=lambda p=page: self._navigate(p))
            b.pack(padx=14, pady=3, fill="x")
            self._nav_btns[page] = b

        # Bottom of sidebar
        ctk.CTkFrame(self._sidebar, height=1, fg_color="#1E293B").pack(fill="x", padx=20, side="bottom", pady=(10, 0))
        ctk.CTkButton(self._sidebar, text="⬅   Logout", height=42, anchor="w",
                      fg_color="transparent", hover_color="#1E293B", text_color="#64748B",
                      font=ctk.CTkFont(size=13), corner_radius=10,
                      command=self._show_login).pack(padx=14, pady=(0, 14), fill="x", side="bottom")

        usr = ctk.CTkFrame(self._sidebar, fg_color="#1E293B", corner_radius=12)
        usr.pack(padx=14, side="bottom", fill="x", pady=(0, 8))
        label(usr, "👤  Canteen Manager", size=12, weight="bold", color=WHITE).pack(padx=14, pady=(12, 2), anchor="w")
        label(usr, "manager@canteen.in", size=10, color="#64748B").pack(padx=14, pady=(0, 12), anchor="w")

        # Content area
        self._content = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        self._content.pack(side="right", fill="both", expand=True)

        self._navigate("dashboard")

    def _navigate(self, page):
        for p, b in self._nav_btns.items():
            if p == page:
                b.configure(fg_color=BLUE, text_color=WHITE)
            else:
                b.configure(fg_color="transparent", text_color="#94A3B8")
        for w in self._content.winfo_children():
            w.destroy()
        {"dashboard": self._page_dashboard,
         "sales":     self._page_sales,
         "inventory": self._page_inventory,
         "report":    self._page_report}[page]()

    # ── Page helpers ────────────────────────────────────────────────────────────
    def _page_header(self, title, subtitle=""):
        hf = ctk.CTkFrame(self._content, fg_color="transparent")
        hf.pack(fill="x", padx=30, pady=(28, 0))
        label(hf, title, size=26, weight="bold").pack(side="left")
        if subtitle:
            label(hf, subtitle, size=13, color=MID).pack(side="right", pady=6)
        return hf

    # ══════════════════════════════════════════════════════════════════════════
    # Dashboard
    # ══════════════════════════════════════════════════════════════════════════
    def _page_dashboard(self):
        date_str = datetime.now().strftime("%d %B %Y  —  %A")
        self._page_header("Dashboard", f"📅  {date_str}")

        total_rev  = sum(s["sp"] * s["sold"] for s in SALES)
        total_cost = sum(s["cogs"] for s in SALES)
        net_profit = total_rev - total_cost
        meals_sold = sum(s["sold"] for s in SALES)
        low_count  = len(LOW_ITEMS)

        # ── Stat cards ──
        cards_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=20)

        stat_data = [
            ("Total Revenue",    f"₹ {total_rev:,}",   BLUE,   "💰"),
            ("Total COGS",       f"₹ {total_cost:,}",  PURPLE, "🧾"),
            ("Net Profit",       f"₹ {net_profit:,}",  GREEN,  "📈"),
            ("Meals Sold",       str(meals_sold),       AMBER,  "🍛"),
            ("Low Stock Alerts", str(low_count),        RED,    "⚠️"),
        ]

        for i, (lbl, val, color, icon) in enumerate(stat_data):
            c = card(cards_frame)
            c.grid(row=0, column=i, padx=5, pady=0, sticky="nsew")
            cards_frame.grid_columnconfigure(i, weight=1)
            label(c, icon, size=28).pack(pady=(20, 6), padx=18, anchor="w")
            label(c, val, size=22, weight="bold", color=color).pack(padx=18, anchor="w")
            label(c, lbl, size=11, color=MID).pack(padx=18, pady=(2, 20), anchor="w")

        # ── Bottom: Sales table + Alerts ──
        bottom = ctk.CTkFrame(self._content, fg_color="transparent")
        bottom.pack(fill="both", expand=True, padx=30, pady=(0, 24))
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)

        # Sales table card
        sc = card(bottom)
        sc.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        label(sc, "Today's Sales Breakdown", size=15, weight="bold").pack(padx=22, pady=(20, 12), anchor="w")

        th = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=8)
        th.pack(padx=22, fill="x")
        for j, col in enumerate(["Meal", "Qty Sold", "Rate", "Revenue"]):
            label(th, col, size=11, weight="bold", color=MID).grid(row=0, column=j, padx=14, pady=9, sticky="w")
            th.grid_columnconfigure(j, weight=1)

        for idx, row in enumerate(SALES):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg, corner_radius=0)
            rf.pack(padx=22, fill="x")
            for j, val in enumerate([row["meal"], str(row["sold"]),
                                      f"₹{row['sp']}", f"₹{row['sp']*row['sold']:,}"]):
                label(rf, val, size=13, color=DARK).grid(row=0, column=j, padx=14, pady=10, sticky="w")
                rf.grid_columnconfigure(j, weight=1)

        # Total row
        totrow = ctk.CTkFrame(sc, fg_color="#EFF6FF", corner_radius=8)
        totrow.pack(padx=22, pady=(6, 22), fill="x")
        for j, (v, c_) in enumerate(zip(["TOTAL", str(meals_sold), "", f"₹{total_rev:,}"],
                                        ["#1E40AF"]*4)):
            label(totrow, v, size=13, weight="bold", color=c_).grid(row=0, column=j, padx=14, pady=10, sticky="w")
            totrow.grid_columnconfigure(j, weight=1)

        # Low stock alerts card
        ac = card(bottom)
        ac.grid(row=0, column=1, sticky="nsew")
        label(ac, "⚠️  Low Stock Alerts", size=15, weight="bold", color=RED).pack(padx=22, pady=(20, 12), anchor="w")

        if not LOW_ITEMS:
            label(ac, "✅  All items are sufficiently stocked.", size=13, color=GREEN).pack(padx=22, pady=20)
        else:
            for item in LOW_ITEMS:
                row_f = ctk.CTkFrame(ac, fg_color="#FEF2F2", corner_radius=10)
                row_f.pack(padx=22, pady=4, fill="x")
                label(row_f, item["item"], size=13, weight="bold", color="#991B1B").pack(padx=14, pady=(10, 2), anchor="w")
                sf = ctk.CTkFrame(row_f, fg_color="transparent")
                sf.pack(padx=14, pady=(0, 10), fill="x")
                label(sf, f"Have: {item['stock']} {item['unit']}", size=11, color=RED).pack(side="left")
                label(sf, f"Min: {item['min']} {item['unit']}", size=11, color=MID).pack(side="right")

        ctk.CTkButton(ac, text="🛒  Generate Shopping List", height=44, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=RED, hover_color="#B91C1C",
                      command=lambda: self._popup("Shopping List Generated!",
                          "\n".join(f"• {i['item']}  ({i['min']-i['stock']:.1f} {i['unit']} needed)"
                                    for i in LOW_ITEMS))
                      ).pack(padx=22, pady=(10, 22), fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # Sales Entry
    # ══════════════════════════════════════════════════════════════════════════
    def _page_sales(self):
        self._page_header("💰  Daily Sales Entry",
                          datetime.now().strftime("Date: %d %B %Y"))

        wrap = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=30, pady=(18, 24))

        sc = card(wrap)
        sc.pack(fill="x", pady=(0, 16))

        label(sc, "Meal Preparation & Sales Count", size=15, weight="bold").pack(padx=24, pady=(20, 4), anchor="w")
        label(sc, "Enter quantities prepared, sold, and wastage for each item.", size=12, color=MID).pack(padx=24, pady=(0, 16), anchor="w")

        # Column headers
        hrow = ctk.CTkFrame(sc, fg_color=STRIPE, corner_radius=8)
        hrow.pack(padx=24, fill="x")
        for j, col in enumerate(["Meal Item", "Qty Prepared", "Qty Sold", "Wastage"]):
            label(hrow, col, size=12, weight="bold", color=MID).grid(row=0, column=j, padx=16, pady=10, sticky="w")
            hrow.grid_columnconfigure(j, weight=1 if j > 0 else 2)

        meals = ["Standard Lunch", "VIP Thali", "Tea", "Snacks", "Breakfast", "Evening Snacks"]
        self._entries = {}
        for idx, meal in enumerate(meals):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(sc, fg_color=bg, corner_radius=0)
            rf.pack(padx=24, fill="x")

            label(rf, f"🍽  {meal}", size=13, weight="bold").grid(row=0, column=0, padx=16, pady=12, sticky="w")

            entries = []
            for j, (ph, bc) in enumerate(
                    [("0", BORDER), ("0", BORDER), ("0", "#FCA5A5")], start=1):
                e = ctk.CTkEntry(rf, width=110, height=40, corner_radius=8,
                                 placeholder_text=ph, font=ctk.CTkFont(size=13),
                                 border_color=bc)
                e.grid(row=0, column=j, padx=16, pady=10, sticky="w")
                rf.grid_columnconfigure(j, weight=1)
                entries.append(e)
            rf.grid_columnconfigure(0, weight=2)
            self._entries[meal] = entries

        # Payment section
        pc = card(wrap)
        pc.pack(fill="x", pady=(0, 16))
        label(pc, "Payment Collection Breakdown", size=15, weight="bold").pack(padx=24, pady=(20, 14), anchor="w")

        pay_frame = ctk.CTkFrame(pc, fg_color="transparent")
        pay_frame.pack(padx=24, fill="x", pady=(0, 20))

        for i, (mode, color, icon) in enumerate([
                ("Cash",  GREEN,  "💵"),
                ("UPI",   PURPLE, "📱"),
                ("Card",  BLUE,   "💳")]):
            b = card(pay_frame, corner_radius=12)
            b.grid(row=0, column=i, padx=6, sticky="nsew")
            pay_frame.grid_columnconfigure(i, weight=1)
            label(b, f"{icon}  {mode}", size=13, weight="bold", color=color).pack(padx=16, pady=(16, 6), anchor="w")
            label(b, "Amount (₹)", size=11, color=MID).pack(padx=16, anchor="w")
            ctk.CTkEntry(b, height=44, placeholder_text="0.00", corner_radius=8,
                         font=ctk.CTkFont(size=16), border_color=BORDER).pack(padx=16, pady=(4, 16), fill="x")

        # Buttons
        bf = ctk.CTkFrame(wrap, fg_color="transparent")
        bf.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(bf, text="✓  Save & Deduct Stock Automatically",
                      height=54, corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=lambda: self._popup(
                          "✅  Entry Saved!",
                          "Sales recorded successfully.\nInventory has been automatically deducted based on recipes.")
                      ).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ctk.CTkButton(bf, text="🖨  Preview Report",
                      height=54, corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=BLUE, hover_color=DBLUE,
                      command=lambda: self._navigate("report")
                      ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    # ══════════════════════════════════════════════════════════════════════════
    # Inventory
    # ══════════════════════════════════════════════════════════════════════════
    def _page_inventory(self):
        hf = self._page_header("📦  Inventory Ledger",
                               f"📅  {datetime.now().strftime('%d %B %Y')}")

        # Category filter buttons
        ff = ctk.CTkFrame(hf, fg_color="transparent")
        ff.pack(side="right")
        self._cat_filter = ctk.StringVar(value="All")
        for cat in ["All", "Dry", "Fresh", "Dairy", "Packaging"]:
            ctk.CTkButton(ff, text=cat, width=84, height=34, corner_radius=8,
                          font=ctk.CTkFont(size=12),
                          fg_color=BLUE if cat == "All" else "#E2E8F0",
                          text_color=WHITE if cat == "All" else "#374151",
                          hover_color=DBLUE if cat == "All" else "#CBD5E1",
                          command=lambda c=cat: self._filter_inventory(c)
                          ).pack(side="left", padx=3)

        # Add stock button row
        bf = ctk.CTkFrame(self._content, fg_color="transparent")
        bf.pack(fill="x", padx=30, pady=(14, 0))
        ctk.CTkButton(bf, text="+ Add Received Stock", height=42, width=200,
                      corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=GREEN, hover_color=DGREEN,
                      command=lambda: self._popup("Add Stock", "Stock receipt entry form\n(Full functionality in production build.)")
                      ).pack(side="left")
        ctk.CTkButton(bf, text="🔧  Manual Adjustment", height=42, width=180,
                      corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color="#7C3AED", hover_color="#6D28D9",
                      command=lambda: self._popup("Manual Adjustment", "Admin-only adjustment feature.\n(Requires Admin role in production.)")
                      ).pack(side="left", padx=10)

        # Table card
        tc = card(self._content, corner_radius=14)
        tc.pack(fill="both", expand=True, padx=30, pady=14)

        cols  = ["Item Name",   "Cat",    "Unit", "Opening", "Received", "Used",   "Closing Stock", "Status"]
        wts   = [3,              1,        1,       1,          1,          1,         2,               2]

        thead = ctk.CTkFrame(tc, fg_color=STRIPE, corner_radius=8)
        thead.pack(fill="x", padx=0)
        for j, (col, w) in enumerate(zip(cols, wts)):
            label(thead, col, size=12, weight="bold", color=MID).grid(
                row=0, column=j, padx=14, pady=11, sticky="w")
            thead.grid_columnconfigure(j, weight=w)

        self._inv_scroll = ctk.CTkScrollableFrame(tc, fg_color="transparent")
        self._inv_scroll.pack(fill="both", expand=True)
        self._render_inv_rows(INVENTORY)

    def _filter_inventory(self, cat):
        for w in self._inv_scroll.winfo_children():
            w.destroy()
        data = INVENTORY if cat == "All" else [i for i in INVENTORY if i["cat"] == cat]
        self._render_inv_rows(data)

    def _render_inv_rows(self, data):
        wts = [3, 1, 1, 1, 1, 1, 2, 2]
        for idx, item in enumerate(data):
            is_low = item["stock"] < item["min"]
            used   = item["opening"] + item["received"] - item["stock"]
            bg     = "#FFF5F5" if is_low else (WHITE if idx % 2 == 0 else STRIPE)

            rf = ctk.CTkFrame(self._inv_scroll, fg_color=bg, corner_radius=0)
            rf.pack(fill="x")

            vals   = [item["item"], item["cat"], item["unit"],
                      f"{item['opening']:.1f}", f"{item['received']:.1f}",
                      f"{used:.1f}", f"{item['stock']:.1f}",
                      "⚠️  LOW" if is_low else "✓ OK"]
            colors = [DARK, MID, MID, DARK, GREEN, PURPLE,
                      RED if is_low else GREEN,
                      RED if is_low else GREEN]
            bolds  = [True, False, False, False, False, False, True, True]

            for j, (v, c, bo) in enumerate(zip(vals, colors, bolds)):
                label(rf, v, size=13, weight="bold" if bo else "normal", color=c).grid(
                    row=0, column=j, padx=14, pady=11, sticky="w")
                rf.grid_columnconfigure(j, weight=wts[j])

    # ══════════════════════════════════════════════════════════════════════════
    # Daily Report
    # ══════════════════════════════════════════════════════════════════════════
    def _page_report(self):
        hf = self._page_header("📋  Daily Report",
                               datetime.now().strftime("%d %B %Y"))

        ctk.CTkButton(hf, text="🖨  Export PDF", height=40, width=150,
                      corner_radius=8, font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=BLUE, hover_color=DBLUE,
                      command=lambda: self._popup("PDF Export",
                          "Report exported to:\nCanteen_Report_" +
                          datetime.now().strftime("%d%m%Y") + ".pdf\n\n(Full PDF in production build.)")
                      ).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self._content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=(16, 24))

        # Report header
        rc = card(scroll)
        rc.pack(fill="x", pady=(0, 14))

        label(rc, "CANTEEN DAILY OPERATIONS REPORT", size=18, weight="bold").pack(pady=(28, 4))
        label(rc, f"Date: {datetime.now().strftime('%d %B %Y')}   |   Unit: Indian Army Canteen",
              size=13, color=MID).pack(pady=(0, 22))

        ctk.CTkFrame(rc, height=2, fg_color=BLUE).pack(fill="x", padx=30, pady=(0, 22))

        # 1. Sales Summary
        label(rc, "1.  Sales Summary", size=14, weight="bold", color="#1E40AF").pack(padx=30, anchor="w", pady=(0, 10))

        th = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=8)
        th.pack(padx=30, fill="x")
        report_cols = ["Meal Item", "Prepared", "Sold", "Wastage", "Rate", "Revenue"]
        for j, col in enumerate(report_cols):
            label(th, col, size=12, weight="bold", color=MID).grid(row=0, column=j, padx=14, pady=10, sticky="w")
            th.grid_columnconfigure(j, weight=1)

        report_rows = [
            ("Standard Lunch", 50, 45, 5, "₹80",  "₹3,600"),
            ("VIP Thali",       15, 12, 3, "₹150", "₹1,800"),
            ("Tea",             90, 80, 10,"₹10",  "₹800"),
            ("Snacks",          30, 25, 5, "₹30",  "₹750"),
        ]
        for idx, row in enumerate(report_rows):
            bg = WHITE if idx % 2 == 0 else STRIPE
            rf = ctk.CTkFrame(rc, fg_color=bg, corner_radius=0)
            rf.pack(padx=30, fill="x")
            for j, val in enumerate(row):
                label(rf, str(val), size=13).grid(row=0, column=j, padx=14, pady=10, sticky="w")
                rf.grid_columnconfigure(j, weight=1)

        tot = ctk.CTkFrame(rc, fg_color="#DBEAFE", corner_radius=8)
        tot.pack(padx=30, pady=(4, 0), fill="x")
        for j, val in enumerate(["TOTAL", "185", "162", "23", "", "₹6,950"]):
            label(tot, val, size=13, weight="bold", color="#1E40AF").grid(row=0, column=j, padx=14, pady=10, sticky="w")
            tot.grid_columnconfigure(j, weight=1)

        ctk.CTkFrame(rc, height=1, fg_color=BORDER).pack(fill="x", padx=30, pady=20)

        # 2. Financial Summary
        label(rc, "2.  Financial Summary", size=14, weight="bold", color="#1E40AF").pack(padx=30, anchor="w", pady=(0, 10))

        for lbl_text, val, color in [
                ("Total Revenue (Sales)", "₹ 6,950", GREEN),
                ("Total Cost of Goods Sold (COGS)", "₹ 4,800", RED),
                ("Net Daily Profit", "₹ 2,150", BLUE)]:
            fr = ctk.CTkFrame(rc, fg_color=STRIPE, corner_radius=10)
            fr.pack(padx=30, fill="x", pady=4)
            label(fr, lbl_text, size=13).pack(side="left", padx=18, pady=14)
            label(fr, val, size=16, weight="bold", color=color).pack(side="right", padx=18)

        ctk.CTkFrame(rc, height=1, fg_color=BORDER).pack(fill="x", padx=30, pady=20)

        # 3. Payment Breakdown
        label(rc, "3.  Payment Breakdown", size=14, weight="bold", color="#1E40AF").pack(padx=30, anchor="w", pady=(0, 10))

        pf = ctk.CTkFrame(rc, fg_color="transparent")
        pf.pack(padx=30, fill="x", pady=(0, 0))
        for i, (mode, amt, color) in enumerate([
                ("💵  Cash", "₹ 4,200", GREEN),
                ("📱  UPI",  "₹ 2,000", PURPLE),
                ("💳  Card", "₹ 750",   BLUE)]):
            b = card(pf, corner_radius=12)
            b.grid(row=0, column=i, padx=6, sticky="nsew")
            pf.grid_columnconfigure(i, weight=1)
            label(b, mode, size=13, weight="bold", color=color).pack(padx=16, pady=(16, 4), anchor="w")
            label(b, amt, size=20, weight="bold", color=color).pack(padx=16, pady=(0, 16), anchor="w")

        ctk.CTkFrame(rc, height=1, fg_color=BORDER).pack(fill="x", padx=30, pady=20)

        # 4. Signature Block
        label(rc, "4.  Signatures & Sign-off", size=14, weight="bold", color="#1E40AF").pack(padx=30, anchor="w", pady=(0, 14))

        sf = ctk.CTkFrame(rc, fg_color="transparent")
        sf.pack(padx=30, fill="x", pady=(0, 32))
        for i, (role, name) in enumerate([
                ("Prepared By", "Canteen Manager"),
                ("Checked By",  "Supervisor / JCO"),
                ("Approved By", "Officer-in-Charge")]):
            b = card(sf, corner_radius=12)
            b.grid(row=0, column=i, padx=8, sticky="nsew")
            sf.grid_columnconfigure(i, weight=1)
            label(b, role, size=11, weight="bold", color=MID).pack(padx=20, pady=(18, 40), anchor="w")
            ctk.CTkFrame(b, height=1, fg_color=DARK).pack(fill="x", padx=20)
            label(b, name, size=12, weight="bold").pack(padx=20, pady=(8, 18), anchor="w")

    # ── Popup helper ────────────────────────────────────────────────────────────
    def _popup(self, title, message):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("460x260")
        win.resizable(False, False)
        win.grab_set()
        win.lift()
        win.configure(fg_color=WHITE)

        icon = "✅" if "Saved" in title or "Generated" in title or "Export" in title else "ℹ️"
        label(win, icon, size=40).pack(pady=(30, 8))
        label(win, message, size=13, color=DARK, justify="center", wraplength=380).pack(pady=(0, 22))
        ctk.CTkButton(win, text="OK", width=130, height=42, corner_radius=10,
                      fg_color=BLUE, hover_color=DBLUE,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=win.destroy).pack()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CanteenApp()
    app.mainloop()
