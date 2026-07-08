# Final mapped script to map all 3 sheets to database items strictly
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

def get_inventory_items():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    items = conn.execute("SELECT id, item, cp, stock FROM inventory").fetchall()
    conn.close()
    return {r["item"].strip().lower(): dict(r) for r in items}

db_items = get_inventory_items()

# Define the extracted sheet rows for July 7, 2026
# Each item format: (Sheet Name, Rate/CP, BCF/Closing Stock)
sheet_rows_img1 = [
    ("ATTA", 31.00, 1370.00),
    ("RICE", 68.00, 615.50),
    ("R/OI", 180.92, 20.00), # Refined Oil (Expensive)
    ("R/OI", 175.00, 240.00), # Refined Oil
    ("Sarso Dana", 120.00, 0.44),
    ("KALI SARSO", 200.00, 0.00),
    ("PANCH PHURAN", 400.00, 0.00),
    ("RAJMA", 115.00, 13.00), # Rajma
    ("RAJMA", 125.00, 80.00), # Rajma (Expensive)
    ("URD (S)", 120.00, 0.00),
    ("DAL CHANA", 80.00, 52.00),
    ("BESAN", 94.50, 0.00), # Besan Expensive
    ("BESAN", 90.00, 50.00), # Besan
    ("DAL ARHAR", 120.00, 50.00),
    ("DAL MASOOR (S)", 84.00, 16.00),
    ("URD CRD(CHILKA)", 110.00, 0.00), # Urad Dal Chilka
    ("URD CRD(CHILKA)", 120.00, 13.00), # URD CRD CHILKAT (Expensive)
    ("MASUR Crd(Malka)", 84.00, 12.00), # Masoor Dal Malka
    ("MOONG Crd(Malka)", 115.00, 12.00), # Moong Dal Chilka
    ("URD DHULI", 135.00, 10.00),
    ("LOBHIYA", 100.00, 0.00),
    ("JEERA (S)", 300.00, 3.45),
    ("HALDI PDR", 231.00, 0.10), # Haldi Powder
    ("HALDI PDR", 290.00, 8.00), # Haldi Powder(Expensive)
    ("MIRCHI PDR", 315.00, 0.00), # Mirchi Powder(Expensive)
    ("MIRCHI PDR", 300.00, 5.90), # Mirchi Powder
    ("DAL CHINI", 400.00, 0.27),
    ("LAUNG", 1800.00, 0.00),
    ("HING", 89.25, 5.00), # Hing
    ("HING", 130.00, 30.00), # Hing Expensive
    ("KITCHEN KING", 76.00, 42.00), # Kitchen King
    ("DEGI MIRCH", 106.00, 40.00), # Deggi Mirch
    ("KASTURI METHI", 700.00, 0.00), # Kasuri Methi
    ("KASTURI METHI", 200.00, 0.80), # Kasuri methi (Expensive)
    ("GARAM MASALA", 95.00, 41.00),
    ("SALT", 28.00, 44.00),
    ("DANIYA (S)", 199.50, 0.00), # Dhaniya (S)
    ("JEERA PDR", 70.00, 24.90),
    ("B ELAICHI", 1995.00, 0.00), # Badi Elaichi
    ("METHI DANA", 105.00, 0.00), # Methi Dana
    ("METHI DANA", 120.00, 0.38), # Methi Dana(Expensive)
    ("RAJMA MASALA", 85.00, 0.00),
    ("TEJ PATTA", 168.00, 0.00), # Tej Patta
    ("TEJ PATTA", 200.00, 0.38), # Tej Patta(Expensive)
    ("AJINO MOTO", 130.00, 2.00), # Ajinomoto
    ("DESI GHEE", 475.00, 24.50),
    ("SARSOO", 210.00, 0.00), # Sarson
    ("ENO", 55.04, 1.00),
    ("AJWAIN", 400.00, 1.15),
    ("MIRCHI (S)", 340.00, 0.65), # Mirchi (S)
    ("KADHAI PANEER MASALA", 50.00, 0.00), # Kadhai Paneer Masala
    ("CHAT MASALA", 76.00, 15.00), # Chaat Masala
    ("RAJMAH MASALA", 736.25, 1.00), # Rajmah Masala
    ("RAJMAH MASALA", 74.00, 16.00), # Rajmah Masala(Expensive)
    ("GULAB JAL", 66.15, 9.00),
    ("CHANA MASALA", 751.88, 0.40), # Chana Masala
    ("CHANA MASALA", 80.00, 8.00), # Chana Masala(Expensive)
    ("KALA CHANA", 78.00, 37.00), # Kala Chana
    ("KALA CHANA", 80.00, 80.00), # Kala Chana(Expensive)
    ("RICE (idlee)", 40.00, 21.00), # Rice(Idlee)
    ("Red CHILLI SAUCE", 80.00, 3.00), # Red Chilli Sauce
    ("GREEN CHILIS SAUCE", 80.00, 0.00), # Green Chilli Sause
    ("TOMATO KATCH UP", 170.00, 0.00), # Tomato Sauce
    ("MATAR PANEER MASALA", 35.00, 0.00),
    ("PAV BHAJI MASALA", 78.00, 7.00),
    ("MATAR TF", 60.00, 15.00), # Matar (Frozen)
    ("FOOD COLOUR", 68.44, 0.00), # Food Colour
    ("FOOD COLOUR", 40.00, 4.00), # Food Colour(Expensive)
    ("KEVADA WATER", 70.80, 10.00), # Kevada Water
    ("BIRIYANI MASALA", 73.50, 13.70), # Biryani Masala
    ("Ilaychi small Gr", 4000.00, 0.08), # Elaichi Small Gr
    ("DHANIYA PDR", 199.50, 0.00), # Dhaniya Powder
    ("DHANIYA PDR", 190.00, 2.10), # Dhaniya Powder(Expensive)
    ("DHANIYA PDR (Extra)", 180.00, 8.00), # Unmatched
    ("KALI MIRCH( S)", 850.00, 0.50), # Kali Mirch (S)
    ("KALI MIRCH PDR", 120.00, 3.00), # Kali Mirch Powder
    ("MUMFALI DANA", 160.00, 17.00), # Moongphali Dana
    ("SAMBHAR MASALA", 74.00, 0.00),
    ("LPG", 63.87, 68.60),
    ("RAI", 315.00, 0.00),
    ("EMLI", 120.00, 0.65), # Imli (Expensive)
    ("BAKING PDR", 67.20, 0.00), # Baking Powder
    ("BAKING PDR", 20.00, 4.00), # Baking Powder(Expensive)
    ("SCHEZAN SAUSE", 85.00, 2.00), # Schezwan Sauce
    ("SAHI PANEER MASALA", 88.00, 16.00), # Shahi Paneer Masala (Kgs)
    ("SAHI PANEER MASALA", 90.00, 0.00), # Shahi Paneer Masala (Pkt)
    ("SABJI MASALA", 70.00, 11.90), # Sabzi Masala
    ("SOYA BEAN BADIYA", 94.50, 17.00),
    ("MAIDA", 40.00, 2.80),
    ("SAYA SAUCE", 80.00, 2.00), # Soya Sauce
    ("VINEGAR", 45.00, 2.00),
    ("KALI MIRCH PDR (Extra)", 180.00, 0.00), # Unmatched
    ("CORN FLOUR", 80.00, 2.80),
    ("AACHAR", 147.00, 7.00), # Achar
    ("CREAM", 250.00, 0.00), # Unmatched
    ("CREAM", 220.00, 4.00), # Cream
    ("PARATHA MASALA", 10.00, 0.00)
]

sheet_rows_img2 = [
    ("PP BOX (DAL) MINI MEAL", 3.186, 8762.0),
    ("FOIL BOX (RICE,SABJI)", 1.680, 7616.0),
    ("ROTI POUCH", 236.000, 21.1), # Unmatched
    ("SALAD PKT", 0.177, 9155.0),
    ("SPOON/MINI MEAL", 0.504, 4272.0),
    ("NEPKIN TUSSU PEPAR", 0.354, 3191.0),
    ("TISUE PEPPAR", 0.528, 5628.0), # Unmatched
    ("SALT POUCH", 0.150, 7407.0),
    ("PICKLE & PARATHA", 0.896, 2722.0),
    ("PICKLE", 0.899, 5184.0), # Unmatched
    ("TAPE", 23.600, 6.0),
    ("BIG FOIL BOX (BIRIYANI)", 3.360, 143.0),
    ("PAPER BOX (LUNCH)", 4.956, 3827.0),
    ("BUTTER ROTI PAPER", 236.000, 1.25), # Unmatched
    ("PARATHA BOX", 3.360, 1505.0),
    ("PARTATION BOX", 6.960, 47.0),
    ("BLACK PACKET", 141.600, 1.0),
    ("400 ML PP BOX", 4.720, 170.0),
    ("SILVER FOIL", 708.000, 5.20),
    ("FOIL SILVER", 531.000, 0.0), # Unmatched
    ("SWEET (BURFI)", 280.00, 21.0),
    ("PETHA", 150.00, 10.0),
    ("BUNDI", 250.00, 0.0)
]

sheet_rows_img3 = [
    ("POTATO", 13.00, 355.00),
    ("ONION", 24.00, 73.50),
    ("ONION", 26.00, 54.00), # Unmatched
    ("TOMATO", 48.00, 6.49),
    ("TOMATO 'R'", 45.00, 28.00), # Unmatched
    ("GINGER", 187.00, 4.965),
    ("GINGER", 250.00, 0.00), # Unmatched
    ("GARLIC", 176.00, 6.59),
    ("GARLIC", 150.00, 0.00), # Unmatched
    ("PUMPKIN", 15.00, 30.00),
    ("GREEN CHILLI", 65.00, 0.00),
    ("CHILLIES GREEN", 65.00, 6.00), # Unmatched
    ("CORRENDER", 35.00, 0.00),
    ("CORRENDER", 132.00, 2.235),
    ("CAPSICUM", 88.00, 17.715),
    ("BEANS", 120.00, 0.00),
    ("CARROT", 80.00, 0.00),
    ("CAULI FLOWER", 120.00, 0.00),
    ("GREEN ONION", 35.00, 0.00),
    ("BOTTLE GD", 18.00, 0.00),
    ("CABBAGE", 20.00, 0.00),
    ("CABBAGE", 60.00, 0.00), # Unmatched
    ("CUCUMBER", 33.00, 0.00),
    ("CUCUMBER", 22.00, 12.00), # Cucumber (Expensive)
    ("BEANS", 83.00, 0.285), # Unmatched
    ("BRINJAL", 37.00, 0.785), # Unmatched
    ("DRUM STICK", 99.00, 0.00), # Unmatched
    ("PANEER", 250.00, 0.00),
    ("LIME S", 80.00, 0.00),
    ("MILK FRESH", 62.00, 0.00), # Unmatched
    ("DAHI", 80.00, 0.00),
    ("KULCHA", 30.00, 0.00),
    ("TORI", 25.00, 0.00),
    ("PAV", 35.00, 0.00)
]

mapping = {
    # Image 1 (Dry)
    "atta": "atta",
    "rice": "rice",
    ("r/oi", 180.92): "refined oil (expensive)",
    ("r/oi", 175.00): "refined oil",
    "sarso dana": "sarson dana",
    "kali sarso": "kali sarson",
    "panch phuran": "panch phuran",
    ("rajma", 115.00): "rajma",
    ("rajma", 125.00): "rajma (expensive)",
    "urd (s)": "urad (s)",
    "dal chana": "dal chana",
    ("besan", 94.50): "besan expensive",
    ("besan", 90.00): "besan",
    "dal arhar": "dal arhar",
    "dal masoor (s)": "dal masoor (s)",
    ("urd crd(chilka)", 110.00): "urad dal chilka",
    ("urd crd(chilka)", 120.00): "urd crd chilkat (expensive)",
    "masur crd(malka)": "masoor dal malka",
    "moong crd(malka)": "moong dal chilka",
    "urd dhuli": "urad dhuli",
    "lobhiya": "lobia",
    "jeera (s)": "jeera (s)",
    ("haldi pdr", 231.00): "haldi powder",
    ("haldi pdr", 290.00): "haldi powder(expensive)",
    ("mirchi pdr", 315.00): "mirchi powder(expensive)",
    ("mirchi pdr", 300.00): "mirchi powder",
    "dal chini": "dalchini",
    "laung": "laung",
    ("hing", 89.25): "hing",
    ("hing", 130.00): "hing expensive",
    "kitchen king": "kitchen king",
    "degi mirch": "deggi mirch",
    ("kasturi methi", 700.00): "kasuri methi",
    ("kasturi methi", 200.00): "kasuri methi (expensive)",
    "garam masala": "garam masala",
    "salt": "salt",
    "daniya (s)": "dhaniya (s)",
    "jeera pdr": "jeera powder",
    "b elaichi": "badi elaichi",
    ("methi dana", 105.00): "methi dana",
    ("methi dana", 120.00): "methi dana(expensive)",
    "rajma masala": "rajma masala",
    ("tej patta", 168.00): "tej patta",
    ("tej patta", 200.00): "tej patta(expensive)",
    "ajino moto": "ajinomoto",
    "desi ghee": "desi ghee",
    "sarsoo": "sarson",
    "eno": "eno",
    "ajwain": "ajwain",
    "mirchi (s)": "mirchi (s)",
    "kadhai paneer masala": "kadhai paneer masala",
    "chat masala": "chaat masala",
    ("rajmah masala", 736.25): "rajmah masala",
    ("rajmah masala", 74.00): "rajmah masala(expensive)",
    "gulab jal": "gulab jal",
    ("chana masala", 751.88): "chana masala",
    ("chana masala", 80.00): "chana masala(expensive)",
    ("kala chana", 78.00): "kala chana",
    ("kala chana", 80.00): "kala chana(expensive)",
    "rice (idlee)": "rice(idlee)",
    "red chilli sauce": "red chilli sauce",
    "green chilis sauce": "green chilli sause",
    "tomato katch up": "tomato sauce",
    "matar paneer masala": "matar paneer masala",
    "pav bhaji masala": "pav bhaji masala",
    "matar tf": "matar (frozen)",
    ("food colour", 68.44): "food colour",
    ("food colour", 40.00): "food colour(expensive)",
    "kevada water": "kevada water",
    "biriyani masala": "biryani masala",
    "ilaychi small gr": "elaichi small gr",
    ("dhaniya pdr", 199.50): "dhaniya powder",
    ("dhaniya pdr", 190.00): "dhaniya powder(expensive)",
    "kali mirch( s)": "kali mirch (s)",
    ("kali mirch pdr", 120.00): "kali mirch powder",
    "mumfali dana": "moongphali dana",
    "sambhar masala": "sambhar masala",
    "lpg": "lpg",
    "rai": "rai",
    "emli": "imli (expensive)",
    ("baking pdr", 67.20): "baking powder",
    ("baking pdr", 20.00): "baking powder(expensive)",
    "schezan sause": "schezwan sauce",
    ("sahi paneer masala", 88.00): "shahi paneer masala (kgs)",
    ("sahi paneer masala", 90.00): "shahi paneer masala (pkt)",
    "sabji masala": "sabzi masala",
    "soya bean badiya": "soya bean badiya",
    "maida": "maida",
    "saya sauce": "soya sauce",
    "vinegar": "vinegar",
    "corn flour": "corn flour",
    "aachar": "achar",
    ("cream", 220.00): "cream",
    "paratha masala": "paratha masala",

    # Image 2 (Dry/Packing/Sweet)
    "pp box (dal) mini meal": "pp box (dal) mini meal",
    "foil box (rice,sabji)": "foil box (rice, sabji)",
    "salad pkt": "salad pkt",
    "spoon/mini meal": "spoon / mini meal",
    "nepkin tussu pepar": "napkin tissue paper",
    "salt pouch": "salt pouch",
    "pickle & paratha": "pickle & paratha",
    "tape": "tape",
    "big foil box (biriyani)": "big foil box (biryani)",
    "paper box (lunch)": "paper box (lunch)",
    "paratha box": "paratha box",
    "partation box": "partition box",
    "black packet": "black packet",
    "400 ml pp box": "400ml pp box",
    "silver foil": "silver foil",
    "sweet (burfi)": "barfi",
    "petha": "petha",
    "bundi": "bundi",

    # Image 3 (Fresh)
    "potato": "potato",
    ("onion", 24.00): "onion",
    "tomato": "tomato",
    ("ginger", 187.00): "ginger",
    ("garlic", 176.00): "garlic",
    "pumpkin": "pumpkin",
    "green chilli": "green chilli",
    ("corrender", 35.00): "coriander",
    ("corrender", 132.00): "coriander(expensive)",
    "capsicum": "capsicum",
    ("beans", 120.00): "beans",
    "carrot": "carrot",
    "cauli flower": "cauliflower",
    "green onion": "green onion",
    "bottle gd": "bottle gourd",
    ("cabbage", 20.00): "cabbage",
    ("cucumber", 33.00): "cucumber",
    ("cucumber", 22.00): "cucumber(expensive)",
    "paneer": "paneer",
    "lime s": "lemon",
    "dahi": "dahi",
    "kulcha": "kulcha",
    "tori": "tori",
    "pav": "pav"
}

unmatched = []
matched_updates = []

all_sheet_rows = sheet_rows_img1 + sheet_rows_img2 + sheet_rows_img3

for item, rate, bcf in all_sheet_rows:
    item_l = item.strip().lower()
    db_name = None
    
    # Check compound keys first (name, rate)
    if (item_l, rate) in mapping:
        db_name = mapping[(item_l, rate)]
    elif item_l in mapping:
        db_name = mapping[item_l]
        
    if db_name and db_name in db_items:
        db_item = db_items[db_name]
        matched_updates.append({
            "sheet_name": item,
            "db_name": db_item["item"],
            "prev_stock": db_item["stock"],
            "new_stock": bcf,
            "prev_cp": db_item["cp"],
            "new_cp": rate,
            "id": db_item["id"]
        })
    else:
        unmatched.append({"sheet_name": item, "rate": rate, "bcf": bcf})

print(f"Total matched: {len(matched_updates)}")
print(f"Total unmatched: {len(unmatched)}")

print("\n--- UNMATCHED ---")
for u in unmatched:
    print(f"  Item: {u['sheet_name']} (Rate: {u['rate']}, Stock: {u['bcf']})")
