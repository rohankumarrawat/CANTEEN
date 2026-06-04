import re

path = "/Users/rohan/Desktop/canteen/app.py"
with open(path) as f:
    code = f.read()

# ════════════════════════════════════════════════════════════════════════
# 1. Add matplotlib import at the top
# ════════════════════════════════════════════════════════════════════════
code = code.replace(
    "import tkinter as tk\nfrom tkinter import filedialog, messagebox",
    """import tkinter as tk
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
    CHART_OK = False"""
)

# ════════════════════════════════════════════════════════════════════════
# 2. DASHBOARD — complete rewrite with charts
# ════════════════════════════════════════════════════════════════════════
DASH_OLD = '''    # ══════════════════════════════════════════════════════════════════════════
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
            "\\n".join(f"• {i['item']}  →  need {i['min_lvl']-i['stock']:.1f} {i['unit']}" for i in low)
            or "All stock sufficient!"),
            fg=DRED, hv=RED, h=38).pack(fill="x", side="bottom")'''

DASH_NEW = '''    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD — with charts
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_dashboard(self):
        self._hdr("Dashboard",
                  f"\\U0001F1EE\\U0001F1F3  {datetime.now().strftime('%A, %d %B %Y')}  \\u00b7  56 APO Field Canteen")
        today = datetime.now().strftime("%Y-%m-%d")
        with get_db() as conn:
            sales = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
            inv   = conn.execute("SELECT * FROM inventory").fetchall()
            waste = conn.execute("SELECT * FROM waste_tracker WHERE date=?", (today,)).fetchall()
            exp   = conn.execute("SELECT SUM(amount) FROM expenditure WHERE date=?", (today,)).fetchone()[0] or 0
            # 7-day trend data
            week_data = conn.execute(
                "SELECT date, SUM(sp*sold) as rev, SUM(sold) as meals "
                "FROM sales WHERE date >= ? GROUP BY date ORDER BY date",
                ((datetime.now()-timedelta(days=6)).strftime("%Y-%m-%d"),)).fetchall()
            cat_data = conn.execute(
                "SELECT cat, SUM(stock) as total FROM inventory GROUP BY cat").fetchall()

        rev    = sum(r["sp"]*r["sold"] for r in sales)
        cogs   = sum(r["cogs"] for r in sales)
        profit = rev - cogs - exp
        meals  = sum(r["sold"] for r in sales)
        low    = [i for i in inv if i["stock"] < i["min_lvl"]]
        wcost  = sum(w["cost_lost"] or 0 for w in waste)

        # ── KPI cards ─────────────────────────────────────────────────────────
        KPI = [
            ("\\U0001f4b0", "Revenue",     f"\\u20b9{rev:,.0f}",    SAFFRON, BG_SAF, T_SAF),
            ("\\U0001f35b", "Meals Served", str(meals),         GREEN,   BG_GRN, T_GRN),
            ("\\U0001f4c8", "Net Profit",  f"\\u20b9{profit:,.0f}",  BLUE,    BG_BLU, T_BLU),
            ("\\U0001f4b8", "Expenditure", f"\\u20b9{exp:,.0f}",     PURPLE,  BG_PUR, T_PUR),
            ("\\u267b\\ufe0f", "Waste Cost",  f"\\u20b9{wcost:,.0f}",   ORANGE,  BG_SAF, T_SAF),
            ("\\u26a0\\ufe0f", "Low Stock",   str(len(low)),       RED,     BG_RED, T_RED),
        ]
        kr = ctk.CTkFrame(self._area, fg_color="transparent")
        kr.pack(fill="x", padx=PAD, pady=(14,0))
        for i, (icon, title, val, color, bg, border) in enumerate(KPI):
            c = ctk.CTkFrame(kr, fg_color=WHITE, corner_radius=12, border_width=1, border_color=border)
            c.grid(row=0, column=i, padx=(0 if i==0 else 6), sticky="nsew")
            kr.grid_columnconfigure(i, weight=1)
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
            chart_row = ctk.CTkFrame(self._area, fg_color="transparent")
            chart_row.pack(fill="x", padx=PAD, pady=(12,0))
            chart_row.grid_columnconfigure(0, weight=3)
            chart_row.grid_columnconfigure(1, weight=2)

            # Revenue trend line chart
            cf1 = ctk.CTkFrame(chart_row, fg_color=WHITE, corner_radius=12,
                               border_width=1, border_color=BORDER)
            cf1.grid(row=0, column=0, padx=(0,8), sticky="nsew")
            lbl(cf1, "  \\U0001f4c8  7-Day Revenue Trend", size=11, weight="bold",
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
                ax1.set_ylabel("\\u20b9", fontsize=8)
                for i2, v in enumerate(revs):
                    ax1.annotate(f"\\u20b9{v:,.0f}", (i2, v), textcoords="offset points",
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
            lbl(cf2, "  \\U0001f4e6  Stock by Category", size=11, weight="bold",
                color=ARMY_BG).pack(anchor="w", padx=12, pady=(10,0))

            fig2 = Figure(figsize=(2.8, 2.2), dpi=100, facecolor="#FFFFFF")
            ax2 = fig2.add_subplot(111)
            if cat_data:
                cats = [r["cat"] for r in cat_data]
                vals = [r["total"] for r in cat_data]
                colors_pie = ["#FF9933","#138808","#3B82F6","#8B5CF6","#F59E0B","#EF4444"]
                wedges, texts, autotexts = ax2.pie(
                    vals, labels=cats, autopct="%1.0f%%", startangle=90,
                    colors=colors_pie[:len(cats)], pctdistance=0.75,
                    textprops={"fontsize": 7})
                for at in autotexts: at.set_fontsize(6); at.set_color("white")
                centre = plt.Circle((0,0), 0.55, fc="white"); ax2.add_artist(centre)
            else:
                ax2.text(0.5, 0.5, "No stock", ha="center", va="center",
                         fontsize=10, color="#94A3B8", transform=ax2.transAxes)
            fig2.tight_layout(pad=0.5)
            canvas2 = FigureCanvasTkAgg(fig2, master=cf2)
            canvas2.draw(); canvas2.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=(0,8))

        # ── Bottom: Sales table + Alerts ──────────────────────────────────────
        bot = ctk.CTkFrame(self._area, fg_color="transparent")
        bot.pack(fill="both", expand=True, padx=PAD, pady=(10,PAD))
        bot.grid_columnconfigure(0, weight=6); bot.grid_columnconfigure(1, weight=4)
        bot.grid_rowconfigure(0, weight=1)

        sc = card(bot); sc.grid(row=0, column=0, padx=(0,8), sticky="nsew")
        band(sc, "\\U0001f4ca  Today\\u2019s Sales")
        COLS = [("Meal",3),("Sold",1),("Revenue",2),("Payment",1)]
        thead(sc, COLS)
        sf = ctk.CTkScrollableFrame(sc, fg_color="transparent")
        sf.pack(fill="both", expand=True)
        for ix, r in enumerate(sales):
            pi = {"Cash":"\\U0001f4b5","UPI":"\\U0001f4f1","Card":"\\U0001f4b3"}.get(r["payment"],"\\U0001f4b0")
            trow(sf,[r["meal"],str(r["sold"]),
                     f"\\u20b9{r['sp']*r['sold']:,.0f}",f"{pi} {r['payment']}"],
                 [3,1,2,1],
                 colors=[DARK,MID,GREEN,MID],bolds=[True,False,True,False],
                 bg=WHITE if ix%2==0 else STRIPE)
        totf = ctk.CTkFrame(sc, fg_color=BG_SAF, corner_radius=0, height=34)
        totf.pack(fill="x"); totf.pack_propagate(False)
        lbl(totf, f"  TOTAL: {meals} meals  \\u2022  \\u20b9{rev:,.0f}", size=11,
            weight="bold", color=SAFFRON).pack(side="left", padx=10)

        ac = card(bot); ac.grid(row=0, column=1, sticky="nsew")
        band(ac, f"\\u26a0\\ufe0f  Low Stock  ({len(low)})", bg=DRED, tc=WHITE)
        sf2 = ctk.CTkScrollableFrame(ac, fg_color="transparent")
        sf2.pack(fill="both", expand=True, padx=6, pady=6)
        if not low:
            lbl(sf2, "\\u2705  All items OK", size=12, color=GREEN).pack(pady=20)
        else:
            for item in low:
                rf2 = ctk.CTkFrame(sf2, fg_color=BG_RED, corner_radius=8)
                rf2.pack(fill="x", pady=2)
                lbl(rf2, f"  {item['item']}  \\u2022  {item['stock']:.1f}/{item['min_lvl']:.1f} {item['unit']}",
                    size=10, weight="bold", color="#991B1B").pack(padx=8, pady=6, anchor="w")'''

code = code.replace(DASH_OLD, DASH_NEW)

# ════════════════════════════════════════════════════════════════════════
# 3. WASTE — rewrite with stock selector + modern UI
# ════════════════════════════════════════════════════════════════════════
WASTE_OLD = '''    # ══════════════════════════════════════════════════════════════════════════
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
        self._toast(f"✅ Waste: {item} ({qty}) — {self._wr.get()}")
        self._live_refresh("waste")'''

WASTE_NEW = '''    # ══════════════════════════════════════════════════════════════════════════
    # WASTE — modern with stock selector
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_waste(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")
        self._hdr("\\u267b\\ufe0f  Waste Management", f"\\U0001f4c5  {today_disp}")

        with get_db() as conn:
            inv_items = sorted([f"{r['item']} ({r['unit']})" for r in
                                conn.execute("SELECT item,unit FROM inventory ORDER BY item")])
            wr = conn.execute("SELECT * FROM waste_tracker WHERE date=? ORDER BY id DESC",
                              (today,)).fetchall()

        total_wc = sum(w["cost_lost"] or 0 for w in wr)

        # Summary strip
        sf = ctk.CTkFrame(self._area, fg_color=ARMY_BG, corner_radius=0, height=52)
        sf.pack(fill="x", padx=PAD, pady=(10,0)); sf.pack_propagate(False)
        for icon, label, val, clr in [
            ("\\U0001f5d1", "Entries Today", str(len(wr)), SAFFRON),
            ("\\U0001f4b8", "Total Loss", f"\\u20b9{total_wc:,.0f}", "#F87171"),
        ]:
            cf = ctk.CTkFrame(sf, fg_color="transparent"); cf.pack(side="left", padx=24, expand=True)
            lbl(cf, f"{icon}  {label}", size=10, color="#94A3B8").pack(anchor="w")
            lbl(cf, val, size=18, weight="bold", color=clr).pack(anchor="w")

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(10,PAD))

        # ── Record form ───────────────────────────────────────────────────────
        wc = card(wrap); wc.pack(fill="x", pady=(0,14))
        band(wc, "\\U0001f4dd  Record Wastage")

        body = ctk.CTkFrame(wc, fg_color="transparent"); body.pack(fill="x", padx=18, pady=14)

        # Row 1: Item selection with search
        lbl(body, "Select Stock Item (Searchable)", size=11, weight="bold",
            color=ARMY_BG).pack(anchor="w", pady=(0,4))
        se = ctk.CTkEntry(body, placeholder_text="\\U0001f50d  Type to search stock...", height=32)
        se.pack(fill="x", pady=(0,6))
        self._wi_om = ctk.CTkOptionMenu(body, values=inv_items or ["(none)"],
                                        font=ctk.CTkFont(size=12))
        self._wi_om.set(inv_items[0] if inv_items else "")
        self._wi_om.pack(fill="x", pady=(0,10))

        def filter_waste_items(*args):
            q = se.get().lower()
            fil = [x for x in inv_items if q in x.lower()]
            self._wi_om.configure(values=fil or ["(none)"])
            if fil: self._wi_om.set(fil[0])
        se.bind("<KeyRelease>", filter_waste_items)

        # Row 2: Qty + Cost side by side
        r2 = ctk.CTkFrame(body, fg_color="transparent"); r2.pack(fill="x", pady=(0,10))
        r2.grid_columnconfigure(0, weight=1); r2.grid_columnconfigure(1, weight=1)

        lbl(r2, "Qty Wasted", size=11, weight="bold", color=ARMY_BG).grid(
            row=0, column=0, sticky="w", pady=(0,4))
        self._wq = entry(r2, ph="e.g., 2.5", h=36)
        self._wq.grid(row=1, column=0, sticky="ew", padx=(0,8))

        lbl(r2, "Estimated Cost (\\u20b9)", size=11, weight="bold", color=ARMY_BG).grid(
            row=0, column=1, sticky="w", padx=(8,0), pady=(0,4))
        self._wc = entry(r2, ph="e.g., 150", h=36)
        self._wc.grid(row=1, column=1, sticky="ew", padx=(8,0))

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

        btn(wc, "\\u2705  Record Waste", self._save_waste,
            fg=ORANGE, hv="#EA580C", h=46).pack(padx=18, pady=(0,14), fill="x")

        # ── Today\'s log ──────────────────────────────────────────────────────
        lc = card(wrap); lc.pack(fill="both", expand=True)
        band(lc, f"\\U0001f4cb  Today\\u2019s Waste Log  \\u2022  {today_disp}")
        if not wr:
            lbl(lc, "\\u2705  No wastage recorded today.", size=12, color=GREEN).pack(pady=22)
        else:
            COLS = [("Item",3),("Qty",1),("Reason",2),("Cost",1),("By",2)]
            thead(lc, COLS, bg=STRIPE, tc=MID)
            for ix, w in enumerate(wr):
                trow(lc,[w["item"],f"{w[\'qty_wasted\']:.1f}",w["reason"],
                         f"\\u20b9{w[\'cost_lost\']:.0f}",w["recorded_by"] or "\\u2014"],
                     [3,1,2,1,2], bg=WHITE if ix%2==0 else STRIPE)
            tot = ctk.CTkFrame(lc, fg_color=BG_RED, height=34, corner_radius=0)
            tot.pack(fill="x"); tot.pack_propagate(False)
            lbl(tot, f"  TOTAL WASTE: \\u20b9{total_wc:,.0f}", size=11,
                weight="bold", color=RED).pack(side="left", padx=10)

    def _save_waste(self):
        try:
            qty  = float(self._wq.get())
            cost = float(self._wc.get())
        except ValueError:
            self._popup("\\u26a0\\ufe0f Invalid","Numeric values for qty and cost."); return
        raw = self._wi_om.get()
        item = raw.split(" (")[0].strip() if " (" in raw else raw.strip()
        if not item or qty <= 0:
            self._popup("\\u26a0\\ufe0f Invalid","Select item and enter qty > 0."); return
        with get_db() as conn:
            conn.execute(
                "INSERT INTO waste_tracker (date,item,qty_wasted,reason,cost_lost,recorded_by) "
                "VALUES (?,?,?,?,?,?)",
                (datetime.now().strftime("%Y-%m-%d"), item, qty,
                 self._wr.get(), cost, self._user["name"]))
            if getattr(self, "_waste_deduct", None) and self._waste_deduct.get():
                conn.execute("UPDATE inventory SET stock=stock-? WHERE item=?", (qty, item))
        self._toast(f"\\u2705 Waste: {item} ({qty}) \\u2014 {self._wr.get()}")
        self._live_refresh("waste")'''

code = code.replace(WASTE_OLD, WASTE_NEW)

# ════════════════════════════════════════════════════════════════════════
# 4. SALES — add search filter
# ════════════════════════════════════════════════════════════════════════
SALES_SEARCH_OLD = '''        # ── Meal cards grid ───────────────────────────────────────────────────
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(12, PAD))

        self._sq = {}
        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        for ix, meal in enumerate(meals):'''

SALES_SEARCH_NEW = '''        # ── Search + Meal cards grid ──────────────────────────────────────────
        search_bar = ctk.CTkFrame(self._area, fg_color="transparent")
        search_bar.pack(fill="x", padx=PAD, pady=(8,0))
        self._sale_search = ctk.CTkEntry(search_bar, placeholder_text="\\U0001f50d  Search meals...",
                                         height=34, corner_radius=10)
        self._sale_search.pack(fill="x")
        self._sale_search.bind("<KeyRelease>", lambda e: self._filter_sale_cards())

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(8, PAD))

        self._sq = {}
        self._sale_cards = []  # (name, card_widget)
        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        self._sale_grid = grid
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        for ix, meal in enumerate(meals):'''

code = code.replace(SALES_SEARCH_OLD, SALES_SEARCH_NEW)

# Track cards in sales
code = code.replace(
    '''            self._sq[mid2] = (name2, sp2, e_qty, pm)

        # ── Save All bar''',
    '''            self._sq[mid2] = (name2, sp2, e_qty, pm)
            self._sale_cards.append((name2.lower(), mc))

        # ── Save All bar'''
)

# ════════════════════════════════════════════════════════════════════════
# 5. BATCH — add search filter
# ════════════════════════════════════════════════════════════════════════
BATCH_SEARCH_OLD = '''        # ── Cards grid ────────────────────────────────────────────────────────
        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(10,PAD))

        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        self._be = {}
        for ix, meal in enumerate(meals):'''

BATCH_SEARCH_NEW = '''        # ── Search + Cards grid ────────────────────────────────────────────────
        search_bar = ctk.CTkFrame(self._area, fg_color="transparent")
        search_bar.pack(fill="x", padx=PAD, pady=(8,0))
        self._batch_search = ctk.CTkEntry(search_bar, placeholder_text="\\U0001f50d  Search meals...",
                                          height=34, corner_radius=10)
        self._batch_search.pack(fill="x")
        self._batch_search.bind("<KeyRelease>", lambda e: self._filter_batch_cards())

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(8,PAD))

        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        self._batch_grid = grid
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        self._be = {}
        self._batch_cards = []
        for ix, meal in enumerate(meals):'''

code = code.replace(BATCH_SEARCH_OLD, BATCH_SEARCH_NEW)

# Track cards in batch
code = code.replace(
    '''            self._be[mid2] = e

        # ── Save bar''',
    '''            self._be[mid2] = e
            self._batch_cards.append((nm.lower(), mc))

        # ── Save bar'''
)

# ════════════════════════════════════════════════════════════════════════
# 6. INVENTORY — add search bar in inventory page header
# ════════════════════════════════════════════════════════════════════════
INV_SEARCH_OLD = '''        # Action bar
        ab = ctk.CTkFrame(self._area, fg_color="transparent")
        ab.pack(fill="x", padx=PAD, pady=(10,0))'''

INV_SEARCH_NEW = '''        # Search bar
        sb = ctk.CTkFrame(self._area, fg_color="transparent")
        sb.pack(fill="x", padx=PAD, pady=(8,0))
        self._inv_search = ctk.CTkEntry(sb, placeholder_text="\\U0001f50d  Search inventory items...",
                                        height=34, corner_radius=10)
        self._inv_search.pack(fill="x")
        self._inv_search.bind("<KeyRelease>", lambda e: self._inv_filter_search())

        # Action bar
        ab = ctk.CTkFrame(self._area, fg_color="transparent")
        ab.pack(fill="x", padx=PAD, pady=(8,0))'''

code = code.replace(INV_SEARCH_OLD, INV_SEARCH_NEW)

# ════════════════════════════════════════════════════════════════════════
# 7. Add filter helper methods before the MASTER DATA section
# ════════════════════════════════════════════════════════════════════════
MASTER_MARKER = '''    # ══════════════════════════════════════════════════════════════════════════
    # MASTER DATA'''

FILTER_METHODS = '''    def _filter_sale_cards(self):
        q = self._sale_search.get().lower() if hasattr(self, "_sale_search") else ""
        for name, w in self._sale_cards:
            if q in name: w.grid()
            else: w.grid_remove()

    def _filter_batch_cards(self):
        q = self._batch_search.get().lower() if hasattr(self, "_batch_search") else ""
        for name, w in self._batch_cards:
            if q in name: w.grid()
            else: w.grid_remove()

    def _inv_filter_search(self):
        q = self._inv_search.get().lower() if hasattr(self, "_inv_search") else ""
        for w in self._inv_sf.winfo_children(): w.destroy()
        with get_db() as conn:
            if self._inv_filter == "All":
                data = conn.execute("SELECT * FROM inventory ORDER BY cat,item").fetchall()
            else:
                data = conn.execute("SELECT * FROM inventory WHERE cat=? ORDER BY item",
                                    (self._inv_filter,)).fetchall()
        if q:
            data = [d for d in data if q in d["item"].lower()]
        ci = {"Dry":"\\U0001f33e","Fresh":"\\U0001f966","Dairy":"\\U0001f95b","Bakery":"\\U0001f950","Prepared":"\\U0001f372"}
        for ix, item in enumerate(data):
            low = item["stock"] < item["min_lvl"]
            bg2 = BG_RED if low else (WHITE if ix%2==0 else STRIPE)
            trow(self._inv_sf,
                 [f"  {item['item']}", f"{ci.get(item['cat'],'\\u2022')} {item['cat']}",
                  item["unit"], f"{item['opening']:.1f}", f"{item['received']:.1f}",
                  f"{item['stock']:.1f}", f"{item['min_lvl']:.1f}",
                  "\\u26a0 LOW" if low else "\\u2713 OK"],
                 self._inv_wts,
                 colors=[DARK,MID,MID,MID,MID,
                         RED if low else GREEN, MID,
                         RED if low else GREEN],
                 bolds=[True,False,False,False,False,True,False,True],
                 bg=bg2, row_h=40)

    # ══════════════════════════════════════════════════════════════════════════
    # MASTER DATA'''

code = code.replace(MASTER_MARKER, FILTER_METHODS, 1)

with open(path, "w") as f:
    f.write(code)
print("✅ Patch applied successfully")
