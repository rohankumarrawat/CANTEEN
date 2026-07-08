# Debug map script
import sqlite3, os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../canteen.db'))

def get_inventory_items():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    items = conn.execute("SELECT id, item, cp, stock FROM inventory").fetchall()
    conn.close()
    return {r["item"].strip().lower(): dict(r) for r in items}

db_items = get_inventory_items()

# Data from July 8 sheets: (Sheet Name, BBF, Issue, Rate, BCF, Receipt)
sheet_rows_july8 = [
    # Image 3 (Dry top)
    ("ATTA", 1370.000, 50.000, 31.00, 1320.000, 0.0),
    ("RICE", 615.500, 35.000, 68.00, 580.500, 0.0),
    ("R/OI", 20.000, 11.500, 180.92, 8.500, 0.0), # Refined Oil (Expensive)
    ("R/OI", 240.000, 0.000, 175.00, 240.000, 0.0), # Refined Oil
    ("Sarso Dana", 0.440, 0.020, 120.00, 0.420, 0.0),
    ("KALI SARSO", 0.0, 0.0, 200.0, 0.0, 0.0),
    ("PANCH PHURAN", 0.0, 0.0, 400.0, 0.0, 0.0),
    ("RAJMA", 13.000, 13.000, 115.00, 0.000, 0.0), # Rajma
    ("RAJMA", 80.000, 4.000, 125.00, 76.000, 0.0), # Rajma (Expensive)
    ("URD (S)", 0.0, 0.0, 120.0, 0.0, 0.0),
    ("DAL CHANA", 52.000, 0.000, 80.00, 52.000, 0.0),
    ("BESAN", 0.0, 0.0, 94.50, 0.0, 0.0),
    ("BESAN", 50.000, 0.000, 90.00, 50.000, 0.0),
    ("DAL ARHAR", 50.000, 0.000, 120.00, 50.000, 0.0),
    ("DAL MASOOR (S)", 16.000, 0.000, 84.00, 16.000, 0.0),
    ("URD CRD(CHILKA)", 0.0, 0.0, 110.0, 0.0, 0.0),
    ("URD CRD(CHILKA)", 13.000, 0.000, 120.00, 13.000, 0.0),
    ("MASUR Crd(Malika)", 12.000, 0.000, 84.00, 12.000, 0.0),
    ("MOONG Crd(Chilka)", 12.000, 0.000, 115.00, 12.000, 0.0),
    ("URD DHULI", 10.000, 0.000, 135.00, 10.000, 0.0),
    ("LOBHIYA", 0.0, 0.0, 100.0, 0.0, 0.0),
    ("JEERA (S)", 3.450, 0.200, 300.00, 3.250, 0.0),
    ("HALDI PDR", 0.100, 0.100, 231.00, 0.000, 0.0), # Haldi Powder
    ("HALDI PDR", 8.000, 0.100, 290.00, 7.900, 0.0), # Haldi Powder(Expensive)
    ("MIRCHI PDR", 0.0, 0.0, 315.00, 0.0, 0.0),
    ("MIRCHI PDR", 5.900, 0.200, 300.00, 5.700, 0.0), # Mirchi Powder
    
    # Image 4 (Dry middle)
    ("DAL CHINI", 0.270, 0.200, 400.00, 0.070, 0.0),
    ("LAUNG", 0.0, 0.0, 1800.00, 0.0, 0.0),
    ("HING", 5.000, 1.000, 89.25, 4.000, 0.0), # Hing
    ("HING", 30.000, 0.000, 130.00, 30.000, 0.0), # Hing Expensive
    ("KITCHEN KING", 42.000, 0.200, 76.00, 41.800, 0.0),
    ("DEGI MIRCH", 40.000, 0.200, 106.00, 39.800, 0.0),
    ("KASTURI METHI", 0.0, 0.0, 700.00, 0.0, 0.0),
    ("KASTURI METHI", 0.800, 0.050, 200.00, 0.750, 0.0), # Kasuri methi (Expensive)
    ("GARAM MASALA", 41.000, 0.200, 95.00, 40.800, 0.0),
    ("SALT", 44.000, 2.000, 28.00, 42.000, 0.0),
    ("DANIYA (S)", 0.0, 0.0, 199.50, 0.0, 0.0),
    ("JEERA PDR", 24.900, 0.200, 70.00, 24.700, 0.0),
    ("B ELAICHI", 0.0, 0.0, 1995.00, 0.0, 0.0),
    ("METHI DANA", 0.0, 0.0, 105.00, 0.0, 0.0),
    ("METHI DANA", 0.380, 0.050, 120.00, 0.330, 0.0), # Methi Dana(Expensive)
    ("RAJMA MASALA", 0.0, 0.0, 85.00, 0.0, 0.0),
    ("TEJ PATTA", 0.0, 0.0, 168.00, 0.0, 0.0),
    ("TEJ PATTA", 0.380, 0.020, 200.00, 0.360, 0.0), # Tej Patta(Expensive)
    ("AJINO MOTO", 2.000, 0.000, 130.00, 2.000, 0.0),
    ("DESI GHEE", 24.500, 1.000, 475.00, 23.500, 0.0),
    ("SARSOO", 0.0, 0.0, 210.00, 0.0, 0.0),
    ("ENO", 1.000, 0.000, 55.04, 1.000, 0.0),
    ("AJWAIN", 1.150, 0.050, 400.00, 1.100, 0.0),
    ("MIRCHI (S)", 0.650, 0.050, 340.00, 0.600, 0.0),

    # Image 5 (Dry bottom)
    ("DHANIYA PDR", 2.100, 0.200, 190.00, 1.900, 0.0), # Dhaniya Powder(Expensive)
    ("DHANIYA PDR (Extra)", 8.000, 0.000, 180.00, 8.000, 0.0), # Unmatched
    ("KALI MIRCH(S)", 0.500, 0.000, 850.00, 0.500, 0.0),
    ("KALI MIRCH PDR", 3.000, 0.000, 120.00, 3.000, 0.0),
    ("MUMFALI DANA", 17.000, 0.000, 160.00, 17.000, 0.0),
    ("SAMBHAR MASALA", 0.0, 0.0, 74.00, 0.0, 0.0),
    ("LPG", 68.600, 26.900, 63.87, 41.700, 18.9), # LPG has a receipt of 18.9
    ("RAI", 0.0, 0.0, 315.00, 0.0, 0.0),
    ("EMLI", 0.650, 0.100, 120.00, 0.550, 0.0), # Imli (Expensive)
    ("BAKING PDR", 0.0, 0.0, 67.20, 0.0, 0.0),
    ("BAKING PDR", 4.000, 0.000, 20.00, 4.000, 0.0),
    ("SCHEZAN SAUSE", 2.000, 0.000, 85.00, 2.000, 0.0),
    ("SAHI PANEER MASALA", 16.000, 2.000, 88.00, 14.000, 0.0), # Shahi Paneer Masala (Kgs)
    ("SAHI PANEER MASALA", 0.0, 0.0, 90.00, 0.0, 0.0),
    ("SABJI MASALA", 11.900, 0.000, 70.00, 11.900, 0.0),
    ("SOYA BEAN BADIYA", 17.000, 0.000, 94.50, 17.000, 0.0),
    ("MAIDA", 2.800, 0.000, 40.00, 2.800, 0.0),
    ("SAYA SAUCE", 2.000, 0.000, 80.00, 2.000, 0.0),
    ("VINEGAR", 2.000, 0.000, 45.00, 2.000, 0.0),
    ("KALI MIRCH PDR (Extra)", 0.0, 0.0, 180.00, 0.0, 0.0), # Unmatched
    ("CORN FLOUR", 2.800, 0.000, 80.00, 2.800, 0.0),
    ("AACHAR", 7.000, 0.000, 147.00, 7.000, 0.0),
    ("CREAM", 0.0, 0.0, 250.00, 0.0, 0.0),
    ("CREAM", 4.000, 1.000, 220.00, 3.000, 1.0), # Cream has a receipt of 1.0
    ("PARATHA MASALA", 0.0, 0.0, 10.00, 0.0, 0.0),
    
    # Sweets
    ("SWEET (BURFI)", 21.000, 12.000, 280.00, 9.000, 12.0),
    ("PETHA", 10.000, 0.000, 150.00, 10.000, 0.0),
    ("BUNDI", 0.0, 0.0, 250.0, 0.0, 0.0),
    
    # Image 2 (Weekly Dry Items)
    ("PP BOX (DAL) MINI MEAL", 8762.0, 800.0, 3.186, 7962.0, 0.0),
    ("FOIL BOX (RICE,SABJI)", 7616.0, 400.0, 1.680, 7216.0, 0.0),
    ("ROTI POUCH", 21.100, 2.300, 236.000, 18.800, 0.0), # Unmatched
    ("SALAD PKT", 9155.0, 800.0, 0.177, 8355.0, 0.0),
    ("SPOON/MINI MEAL", 4272.0, 440.0, 0.504, 3832.0, 0.0),
    ("NEPKIN TUSSU PEPAR", 3191.0, 472.0, 0.354, 2719.0, 0.0),
    ("TISUE PEPPAR", 5628.0, 0.0, 0.528, 5628.0, 0.0), # Unmatched
    ("SALT POUCH", 7407.0, 400.0, 0.150, 7007.0, 0.0),
    ("PICKLE & PARATHA", 2722.0, 472.0, 0.896, 2250.0, 0.0),
    ("PICKLE", 5184.0, 0.0, 0.899, 5184.0, 0.0), # Unmatched
    
    # Image 1 (Dry weekly top)
    ("TAPE", 6.0, 1.0, 23.60, 5.0, 1.0),
    ("BIG FOIL BOX (BIRIYANI)", 143.0, 40.0, 3.360, 103.0, 0.0),
    ("PAPER BOX (LUNCH)", 3827.0, 400.0, 4.956, 3427.0, 400.0),
    ("BUTTER ROTI PAPER", 1.250, 0.150, 236.000, 1.100, 0.0), # Unmatched
    ("PARATHA BOX", 1505.0, 72.0, 3.360, 1433.0, 0.0),
    ("PARTATION BOX", 47.0, 0.0, 6.960, 47.0, 0.0),
    ("BLACK PACKET", 1.0, 0.0, 141.600, 1.0, 0.0),
    ("400 ML PP BOX", 170.0, 40.0, 4.720, 130.0, 0.0),
    ("SILVER FOIL", 5.200, 0.500, 708.000, 4.700, 0.0),
    ("FOIL SILVER", 0.0, 0.0, 531.000, 0.0, 0.0)
]

mapping = {
    # Image 1 & 3 & 4 & 5 (Dry)
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
    "masur crd(malika)": "masoor dal malka",
    "moong crd(chilka)": "moong dal chilka",
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
    "kali mirch(s)": "kali mirch (s)",
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
    "sweet (burfi)": "barfi",
    "petha": "petha",
    "bundi": "bundi",
    
    # Image 1 (Dry weekly top)
    "tape": "tape",
    "big foil box (biriyani)": "big foil box (biryani)",
    "paper box (lunch)": "paper box (lunch)",
    "paratha box": "paratha box",
    "partation box": "partition box",
    "black packet": "black packet",
    "400 ml pp box": "400ml pp box",
    "silver foil": "silver foil"
}

print("Running manual checks for unmatched items:")
for item, bbf, issue, rate, bcf, receipt in sheet_rows_july8:
    item_l = item.strip().lower()
    db_name = None
    
    if (item_l, rate) in mapping:
        db_name = mapping[(item_l, rate)]
    elif item_l in mapping:
        db_name = mapping[item_l]
        
    if db_name:
        if db_name in db_items:
            # Matched successfully!
            pass
        else:
            print(f"  Mapping defined but NOT found in DB: {item_l} -> {db_name}")
    else:
        print(f"  NO MAPPING DEFINED at all for: {item_l} (rate {rate})")
