---
name: "web-ssg"
description: "Add build-time Static Site Generation to a React + Vite + React Router SPA. Generates static HTML for every route at build time so AI crawlers and search engines see real content. Designed for Lovable-hosted sites but works with any static host. Use when the site is an SPA that renders blank pages for bots, or when you need prerendered HTML for SEO/GEO."
license: MIT
metadata:
  version: 1.0.0
  author: Adam Savage
  category: web
  updated: 2026-04-09
---

# web-ssg

Add build-time Static Site Generation (SSG) to a React + Vite + React Router SPA. Generates static HTML for every route so bots and crawlers see real content instead of an empty `<div id="root"></div>`.

## When to use

- React SPA where bots see an empty root div with no content
- Lovable-hosted sites (or any static file host)
- Sites failing GEO/SEO audits because content is JS-only
- 69% of AI crawlers (GPTBot, ClaudeBot, PerplexityBot) do not execute JavaScript
- You want prerendered HTML without switching to Next.js or Astro

## Pre-flight checks

Before starting, verify these:

1. **Confirm React + Vite + React Router** - check `package.json` for `vite`, `react-router-dom`
2. **Check for React.lazy()** - open `App.tsx` and search for `React.lazy` or `lazy(`. The SSG entry file must use static imports, so note every lazy-loaded component
3. **Identify all routes** - find every `<Route path="..." />` in `App.tsx`. List them. Skip dynamic routes with `:params` (those fall back to SPA behaviour)
4. **Check for client-only dependencies** - look for `framer-motion`, `AnimatePresence`, browser API usage (`window`, `document`, `localStorage`), `ScrollToTop`, `CookieConsent`

## Step 1: Create `src/entry-server.tsx`

This file renders your app to static HTML on the server (Node). It must use static imports (no lazy), and strip client-only wrappers.

```tsx
// src/entry-server.tsx
import { renderToString } from "react-dom/server";
import { StaticRouter } from "react-router-dom/server";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Routes, Route } from "react-router-dom";

// STATIC imports - replace these with your actual page components
import Index from "./pages/Index";
import About from "./pages/About";
import Pricing from "./pages/Pricing";
import Privacy from "./pages/Privacy";
import Terms from "./pages/Terms";
import NotFound from "./pages/NotFound";
// Add every page component here - NO lazy() imports

export function render(url: string): string {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: Infinity },
    },
  });

  const html = renderToString(
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <StaticRouter location={url}>
          <Routes>
            {/* Mirror your App.tsx routes exactly */}
            <Route path="/" element={<Index />} />
            <Route path="/about" element={<About />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/privacy" element={<Privacy />} />
            <Route path="/terms" element={<Terms />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </StaticRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );

  return html;
}
```

**Key rules:**
- Import every page component statically at the top
- Do NOT include `BrowserRouter` - use `StaticRouter` instead
- Do NOT include `AnimatePresence`, `ScrollToTop`, `CookieConsent`, or anything that touches browser APIs
- DO keep context providers (`QueryClientProvider`, `TooltipProvider`) so child components don't throw

## Step 2: Create `build-ssg.mjs`

This script runs after the Vite build. It calls your render function for each route and writes the HTML files.

```js
// build-ssg.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// All static routes to prerender - update this list when routes change
const routes = [
  "/",
  "/about",
  "/pricing",
  "/privacy",
  "/terms",
];

async function build() {
  const templatePath = path.resolve(__dirname, "dist/client/index.html");
  const template = fs.readFileSync(templatePath, "utf-8");
  const { render } = await import("./dist/server/entry-server.js");

  let succeeded = 0;
  let failed = 0;

  for (const route of routes) {
    try {
      const appHtml = render(route);
      const html = template.replace(
        '<div id="root"></div>',
        `<div id="root">${appHtml}</div>`
      );

      if (route === "/") {
        fs.writeFileSync(templatePath, html);
      } else {
        const dir = path.resolve(__dirname, `dist/client${route}`);
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(path.resolve(dir, "index.html"), html);
      }

      console.log(`  OK  ${route}`);
      succeeded++;
    } catch (err) {
      // Non-fatal: this route falls back to SPA client-side rendering
      console.error(`  FAIL  ${route} - ${err.message}`);
      failed++;
    }
  }

  console.log(`\nSSG complete: ${succeeded} succeeded, ${failed} failed out of ${routes.length} routes`);

  if (failed > 0) {
    console.log("Failed routes will still work via client-side SPA rendering.");
  }
}

build();
```

## Step 3: Update `src/main.tsx`

Add conditional hydration so the client picks up the server-rendered HTML correctly in production, while dev mode still works with `createRoot`.

Find the existing render call in `main.tsx` and replace it:

```tsx
// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

const rootElement = document.getElementById("root")!;

if (rootElement.hasChildNodes()) {
  // Production with SSG: hydrate the server-rendered HTML
  ReactDOM.hydrateRoot(rootElement, <React.StrictMode><App /></React.StrictMode>);
} else {
  // Dev mode or non-SSG: standard client render
  ReactDOM.createRoot(rootElement).render(<React.StrictMode><App /></React.StrictMode>);
}
```

## Step 4: Update `vite.config.ts`

Add `ssr.noExternal` for packages that break when treated as external ESM in Node. Only include packages your project actually uses.

```ts
// Add this to your existing vite.config.ts - merge with existing config
export default defineConfig({
  // ... your existing config ...
  ssr: {
    noExternal: [
      // Add ONLY the ones your project uses:
      "framer-motion",
      "lucide-react",
      "class-variance-authority",
      "clsx",
      "tailwind-merge",
      "sonner",
      // Radix UI - add any @radix-ui/* packages you use
      /^@radix-ui\/.*/,
    ],
  },
});
```

## Step 5: Update `package.json` scripts

Replace the build and preview scripts:

```json
{
  "scripts": {
    "build": "vite build --outDir dist/client && vite build --ssr src/entry-server.tsx --outDir dist/server && node build-ssg.mjs",
    "preview": "vite preview --outDir dist/client"
  }
}
```

The build now runs three stages:
1. Standard client build to `dist/client/`
2. SSR build of the entry server to `dist/server/`
3. SSG script that generates static HTML for each route

## Step 6: Lovable-specific notes

- **Publish directory**: Lovable may need the publish directory set to `dist/client` instead of the default `dist`. Check your Lovable deploy settings.
- **Blank page after deploy**: If the deployed site shows a blank page after adding SSG, the publish directory is almost certainly wrong. Set it to `dist/client`.
- **Route changes in Lovable editor**: If you add or remove routes using the Lovable editor, you need to update both `src/entry-server.tsx` (imports and Route elements) and `build-ssg.mjs` (routes array). Re-run this skill when routes change.
- **Lovable AI edits**: Lovable's AI may overwrite `main.tsx` and remove the hydration logic. If interactions break after a Lovable edit, check that `main.tsx` still has the `hasChildNodes()` conditional.

## Route detection

To extract routes from your project, look for patterns like these in `App.tsx`:

```
<Route path="/about" element={<About />} />
<Route path="/pricing" element={<Pricing />} />
<Route path="/:slug" element={<BlogPost />} />   // SKIP - dynamic param
<Route path="/blog/:id" element={<Post />} />     // SKIP - dynamic param
```

**Rules:**
- Include every route with a fixed path (no `:params`)
- Skip routes with dynamic segments like `:slug`, `:id` - these fall back to SPA client rendering
- Skip catch-all routes (`path="*"`) from the SSG routes list, but keep the `<Route path="*">` in entry-server.tsx
- The `"/"` root route is mandatory

## Common pitfalls

### framer-motion crashes in Node
`useReducedMotion` and other hooks call browser APIs. Wrap motion components or mock them:

```tsx
// In entry-server.tsx, wrap problematic components:
const SafeMotionDiv = typeof window !== "undefined"
  ? require("framer-motion").motion.div
  : (props: any) => <div {...props} />;
```

Or simpler: exclude animated wrappers from entry-server.tsx entirely.

### window/document references
Guard any browser API usage in components that render during SSG:

```tsx
const isBrowser = typeof window !== "undefined";
const scrollY = isBrowser ? window.scrollY : 0;
```

### Image imports
Vite resolves image imports differently in SSR vs client builds. If images show broken paths in the static HTML, use public directory paths (`/images/hero.png`) instead of imports (`import hero from './hero.png'`).

### Radix UI components
Radix packages must be bundled (via `ssr.noExternal`), not left as external imports. If you see "Cannot find module" errors during the SSR build, add the specific `@radix-ui/*` package to the `noExternal` array.

### React Router version
This skill targets React Router v6+. If using v5 or earlier, `StaticRouter` is imported from `react-router-dom` directly (not `react-router-dom/server`).

### Hydration mismatches
If the console shows hydration mismatch warnings after SSG:
- Check that entry-server.tsx routes match App.tsx routes exactly
- Ensure no component renders different content based on `window` or `Date.now()`
- Timestamps, random values, and viewport-dependent content cause mismatches

## Quality checklist

After running the build, verify:

- [ ] Build completes without errors (`npm run build`)
- [ ] All static routes have generated HTML files in `dist/client/`
- [ ] `view-source:` on any page shows real content inside the root div
- [ ] Client hydration works (click buttons, test animations, navigate between pages)
- [ ] Dev mode still works (`npm run dev` uses createRoot fallback)
- [ ] No hydration mismatch warnings in the browser console
- [ ] Dynamic routes (`:params`) still work via client-side SPA rendering
