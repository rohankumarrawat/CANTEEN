"""
Patcher: Modernise all dialogs → in-app modals, seed menu/stock/sales data.
Run once from the canteen/ directory.
"""
import os, sqlite3, hashlib, shutil
from datetime import datetime, timedelta

BASE  = os.path.dirname(os.path.abspath(__file__))
SRC   = os.path.join(BASE, "app.py")
BCK   = os.path.join(BASE, "app_backup_before_modal.py")
DB    = os.path.join(BASE, "canteen.db")

shutil.copy2(SRC, BCK)
print("✓ Backup saved:", BCK)

# ── 1. Read original ──────────────────────────────────────────────────────────
with open(SRC) as f:
    code = f.read()

# ── 2. Insert _show_modal after _popup ────────────────────────────────────────
MODAL_METHOD = '''
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

'''

# Insert right after _popup closes (before _pg_dashboard)
code = code.replace(
    "    # ══════════════════════════════════════════════════════════════════════════\n"
    "    # DASHBOARD",
    MODAL_METHOD +
    "    # ══════════════════════════════════════════════════════════════════════════\n"
    "    # DASHBOARD"
)

# ── 3. Replace _dlg_inv_add ───────────────────────────────────────────────────
OLD_ADD = '''    def _dlg_inv_add(self):
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

        btn(win, "✅  Save Item", save, fg=GREEN, hv=DGREEN, h=46).pack(padx=24, pady=18, fill="x")'''

NEW_ADD = '''    def _dlg_inv_add(self):
        body, card, close = self._show_modal("＋  Add New Inventory Item", 540, 500)
        fields = {}
        CATEGORIES = ["Dry", "Fresh", "Dairy", "Bakery", "Prepared", "Misc"]

        for lbl_t, ph, attr, is_menu in [
            ("Item Name", "e.g., Mustard Oil", "name", False),
            ("Unit (kg / ltr / pcs)", "e.g., kg", "unit", False),
            ("Opening Stock", "e.g., 20", "stock", False),
            ("Minimum Level Alert", "e.g., 5", "min_lvl", False),
            ("Cost Price per Unit (₹)", "e.g., 90", "cp", False),
        ]:
            lbl(body, lbl_t, size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(8,3))
            e = entry(body, ph=ph, h=38); e.pack(fill="x")
            fields[attr] = e

        lbl(body, "Category", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(8,3))
        cat_menu = ctk.CTkOptionMenu(body, values=CATEGORIES,
                                     font=ctk.CTkFont(size=12))
        cat_menu.set("Dry"); cat_menu.pack(fill="x")

        def save():
            try:
                nm  = fields["name"].get().strip()
                unit = fields["unit"].get().strip()
                stk = float(fields["stock"].get() or 0)
                mn  = float(fields["min_lvl"].get() or 0)
                cp  = float(fields["cp"].get() or 0)
                cat = cat_menu.get()
            except ValueError:
                self._popup("⚠️ Invalid", "Enter numeric values for stock/min/cost."); return
            if not nm or not unit:
                self._popup("⚠️ Missing", "Item name and unit are required."); return
            with get_db() as conn:
                try:
                    conn.execute("INSERT INTO inventory (item,cat,unit,stock,min_lvl,opening,cp) VALUES (?,?,?,?,?,?,?)",
                                 (nm, cat, unit, stk, mn, stk, cp))
                except sqlite3.IntegrityError:
                    self._popup("⚠️ Duplicate", f"'{nm}' already exists."); return
            self._popup("✅ Added!", f"{nm} ({cat}) added to inventory.")
            close(); self._go("inventory")

        btn(card, "✅  Add Item", save, fg=GREEN, hv=DGREEN, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")'''

code = code.replace(OLD_ADD, NEW_ADD)

# ── 4. Replace _dlg_inv_receive ──────────────────────────────────────────────
OLD_RCV = '''    def _dlg_inv_receive(self):
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

        btn(win,"✅  Confirm Receipt",save,fg=TEAL,hv=ARMY_BG,h=46).pack(padx=24,pady=18,fill="x")'''

NEW_RCV = '''    def _dlg_inv_receive(self):
        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        body, card, close = self._show_modal("📥  Receive / Add Stock", 520, 380)

        lbl(body, "Select Item", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        iom = ctk.CTkOptionMenu(body, values=items, font=ctk.CTkFont(size=12))
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
            padx=18, pady=12, fill="x", side="bottom")'''

code = code.replace(OLD_RCV, NEW_RCV)

# ── 5. Replace _dlg_inv_edit ─────────────────────────────────────────────────
OLD_EDIT = '''    def _dlg_inv_edit(self):
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

        btn(win,"✅  Save Changes",save,fg=BLUE,hv=DBLUE,h=46).pack(padx=24,pady=18,fill="x")'''

NEW_EDIT = '''    def _dlg_inv_edit(self):
        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        body, card, close = self._show_modal("✏️  Edit Inventory Item", 520, 420)

        lbl(body, "Select Item", size=11, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,3))
        iom = ctk.CTkOptionMenu(body, values=items, font=ctk.CTkFont(size=12))
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
            padx=18, pady=12, fill="x", side="bottom")'''

code = code.replace(OLD_EDIT, NEW_EDIT)

# ── 6. Replace _dlg_inv_del ──────────────────────────────────────────────────
OLD_DEL = '''    def _dlg_inv_del(self):
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

        btn(win,"🗑  Delete Permanently",delete,fg=RED,hv=DRED,h=46).pack(padx=24,pady=16,fill="x")'''

NEW_DEL = '''    def _dlg_inv_del(self):
        with get_db() as conn:
            items = sorted([r["item"] for r in conn.execute("SELECT item FROM inventory ORDER BY item")])

        body, card, close = self._show_modal("🗑  Delete Inventory Item", 500, 280)

        lbl(body, "Select Item to Delete", size=12, weight="bold", color=ARMY_BG).pack(anchor="w", pady=(4,6))
        iom = ctk.CTkOptionMenu(body, values=items, font=ctk.CTkFont(size=12))
        iom.set(items[0] if items else ""); iom.pack(fill="x", pady=(0,10))

        warn = ctk.CTkFrame(body, fg_color=BG_RED, corner_radius=10)
        warn.pack(fill="x", pady=(4,0))
        lbl(warn, "⚠️  This permanently removes the item and all its recipe links.",
            size=10, color=RED).pack(padx=12, pady=10)

        def delete():
            item = iom.get()
            with get_db() as conn:
                conn.execute("DELETE FROM inventory WHERE item=?", (item,))
            self._popup("✅ Deleted!", f"{item} removed.")
            close(); self._go("inventory")

        btn(card, "🗑  Delete Permanently", delete, fg=RED, hv=DRED, h=46).pack(
            padx=18, pady=12, fill="x", side="bottom")'''

code = code.replace(OLD_DEL, NEW_DEL)

# ── 7. Also modernise _dlg_add_user ──────────────────────────────────────────
OLD_ADD_U = '''    def _dlg_add_user(self):
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

        btn(win,"✅  Create User",save,fg=GREEN,hv=DGREEN,h=46).pack(padx=24,pady=16,fill="x")'''

NEW_ADD_U = '''    def _dlg_add_user(self):
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
            padx=18, pady=12, fill="x", side="bottom")'''

code = code.replace(OLD_ADD_U, NEW_ADD_U)

# ── 8. Modernise _dlg_reset_pwd ──────────────────────────────────────────────
OLD_RPW = '''    def _dlg_reset_pwd(self):
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
        btn(win,"✅  Reset",save,fg=BLUE,hv=DBLUE,h=44).pack(padx=24,pady=16,fill="x")'''

NEW_RPW = '''    def _dlg_reset_pwd(self):
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
            padx=18,pady=12,fill="x",side="bottom")'''

code = code.replace(OLD_RPW, NEW_RPW)

# ── 9. Modernise _dlg_toggle_user ────────────────────────────────────────────
OLD_TOG = '''    def _dlg_toggle_user(self):
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
        btn(win,"✅  Update",save,fg=TEAL,hv=ARMY_BG,h=44).pack(padx=24,pady=14,fill="x")'''

NEW_TOG = '''    def _dlg_toggle_user(self):
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
            padx=18,pady=12,fill="x",side="bottom")'''

code = code.replace(OLD_TOG, NEW_TOG)


# ── 10. Write patched file ────────────────────────────────────────────────────
with open(SRC, "w") as f:
    f.write(code)
print("✓ app.py patched — all dialogs now use in-app modals")

# ── 11. Seed real sales data from menu photo ──────────────────────────────────
def _hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

# Ensure all menu + inventory from photo exist
menus = {r["name"]: r["id"] for r in conn.execute("SELECT id,name FROM menu")}
inv   = {r["item"]: r["id"] for r in conn.execute("SELECT id,item FROM inventory")}
inv_cp= {r["item"]: r["cp"]  for r in conn.execute("SELECT item,cp FROM inventory")}

# Add any missing menu items (they should already exist)
MENU_ITEMS = [
    ("Panchratna Dal Thali", 70),
    ("Kadhi Pakoda Thali",   70),
    ("Rajma Thali",          70),
    ("Kala Chana Thali",     70),
    ("Chana Dal Paneer Thali",70),
    ("Veg Manchurian & Fried Rice", 50),
    ("Kadhi Chawal",  50),
    ("Rajma Rice",    50),
    ("Veg Biryani",   50),
    ("Matar Kulcha",  50),
]
for nm, sp in MENU_ITEMS:
    conn.execute("INSERT OR IGNORE INTO menu (name,sp,active) VALUES (?,?,1)", (nm, sp))
conn.commit()
menus = {r["name"]: r["id"] for r in conn.execute("SELECT id,name FROM menu")}

# ── Seed sales for past 6 days ──────────────────────────────────────────────
# AWWA Weekly schedule from the menu board:
# Mon: Panchratna Dal Thali (lunch) + Veg Manchurian & Fried Rice (mini)
# Tue: Kadhi Pakoda Thali  + Kadhi Chawal
# Wed: Rajma Thali          + Rajma Rice
# Thu: Kala Chana Thali     + Veg Biryani
# Fri: Chana Dal Paneer Thali + Matar Kulcha
WEEKDAY_MENU = {
    0: ("Panchratna Dal Thali",     "Veg Manchurian & Fried Rice"),  # Mon
    1: ("Kadhi Pakoda Thali",       "Kadhi Chawal"),                  # Tue
    2: ("Rajma Thali",              "Rajma Rice"),                    # Wed
    3: ("Kala Chana Thali",         "Veg Biryani"),                   # Thu
    4: ("Chana Dal Paneer Thali",   "Matar Kulcha"),                  # Fri
}
import random
random.seed(42)

today = datetime.now().date()
for days_ago in range(1, 7):
    d = today - timedelta(days=days_ago)
    dt_str = d.strftime("%Y-%m-%d")
    wd = d.weekday()
    if wd not in WEEKDAY_MENU:
        continue  # skip weekends
    lunch_nm, mini_nm = WEEKDAY_MENU[wd]
    if lunch_nm not in menus or mini_nm not in menus:
        continue
    # Skip if already seeded
    existing = conn.execute("SELECT COUNT(*) FROM sales WHERE date=?", (dt_str,)).fetchone()[0]
    if existing > 0:
        continue

    for meal_nm, sold_range, pay_mode in [
        (lunch_nm, (85, 140), "Cash"),
        (mini_nm,  (30, 70),  "UPI"),
    ]:
        if meal_nm not in menus: continue
        mid = menus[meal_nm]
        sp  = conn.execute("SELECT sp FROM menu WHERE id=?", (mid,)).fetchone()["sp"]
        sold = random.randint(*sold_range)
        waste = random.randint(0, 6)

        # Calculate cost from recipes
        recipes = conn.execute("SELECT inv_id,qty_per_unit FROM recipes WHERE menu_id=?", (mid,)).fetchall()
        cpu = 0
        for rc in recipes:
            row = conn.execute("SELECT cp FROM inventory WHERE id=?", (rc["inv_id"],)).fetchone()
            if row: cpu += rc["qty_per_unit"] * row["cp"]

        conn.execute(
            "INSERT INTO sales (date,menu_id,meal,sp,sold,wastage,cogs,payment) VALUES (?,?,?,?,?,?,?,?)",
            (dt_str, mid, meal_nm, sp, sold, waste, (sold+waste)*cpu, pay_mode))

conn.commit()
print("✓ Sample sales seeded for past 6 working days (Mon–Fri)")

# ── 12. Add extra stock receives to make dashboard interesting ────────────────
today_str = today.strftime("%Y-%m-%d")
extra_stock = [
    ("Rice",               50, 40),
    ("Roti Dough",         20, 20),
    ("Seasonal Vegetables",30, 30),
    ("Panchratna Dal Mix", 15, 120),
    ("Kadhi Base",         12, 120),
    ("Rajma",              20, 150),
    ("Kala Chana",         18, 140),
    ("Chana Dal",          15, 130),
    ("Paneer",             10, 260),
    ("Kulcha",             80, 25),
]
for item_nm, qty, cp in extra_stock:
    row = conn.execute("SELECT id FROM inventory WHERE item=?", (item_nm,)).fetchone()
    if not row: continue
    inv_id = row["id"]
    already = conn.execute("SELECT COUNT(*) FROM goods_received WHERE date=? AND inv_id=?",
                           (today_str, inv_id)).fetchone()[0]
    if already: continue
    conn.execute("UPDATE inventory SET stock=stock+?,received=received+?,cp=? WHERE id=?",
                 (qty, qty, cp, inv_id))
    conn.execute("INSERT INTO goods_received (date,inv_id,qty,total_cost) VALUES (?,?,?,?)",
                 (today_str, inv_id, qty, qty*cp))

conn.commit()
conn.close()
print("✓ Stock replenished for today")
print("\n✅  All done! Run:  .venv/bin/python3 app.py")
