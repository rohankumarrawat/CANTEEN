import sqlite3

def migrate():
    conn = sqlite3.connect('/Users/rohan/Desktop/canteen/canteen.db')
    cursor = conn.cursor()

    package_items = [
        "PP Box (Dal) Mini Meal",
        "Foil Box (Rice, Sabji)",
        "Roti pouch",
        "Salad Pkt",
        "Spoon/Mini Meal",
        "Napkin Tissue Paper",
        "Salt Pouch",
        "Pickle & Paratha",
        "Tape",
        "Big Foil Box (Biryani)",
        "Paper Box (Lunch)",
        "Butter Roti Paper",
        "Paratha Box",
        "Partition Box",
        "Black Packet",
        "400 ML PP Box",
        "Silver foil",
        "Foil silver"
    ]

    for item in package_items:
        cursor.execute(
            "UPDATE inventory SET cat = 'Packaging Material' WHERE item = ? COLLATE NOCASE",
            (item,)
        )
        print(f"Updated category of '{item}' to 'Packaging Material'")

    conn.commit()
    conn.close()
    print("Database packaging category migration finished successfully!")

if __name__ == '__main__':
    migrate()
