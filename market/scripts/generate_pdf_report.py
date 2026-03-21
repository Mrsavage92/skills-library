#!/usr/bin/env python3
"""
Marketing Audit — Enterprise PDF Report Generator
Reads MARKETING-AUDIT.md and produces a premium, client-ready A4 PDF.
Usage: py generate_pdf_report.py "C:\\path\\to\\audit\\folder"
       py generate_pdf_report.py "C:\\path\\to\\MARKETING-AUDIT.md"
"""
import sys, os, re, math
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor, Color
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus import (
        BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
        Table, TableStyle, PageBreak, Flowable, NextPageTemplate, KeepTogether
    )
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("ERROR: reportlab required. Run: py -m pip install reportlab")
    sys.exit(1)

# ─── FONTS ────────────────────────────────────────────────────────────────────

_FONT_MAP = [
    ("Seg",      "C:/Windows/Fonts/segoeui.ttf"),
    ("Seg-Sb",   "C:/Windows/Fonts/seguisb.ttf"),
    ("Seg-Bd",   "C:/Windows/Fonts/segoeuib.ttf"),
    ("Seg-Li",   "C:/Windows/Fonts/segoeuil.ttf"),
]
_loaded = set()
for _n, _p in _FONT_MAP:
    if os.path.exists(_p):
        try:
            pdfmetrics.registerFont(TTFont(_n, _p))
            _loaded.add(_n)
        except Exception:
            pass

if "Seg" in _loaded:
    R  = "Seg"
    SB = "Seg-Sb" if "Seg-Sb" in _loaded else "Seg"
    BD = "Seg-Bd" if "Seg-Bd" in _loaded else "Seg"
    LI = "Seg-Li" if "Seg-Li" in _loaded else "Seg"
else:
    R = SB = BD = LI = "Helvetica"
    BD = "Helvetica-Bold"

# ─── LAYOUT ───────────────────────────────────────────────────────────────────

PW, PH   = A4          # 595.28 x 841.89 pt
MAR      = 1.8 * cm
CW       = PW - 2 * MAR   # usable content width

# ─── COLOUR PALETTE ───────────────────────────────────────────────────────────

C = {
    "brand":   HexColor("#1a1a2e"),    # dark navy
    "brand2":  HexColor("#16213e"),    # slightly lighter navy
    "accent":  HexColor("#e94560"),    # red-pink
    "ink":     HexColor("#0f172a"),
    "body":    HexColor("#334155"),
    "muted":   HexColor("#64748b"),
    "subtle":  HexColor("#94a3b8"),
    "border":  HexColor("#e2e8f0"),
    "surf":    HexColor("#f8fafc"),
    "surf2":   HexColor("#f1f5f9"),
    "white":   HexColor("#ffffff"),
    "ok":      HexColor("#16a34a"),
    "ok_bg":   HexColor("#f0fdf4"),
    "warn":    HexColor("#d97706"),
    "warn_bg": HexColor("#fffbeb"),
    "err":     HexColor("#dc2626"),
    "err_bg":  HexColor("#fef2f2"),
    "info":    HexColor("#2563eb"),
    "info_bg": HexColor("#eff6ff"),
    "vio":     HexColor("#6d28d9"),
    "vio_bg":  HexColor("#f5f3ff"),
}

CAT_COLS = [
    HexColor("#e94560"), HexColor("#2563eb"), HexColor("#16a34a"),
    HexColor("#d97706"), HexColor("#6d28d9"), HexColor("#0891b2"),
]

def sc_col(s):
    if s >= 80: return C["ok"]
    if s >= 65: return C["info"]
    if s >= 50: return C["warn"]
    return C["err"]

def grade(s):
    if s >= 90: return "A+"
    if s >= 80: return "A"
    if s >= 70: return "B"
    if s >= 60: return "C"
    if s >= 50: return "D"
    return "F"

def esc(t):
    return (str(t)
        .replace("—", " - ").replace("–", " - ")
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ─── FLOWABLES ────────────────────────────────────────────────────────────────

class HRule(Flowable):
    def __init__(self, width=None, height=0.5, color=None):
        super().__init__()
        self.width  = width or CW
        self.height = height
        self.color  = color or C["border"]
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


class AccentBar(Flowable):
    def __init__(self, height=3, color=None):
        super().__init__()
        self.width  = CW
        self.height = height
        self.color  = color or C["accent"]
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


class ScoreGauge(Flowable):
    """
    Semicircular (top-half) score gauge.
    Track goes from 9-o'clock (180°) to 3-o'clock (0°) counterclockwise.
    Fill goes from 9-o'clock clockwise to proportional point.
    """
    def __init__(self, score, size=180, label="", on_dark=False):
        super().__init__()
        self.score   = max(0, min(100, int(score)))
        self.size    = size
        self.label   = label
        self.on_dark = on_dark
        self.width   = size
        # cy = circle centre measured from flowable bottom
        # r  = radius, lw = stroke width
        # height must satisfy: cy + r + lw/2 + 4 ≤ height   (arc fits at top)
        #                  and: cy - inner_r ≥ 4             (inner circle doesn't overflow bottom)
        # inner_r = r - lw*0.70
        # With cy=sz*0.38, r=sz*0.40, lw=sz*0.082:
        #   top check:    0.38+0.40+0.041 = 0.821 → height = sz*0.85 gives 0.029 margin ✓
        #   bottom check: cy - inner_r = 0.38 - (0.40-0.057) = 0.38 - 0.343 = 0.037*sz ≈ 7pt ✓
        self.height  = size * 0.85

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c   = self.canv
        sz  = self.size
        cx  = sz / 2
        cy  = sz * 0.38          # circle centre (raised so inner circle stays above y=0)
        r   = sz * 0.40
        lw  = sz * 0.082
        col = sc_col(self.score)

        # Track: from 0° CCW for 180° → top semicircle (3 o'clock → 9 o'clock)
        track_col = HexColor("#2a2a4e") if self.on_dark else C["surf2"]
        c.setStrokeColor(track_col)
        c.setLineWidth(lw)
        c.arc(cx - r, cy - r, cx + r, cy + r, 0, 180)

        # Score fill: from 180° (9 o'clock) clockwise to proportional point
        fill_deg = self.score / 100 * 180
        c.setStrokeColor(col)
        c.setLineWidth(lw)
        c.arc(cx - r, cy - r, cx + r, cy + r, 180, -fill_deg)

        # Inner donut fill — masks interior of arc, does NOT go below y=0
        inner_r = r - lw * 0.70   # 0.343*sz; cy - inner_r = 0.037*sz > 0
        bg_col  = C["brand"] if self.on_dark else C["white"]
        c.setFillColor(bg_col)
        c.circle(cx, cy, inner_r, fill=1, stroke=0)

        # Score number — baseline placed comfortably above badge
        num_col = C["white"] if self.on_dark else C["ink"]
        c.setFillColor(num_col)
        c.setFont(BD, sz * 0.235)
        c.drawCentredString(cx, cy + sz * 0.048, str(self.score))

        # Grade badge — sits below the number with clear gap
        g   = grade(self.score)
        bw  = sz * 0.28
        bh  = sz * 0.10
        bx  = cx - bw / 2
        by  = cy - bh - sz * 0.035   # clear gap below number baseline
        c.setFillColor(col)
        c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=0)
        c.setFillColor(C["white"])
        c.setFont(BD, sz * 0.068)
        c.drawCentredString(cx, by + bh * 0.26, f"Grade  {g}")

        # Label below badge
        if self.label:
            lab_col = C["subtle"] if self.on_dark else C["muted"]
            c.setFillColor(lab_col)
            c.setFont(R, sz * 0.060)
            c.drawCentredString(cx, by - sz * 0.095, self.label)


class ScoreBar(Flowable):
    """Horizontal labelled score bar."""
    def __init__(self, label, score, color=None):
        super().__init__()
        self.label  = label
        self.score  = max(0, min(100, score))
        self.color  = color or sc_col(score)
        self.width  = CW
        self.height = 26

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c      = self.canv
        lw     = 4.6 * cm          # label column width
        gap    = 0.28 * cm
        sw     = 1.6 * cm          # score text column
        bw     = CW - lw - gap - sw  # bar width
        bh     = 10
        bx     = lw + gap
        by     = (self.height - bh) / 2
        fw     = max(0.0, (self.score / 100) * bw)

        # Label
        c.setFillColor(C["body"])
        c.setFont(R, 9)
        c.drawString(0, by + 1.5, self.label)

        # Track
        c.setFillColor(C["surf2"])
        c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)

        # Fill
        if fw > 6:
            c.setFillColor(self.color)
            c.roundRect(bx, by, fw, bh, 4, fill=1, stroke=0)

        # Score text
        c.setFillColor(self.color)
        c.setFont(BD, 9.5)
        score_x = bx + bw + 0.2 * cm
        c.drawString(score_x, by + 1.5, f"{int(self.score)}/100")


class MetricBox(Flowable):
    """Small metric card: big value + label."""
    def __init__(self, value, label, color=None, w=3.6*cm, h=2.5*cm):
        super().__init__()
        self.value    = str(value)
        self.label    = label
        self.color    = color or C["brand"]
        self.width    = w
        self.height   = h

    def wrap(self, aw, ah):
        # Adapt to actual available width (accounts for table cell padding)
        self.width = min(self.width, aw)
        return self.width, self.height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        # Card
        c.setFillColor(C["surf"])
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        # Top stripe
        c.setFillColor(self.color)
        c.roundRect(0, h - 5, w, 5, 3, fill=1, stroke=0)
        c.rect(0, h - 5, w, 3, fill=1, stroke=0)
        # Value
        c.setFillColor(self.color)
        c.setFont(BD, h * 0.36)
        c.drawCentredString(w / 2, h * 0.38, self.value)
        # Label
        c.setFillColor(C["muted"])
        c.setFont(R, h * 0.13)
        c.drawCentredString(w / 2, h * 0.14, self.label)


# ─── PAGE CALLBACKS ───────────────────────────────────────────────────────────

def on_cover(canvas, doc):
    """Full-bleed dark navy top 56% of cover page."""
    canvas.saveState()
    canvas.setFillColor(C["brand"])
    canvas.rect(0, PH * 0.44, PW, PH * 0.56, fill=1, stroke=0)
    # Accent stripe at the boundary
    canvas.setFillColor(C["accent"])
    canvas.rect(0, PH * 0.44, PW, 3, fill=1, stroke=0)
    canvas.restoreState()


def on_page(brand):
    def _cb(canvas, doc):
        canvas.saveState()
        # Header rule
        canvas.setStrokeColor(C["border"])
        canvas.setLineWidth(0.5)
        canvas.line(MAR, PH - 1.3 * cm, PW - MAR, PH - 1.3 * cm)
        # Header text
        canvas.setFillColor(C["brand"])
        canvas.setFont(SB, 7.5)
        canvas.drawString(MAR, PH - 1.05 * cm, "Marketing Audit Report")
        if brand:
            canvas.setFillColor(C["muted"])
            canvas.setFont(R, 7.5)
            canvas.drawRightString(PW - MAR, PH - 1.05 * cm, brand)
        # Footer rule
        canvas.line(MAR, 1.6 * cm, PW - MAR, 1.6 * cm)
        canvas.setFillColor(C["subtle"])
        canvas.setFont(R, 7)
        canvas.drawString(MAR, 0.9 * cm, "Confidential — prepared for discussion purposes only")
        canvas.drawRightString(PW - MAR, 0.9 * cm, f"Page {doc.page}")
        canvas.restoreState()
    return _cb


# ─── STYLES ───────────────────────────────────────────────────────────────────

def ST():
    def s(nm, fn=R, fs=9.5, col=None, sb=0, sa=6, ld=None, ali=TA_LEFT, li=0, fi=0):
        return ParagraphStyle(nm, fontName=fn, fontSize=fs,
                              textColor=col or C["body"],
                              spaceBefore=sb, spaceAfter=sa,
                              leading=ld or round(fs * 1.4),
                              alignment=ali, leftIndent=li, firstLineIndent=fi)
    return {
        "h1":   s("h1",  BD, 21, C["ink"],   sa=6,  ld=28),
        "h2":   s("h2",  SB, 13, C["brand"], sb=10, sa=4,  ld=18),
        "h3":     s("h3",   SB, 10.5, C["ink"],   sb=6,  sa=3,  ld=15),
        "h4":     s("h4",   SB, 9,   C["muted"], sb=4,  sa=2,  ld=13),
        "body":   s("body", R,  9.5, C["body"],  sa=5,  ld=15, ali=TA_JUSTIFY),
        "sm":     s("sm",   R,  8.5, C["muted"], sa=3,  ld=12),
        "cap":    s("cap",  LI, 7.5, C["subtle"],sa=2,  ld=11),
        "ni":     s("ni",   R,  9.5, C["body"],  sa=4,  ld=15, li=14, fi=-14),
        "exec":   s("exec", R, 10.5, C["body"],  sa=6,  ld=16, ali=TA_JUSTIFY),
        "bullet": s("bul",  R,  9,   C["body"],  sa=2,  ld=13.5, li=16, fi=-10),
        "subhd":  s("shd",  SB, 9.5, C["ink"],   sb=0,  sa=0,  ld=13),
    }


def P(text, style):
    """Render plain text with **bold** → <b>. Escapes HTML."""
    parts = re.split(r'(\*\*[^*\n]{1,400}?\*\*)', str(text))
    out = []
    for part in parts:
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            out.append(f'<b>{esc(part[2:-2])}</b>')
        else:
            out.append(esc(part))
    return Paragraph(''.join(out), style)


def HP(html, style):
    return Paragraph(str(html), style)


def TC(text, bold=False, size=8.5, color=None, align=TA_LEFT):
    fn  = BD if bold else R
    col = color or C["body"]
    st  = ParagraphStyle("_tc", fontName=fn, fontSize=size,
                          textColor=col, leading=round(size * 1.4),
                          spaceAfter=0, spaceBefore=0, alignment=align)
    return P(str(text), st)


# ─── TABLE HELPERS ────────────────────────────────────────────────────────────

def alt_rows(n_data_rows, even_col=None, odd_col=None):
    """Return TableStyle commands for alternating row bg (data rows only, skip header at row 0)."""
    even_col = even_col or C["white"]
    odd_col  = odd_col  or C["surf"]
    cmds = []
    for i in range(1, n_data_rows + 1):
        col = even_col if i % 2 == 1 else odd_col
        cmds.append(("BACKGROUND", (0, i), (-1, i), col))
    return cmds


BASE_TBL = [
    ("BACKGROUND",    (0, 0), (-1, 0),  C["brand"]),
    ("TOPPADDING",    (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING",   (0, 0), (-1, -1), 9),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 9),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("LINEBELOW",     (0, 0), (-1, -1), 0.3, C["border"]),
]


# ─── MARKDOWN PARSERS ─────────────────────────────────────────────────────────

def _section(content, pattern):
    m = re.search(pattern, content, re.IGNORECASE)
    if not m: return ""
    rest = content[m.end():]
    end  = re.search(r'^(?:---+|## )', rest, re.MULTILINE)
    return (rest[:end.start()] if end else rest).strip()


def parse_header(content):
    brand = url = date_str = ""
    score = None

    m = re.search(r'^#\s+Marketing Audit:\s+(.+)$', content, re.MULTILINE)
    if m: brand = m.group(1).strip()

    m = re.search(r'\*\*URL:\*\*\s*(.+)', content)
    if m: url = m.group(1).strip()

    m = re.search(r'\*\*Date:\*\*\s*(.+)', content)
    if m: date_str = m.group(1).strip()

    m = re.search(r'Overall Marketing Score:\s*(\d+)', content)
    if m: score = int(m.group(1))

    if not date_str:
        date_str = datetime.now().strftime("%d %B %Y")

    return brand, url, date_str, score


def parse_score_table(content):
    sec  = _section(content, r'## Score Breakdown')
    rows = []
    for line in sec.splitlines():
        line = line.strip()
        if not line.startswith('|') or re.search(r'[-:]{3}', line): continue
        cols = [c.strip().strip('*') for c in line.split('|') if c.strip()]
        if len(cols) < 2: continue
        if re.search(r'category|score', cols[0], re.I): continue  # header row
        if re.search(r'TOTAL', cols[0], re.I): continue
        num = re.search(r'(\d+)', cols[1]) if len(cols) > 1 else None
        rows.append({
            "name":    cols[0],
            "score":   int(num.group(1)) if num else 50,
            "weight":  cols[2].strip() if len(cols) > 2 else "",
            "finding": cols[4].strip() if len(cols) > 4 else "",
        })
    return rows


def parse_numbered_list(content, pattern):
    sec   = _section(content, pattern)
    items = []
    for m in re.finditer(r'^\d+\.\s+(.+?)(?=^\d+\.|\Z)', sec, re.MULTILINE | re.DOTALL):
        text = re.sub(r'\s+', ' ', m.group(1)).strip()
        items.append(text)
    return items


def parse_exec_summary(content):
    sec   = _section(content, r'## Executive Summary')
    paras = [p.strip() for p in re.split(r'\n\n+', sec) if p.strip()]
    return paras


def parse_detailed_analysis(content):
    secs = []
    for m in re.finditer(
        r'###\s+Category\s+\d+:\s+(.+?)\s+\((\d+)/100\)(.*?)(?=\n#|\Z)',
        content, re.DOTALL
    ):
        secs.append({
            "name":  m.group(1).strip(),
            "score": int(m.group(2)),
            "body":  m.group(3).strip(),
        })
    return secs


# ─── SECTION BUILDERS ─────────────────────────────────────────────────────────

def build_cover(brand, url, date_str, score, exec_paras, st):
    el  = []
    sc  = score or 50

    # Spacer — 3.5cm keeps title in dark zone; gauge (161.5pt) fits fully in dark zone too.
    # Maths (A4): frame_top=827.7pt, dark_boundary=PH*0.44=370.4pt.
    # gauge_bottom = 827.7 - (99.2+152.4+19.8+161.5) = 394.8pt > 370.4 ✓
    el.append(Spacer(1, 3.5 * cm))

    # Title (white on dark)
    def wht(txt, fn, fs, sa=0):
        return HP(f'<font color="#FFFFFF">{esc(txt)}</font>',
                  ParagraphStyle("_cov", fontName=fn, fontSize=fs,
                                 textColor=C["white"], spaceAfter=sa, leading=round(fs*1.25)))

    el.append(wht("Marketing Audit", BD, 34))
    el.append(HP('<font color="#e94560">Report</font>',
                 ParagraphStyle("_cov2", fontName=BD, fontSize=34,
                                textColor=C["accent"], spaceAfter=16, leading=42)))
    if brand:
        el.append(wht(brand, SB, 17, sa=4))
    if url:
        el.append(HP(f'<font color="#64748b">{esc(url)}</font>',
                     ParagraphStyle("_url", fontName=R, fontSize=10,
                                    textColor=HexColor("#64748b"), spaceAfter=3, leading=14)))
    el.append(HP(f'<font color="#475569">{esc(date_str)}</font>',
                 ParagraphStyle("_dt", fontName=R, fontSize=8.5,
                                textColor=HexColor("#475569"), spaceAfter=0, leading=12)))

    el.append(Spacer(1, 0.7 * cm))

    # Score gauge — sits fully inside the dark zone (on_dark=True for correct inner-circle colour)
    gauge = ScoreGauge(sc, size=190, label="Overall Marketing Score", on_dark=True)
    gt    = Table([[gauge]], colWidths=[CW])
    gt.setStyle(TableStyle([
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    el.append(gt)

    # 1.3cm gap pushes the excerpt clearly into the white zone below the accent stripe
    el.append(Spacer(1, 1.3 * cm))

    # Excerpt (first exec para in white zone — dark body text on white background)
    if exec_paras:
        # Take roughly first 2 sentences
        sentences = re.split(r'(?<=\.) ', exec_paras[0])
        excerpt   = ' '.join(sentences[:2])
        el.append(P(excerpt,
                    ParagraphStyle("_ex", fontName=R, fontSize=9,
                                   textColor=C["body"], leading=14, spaceAfter=0,
                                   alignment=TA_JUSTIFY)))

    el.append(Spacer(1, 0.4 * cm))
    el.append(HRule(color=C["border"], height=0.5))
    el.append(NextPageTemplate("content"))
    el.append(PageBreak())
    return el


def build_exec_summary(exec_paras, score, score_rows, st):
    el = []
    sc = score or 50

    el.append(P("Executive Summary", st["h1"]))
    el.append(AccentBar())
    el.append(Spacer(1, 0.45 * cm))

    # 4 metric boxes — mw = CW/4 exactly, zero cell padding so wrap() gets full mw
    mw    = CW / 4
    boxes = [
        MetricBox(str(sc),              "Overall Score",   sc_col(sc), w=mw, h=2.4*cm),
        MetricBox(grade(sc),            "Grade",           sc_col(sc), w=mw, h=2.4*cm),
        MetricBox(str(len(score_rows)), "Categories",      C["brand"],  w=mw, h=2.4*cm),
        MetricBox("6",                  "Priority Actions",C["accent"], w=mw, h=2.4*cm),
    ]
    bt = Table([boxes], colWidths=[mw] * 4)
    bt.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
    ]))
    el.append(bt)
    el.append(Spacer(1, 0.5 * cm))

    for para in exec_paras:
        el.append(P(para, st["exec"]))

    el.append(Spacer(1, 0.3 * cm))
    el.append(HRule())
    el.append(NextPageTemplate("content"))
    el.append(PageBreak())
    return el


def build_scorecard(score_rows, st):
    el = []
    el.append(P("Score Breakdown", st["h1"]))
    el.append(AccentBar())
    el.append(Spacer(1, 0.45 * cm))

    # Score bars
    for i, row in enumerate(score_rows):
        el.append(ScoreBar(row["name"], row["score"], color=CAT_COLS[i % len(CAT_COLS)]))
        el.append(Spacer(1, 0.08 * cm))

    el.append(Spacer(1, 0.4 * cm))

    # Detail table
    hdr  = [TC("Category",    bold=True, size=8, color=C["white"]),
            TC("Score",       bold=True, size=8, color=C["white"], align=TA_CENTER),
            TC("Weight",      bold=True, size=8, color=C["white"], align=TA_CENTER),
            TC("Grade",       bold=True, size=8, color=C["white"], align=TA_CENTER),
            TC("Key Finding", bold=True, size=8, color=C["white"])]
    rows = [hdr]
    for row in score_rows:
        sc  = row["score"]
        col = sc_col(sc)
        rows.append([
            TC(row["name"]),
            TC(f'{sc}/100',    bold=True, color=col, align=TA_CENTER),
            TC(row["weight"],             align=TA_CENTER),
            TC(grade(sc),      bold=True, color=col, align=TA_CENTER),
            TC(row["finding"][:90] if row.get("finding") else "", size=8),
        ])

    cw   = [4.6*cm, 1.7*cm, 1.5*cm, 1.4*cm, CW - 9.2*cm]
    tbl  = Table(rows, colWidths=cw, repeatRows=1)
    cmds = BASE_TBL[:] + alt_rows(len(score_rows))
    tbl.setStyle(TableStyle(cmds))
    el.append(tbl)

    el.append(Spacer(1, 0.3 * cm))
    el.append(HRule())
    el.append(NextPageTemplate("content"))
    el.append(PageBreak())
    return el


def _action_table(number, text, color, bg):
    """Renders a single action item as a reliable Table (auto-wraps text)."""
    # Isolate the bold 'title' part (up to first '. ') from the body
    m = re.match(r'^(.+?\.) (.*)', text, re.DOTALL)
    if m and len(m.group(1)) < 120:
        title, rest = m.group(1).strip(), m.group(2).strip()
        cell_content = HP(
            f'<b>{esc(title)}</b> {esc(rest)}',
            ParagraphStyle("_ai", fontName=R, fontSize=9, textColor=C["body"],
                           leading=14, spaceAfter=0)
        )
    else:
        cell_content = P(text, ParagraphStyle("_ai", fontName=R, fontSize=9,
                                               textColor=C["body"], leading=14, spaceAfter=0))

    num_cell  = HP(
        f'<font color="#FFFFFF"><b>{number}</b></font>',
        ParagraphStyle("_num", fontName=BD, fontSize=9.5,
                       textColor=C["white"], alignment=TA_CENTER,
                       leading=14, spaceAfter=0)
    )

    num_w  = 1.5 * cm
    text_w = CW - num_w

    tbl = Table([[num_cell, cell_content]], colWidths=[num_w, text_w])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0),   color),
        ("BACKGROUND",    (1, 0), (1, 0),   bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (0, 0),   6),
        ("RIGHTPADDING",  (0, 0), (0, 0),   6),
        ("LEFTPADDING",   (1, 0), (1, 0),   12),
        ("RIGHTPADDING",  (1, 0), (1, 0),   10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def _section_hdr(title, color):
    row = [HP(f'<font color="#FFFFFF"><b>{esc(title)}</b></font>',
              ParagraphStyle("_sh", fontName=BD, fontSize=10.5,
                             textColor=C["white"], leading=14, spaceAfter=0))]
    t = Table([row], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), color),
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
    ]))
    return t


def build_action_plan(quick_wins, strategic, longterm, st):
    el = []
    el.append(P("Integrated Action Plan", st["h1"]))
    el.append(AccentBar())
    el.append(Spacer(1, 0.45 * cm))

    first_tier = [True]
    def tier(title, items, color, bg):
        if not items: return
        if not first_tier[0]:
            el.append(PageBreak())
        first_tier[0] = False
        el.append(_section_hdr(title, color))
        el.append(Spacer(1, 0.2 * cm))
        for i, item in enumerate(items, 1):
            el.append(_action_table(i, item, color, bg))
            el.append(Spacer(1, 0.15 * cm))
        el.append(Spacer(1, 0.3 * cm))

    tier("Quick Wins — This Week",        quick_wins, C["ok"],   C["ok_bg"])
    tier("Strategic — This Month",        strategic,  C["info"], C["info_bg"])
    tier("Long-Term — This Quarter+",     longterm,   C["vio"],  C["vio_bg"])

    el.append(HRule())
    el.append(NextPageTemplate("content"))
    el.append(PageBreak())
    return el


def _cat_subheading(text, col):
    """Styled sub-heading: light tinted background, left colour accent, bold label."""
    bar_w  = 4
    text_w = CW - bar_w
    tbl = Table(
        [[None,
          P(f"**{text}**",
            ParagraphStyle("_sh", fontName=SB, fontSize=9.5,
                           textColor=C["ink"], leading=13, spaceAfter=0, spaceBefore=0))]],
        colWidths=[bar_w, text_w]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0),   col),
        ("BACKGROUND",    (1, 0), (1, 0),   C["surf"]),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (0, 0),   0),
        ("RIGHTPADDING",  (0, 0), (0, 0),   0),
        ("LEFTPADDING",   (1, 0), (1, 0),   10),
        ("RIGHTPADDING",  (1, 0), (1, 0),   10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def _render_cat_body(body, el, st, col):
    """
    Parse category body text and render with proper structure.
    Handles three line patterns per block:
      • **Bold Heading:** [optional inline text]
        [optional continuation lines — could be plain text or '- bullets']
      • - bullet item (pure bullet block)
      • plain paragraph
    """
    # Split on blank lines for major paragraph groups
    for block in re.split(r'\n\n+', body.strip()):
        block = block.strip()
        if not block: continue
        # Skip dividers, markdown table rows, heading lines, italic footers
        if re.match(r'^-{2,}$', block): continue
        if block.startswith('|'): continue
        if block.startswith('#'): continue
        if block.startswith('*Generated') or block.startswith('*Audit'): continue

        lines = block.splitlines()
        first = lines[0].strip()

        # ── Bold sub-heading line ──────────────────────────────────────────────
        bm = re.match(r'^\*\*(.+?)\*\*[:\s]*(.*)', first)
        if bm:
            heading   = bm.group(1).strip()
            inline    = bm.group(2).strip()   # text on same line as heading
            rest_lines = [ln.strip() for ln in lines[1:] if ln.strip()]

            el.append(Spacer(1, 0.12 * cm))
            el.append(_cat_subheading(heading, col))
            el.append(Spacer(1, 0.1 * cm))

            # Collect what follows the heading: inline text + rest_lines
            # They can be plain prose lines or '- bullet' lines, interleaved.
            all_rest = []
            if inline:
                all_rest.append(inline)
            all_rest.extend(rest_lines)

            para_buf  = []
            for ln in all_rest:
                if ln.startswith('- '):
                    if para_buf:
                        el.append(P(' '.join(para_buf), st["body"]))
                        para_buf = []
                    el.append(P(f"• {ln[2:]}", st["bullet"]))
                else:
                    para_buf.append(ln)
            if para_buf:
                el.append(P(' '.join(para_buf), st["body"]))
            continue

        # ── Pure bullet block ─────────────────────────────────────────────────
        if all(ln.strip().startswith('- ') or not ln.strip() for ln in lines):
            for ln in lines:
                ln = ln.strip()
                if ln.startswith('- '):
                    el.append(P(f"• {ln[2:]}", st["bullet"]))
            continue

        # ── Plain paragraph ───────────────────────────────────────────────────
        el.append(P(re.sub(r'\s+', ' ', block), st["body"]))


def build_detailed_analysis(secs, st):
    el = []
    el.append(P("Detailed Analysis by Category", st["h1"]))
    el.append(AccentBar())
    el.append(Spacer(1, 0.45 * cm))

    for i, sec in enumerate(secs):
        sc  = sec["score"]
        col = CAT_COLS[i % len(CAT_COLS)]
        g   = grade(sc)

        # Each category on its own page (except the first which follows the section title)
        if i > 0:
            el.append(PageBreak())

        # Category header banner
        hdr_t = Table([[
            HP(f'<font color="#FFFFFF"><b>{esc(sec["name"])}</b></font>',
               ParagraphStyle("_ch", fontName=BD, fontSize=11.5,
                              textColor=C["white"], leading=16, spaceAfter=0)),
            HP(f'<font color="#CBD5E1">{sc}/100 - Grade {g}</font>',
               ParagraphStyle("_cs", fontName=SB, fontSize=10.5,
                              textColor=HexColor("#CBD5E1"), leading=16,
                              spaceAfter=0, alignment=TA_RIGHT)),
        ]], colWidths=[CW * 0.60, CW * 0.40])
        hdr_t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), col),
            ("TOPPADDING",    (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
            ("LEFTPADDING",   (0, 0), (-1, -1), 14),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        el.append(KeepTogether([hdr_t, Spacer(1, 0.3 * cm)]))

        _render_cat_body(sec["body"], el, st, col)

    el.append(NextPageTemplate("content"))
    el.append(PageBreak())
    return el


def build_methodology(st):
    el = []
    el.append(P("Methodology & Scoring", st["h1"]))
    el.append(AccentBar())
    el.append(Spacer(1, 0.45 * cm))

    el.append(P(
        "This marketing audit evaluates digital effectiveness across six weighted dimensions. "
        "Scores are derived entirely from publicly observable signals - website content, search "
        "engine presence, conversion architecture, review platforms, and competitive context. "
        "No access to internal analytics, CRM, or paid advertising data was used.",
        st["body"]
    ))
    el.append(Spacer(1, 0.4 * cm))

    # Methodology table
    meth = [
        ("Content & Messaging",     "25%", "Headline clarity, value proposition, copy quality, social proof, brand voice consistency"),
        ("Conversion Optimisation", "20%", "CTA effectiveness, form friction, trust signals, pricing transparency, urgency mechanisms"),
        ("SEO & Discoverability",   "20%", "Title tags, meta descriptions, schema markup, internal linking, content depth and freshness"),
        ("Competitive Positioning", "15%", "Differentiation clarity, competitor comparison content, awards evidence, market reputation"),
        ("Brand & Trust",           "10%", "Review ratings, response management, design quality, about page depth, contact accessibility"),
        ("Growth & Strategy",       "10%", "Email capture, lead magnets, remarketing signals, audience diversification, loyalty mechanics"),
    ]
    hdr  = [TC("Category",       bold=True, size=8, color=C["white"]),
            TC("Weight",         bold=True, size=8, color=C["white"], align=TA_CENTER),
            TC("What We Measure",bold=True, size=8, color=C["white"])]
    rows = [hdr] + [[TC(n), TC(w, align=TA_CENTER), TC(m, size=8)] for n, w, m in meth]
    cw   = [4.6 * cm, 1.6 * cm, CW - 6.2 * cm]
    tbl  = Table(rows, colWidths=cw, repeatRows=1)
    cmds = BASE_TBL[:] + alt_rows(len(meth))
    tbl.setStyle(TableStyle(cmds))
    el.append(tbl)
    el.append(Spacer(1, 0.5 * cm))

    # Grade key
    el.append(P("Score Interpretation", st["h3"]))
    el.append(Spacer(1, 0.2 * cm))
    grades = [
        ("85-100", "A / A+", C["ok"],   "Excellent - performing strongly, minor optimisations only"),
        ("70-84",  "B",      C["info"], "Good - clear improvement opportunities exist"),
        ("55-69",  "C",      C["warn"], "Average - significant gaps requiring planned attention"),
        ("40-54",  "D",      C["err"],  "Below average - major overhaul needed"),
        ("0-39",   "F",      C["err"],  "Critical - fundamental issues impacting performance"),
    ]
    ghdr = [TC("Range", bold=True, size=8, color=C["white"]),
            TC("Grade", bold=True, size=8, color=C["white"], align=TA_CENTER),
            TC("Interpretation", bold=True, size=8, color=C["white"])]
    grows = [ghdr]
    for rng, g, col, interp in grades:
        grows.append([TC(rng), TC(g, bold=True, color=col, align=TA_CENTER), TC(interp)])
    gcw  = [2.0 * cm, 2.0 * cm, CW - 4.0 * cm]
    gtbl = Table(grows, colWidths=gcw, repeatRows=1)
    gcmds = BASE_TBL[:] + alt_rows(len(grades))
    gtbl.setStyle(TableStyle(gcmds))
    el.append(gtbl)

    el.append(Spacer(1, 0.5 * cm))
    el.append(HRule())
    el.append(Spacer(1, 0.3 * cm))
    el.append(P(
        "DISCLAIMER: All findings are based on publicly observable signals at time of audit. "
        "This report is prepared for discussion purposes and does not constitute legal or "
        "professional advice. AI-assisted analysis — findings should be validated before action.",
        st["cap"]
    ))
    return el


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

def generate(source, output=None):
    if os.path.isdir(source):
        md_path  = os.path.join(source, "MARKETING-AUDIT.md")
        output   = output or os.path.join(source, "MARKETING-AUDIT.pdf")
    else:
        md_path  = source
        output   = output or os.path.splitext(source)[0] + ".pdf"

    if not os.path.exists(md_path):
        print(f"ERROR: Not found: {md_path}")
        sys.exit(1)

    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    brand, url, date_str, score = parse_header(content)
    exec_paras   = parse_exec_summary(content)
    score_rows   = parse_score_table(content)
    quick_wins   = parse_numbered_list(content, r'## Quick Wins')
    strategic    = parse_numbered_list(content, r'## Strategic Recommendations')
    longterm     = parse_numbered_list(content, r'## Long.Term Initiatives')
    analysis     = parse_detailed_analysis(content)

    brand = brand or "Marketing Audit"
    sc    = score or 62

    print(f"Reading:  {md_path}")
    print(f"Fonts:    {R} / {BD}")
    print(f"Brand:    {brand}  |  Score: {sc}/100  |  Categories: {len(score_rows)}")
    print(f"Actions:  {len(quick_wins)} quick, {len(strategic)} strategic, {len(longterm)} long-term")

    st = ST()

    doc = BaseDocTemplate(
        output, pagesize=A4,
        leftMargin=MAR, rightMargin=MAR,
        topMargin=2.0 * cm, bottomMargin=2.0 * cm,
        title=f"Marketing Audit — {brand}",
    )

    cover_f = Frame(MAR, 0, CW, PH - 0.5 * cm, id="cover", showBoundary=0)
    body_f  = Frame(MAR, 2.0 * cm, CW, PH - 4.6 * cm, id="body",  showBoundary=0)

    doc.addPageTemplates([
        PageTemplate(id="cover",   frames=[cover_f], onPage=on_cover),
        PageTemplate(id="content", frames=[body_f],  onPage=on_page(brand)),
    ])

    story = []
    print("  cover...")
    story += build_cover(brand, url, date_str, sc, exec_paras, st)
    print("  exec summary...")
    story += build_exec_summary(exec_paras, sc, score_rows, st)
    print("  scorecard...")
    story += build_scorecard(score_rows, st)
    print("  action plan...")
    story += build_action_plan(quick_wins, strategic, longterm, st)
    print("  detailed analysis...")
    story += build_detailed_analysis(analysis, st)
    print("  methodology...")
    story += build_methodology(st)

    print("Rendering...")
    doc.build(story)

    kb = os.path.getsize(output) // 1024
    print(f"\nDone: {output} ({kb} KB)")
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py generate_pdf_report.py <folder-or-md-file> [output.pdf]")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
