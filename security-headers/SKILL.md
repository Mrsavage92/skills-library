# HTTP Security Headers Analysis

## Skill Purpose
Deep analysis of HTTP security headers. Identifies missing headers, weak configurations, and produces specific implementation guidance.

## When to Use
- `security headers <url>`
- Follow-up to `security audit` when Security Headers score is below 60

## How to Execute

### Step 1: Check All Security Headers
From the fetched page response (headers and meta tags), check for:

1. **Content-Security-Policy (CSP)** - Controls what resources can load. Most important but complex.
2. **Strict-Transport-Security (HSTS)** - Forces HTTPS. Include `max-age`, `includeSubDomains`.
3. **X-Frame-Options** - Prevents clickjacking. Should be `DENY` or `SAMEORIGIN`.
4. **X-Content-Type-Options** - Prevents MIME sniffing. Should be `nosniff`.
5. **Referrer-Policy** - Controls referrer info. Should be `strict-origin-when-cross-origin` or stricter.
6. **Permissions-Policy** - Controls browser features. Restrict camera, microphone, geolocation, etc.
7. **X-XSS-Protection** - Deprecated but still useful signal. Should be `1; mode=block`.
8. **Cross-Origin-Opener-Policy** - Isolates browsing context.
9. **Cross-Origin-Resource-Policy** - Controls cross-origin resource loading.

### Step 2: Assess Each Header
For each: present/missing, current value, recommended value, implementation priority.

### Step 3: Generate Report
Save to `HEADERS-AUDIT.md` with header inventory, specific implementation code for each missing header (Apache .htaccess, nginx config, meta tags), and priority order.
