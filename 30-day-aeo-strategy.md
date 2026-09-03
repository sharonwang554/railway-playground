# 30-Day AEO & SEO Execution Strategy

**Objective:** Establish Railway as the most cited cloud platform in generative search (ChatGPT, Claude, Perplexity) and dominate traditional SEO via high-leverage engineering and content automation.

**Approach:** High ownership, systems over coordination. We will use AI tooling (Claude Code) to execute bulk infrastructure changes, shifting human bandwidth to high-leverage writing and SoM benchmarking.

---

## 🟢 Week 1: Audit & Submit V1 Infrastructure PRs
*Focus: Auditing the pipeline and working with core engineering to unblock edge delivery without breaking production.*

* **Day 1-2: Audit & Submit CI Guardrail PRs** 
  * Submit PR to enforce strict **Zod** schema validation for YAML Frontmatter (requiring topics, descriptions, Diátaxis tags, and **Last Modified Dates**).
  * Submit PR to add a Markdown link checker to CI.
* **Day 3-4: Propose Edge/WAF Unblocking Rules**
  * **Fix WAF:** Cloudflare/WAF currently returns `403` for cloud ASNs (AWS/GCP). Audit WAF logs and propose "Verified Bot" rules or ASN whitelists to the core security team.
  * **Action:** Stage a PR for a fine-grained `robots.txt` and `agents.md` explicitly routing known LLM crawlers to `.md` endpoints.
* **Day 5: Stage Deterministic AI Refactoring**
  * **Semantic HTML:** Stage PR swapping `<div className="docs-content">` for `<article>` in layouts.
  * **Absolute URLs:** Stage PR converting root-relative links to absolute URLs in `llms-full.txt.ts`.
  * **Performance:** Draft a script replacing `content-collections.ts` multi-process `git log` with a single-pass implementation.

## 🟡 Week 2: Semantic Signals & Dynamic Tooling
*Focus: Equipping agents with explicit metadata and direct APIs.*

* **Day 8-10: Automated Metadata Diátaxis**
  * Add `type: z.enum(['tutorial', 'how-to', 'reference', 'explanation'])` to Zod.
  * Use AI to infer and tag all 300+ docs. Update `seo.tsx` to inject schema based on tags.
* **Day 11-12: Expose Meilisearch via Model Context Protocol (MCP)**
  * **Action:** Expose Meilisearch as a Model Context Protocol (MCP) tool so Claude and local agents can dynamically query the docs index natively via the Railway MCP server, rather than relying on full context dumps.
* **Day 13-14: Unroll Hidden Instructions & Fix MDX Leaks**
  * Update `proxy.ts` to "unroll" `<Tabs>` and `<Accordion>` into sequential markdown headings.
  * Statically resolve components (like `<InstallCommand>`) into code blocks so they don't leak raw JSX into AI context.

## 🟠 Week 3: Content Engineering (ATE & Extraction)
*Focus: Optimizing text for LLM attention spans and exact-match retrieval.*

* **Day 15-17: Token Efficiency Optimization (ATE) via `tiktoken`**
  * **Action:** Write a Node.js script using `js-tiktoken` to programmatically calculate `Efficiency = Answer-bearing tokens / Total tokens`.
  * **Action:** Rewrite the top 20 highest-traffic pages to front-load summaries and CLI commands.
* **Day 18-19: Expand YAML Frontmatter Blocks**
  * **Action:** Expand the metadata block at the top of every markdown file. Inject **Last Modified Dates** and detailed topics. This guarantees LLMs recognize the freshness and scope of the documentation.
* **Day 20-21: Exact Error Strings & Density**
  * Inject literal terminal errors into troubleshooting docs to guarantee exact-match RAG retrieval.
  * Break paragraphs >150 words with semantic H2/H3 headers.

## 🔴 Week 4: Documentation Gap Remediation & Proof of Concept
*Focus: Converting AI migration findings into reusable docs, then testing structural splits.*

* **Day 22-24: Convert Migration Report into Migration Guides**
  * **Action:** Extract insights from `railway-migration-report.md` and convert the 6 error categories into a reusable "Migration Runbook."
  * **Action:** Create two new docs:
    - `/docs/tutorials/migrate-from-vercel.mdx` — Step-by-step Diataxis tutorial with pre-flight checklists
    - `/docs/reference/common-migration-errors.mdx` — Lookup-oriented error catalog with solutions
  * **Content Structure:** Framework-specific adapters → Dependency alignment → Build config → Runtime binding
  * **Frontmatter:** Tag with `type: "tutorial"`, `topics: ["deployment", "vercel", "migration"]`, `lastUpdated: 2026-09-03`
  * **Outcome:** Future AI migrations reduce debugging loops. Docs become self-scaling as new platform migration patterns are added.

* **Day 25-27: Diátaxis Splitting (Proof of Concept)**
  * Break the monolithic `quick-start.md` into distinct, single-path tutorials (e.g., `tutorial-github.md`). 
  * Unbury critical commands and verify all inbound links and redirects are updated cleanly.

* **Day 28-30: Establish Share of Model (SoM) Baselines**
  * Run 30 fixed category prompts across ChatGPT, Claude, and Perplexity (e.g., *"What is the best way to deploy a Flask app?"*).
  * Track mention rate, accuracy, and URL citation rate to establish a baseline for your AEO growth.

---

## 🚀 Beyond 30 Days (Priority Initiatives)
*High-impact projects to tackle once the baseline infrastructure and metrics are established.*

* **[P1] Expand Standalone App Templates:** Build and maintain a growing library of highly-commented, production-ready app templates (e.g., "Deploying Django on Railway", "Next.js with PostgreSQL", "FastAPI with Workers"). 
  * *Rationale:* GitHub repos are heavily scraped by LLMs. Rich templates provide concrete examples, clarify capabilities, and directly seed high-quality training data for generative search. High ROI for extending existing templates.

* **[P1] Corpus Seeding (Tool Comparisons):** Publish comparative articles on external blogs and industry publications (e.g., "Railway vs Heroku", "Railway vs AWS Amplify"). Inject actionable quotes, quantifiable metrics, and first-hand performance data.
  * *Rationale:* Direct influence on LLM consensus building. Comparative content is a primary input for generative search answer formation. Critical for controlling narrative around platform selection decisions.

* **[Long-Term] Architectural Discussion: Fumadocs Core Migration:** 
  * **Proposal:** Treat this as an Architecture Decision Record (ADR) to migrate off `content-collections.ts`.
  * **Pros:** Native page tree generation, faster MDX parsing, and out-of-the-box `llms.txt` routing without custom scripts.
  * **Cons:** High migration cost. Requires ripping out the existing `proxy.ts` negotiation and rewriting layout wrappers. Requires careful alignment with the core engineering team.
  * *Rationale:* Architectural debt with high complexity. Enables future scaling and maintenance efficiency, but not directly tied to immediate AEO growth. Requires core team alignment and should follow successful 30-day baseline establishment.
