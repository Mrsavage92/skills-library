#!/usr/bin/env python3
"""
Marketing Report PDF Generator
AI Marketing Suite for Claude Code
"""

import sys
import json
import math
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.units import mm, cm
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable
    )
    from reportlab.graphics.shapes import Drawing, Circle, Wedge, Rect, String, Line
    from reportlab.graphics.charts.barcharts import HorizontalBarChart
    from reportlab.graphics import renderPDF
    from reportlab.platypus.flowables import Flowable
except ImportError:
    print("ERROR: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)

# ─── Colour Palette ────────────────────────────────────────────────────────────
C_NAVY   = HexColor("#1B2A4A")
C_BLUE   = HexColor("#2D5BFF")
C_ORANGE = HexColor("#FF6B35")
C_GREEN  = HexColor("#00C853")
C_AMBER  = HexColor("#FFB300")
C_RED    = HexColor("#FF1744")
C_LGRAY  = HexColor("#F5F7FA")
C_BODY   = HexColor("#2C3E50")
C_SEC    = HexColor("#7F8C9B")
C_BORDER = HexColor("#E0E6ED")
C_WHITE  = white

def score_color(score):
    if score >= 80: return C_GREEN
    if score >= 60: return C_BLUE
    if score >= 40: return C_AMBER
    return C_RED

def score_grade(score):
    if score >= 85: return "A"
    if score >= 70: return "B"
    if score >= 55: return "C"
    if score >= 40: return "D"
    return "F"

def severity_color(sev):
    s = sev.lower()
    if s == "critical": return C_RED
    if s == "high":     return C_ORANGE
    if s == "medium":   return C_AMBER
    return C_BLUE

# ─── Custom Flowables ──────────────────────────────────────────────────────────

class ScoreGauge(Flowable):
    """Circular gauge showing the overall score."""
    def __init__(self, score, width=160, height=160):
        Flowable.__init__(self)
        self.score = score
        self.width = width
        self.height = height

    def draw(self):
        cx, cy = self.width / 2, self.height / 2
        r_outer = min(cx, cy) - 8
        r_inner = r_outer * 0.65
        stroke_w = r_outer - r_inner

        # Background arc (full circle, grey)
        # Draw as thick circle using multiple wedges
        bg = C_BORDER
        fg = score_color(self.score)

        # Background circle (grey)
        self.canv.setStrokeColor(C_BORDER)
        self.canv.setFillColor(C_BORDER)
        self.canv.circle(cx, cy, r_outer, fill=0, stroke=0)

        # Draw background donut
        angle_bg = 360
        self.canv.setFillColor(C_LGRAY)
        self.canv.circle(cx, cy, r_outer, fill=1, stroke=0)
        self.canv.setFillColor(C_WHITE)
        self.canv.circle(cx, cy, r_inner, fill=1, stroke=0)

        # Draw score arc (from 225° going clockwise, 270° total sweep)
        start_angle = 225  # bottom-left
        sweep = 270        # three-quarters
        score_sweep = (self.score / 100) * sweep

        # Draw background track
        self._draw_arc(cx, cy, r_outer, r_inner, start_angle, sweep, C_BORDER)
        # Draw score fill
        if score_sweep > 0:
            self._draw_arc(cx, cy, r_outer, r_inner, start_angle, score_sweep, score_color(self.score))

        # Inner white circle
        self.canv.setFillColor(C_WHITE)
        self.canv.circle(cx, cy, r_inner - 2, fill=1, stroke=0)

        # Score number
        self.canv.setFillColor(C_NAVY)
        self.canv.setFont("Helvetica-Bold", int(r_inner * 0.65))
        self.canv.drawCentredString(cx, cy - 2, str(self.score))

        # Grade label
        grade = score_grade(self.score)
        self.canv.setFont("Helvetica", int(r_inner * 0.28))
        self.canv.setFillColor(C_SEC)
        self.canv.drawCentredString(cx, cy - r_inner * 0.45, f"Grade {grade}")

    def _draw_arc(self, cx, cy, r_outer, r_inner, start_angle, sweep, color):
        """Draw a donut arc segment."""
        self.canv.setFillColor(color)
        self.canv.setStrokeColor(color)
        steps = max(int(sweep), 1)
        step_size = sweep / steps
        import math
        for i in range(steps):
            a1 = math.radians(start_angle - i * step_size)
            a2 = math.radians(start_angle - (i + 1) * step_size)
            # Draw thin wedge
            x1o = cx + r_outer * math.cos(a1)
            y1o = cy + r_outer * math.sin(a1)
            x2o = cx + r_outer * math.cos(a2)
            y2o = cy + r_outer * math.sin(a2)
            x1i = cx + r_inner * math.cos(a1)
            y1i = cy + r_inner * math.sin(a1)
            x2i = cx + r_inner * math.cos(a2)
            y2i = cy + r_inner * math.sin(a2)
            p = self.canv.beginPath()
            p.moveTo(x1o, y1o)
            p.lineTo(x2o, y2o)
            p.lineTo(x2i, y2i)
            p.lineTo(x1i, y1i)
            p.close()
            self.canv.drawPath(p, fill=1, stroke=0)


class ColorBar(Flowable):
    """Horizontal color bar for category scores."""
    def __init__(self, score, width=300, height=16):
        Flowable.__init__(self)
        self.score = score
        self.width = width
        self.height = height

    def draw(self):
        # Background
        self.canv.setFillColor(C_LGRAY)
        self.canv.roundRect(0, 0, self.width, self.height, self.height/2, fill=1, stroke=0)
        # Fill
        fill_w = (self.score / 100) * self.width
        if fill_w > 0:
            self.canv.setFillColor(score_color(self.score))
            self.canv.roundRect(0, 0, fill_w, self.height, self.height/2, fill=1, stroke=0)


class SeverityBadge(Flowable):
    """Colored severity badge."""
    def __init__(self, text, width=70, height=18):
        Flowable.__init__(self)
        self.text = text
        self.width = width
        self.height = height

    def draw(self):
        color = severity_color(self.text)
        self.canv.setFillColor(color)
        self.canv.roundRect(0, 0, self.width, self.height, self.height/2, fill=1, stroke=0)
        self.canv.setFillColor(C_WHITE)
        self.canv.setFont("Helvetica-Bold", 8)
        self.canv.drawCentredString(self.width/2, self.height/2 - 3, self.text.upper())


# ─── Styles ────────────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["cover_title"] = ParagraphStyle("cover_title",
        fontName="Helvetica-Bold", fontSize=28, textColor=C_NAVY,
        spaceAfter=6, leading=34)

    styles["cover_subtitle"] = ParagraphStyle("cover_subtitle",
        fontName="Helvetica", fontSize=13, textColor=C_SEC,
        spaceAfter=4, leading=18)

    styles["section_heading"] = ParagraphStyle("section_heading",
        fontName="Helvetica-Bold", fontSize=16, textColor=C_NAVY,
        spaceBefore=16, spaceAfter=8, leading=20)

    styles["subsection_heading"] = ParagraphStyle("subsection_heading",
        fontName="Helvetica-Bold", fontSize=11, textColor=C_NAVY,
        spaceBefore=8, spaceAfter=4, leading=14)

    styles["body"] = ParagraphStyle("body",
        fontName="Helvetica", fontSize=10, textColor=C_BODY,
        spaceAfter=6, leading=15)

    styles["body_small"] = ParagraphStyle("body_small",
        fontName="Helvetica", fontSize=9, textColor=C_BODY,
        spaceAfter=4, leading=13)

    styles["caption"] = ParagraphStyle("caption",
        fontName="Helvetica", fontSize=8, textColor=C_SEC,
        spaceAfter=2, leading=11)

    styles["action_item"] = ParagraphStyle("action_item",
        fontName="Helvetica", fontSize=10, textColor=C_BODY,
        spaceAfter=5, leading=14, leftIndent=16)

    styles["table_header"] = ParagraphStyle("table_header",
        fontName="Helvetica-Bold", fontSize=9, textColor=C_WHITE, leading=12)

    styles["table_cell"] = ParagraphStyle("table_cell",
        fontName="Helvetica", fontSize=9, textColor=C_BODY, leading=12)

    styles["url_style"] = ParagraphStyle("url_style",
        fontName="Helvetica", fontSize=11, textColor=C_BLUE,
        spaceAfter=2, leading=14)

    styles["footer"] = ParagraphStyle("footer",
        fontName="Helvetica", fontSize=7, textColor=C_SEC,
        alignment=TA_CENTER, leading=10)

    return styles


# ─── Page Template ─────────────────────────────────────────────────────────────

def on_page(canvas, doc, brand_name, date_str):
    """Header/footer on every page except cover."""
    W, H = A4
    if doc.page == 1:
        return
    # Top bar
    canvas.saveState()
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, H - 28, W, 28, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(20, H - 18, f"Marketing Audit Report — {brand_name}")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(W - 20, H - 18, date_str)

    # Bottom bar
    canvas.setFillColor(C_LGRAY)
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setFillColor(C_SEC)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(20, 7, "Generated by AI Marketing Suite for Claude Code")
    canvas.drawRightString(W - 20, 7, f"Page {doc.page}")
    canvas.restoreState()


# ─── Report Sections ──────────────────────────────────────────────────────────

def build_cover(data, styles):
    W, H = A4
    elements = []

    # Top navy band (full width illusion via table)
    band_data = [["" ]]
    band = Table(band_data, colWidths=[W - 80], rowHeights=[6])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_ORANGE),
        ("LINEABOVE", (0,0), (-1,0), 0, C_ORANGE),
    ]))
    elements.append(band)
    elements.append(Spacer(1, 30))

    # Title block
    elements.append(Paragraph("Marketing Audit Report", styles["cover_title"]))
    elements.append(Paragraph(data.get("brand_name", ""), ParagraphStyle("bn",
        fontName="Helvetica-Bold", fontSize=20, textColor=C_ORANGE, spaceAfter=4)))
    elements.append(Paragraph(data.get("url", ""), styles["url_style"]))
    elements.append(Paragraph(data.get("date", ""), styles["cover_subtitle"]))
    elements.append(Spacer(1, 24))

    # Score gauge + executive summary side by side
    gauge = ScoreGauge(data.get("overall_score", 0), width=160, height=160)
    grade = score_grade(data.get("overall_score", 0))
    score_val = data.get("overall_score", 0)
    color_hex = {
        score_color(score_val) == C_GREEN: "#00C853",
        score_color(score_val) == C_BLUE:  "#2D5BFF",
        score_color(score_val) == C_AMBER: "#FFB300",
        score_color(score_val) == C_RED:   "#FF1744",
    }.get(True, "#7F8C9B")

    exec_text = data.get("executive_summary", "")
    exec_para = Paragraph(exec_text, ParagraphStyle("exec",
        fontName="Helvetica", fontSize=10, textColor=C_BODY,
        leading=16, spaceAfter=0))

    grade_para = Paragraph(
        f'<font color="{color_hex}"><b>Overall Score: {score_val}/100 — Grade {grade}</b></font>',
        ParagraphStyle("gp", fontName="Helvetica-Bold", fontSize=13,
                       textColor=C_NAVY, spaceAfter=10, leading=16))

    right_col = [grade_para, exec_para]

    cover_table = Table(
        [[gauge, right_col]],
        colWidths=[180, W - 80 - 180],
        rowHeights=[None]
    )
    cover_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (0,0), 0),
        ("RIGHTPADDING", (0,0), (0,0), 20),
    ]))
    elements.append(cover_table)
    elements.append(Spacer(1, 30))

    # Divider
    elements.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    elements.append(Spacer(1, 16))

    # Category score pills row
    categories = data.get("categories", {})
    pill_rows = []
    cat_items = list(categories.items())
    for i in range(0, len(cat_items), 3):
        row = []
        for cat_name, cat_data in cat_items[i:i+3]:
            s = cat_data.get("score", 0)
            w = cat_data.get("weight", "")
            sc = score_color(s)
            hex_c = "#00C853" if sc == C_GREEN else ("#2D5BFF" if sc == C_BLUE else ("#FFB300" if sc == C_AMBER else "#FF1744"))
            cell = Paragraph(
                f'<b>{cat_name}</b><br/>'
                f'<font color="{hex_c}" size="18"><b>{s}</b></font>'
                f'<font color="#7F8C9B" size="8">/100 · {w}</font>',
                ParagraphStyle("pill", fontName="Helvetica", fontSize=10,
                               textColor=C_BODY, leading=16, alignment=TA_CENTER))
            row.append(cell)
        while len(row) < 3:
            row.append("")
        pill_rows.append(row)

    pill_table = Table(pill_rows, colWidths=[(W-80)/3]*3)
    pill_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_LGRAY),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWPADDING", (0,0), (-1,-1), 10),
        ("BOX", (0,0), (-1,-1), 0.5, C_BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.5, C_BORDER),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ]))
    elements.append(pill_table)
    elements.append(PageBreak())
    return elements


def build_score_breakdown(data, styles):
    W, H = A4
    elements = []
    elements.append(Paragraph("Score Breakdown", styles["section_heading"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    elements.append(Spacer(1, 12))

    categories = data.get("categories", {})
    bar_w = 260

    rows = [
        [
            Paragraph("<b>Category</b>", styles["table_header"]),
            Paragraph("<b>Score</b>", styles["table_header"]),
            Paragraph("<b>Weight</b>", styles["table_header"]),
            Paragraph("<b>Weighted</b>", styles["table_header"]),
            Paragraph("<b>Bar</b>", styles["table_header"]),
            Paragraph("<b>Status</b>", styles["table_header"]),
        ]
    ]

    for cat_name, cat_data in categories.items():
        s = cat_data.get("score", 0)
        w_str = cat_data.get("weight", "0%")
        w_float = float(w_str.replace("%","")) / 100
        weighted = round(s * w_float, 1)

        sc = score_color(s)
        hex_c = "#00C853" if sc == C_GREEN else ("#2D5BFF" if sc == C_BLUE else ("#FFB300" if sc == C_AMBER else "#FF1744"))
        status = "Strong" if s >= 80 else ("Good" if s >= 60 else ("Needs Work" if s >= 40 else "Critical"))

        rows.append([
            Paragraph(cat_name, styles["table_cell"]),
            Paragraph(f'<font color="{hex_c}"><b>{s}/100</b></font>', styles["table_cell"]),
            Paragraph(w_str, styles["table_cell"]),
            Paragraph(f"{weighted}", styles["table_cell"]),
            ColorBar(s, width=bar_w * 0.55, height=12),
            Paragraph(f'<font color="{hex_c}"><b>{status}</b></font>', styles["table_cell"]),
        ])

    col_widths = [150, 55, 50, 55, bar_w * 0.55, 60]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_NAVY),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LGRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, C_BORDER),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    # Score legend
    legend_items = [
        ("80–100", "Strong", "#00C853"),
        ("60–79",  "Good",   "#2D5BFF"),
        ("40–59",  "Needs Work", "#FFB300"),
        ("0–39",   "Critical",  "#FF1744"),
    ]
    legend_row = []
    for rng, label, col in legend_items:
        legend_row.append(Paragraph(
            f'<font color="{col}">■</font> <b>{rng}</b> {label}',
            ParagraphStyle("leg", fontName="Helvetica", fontSize=8, textColor=C_BODY, leading=11)
        ))
    leg_table = Table([legend_row], colWidths=[(W-80)/4]*4)
    leg_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("BACKGROUND", (0,0), (-1,-1), C_LGRAY),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("BOX", (0,0), (-1,-1), 0.5, C_BORDER),
    ]))
    elements.append(leg_table)
    elements.append(PageBreak())
    return elements


def build_findings(data, styles):
    W, H = A4
    elements = []
    elements.append(Paragraph("Key Findings", styles["section_heading"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    elements.append(Spacer(1, 12))

    findings = data.get("findings", [])
    if not findings:
        elements.append(Paragraph("No findings recorded.", styles["body"]))
        elements.append(PageBreak())
        return elements

    rows = [[
        Paragraph("<b>Severity</b>", styles["table_header"]),
        Paragraph("<b>Finding</b>", styles["table_header"]),
    ]]

    for f in findings:
        sev = f.get("severity", "Low")
        text = f.get("finding", "")
        sc = severity_color(sev)
        hex_c = {
            C_RED: "#FF1744", C_ORANGE: "#FF6B35",
            C_AMBER: "#FFB300", C_BLUE: "#2D5BFF",
        }.get(sc, "#2D5BFF")

        rows.append([
            Paragraph(f'<font color="{hex_c}"><b>{sev}</b></font>', styles["table_cell"]),
            Paragraph(text, styles["table_cell"]),
        ])

    t = Table(rows, colWidths=[75, W - 80 - 75], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_NAVY),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LGRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, C_BORDER),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    elements.append(t)
    elements.append(PageBreak())
    return elements


def build_action_plan(data, styles):
    W, H = A4
    elements = []
    elements.append(Paragraph("Prioritised Action Plan", styles["section_heading"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    elements.append(Spacer(1, 12))

    sections = [
        ("quick_wins",   "Quick Wins",    "This Week",      C_GREEN,  "#00C853"),
        ("medium_term",  "Medium Term",   "1–3 Months",     C_BLUE,   "#2D5BFF"),
        ("strategic",    "Strategic",     "3–6 Months",     C_ORANGE, "#FF6B35"),
    ]

    for key, label, timeline, color, hex_c in sections:
        items = data.get(key, [])
        if not items:
            continue

        # Section header band
        header_data = [[
            Paragraph(f'<font color="white"><b>{label}</b></font>',
                      ParagraphStyle("ah", fontName="Helvetica-Bold", fontSize=11, textColor=C_WHITE, leading=14)),
            Paragraph(f'<font color="white">{timeline}</font>',
                      ParagraphStyle("at", fontName="Helvetica", fontSize=9, textColor=C_WHITE,
                                     leading=14, alignment=TA_RIGHT)),
        ]]
        ht = Table(header_data, colWidths=[W-80-100, 100])
        ht.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), color),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 12),
            ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ]))
        elements.append(ht)

        # Action items
        action_rows = []
        for i, item in enumerate(items, 1):
            action_rows.append([
                Paragraph(f'<font color="{hex_c}"><b>{i}</b></font>',
                          ParagraphStyle("num", fontName="Helvetica-Bold", fontSize=12,
                                         textColor=color, leading=15, alignment=TA_CENTER)),
                Paragraph(item, styles["body_small"]),
            ])

        at = Table(action_rows, colWidths=[30, W-80-30])
        at.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("ALIGN", (0,0), (0,-1), "CENTER"),
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [C_WHITE, C_LGRAY]),
            ("GRID", (0,0), (-1,-1), 0.3, C_BORDER),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]))
        elements.append(at)
        elements.append(Spacer(1, 14))

    elements.append(PageBreak())
    return elements


def build_competitors(data, styles):
    W, H = A4
    elements = []
    competitors = data.get("competitors", [])
    if not competitors:
        return elements

    elements.append(Paragraph("Competitive Landscape", styles["section_heading"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    elements.append(Spacer(1, 12))

    brand = data.get("brand_name", "Client")
    target = data.get("target_comparison", {})

    headers = ["Factor", brand] + [c.get("name", f"Competitor {i+1}") for i, c in enumerate(competitors[:3])]
    rows = [headers]

    factors = ["positioning", "pricing", "social_proof", "content"]
    factor_labels = ["Positioning", "Pricing", "Social Proof", "Content"]

    for factor, label in zip(factors, factor_labels):
        row = [label]
        row.append(target.get(factor, "—"))
        for comp in competitors[:3]:
            row.append(comp.get(factor, "—"))
        rows.append(row)

    n_cols = len(headers)
    col_w = (W - 80) / n_cols
    t = Table(
        [[Paragraph(str(cell), ParagraphStyle("ct", fontName="Helvetica-Bold" if i==0 else "Helvetica",
                                               fontSize=8, textColor=C_WHITE if i==0 else C_BODY, leading=11))
          for i, cell in enumerate(row)]
         for row in rows],
        colWidths=[col_w] * n_cols,
        repeatRows=1
    )

    style_cmds = [
        ("BACKGROUND", (0,0), (-1,0), C_NAVY),
        ("BACKGROUND", (1,0), (1,0), C_ORANGE),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LGRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, C_BORDER),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), C_NAVY),
    ]
    t.setStyle(TableStyle(style_cmds))
    elements.append(t)
    elements.append(PageBreak())
    return elements


def build_methodology(data, styles):
    W, H = A4
    elements = []
    elements.append(Paragraph("Methodology & Scoring", styles["section_heading"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "This audit was conducted using the AI Marketing Suite for Claude Code. "
        "Each category was assessed against industry benchmarks and best practices, "
        "with scores derived from direct website analysis, third-party review data, "
        "and competitive research.",
        styles["body"]
    ))
    elements.append(Spacer(1, 10))

    def _cell(content, style):
        """Wrap a string in a Paragraph; pass through existing flowables unchanged."""
        if isinstance(content, str):
            return Paragraph(content, style)
        return content

    meth_data = [
        ("Category",              "Weight", "What It Measures",                                                                              True),
        ("Content & Messaging",   "25%",    "Copy quality, value proposition clarity, headline effectiveness, social proof, content depth",   False),
        ("Conversion Optimization","20%",   "CTA placement and clarity, form friction, trust signals near CTAs, pricing transparency, urgency",False),
        ("SEO & Discoverability", "20%",    "Title tags, meta descriptions, header hierarchy, schema markup, local SEO, content marketing",    False),
        ("Competitive Positioning","15%",   "Differentiation, awards, comparison content, review reputation vs competitors",                   False),
        ("Brand & Trust",         "10%",    "Review ratings, design quality, About page depth, contact accessibility, review management",      False),
        ("Growth & Strategy",     "10%",    "Email capture, loyalty programs, remarketing, revenue diversification, events/seasonal",          False),
    ]

    meth_rows = []
    for cat, weight, desc, is_header in meth_data:
        s_cat  = styles["table_header"] if is_header else styles["table_cell"]
        s_body = styles["table_header"] if is_header else styles["table_cell"]
        cat_text  = f"<b>{cat}</b>"  if is_header else cat
        desc_text = f"<b>{desc}</b>" if is_header else desc
        meth_rows.append([
            Paragraph(cat_text,  s_cat),
            Paragraph(weight,    s_body),
            Paragraph(desc_text, s_body),
        ])

    t = Table(meth_rows, colWidths=[150, 50, W-80-200], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_NAVY),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LGRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, C_BORDER),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 16))
    elements.append(Paragraph(
        "Score bands: 85–100 (A) Excellent · 70–84 (B) Good · 55–69 (C) Average · 40–54 (D) Below Average · 0–39 (F) Critical",
        styles["caption"]
    ))
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        "Generated by AI Marketing Suite for Claude Code · Not for redistribution without client permission.",
        styles["footer"]
    ))
    return elements


# ─── Main ──────────────────────────────────────────────────────────────────────

def generate(json_path, output_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    brand_name = data.get("brand_name", "Client")
    date_str   = data.get("date", datetime.now().strftime("%B %d, %Y"))

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40, rightMargin=40,
        topMargin=48, bottomMargin=30,
        title=f"Marketing Audit — {brand_name}",
        author="AI Marketing Suite",
        subject="Marketing Audit Report",
    )

    styles = make_styles()
    story  = []

    story += build_cover(data, styles)
    story += build_score_breakdown(data, styles)
    story += build_findings(data, styles)
    story += build_action_plan(data, styles)
    story += build_competitors(data, styles)
    story += build_methodology(data, styles)

    def _on_page(canvas, doc):
        on_page(canvas, doc, brand_name, date_str)

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    print(f"PDF generated: {output_path}")


def demo():
    """Generate a demo report with sample data."""
    sample = {
        "url": "https://www.example.com",
        "date": datetime.now().strftime("%B %d, %Y"),
        "brand_name": "Example Business",
        "overall_score": 62,
        "executive_summary": "Example Business has a solid foundation with good brand recognition and active social media. The primary opportunities lie in conversion optimisation—particularly the lack of social proof on key pages—and a fragmented SEO strategy. Implementing the Quick Wins below could yield an estimated $5,000–$12,000/month in additional revenue within 90 days.",
        "categories": {
            "Content & Messaging":    {"score": 68, "weight": "25%"},
            "Conversion Optimization":{"score": 52, "weight": "20%"},
            "SEO & Discoverability":  {"score": 74, "weight": "20%"},
            "Competitive Positioning":{"score": 48, "weight": "15%"},
            "Brand & Trust":          {"score": 70, "weight": "10%"},
            "Growth & Strategy":      {"score": 55, "weight": "10%"},
        },
        "findings": [
            {"severity": "Critical", "finding": "Homepage has no call-to-action button above the fold. Primary conversion path is invisible to most visitors."},
            {"severity": "High",     "finding": "No review ratings or testimonials displayed anywhere on the website despite having 400+ Google reviews."},
            {"severity": "High",     "finding": "Meta descriptions missing on all pages, reducing organic search click-through rate."},
            {"severity": "Medium",   "finding": "Functions/bookings page has no pricing or capacity information, forcing potential clients to email for basics."},
            {"severity": "Low",      "finding": "Newsletter signup has no stated benefit, reducing conversion from interested visitors."},
        ],
        "quick_wins": [
            "Add star rating badge (e.g. '4.4★ on Google · 400+ reviews') to homepage hero section",
            "Insert a 'Book Now' CTA button in the hero, linking to the booking form",
            "Write meta descriptions for all 8 main pages and update in CMS",
        ],
        "medium_term": [
            "Overhaul the functions page with pricing tiers, capacity info, and 2–3 testimonials",
            "Add Event schema (JSON-LD) to all entertainment listings to enable Google Event rich results",
            "Upgrade newsletter signup with a clear benefit statement and incentive",
        ],
        "strategic": [
            "Launch a local content blog (2 posts/month) targeting high-intent local search terms",
            "Implement Facebook Pixel and Google Analytics for retargeting and attribution",
            "Build a 'Why Choose Us' page addressing competitor differentiators directly",
        ],
        "target_comparison": {
            "positioning": "Local multi-venue pub and events space",
            "pricing":     "Mid-range, pub classics",
            "social_proof":"4.4★ Google (400+ reviews)",
            "content":     "Static brochure site, no blog",
        },
        "competitors": [
            {"name": "Competitor A", "positioning": "Historic hinterland pub", "pricing": "Mid-range",
             "social_proof": "4.1★ TripAdvisor", "content": "Events calendar, blog"},
            {"name": "Competitor B", "positioning": "Craft brewery + dining", "pricing": "Premium",
             "social_proof": "4.6★ Google (800+)", "content": "Active social, weekly posts"},
        ],
    }
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tf:
        json.dump(sample, tf, indent=2)
        tmp = tf.name
    generate(tmp, "MARKETING-REPORT-sample.pdf")
    os.unlink(tmp)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        demo()
    elif len(sys.argv) == 3:
        generate(sys.argv[1], sys.argv[2])
    else:
        print("Usage: generate_pdf_report.py <data.json> <output.pdf>")
        print("       generate_pdf_report.py   (demo mode)")
        sys.exit(1)
