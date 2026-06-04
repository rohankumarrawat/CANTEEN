    # ══════════════════════════════════════════════════════════════════════════
    # SALES ENTRY
    # ══════════════════════════════════════════════════════════════════════════
    def _pg_sales(self):
        today      = datetime.now().strftime("%Y-%m-%d")
        today_disp = datetime.now().strftime("%d %B %Y")

        hf = self._hdr("🍽️  Sales Entry", f"📅  {today_disp}")
        btn(hf, "📄  Export PDF", lambda: self._export_pdf_report(today, today),
            fg=ARMY_BG, hv=ARMY_HVR, h=32).pack(side="right", padx=PAD)

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
        recipes = conn.execute(
            "SELECT r.inv_id, r.qty_per_unit "
            "FROM recipes r WHERE r.menu_id=?", (menu_id,)).fetchall()
        cpu = 0.0
        deductions = []
        warnings   = []
        for rc in recipes:
            inv = conn.execute(
                "SELECT id, item, unit, cp, stock FROM inventory WHERE id=?",
                (rc["inv_id"],)).fetchone()
            if not inv:
                continue
            inv_id        = inv["id"]
            item_name     = inv["item"]
            unit          = inv["unit"]
            qty_per_unit  = rc["qty_per_unit"]
            total_deduct  = qty_per_unit * qty_sold
            cpu          += qty_per_unit * (inv["cp"] or 0)
            current_stock = inv["stock"] or 0.0
            if current_stock < total_deduct:
                warnings.append(
                    f"⚠ Low stock: {item_name} needs {total_deduct:.2f}{unit}, "
                    f"only {current_stock:.2f}{unit} left")
            new_stock = max(0.0, current_stock - total_deduct)
            conn.execute(
                "UPDATE inventory SET stock=?, updated=? WHERE id=?",
                (new_stock, today, inv_id))
            conn.execute(
                "INSERT INTO stock_ledger "
                "(date, inv_id, transaction_type, qty_change, notes) "
                "VALUES (?, ?, 'Sale', ?, ?)",
                (today, inv_id, -total_deduct,
                 f"Sale:{sale_id} | {item_name} "
                 f"({qty_per_unit:.4f} {unit}/portion x {qty_sold} portions)"))
            deductions.append({
                "item":           item_name,
                "unit":           unit,
                "qty_per_unit":   qty_per_unit,
                "total_deducted": total_deduct,
                "stock_before":   current_stock,
                "stock_after":    new_stock,
            })
        return cpu, deductions, warnings

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

