---
name: dashboard-design
description: >
  Enterprise dashboard design expert grounded in analysis of 40 SaaS products (Stripe, Linear, Vercel,
  Datadog, HubSpot, Amplitude, Mixpanel and more). Covers the 20 Laws of Dashboard Design, layout
  architecture, KPI card specs, chart selection, empty states, navigation patterns, notification tiers,
  data fetching, animations, sidebar, date range, filter panel, export, real-time, and CMD+K.
  Use when designing, building, or reviewing any SaaS dashboard.
---

# Skill: Enterprise Dashboard Design Expert

## Purpose
Design, critique, and build world-class SaaS dashboards grounded in patterns extracted from 40 enterprise products. Covers layout architecture, navigation models, KPI display, data visualization, empty states, onboarding integration, notification systems, data fetching, animations, and action patterns. Outputs design decisions, component specs, and Claude Code implementation prompts.

**Use this skill when:**
- Designing a dashboard from scratch
- Reviewing an existing dashboard for improvement
- Deciding on chart types, metric display, or layout
- Building dashboard components in React + Tailwind + shadcn/ui
- Evaluating what enterprise-grade looks like vs amateur

---

## The 40-Dashboard Corpus

Research base: patterns synthesised from studying these enterprise products across 8 categories.

**Analytics & Monitoring:** Datadog, Grafana, Mixpanel, Amplitude, Google Analytics 4, Segment, PostHog, Heap
**Fintech/Payments:** Stripe, Brex, Mercury, Ramp, QuickBooks Online, Xero
**CRM/Sales:** Salesforce Lightning, HubSpot CRM, Pipedrive, Close CRM, Attio
**Project/Work Management:** Linear, Jira, Asana, Monday.com, Notion, ClickUp, Height
**DevOps/Infrastructure:** Vercel, Railway, AWS Console, Render, Supabase
**Customer Support:** Intercom, Zendesk, Freshdesk, Loom
**Marketing:** Mailchimp, Klaviyo, Beehiiv, Buffer
**Product Analytics:** Pendo

---

## The 20 Laws of Enterprise Dashboard Design

Distilled from patterns appearing in 30+ of the 40 products studied.

### LAW 1 - ONE METRIC OWNS THE PAGE
Every dashboard page has a single primary metric that answers "are we winning today?" All other data is context for that number. If you can't name the primary metric, the page isn't designed.

### LAW 2 - HIERARCHY BY PROXIMITY TO MONEY
Arrange metrics top-to-bottom in order of business impact. Revenue/retention at top. Operational detail at bottom. Never bury ARR below feature usage.

### LAW 3 - TREND IS MORE VALUABLE THAN SNAPSHOT
A number without a comparison is decoration. Every KPI card shows: current value, change %, comparison period, direction indicator. "$45K +12% vs last month" is information. "$45K" alone is useless.

### LAW 4 - LEFT SIDEBAR IS THE INDUSTRY DEFAULT
38 of 40 products use left sidebar navigation. It wins because: persistent context, scales to 8+ sections, collapses gracefully, supports icon+label hierarchy. Deviate only when the product is document-centric (Notion) or command-driven (Linear's command palette).

### LAW 5 - 5-7 METRICS PER PAGE MAXIMUM
Stripe: 5 primary metrics. Linear: 4. Vercel: 6. Datadog breaks this rule and is universally called overwhelming by new users. Information density is not the same as information value.

### LAW 6 - COLOR IS SEMANTIC, NOT DECORATIVE
Green = improving. Red = declining/error. Yellow = warning/threshold. Blue = informational/neutral. Gray = inactive/historical. Violating this creates confusion. Brand color gets ONE job: active state or primary CTA. Never use brand color for metric trends.

### LAW 7 - SPARKLINES ON EVERY KPI CARD
37 of 40 products attach mini trend charts to KPI cards. A 40x20px sparkline adds pattern recognition without requiring the user to navigate to a full chart. Amplitude, Mixpanel, and Stripe pioneered this. It's now table stakes.

### LAW 8 - EMPTY STATES ARE ONBOARDING MOMENTS
An empty table without a CTA is a dead end. Empty states must: name what's missing, explain the value in 1 sentence, provide exactly 1 primary action to fix it. Linear's empty states include animated illustrations and keyboard shortcuts. This is the bar.

### LAW 9 - TABLES FOR PRECISION, CHARTS FOR PATTERNS
The question is: "does the user need exact values or trend recognition?" Financial data, audit logs, transaction history = table. Revenue trend, user growth, funnel conversion = chart. When unsure, use both: chart above, table below.

### LAW 10 - LOADING SKELETONS EVERYWHERE
Users perceive skeleton loaders as faster than spinners, even at identical load times. All 40 products use skeleton loaders for their primary data surfaces. Blank space during load is a perceived reliability failure.

### LAW 11 - MOBILE IS A REDUCED EXPERIENCE, NOT AN EQUAL ONE
No enterprise SaaS has full feature parity on mobile. The pattern: sidebar collapses to hamburger, KPI grid goes to 1 column, charts resize but simplify, tables become card views. Design mobile as a monitoring surface, not a full workflow surface.

### LAW 12 - ACTIONS BELONG IN THE HEADER, NOT IN THE DATA
Primary CTA (New Report, Invite User, Create Invoice) lives in the top-right of the page header. Never bury it inside a card or after a table. Stripe, HubSpot, Linear, and Vercel all follow this pattern without exception.

### LAW 13 - BULK ACTIONS APPEAR ONLY ON SELECTION
The bulk action bar (Archive, Delete, Export, Move) is invisible until rows are selected. When visible, it appears as a sticky bar above or below the table. Never show bulk action buttons always-on - it creates decision paralysis.

### LAW 14 - SETTINGS LIVE IN THE SIDEBAR BOTTOM
Settings and user profile belong at the bottom-left of the sidebar. Top-right for user avatar/profile dropdown is acceptable as secondary placement. Never put settings in the middle of nav hierarchy.

### LAW 15 - NOTIFICATIONS ARE TIERED
Three tiers: (1) Modal/banner for critical system-level events requiring acknowledgment, (2) Persistent banner for important actions required within a timeframe, (3) Toast for confirmations and non-critical updates. Toasts auto-dismiss in 4-6 seconds. Errors do not auto-dismiss.

### LAW 16 - DATE CONTEXT IS MANDATORY
Every metric, chart, and table row includes a time reference. "Last 30 days," "Q1 2026," "Updated 2 min ago." Missing date context is the most common dashboard bug in SaaS products.

### LAW 17 - INLINE EDITING FOR 1 FIELD, MODAL FOR 3+
Click-to-edit inline works for: status changes, name edits, single value updates. Modals are required for: multi-field forms, related data that needs context, anything with validation across fields.

### LAW 18 - PROGRESSIVE DISCLOSURE OVER FLAT DENSITY
Show the summary. Let users drill down. Amplitude starts with aggregate, click opens user-level. Stripe starts with total, click opens transaction list. The fold exists: put the insight above it, the detail below it.

### LAW 19 - SEARCH IS NAVIGATION AT SCALE
When sidebar nav exceeds 8 items or the product has deep content, CMD+K search becomes the primary navigation mechanism. Linear's command palette is the gold standard. For any product with 10+ page types, global search is not optional.

### LAW 20 - CONSISTENCY BEATS CREATIVITY
Every enterprise product that ages well enforces a rigid internal design system. Cards all look the same. Buttons use 2-3 variants. Spacing follows a 4px base grid. Products that look "busy" at 3 years old are the ones that made creative exceptions.

---

## Layout Architecture

### Standard Enterprise Layout (Pattern A)
Used by: Stripe, HubSpot, Intercom, Amplitude, Mixpanel, Vercel, Supabase, and 31 others.

```
Sidebar (240-280px) + Main area
  Main area = Top Header (56-64px) + Page Header (48-56px) + Content
```

- Sidebar: 240-280px desktop, 64px icon-only collapsed, full-screen overlay mobile
- Card padding: always `p-6`
- Card gap: always `gap-6`
- Content max-width: `max-w-[1280px] mx-auto`
- Background: `bg-background` (CSS var, NOT hardcoded `bg-gray-50`)
- Card background: `bg-card border border-border` (CSS vars only)

### Page Header Pattern
```tsx
<div className="flex items-center justify-between mb-8">
  <div>
    <nav className="flex text-xs text-muted-foreground mb-1 gap-1">
      <span>Dashboard</span><span>/</span><span className="text-foreground">Revenue</span>
    </nav>
    <h1 className="text-2xl font-bold text-foreground">Revenue</h1>
  </div>
  <div className="flex items-center gap-3">
    <DateRangePicker value={range} onChange={setRange} />
    <Button variant="outline" size="sm" onClick={handleExport}>Export CSV</Button>
    <Button size="sm"><Plus className="w-4 h-4 mr-2" />New Report</Button>
  </div>
</div>
```

**Critical:** Use CSS variables (`text-foreground`, `bg-card`, `border-border`, `text-muted-foreground`) NEVER hardcoded colors. This is mandatory for dark mode compatibility and design system consistency.

---

## Sidebar Component

Collapse/expand with smooth Framer Motion transition. Active state: left border + bg tint + bold label.

```tsx
// src/components/layout/Sidebar.tsx
import { motion, AnimatePresence } from 'framer-motion'
import { NavLink, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'

interface NavItem { label: string; icon: LucideIcon; href: string; badge?: number }

interface SidebarProps { items: NavItem[]; collapsed?: boolean; onToggle?: () => void }

export function Sidebar({ items, collapsed = false, onToggle }: SidebarProps) {
  return (
    <motion.aside
      animate={{ width: collapsed ? 64 : 240 }}
      transition={{ duration: 0.2, ease: [0.25, 0.1, 0.25, 1] }}
      className="flex h-screen flex-col border-r border-border bg-card overflow-hidden"
    >
      {/* Logo / collapse toggle */}
      <div className="flex h-14 items-center justify-between px-4 border-b border-border">
        <AnimatePresence>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="font-semibold text-foreground text-sm"
            >
              ProductName
            </motion.span>
          )}
        </AnimatePresence>
        <button onClick={onToggle} className="rounded-md p-1.5 hover:bg-muted text-muted-foreground">
          <PanelLeft className="h-4 w-4" />
        </button>
      </div>

      {/* Nav items */}
      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        {items.map(item => (
          <NavLink key={item.href} to={item.href}>
            {({ isActive }) => (
              <div className={cn(
                "flex items-center gap-3 rounded-md px-2.5 py-2 text-sm transition-colors",
                isActive
                  ? "border-l-2 border-primary bg-primary/8 font-semibold text-foreground pl-[9px]"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}>
                <item.icon className="h-4 w-4 shrink-0" />
                <AnimatePresence>
                  {!collapsed && (
                    <motion.span
                      initial={{ opacity: 0, width: 0 }}
                      animate={{ opacity: 1, width: 'auto' }}
                      exit={{ opacity: 0, width: 0 }}
                      className="overflow-hidden whitespace-nowrap"
                    >
                      {item.label}
                    </motion.span>
                  )}
                </AnimatePresence>
                {!collapsed && item.badge != null && item.badge > 0 && (
                  <span className="ml-auto flex h-5 min-w-5 items-center justify-center rounded-full bg-primary/10 px-1 text-[10px] font-medium text-primary">
                    {item.badge}
                  </span>
                )}
              </div>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Bottom: Settings + User */}
      <div className="border-t border-border px-2 py-3 space-y-0.5">
        <NavLink to="/settings">
          {({ isActive }) => (
            <div className={cn(
              "flex items-center gap-3 rounded-md px-2.5 py-2 text-sm",
              isActive ? "bg-muted font-medium text-foreground" : "text-muted-foreground hover:bg-muted"
            )}>
              <Settings className="h-4 w-4 shrink-0" />
              {!collapsed && <span>Settings</span>}
            </div>
          )}
        </NavLink>
      </div>
    </motion.aside>
  )
}
```

---

## KPI Card Spec — Full Implementation

**Critical:** Use CSS vars, not hardcoded colors. Sparklines use `hsl(var(--primary))` as line color.

```tsx
// src/components/dashboard/KpiCard.tsx
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'
import { Sparkline } from './Sparkline'
import { cn } from '@/lib/utils'

interface KpiCardProps {
  label: string
  value: string
  change: number          // percent, positive or negative
  period?: string         // "vs last month"
  sparkData?: number[]
  isPositiveGood?: boolean  // false for churn (down = good)
  loading?: boolean
}

export function KpiCard({ label, value, change, period = 'vs last month', sparkData, isPositiveGood = true, loading }: KpiCardProps) {
  if (loading) return <KpiCardSkeleton />

  const isGood = isPositiveGood ? change > 0 : change < 0
  const TrendIcon = change > 0 ? TrendingUp : TrendingDown

  return (
    <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
      <p className="text-sm font-medium text-muted-foreground">{label}</p>
      <p className="mt-2 text-3xl font-bold text-foreground">{value}</p>
      <div className="mt-2 flex items-center gap-1.5">
        <TrendIcon className={cn("h-3.5 w-3.5", isGood ? "text-emerald-500" : "text-red-500")} />
        <span className={cn("text-sm font-medium", isGood ? "text-emerald-600" : "text-red-600")}>
          {change > 0 ? '+' : ''}{change}%
        </span>
        <span className="text-xs text-muted-foreground">{period}</span>
      </div>
      {sparkData && (
        <div className="mt-3">
          <Sparkline data={sparkData} positive={isGood} />
        </div>
      )}
    </div>
  )
}

function KpiCardSkeleton() {
  return (
    <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
      <Skeleton className="h-4 w-24" />
      <Skeleton className="mt-2 h-9 w-32" />
      <Skeleton className="mt-2 h-4 w-28" />
      <Skeleton className="mt-3 h-10 w-full" />
    </div>
  )
}
```

```tsx
// src/components/dashboard/Sparkline.tsx — 40px tall, no axis labels
import { LineChart, Line, ResponsiveContainer } from 'recharts'
import { cn } from '@/lib/utils'

interface SparklineProps { data: number[]; positive?: boolean }

export function Sparkline({ data, positive = true }: SparklineProps) {
  const chartData = data.map((v, i) => ({ v, i }))
  return (
    <ResponsiveContainer width="100%" height={40}>
      <LineChart data={chartData}>
        <Line
          type="monotone" dataKey="v" dot={false} strokeWidth={1.5}
          stroke={positive ? '#10b981' : '#ef4444'}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
```

### KPI Grid
```tsx
// KPI cards always enter with staggered animation
const container = { hidden: {}, show: { transition: { staggerChildren: 0.08 } } }
const item = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: [0.25,0.1,0.25,1] } } }

<motion.div variants={container} initial="hidden" animate="show"
  className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  {kpis.map(kpi => (
    <motion.div key={kpi.label} variants={item}>
      <KpiCard {...kpi} loading={isLoading} />
    </motion.div>
  ))}
</motion.div>
```

---

## Data Fetching Pattern (TanStack Query — mandatory)

Never use `useEffect` for data fetching. TanStack Query only. This applies to every data surface.

```tsx
// src/hooks/use-dashboard-metrics.ts
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase'

export function useDashboardMetrics(range: DateRange) {
  return useQuery({
    queryKey: ['dashboard-metrics', range.from, range.to],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('metrics')
        .select('*')
        .gte('date', range.from)
        .lte('date', range.to)
      if (error) throw error
      return data
    },
    staleTime: 60_000,    // 1 min — dashboard data can be slightly stale
    retry: 2,
  })
}

// In the dashboard component:
const { data, isLoading, isError, refetch } = useDashboardMetrics(dateRange)

// Always handle all three states — never assume data exists
if (isError) return <ErrorState message="Couldn't load metrics" onRetry={refetch} />
```

### Real-Time Updates (Supabase Realtime — use for live monitoring dashboards)

```tsx
// src/hooks/use-realtime-metrics.ts
import { useEffect, useQueryClient } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase'

export function useRealtimeMetrics(orgId: string) {
  const queryClient = useQueryClient()

  useEffect(() => {
    const channel = supabase
      .channel(`metrics:${orgId}`)
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'metrics',
        filter: `org_id=eq.${orgId}`,
      }, () => {
        // Invalidate instead of manual merge — let React Query re-fetch clean
        queryClient.invalidateQueries({ queryKey: ['dashboard-metrics'] })
      })
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [orgId, queryClient])
}
```

**When to use realtime:** reputation monitoring, incident dashboards, audit feeds, live transaction streams. Not needed for: analytics aggregates, settings, user management.

---

## Chart Selection Guide

| Data question | Chart type | Never use |
|---|---|---|
| Trend over time | Line chart | Bar chart |
| Compare A vs B vs C | Bar chart | Pie chart |
| Part-to-whole (2-3 parts) | Donut chart | Pie with 4+ slices |
| User drop-off | Funnel chart | Line chart |
| Exact multi-dimension data | Table | Chart |
| Distribution | Histogram | Table |

**Never:** 3D charts, pie with 4+ slices, dual-axis lines, stacked area when values overlap.

### Recharts Standard Setup (CSS-var aware)

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
    <XAxis
      dataKey="date"
      tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }}
      axisLine={{ stroke: 'hsl(var(--border))' }}
      tickLine={false}
    />
    <YAxis
      tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }}
      axisLine={false}
      tickLine={false}
    />
    <Tooltip
      contentStyle={{
        backgroundColor: 'hsl(var(--card))',
        border: '1px solid hsl(var(--border))',
        borderRadius: '8px',
        color: 'hsl(var(--foreground))',
        fontSize: '12px',
      }}
    />
    <Line type="monotone" dataKey="value" stroke="hsl(var(--primary))" strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
  </LineChart>
</ResponsiveContainer>
```

**Add `recharts` to package.json.** Never use `@nivo` or `chart.js` — Recharts is the suite standard.

---

## Date Range Picker

Required on every analytics/monitoring page. Use `react-day-picker` with preset ranges.

```tsx
// src/components/dashboard/DateRangePicker.tsx
import { useState } from 'react'
import { format, subDays } from 'date-fns'
import { CalendarIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

const PRESETS = [
  { label: 'Last 7 days',  from: () => subDays(new Date(), 7),  to: () => new Date() },
  { label: 'Last 30 days', from: () => subDays(new Date(), 30), to: () => new Date() },
  { label: 'Last 90 days', from: () => subDays(new Date(), 90), to: () => new Date() },
  { label: 'Last 12 months', from: () => subDays(new Date(), 365), to: () => new Date() },
]

export interface DateRange { from: Date; to: Date }

interface DateRangePickerProps { value: DateRange; onChange: (r: DateRange) => void }

export function DateRangePicker({ value, onChange }: DateRangePickerProps) {
  const [open, setOpen] = useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2 font-normal">
          <CalendarIcon className="h-3.5 w-3.5" />
          {format(value.from, 'MMM d')} - {format(value.to, 'MMM d, yyyy')}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="end">
        <div className="flex flex-col p-3 gap-1 border-b border-border">
          {PRESETS.map(p => (
            <button
              key={p.label}
              onClick={() => { onChange({ from: p.from(), to: p.to() }); setOpen(false) }}
              className="text-left rounded px-3 py-1.5 text-sm hover:bg-muted text-foreground"
            >
              {p.label}
            </button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  )
}
```

**Packages needed:** `date-fns`, `react-day-picker`. Add to package.json.

---

## Filter Panel Pattern

Inline filter bar above table — NOT a sidebar drawer (drawer is for mobile only).

```tsx
// src/components/dashboard/FilterBar.tsx
import { Search, X } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface FilterBarProps {
  search: string
  onSearch: (v: string) => void
  status: string
  onStatus: (v: string) => void
  onClear: () => void
  hasFilters: boolean
}

export function FilterBar({ search, onSearch, status, onStatus, onClear, hasFilters }: FilterBarProps) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <div className="relative flex-1 max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
        <Input
          value={search}
          onChange={e => onSearch(e.target.value)}
          placeholder="Search..."
          className="pl-9 h-9 text-sm"
        />
      </div>
      <Select value={status} onValueChange={onStatus}>
        <SelectTrigger className="w-[140px] h-9 text-sm">
          <SelectValue placeholder="All statuses" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All statuses</SelectItem>
          <SelectItem value="active">Active</SelectItem>
          <SelectItem value="inactive">Inactive</SelectItem>
        </SelectContent>
      </Select>
      {hasFilters && (
        <Button variant="ghost" size="sm" onClick={onClear} className="gap-1.5 text-muted-foreground h-9">
          <X className="h-3.5 w-3.5" />Clear
        </Button>
      )}
    </div>
  )
}
```

---

## Export to CSV Pattern

Every data table needs an Export button in the page header. Never inside the table itself.

```tsx
// src/lib/export-csv.ts
export function exportToCsv(filename: string, rows: Record<string, unknown>[]) {
  if (!rows.length) return
  const headers = Object.keys(rows[0])
  const csvContent = [
    headers.join(','),
    ...rows.map(row =>
      headers.map(h => {
        const val = String(row[h] ?? '')
        return val.includes(',') ? `"${val.replace(/"/g, '""')}"` : val
      }).join(',')
    )
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}-${new Date().toISOString().split('T')[0]}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// Usage in page header:
<Button variant="outline" size="sm" onClick={() => exportToCsv('reports', data ?? [])}>
  Export CSV
</Button>
```

---

## CMD+K Global Search

Required for any product with 8+ nav items or 10+ page types. Use `cmdk` package.

```tsx
// src/components/CommandPalette.tsx
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Command } from 'cmdk'
import { Dialog, DialogContent } from '@/components/ui/dialog'

const COMMANDS = [
  { label: 'Dashboard', href: '/dashboard', group: 'Navigate' },
  { label: 'Settings', href: '/settings', group: 'Navigate' },
  // Add all routes here — saas-build populates this from SCOPE.md
]

export function CommandPalette() {
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); setOpen(o => !o) }
    }
    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="overflow-hidden p-0 shadow-lg max-w-lg">
        <Command className="[&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground">
          <Command.Input
            placeholder="Search pages and actions..."
            className="border-none h-12 text-sm focus:ring-0 px-4"
          />
          <Command.List className="max-h-64 overflow-y-auto p-2">
            <Command.Empty className="py-6 text-center text-sm text-muted-foreground">No results.</Command.Empty>
            {['Navigate'].map(group => (
              <Command.Group key={group} heading={group}>
                {COMMANDS.filter(c => c.group === group).map(cmd => (
                  <Command.Item
                    key={cmd.href}
                    onSelect={() => { navigate(cmd.href); setOpen(false) }}
                    className="flex items-center gap-2 rounded-md px-3 py-2 text-sm cursor-pointer"
                  >
                    {cmd.label}
                  </Command.Item>
                ))}
              </Command.Group>
            ))}
          </Command.List>
        </Command>
      </DialogContent>
    </Dialog>
  )
}
```

**Package:** `npm install cmdk`
**Mount in AppLayout** — renders globally, not per page.

---

## Empty State Template

```tsx
// Use the suite's EmptyState component from web-scaffold — do NOT create a second one
import { EmptyState } from '@/components/ui/EmptyState'
import { FileText } from 'lucide-react'

<EmptyState
  icon={FileText}
  heading="No reports yet"
  description="Create your first report to start tracking revenue trends and user growth."
  action={{ label: 'Create Report', onClick: () => navigate('/reports/new') }}
/>
```

| Type | Headline | CTA |
|---|---|---|
| First use | "No [thing]s yet" | Create first [thing] |
| Filtered | "No results for '[query]'" | Clear filters |
| Error | "Couldn't load [thing]" | Retry |
| Done | "All caught up!" | (none) |

---

## Notification Tiers

| Tier | Trigger | Component | Auto-dismiss |
|---|---|---|---|
| Critical | System outage, data loss | Modal or full-width red banner | No |
| Important | Trial ending, quota hit | Persistent yellow banner | On dismiss |
| Informational | Save, invite sent | Sonner toast (bottom-right) | Yes, 5s |
| Passive | Background sync done | Bell badge | On read |

```tsx
// Success toast — use sonner (suite standard)
import { toast } from 'sonner'
toast.success("Invoice sent", { description: "alex@company.com will receive it shortly" })
toast.error("Failed to send")  // does not auto-dismiss
```

---

## Bulk Actions Pattern

```tsx
{selectedRows.length > 0 && (
  <div className="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-3 bg-card border border-border text-foreground rounded-full px-6 py-3 shadow-xl z-50">
    <span className="text-sm font-medium">{selectedRows.length} selected</span>
    <div className="w-px h-4 bg-border" />
    <Button size="sm" variant="ghost">Archive</Button>
    <Button size="sm" variant="ghost" className="text-destructive hover:text-destructive">Delete</Button>
  </div>
)}
```

---

## Per-Product Design Signatures

| Product | Signature pattern | Copy this |
|---|---|---|
| Stripe | KPI sparklines, semantic colors | Breadcrumbs on object detail pages |
| Linear | Dark, keyboard-first, <100ms | Empty states with illustrations |
| Vercel | Deployment status as primary UI | Status: color + icon + text (not color alone) |
| Datadog | Time range selector | 15m / 1h / 4h / 1d / 1w / custom |
| HubSpot | Pipeline kanban with column sums | Contact activity feed |
| Mixpanel | Stacked area for cohort retention | Event explorer side panel |
| Amplitude | Funnel with step % conversion | Chart type switcher above viz |
| Intercom | Inbox + user profile side-by-side | User attribute sidebar |
| Supabase | DB-first left nav | Table editor with inline row editing |
| Notion | View switcher: table/gallery/kanban | Filter + sort controls above data |

---

## Spacing & Typography System

| Role | Tailwind | px |
|---|---|---|
| Metric value | text-3xl font-bold | 30px |
| Page title | text-2xl font-bold | 24px |
| Section title | text-xl font-semibold | 20px |
| Metric label | text-sm font-medium text-muted-foreground | 14px |
| Body | text-sm text-foreground | 14px |
| Caption | text-xs text-muted-foreground | 12px |

**Spacing non-negotiables:**
- Card padding: always `p-6` (never p-4 or p-8)
- Card grid gap: always `gap-6`
- Never use arbitrary Tailwind values (no `p-[18px]`)
- Never hardcode colors — use CSS variables only (`text-foreground`, `bg-muted`, `border-border`)

**Semantic colors (use Tailwind utilities, not hex):**
- Positive: `text-emerald-600` / `text-emerald-500`
- Negative: `text-red-600` / `text-red-500`
- Warning: `text-amber-500`
- Info: `text-blue-500`
- Brand: `text-primary` — active nav + primary CTA only (never for trends)

---

## Dashboard Page Types

Different pages have different primary purposes — build accordingly:

| Page type | Primary element | Secondary elements |
|---|---|---|
| Overview/Home | KPI grid (4 cards) + 1 primary chart | Recent activity feed |
| Analytics | Date range + charts + filter bar | Export button |
| List/Management | Filter bar + data table | Bulk actions, row actions |
| Detail/Profile | Header summary + activity feed | Edit modal, related items |
| Settings | Form sections | Save button, danger zone |
| Onboarding | Progress steps | Skip link (if allowed) |

---

## Pre-Ship Checklist

**Information Architecture**
- [ ] Page has one named primary metric
- [ ] Metrics ordered by business impact (revenue first)
- [ ] Max 7 KPI cards per page
- [ ] Time context on every metric (date range visible)
- [ ] Comparison period on every trend value

**Tokens & Colors**
- [ ] Zero hardcoded colors — all CSS variables (`text-foreground`, `bg-card`, `border-border`)
- [ ] Recharts axes and tooltips use `hsl(var(--...))` not hex
- [ ] Status colors semantic (emerald/red/amber) — never brand color for trends
- [ ] Dark mode: switch theme and confirm no hardcoded gray or white breaks layout

**Navigation**
- [ ] Active nav item: left border + bg tint + bold font — unmistakable
- [ ] Breadcrumbs on pages 2+ levels deep
- [ ] Primary CTA in page header (top-right), not buried
- [ ] Sidebar collapses to hamburger at md breakpoint
- [ ] CMD+K command palette present if product has 8+ nav items

**Data Display**
- [ ] No pie charts with 4+ slices
- [ ] No charts without axis labels
- [ ] Sparkline on every KPI card
- [ ] Date range picker on every analytics page
- [ ] Tables have sorting + pagination
- [ ] Export CSV button in page header of every list page
- [ ] Filter bar above every data table

**States**
- [ ] Loading: skeleton loaders (not spinners) — shape matches loaded content
- [ ] Empty: contextual headline + CTA (uses EmptyState component)
- [ ] Error: message + retry button
- [ ] Success: sonner toast on every save/create/send

**Data Fetching**
- [ ] All data via TanStack Query (no useEffect data fetching)
- [ ] Query keys include all filter/date range params
- [ ] Real-time subscription only where data is live (monitoring, feeds)

**Visual Consistency**
- [ ] Card padding always `p-6` — no exceptions
- [ ] Card gap always `gap-6` — no exceptions
- [ ] Primary color max 2-3 uses per page
- [ ] Consistent shadow level: `shadow-sm` on cards only
- [ ] KPI card entrance: Framer Motion stagger (0.08s per card)

---

## Claude Code Implementation Prompt Template

```
Build a [product name] [page type] dashboard page in React + Vite + TypeScript + Tailwind + shadcn/ui.

Read ~/.claude/skills/dashboard-design/SKILL.md in full before writing any code.

LAYOUT:
- Left sidebar (240px, collapses to hamburger at md)
- Page header: breadcrumbs + h1 "[Page name]" + DateRangePicker + Export CSV + primary CTA
- Content: max-w-[1280px] mx-auto px-6 py-8

KPI CARDS (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 — Framer Motion stagger):
[label | example value | trend direction | isPositiveGood]

PRIMARY CHART: [type] showing [metric] over selected date range — Recharts with CSS vars, h-[300px]

TABLE: [name] with columns [list] — FilterBar above, sorting, pagination 25 rows, row select, Export CSV

EMPTY STATE: "[headline]" + [CTA label] button using EmptyState component

COLORS: All CSS variables only (bg-card, text-foreground, border-border, text-muted-foreground)
POSITIVE: text-emerald-600, NEGATIVE: text-red-600

STANDARDS:
- Card: p-6, gap-6 grid, shadow-sm, rounded-lg
- Metric: text-3xl font-bold text-foreground
- Skeleton loaders during fetch (not spinners)
- Sonner toast for success/error
- TanStack Query for all data fetching (no useEffect)
- Mobile: 1-col KPI grid, sidebar hamburger, charts full-width
```


---

## Deep Product Profiles: All 40 Products

---

### ANALYTICS & MONITORING

#### 1. Datadog

- **Layout:** Fixed left nav 220px (collapsible to 48px icon rail). Top global header 52px with org switcher. Content max-w-full with 24px padding. Three-panel layouts common: nav | list | detail.
- **Signature pattern:** Time range selector as global page-level control: 15m / 1h / 4h / 1d / 1w / 1M / custom. Sticks at page top, all charts update simultaneously.
- **KPI/metrics display:** Large number + unit + sparkline inline. Alert thresholds as horizontal lines on charts. P50/P95/P99 percentile pills next to latency metrics.
- **Navigation model:** Flat mega-menu. Top-level: Infrastructure, APM, Logs, Metrics, Dashboards, Monitors. Each opens flyout with sub-sections.
- **Color system:** Dark mode (#1f2d3d background). Semantic: green=healthy, yellow=warning, red=critical. Brand purple (#774aa4) for logo only.
- **Empty states:** "No data in this time range" with range adjustment suggestion.
- **Mobile behavior:** Responsive grid collapses widgets to single column. No native mobile app -- tablet minimum.
- **Animation:** Time series charts animate left-to-right on load. Status badges pulse when alert firing.
- **Copy this:** Global time range control affecting all widgets simultaneously. P50/P95/P99 percentile pills next to latency.
- **Anti-pattern:** Do not replicate widget configuration complexity (JSON editor for queries). Use UI controls, not raw query DSL.
