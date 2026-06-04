import os
path = "/Users/rohan/Desktop/canteen/app.py"
with open(path) as f: code = f.read()

# 1. Batch Prep Auto-Deduct
code = code.replace(
'''        band(bc, "📝  Enter Batch Quantities  — stock auto-deducted on save")''',
'''        band(bc, "📝  Enter Batch Quantities")
        self._batch_deduct = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(bc, text="Auto-deduct stock for ingredients based on 'Master > Daily Recipes'", 
                        variable=self._batch_deduct, text_color=ARMY_BG, font=ctk.CTkFont(size=11, weight="bold")
                       ).pack(anchor="w", padx=14, pady=(10,0))'''
)

code = code.replace(
'''                for rc in conn.execute("SELECT inv_id,qty_per_unit FROM recipes WHERE menu_id=?",
                                       (mid2,)):
                    conn.execute("UPDATE inventory SET stock=stock-?,received=received WHERE id=?",
                                 (rc["qty_per_unit"]*qty, rc["inv_id"]))''',
'''                if getattr(self, "_batch_deduct", None) and self._batch_deduct.get():
                    for rc in conn.execute("SELECT inv_id,qty_per_unit FROM recipes WHERE menu_id=?", (mid2,)):
                        conn.execute("UPDATE inventory SET stock=stock-?,received=received WHERE id=?",
                                     (rc["qty_per_unit"]*qty, rc["inv_id"]))'''
)

# 2. Expenditure Deduct (Update Stock)
EXP_TITLE = '''        lbl(ff,"Amount (₹)",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=2,sticky="w",padx=(20,0),pady=(0,4))'''
EXP_NEW_TITLE = '''        lbl(ff,"Amount (₹)",size=11,weight="bold",color=ARMY_BG).grid(row=0,column=2,sticky="w",padx=(20,0),pady=(0,4))

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
        cdc.configure(command=toggle_inv)'''
code = code.replace(EXP_TITLE, EXP_NEW_TITLE)

EXP_SAVE = '''            with get_db() as conn:
                conn.execute("INSERT INTO expenditure (date,amount,category,notes) VALUES (?,?,?,?)",
                             (exp_date, amt, cat, notes or None))'''
EXP_NEW_SAVE = '''            try: 
                eq = float(exp_qty.get() or 0) if self._exp_deduct.get() else 0
            except: 
                self._popup("⚠️ Invalid","Enter numeric qty"); return
            
            with get_db() as conn:
                conn.execute("INSERT INTO expenditure (date,amount,category,notes) VALUES (?,?,?,?)",
                             (exp_date, amt, cat, notes or None))
                if self._exp_deduct.get() and eq > 0:
                    it = exp_iom.get()
                    row = conn.execute("SELECT id,cp FROM inventory WHERE item=?", (it,)).fetchone()
                    conn.execute("UPDATE inventory SET stock=stock+?,received=received+?,cp=? WHERE item=?",
                                 (eq, eq, row["cp"], it))
                    conn.execute("INSERT INTO goods_received (date,inv_id,qty,total_cost) VALUES (?,?,?,?)",
                                 (exp_date, row["id"], eq, amt))'''
code = code.replace(EXP_SAVE, EXP_NEW_SAVE)

# 3. Add search to stock dialogs
s1_old = '''        lbl(body, "Select Item", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        iom = ctk.CTkOptionMenu(body, values=items, font=ctk.CTkFont(size=12))'''
s1_new = '''        lbl(body, "Select Item (Searchable)", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        se = ctk.CTkEntry(body, placeholder_text="🔍 Type to search...", height=32); se.pack(fill="x", pady=(0,4))
        iom = ctk.CTkOptionMenu(body, values=items or ["(none)"], font=ctk.CTkFont(size=12))
        def filter_items(*args, e=se, i=iom, opts=items):
            q = e.get().lower(); fil = [x for x in opts if q in x.lower()]
            i.configure(values=fil or ["(none)"])
            if fil: i.set(fil[0])
        se.bind("<KeyRelease>", filter_items)'''
code = code.replace(s1_old, s1_new)

s2_old = '''        lbl(body, "Select Item to Delete", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,6))
        iom = ctk.CTkOptionMenu(body, values=items, font=ctk.CTkFont(size=12))'''
s2_new = '''        lbl(body, "Select Item to Delete (Searchable)", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,6))
        se = ctk.CTkEntry(body, placeholder_text="🔍 Type to search...", height=32); se.pack(fill="x", pady=(0,4))
        iom = ctk.CTkOptionMenu(body, values=items or ["(none)"], font=ctk.CTkFont(size=12))
        def filter_items(*args, e=se, i=iom, opts=items):
            q = e.get().lower(); fil = [x for x in opts if q in x.lower()]
            i.configure(values=fil or ["(none)"])
            if fil: i.set(fil[0])
        se.bind("<KeyRelease>", filter_items)'''
code = code.replace(s2_old, s2_new)

# 4. Add Ingredients button to Menu Master
BTN_OLD = '''            ctk.CTkButton(af, text="✏️", width=32, height=28, corner_radius=6,'''
BTN_NEW = '''            ctk.CTkButton(af, text="🥗", width=32, height=28, corner_radius=6,
                          fg_color=BG_GRN, hover_color=T_GRN, text_color=GREEN,
                          font=ctk.CTkFont(size=13),
                          command=lambda mid=m["id"],nm=m["name"]:
                              self._modal_edit_ingredients(mid, nm)).pack(side="left", padx=(0,4))
            ctk.CTkButton(af, text="✏️", width=32, height=28, corner_radius=6,'''
code = code.replace(BTN_OLD, BTN_NEW)

# 5. _modal_edit_ingredients
MODAL_FUNC = '''    def _modal_edit_ingredients(self, mid, name):
        body, card, close = self._show_modal(f"🥗  Ingredients: {name}", 600, 480)
        
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
'''

code = code.replace(
    '    def _dlg_add_menu(self):        self._modal_add_menu()',
    MODAL_FUNC + '\n    def _dlg_add_menu(self):        self._modal_add_menu()'
)

with open(path, "w") as f: f.write(code)
print("done")
