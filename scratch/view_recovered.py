import ast
import os

with open("/Users/rohan/Desktop/canteen/recovered_master_daily_menu.py") as f:
    c = f.read()

try:
    decoded = ast.literal_eval(c)
    with open("/Users/rohan/Desktop/canteen/scratch/recovered_decoded.py", "w") as out:
        out.write(decoded)
    print("Decoded recovered_master_daily_menu.py successfully via ast!")
except Exception as e:
    print("Failed to decode recovered_master_daily_menu.py via ast:", e)
