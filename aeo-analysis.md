# AEO Analysis: Railway Documentation

## 1. Current State (Strengths)
Railway has a mature AEO foundation:
* **Content Negotiation:** `proxy.ts` auto-serves Markdown to 14+ AI crawlers.
* **Corpus Dumps:** Dynamic `llms.txt` and `llms-full.txt`.
* **JSON-LD Schema:** Auto-generates Organization, Breadcrumbs, Article, and FAQPage schemas.

---

## 2. Gap Analysis (By Domain)

### 🏗️ Infrastructure & Delivery
* **[P0] WAF Blocking AI Bots:** Cloudflare/Edge returns `403` for cloud ASNs (AWS, GCP). Major AI crawlers are blocked before reaching `proxy.ts`. 
  * *Fix:* Audit WAF logs and propose "Verified Bot" rules or ASN whitelists to the core security team.
* **[P0] Fine-Grained Search Discovery:** Relying entirely on a wild-card `robots.txt` misses the opportunity to route specific bots.
  * *Fix:* Create a strict `robots.txt` directing known AI crawlers to the `/llms.txt` dumps, and implement an `agents.md` or `.well-known/ai-plugin.json`.
* **[Long-Term] Architectural Discussion: Fumadocs Core Migration:** The current `content-collections.ts` setup is heavy and requires manual `llms.txt` maintenance.
  * *Discussion:* We should evaluate migrating to `Fumadocs core` to natively automate MDX parsing. 
  * *Pros:* Native page tree data generation, out-of-the-box `llms.txt` routing, eliminates 300+ `git log` sub-processes natively.
  * *Cons:* Heavy migration. Requires ripping out existing `proxy.ts` negotiation and rewriting React layout wrappers. Requires careful team discussion.

### 🧠 Content Architecture & Token Efficiency
* **[P1] AEO Token Efficiency Ratio (ATE):** The ultimate AEO metric is `Efficiency = Answer-bearing tokens / Total tokens`.
  * *Fix:* Integrate `js-tiktoken` into a CI Node script to programmatically measure the token ratio of high-traffic pages. Front-load CLI commands into the first 500 tokens.
* **[P1] Expand YAML Frontmatter Blocks:** The metadata block at the top of every `.md` file is crucial for automated search and retrieval.
  * *Fix:* Expand the frontmatter to require rich search metadata: explicit topics, Diátaxis intent, and **Last Modified Dates** so AI systems prioritize fresh content.
* **[P1] Unroll Hidden Instructions:** Critical commands are hidden behind `<Tabs>` and `<Accordion>` components.
  * *Fix:* Update MDX serializers to "unroll" interactive components into sequential markdown headings for AI endpoints.
* **[P1] Zod Schema Guardrails:** Without CI validation, developers forget to update the frontmatter block.
  * *Fix:* Enforce strict Zod schema validation on the frontmatter so the build fails if `lastUpdated` or `type: z.enum(['tutorial', 'how-to', 'reference', 'explanation'])` is missing.
* **[P1] Semantic HTML5:** HTML falls back to generic `<div>`s, confusing DOM scrapers.
  * *Fix:* Swap `<div className="docs-content">` to `<article>`.

### 🛠️ Agent Tooling & Code
* **[P1] Model Context Protocol (MCP) Search:** Agents shouldn't have to ingest the full 300-page context dump.
  * *Fix:* Expose Meilisearch as a Model Context Protocol (MCP) tool so Claude and local agents can dynamically query the docs natively via the Railway MCP server.
* **[P0] MDX Component Leaks:** The `.md` endpoint fails to resolve components like `<InstallCommand>`, leaking raw JSX.
  * *Fix:* Statically resolve critical MDX components into code blocks before serving to AI.
* **[Long-Term] Standalone App Examples:** Models and users need clean references.
  * *Fix:* Build standalone, highly-commented app templates to demonstrate capabilities and seed GitHub repos for LLM scraping.

### 🎯 Long-Tail & Corpus Seeding
* **[P2] Exact Error Strings:** Troubleshooting docs currently paraphrase errors.
  * *Fix:* Inject exact terminal error strings for 1:1 LLM matching.
* **[P2] Absolute URLs:** Root-relative links break when directly cited by LLMs.
  * *Fix:* Convert `/docs` to `https://docs.railway.com/docs` in markdown dumps.
* **[Long-Term] Actionable Quotes & Tool Comparisons:** LLMs need definitive consensus markers and evaluation-phase content.
  * *Fix:* Publish comparison articles (e.g., "Railway vs Heroku") and inject hard metrics (*"provisions in 10s"*) and authoritative quotes.

### 📦 Migration & Documentation Scalability
* **[P1] AI-Assisted Migration with Zero-Touch Documentation:** The Vercel-to-Railway migration (via AI agents fed the docs site) uncovered a single critical documentation gap.
  * *Finding:* Railway's documentation correctly describes Nixpacks auto-detection of Astro projects and static site serving, but **fails to warn developers about removing Vercel-specific adapters** before deployment.
  * *Root Cause:* The docs lack a "Migration Checklist" section that consolidates platform-specific lock-in artifacts (adapters, analytics, config files) into a single, discoverable location.
  * *Fix:* Add dedicated migration guides following this structure:
    - **Pre-flight Checklist:** Framework-specific adapters to remove (e.g., `@astrojs/vercel`, `@vercel/analytics`)
    - **Dependency Alignment:** Node.js/runtime version requirements per framework version
    - **Build Configuration:** Critical files to delete or modify (`vercel.json`, `start` scripts)
    - **Runtime Binding:** Common "Application failed to respond" patterns and solutions
  * *Deliverables:* 
    - `/docs/tutorials/migrate-from-vercel.mdx` (step-by-step, Diataxis tutorial)
    - `/docs/reference/common-migration-errors.mdx` (lookup-oriented, error catalog)
    - Update frontmatter: `type: "tutorial"`, `topics: ["deployment", "vercel", "migration"]`, `lastUpdated: 2026-09-03`
  * *Outcome:* Replicable migration patterns reduce AI debugging loops. Future platform migrations (AWS → Railway, Netlify → Railway) will reference the same structure, making documentation self-scaling as the ecosystem grows.

---

## 3. Implementation Roadmap
*(See 30-Day Strategy for execution timeline)*
