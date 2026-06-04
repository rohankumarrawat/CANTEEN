"""
Canteen Inventory & Sales Management System
PDF Presentation Generator
Indian Army | 56 APO Field Canteen
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import Flowable
from reportlab.pdfgen import canvas
import os

# ── Colour Palette ──────────────────────────────────────────────────────────
ARMY_OLIVE   = colors.HexColor("#4B5320")   # deep olive green
ARMY_GOLD    = colors.HexColor("#C8960C")   # Indian Army gold
ARMY_DARK    = colors.HexColor("#1C1C1C")   # near-black
ARMY_LIGHT   = colors.HexColor("#F5F0E8")   # warm off-white
ARMY_MED     = colors.HexColor("#6B7040")   # medium olive
ACCENT_RED   = colors.HexColor("#8B1A1A")   # deep red accent
ACCENT_BLUE  = colors.HexColor("#1A3A5C")   # navy accent
SLATE        = colors.HexColor("#E8E4DA")   # card background
WHITE        = colors.white
TABLE_HEADER = colors.HexColor("#2E3615")   # darkened olive for table headers
TABLE_ALT    = colors.HexColor("#EDE9DE")   # alternating row tint

W, H = A4

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Canteen_System_Presentation.pdf")

# ── Slide-background canvas override ────────────────────────────────────────
class SlidePage:
    """Adds a full-bleed gradient-style background to each page."""
    def __init__(self, doc):
        self.doc = doc

    def __call__(self, canv, doc):
        canv.saveState()
        # Full background
        canv.setFillColor(ARMY_LIGHT)
        canv.rect(0, 0, W, H, fill=1, stroke=0)

        # Left sidebar strip
        canv.setFillColor(ARMY_OLIVE)
        canv.rect(0, 0, 1.1*cm, H, fill=1, stroke=0)

        # Top banner
        canv.setFillColor(ARMY_OLIVE)
        canv.rect(0, H - 2.0*cm, W, 2.0*cm, fill=1, stroke=0)

        # Gold accent line under top banner
        canv.setFillColor(ARMY_GOLD)
        canv.rect(0, H - 2.15*cm, W, 0.15*cm, fill=1, stroke=0)

        # Bottom bar
        canv.setFillColor(ARMY_OLIVE)
        canv.rect(0, 0, W, 0.85*cm, fill=1, stroke=0)

        # Footer text
        canv.setFillColor(ARMY_GOLD)
        canv.setFont("Helvetica", 7)
        footer = "INDIAN ARMY  |  56 APO FIELD CANTEEN  |  CONFIDENTIAL"
        canv.drawCentredString(W / 2, 0.28*cm, footer)

        # Page number (skip cover)
        if doc.page > 1:
            canv.setFillColor(WHITE)
            canv.setFont("Helvetica", 7)
            canv.drawRightString(W - 1.2*cm, 0.28*cm, f"Slide {doc.page}")

        # Top-banner label
        canv.setFillColor(ARMY_GOLD)
        canv.setFont("Helvetica-Bold", 9)
        canv.drawString(1.6*cm, H - 1.35*cm, "CANTEEN INVENTORY & SALES MANAGEMENT SYSTEM")
        canv.setFillColor(WHITE)
        canv.setFont("Helvetica", 8)
        canv.drawRightString(W - 0.8*cm, H - 1.35*cm, "56 APO Field Canteen · Indian Army")

        canv.restoreState()


# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

SLIDE_TITLE = S("SlideTitle",
    fontName="Helvetica-Bold", fontSize=26, textColor=ARMY_OLIVE,
    alignment=TA_CENTER, spaceAfter=4)

SLIDE_SUBTITLE = S("SlideSubtitle",
    fontName="Helvetica", fontSize=13, textColor=ARMY_MED,
    alignment=TA_CENTER, spaceAfter=8)

SECTION_TITLE = S("SectionTitle",
    fontName="Helvetica-Bold", fontSize=17, textColor=ARMY_OLIVE,
    alignment=TA_LEFT, spaceBefore=6, spaceAfter=6)

BODY = S("Body",
    fontName="Helvetica", fontSize=10, textColor=ARMY_DARK,
    leading=16, spaceAfter=4)

BODY_BOLD = S("BodyBold",
    fontName="Helvetica-Bold", fontSize=10, textColor=ARMY_DARK,
    leading=16, spaceAfter=4)

BULLET = S("Bullet",
    fontName="Helvetica", fontSize=10, textColor=ARMY_DARK,
    leading=16, leftIndent=18, spaceAfter=3,
    bulletText="•")

SUBBULLET = S("SubBullet",
    fontName="Helvetica", fontSize=9, textColor=ARMY_MED,
    leading=14, leftIndent=36, spaceAfter=2,
    bulletText="–")

CAPTION = S("Caption",
    fontName="Helvetica-Oblique", fontSize=8, textColor=ARMY_MED,
    alignment=TA_CENTER)

COVER_TITLE = S("CoverTitle",
    fontName="Helvetica-Bold", fontSize=34, textColor=ARMY_OLIVE,
    alignment=TA_CENTER, leading=40)

COVER_SUB = S("CoverSub",
    fontName="Helvetica-Bold", fontSize=16, textColor=ARMY_GOLD,
    alignment=TA_CENTER, spaceAfter=6)

COVER_BODY = S("CoverBody",
    fontName="Helvetica", fontSize=11, textColor=ARMY_MED,
    alignment=TA_CENTER, spaceAfter=6)

TH_STYLE = S("TableHead",
    fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
    alignment=TA_CENTER)

TD_STYLE_C = S("TableDataC",
    fontName="Helvetica", fontSize=9, textColor=ARMY_DARK,
    alignment=TA_CENTER)

TD_STYLE_L = S("TableDataL",
    fontName="Helvetica", fontSize=9, textColor=ARMY_DARK,
    alignment=TA_LEFT)

LABEL_TAG = S("LabelTag",
    fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
    alignment=TA_CENTER)

# ── Helper Flowables ─────────────────────────────────────────────────────────
def gold_rule():
    return HRFlowable(width="100%", thickness=2, color=ARMY_GOLD, spaceAfter=10, spaceBefore=4)

def olive_rule():
    return HRFlowable(width="100%", thickness=0.5, color=ARMY_MED, spaceAfter=8)

def vspace(n=0.3):
    return Spacer(1, n*cm)

def slide_title(text):
    return [Paragraph(text, SECTION_TITLE), gold_rule()]

def bullet(text):
    return Paragraph(text, BULLET)

def subbullet(text):
    return Paragraph(text, SUBBULLET)

def body(text):
    return Paragraph(text, BODY)

def bold(text):
    return Paragraph(text, BODY_BOLD)

# ── Tag badge ────────────────────────────────────────────────────────────────
def tag_table(labels, colors_list):
    """Render coloured pill-style badge row."""
    cells = [Paragraph(lbl, LABEL_TAG) for lbl in labels]
    col_w = (W - 4.5*cm) / len(labels)
    t = Table([cells], colWidths=[col_w]*len(labels))
    style_cmds = [
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ("ROUNDEDCORNERS", [4]),
    ]
    for i, c in enumerate(colors_list):
        style_cmds.append(("BACKGROUND", (i,0), (i,0), c))
    t.setStyle(TableStyle(style_cmds))
    return t


def styled_table(headers, rows, col_widths=None, alt_rows=True):
    header_row = [Paragraph(h, TH_STYLE) for h in headers]
    data = [header_row]
    for rw in rows:
        data.append([Paragraph(str(c), TD_STYLE_C) for c in rw])

    if col_widths is None:
        avail = W - 4.5*cm
        col_widths = [avail / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND",    (0,0), (-1,0),  TABLE_HEADER),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, TABLE_ALT] if alt_rows else [WHITE]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCBB")),
        ("LINEABOVE",     (0,0), (-1,0),  1.5, ARMY_GOLD),
        ("LINEBELOW",     (0,-1),(-1,-1), 1.5, ARMY_GOLD),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def info_card(label, value, label_color=ARMY_OLIVE):
    """Two-cell card for key metric display."""
    t = Table([[Paragraph(label, S("cl", fontName="Helvetica-Bold", fontSize=8,
                                   textColor=WHITE, alignment=TA_CENTER)),
                Paragraph(value, S("cv", fontName="Helvetica-Bold", fontSize=12,
                                   textColor=label_color, alignment=TA_CENTER))]],
              colWidths=[3.5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), label_color),
        ("BACKGROUND",    (1,0), (1,0), WHITE),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 1, ARMY_OLIVE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t


# ── Build Slides ─────────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2.8*cm, rightMargin=1.8*cm,
        topMargin=3.0*cm,  bottomMargin=1.8*cm,
        title="Canteen Inventory & Sales System – Presentation",
        author="56 APO Field Canteen · Indian Army",
    )

    story = []
    bg = SlidePage(doc)

    # ── SLIDE 1 · COVER ──────────────────────────────────────────────────────
    story += [
        vspace(2.2),
        Paragraph("☆  INDIAN ARMY  ☆", COVER_SUB),
        vspace(0.3),
        Paragraph("Canteen Inventory &amp;<br/>Sales Management System", COVER_TITLE),
        vspace(0.5),
        gold_rule(),
        vspace(0.2),
        Paragraph("56 APO Field Canteen", COVER_SUB),
        vspace(0.1),
        Paragraph(
            "A digital solution replacing paper ledgers with automated, role-based "
            "inventory tracking, daily sales reporting, and one-click official sign-off.",
            COVER_BODY),
        vspace(0.6),
        Paragraph("Version 1.0  ·  April 2026", CAPTION),
        vspace(0.3),
        Paragraph("Platform: Python · CustomTkinter · SQLite", CAPTION),
        PageBreak(),
    ]

    # ── SLIDE 2 · TABLE OF CONTENTS ──────────────────────────────────────────
    story += slide_title("📋  Table of Contents")
    toc_rows = [
        ("1", "Problem Statement & Objectives"),
        ("2", "System Overview"),
        ("3", "User Roles & Access Control"),
        ("4", "Core Features"),
        ("5", "Auto Stock Deduction — Recipe Engine"),
        ("6", "Daily Ledger & Inventory Tracking"),
        ("7", "Sales, Revenue & Profit Tracking"),
        ("8", "Smart Alerts & Reports"),
        ("9", "Non-Functional Requirements"),
        ("10", "Data Model Summary"),
        ("11", "Sample Daily Report"),
        ("12", "Summary & Next Steps"),
    ]
    toc_data = [[Paragraph(f"<b>{n}</b>", TD_STYLE_C), Paragraph(t, TD_STYLE_L)] for n,t in toc_rows]
    toc_t = Table(toc_data, colWidths=[1.2*cm, 13.5*cm])
    toc_t.setStyle(TableStyle([
        ("FONTSIZE",      (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW",     (0,0), (-1,-1), 0.3, colors.HexColor("#CCCCBB")),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, TABLE_ALT]),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [toc_t, PageBreak()]

    # ── SLIDE 3 · PROBLEM STATEMENT ──────────────────────────────────────────
    story += slide_title("01  Problem Statement & Objectives")
    story += [
        bold("Current Challenges"),
        bullet("Manual paper ledgers are error-prone and time-consuming for canteen staff"),
        bullet("No automated deduction of raw materials when meals are prepared"),
        bullet("Revenue, COGS, and profit tracked manually — prone to discrepancies"),
        bullet("Stock alerts, shopping lists, and reports prepared by hand daily"),
        bullet("Official sign-off documents require manual compilation each day"),
        vspace(0.3),
        bold("Project Objectives"),
        bullet("Replace paper ledgers with a desktop-based digital system"),
        bullet("Automate inventory deduction via a recipe engine"),
        bullet("Provide real-time sales, revenue, and profit visibility"),
        bullet("Generate print-ready, signed daily reports with one click"),
        bullet("Enforce role-based access so officers cannot alter operational data"),
        PageBreak(),
    ]

    # ── SLIDE 4 · SYSTEM OVERVIEW ────────────────────────────────────────────
    story += slide_title("02  System Overview")
    story += [
        body(
            "A <b>lightweight, offline desktop application</b> built in Python with a "
            "CustomTkinter GUI and SQLite database. Designed specifically for canteen "
            "operations in a low-connectivity military field environment."
        ),
        vspace(0.4),
        bold("Technology Stack"),
    ]
    tech_rows = [
        ("Layer",         "Technology",          "Purpose"),
        ("Frontend (UI)", "Python + CustomTkinter", "Responsive desktop GUI — big buttons, clear fonts"),
        ("Backend Logic", "Python 3.12",          "Business logic, recipe engine, report generation"),
        ("Database",      "SQLite",               "Embedded, zero-config, file-based storage"),
        ("Reports",       "ReportLab (PDF)",      "A4 print-ready daily reports with signatures"),
        ("Deployment",    "PyInstaller (.exe)",   "Standalone Windows executable — no Python needed"),
    ]
    story += [
        styled_table(tech_rows[0], tech_rows[1:],
                     col_widths=[4.0*cm, 5.5*cm, 5.5*cm]),
        vspace(0.4),
        bold("Deployment"),
        bullet("Packaged as a single <b>.exe</b> (Windows) via PyInstaller"),
        bullet("Runs entirely offline — no internet connection required"),
        bullet("Data stored in <code>canteen.db</code> alongside the executable"),
        bullet("Daily automated backup to the <code>backups/</code> folder"),
        PageBreak(),
    ]

    # ── SLIDE 5 · USER ROLES ─────────────────────────────────────────────────
    story += slide_title("03  User Roles & Access Control")
    story += [
        body("Three clearly separated roles enforce a least-privilege security model:"),
        vspace(0.3),
    ]

    role_rows = [
        ("Role",          "Default Login",          "Access Level",  "Key Responsibilities"),
        ("Admin",         "admin / admin123",        "Full (CRUD)",   "Master data, user mgmt, DB backup/restore, audit"),
        ("Manager",       "manager / manager123",    "Operational",   "Sales entry, batch prep, stock mgmt, reports"),
        ("Officer",       "officer / officer123",    "Read-Only",     "View dashboard, stock levels, daily reports"),
    ]
    story += [
        styled_table(role_rows[0], role_rows[1:],
                     col_widths=[2.5*cm, 4.0*cm, 3.0*cm, 5.5*cm]),
        vspace(0.4),
        bold("Permissions Highlights"),
        bullet("<b>Admin only:</b> Master Data (items, menus, recipes, users), Manual Audit Adjustments, DB Backup/Restore"),
        bullet("<b>Manager:</b> Full operational access — sales, batch prep, stock add/receive, expenditure, reports"),
        bullet("<b>Officer:</b> View-only — all write controls are <i>hidden</i> from navigation (not just disabled)"),
        vspace(0.3),
        bold("Security Policy"),
        bullet("Password-protected login with SHA-256 hashed credentials"),
        bullet("Operators cannot edit historical data without Admin approval"),
        bullet("Navigation items for inaccessible features are fully hidden per role"),
        PageBreak(),
    ]

    # ── SLIDE 6 · CORE FEATURES ──────────────────────────────────────────────
    story += slide_title("04  Core Features at a Glance")
    feat_rows = [
        ("Module",                    "What It Does"),
        ("Master Data Management",    "Item master, menu/product master, pricing setup"),
        ("Auto-Stock Deduction",      "Recipe-based batch prep entry auto-reduces inventory"),
        ("Daily Digital Ledger",      "Opening → Received → Issued → Closing stock tracking"),
        ("Sales & Profit Tracker",    "Revenue, COGS, net daily profit in real time"),
        ("Smart Inventory Alerts",    "Colour-coded low-stock warnings + shopping list generator"),
        ("One-Click Daily Reports",   "A4 PDF with signature blocks, historical calendar access"),
        ("Wastage Logging",           "Records unsold / spoiled food for accurate P&L"),
        ("Payment Mode Tracking",     "Tags revenue as Cash / UPI / Card"),
        ("User Management",           "Admin creates & manages user accounts and roles"),
        ("DB Backup & Restore",       "One-click backup + restore from any previous archive"),
    ]
    story += [
        styled_table(feat_rows[0], feat_rows[1:],
                     col_widths=[6.0*cm, 9.0*cm]),
        PageBreak(),
    ]

    # ── SLIDE 7 · RECIPE ENGINE ──────────────────────────────────────────────
    story += slide_title("05  Auto Stock Deduction — Recipe Engine")
    story += [
        body(
            "The <b>Recipe Engine</b> is the heart of the system. It eliminates manual "
            "calculation of raw material usage when meals are prepared."
        ),
        vspace(0.35),
        bold("How It Works"),
        bullet("Admin defines a <b>Recipe</b> per menu item — exact ingredient quantities for 1 unit"),
        bullet("Manager enters <b>Batch Preparation Count</b> (e.g., 150 Lunches prepared today)"),
        bullet("System calculates: <i>Total Usage = Qty per Unit × Batch Count</i>"),
        bullet("Inventory is automatically debited — no manual calculation needed"),
        bullet("Wastage can be logged separately to maintain accurate stock records"),
        vspace(0.35),
        bold("Example — Standard Lunch (1 Unit)"),
    ]
    recipe_rows = [
        ("Ingredient",  "Unit",  "Qty / Meal",  "Usage (150 Meals)"),
        ("Rice",        "kg",    "0.100",        "15.0 kg"),
        ("Dal",         "kg",    "0.050",        "7.5 kg"),
        ("Vegetables",  "kg",    "0.080",        "12.0 kg"),
        ("Cooking Oil", "ltr",   "0.020",        "3.0 ltr"),
        ("Box/Pack",    "pcs",   "1",            "150 pcs"),
    ]
    story += [
        styled_table(recipe_rows[0], recipe_rows[1:],
                     col_widths=[4.5*cm, 2.0*cm, 3.0*cm, 4.5*cm]),
        vspace(0.3),
        body(
            "<b>Result:</b> After entering 150 lunches, the system debits the above quantities "
            "from inventory automatically, and recalculates COGS in real time."
        ),
        PageBreak(),
    ]

    # ── SLIDE 8 · DAILY LEDGER ───────────────────────────────────────────────
    story += slide_title("06  Daily Ledger & Inventory Tracking")
    story += [
        body("Every stock movement is tracked in a structured digital ledger with automated balance calculation."),
        vspace(0.3),
        bold("The Ledger Formula"),
    ]

    formula_data = [[
        Paragraph("Opening Stock", S("F1", fontName="Helvetica-Bold", fontSize=11,
                                     textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("+", S("F2", fontName="Helvetica-Bold", fontSize=16,
                          textColor=ARMY_GOLD, alignment=TA_CENTER)),
        Paragraph("Received Stock", S("F3", fontName="Helvetica-Bold", fontSize=11,
                                      textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("−", S("F4", fontName="Helvetica-Bold", fontSize=16,
                          textColor=ACCENT_RED, alignment=TA_CENTER)),
        Paragraph("Issued (Cooked)", S("F5", fontName="Helvetica-Bold", fontSize=11,
                                       textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("=", S("F6", fontName="Helvetica-Bold", fontSize=16,
                          textColor=ARMY_GOLD, alignment=TA_CENTER)),
        Paragraph("Closing Stock", S("F7", fontName="Helvetica-Bold", fontSize=11,
                                     textColor=WHITE, alignment=TA_CENTER)),
    ]]
    formula_t = Table(formula_data, colWidths=[3.0*cm, 0.8*cm, 3.0*cm, 0.8*cm, 3.0*cm, 0.8*cm, 3.0*cm])
    formula_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), ARMY_MED),
        ("BACKGROUND",    (2,0), (2,0), ARMY_OLIVE),
        ("BACKGROUND",    (4,0), (4,0), ACCENT_RED),
        ("BACKGROUND",    (6,0), (6,0), colors.HexColor("#1A4A1A")),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [formula_t, vspace(0.4)]
    story += [
        bold("Key Capabilities"),
        bullet("<b>Goods Received Entry:</b> Log new stock purchases with quantity and total cost"),
        bullet("<b>Category Filtering:</b> View ledgers for Dry Rations, Fresh Vegetables, Dairy, Packaging"),
        bullet("<b>Manual Adjustment (Admin only):</b> Reconcile physical count vs system count with reason logging"),
        bullet("<b>Reorder Level Alerts:</b> Set minimum stock limits per item; dashboard shows red warnings"),
        bullet("<b>Shopping List:</b> Auto-generate purchase list from all low-stock items"),
        PageBreak(),
    ]

    # ── SLIDE 9 · SALES & PROFIT ─────────────────────────────────────────────
    story += slide_title("07  Sales, Revenue & Profit Tracking")
    story += [
        body("Real-time financial visibility for every operational day."),
        vspace(0.3),
    ]

    metrics = [
        ("Total Revenue",       "Meals Sold × Selling Price (SP)", ARMY_OLIVE),
        ("Total COGS",          "Ingredients used × Cost Price (CP)", ACCENT_RED),
        ("Net Daily Profit",    "Revenue − COGS", colors.HexColor("#1A4A1A")),
    ]
    metric_cells = [[
        Paragraph(lbl, S("ml", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(frm, S("mf", fontName="Helvetica", fontSize=9, textColor=ARMY_DARK, alignment=TA_CENTER)),
    ] for lbl, frm, _ in metrics]
    metric_bg = [c for _, _, c in metrics]
    mt = Table(metric_cells, colWidths=[5.0*cm, 10.0*cm])
    mt.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("GRID",          (0,0), (-1,-1), 0.4, SLATE),
        *[(("BACKGROUND", (0,i), (0,i), metric_bg[i])) for i in range(len(metrics))],
        *[(("BACKGROUND", (1,i), (1,i), TABLE_ALT if i%2 else WHITE)) for i in range(len(metrics))],
    ]))
    story += [mt, vspace(0.4)]
    story += [
        bold("Additional Features"),
        bullet("<b>Payment Mode Tagging:</b> Each sale tagged as Cash, UPI, or Card"),
        bullet("<b>Wastage Accounting:</b> Unsold/spoiled meals deducted before profit calculation"),
        bullet("<b>Daily Dashboard Widget:</b> Live profit/loss display updated on each entry"),
        bullet("<b>Historical Data:</b> Browse and compare profit across any past date"),
        PageBreak(),
    ]

    # ── SLIDE 10 · ALERTS & REPORTS ──────────────────────────────────────────
    story += slide_title("08  Smart Alerts & One-Click Reports")
    story += [
        bold("Smart Inventory Alerts"),
        bullet("Configurable reorder levels per item (e.g., Sugar: minimum 2 kg)"),
        bullet("🔴 Red dashboard warning badges appear when stock drops below minimum"),
        bullet("Shopping list auto-generated from all items below reorder level"),
        vspace(0.35),
        bold("One-Click Daily Report — Contents"),
    ]
    report_rows = [
        ("Report Section",           "Description"),
        ("Opening Balance",          "Stock at start of day for all items"),
        ("Purchases (Goods Received)", "New stock added during the day"),
        ("Usage (Issued / Cooked)",  "Ingredients consumed via recipe engine"),
        ("Closing Balance",          "Auto-calculated: Opening + Received − Issued"),
        ("Meal Sales Summary",       "Meals sold, wastage, revenue per item"),
        ("Financial Summary",        "Total Revenue, COGS, Net Daily Profit"),
        ("Signature Blocks",         "Prepared By / Checked By / Approved By JCO/Officer"),
    ]
    story += [
        styled_table(report_rows[0], report_rows[1:],
                     col_widths=[6.5*cm, 8.5*cm]),
        vspace(0.3),
        bullet("Report output is an <b>A4-optimised PDF</b> ready to print and sign"),
        bullet("Historical calendar view lets you retrieve any past date's signed report"),
        PageBreak(),
    ]

    # ── SLIDE 11 · NON-FUNCTIONAL REQUIREMENTS ───────────────────────────────
    story += slide_title("09  Non-Functional Requirements")
    nfr_rows = [
        ("Category",       "Requirement"),
        ("Usability",      "Simple enough for non-technical canteen staff with minimal training; large buttons & clear fonts"),
        ("Accessibility",  "Mobile/Tablet responsive interface — staff can enter prep numbers from a tablet in the kitchen"),
        ("Security",       "Password-protected logins; SHA-256 hashed credentials; operators cannot alter historical data without Admin approval"),
        ("Data Backup",    "Daily automated SQLite database backup; one-click manual backup and restore via Admin panel"),
        ("Performance",    "Sub-second response for all common operations; lightweight footprint for field-grade hardware"),
        ("Offline First",  "No internet required — fully functional in low/no-connectivity military field environments"),
    ]
    story += [
        styled_table(nfr_rows[0], nfr_rows[1:], col_widths=[4.5*cm, 10.5*cm]),
        PageBreak(),
    ]

    # ── SLIDE 12 · DATA MODEL ────────────────────────────────────────────────
    story += slide_title("10  Data Model Summary")
    story += [body("The SQLite database contains the following core tables:"), vspace(0.3)]
    dm_rows = [
        ("Table",           "Key Fields",                                  "Purpose"),
        ("users",           "id, username, pw_hash, role, name, rank",     "Authentication & role management"),
        ("inventory",       "id, item, cat, unit, stock, min_lvl, cp",     "Raw material master & live stock"),
        ("menu",            "id, name, sp, active",                        "Finished meal catalogue & pricing"),
        ("recipes",         "id, menu_id, inv_id, qty_per_unit",           "Ingredient–meal linkage (recipe engine)"),
        ("sales",           "id, date, meal, sp, sold, wastage, cogs, payment", "Daily sales & COGS recording"),
        ("goods_received",  "id, date, inv_id, qty, total_cost",           "Inbound stock purchase log"),
        ("batch_prep",      "id, date, menu_id, qty_prepared",             "Batch cook log → triggers auto-deduction"),
        ("expenditure",     "id, date, amount, category, notes",           "Direct cash expenditure tracking"),
    ]
    story += [
        styled_table(dm_rows[0], dm_rows[1:],
                     col_widths=[3.5*cm, 6.5*cm, 5.0*cm]),
        vspace(0.3),
        body("All tables use <b>foreign key constraints</b> (SQLite PRAGMA) and "
             "cascade deletes to maintain referential integrity."),
        PageBreak(),
    ]

    # ── SLIDE 13 · SAMPLE REPORT ─────────────────────────────────────────────
    story += slide_title("11  Sample Daily Operations Report — 06 Apr 2026")
    story += [
        body("Below is a snapshot of an actual report generated by the system for 56 APO Field Canteen."),
        vspace(0.3),
        bold("Meal Sales Summary"),
    ]
    ms_rows = [
        ("Meal Item",  "Sold",  "Wastage",  "Rate",    "Revenue",  "Payment"),
        ("Lunch",      "10",    "0",         "₹10",     "₹100",    "Cash"),
        ("GRAND TOTAL","10",    "0",         "—",       "₹100",    ""),
    ]
    story += [styled_table(ms_rows[0], ms_rows[1:],
                           col_widths=[4.5*cm, 1.8*cm, 2.2*cm, 2.2*cm, 2.5*cm, 2.0*cm]),
              vspace(0.35),
              bold("Financial Summary")]
    fin_rows = [
        ("Total Revenue", "Total COGS",  "Net Daily Profit"),
        ("₹100",          "₹30,000",     "₹ −29,900  (test data)"),
    ]
    story += [styled_table(fin_rows[0], fin_rows[1:]),
              vspace(0.35),
              bold("Inventory Closing Stock")]
    inv_rows = [
        ("Item",  "Category",  "Unit",  "Opening",  "Received",  "Closing",  "Status"),
        ("Rice",  "Dry",       "kg",    "10.0",     "0.0",       "7.0",      "OK"),
    ]
    story += [styled_table(inv_rows[0], inv_rows[1:],
                           col_widths=[2.5*cm, 2.5*cm, 1.5*cm, 2.2*cm, 2.5*cm, 2.3*cm, 1.5*cm]),
              vspace(0.35),
              bold("Official Sign-Off")]
    sig_rows = [
        ("Prepared By",             "Checked By",                    "Approved By"),
        ("Canteen Manager (JCO)",   "Supervision Officer (Subedar)", "Officer-in-Charge (Captain)"),
        ("Signature: ____________", "Signature: ____________",       "Signature: ____________"),
        ("Date: 2026-04-06",        "Date: 2026-04-06",             "Date: 2026-04-06"),
    ]
    story += [styled_table(sig_rows[0], sig_rows[1:]),
              PageBreak()]

    # ── SLIDE 14 · SUMMARY & NEXT STEPS ─────────────────────────────────────
    story += slide_title("12  Summary & Recommended Next Steps")
    story += [
        bold("What Has Been Delivered"),
        bullet("Fully functional <b>desktop application</b> — Python + CustomTkinter + SQLite"),
        bullet("3-tier role-based access (Admin / Manager / Officer) with SHA-256 auth"),
        bullet("Recipe engine for <b>automated stock deduction</b> on batch preparation"),
        bullet("Real-time <b>sales, COGS, and profit</b> tracking per day"),
        bullet("One-click <b>A4 PDF daily report</b> with official signature blocks"),
        bullet("Colour-coded dashboard alerts + auto-generated shopping list"),
        bullet("PyInstaller <b>standalone .exe</b> for zero-dependency deployment"),
        vspace(0.4),
        bold("Recommended Next Steps"),
        bullet("📋  <b>Populate master data:</b> Add all raw materials, menu items and recipes to the system"),
        bullet("📦  <b>Enter opening stock:</b> Conduct physical count and enter opening balances"),
        bullet("🖨  <b>Test report format:</b> Run a sample day, generate and print a report for sign-off approval"),
        bullet("💾  <b>Schedule backups:</b> Enable and verify nightly automated database backup"),
        bullet("📱  <b>Tablet deployment:</b> Test on tablet for kitchen-floor entry by canteen staff"),
        bullet("🔒  <b>Change default passwords</b> for Admin, Manager, and Officer accounts before go-live"),
        vspace(0.5),
        gold_rule(),
        Paragraph(
            "INDIAN ARMY  ·  56 APO FIELD CANTEEN  ·  CONFIDENTIAL — For Official Use Only",
            CAPTION),
    ]

    doc.build(story, onFirstPage=bg, onLaterPages=bg)
    print(f"✅  Presentation saved to:\n    {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
