import sys

def main():
    filepath = '/Users/rohan/Desktop/canteen/app.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_anchor = '    def _master_daily_menu(self, wrap):'
    end_anchor = '    def _master_schedule(self, wrap):'

    start_idx = content.find(start_anchor)
    if start_idx == -1:
        print("Error: Could not find start anchor")
        sys.exit(1)

    end_idx = content.find(end_anchor)
    if end_idx == -1:
        print("Error: Could not find end anchor")
        sys.exit(1)

    new_implementation = """    def _master_daily_menu(self, wrap):
        \"\"\"
        Date-wise daily menu creation & viewing.
        - All 3 meal slots always visible (Lunch, Paratha, Mini Meal)
        - Each slot: Dropdown menu for item selection, Plates (Qty), Samples, Staff inputs
        - Auto-ingredient preview for known items
        - Save: auto-deducts stock, creates expenditure, batch_prep, samples
        \"\"\"
        import datetime as _dt

        today_str = datetime.now().strftime("%Y-%m-%d")
        MEAL_SLOTS = ["Lunch", "Paratha", "Mini Meal"]

        # ── State ─────────────────────────────────────────────────────────────
        slot_widgets = {}  # meal_type → {dropdown, qty_entry, samp_entry, staff_entry, preview_lbl, preview_frame}
        menu_state   = {"menu_by_name": {}, "menu_names": [], "recipe_detail": {},
                        "sched_map": {}}

        def _load_data(date_str):
            \"\"\"Load menus, schedule and recipes for the given date.\"\"\"
            with get_db() as conn:
                all_menus = conn.execute(
                    "SELECT id, name, sp, cogs, default_samples, default_staff "
                    "FROM menu WHERE active=1 ORDER BY name"
                ).fetchall()
                sched_rows = conn.execute(
                    "SELECT dm.day, dm.meal_type, m.name, m.id as menu_id, "
                    "m.default_samples, m.default_staff "
                    "FROM daily_menu dm JOIN menu m ON m.id=dm.menu_id"
                ).fetchall()
                all_recipes = conn.execute(
                    "SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
                    "FROM recipes r JOIN inventory i ON i.id=r.inv_id"
                ).fetchall()

            menu_state["menu_by_name"] = {m["name"]: m for m in all_menus}
            menu_state["menu_names"]   = [m["name"] for m in all_menus]
            sched_map = {}
            for s in sched_rows:
                sched_map.setdefault(s["day"], {})[s["meal_type"]] = s["name"]
            menu_state["sched_map"] = sched_map
            recipe_detail = {}
            for r in all_recipes:
                recipe_detail.setdefault(r["menu_id"], []).append({
                    "item": r["item"], "qpu": r["qty_per_unit"],
                    "unit": r["unit"],  "cp":  r["cp"],
                    "inv_id": r["inv_id"]
                })
            menu_state["recipe_detail"] = recipe_detail

        # ── Date picker card ──────────────────────────────────────────────────
        date_card = card(wrap); date_card.pack(fill="x", pady=(0, 10))
        band(date_card, "📅  Select Date  —  View or Create Daily Menu",
             bg=ARMY_BG, tc=GOLD_LT, h=38)

        dr = ctk.CTkFrame(date_card, fg_color="transparent")
        dr.pack(fill="x", padx=14, pady=(10, 4))
        lbl(dr, "Date (YYYY-MM-DD):", size=11, weight="bold", color=ARMY_BG
            ).pack(side="left", padx=(0, 10))
        date_var   = ctk.StringVar(value=today_str)
        date_entry = ctk.CTkEntry(dr, textvariable=date_var, height=40, width=170,
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  border_color=BORDER, justify="center")
        date_entry.pack(side="left", padx=(0, 10))
        day_lbl    = lbl(dr, "", size=13, weight="bold", color=ARMY_BG)
        day_lbl.pack(side="left", padx=8)
        status_lbl = ctk.CTkLabel(dr, text="", font=ctk.CTkFont(size=11),
                                  text_color=GREEN)
        status_lbl.pack(side="left", padx=8)

        # ── Slots container ───────────────────────────────────────────────────
        slots_container = ctk.CTkFrame(wrap, fg_color="transparent")
        slots_container.pack(fill="x")

        def _update_slot_preview(meal_type):
            sw = slot_widgets.get(meal_type)
            if not sw: return

            sel = sw["dropdown"].get()
            if sel.startswith("⭐ "):
                sel = sel[2:]

            m = menu_state["menu_by_name"].get(sel)
            pf = sw["preview_frame"]
            pl = sw["preview_lbl"]

            if not m:
                pf.pack_forget()
                return

            mid = m["id"]
            details = menu_state["recipe_detail"].get(mid, [])
            try:
                qty = int(sw["qty_entry"].get() or 0)
            except ValueError:
                qty = 0

            if details and qty > 0:
                lines = [f"⚡ Auto-calc for {qty} plates of {sel}:"]
                for d in details[:8]:
                    total = d["qpu"] * qty
                    lines.append(f"  {d['item']}: {total:.2f} {d['unit']} "
                                 f"({d['qpu']:.3f}/plate × {qty})")
                if len(details) > 8:
                    lines.append(f"  +{len(details)-8} more")
                total_cost = sum(d["qpu"] * qty * d["cp"] for d in details)
                lines.append(f"\\n  💰 Total raw cost: ₹{total_cost:,.0f}")
                pl.configure(text="\\n".join(lines))
                pf.pack(fill="x", pady=(8,0))
            elif details and qty == 0:
                pl.configure(text=f"⚡ {sel} has {len(details)} ingredients — enter plates to see breakdown")
                pf.pack(fill="x", pady=(8,0))
            elif not details:
                pl.configure(text="⚠️ No ingredient recipes for this item — it has no recipes linked")
                pf.pack(fill="x", pady=(8,0))

        def _on_new_item_created(m_type, new_name):
            with get_db() as conn:
                r_menus = conn.execute(
                    "SELECT id, name, sp, cogs, default_samples, default_staff "
                    "FROM menu WHERE active=1 ORDER BY name"
                ).fetchall()
                r_recipes = conn.execute(
                    "SELECT r.menu_id, i.item, r.qty_per_unit, i.unit, i.cp, i.id as inv_id "
                    "FROM recipes r JOIN inventory i ON i.id=r.inv_id"
                ).fetchall()

            menu_state["menu_by_name"] = {m["name"]: m for m in r_menus}
            menu_state["menu_names"] = [m["name"] for m in r_menus]

            r_detail = {}
            for r in r_recipes:
                r_detail.setdefault(r["menu_id"], []).append({
                    "item": r["item"], "qpu": r["qty_per_unit"],
                    "unit": r["unit"], "cp": r["cp"], "inv_id": r["inv_id"]
                })
            menu_state["recipe_detail"] = r_detail

            try:
                d = _dt.date.fromisoformat(date_entry.get().strip())
                dow = d.strftime("%A")
            except:
                dow = "Monday"

            for m_t, sw in slot_widgets.items():
                curr_sel = sw["dropdown"].get()
                s_name = menu_state["sched_map"].get(dow, {}).get(m_t, "")

                dropdown_values = ["— Skip —", "＋ New Item"]
                if s_name and s_name in menu_state["menu_by_name"]:
                    dropdown_values.insert(1, f"⭐ {s_name}")
                for mn in menu_state["menu_names"]:
                    if mn != s_name:
                        dropdown_values.append(mn)

                sw["dropdown"].configure(values=dropdown_values)

                if m_t == m_type:
                    sw["dropdown"].set(new_name)
                    m_item = menu_state["menu_by_name"].get(new_name)
                    if m_item:
                        ds = m_item.get("default_samples", 0) or 0
                        dst = m_item.get("default_staff", 0) or 0
                        sw["samp_entry"].delete(0, "end")
                        if ds > 0: sw["samp_entry"].insert(0, str(ds))
                        sw["staff_entry"].delete(0, "end")
                        if dst > 0: sw["staff_entry"].insert(0, str(dst))
                else:
                    if curr_sel in dropdown_values:
                        sw["dropdown"].set(curr_sel)
                    else:
                        sw["dropdown"].set("— Skip —")

            _update_slot_preview(m_type)

        def _on_dd_change(val, mt):
            if val == "＋ New Item":
                slot_widgets[mt]["dropdown"].set("— Skip —")
                _update_slot_preview(mt)
                self._modal_add_menu(
                    target_date=date_entry.get().strip(),
                    callback=lambda new_name, m_type=mt: _on_new_item_created(m_type, new_name)
                )
            else:
                sw = slot_widgets.get(mt)
                if sw:
                    sel = val
                    if sel.startswith("⭐ "):
                        sel = sel[2:]
                    m = menu_state["menu_by_name"].get(sel)
                    if m:
                        ds = m.get("default_samples", 0) or 0
                        dst = m.get("default_staff", 0) or 0
                        sw["samp_entry"].delete(0, "end")
                        if ds > 0: sw["samp_entry"].insert(0, str(ds))
                        sw["staff_entry"].delete(0, "end")
                        if dst > 0: sw["staff_entry"].insert(0, str(dst))
                _update_slot_preview(mt)

        def _build_slots():
            for w in slots_container.winfo_children():
                w.destroy()
            slot_widgets.clear()

            date_str = date_entry.get().strip()
            try:
                d = _dt.date.fromisoformat(date_str)
                dow = d.strftime("%A")
                day_lbl.configure(text=f"{dow}  •  {d.strftime('%d %b %Y')}", text_color=ARMY_BG)
            except Exception:
                day_lbl.configure(text="⚠️ Invalid date format (use YYYY-MM-DD)", text_color=RED)
                return

            _load_data(date_str)

            type_colors = {"Lunch": ARMY_BG, "Paratha": TEAL, "Mini Meal": "#0F766E"}
            type_icons = {"Lunch": "🍛", "Paratha": "🥞", "Mini Meal": "🍱"}

            for meal_type in MEAL_SLOTS:
                tc = type_colors.get(meal_type, ARMY_BG)
                ti = type_icons.get(meal_type, "🍽")
                scheduled_name = menu_state["sched_map"].get(dow, {}).get(meal_type, "")

                dropdown_values = ["— Skip —", "＋ New Item"]
                if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
                    dropdown_values.insert(1, f"⭐ {scheduled_name}")
                for mn in menu_state["menu_names"]:
                    if mn != scheduled_name:
                        dropdown_values.append(mn)

                slot_card = ctk.CTkFrame(slots_container, fg_color=WHITE, corner_radius=14,
                                         border_width=2, border_color=BORDER)
                slot_card.pack(fill="x", pady=6)

                sh = ctk.CTkFrame(slot_card, fg_color=tc, corner_radius=0, height=34)
                sh.pack(fill="x"); sh.pack_propagate(False)
                lbl(sh, f"  {ti}  {meal_type}", size=12, weight="bold", color=WHITE).pack(side="left", padx=8)
                if scheduled_name:
                    lbl(sh, f"Scheduled: {scheduled_name}", size=9, color="#CCCCCC").pack(side="right", padx=12)

                body = ctk.CTkFrame(slot_card, fg_color="transparent")
                body.pack(fill="x", padx=14, pady=10)

                r1 = ctk.CTkFrame(body, fg_color="transparent")
                r1.pack(fill="x")
                r1.grid_columnconfigure(0, weight=4)
                r1.grid_columnconfigure(1, weight=2)
                r1.grid_columnconfigure(2, weight=1)
                r1.grid_columnconfigure(3, weight=1)

                dd_frame = ctk.CTkFrame(r1, fg_color="transparent")
                dd_frame.grid(row=0, column=0, sticky="nsew", padx=(0,8))
                lbl(dd_frame, "Menu Item", size=10, weight="bold", color=ARMY_BG).pack(anchor="w")
                dd = ctk.CTkOptionMenu(
                    dd_frame, values=dropdown_values,
                    font=ctk.CTkFont(size=12), height=40,
                    fg_color=ARMY_BG, button_color=ARMY_HVR, text_color=WHITE)
                dd.pack(fill="x", pady=(4,0))

                qty_frame = ctk.CTkFrame(r1, fg_color="transparent")
                qty_frame.grid(row=0, column=1, sticky="nsew", padx=(0,8))
                lbl(qty_frame, "Plates", size=10, weight="bold", color=ARMY_BG).pack(anchor="w")
                qty_e = ctk.CTkEntry(qty_frame, height=40, corner_radius=10,
                                     placeholder_text="0",
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     border_color=BORDER, justify="center")
                qty_e.pack(fill="x", pady=(4,0))

                samp_frame = ctk.CTkFrame(r1, fg_color="transparent")
                samp_frame.grid(row=0, column=2, sticky="nsew", padx=(0,8))
                lbl(samp_frame, "🎁 Samples", size=10, color=TEAL).pack(anchor="w")
                samp_e = ctk.CTkEntry(samp_frame, height=40, corner_radius=10,
                                      placeholder_text="0",
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      border_color=TEAL, justify="center",
                                      fg_color="#F0FDFA")
                samp_e.pack(fill="x", pady=(4,0))

                staff_frame = ctk.CTkFrame(r1, fg_color="transparent")
                staff_frame.grid(row=0, column=3, sticky="nsew")
                lbl(staff_frame, "👥 Staff", size=10, color=ARMY_BG).pack(anchor="w")
                staff_e = ctk.CTkEntry(staff_frame, height=40, corner_radius=10,
                                       placeholder_text="0",
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       border_color=ARMY_BG, justify="center",
                                       fg_color=BG_GRN)
                staff_e.pack(fill="x", pady=(4,0))

                if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
                    dd.set(f"⭐ {scheduled_name}")
                    ds = menu_state["menu_by_name"][scheduled_name].get("default_samples", 0) or 0
                    dst = menu_state["menu_by_name"][scheduled_name].get("default_staff", 0) or 0
                    if ds > 0: samp_e.insert(0, str(ds))
                    if dst > 0: staff_e.insert(0, str(dst))
                else:
                    dd.set("— Skip —")

                preview_f = ctk.CTkFrame(body, fg_color="#F0FDF4", corner_radius=8,
                                         border_width=1, border_color="#BBF7D0")
                preview_lbl = lbl(preview_f, "", size=9, color=ARMY_BG, wraplength=800)
                preview_lbl.pack(padx=8, pady=6, anchor="w")

                slot_widgets[meal_type] = {
                    "dropdown": dd,
                    "qty_entry": qty_e,
                    "samp_entry": samp_e,
                    "staff_entry": staff_e,
                    "preview_frame": preview_f,
                    "preview_lbl": preview_lbl,
                }

                qty_e.bind("<KeyRelease>", lambda e, mt=meal_type: _update_slot_preview(mt))
                dd.configure(command=lambda val, mt=meal_type: _on_dd_change(val, mt))

                if scheduled_name and scheduled_name in menu_state["menu_by_name"]:
                    self.after(100, lambda mt=meal_type: _update_slot_preview(mt))

        _build_slots()

        date_entry.bind("<Return>", lambda e: _build_slots())
        date_entry.bind("<FocusOut>", lambda e: _build_slots())

        # ── Buttons row ───────────────────────────────────────────────────────
        btn_row = ctk.CTkFrame(date_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=14, pady=(4, 12))

        btn(btn_row, "🔍  Load / Refresh", _build_slots,
            fg=BLUE, hv=DBLUE, h=40, w=180).pack(side="left", padx=(0, 10))

        # ── Save button ───────────────────────────────────────────────────────
        def _save_daily():
            date_str = date_entry.get().strip()
            try:
                _dt.date.fromisoformat(date_str)
            except Exception:
                self._popup("⚠️ Invalid Date", "Use YYYY-MM-DD format.")
                return

            saved = 0
            logs = []

            with get_db() as conn:
                for meal_type, sw in slot_widgets.items():
                    sel = sw["dropdown"].get()

                    if sel == "— Skip —":
                        continue

                    if sel.startswith("⭐ "):
                        sel = sel[2:]

                    m = menu_state["menu_by_name"].get(sel)
                    if not m:
                        continue

                    mid = m["id"]
                    sp = m["sp"]
                    cogs_per = m["cogs"] if m["cogs"] else 0.0

                    try:
                        qty = int(sw["qty_entry"].get() or 0)
                    except ValueError:
                        self._popup("⚠️ Invalid", f"Enter a valid number for {meal_type} plates.")
                        return
                    if qty <= 0:
                        continue

                    try:
                        samp_qty = max(0, int(sw["samp_entry"].get() or 0))
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

                    # 2. Auto-deduct stock + log stock_ledger
                    details = menu_state["recipe_detail"].get(mid, [])
                    total_raw_cost = 0.0
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
                        total_raw_cost += deduct * (d["cp"] or 0.0)

                    # Log cost as Expenditure
                    if total_raw_cost > 0:
                        conn.execute(
                            "INSERT INTO expenditure (date, amount, category, notes) "
                            "VALUES (?,?,?,?)",
                            (date_str, round(total_raw_cost, 2), "Raw Material",
                             f"Auto-expenditure for {sel} batch x{qty}"))

                    # 3. Samples table (given_to='General')
                    if samp_qty > 0:
                        conn.execute(
                            "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                            (date_str, mid, meal_type, sp, samp_qty,
                             round(cogs_per * samp_qty, 2), "General",
                             f"Auto from daily menu: {sel}"))

                    # 4. Samples table for Staff (given_to='Staff')
                    if staff_qty > 0:
                        conn.execute(
                            "INSERT INTO samples (date, menu_id, meal, sp, qty, cost, given_to, notes) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                            (date_str, mid, meal_type, sp, staff_qty,
                             round(cogs_per * staff_qty, 2), "Staff",
                             f"Auto from daily menu: {sel}"))

                    logs.append(f"{meal_type}: {sel} x{qty}")
                    saved += 1

            if saved > 0:
                self._toast(f"✅ Daily menu saved  •  " + " | ".join(logs))
                self._switch_master_tab("daily_menu")
            else:
                self._popup("⚠️ Nothing to save",
                            "Enter plates for at least one meal, or select items from dropdowns.")

        btn(btn_row, "✅  Save Daily Menu", _save_daily,
            fg=GREEN, hv=DGREEN, h=40, w=200).pack(side="left")

"""

    updated_content = content[:start_idx] + new_implementation + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("Success: Updated app.py daily menu tab!")

if __name__ == '__main__':
    main()
