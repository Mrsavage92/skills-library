# Page Speed Deep Dive

## Skill Purpose
Deep analysis of page load performance. Maps every render-blocking resource, catalogues unoptimised assets, and produces a prioritised optimisation plan with estimated load time improvements.

## When to Use
- `techaudit speed <url>`
- Follow-up to `techaudit audit` when Speed score is below 60

## How to Execute

### Step 1: Resource Inventory
Fetch the page and catalogue every resource:
- Scripts: URL, size indicator, blocking/async/defer, first-party vs third-party
- Stylesheets: URL, size indicator, critical vs non-critical
- Images: URL, format, dimensions (if specified), lazy loaded, estimated size
- Fonts: URL, format, font-display setting, preloaded
- iframes: Third-party embeds (YouTube, maps, social widgets)

### Step 2: Bottleneck Identification
Identify the top 5 performance bottlenecks:
- Largest unoptimised images
- Render-blocking third-party scripts
- Unused CSS/JS (large libraries loaded for minimal use)
- Unoptimised font loading
- Too many HTTP requests

### Step 3: Generate Report
Save to `SPEED-AUDIT.md` with resource inventory, bottleneck analysis, prioritised optimisation plan with estimated impact, and recommended tools (Cloudflare, image CDN, etc.)
