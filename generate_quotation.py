
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime

# ── Color Palette (Premium Corporate) ────────────────────────────────────────
PRIMARY = colors.HexColor("#1A3A5C")   # Deep Navy
SECONDARY = colors.HexColor("#2E5A88") # Lighter Blue
ACCENT = colors.HexColor("#C8960C")    # Gold
TEXT_DARK = colors.HexColor("#1C1C1C")
TEXT_LIGHT = colors.HexColor("#555555")
BG_LIGHT = colors.HexColor("#F9FAFB")
WHITE = colors.white

W, H = A4
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Software_Quotation_45k.pdf")

class QuotationCanvas:
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
        canv.drawCentredString(W / 2, 0.3*cm, "Confidential Quotation  |  Generated for Client  |  2026")
        
        # Page Number
        canv.drawRightString(W - 1*cm, 0.3*cm, f"Page {doc.page}")
        
        canv.restoreState()

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE = S("Title", fontName="Helvetica-Bold", fontSize=24, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=12)
SUBTITLE = S("Subtitle", fontName="Helvetica-Bold", fontSize=14, textColor=SECONDARY, alignment=TA_LEFT, spaceAfter=6)
BODY = S("Body", fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, leading=14)
BODY_SMALL = S("BodySmall", fontName="Helvetica", fontSize=9, textColor=TEXT_LIGHT, leading=12)
TH_STYLE = S("TableHead", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, alignment=TA_CENTER)
TD_STYLE_L = S("TableDataL", fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, alignment=TA_LEFT)
TD_STYLE_R = S("TableDataR", fontName="Helvetica", fontSize=10, textColor=TEXT_DARK, alignment=TA_RIGHT)
TOTAL_STYLE = S("TotalStyle", fontName="Helvetica-Bold", fontSize=12, textColor=PRIMARY, alignment=TA_RIGHT)

def build_quotation():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="Software Solution Quotation",
    )

    story = []
    bg = QuotationCanvas(doc)

    # ── Header Section ────────────────────────────────────────────────────────
    story.append(Paragraph("QUOTATION", TITLE))
    
    # Client & Date Info Table
    info_data = [
        [Paragraph("<b>Prepared For:</b><br/>Valued Client<br/>Subject: Software Solution Development", BODY),
         Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d %b %Y')}", BODY)]
    ]
    info_table = Table(info_data, colWidths=[10*cm, 7*cm])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 1*cm))

    # ── Executive Summary ─────────────────────────────────────────────────────
    story.append(Paragraph("Project Overview", SUBTITLE))
    story.append(Paragraph(
        "This quotation outlines the investment for a comprehensive software solution tailored to your operational needs. "
        "The proposed system includes full core development, system setup, and an initial management period to ensure "
        "seamless integration and adoption.", BODY))
    story.append(Spacer(1, 0.8*cm))

    # ── Financial Proposal ────────────────────────────────────────────────────
    story.append(Paragraph("Financial Summary", SUBTITLE))
    
    headers = ["Description", "Quantity", "Unit Price", "Total Amount"]
    rows = [
        ["Software Licensing & Core Development\n(Feature-rich customized module)", "1", "₹30,000", "₹30,000"],
        ["System Setup, Configuration & Deployment\n(On-site/Cloud setup & training)", "1", "₹15,000", "₹15,000"],
    ]
    
    # Table Formatting
    table_data = [[Paragraph(h, TH_STYLE) for h in headers]]
    for r in rows:
        table_data.append([
            Paragraph(r[0], TD_STYLE_L),
            Paragraph(r[1], S("C", alignment=TA_CENTER, fontSize=10)),
            Paragraph(r[2], TD_STYLE_R),
            Paragraph(r[3], TD_STYLE_R),
        ])
    
    t = Table(table_data, colWidths=[8*cm, 2.5*cm, 3*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t)
    
    # Grand Total
    total_data = [
        ["", "", Paragraph("<b>Grand Total:</b>", TOTAL_STYLE), Paragraph("<b>₹45,000</b>", TOTAL_STYLE)]
    ]
    tt = Table(total_data, colWidths=[8*cm, 2.5*cm, 3*cm, 3.5*cm])
    tt.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(tt)
    story.append(Spacer(1, 1*cm))

    # ── Maintenance & Support ────────────────────────────────────────────────
    story.append(Paragraph("Maintenance & Support Terms", SUBTITLE))
    
    m_data = [
        ["Phase", "Duration", "Cost", "Status"],
        ["Initial Support Period", "3 Months", "FREE", "Included"],
        ["Post-Warranty Maintenance", "3 Months Cycle", "₹10,000", "Optional"],
    ]
    
    mt = Table(m_data, colWidths=[6*cm, 4*cm, 3.5*cm, 3.5*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(mt)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(
        "<b>Note:</b> The initial 3-month period includes free management and technical maintenance. "
        "Subsequent maintenance is available at ₹10,000 per quarter if required by the client.", BODY_SMALL))
    
    story.append(Spacer(1, 1.5*cm))

    # ── Signatures removed per request ────────────────────────────────────────

    doc.build(story, onFirstPage=bg, onLaterPages=bg)
    return OUTPUT_PATH

if __name__ == "__main__":
    path = build_quotation()
    print(f"Quotation generated: {path}")
