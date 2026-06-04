from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

# ── Color Palette (Premium Corporate) ────────────────────────────────────────
PRIMARY = colors.HexColor("#1A3A5C")   # Deep Navy
SECONDARY = colors.HexColor("#2E5A88") # Lighter Blue
ACCENT = colors.HexColor("#C8960C")    # Gold
TEXT_DARK = colors.HexColor("#1C1C1C")
TEXT_LIGHT = colors.HexColor("#555555")
BG_LIGHT = colors.HexColor("#F9FAFB")
WHITE = colors.white

W, H = A4
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Technical_Specifications.pdf")

class TechSpecCanvas:
    """Adds branding and footer to each page."""
    def __init__(self, doc):
        self.doc = doc

    def __call__(self, canv, doc):
        canv.saveState()
        
        # Header Accent
        canv.setFillColor(PRIMARY)
        canv.rect(0, H - 1.5*cm, W, 1.5*cm, fill=1, stroke=0)
        
        # Footer
        canv.setFillColor(PRIMARY)
        canv.rect(0, 0, W, 0.8*cm, fill=1, stroke=0)
        
        canv.setFillColor(WHITE)
        canv.setFont("Helvetica", 8)
        canv.drawCentredString(W / 2, 0.3*cm, "Technical Specifications  |  System Architecture")
        
        # Page Number
        canv.drawRightString(W - 1*cm, 0.3*cm, f"Page {doc.page}")
        
        canv.restoreState()

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE = S("Title", fontName="Helvetica-Bold", fontSize=24, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=12)
SUBTITLE = S("Subtitle", fontName="Helvetica-Bold", fontSize=14, textColor=SECONDARY, alignment=TA_LEFT, spaceAfter=6, spaceBefore=12)
BODY = S("Body", fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, leading=14, spaceAfter=8)
BULLET = S("Bullet", fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, leading=14, leftIndent=15, spaceAfter=4)
TH_STYLE = S("TableHead", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, alignment=TA_LEFT)
TD_STYLE_L = S("TableDataL", fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, alignment=TA_LEFT)

def build_tech_specs():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="Technical Specifications",
    )

    story = []
    bg = TechSpecCanvas(doc)

    # ── Header Section ────────────────────────────────────────────────────────
    story.append(Paragraph("TECHNICAL SPECIFICATIONS", TITLE))
    story.append(Paragraph("<b>Document:</b> System Architecture & Technology Stack Overview", BODY))
    story.append(Spacer(1, 1*cm))

    # ── Executive Summary ─────────────────────────────────────────────────────
    story.append(Paragraph("1. System Overview", SUBTITLE))
    story.append(Paragraph(
        "The proposed application is a robust, offline-first desktop management system designed for high reliability "
        "and ease of use in environments with limited internet connectivity. It is built as a monolithic desktop application "
        "with an embedded local database, ensuring zero dependencies on external cloud infrastructure for core operations.", BODY))

    # ── Technology Stack ────────────────────────────────────────────────────
    story.append(Paragraph("2. Core Technology Stack", SUBTITLE))
    
    tech_data = [
        ["Component", "Technology", "Description & Purpose"],
        ["Programming Language", "Python 3.12+", "Core backend logic, data processing, and application structure."],
        ["GUI Framework", "CustomTkinter", "Modern, hardware-accelerated user interface supporting dark/light themes."],
        ["Database Engine", "SQLite3", "Embedded, serverless database for secure, local data storage. Zero configuration required."],
        ["Reporting Engine", "ReportLab", "Dynamic generation of A4 print-ready PDF reports and ledgers."],
        ["Image Processing", "Pillow (PIL)", "Efficient handling and rendering of UI images, icons, and diagrams."],
        ["Deployment", "PyInstaller", "Packages the application into a standalone Windows .exe file with all dependencies."]
    ]
    
    # Table Formatting
    table_data = []
    for i, r in enumerate(tech_data):
        if i == 0:
            table_data.append([Paragraph(c, TH_STYLE) for c in r])
        else:
            table_data.append([Paragraph(c, TD_STYLE_L) for c in r])
            
    t = Table(table_data, colWidths=[4*cm, 4*cm, 9*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t)
    
    # ── Architecture & Security ──────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("3. Architecture & Security Features", SUBTITLE))
    
    security_features = [
        "<b>Role-Based Access Control (RBAC):</b> Hierarchical access (Admin, Manager, Officer) ensuring users only see what they are authorized to access.",
        "<b>Cryptographic Hashing:</b> All user passwords are encrypted using SHA-256 hashing algorithms; no plain-text credentials are saved.",
        "<b>Offline-First Design:</b> The system requires absolutely no active internet connection, minimizing external attack vectors and downtime.",
        "<b>Automated Data Redundancy:</b> Built-in automated SQLite database backups to prevent data loss, with one-click restore capabilities.",
        "<b>Referential Integrity:</b> Strict foreign key constraints and cascading operations within the database to prevent orphaned records."
    ]
    
    for feature in security_features:
        story.append(Paragraph(f"• {feature}", BULLET))

    # ── Hardware Requirements ──────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("4. Minimum Hardware Requirements", SUBTITLE))
    
    hw_data = [
        ["Hardware", "Minimum Requirement"],
        ["Operating System", "Windows 10 / 11 (64-bit)"],
        ["Processor (CPU)", "Intel Core i3 or equivalent AMD processor"],
        ["Memory (RAM)", "4 GB RAM (8 GB recommended for optimal performance)"],
        ["Storage", "500 MB available disk space (SSD recommended)"],
        ["Display Resolution", "1366 x 768 minimum (1920 x 1080 recommended)"]
    ]
    
    hw_table_data = []
    for i, r in enumerate(hw_data):
        if i == 0:
            hw_table_data.append([Paragraph(c, TH_STYLE) for c in r])
        else:
            hw_table_data.append([Paragraph(c, TD_STYLE_L) for c in r])
            
    hw_t = Table(hw_table_data, colWidths=[5*cm, 12*cm])
    hw_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(hw_t)

    doc.build(story, onFirstPage=bg, onLaterPages=bg)
    return OUTPUT_PATH

if __name__ == "__main__":
    path = build_tech_specs()
    print(f"Specs generated: {path}")
