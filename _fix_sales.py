"""
Final fix: inject _sales_methods.py into app.py at the right location.
Reads from original backup, removes broken sections, inserts new clean methods.
"""

BACKUP  = "/Users/rohan/Desktop/canteen/app.py.bak_sales_fix_20260521_103941"
METHODS = "/Users/rohan/Desktop/canteen/_sales_methods.py"
OUTFILE = "/Users/rohan/Desktop/canteen/app.py"

# Read backup as bytes
cur_lines = open(BACKUP, "rb").read().split(b"\n")
cur_lines = [l + b"\n" for l in cur_lines[:-1]] + ([cur_lines[-1]] if cur_lines[-1] else [])
print(f"Backup lines: {len(cur_lines)}")

# Read new methods as UTF-8 bytes
new_methods_bytes = open(METHODS, "rb").read()
new_method_lines  = [l + b"\n" for l in new_methods_bytes.split(b"\n")[:-1]]

# ─── Step 1: Find insertion point ─────────────────────────────────────────────
# We want to insert _pg_sales right before _pg_batch and the section comment before it
pg_batch_start = None
for i, l in enumerate(cur_lines):
    if b"def _pg_batch(self):" in l:
        pg_batch_start = i
        break
assert pg_batch_start is not None, "_pg_batch not found"
print(f"_pg_batch at line {pg_batch_start+1}")

# Walk backwards to find the section header (═══ line) before _pg_batch
insert_point = pg_batch_start
for i in range(pg_batch_start-1, max(0, pg_batch_start-6), -1):
    if cur_lines[i].startswith(b"    # \xe2\x95\x90"):
        insert_point = i
        break
print(f"Insertion point: line {insert_point+1}")

# ─── Step 2: Remove broken/mangled content between _pg_dashboard and _pg_batch ──
# The old _pg_sales (mangled) code is somewhere in this range
# Also remove any _save_one_sale, _save_all_sales, _apply_stock_deduction, _filter_sale_cards

methods_to_remove = [
    b"def _save_one_sale(self",
    b"def _save_all_sales(self)",
    b"def _apply_stock_deduction(self",
    b"def _filter_sale_cards(self)",
]

# Find and mark ranges to remove (in reverse order)
remove_ranges = []
for target in methods_to_remove:
    for i, l in enumerate(cur_lines):
        if target in l and l.startswith(b"    def "):
            func_end = len(cur_lines)
            for j in range(i+1, i+400):
                if j >= len(cur_lines): break
                if (cur_lines[j].startswith(b"    def ") or
                    cur_lines[j].startswith(b"    # \xe2\x95\x90")) and j != i:
                    func_end = j
                    break
            remove_ranges.append((i, func_end))
            print(f"Will remove '{target.decode('latin-1')}' at lines {i+1}-{func_end}")
            break

# Also remove the mangled bot.pack area (line 743 in the backup) and clean it
# Line 743 (0-indexed: 742): bot.pack mangle
mangled_bot = None
for i, l in enumerate(cur_lines):
    if b'bot.pack(fill="both", expand=True, padx=PAD, p' in l and b'with get_db()' in l:
        mangled_bot = i
        break

if mangled_bot is not None:
    print(f"Mangled bot.pack at line {mangled_bot+1}: {cur_lines[mangled_bot][:80]}")
    cur_lines[mangled_bot] = b'        bot.pack(fill="both", expand=True, padx=PAD, pady=(8,0))\n'
    cur_lines.insert(mangled_bot+1, b'        with get_db() as conn:\n')
    # Adjust remove_ranges (all indices > mangled_bot shift +1)
    remove_ranges = [(s+1 if s > mangled_bot else s, e+1 if e > mangled_bot else e)
                     for s, e in remove_ranges]
    # Also adjust insert_point
    insert_point += 1
    print(f"Fixed bot.pack mangle, new line count: {len(cur_lines)}")

# Also remove the mangled card-loop duplicate (if present)
# Look for self._sale_cards.append mangled with border_width
for i, l in enumerate(cur_lines):
    if b"self._sale_cards.append" in l and b"border_width" in l:
        print(f"Mangled append at line {i+1}")
        cur_lines[i] = b'            self._sale_cards.append((name2.lower(), mc))\n'
        # Find end of dead duplicate loop: look for "Save All bar" comment
        dead_end = None
        for j in range(i+1, i+70):
            if j >= len(cur_lines): break
            if b"Save All bar" in cur_lines[j]:
                dead_end = j
                break
        if dead_end:
            print(f"Removing dead duplicate loop lines {i+2} to {dead_end}")
            del cur_lines[i+1:dead_end]
            # Adjust all indices > i
            remove_ranges = [(s - (dead_end - i - 1) if s > i else s,
                              e - (dead_end - i - 1) if e > i else e)
                             for s, e in remove_ranges]
            insert_point -= (dead_end - i - 1) if insert_point > i else 0
        break

print(f"After cleaning: {len(cur_lines)} lines")

# Sort and remove in reverse order
remove_ranges.sort(reverse=True)
for start, end in remove_ranges:
    if start < len(cur_lines):
        print(f"Deleting lines {start+1} to {end}")
        del cur_lines[start:end]

print(f"After removals: {len(cur_lines)} lines")

# Recalculate insert_point (find _pg_batch again)
pg_batch_start2 = None
for i, l in enumerate(cur_lines):
    if b"def _pg_batch(self):" in l:
        pg_batch_start2 = i
        break
insert_point2 = pg_batch_start2
for i in range(pg_batch_start2-1, max(0, pg_batch_start2-6), -1):
    if cur_lines[i].startswith(b"    # \xe2\x95\x90"):
        insert_point2 = i
        break
print(f"Final insertion point: line {insert_point2+1}")

# ─── Step 3: Insert new methods ───────────────────────────────────────────────
for j, nl in enumerate(new_method_lines):
    cur_lines.insert(insert_point2 + j, nl)
print(f"After insertion: {len(cur_lines)} lines")

# ─── Write ────────────────────────────────────────────────────────────────────
open(OUTFILE, "wb").write(b"".join(cur_lines))
print(f"Written to {OUTFILE}")

# ─── Syntax check ─────────────────────────────────────────────────────────────
import py_compile, tempfile, shutil
tmp = tempfile.mktemp(suffix=".py")
shutil.copy(OUTFILE, tmp)
try:
    py_compile.compile(tmp, doraise=True)
    print("SYNTAX CHECK: PASSED ✓")
except py_compile.PyCompileError as e:
    print(f"SYNTAX CHECK: FAILED — {e}")

# ─── Verify ───────────────────────────────────────────────────────────────────
lines2 = open(OUTFILE, "rb").read().split(b"\n")
pg_defs = [(i+1, l.decode("latin-1", errors="replace").strip())
           for i, l in enumerate(lines2) if b"def _pg_" in l]
print(f"\nPage methods found:")
for lineno, content in pg_defs:
    print(f"  Line {lineno}: {content}")
