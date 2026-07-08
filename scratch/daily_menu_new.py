    # ── Daily Schedule tab ────────────────────────────────────────────────────
    # ── Daily Menu tab ─────────────────────────────────────────────────────────
    def _master_daily_menu(self, wrap):
        """
        Date-wise daily menu creation & viewing.
        - LEFT sidebar: scrollable list of all dates that have saved batch_prep data
        - RIGHT: date picker + view mode (if date has data) or create mode (if not)
        - 3 main slots: Lunch, Paratha, Mini Meal — pre-filled from weekly schedule
        - Extra items: add Chach, Lassi, or any extra dish dynamically
        - Per slot: Menu Item dropdown, Plates, Samples, Staff
        - New Item option opens the full item-creation form inline
        - Save: auto-deducts stock, creates batch_prep, samples, expenditure
        """
        import datetime as _dt

        today_str = datetime.now().strftime("%Y-%m-%d")
        MEAL_SLOTS = ["Lunch", "Paratha", "Mini Meal"]

        # ── Shared state ──────────────────────────────────────────────────────
        slot_widgets = {}   # meal_type → widget dict
        extra_rows   = []   # list of widget dicts for extra dishes
        menu_state   = {
            "menu_by_name": {}, "menu_names": [], "recipe_detail": {},
            "sched_map": {}, "existing_batch": [], "saved_dates": []
        }

        # ── Root layout: left sidebar + right scrollable content ───────────
        root_f = ctk.CTkFrame(wrap, fg_color="transparent")
        root_f.pack(fill="both", expand=True)
        root_f.grid_columnconfigure(0, weight=0)
        root_f.grid_columnconfigure(1, weight=1)
        root_f.grid_rowconfigure(0, weight=1)

        # LEFT: saved-dates sidebar
        sidebar = ctk.CTkFrame(root_f, fg_color=WHITE, corner_radius=12,
                               border_width=2, border_color=BORDER, width=190)
        sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        sidebar.grid_propagate(False)
        band(sidebar, "📅  Saved Dates", bg=ARMY_BG, tc=GOLD_LT, h=34)
        dates_scroll = ctk.CTkScrollableFrame(sidebar, fg_color="transparent",
                                              width=180, height=500)
        dates_scroll.pack(fill="both", expand=True, padx=2, pady=4)

        # RIGHT: content area
        right_f = ctk.CTkFrame(root_f, fg_color="transparent")
        right_f.grid(row=0, column=1, sticky="nsew")

        # Date picker card
        date_card = card(right_f); date_card.pack(fill="x", pady=(0, 8))
        band(date_card, "📋  Daily Menu  —  View or Create", bg=ARMY_BG, tc=GOLD_LT, h=38)
        dr = ctk.CTkFrame(date_card, fg_color="transparent")
        dr.pack(fill="x", padx=14, pady=(10, 4))
        lbl(dr, "Date:", size=11, weight="bold", color=ARMY_BG).pack(side="left", padx=(0,8))
        date_var   = ctk.StringVar(value=today_str)
        date_entry = ctk.CTkEntry(dr, textvariable=date_var, height=40, width=160,
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  border_color=BORDER, justify="center")
        date_entry.pack(side="left", padx=(0, 8))
        day_lbl = lbl(dr, "", size=13, weight="bold", color=ARMY_BG)
        day_lbl.pack(side="left", padx=6)
        status_lbl = ctk.CTkLabel(dr, text="", font=ctk.CTkFont(size=11), text_color=GREEN)
        status_lbl.pack(side="left", padx=6)

        load_row = ctk.CTkFrame(date_card, fg_color="transparent")
        load_row.pack(fill="x", padx=14, pady=(4, 12))
        btn(load_row, "🔍  Load", lambda: _build_slots(),
            fg=BLUE, hv=DBLUE, h=38, w=130).pack(side="left")

        # Scrollable slots area
        slots_outer = ctk.CTkScrollableFrame(right_f, fg_color="transparent")
        slots_outer.pack(fill="both", expand=True)

        # ──────────────────────────────────────────────────────────────────
        # DATA LOADING
        # ──────────────────────────────────────────────────────────────────
        def _load_data(date_str):
            with get_db() as conn:
                all_menus = conn.execute(
                    "SELECT id, name, sp, cogs, default_samples, default_staff "
                    "FROM menu WHERE active=1 ORDER BY name"
                ).fetchall()
                sched_rows = conn.execute(
                    "SELECT dm.day, dm.meal_type, m.name "
                    "FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"
                ).fetchall()
                all_recipes = conn.execute(
                    "SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
                    "FROM recipes r JOIN inventory i ON i.id=r.inv_id"
                ).fetchall()
                existing_batch = conn.execute(
                    "SELECT bp.id, bp.menu_id, bp.qty_prepared, "
                    "bp.samples, bp.staff, m.name as menu_name "
                    "FROM batch_prep bp JOIN menu m ON m.id=bp.menu_id "
                    "WHERE bp.date=? ORDER BY bp.id",
                    (date_str,)
                ).fetchall()
                saved_dates = conn.execute(
                    "SELECT DISTINCT date FROM batch_prep ORDER BY date DESC LIMIT 60"
                ).fetchall()

            menu_state["menu_by_name"]  = {m["name"]: m for m in all_menus}
            menu_state["menu_names"]    = [m["name"] for m in all_menus]
            sm = {}
            for s in sched_rows:
                sm.setdefault(s["day"], {})[s["meal_type"]] = s["name"]
            menu_state["sched_map"] = sm
            rd = {}
            for r in all_recipes:
                rd.setdefault(r["menu_id"], []).append({
                    "item": r["item"], "qpu": r["qty_per_unit"],
                    "unit": r["unit"], "cp": r["cp"], "inv_id": r["inv_id"]
                })
            menu_state["recipe_detail"] = rd
            menu_state["existing_batch"] = [dict(r) for r in existing_batch]
            menu_state["saved_dates"]    = [r["date"] for r in saved_dates]

        # ──────────────────────────────────────────────────────────────────
        # SIDEBAR REFRESH
        # ──────────────────────────────────────────────────────────────────
        def _refresh_sidebar():
            for w in dates_scroll.winfo_children():
                w.destroy()
            if not menu_state["saved_dates"]:
                lbl(dates_scroll, "No saved\ndates yet", size=10,
                    color="#9CA3AF").pack(pady=20)
                return
            for d in menu_state["saved_dates"]:
                try:
                    dp    = _dt.date.fromisoformat(d)
                    top   = dp.strftime("%d %b")
                    bot   = dp.strftime("%A")[:3]
                except Exception:
                    top, bot = d, ""
                is_sel = (d == date_var.get())
                fb = ctk.CTkFrame(dates_scroll,
                                  fg_color=ARMY_BG if is_sel else "#F0F4F8",
                                  corner_radius=8)
                fb.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(fb, text=f"{top}\n{bot}",
                             font=ctk.CTkFont(size=10, weight="bold"),
                             text_color=WHITE if is_sel else ARMY_BG,
                             justify="center").pack(pady=5, padx=6)
                fb.bind("<Button-1>", lambda e, ds=d: _jump_to(ds))
                for c in fb.winfo_children():
                    c.bind("<Button-1>", lambda e, ds=d: _jump_to(ds))

        def _jump_to(ds):
            date_var.set(ds)
            _build_slots()

        # ──────────────────────────────────────────────────────────────────
        # INGREDIENT PREVIEW
        # ──────────────────────────────────────────────────────────────────
        def _update_preview(meal_type, sw):
            sel = sw["dropdown"].get()
            if sel.startswith("⭐ "):
                sel = sel[2:]
            m  = menu_state["menu_by_name"].get(sel)
            pf = sw["preview_frame"]
            pl = sw["preview_lbl"]
            if not m:
                pf.pack_forget(); return
            details = menu_state["recipe_detail"].get(m["id"], [])
            try:
                qty = int(sw["qty_entry"].get() or 0)
            except ValueError:
                qty = 0
            if details and qty > 0:
                lines = [f"⚡ {sel}  ×{qty} plates:"]
                for d in details[:8]:
                    lines.append(f"  {d['item']}: {d['qpu']*qty:.2f} {d['unit']}")
                if len(details) > 8:
                    lines.append(f"  +{len(details)-8} more ingredients")
                cost = sum(d["qpu"] * qty * (d["cp"] or 0) for d in details)
                lines.append(f"  💰 Raw cost: ₹{cost:,.0f}")
                pl.configure(text="\n".join(lines))
                pf.pack(fill="x", pady=(6, 0))
            elif details:
                pl.configure(text=f"⚡ {sel} — {len(details)} ingredients linked. Enter plates to preview.")
                pf.pack(fill="x", pady=(6, 0))
            else:
                pl.configure(text="⚠️ No recipes linked — stock won't auto-deduct for this item.")
                pf.pack(fill="x", pady=(6, 0))

        # ──────────────────────────────────────────────────────────────────
        # DROPDOWN CHANGE HANDLER
        # ──────────────────────────────────────────────────────────────────
        def _on_dd_change(val, meal_type, sw):
            if val == "＋ New Item":
                sw["dropdown"].set("— Skip —")
                self._modal_add_menu(
                    target_date=date_entry.get().strip(),
                    callback=lambda new_name, mt=meal_type, s=sw: _after_new_item(mt, new_name, s)
                )
                return
            sel = val[2:] if val.startswith("⭐ ") else val
            m   = menu_state["menu_by_name"].get(sel)
            if m:
                ds  = m.get("default_samples", 0) or 0
                dst = m.get("default_staff",   0) or 0
                sw["samp_entry"].delete(0, "end")
                if ds  > 0: sw["samp_entry"].insert(0, str(ds))
                sw["staff_entry"].delete(0, "end")
                if dst > 0: sw["staff_entry"].insert(0, str(dst))
            _update_preview(meal_type, sw)

        def _after_new_item(meal_type, new_name, sw):
            """After a new item is created: refresh dropdowns, select new item."""
            with get_db() as conn:
                rows = conn.execute(
                    "SELECT id,name,sp,cogs,default_samples,default_staff "
                    "FROM menu WHERE active=1 ORDER BY name"
                ).fetchall()
            menu_state["menu_by_name"] = {m["name"]: m for m in rows}
            menu_state["menu_names"]   = [m["name"] for m in rows]
            try:
                d   = _dt.date.fromisoformat(date_entry.get().strip())
                dow = d.strftime("%A")
            except Exception:
                dow = "Monday"
            # Refresh main slot dropdowns
            for mt, s in slot_widgets.items():
                sn   = menu_state["sched_map"].get(dow, {}).get(mt, "")
                vals = ["— Skip —", "＋ New Item"]
                if sn and sn in menu_state["menu_by_name"]:
                    vals.insert(1, f"⭐ {sn}")
                for mn in menu_state["menu_names"]:
                    if mn != sn: vals.append(mn)
                s["dropdown"].configure(values=vals)
                if mt == meal_type:
                    s["dropdown"].set(new_name)
                    _on_dd_change(new_name, mt, s)
            # Refresh extra row dropdowns
            for er in extra_rows:
                ev = ["— Skip —", "＋ New Item"] + menu_state["menu_names"]
                er["dropdown"].configure(values=ev)

        # ──────────────────────────────────────────────────────────────────
        # BUILD ONE SLOT CARD
        # ──────────────────────────────────────────────────────────────────
        def _make_slot_card(parent, meal_type, dropdown_values,
                            scheduled_name="", header_color=ARMY_BG,
                            header_icon="🍽", is_extra=False):
            slot_card = ctk.CTkFrame(parent, fg_color=WHITE, corner_radius=12,
                                     border_width=2, border_color=BORDER)
            slot_card.pack(fill="x", pady=5)

            sh = ctk.CTkFrame(slot_card, fg_color=header_color, corner_radius=0, height=34)
            sh.pack(fill="x"); sh.pack_propagate(False)
            lbl(sh, f"  {header_icon}  {meal_type}", size=12,
                weight="bold", color=WHITE).pack(side="left", padx=8)
            if scheduled_name:
                lbl(sh, f"Scheduled: {scheduled_name}", size=9,
                    color="#CCCCCC").pack(side="right", padx=12)

            sw_holder = {}  # filled below so remove button can reference it

            if is_extra:
                def _remove():
                    er = sw_holder.get("sw")
                    if er and er in extra_rows:
                        extra_rows.remove(er)
                    slot_card.destroy()
                ctk.CTkButton(sh, text="✕", width=28, height=22,
                              fg_color="#991B1B", hover_color="#7F1D1D",
                              font=ctk.CTkFont(size=10, weight="bold"),
                              text_color=WHITE, command=_remove
                              ).pack(side="right", padx=6)

            body = ctk.CTkFrame(slot_card, fg_color="transparent")
            body.pack(fill="x", padx=12, pady=8)

            r1 = ctk.CTkFrame(body, fg_color="transparent")
            r1.pack(fill="x")
            r1.grid_columnconfigure(0, weight=4)
            r1.grid_columnconfigure(1, weight=2)
            r1.grid_columnconfigure(2, weight=1)
            r1.grid_columnconfigure(3, weight=1)

            # Dropdown
            ddf = ctk.CTkFrame(r1, fg_color="transparent")
            ddf.grid(row=0, column=0, sticky="nsew", padx=(0,8))
            lbl(ddf, "Menu Item", size=10, weight="bold", color=ARMY_BG).pack(anchor="w")
            dd = ctk.CTkOptionMenu(ddf, values=dropdown_values,
                                   font=ctk.CTkFont(size=12), height=40,
                                   fg_color=ARMY_BG, button_color=ARMY_HVR, text_color=WHITE)
            dd.pack(fill="x", pady=(3, 0))

            # Plates
            qf = ctk.CTkFrame(r1, fg_color="transparent")
            qf.grid(row=0, column=1, sticky="nsew", padx=(0,8))
            lbl(qf, "🍽 Plates", size=10, weight="bold", color=ARMY_BG).pack(anchor="w")
            qty_e = ctk.CTkEntry(qf, height=40, corner_radius=10, placeholder_text="0",
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 border_color=BORDER, justify="center")
            qty_e.pack(fill="x", pady=(3, 0))

            # Samples
            sf = ctk.CTkFrame(r1, fg_color="transparent")
            sf.grid(row=0, column=2, sticky="nsew", padx=(0,8))
            lbl(sf, "🎁 Samples", size=10, color=TEAL).pack(anchor="w")
            samp_e = ctk.CTkEntry(sf, height=40, corner_radius=10, placeholder_text="0",
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  border_color=TEAL, justify="center", fg_color="#F0FDFA")
            samp_e.pack(fill="x", pady=(3, 0))

            # Staff
            stf = ctk.CTkFrame(r1, fg_color="transparent")
            stf.grid(row=0, column=3, sticky="nsew")
            lbl(stf, "👥 Staff", size=10, color=ARMY_BG).pack(anchor="w")
            staff_e = ctk.CTkEntry(stf, height=40, corner_radius=10, placeholder_text="0",
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   border_color=ARMY_BG, justify="center", fg_color=BG_GRN)
            staff_e.pack(fill="x", pady=(3, 0))

            # Ingredient preview strip
            pf = ctk.CTkFrame(body, fg_color="#F0FDF4", corner_radius=8,
                              border_width=1, border_color="#BBF7D0")
            pl = lbl(pf, "", size=9, color=ARMY_BG, wraplength=680)
            pl.pack(padx=8, pady=5, anchor="w")

            sw = {"dropdown": dd, "qty_entry": qty_e, "samp_entry": samp_e,
                  "staff_entry": staff_e, "preview_frame": pf, "preview_lbl": pl}
            sw_holder["sw"] = sw  # allow remove button to find it

            # Pre-fill from schedule
            if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
                dd.set(f"⭐ {scheduled_name}")
                m_obj = menu_state["menu_by_name"][scheduled_name]
                ds  = m_obj.get("default_samples", 0) or 0
                dst = m_obj.get("default_staff",   0) or 0
                if ds  > 0: samp_e.insert(0, str(ds))
                if dst > 0: staff_e.insert(0, str(dst))
                self.after(120, lambda mt=meal_type, s=sw: _update_preview(mt, s))
            else:
                dd.set("— Skip —")

            dd.configure(command=lambda val, mt=meal_type, s=sw: _on_dd_change(val, mt, s))
            qty_e.bind("<KeyRelease>", lambda e, mt=meal_type, s=sw: _update_preview(mt, s))
            return sw

        # ──────────────────────────────────────────────────────────────────
        # VIEW MODE — date already has saved entries
        # ──────────────────────────────────────────────────────────────────
        def _build_view_mode(rows, date_str, dow):
            for w in slots_outer.winfo_children(): w.destroy()
            slot_widgets.clear(); extra_rows.clear()

            vc = ctk.CTkFrame(slots_outer, fg_color=WHITE, corner_radius=14,
                              border_width=2, border_color="#BBF7D0")
            vc.pack(fill="x", pady=4)

            hdr = ctk.CTkFrame(vc, fg_color="#14532D", corner_radius=0, height=40)
            hdr.pack(fill="x"); hdr.pack_propagate(False)
            try:
                dstr = _dt.date.fromisoformat(date_str).strftime("%d %b %Y")
            except Exception:
                dstr = date_str
            lbl(hdr, f"✅  {dow},  {dstr}  —  Daily Menu",
                size=12, weight="bold", color=WHITE).pack(side="left", padx=14)
            lbl(hdr, f"{len(rows)} item(s)", size=10,
                color="#A7F3D0").pack(side="right", padx=14)

            # Table header
            th = ctk.CTkFrame(vc, fg_color="#F0FDF4")
            th.pack(fill="x")
            th.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(th, text="#",        width=36, anchor="center",
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=ARMY_BG).grid(row=0, column=0, padx=6, pady=7)
            ctk.CTkLabel(th, text="Menu Item", anchor="w",
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=ARMY_BG).grid(row=0, column=1, sticky="ew", padx=8)
            for ci, hd in enumerate(["Plates", "Samples", "Staff"], 2):
                ctk.CTkLabel(th, text=hd, width=90, anchor="center",
                             font=ctk.CTkFont(size=10, weight="bold"),
                             text_color=ARMY_BG).grid(row=0, column=ci, padx=4)

            # Data rows
            for ix, row in enumerate(rows, 1):
                rf = ctk.CTkFrame(vc, fg_color=WHITE if ix % 2 else "#F8FFF8")
                rf.pack(fill="x")
                rf.grid_columnconfigure(1, weight=1)
                ctk.CTkLabel(rf, text=str(ix), width=36, anchor="center",
                             font=ctk.CTkFont(size=11), text_color="#9CA3AF"
                             ).grid(row=0, column=0, padx=6, pady=9)
                ctk.CTkLabel(rf, text=row["menu_name"], anchor="w",
                             font=ctk.CTkFont(size=12, weight="bold"),
                             text_color=ARMY_BG).grid(row=0, column=1, sticky="ew", padx=8)
                for ci, (val, col) in enumerate([
                    (row["qty_prepared"],    "#1E3A5F"),
                    (row["samples"] or 0,    TEAL),
                    (row["staff"]   or 0,    "#374151"),
                ], 2):
                    ctk.CTkLabel(rf, text=str(val), width=90, anchor="center",
                                 font=ctk.CTkFont(size=13, weight="bold"),
                                 text_color=col).grid(row=0, column=ci, padx=4)

            # Totals
            tot_p  = sum(r["qty_prepared"]  for r in rows)
            tot_s  = sum(r["samples"] or 0 for r in rows)
            tot_st = sum(r["staff"]   or 0 for r in rows)
            tf = ctk.CTkFrame(vc, fg_color="#DCFCE7")
            tf.pack(fill="x")
            tf.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(tf, text="TOTAL", width=36, anchor="center",
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=ARMY_BG).grid(row=0, column=0, padx=6, pady=8)
            ctk.CTkLabel(tf, text="", anchor="w").grid(row=0, column=1, sticky="ew")
            for ci, (val, col) in enumerate(
                [(tot_p, "#1E3A5F"), (tot_s, TEAL), (tot_st, "#374151")], 2):
                ctk.CTkLabel(tf, text=str(val), width=90, anchor="center",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=col).grid(row=0, column=ci, padx=4, pady=8)

            # "Add more" action
            af = ctk.CTkFrame(vc, fg_color="transparent")
            af.pack(fill="x", padx=14, pady=(8, 14))
            btn(af, "＋  Add More Items to this Date",
                lambda: _build_create_mode(date_str, dow),
                fg=ARMY_BG, hv=ARMY_HVR, h=38, w=240).pack(side="left", padx=(0, 10))
            lbl(af, "Adds new entries (existing stock already deducted)",
                size=9, color="#6B7280").pack(side="left")

        # ──────────────────────────────────────────────────────────────────
        # CREATE MODE — fresh form for a date with no entries
        # ──────────────────────────────────────────────────────────────────
        def _build_create_mode(date_str, dow):
            for w in slots_outer.winfo_children(): w.destroy()
            slot_widgets.clear(); extra_rows.clear()

            type_colors = {"Lunch": ARMY_BG, "Paratha": TEAL, "Mini Meal": "#0F766E"}
            type_icons  = {"Lunch": "🍛",    "Paratha": "🥞",  "Mini Meal": "🍱"}

            # ─ Main 3 slots ─────────────────────────────────────────────
            main_hdr_f = ctk.CTkFrame(slots_outer, fg_color="transparent")
            main_hdr_f.pack(fill="x", pady=(0, 2))
            lbl(main_hdr_f, "  📋  Main Meal Slots",
                size=11, weight="bold", color=ARMY_BG).pack(side="left")

            main_cont = ctk.CTkFrame(slots_outer, fg_color="transparent")
            main_cont.pack(fill="x")

            for meal_type in MEAL_SLOTS:
                tc = type_colors.get(meal_type, ARMY_BG)
                ti = type_icons.get(meal_type, "🍽")
                sn = menu_state["sched_map"].get(dow, {}).get(meal_type, "")
                vals = ["— Skip —", "＋ New Item"]
                if sn and sn in menu_state["menu_by_name"]:
                    vals.insert(1, f"⭐ {sn}")
                for mn in menu_state["menu_names"]:
                    if mn != sn: vals.append(mn)
                sw = _make_slot_card(main_cont, meal_type, vals,
                                     scheduled_name=sn, header_color=tc,
                                     header_icon=ti, is_extra=False)
                slot_widgets[meal_type] = sw

            # ─ Separator ────────────────────────────────────────────────
            ctk.CTkFrame(slots_outer, fg_color=BORDER, height=1).pack(fill="x", pady=(12, 4))

            # ─ Extra items ──────────────────────────────────────────────
            eh_f = ctk.CTkFrame(slots_outer, fg_color="transparent")
            eh_f.pack(fill="x", pady=(0, 2))
            lbl(eh_f, "  🍶  Extra Items  (Chach, Lassi, sweets, add-ons…)",
                size=11, weight="bold", color="#0F766E").pack(side="left")

            extra_cont = ctk.CTkFrame(slots_outer, fg_color="transparent")
            extra_cont.pack(fill="x")

            def _add_extra():
                ev = ["— Skip —", "＋ New Item"] + menu_state["menu_names"]
                ix = len(extra_rows) + 1
                er = _make_slot_card(extra_cont, f"Extra Item {ix}", ev,
                                     header_color="#0F766E", header_icon="➕",
                                     is_extra=True)
                extra_rows.append(er)

            add_f = ctk.CTkFrame(slots_outer, fg_color="transparent")
            add_f.pack(fill="x", pady=(6, 0))
            btn(add_f, "➕  Add Extra Dish / Add-on",
                _add_extra, fg="#0F766E", hv="#065F46", h=38, w=210
                ).pack(side="left", padx=4)
            lbl(add_f, "e.g. Chach, Lassi, Sweet, Raita…",
                size=9, color="#6B7280").pack(side="left", padx=8)

            # ─ Save button ──────────────────────────────────────────────
            save_f = ctk.CTkFrame(slots_outer, fg_color="transparent")
            save_f.pack(fill="x", pady=(16, 8))
            btn(save_f, "✅  Save Daily Menu",
                lambda: _save_daily(date_str),
                fg=GREEN, hv=DGREEN, h=44, w=220).pack(side="left", padx=4)

        # ──────────────────────────────────────────────────────────────────
        # MAIN ENTRY: load + decide view vs create
        # ──────────────────────────────────────────────────────────────────
        def _build_slots():
            date_str = date_entry.get().strip()
            try:
                d   = _dt.date.fromisoformat(date_str)
                dow = d.strftime("%A")
                day_lbl.configure(text=f"{dow}  •  {d.strftime('%d %b %Y')}",
                                  text_color=ARMY_BG)
            except Exception:
                day_lbl.configure(text="⚠️ Invalid date (YYYY-MM-DD)", text_color=RED)
                return

            _load_data(date_str)
            _refresh_sidebar()

            existing = menu_state["existing_batch"]
            if existing:
                status_lbl.configure(
                    text=f"✅ {len(existing)} saved", text_color=GREEN)
                _build_view_mode(existing, date_str, dow)
            else:
                status_lbl.configure(
                    text="No entries — create below", text_color="#9CA3AF")
                _build_create_mode(date_str, dow)

        date_entry.bind("<Return>",   lambda e: _build_slots())
        date_entry.bind("<FocusOut>", lambda e: _build_slots())
        _build_slots()

        # ──────────────────────────────────────────────────────────────────
        # SAVE LOGIC
        # ──────────────────────────────────────────────────────────────────
        def _save_daily(date_str):
            try:
                _dt.date.fromisoformat(date_str)
            except Exception:
                self._popup("⚠️ Invalid Date", "Use YYYY-MM-DD format.")
                return

            all_sources = (
                list(slot_widgets.items()) +
                [(f"Extra {i+1}", er) for i, er in enumerate(extra_rows)]
            )
            saved = 0
            logs  = []

            with get_db() as conn:
                for meal_type, sw in all_sources:
                    sel = sw["dropdown"].get()
                    if sel in ("— Skip —", ""):
                        continue
                    if sel.startswith("⭐ "):
                        sel = sel[2:]
                    m = menu_state["menu_by_name"].get(sel)
                    if not m:
                        continue
                    mid      = m["id"]
                    sp       = m["sp"]
                    cogs_per = m["cogs"] if m["cogs"] else 0.0
                    try:
                        qty = int(sw["qty_entry"].get() or 0)
                    except ValueError:
                        self._popup("⚠️ Invalid", f"Enter a valid number for {meal_type}.")
                        return
                    if qty <= 0:
                        continue
                    try:
                        samp_qty  = max(0, int(sw["samp_entry"].get()  or 0))
                    except ValueError:
                        samp_qty = 0
                    try:
                        staff_qty = max(0, int(sw["staff_entry"].get() or 0))
                    except ValueError:
                        staff_qty = 0

                    # 1. batch_prep
                    conn.execute(
                        "INSERT INTO batch_prep (date, menu_id, qty_prepared, samples, staff) "
                        "VALUES (?,?,?,?,?)",
                        (date_str, mid, qty, samp_qty, staff_qty))

                    # 2. Auto-deduct stock + ledger
                    details   = menu_state["recipe_detail"].get(mid, [])
                    total_raw = 0.0
                    for d in details:
                        deduct = d["qpu"] * qty
                        conn.execute(
                            "UPDATE inventory SET stock = MAX(0, stock - ?) WHERE id=?",
                            (deduct, d["inv_id"]))
                        conn.execute(
                            "INSERT INTO stock_ledger "
                            "(date, inv_id, transaction_type, qty_change, notes) "
                            "VALUES (?,?,?,?,?)",
                            (date_str, d["inv_id"], "DAILY_MENU", -deduct,
                             f"Daily menu: {sel} ({meal_type}) x{qty}"))
                        total_raw += deduct * (d["cp"] or 0.0)

                    # 3. Expenditure entry
                    if total_raw > 0:
                        conn.execute(
                            "INSERT INTO expenditure (date, amount, category, notes) "
                            "VALUES (?,?,?,?)",
                            (date_str, round(total_raw, 2), "Raw Material",
                             f"Auto: {sel} x{qty}"))

                    # 4. General samples
                    if samp_qty > 0:
                        conn.execute(
                            "INSERT INTO samples "
                            "(date, menu_id, meal, sp, qty, cost, given_to, notes) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                            (date_str, mid, meal_type, sp, samp_qty,
                             round(cogs_per * samp_qty, 2), "General",
                             f"Auto from daily menu: {sel}"))

                    # 5. Staff meals
                    if staff_qty > 0:
                        conn.execute(
                            "INSERT INTO samples "
                            "(date, menu_id, meal, sp, qty, cost, given_to, notes) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                            (date_str, mid, meal_type, sp, staff_qty,
                             round(cogs_per * staff_qty, 2), "Staff",
                             f"Auto from daily menu: {sel}"))

                    logs.append(f"{meal_type}: {sel} ×{qty}")
                    saved += 1

            if saved > 0:
                self._toast(f"✅ Saved {saved} item(s)  —  " + " | ".join(logs))
                _build_slots()
            else:
                self._popup("⚠️ Nothing saved",
                            "Select a menu item and enter at least 1 plate.")

