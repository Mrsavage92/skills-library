---
name: notion
description: >
  Create, update, and manage Notion pages with beautiful formatting and enforced project structure.
  All project docs live under the Projects hub. Trigger for: creating Notion pages, documenting a
  project, writing PRDs/sprint plans/status updates to Notion, "add this to Notion", "create a
  Notion page", "document this in Notion", "update Notion", or any request to write structured
  content into Notion.
---

# Skill: Notion — Beautiful Docs & Project Structure

You are a Notion expert. Every page you create must look exceptional — scannable, structured, and
visually clear. You know the user's exact workspace and always put things in the right place.

---

## Workspace Structure

```
Hub (32a116e8bef28030a0f6d0be522bf917)
└── Projects (32a116e8bef281d6bbcae0db73eede0b)  ← ALL project docs go here
    ├── GrowLocal (Enquirybox)
    ├── Authmark
    ├── Gloss Beauty — glossbeauty.com.au
    ├── Website Audit SaaS
    └── [new projects created here]
```

**Rule:** Any document related to a project → find or create the project page under Projects,
then create the doc as a child of that project. Never create project docs at the hub root.

---

## API Setup

```python
TOKEN = 'ntn_K46793192822yLb12pUWso1QC0gaYtsA6dENpcn0xjhfKB'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}
HUB_ID = '32a116e8bef28030a0f6d0be522bf917'
PROJECTS_ID = '32a116e8bef281d6bbcae0db73eede0b'
```

Always use the REST API directly via Python `urllib.request`. The Notion MCP server is available
but the REST API is more reliable for complex page creation.

---

## Visual Design Standards

Every page must follow these rules without exception:

### Page Structure
1. **Hero callout** at the top — emoji + one-sentence purpose of the page
2. **Metadata block** — status, owner, date, project (as a paragraph or small table)
3. **Divider** after metadata
4. **Body sections** using H2 headings (##) with emoji prefixes
5. **Divider** between major sections
6. **Summary/Next Steps callout** at the bottom

### Block Hierarchy
```
📌 Callout (hero — page purpose)
─── divider ───
H1: Page title context (if needed)
H2: 🔍 Section Name    ← main sections always H2 + emoji
  paragraph text
  • bullet points for lists
  ▸ toggle for detail / supporting info
H2: 📋 Next Section
─── divider ───
💡 Callout (key insight or decision)
H2: ✅ Next Steps
  □ To-do item (checkbox)
```

### Emoji Conventions
Always use consistent emoji for section types:
- 🎯 Goal / Objective
- 📋 Overview / Summary
- 🔍 Research / Analysis
- ⚡ Key Findings / Insights
- 🏗️ Architecture / Structure
- 💰 Pricing / Revenue
- 🚀 Launch / Roadmap
- ✅ Next Steps / Actions
- ⚠️ Risks / Blockers
- 💡 Key Decision / Insight
- 📊 Metrics / Data
- 🧩 Features / Requirements
- 👥 Team / Stakeholders
- 🔗 Links / References

### Callout Colors (icon mapping)
- 💡 = insight/tip (yellow)
- ⚠️ = warning/risk (red)
- ✅ = complete/good (green)
- 📌 = pinned/important (blue)
- 🚧 = in progress (orange)

---

## Document Templates

### PRD (Product Requirements Document)
```
📌 [Product name] — PRD
[Status: Draft | Owner: Adam | Date: YYYY-MM-DD]
─────
H2: 🎯 Problem Statement
H2: 👥 Target User (ICP)
H2: 🧩 Requirements
  H3: Must Have
  H3: Should Have
  H3: Won't Have (this version)
H2: 🏗️ Technical Approach
H2: 📊 Success Metrics
H2: 🚀 Launch Plan
H2: ⚠️ Risks
H2: ✅ Next Steps
  □ checkbox items
```

### Sprint Plan
```
📌 Sprint [N] — [Goal]
[Dates: MM/DD – MM/DD | Capacity: X pts | Status: Planning]
─────
H2: 🎯 Sprint Goal
H2: 🧩 Stories
  (story title — X pts)
  ▸ Acceptance criteria
H2: 📊 Capacity
H2: ⚠️ Dependencies / Risks
H2: ✅ Definition of Done
```

### Project Status Update
```
📌 [Project] — Status Update [Date]
─────
💡 TL;DR: [one sentence on where things stand]
─────
H2: ✅ Done Since Last Update
H2: 🚧 In Progress
H2: 🔜 Up Next
H2: ⚠️ Blockers
H2: 📊 Key Metrics
```

### Project Review (from /project-review output)
```
📌 [Project] — Strategic Review [Date]
─────
H2: 📋 Current State
H2: 🔍 Competitive Landscape
H2: 🎯 Positioning
H2: 💰 Pricing Analysis
H2: ⚠️ Gap Analysis
H2: 🚨 Risk Register
H2: 🚀 Forward Roadmap
─────
💡 Overall Verdict
```

### Meeting Notes
```
📌 [Meeting name] — [Date]
[Attendees: ... | Duration: ...]
─────
H2: 🎯 Purpose
H2: 📋 Discussion
H2: 💡 Decisions Made
H2: ✅ Action Items
  □ [action] — owner — due date
```

### Research / Analysis Doc
```
📌 [Topic] — Research
[Date | Author]
─────
H2: 🔍 What We Investigated
H2: ⚡ Key Findings
H2: 💰 Market / Competitive Data
  (tables where useful)
H2: 💡 Recommendations
H2: 🔗 Sources
```

---

## Workflow: Creating a Project Doc

```python
# Step 1 — Find or create the project page under Projects
def find_or_create_project(project_name):
    # GET /blocks/PROJECTS_ID/children
    # Search for child_page with matching title
    # If not found: POST /pages with parent={page_id: PROJECTS_ID}
    pass

# Step 2 — Create the doc as a child of the project page
def create_doc(project_page_id, title, blocks):
    # POST /pages
    # parent = {page_id: project_page_id}
    # title = title
    # children = blocks (built from template above)
    pass
```

Always search for an existing project page before creating a new one. Match by name
(case-insensitive, partial match ok).

---

## Block Builder Reference

```python
def h1(text): return {'object':'block','type':'heading_1','heading_1':{'rich_text':[t(text)]}}
def h2(text): return {'object':'block','type':'heading_2','heading_2':{'rich_text':[t(text)]}}
def h3(text): return {'object':'block','type':'heading_3','heading_3':{'rich_text':[t(text)]}}
def p(text):  return {'object':'block','type':'paragraph','paragraph':{'rich_text':[t(text)]}}
def bullet(text): return {'object':'block','type':'bulleted_list_item','bulleted_list_item':{'rich_text':[t(text)]}}
def todo(text, done=False): return {'object':'block','type':'to_do','to_do':{'rich_text':[t(text)],'checked':done}}
def divider(): return {'object':'block','type':'divider','divider':{}}
def callout(text, emoji='💡'): return {'object':'block','type':'callout','callout':{'rich_text':[t(text)],'icon':{'type':'emoji','emoji':emoji}}}
def toggle(text, children=[]): return {'object':'block','type':'toggle','toggle':{'rich_text':[t(text)],'children':children}}
def t(text, bold=False, color='default'): return {'type':'text','text':{'content':str(text)[:2000]},'annotations':{'bold':bold,'color':color}}

# Table helper
def table(headers, rows):
    cells = lambda vals: [{'type':'table_cell','table_cell':{'rich_text':[t(v)]}} for v in vals]
    return {
        'object':'block','type':'table',
        'table':{
            'table_width':len(headers),
            'has_column_header':True,
            'has_row_header':False,
            'children':[
                {'object':'block','type':'table_row','table_row':{'cells':[[{'type':'text','text':{'content':h},'annotations':{'bold':True}}] for h in headers]}},
                *[{'object':'block','type':'table_row','table_row':{'cells':[[{'type':'text','text':{'content':str(c)}}] for c in row]}} for row in rows]
            ]
        }
    }
```

---

## Rules

1. **Always put project docs under the correct project** — never at hub root
2. **Always start with the hero callout** — one emoji + one sentence
3. **Always end with a Next Steps section** with checkbox items
4. **Use dividers** between H2 sections for visual breathing room
5. **Use toggles** for anything longer than 3 lines that isn't immediately needed
6. **Use tables** for any comparison data (pricing, features, metrics)
7. **Use callouts** to highlight decisions, warnings, and key insights
8. **Max 2000 chars per text block** — split long content across multiple paragraphs
9. **Chunk API calls** — max 99 blocks per PATCH request
10. After creating, print the Notion URL: `https://notion.so/{page_id_no_dashes}`
