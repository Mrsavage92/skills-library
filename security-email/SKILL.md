# Email Authentication Security Check

## Skill Purpose
Check SPF, DKIM, and DMARC configuration for a domain. These records prevent email spoofing and phishing attacks using the business's domain.

## When to Use
- `security email <domain>`
- Follow-up to `security audit` when Email Authentication score is below 60

## How to Execute

### Step 1: Check DNS Records
Search for `[domain] SPF record check` and `[domain] DMARC record` to find existing records.

### Step 2: Analyse SPF
- Record present? Quote it
- Mechanism: `-all` (hard fail - best), `~all` (soft fail - weaker), `?all` (neutral - bad)
- Include count (>10 lookups = broken)
- Includes make sense for the business? (Google, Microsoft, Mailchimp, etc.)

### Step 3: Analyse DMARC
- Record present at `_dmarc.[domain]`? Quote it
- Policy: `p=none` (monitoring), `p=quarantine` (filter), `p=reject` (block - best)
- Reporting: `rua` and `ruf` tags present?
- Subdomains: `sp=` policy set?

### Step 4: Generate Report
Save to `EMAIL-SECURITY.md` with current status, risk assessment, step-by-step remediation guide, and recommended DMARC ramp-up plan (none > quarantine > reject over 4-6 weeks).
