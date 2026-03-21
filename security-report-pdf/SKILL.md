# Security Audit PDF Report Generator

## Skill Purpose
Generate a professional PDF from security audit data.

## When to Use
- `security report-pdf`
- After running `security audit`

## How to Execute

### Step 1: Check for existing data
Look for `SECURITY-AUDIT.md`. If not found, recommend running `security audit` first.

### Step 2: Build JSON
Same structure as other suites with security-specific categories.

### Step 3: Generate
```bash
python3 scripts/generate_pdf_report.py /tmp/report_data.json "SECURITY-REPORT-[company].pdf"
```

## PDF Design
- Accent colour: emerald (#059669)
- Same enterprise design system
- Header reads "Cybersecurity Posture Audit Report"
- Includes disclaimer on every page: "This is not a penetration test."
