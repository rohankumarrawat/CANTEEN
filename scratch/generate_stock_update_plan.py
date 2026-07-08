# Generate stock update plan markdown artifact
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from map_stock_updates import matched_updates, unmatched

artifact_dir = "/Users/rohan/.gemini/antigravity-ide/brain/daa8389e-76e5-4f45-9540-33e2b7eec427"
os.makedirs(artifact_dir, exist_ok=True)

md_path = os.path.join(artifact_dir, "stock_update_plan.md")

with open(md_path, "w") as f:
    f.write("# July 7, 2026 Stock Update Plan\n\n")
    f.write("> [!IMPORTANT]\n")
    f.write("> This plan outlines the matches between your sheet images and the canteen software inventory.\n")
    f.write("> In accordance with your instructions, we will **NOT** change item names or add new items. Only existing records will be updated.\n\n")
    
    f.write("## ⚠️ Unmatched Items (Will NOT be added or updated)\n")
    f.write("The following items from the sheets did not match any corresponding entry in the software's inventory:\n\n")
    f.write("| S/No | Sheet Name | Rate (Rs.) | Sheet Stock (BCF) | Reason / Status |\n")
    f.write("|---|---|---|---|---|\n")
    for idx, u in enumerate(unmatched, 1):
        f.write(f"| {idx} | {u['sheet_name']} | {u['rate']:.2f} | {u['bcf']:.3f} | No matching item name or duplicate slot in software inventory |\n")
    
    f.write("\n## ✅ Matched Items (To be updated)\n")
    f.write("The following updates will be written to the database once you approve:\n\n")
    f.write("| S/No | Sheet Name | Software Item Name | Prev Stock | New Stock (BCF) | Prev Rate | New Rate (Rate) |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for idx, m in enumerate(matched_updates, 1):
        f.write(f"| {idx} | {m['sheet_name']} | **{m['db_name']}** | {m['prev_stock']:.3f} | **{m['new_stock']:.3f}** | Rs. {m['prev_cp']:.2f} | **Rs. {m['new_cp']:.2f}** |\n")

print(f"✅ Generated stock update plan: {md_path}")
