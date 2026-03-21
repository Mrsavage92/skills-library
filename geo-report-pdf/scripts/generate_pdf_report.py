#!/usr/bin/env python3
"""
GEO Audit — Enterprise PDF Report Generator
Reads GEO-AUDIT-REPORT.md and produces a premium, client-ready A4 PDF.
Usage: py generate_pdf_report.py "C:\\path\\to\\audit\\folder"
       py generate_pdf_report.py "C:\\path\\to\\GEO-AUDIT-REPORT.md"
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

# --- FONTS ---

_FONT_MAP = [
    ("Seg",    "C:/Windows/Fonts/segoeui.ttf"),
    ("Seg-Sb", "C:/Windows/Fonts/seguisb.ttf"),
    ("Seg-Bd", "C:/Windows/Fonts/segoeuib.ttf"),
    ("Seg-Li", "C:/Windows/Fonts/segoeuil.ttf"),
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

# --- LAYOUT ---

PW, PH = A4
MAR    = 1.8 * cm
CW     = PW - 2 * MAR

# --- COLOURS ---

ACCENT = HexColor("#059669")   # green

C = {
    "brand":   HexColor("#1a1a2e"),
    "brand2":  HexColor("#16213e"),
    "accent":  ACCENT,
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
}

TIER_COL = {
    "CRITICAL": (HexColor("#dc2626"), HexColor("#fef2f2")),
    "HIGH":     (HexColor("#d97706"), HexColor("#fffbeb")),
    "MEDIUM":   (HexColor("#2563eb"), HexColor("#eff6ff")),
    "LOW":      (HexColor("#64748b"), HexColor("#f8fafc")),
}

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

# --- FLOWABLES ---

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
    def __init__(self, score, size=180, label="", on_dark=False):
        super().__init__()
        self.score   = max(0, min(100, int(score)))
        self.size    = size
        self.label   = label
        self.on_dark = on_dark
        self.width   = size
        self.height  = size * 0.85

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c   = self.canv
        sz  = self.size
        cx  = sz / 2
        cy  = sz * 0.38
        r   = sz * 0.40
        lw  = sz * 0.082
        col = sc_col(self.score)

        track_col = HexColor("#2a2a4e") if self.on_dark else C["surf2"]
        c.setStrokeColor(track_col)
        c.setLineWidth(lw)
        c.arc(cx - r, cy - r, cx + r, cy + r, 0, 180)

        fill_deg = self.score / 100 * 180
        c.setStrokeColor(col)
        c.setLineWidth(lw)
        c.arc(cx - r, cy - r, cx + r, cy + r, 180, -fill_deg)

        inner_r = r - lw * 0.70
        bg_col  = C["brand"] if self.on_dark else C["white"]
        c.setFillColor(bg_col)
        c.circle(cx, cy, inner_r, fill=1, stroke=0)

        num_col = C["white"] if self.on_dark else C["ink"]
        c.setFillColor(num_col)
        c.setFont(BD, sz * 0.235)
        c.drawCentredString(cx, cy + sz * 0.048, str(self.score))

        g   = grade(self.score)
        bw  = sz * 0.28
        bh  = sz * 0.10
        bx  = cx - bw / 2
        by  = cy - bh - sz * 0.035
        c.setFillColor(col)
        c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=0)
        c.setFillColor(C["white"])
        c.setFont(BD, sz * 0.068)
        c.drawCentredString(cx, by + bh * 0.26, f"Grade  {g}")

        if self.label:
            lab_col = C["subtle"] if self.on_dark else C["muted"]
            c.setFillColor(lab_col)
            c.setFont(R, sz * 0.060)
            c.drawCentredString(cx, by - sz * 0.095, self.label)


class ScoreBar(Flowable):
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
        c   = self.canv
        lw  = 4.6 * cm
        gap = 0.28 * cm
        sw  = 1.6 * cm
        bw  = CW - lw - gap - sw
        bh  = 10
        bx  = lw + gap
        by  = (self.height - bh) / 2
        fw  = max(0.0, (self.score / 100) * bw)

        c.setFillColor(C["body"])
        c.setFont(R, 9)
        c.drawString(0, by + 1.5, self.label)

        c.setFillColor(C["surf2"])
        c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)

        if fw > 6:
            c.setFillColor(self.color)
            c.roundRect(bx, by, fw, bh, 4, fill=1, stroke=0)

        c.setFillColor(self.color)
        c.setFont(BD, 9.5)
        c.drawString(bx + bw + 0.2 * cm, by + 1.5, f"{int(self.score)}/100")


class MetricBox(Flowable):
    def __init__(self, value, label, color=None, w=3.6*cm, h=2.5*cm):
        super().__init__()
        self.value  = str(value)
        self.label  = label
        self.color  = color or C["brand"]
        self.width  = w
        self.height = h

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return self.width, self.height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(C["surf"])
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, h - 5, w, 5, 3, fill=1, stroke=0)
        c.rect(0, h - 5, w, 3, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.setFont(BD, h * 0.36)
        c.drawCentredString(w / 2, h * 0.38, self.value)
        c.setFillColor(C["muted"])
        c.setFont(R, h * 0.13)
        c.drawCentredString(w / 2, h * 0.14, self.label)


# --- PAGE CALLBACKS ---

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C["brand"])
    canvas.rect(0, PH * 0.44, PW, PH * 0.56, fill=1, stroke=0)
    canvas.setFillColor(C["accent"])
    canvas.rect(0, PH * 0.44, PW, 3, fill=1, stroke=0)
    canvas.restoreState()


def on_page(brand):
    def _cb(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(C["border"])
        canvas.setLineWidth(0.5)
        canvas.line(MAR, PH - 1.3 * cm, PW - MAR, PH - 1.3 * cm)
        canvas.setFillColor(C["brand"])
        canvas.setFont(SB, 7.5)
        canvas.drawString(MAR, PH - 1.05 * cm, "GEO Audit Report")
        if brand:
            canvas.setFillColor(C["muted"])
            canvas.setFont(R, 7.5)
            canvas.drawRightString(PW - MAR, PH - 1.05 * cm, brand)
        canvas.line(MAR, 1.6 * cm, PW - MAR, 1.6 * cm)
        canvas.setFillColor(C["subtle"])
        canvas.setFont(R, 7)
        canvas.drawString(MAR, 0.9 * cm, "Confidential - prepared for discussion purposes only")
        canvas.drawRightString(PW - MAR, 0.9 * cm, f"Page {doc.page}")
        canvas.restoreState()
    return _cb


# --- STYLES ---

def ST():
    def s(nm, fn=R, fs=9.5, col=None, sb=0, sa=6, ld=None, ali=TA_LEFT, li=0, fi=0):
        return ParagraphStyle(nm, fontName=fn, fontSize=fs,
                              textColor=col or C["body"],
                              spaceBefore=sb, spaceAfter=sa,
                              leading=ld or round(fs * 1.4),
                              alignment=ali, leftIndent=li, firstLineIndent=fi)
    return {
        "h1":     s("h1",  BD, 21, C["ink"],    sa=6,  ld=28),
        "h2":     s("h2",  SB, 13, C["brand"],  sb=10, sa=4,  ld=18),
        "h3":     s("h3",  SB, 10.5, C["ink"],  sb=6,  sa=3,  ld=15),
        "h4":     s("h4",  SB, 9,   C["muted"], sb=4,  sa=2,  ld=13),
        "body":   s("body",R,  9.5, C["body"],  sa=5,  ld=15, ali=TA_JUSTIFY),
        "sm":     s("sm",  R,  8.5, C["muted"], sa=3,  ld=12),
        "cap":    s("cap", LI, 7.5, C["subtle"],sa=2,  ld=11),
        "ni":     s("ni",  R,  9.5, C["body"],  sa=4,  ld=15, li=14, fi=-14),
        "exec":   s("exec",R, 10.5, C["body"],  sa=6,  ld=16, ali=TA_JUSTIFY),
        "bullet": s("bul", R,  9,   C["body"],  sa=2,  ld=13.5, li=16, fi=-10),
        "subhd":  s("shd", SB, 9.5, C["ink"],   sb=0,  sa=0,  ld=13),
    }


def P(text, style):
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


# --- TABLE HELPERS ---

def alt_rows(n_data_rows, even_col=None, odd_col=None):
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


# --- PARSERS ---

def read_md(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def find_md(folder_or_file):
    p = folder_or_file.strip().strip('"')
    if os.path.isfile(p):
        return p
    for name in ["GEO-AUDIT-REPORT.md", "geo-audit-report.md",
                 "GEO-AUDIT.md", "geo-audit.md"]:
        candidate = os.path.join(p, name)
        if os.path.isfile(candidate):
            return candidate
    for fn in os.listdir(p):
        if fn.upper().endswith(".MD"):
            return os.path.join(p, fn)
    raise FileNotFoundError(f"No markdown audit file found in: {p}")

def parse_meta(content):
    brand = ""
    m = re.search(r'# GEO Audit Report[:\s]+(.+)', content, re.IGNORECASE)
    if m:
        brand = m.group(1).strip()
    date_str = datetime.now().strftime("%B %d, %Y")
    dm = re.search(r'\*\*Audit Date:\*\*\s*(.+)', content)
    if dm:
        date_str = dm.group(1).strip()
    score = 50
    sm = re.search(r'Overall GEO Score:\s*(\d+)/100', content, re.IGNORECASE)
    if sm:
        score = int(sm.group(1))
    url = ""
    um = re.search(r'\*\*URL:\*\*\s*(.+)', content)
    if um:
        url = um.group(1).strip()
    return brand, date_str, score, url

def parse_section(content, heading):
    m = re.search(rf'^##\s+{re.escape(heading)}', content, re.MULTILINE | re.IGNORECASE)
    if not m:
        return ""
    rest = content[m.end():]
    end  = re.search(r'^##\s', rest, re.MULTILINE)
    return (rest[:end.start()] if end else rest).strip()

def parse_exec_summary(content):
    return parse_section(content, "Executive Summary")

def parse_score_table(content):
    """Parse ### Score Breakdown table (inside exec summary section)."""
    m = re.search(r'###\s+Score Breakdown', content, re.IGNORECASE)
    if not m:
        m = re.search(r'##\s+Score Breakdown', content, re.IGNORECASE)
    if not m:
        return []
    rest = content[m.end():]
    end  = re.search(r'^#{1,3}\s', rest, re.MULTILINE)
    section = rest[:end.start()] if end else rest
    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line or line.startswith("|---") or "---" in line:
            continue
        if "Overall GEO Score" in line:
            continue
        if line.startswith("|"):
            cols = [c.strip() for c in line.strip("|").split("|")]
            rows.append(cols)
    return rows

def parse_score_cats(content):
    rows = parse_score_table(content)
    cats = []
    if not rows:
        return cats
    for row in rows[1:]:
        if len(row) < 2:
            continue
        name = re.sub(r'\*+', '', row[0]).strip()
        if not name:
            continue
        score_str = row[1].strip() if len(row) > 1 else "50"
        sm = re.search(r'(\d+)', score_str)
        score = int(sm.group(1)) if sm else 50
        cats.append({"name": name, "score": score})
    return cats

def parse_priority_issues(content):
    """Parse H1/H2/H3.., M1/M2.., L1/L2.. priority issues."""
    issues = {"HIGH": [], "MEDIUM": [], "LOW": []}

    # High priority
    m = re.search(r'## High Priority Issues', content, re.IGNORECASE)
    if m:
        rest = content[m.end():]
        end  = re.search(r'^## [^#]', rest, re.MULTILINE)
        section = rest[:end.start()] if end else rest
        for im in re.finditer(
            r'###\s+H\d+\s*[-\u2014]\s*(.+?)\n(.*?)(?=\n###|\Z)',
            section, re.DOTALL
        ):
            issues["HIGH"].append({"title": im.group(1).strip(), "body": im.group(2).strip()})

    # Medium priority
    m = re.search(r'## Medium Priority Issues', content, re.IGNORECASE)
    if m:
        rest = content[m.end():]
        end  = re.search(r'^## [^#]', rest, re.MULTILINE)
        section = rest[:end.start()] if end else rest
        for im in re.finditer(
            r'###\s+M\d+\s*[-\u2014]\s*(.+?)\n(.*?)(?=\n###|\Z)',
            section, re.DOTALL
        ):
            issues["MEDIUM"].append({"title": im.group(1).strip(), "body": im.group(2).strip()})

    # Low priority
    m = re.search(r'## Low Priority Issues', content, re.IGNORECASE)
    if m:
        rest = content[m.end():]
        end  = re.search(r'^## [^#]', rest, re.MULTILINE)
        section = rest[:end.start()] if end else rest
        for im in re.finditer(
            r'###\s+L\d+\s*[-\u2014]\s*(.+?)\n(.*?)(?=\n###|\Z)',
            section, re.DOTALL
        ):
            issues["LOW"].append({"title": im.group(1).strip(), "body": im.group(2).strip()})

    # Critical (if present)
    issues["CRITICAL"] = []
    m = re.search(r'## Critical Issues', content, re.IGNORECASE)
    if m:
        rest = content[m.end():]
        end  = re.search(r'^## [^#]', rest, re.MULTILINE)
        section = rest[:end.start()] if end else rest
        # Check it's not just "None identified"
        if re.search(r'###\s+', section):
            for im in re.finditer(
                r'###\s+C\d*\s*[-\u2014]?\s*(.+?)\n(.*?)(?=\n###|\Z)',
                section, re.DOTALL
            ):
                issues["CRITICAL"].append({"title": im.group(1).strip(), "body": im.group(2).strip()})

    return issues

def parse_category_deep_dives(content):
    """Parse Category Deep Dives section."""
    m = re.search(r'## Category Deep Dives', content, re.IGNORECASE)
    if not m:
        return []
    rest = content[m.end():]
    end  = re.search(r'^## [^#]', rest, re.MULTILINE)
    section = rest[:end.start()] if end else rest

    cats = []
    for cm2 in re.finditer(
        r'###\s+(.+?)\s*[-\u2014]\s*(\d+)/100\n(.*?)(?=\n###|\Z)',
        section, re.DOTALL
    ):
        cats.append({
            "name":  cm2.group(1).strip(),
            "score": int(cm2.group(2)),
            "body":  cm2.group(3).strip(),
        })
    return cats

def parse_quick_wins(content):
    """Parse Quick Wins and 30-Day Action Plan."""
    wins = []
    for heading in ["Quick Wins", "30-Day Action Plan", "30 Day Action Plan"]:
        section = parse_section(content, heading)
        if section:
            for line in section.splitlines():
                line = line.strip()
                m = re.match(r'^\d+\.\s+(.+)', line)
                if m:
                    wins.append(m.group(1).strip())
            if wins:
                break
    return wins


# --- SECTION BUILDERS ---

def build_cover(el, st, brand, date_str, score, url, exec_txt):
    el.append(Spacer(1, 3.5 * cm))

    def wht(txt, fn, fs, sa=0):
        return HP(f'<font color="#FFFFFF">{esc(txt)}</font>',
                  ParagraphStyle("_cov", fontName=fn, fontSize=fs,
                                 textColor=C["white"], spaceAfter=sa, leading=round(fs*1.25)))

    el.append(wht("GEO Audit", BD, 34))
    el.append(HP(f'<font color="{C["accent"].hexval()}">Report</font>',
                 ParagraphStyle("_cov2", fontName=BD, fontSize=34,
                                textColor=C["accent"], spaceAfter=8, leading=42)))
    el.append(HP('<font color="#94a3b8">Generative Engine Optimisation</font>',
                 ParagraphStyle("_cs", fontName=R, fontSize=11, textColor=HexColor("#94a3b8"),
                                leading=15, spaceAfter=8)))
    if brand:
        el.append(wht(brand, SB, 17, sa=4))
    el.append(HP(f'<font color="#475569">{esc(date_str)}</font>',
                 ParagraphStyle("_dt", fontName=R, fontSize=8.5,
                                textColor=HexColor("#475569"), spaceAfter=0, leading=12)))

    el.append(Spacer(1, 0.7 * cm))

    gauge = ScoreGauge(score, size=190, label="Overall GEO Score", on_dark=True)
    gt = Table([[gauge]], colWidths=[CW])
    gt.setStyle(TableStyle([
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    el.append(gt)

    el.append(Spacer(1, 1.3 * cm))

    if exec_txt:
        excerpt = ''
        for chunk in exec_txt.split("\n\n"):
            chunk = chunk.strip()
            if not chunk or chunk.startswith('#') or chunk.startswith('|') or chunk.startswith('**Overall') or chunk.startswith('>') or re.match(r'^\*\*.*Score.*\*\*', chunk):
                continue
            sentences = re.split(r'(?<=\.) ', chunk)
            excerpt = ' '.join(sentences[:2])
            break
        el.append(P(excerpt, ParagraphStyle("_ex", fontName=R, fontSize=9,
                                            textColor=C["body"], leading=14, spaceAfter=0,
                                            alignment=TA_JUSTIFY)))

    el.append(Spacer(1, 0.4 * cm))
    el.append(HRule(color=C["border"], height=0.5))


def build_exec(el, st, content):
    el.append(HP(f'<font color="{C["accent"].hexval()}">EXECUTIVE SUMMARY</font>', st["cap"]))
    el.append(HP('<font size="21"><b>Overview</b></font>',
                 ParagraphStyle("es_h", fontName=BD, fontSize=21, textColor=C["ink"],
                                leading=28, spaceAfter=10)))
    el.append(AccentBar(height=3))
    el.append(Spacer(1, 0.35 * cm))
    for para in content.split("\n\n"):
        para = para.strip()
        if not para or para.startswith("#"):
            continue
        # Skip the score breakdown table lines
        if para.startswith("|") or "Score Breakdown" in para:
            continue
        el.append(P(para, st["exec"]))


def build_score_overview(el, st, cats, score_rows):
    el.append(PageBreak())
    el.append(HP(f'<font color="{C["accent"].hexval()}">SCORE BREAKDOWN</font>', st["cap"]))
    el.append(HP('<font size="21"><b>Category Scores</b></font>',
                 ParagraphStyle("so_h", fontName=BD, fontSize=21, textColor=C["ink"],
                                leading=28, spaceAfter=10)))
    el.append(AccentBar(height=3))
    el.append(Spacer(1, 0.4 * cm))

    for cat in cats:
        el.append(ScoreBar(cat["name"], cat["score"], color=sc_col(cat["score"])))

    el.append(Spacer(1, 0.5 * cm))

    if score_rows and len(score_rows) > 1:
        n_cols = len(score_rows[0])
        tdata = []
        for i, row in enumerate(score_rows):
            padded = (row + [""] * n_cols)[:n_cols]
            bold = (i == 0)
            tdata.append([TC(c, bold=bold, size=8, color=(C["white"] if bold else None))
                          for c in padded])
        col_w = CW / n_cols
        cmds = list(BASE_TBL) + alt_rows(len(tdata) - 1)
        t = Table(tdata, colWidths=[col_w] * n_cols)
        t.setStyle(TableStyle(cmds))
        el.append(t)


def _issue_block(issue, tier, el, st):
    fg, bg = TIER_COL.get(tier, (C["info"], C["surf"]))
    badge = HP(f'<font color="{fg.hexval()}" size="7.5"><b>{tier}</b></font>',
               ParagraphStyle("_b", fontName=BD, fontSize=7.5, textColor=fg,
                              leading=11, spaceAfter=0, spaceBefore=0))
    title = P(issue["title"], ParagraphStyle("_t", fontName=SB, fontSize=10,
                                              textColor=C["ink"], leading=14,
                                              spaceAfter=0, spaceBefore=0))
    hdr_row = Table([[badge, title]], colWidths=[2.0 * cm, CW - 2.0 * cm])
    hdr_row.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0),  bg),
        ("BACKGROUND",    (1, 0), (1, 0),  C["surf"]),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 9),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 9),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))

    body_paras = []
    for para in issue["body"].split("\n\n"):
        para = para.strip()
        if para and not para.startswith("#"):
            body_paras.append(P(para, st["body"]))

    block_items = [hdr_row]
    if body_paras:
        body_inner = Table([[p] for p in body_paras], colWidths=[CW])
        body_inner.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C["white"]),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 9),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 9),
            ("LINEBELOW",     (0, -1), (-1, -1), 0.5, C["border"]),
        ]))
        block_items.append(body_inner)
    el.append(KeepTogether(block_items))
    el.append(Spacer(1, 0.25 * cm))


def build_priority_issues(el, st, issues):
    has_any = any(issues.get(t) for t in ["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    if not has_any:
        return

    el.append(PageBreak())
    el.append(HP(f'<font color="{C["accent"].hexval()}">PRIORITY ISSUES</font>', st["cap"]))
    el.append(HP('<font size="21"><b>Issues by Priority</b></font>',
                 ParagraphStyle("pi_h", fontName=BD, fontSize=21, textColor=C["ink"],
                                leading=28, spaceAfter=10)))
    el.append(AccentBar(height=3))
    el.append(Spacer(1, 0.4 * cm))

    tier_labels = {
        "CRITICAL": ("Critical Issues",       C["err"]),
        "HIGH":     ("High Priority Issues",   C["warn"]),
        "MEDIUM":   ("Medium Priority Issues", C["info"]),
        "LOW":      ("Low Priority Issues",    C["muted"]),
    }

    first = [True]
    for tier in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        tier_issues = issues.get(tier, [])
        if not tier_issues:
            continue
        label, col = tier_labels[tier]
        if not first[0]:
            el.append(Spacer(1, 0.3 * cm))
        first[0] = False
        el.append(AccentBar(height=2, color=col))
        el.append(HP(f'<font color="{col.hexval()}"><b>{label}</b></font>',
                     ParagraphStyle(f"tl_{tier}", fontName=SB, fontSize=11, textColor=col,
                                    leading=15, spaceAfter=6, spaceBefore=8)))
        for issue in tier_issues:
            _issue_block(issue, tier, el, st)


def build_category_deep_dives(el, st, cats):
    if not cats:
        return
    el.append(PageBreak())
    el.append(HP(f'<font color="{C["accent"].hexval()}">CATEGORY ANALYSIS</font>', st["cap"]))
    el.append(HP('<font size="21"><b>Category Deep Dives</b></font>',
                 ParagraphStyle("dd_h", fontName=BD, fontSize=21, textColor=C["ink"],
                                leading=28, spaceAfter=10)))
    el.append(AccentBar(height=3))

    for i, cat in enumerate(cats):
        if i > 0:
            el.append(PageBreak())
        sc  = cat["score"]
        col = sc_col(sc)

        name_txt = HP(f'<b>{esc(cat["name"])}</b>',
                      ParagraphStyle("_cn", fontName=BD, fontSize=12, textColor=C["ink"],
                                     leading=16, spaceAfter=0, spaceBefore=0))
        badge_txt = HP(
            f'<font color="{col.hexval()}" size="9"><b>{sc}/100</b></font>'
            f'<font color="{C["muted"].hexval()}" size="9">  {grade(sc)}</font>',
            ParagraphStyle("_cb", fontName=R, fontSize=9, leading=13,
                           spaceAfter=0, spaceBefore=0))
        hdr = Table([[name_txt, badge_txt]], colWidths=[CW * 0.72, CW * 0.28])
        hdr.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C["surf"]),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN",         (1, 0), (1, 0),   "RIGHT"),
            ("LINEBELOW",     (0, 0), (-1, -1), 2, col),
        ]))

        bar = ScoreBar(cat["name"], sc, color=col)
        el.append(KeepTogether([Spacer(1, 0.4 * cm), hdr]))
        el.append(Spacer(1, 0.3 * cm))
        el.append(bar)
        el.append(Spacer(1, 0.35 * cm))

        body = cat["body"]
        for para in body.split("\n\n"):
            para = para.strip()
            if not para:
                continue
            if para.startswith("**") and para.endswith("**") and "\n" not in para:
                el.append(P(para, st["h3"]))
            elif para.startswith("- ") or "\n- " in para:
                for line in para.splitlines():
                    line = line.strip()
                    if line.startswith("- "):
                        el.append(P(f"- {line[2:].strip()}", st["bullet"]))
            elif para.startswith("|"):
                rows = []
                for line in para.splitlines():
                    line = line.strip()
                    if not line.startswith("|") or re.match(r'^\|[-| :]+\|$', line):
                        continue
                    cells = [c.strip() for c in line.strip("|").split("|")]
                    rows.append(cells)
                if rows:
                    ncols = max(len(r) for r in rows)
                    col_w = CW / ncols
                    tdata = [[TC(c, bold=(ri == 0), size=8) for c in (r + [""] * (ncols - len(r)))]
                             for ri, r in enumerate(rows)]
                    t = Table(tdata, colWidths=[col_w] * ncols)
                    cmds = [
                        ("BACKGROUND",    (0, 0), (-1, 0),  C["brand"]),
                        ("TEXTCOLOR",     (0, 0), (-1, 0),  C["white"]),
                        ("FONTNAME",      (0, 0), (-1, 0),  BD),
                        ("FONTSIZE",      (0, 0), (-1, -1), 8),
                        ("TOPPADDING",    (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
                        ("GRID",          (0, 0), (-1, -1), 0.4, C["border"]),
                        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                    ]
                    cmds += alt_rows(len(rows))
                    t.setStyle(TableStyle(cmds))
                    el.append(Spacer(1, 0.2 * cm))
                    el.append(t)
                    el.append(Spacer(1, 0.2 * cm))
            else:
                el.append(P(para, st["body"]))


def build_action_plan(el, st, quick_wins):
    el.append(PageBreak())
    el.append(HP(f'<font color="{C["accent"].hexval()}">ACTION PLAN</font>', st["cap"]))
    el.append(HP('<font size="21"><b>Quick Wins &amp; 30-Day Plan</b></font>',
                 ParagraphStyle("ap_h", fontName=BD, fontSize=21, textColor=C["ink"],
                                leading=28, spaceAfter=10)))
    el.append(AccentBar(height=3, color=C["ok"]))
    el.append(HP('<b>Immediate Actions</b>',
                 ParagraphStyle("ap_sub", fontName=SB, fontSize=11, textColor=C["ok"],
                                leading=15, spaceAfter=8, spaceBefore=12)))
    if quick_wins:
        for i, item in enumerate(quick_wins, 1):
            el.append(P(f"{i}.  {item}", st["ni"]))
    else:
        el.append(P("See priority issues above for recommended actions.", st["body"]))


def build_methodology(el, st):
    el.append(PageBreak())
    el.append(HP(f'<font color="{C["accent"].hexval()}">METHODOLOGY</font>', st["cap"]))
    el.append(HP('<font size="21"><b>How This Audit Was Conducted</b></font>',
                 ParagraphStyle("mh", fontName=BD, fontSize=21, textColor=C["ink"],
                                leading=28, spaceAfter=10)))
    el.append(AccentBar(height=3))
    el.append(Spacer(1, 0.4 * cm))

    intro = ("This GEO (Generative Engine Optimisation) Audit evaluates how visible and "
             "citable a website is to AI systems - including ChatGPT, Claude, Perplexity, "
             "Google AI Overviews, and Bing Copilot. The audit spans six weighted dimensions "
             "assessed through direct website analysis and public data sources.")
    el.append(P(intro, st["body"]))
    el.append(Spacer(1, 0.3 * cm))

    areas = [
        ("AI Citability",           "25%",
         "How easily AI systems can extract and quote passages. Assessed via structured Q&A blocks, answer format, statistics, and named facts."),
        ("Brand Authority",         "20%",
         "Third-party validation across Wikipedia, Reddit, trade press, directory listings, and review platforms that AI training corpora rely on."),
        ("Content E-E-A-T",         "20%",
         "Experience, Expertise, Authoritativeness, and Trustworthiness signals - named authors, credentials, company history, compliance documents."),
        ("Technical GEO",           "15%",
         "AI crawler access (robots.txt, meta tags), sitemap health, HTTPS, server-side rendering, llms.txt presence, and broken URL audit."),
        ("Schema & Structured Data","10%",
         "JSON-LD schema coverage - Organization, FAQPage, Article, AggregateRating - with FAQPage weighted highest for AI citability."),
        ("Platform Optimisation",   "10%",
         "Specific optimisation signals for Google AI Overviews, ChatGPT, Perplexity, Gemini, and Bing Copilot individually."),
    ]

    hdr = [TC("Category",        bold=True, size=8.5, color=C["white"]),
           TC("Weight",          bold=True, size=8.5, color=C["white"]),
           TC("What Is Assessed", bold=True, size=8.5, color=C["white"])]
    tdata = [hdr]
    for name, weight, desc in areas:
        tdata.append([TC(name,   bold=True, size=8.5),
                      TC(weight, size=8.5,  color=C["accent"]),
                      TC(desc,   size=8.5)])

    cmds = list(BASE_TBL) + alt_rows(len(areas))
    t = Table(tdata, colWidths=[CW * 0.28, CW * 0.10, CW * 0.62])
    t.setStyle(TableStyle(cmds))
    el.append(t)
    el.append(Spacer(1, 0.5 * cm))
    el.append(HRule())
    el.append(Spacer(1, 0.25 * cm))
    el.append(P("Scores reflect publicly available information at the time of audit. "
                "This report is prepared for discussion purposes only and does not constitute "
                "professional legal or regulatory advice.", st["cap"]))


# --- MAIN ---

def generate(md_path):
    content    = read_md(md_path)
    brand, date_str, overall, url = parse_meta(content)
    exec_txt   = parse_exec_summary(content)
    cats       = parse_score_cats(content)
    score_rows = parse_score_table(content)
    issues     = parse_priority_issues(content)
    deep_dives = parse_category_deep_dives(content)
    quick_wins = parse_quick_wins(content)

    folder = os.path.dirname(md_path)
    out    = os.path.join(folder, "GEO-AUDIT.pdf")

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=MAR, rightMargin=MAR,
        topMargin=2.0 * cm, bottomMargin=2.0 * cm,
    )

    cover_f   = Frame(MAR, 0, CW, PH - 0.5 * cm, id="cover", showBoundary=0)
    content_f = Frame(MAR, 2.0 * cm, CW, PH - 4.6 * cm, id="body",  showBoundary=0)

    doc.addPageTemplates([
        PageTemplate(id="Cover",   frames=[cover_f], onPage=on_cover),
        PageTemplate(id="Content", frames=[content_f], onPage=on_page(brand)),
    ])

    st = ST()
    el = []

    build_cover(el, st, brand, date_str, overall, url, exec_txt)
    el.append(NextPageTemplate("Content"))
    el.append(PageBreak())

    build_exec(el, st, exec_txt)

    if cats:
        build_score_overview(el, st, cats, score_rows)

    has_issues = any(issues.get(t) for t in ["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    if has_issues:
        build_priority_issues(el, st, issues)

    if deep_dives:
        build_category_deep_dives(el, st, deep_dives)

    build_action_plan(el, st, quick_wins)
    build_methodology(el, st)

    doc.build(el)
    size_kb = os.path.getsize(out) // 1024
    print(f"Brand: {brand or '(unknown)'} | Score: {overall}/100 | Categories: {len(cats)}")
    print(f"Done: {out} ({size_kb} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py generate_pdf_report.py <audit_folder_or_md_file>")
        sys.exit(1)
    generate(find_md(sys.argv[1]))
