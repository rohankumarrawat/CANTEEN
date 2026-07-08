import re

APP_PATH = "/Users/rohan/Desktop/canteen/app.py"

def replace_rupee():
    with open(APP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace literal ₹
    content_new = content.replace("₹", "Rs. ")
    
    # Replace unicode escape sequences \u20b9
    content_new = content_new.replace(r"\u20b9", "Rs. ")

    # Let's clean up any double spaces or formatting, e.g. "Rs.  "
    content_new = re.sub(r"Rs\.\s+", "Rs. ", content_new)
    # If there is something like "Amount (Rs. )", replace with "Amount (Rs.)"
    content_new = content_new.replace("Rs. )", "Rs.)")
    content_new = content_new.replace("Rs. /", "Rs./")
    content_new = content_new.replace("Rs. \n", "Rs.\n")

    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(content_new)

    print("✅ Replaced all occurrences of Rupee symbol with Rs. successfully!")

if __name__ == "__main__":
    replace_rupee()
