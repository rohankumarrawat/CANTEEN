#!/usr/bin/env python3
"""
Patch script: replaces the sales section (lines 778-1009) of app.py
with a corrected version that properly handles stock deduction.
"""
import shutil, os

TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
shutil.copy(TARGET, TARGET + ".bak_sales_patch")

with open(TARGET, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lines are 1-indexed in view; 0-indexed in list
START = 778 - 1   # line 778 (inclusive)
END   = 1009 - 1  # line 1009 (inclusive)

NEW_BLOCK = '''    # ══════════════════════════════════════════════════════════════════════════
    # SALES ENTRY — with proper stock deduction & audit trail
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_sales(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")

        hf = self._hdr("💰  Sales Entry", f"📅  {today_disp}")
        btn(hf, "📋  Export PDF", lambda: self._export_pdf_report(today, today),
            fg=ARMY_BG, hv=ARMY_HVR, h=32).pack(side="right", padx=PAD)

        with get_db() as conn:
            meals = conn.execute("SELECT id,name,sp FROM menu WHERE active=1 ORDER BY name").fetchall()
            today_sales = conn.execute("SELECT * FROM sales WHERE date=?", (today,)).fetchall()
        today_map = {r["menu_id"]: r for r in today_sales}
        tot_rev  = sum(r["sp"]*r["sold"] for r in today_sales)
        tot_sold = sum(r["sold"] for r in today_sales)

        # ── Summary strip ──────────────────────────────────────────────────────
        sf = ctk.CTkFrame(self._area, fg_color=ARMY_BG, corner_radius=0, height=56)
        sf.pack(fill="x", padx=PAD, pady=(10,0)); sf.pack_propagate(False)
        for icon, label, val, clr in [
            ("🍽", "Items Sold", f"{tot_sold}", SAFFRON),
            ("💰", "Revenue",    f"₹{tot_rev:,.0f}", "#4ADE80"),
            ("📊", "Entries",    f"{len(today_sales)}/{len(meals)}", WHITE),
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
        self._sale_search.bind("<KeyRelease>", lambda e: self._filter_sale_cards())

        wrap = ctk.CTkScrollableFrame(self._area, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=PAD, pady=(8, PAD))

        self._sq = {}
        self._sale_cards = []
        grid = ctk.CTkFrame(wrap, fg_color="transparent"); grid.pack(fill="x")
        self._sale_grid = grid
        for i in range(3): grid.grid_columnconfigure(i, weight=1)

        for ix, meal in enumerate(meals):
            mid2, name2, sp2 = meal["id"], meal["name"], meal["sp"]
            already  = today_map.get(mid2)
            is_saved = already is not None
            is_thali = any(x in name2 for x in ["Thali","Biryani","Rice"])

            mc = ctk.CTkFrame(grid, fg_color=WHITE, corner_radius=14,
                              border_width=2,
                              border_color=T_GRN if is_saved else BORDER)
            mc.grid(row=ix//3, column=ix%3, padx=6, pady=6, sticky="nsew")

            # Top badge
            top = ctk.CTkFrame(mc, fg_color=ARMY_BG if is_thali else TEAL,
                               corner_radius=0, height=36)
            top.pack(fill="x"); top.pack_propagate(False)
            lbl(top, f"  {'🍛' if is_thali else '🍽️'}  {name2}",
                size=11, weight="bold", color=WHITE).pack(side="left", padx=8)
            lbl(top, f"₹{sp2:.0f}", size=12, weight="bold",
                color=SAFFRON).pack(side="right", padx=12)

            # Saved indicator
            if is_saved:
                si = ctk.CTkFrame(mc, fg_color=BG_GRN, corner_radius=0, height=22)
                si.pack(fill="x"); si.pack_propagate(False)
                lbl(si, f"  ✅  Saved: {already['sold']} sold  •  ₹{already['sold']*sp2:,.0f}",
                    size=9, weight="bold", color=GREEN).pack(side="left", padx=6)

            body = ctk.CTkFrame(mc, fg_color="transparent")
            body.pack(fill="x", padx=12, pady=10)

            lbl(body, "Quantity Sold", size=10, color=MID).pack(anchor="w")
            e_qty = ctk.CTkEntry(body, height=40, corner_radius=10,
                                 placeholder_text="0",
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 border_color=BORDER, justify="center")
            if is_saved: e_qty.insert(0, str(already["sold"]))
            e_qty.pack(fill="x", pady=(4,8))

            rev_val = already["sold"]*sp2 if is_saved else 0
            rev_lbl = lbl(body, f"Revenue: ₹{rev_val:,.0f}", size=11,
                          weight="bold", color=GREEN)
            rev_lbl.pack(anchor="w")

            def _upd(event=None, eq=e_qty, rl=rev_lbl, sp=sp2):
                try:    rl.configure(text=f"Revenue: ₹{int(eq.get() or 0)*sp:,.0f}")
                except: rl.configure(text="Revenue: ₹0")
            e_qty.bind("<KeyRelease>", _upd)

            pm = ctk.CTkOptionMenu(body, values=["Cash","UPI","Card"],
                                   width=120, height=30,
                                   font=ctk.CTkFont(size=11))
            pm.set(already["payment"] if is_saved else "Cash")
            pm.pack(fill="x", pady=(8,4))

            def _save(m_id=mid2, m_name=name2, m_sp=sp2, eq=e_qty, epm=pm):
                self._save_one_sale(m_id, m_name, m_sp, eq, epm)

            ctk.CTkButton(mc, text="✅  Save" if not is_saved else "🔄  Update",
                          height=36, corner_radius=10,
                          fg_color=GREEN if not is_saved else BLUE,
                          hover_color=DGREEN if not is_saved else DBLUE,
                          font=ctk.CTkFont(size=12, weight="bold"),
                          command=_save).pack(fill="x", padx=12, pady=(0,12))

            self._sq[mid2] = (name2, sp2, e_qty, pm)
            self._sale_cards.append((name2.lower(), mc))

        # ── Save All bar ───────────────────────────────────────────────────────
        bar = ctk.CTkFrame(wrap, fg_color="transparent")
        bar.pack(fill="x", pady=(14,4))
        btn(bar, "💾  Save All Items at Once", self._save_all_sales,
            fg=ARMY_BG, hv=ARMY_HVR, h=48).pack(fill="x")

        # ── Today's sales log with ingredient deduction detail ─────────────────
        if today_sales:
            sc = card(wrap); sc.pack(fill="x", pady=(14,0))
            band(sc, f"📊  Today's Sales Log  •  {today_disp}")
            COLS2 = [("Meal",4),("Sold",1),("COGS",1),("Revenue",1),("Payment",1),("Ingredients Deducted",3)]
            thead(sc, COLS2, bg=STRIPE, tc=MID)
            tot_cogs = 0
            with get_db() as conn:
                for ix, r in enumerate(today_sales):
                    rev2 = r["sp"]*r["sold"]; tot_cogs += r["cogs"]
                    # Fetch stock deduction from ledger for this sale
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
                        detail_str = ", ".join(parts)
                    else:
                        detail_str = "— no recipe"
                    bg2 = WHITE if ix%2==0 else STRIPE
                    rf = ctk.CTkFrame(sc, fg_color=bg2, corner_radius=0, height=40)
                    rf.pack(fill="x"); rf.pack_propagate(False)
                    for j, (v, wt, c, b) in enumerate(zip(
                        [r["meal"], str(r["sold"]),
                         f"₹{r['cogs']:,.0f}", f"₹{rev2:,.0f}",
                         r["payment"], detail_str],
                        [4,1,1,1,1,3],
                        [DARK,MID,ORANGE,GREEN,MID,TEAL],
                        [True,False,False,True,False,False]
                    )):
                        lbl(rf, str(v), size=10,
                            weight="bold" if b else "normal", color=c).grid(
                            row=0, column=j, padx=12, pady=8, sticky="w")
                        rf.grid_columnconfigure(j, weight=wt)

            totf = ctk.CTkFrame(sc, fg_color=BG_GRN, corner_radius=0, height=38)
            totf.pack(fill="x"); totf.pack_propagate(False)
            for j, (v, wt, c) in enumerate(zip(
                ["TOTAL","",f"₹{tot_cogs:,.0f}",f"₹{tot_rev:,.0f}","",""],
                [4,1,1,1,1,3],
                [GREEN,MID,ORANGE,GREEN,MID,MID]
            )):
                lbl(totf, v, size=11, weight="bold", color=c).grid(
                    row=0, column=j, padx=12, sticky="w")
                totf.grid_columnconfigure(j, weight=wt)

    # ── Core stock deduction engine (single source of truth) ──────────────────
    def _apply_stock_deduction(self, conn, menu_id, qty_sold, sale_id, today):
        """
        Deducts stock for all recipe ingredients of menu_id based on qty_sold.
        Writes an audit entry into stock_ledger for each ingredient.
        Returns (cpu_per_unit, deductions_list, warnings_list).

        cpu_per_unit — weighted cost per portion (for COGS calculation)
        deductions   — list of dicts describing what was deducted
        warnings     — list of strings where stock was insufficient (clamped to 0)
        """
        recipes = conn.execute(
            "SELECT r.inv_id, r.qty_per_unit, i.item, i.unit, i.cp, i.stock "
            "FROM recipes r JOIN inventory i ON i.id=r.inv_id "
            "WHERE r.menu_id=?", (menu_id,)).fetchall()

        cpu        = 0.0
        deductions = []
        warnings   = []

        for rc in recipes:
            inv_id        = rc["inv_id"]
            qty_per_unit  = rc["qty_per_unit"]
            item_name     = rc["item"]
            unit          = rc["unit"]
            cp            = rc["cp"]
            current_stock = rc["stock"]

            cpu += qty_per_unit * cp

            if qty_sold == 0:
                continue

            total_deduct = qty_per_unit * qty_sold   # always positive here

            if current_stock < total_deduct:
                warnings.append(
                    f"⚠ {item_name}: need {total_deduct:.3f} {unit}, "
                    f"only {current_stock:.3f} {unit} available"
                )

            new_stock = max(0.0, current_stock - total_deduct)
            conn.execute(
                "UPDATE inventory SET stock=?, updated=? WHERE id=?",
                (new_stock, today, inv_id))

            # Audit trail: qty_change stored as negative (deduction)
            conn.execute(
                "INSERT INTO stock_ledger "
                "(date, inv_id, transaction_type, qty_change, notes) "
                "VALUES (?, ?, 'Sale', ?, ?)",
                (today, inv_id, -total_deduct,
                 f"Sale:{sale_id} | {item_name} "
                 f"({qty_per_unit:.4f} {unit}/portion × {qty_sold} portions)"))

            deductions.append({
                "item":          item_name,
                "unit":          unit,
                "qty_per_unit":  qty_per_unit,
                "total_deducted": total_deduct,
                "stock_before":  current_stock,
                "stock_after":   new_stock,
            })

        return cpu, deductions, warnings

    def _save_one_sale(self, menu_id, meal, sp, eq, epm):
        try:
            sold = int(eq.get() or 0)
        except:
            self._popup("⚠️ Invalid Entry", "Please enter a whole number for quantity sold.")
            return
        if sold <= 0:
            self._popup("⚠️ No Quantity", "Quantity sold must be greater than 0.")
            return

        today   = datetime.now().strftime("%Y-%m-%d")
        payment = epm.get()

        with get_db() as conn:
            # ── Step 1: Check if a sale already exists for this item today ───
            existing = conn.execute(
                "SELECT id, sold FROM sales WHERE date=? AND menu_id=?",
                (today, menu_id)).fetchone()
            old_sold = existing["sold"] if existing else 0

            # ── Step 2: If updating, fully RESTORE old stock first ───────────
            # This avoids the bug where multiple updates keep accumulating
            # deductions. We restore old qty, then deduct the full new qty.
            if existing:
                # Remove old ledger entries linked to the previous sale
                conn.execute(
                    "DELETE FROM stock_ledger WHERE notes LIKE ? AND date=?",
                    (f"Sale:{existing['id']}%", today))
                # Restore stock for each ingredient by the full old sold qty
                old_recs = conn.execute(
                    "SELECT r.inv_id, r.qty_per_unit "
                    "FROM recipes r WHERE r.menu_id=?", (menu_id,)).fetchall()
                for rc in old_recs:
                    restore = rc["qty_per_unit"] * old_sold
                    conn.execute(
                        "UPDATE inventory SET stock = stock + ?, updated=? WHERE id=?",
                        (restore, today, rc["inv_id"]))
                # Delete the old sales record
                conn.execute("DELETE FROM sales WHERE id=?", (existing["id"],))

            # ── Step 3: Insert new sale record (cogs updated in step 5) ──────
            cur = conn.execute(
                "INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) "
                "VALUES (?,?,?,?,?,0,0.0,?)",
                (today, menu_id, meal, sp, sold, payment))
            new_sale_id = cur.lastrowid

            # ── Step 4: Deduct stock for the FULL new qty & get per-unit cost ─
            cpu, deductions, warnings = self._apply_stock_deduction(
                conn, menu_id, sold, new_sale_id, today)

            # ── Step 5: Update COGS now that cpu is known ─────────────────────
            conn.execute(
                "UPDATE sales SET cogs=? WHERE id=?",
                (sold * cpu, new_sale_id))

        # ── Show low-stock warnings ───────────────────────────────────────────
        if warnings:
            self._popup("⚠️ Stock Warning",
                        "Sale saved, but some ingredients were low:\n\n" +
                        "\n".join(warnings))

        # ── Toast with deduction summary ──────────────────────────────────────
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

                # Restore old qty if updating ─────────────────────────────────
                existing = conn.execute(
                    "SELECT id, sold FROM sales WHERE date=? AND menu_id=?",
                    (today, mid2)).fetchone()
                old_sold = existing["sold"] if existing else 0

                if existing:
                    conn.execute(
                        "DELETE FROM stock_ledger WHERE notes LIKE ? AND date=?",
                        (f"Sale:{existing['id']}%", today))
                    old_recs = conn.execute(
                        "SELECT r.inv_id, r.qty_per_unit "
                        "FROM recipes r WHERE r.menu_id=?", (mid2,)).fetchall()
                    for rc in old_recs:
                        restore = rc["qty_per_unit"] * old_sold
                        conn.execute(
                            "UPDATE inventory SET stock = stock + ?, updated=? WHERE id=?",
                            (restore, today, rc["inv_id"]))
                    conn.execute("DELETE FROM sales WHERE id=?", (existing["id"],))

                # Insert fresh sale record
                cur = conn.execute(
                    "INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) "
                    "VALUES (?,?,?,?,?,0,0.0,?)",
                    (today, mid2, name2, sp2, sold, payment))
                new_sale_id = cur.lastrowid

                # Deduct stock for full new qty
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
            self._popup("⚠️ Stock Warnings",
                        f"{saved} sale(s) saved.\n\nLow-stock warnings:\n" +
                        "\n".join(all_warnings[:8]) +
                        (f"\n... and {len(all_warnings)-8} more" if len(all_warnings) > 8 else ""))

        self._toast(
            f"✅ {saved} item(s) saved — "
            f"{total_deducts} ingredient deductions recorded in ledger",
            duration_ms=3500)
        self._live_refresh("sales")

'''

new_lines = NEW_BLOCK.splitlines(keepends=True)

patched = lines[:START] + new_lines + lines[END+1:]

with open(TARGET, "w", encoding="utf-8") as f:
    f.writelines(patched)

print(f"✅ Patched successfully.")
print(f"   Replaced lines {START+1}–{END+1} ({END-START+1} lines)")
print(f"   New block: {len(new_lines)} lines")
print(f"   Total file: {len(patched)} lines")
