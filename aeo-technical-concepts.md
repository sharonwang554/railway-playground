# AEO Technical Concepts & Pipeline Mapping

This document explains the underlying technical concepts of Agent Engine Optimization (AEO) and maps how the items in the 30-Day Strategy directly improve the AI ingestion pipeline.

---

## 1. The AI Ingestion Pipeline
To understand AEO, you must understand the sequential pipeline an AI agent uses to answer a user's prompt. If a site fails at Step 1, optimizing Step 4 is useless.

1. **Discovery:** The agent must find the relevant URL.
2. **Access:** The agent must be allowed to connect to the server.
3. **Extraction:** The agent must parse the data into readable text.
4. **Retrieval (RAG):** The agent must match the user's prompt to the correct chunk of text.
5. **Generation:** The agent writes the answer to the user.

---

## 2. Strategy Mapping: How Our Fixes Improve the Pipeline

### Step 1: Discovery (Finding the URL)
*Before an AI can read your docs, it usually queries a traditional search engine API (like Bing) to find the URL.*
* **Tool Comparison Articles (Corpus Seeding):** AI models rely heavily on domain authority and backlinks (PageRank) to decide which URL to scrape first. Publishing external articles ensures Railway ranks #1 when an agent searches "Railway vs Heroku".
* **`robots.txt` & `agents.md`:** Explicitly tells asynchronous indexing bots exactly where the AI-optimized files (`llms.txt`) live, bypassing the UI entirely.

### Step 2: Access (The Edge & WAF)
*The physical connection between the AI's server and your documentation.*
* **Concept - The Edge:** Servers distributed globally (Cloudflare/Vercel) that handle requests before they reach your Next.js application.
* **Concept - WAF (Web Application Firewall):** The security layer sitting at the Edge.
* **The Fix - WAF Unblocking:** Because AI bots operate from cloud data centers (AWS/GCP), WAFs frequently block them as malicious DDoS bots. Fixing this ensures the AI doesn't receive a `403 Forbidden` error.

### Step 3: Extraction (Reading the Data)
*Converting a complex React website into pure, readable text.*
* **Concept - Content Negotiation:** Railway's `proxy.ts` detects the bot's `User-Agent` and serves pure Markdown instead of HTML.
* **Concept - DOM Scraping:** If the bot parses HTML, it uses algorithms like Mozilla Readability to strip away noise.
* **The Fix - Semantic HTML5 (`<article>`):** Helps DOM scrapers isolate the tutorial content from the sidebar navigation.
* **The Fix - Unrolling MDX (`<Tabs>`):** Interactive React components hide text from scrapers. Unrolling them ensures commands aren't lost in the extraction phase.

### Step 4: Retrieval (RAG & Semantic Matching)
*Once the text is extracted, the AI uses Vector Embeddings to match the text to the user's prompt.*
* **Concept - Model Context Protocol (MCP):** An open standard that allows AI models to connect securely to local or remote data sources.
* **The Fix - MCP Meilisearch Integration:** Instead of forcing agents to scrape HTML or download massive `.txt` files, exposing Meilisearch as an MCP tool provides a standardized interface for agents like Claude to run precise semantic queries directly against Railway's docs.
* **The Fix - Expand YAML Frontmatter:** AI systems heavily rely on the metadata block at the very top of `.md` files. Expanding this block to include explicit topics, intent, and **Last Modified Dates** guarantees the AI knows exactly what the chunk covers and prioritizes it for freshness.
* **The Fix - AEO Token Efficiency (ATE):** If a page is 80% narrative and 20% commands, the semantic meaning is diluted. Front-loading answers concentrates the vector embedding, making it highly retrievable.
* **The Fix - Exact Error Strings:** When a user pastes a terminal error, the agent searches for that exact semantic string. Injecting exact errors guarantees a 1:1 match in the RAG database.

---

## 3. Zod & CI Validation

To ensure AEO is maintained at scale, we use **Zod**—a TypeScript-first schema declaration and validation library.

In documentation repositories, developers frequently forget to update the YAML Frontmatter block when editing files. By enforcing a Zod schema in your CI/CD pipeline, the build will physically fail if a developer attempts to merge a Markdown file that is missing required AEO metadata, such as:
*   `lastUpdated`: (Required to signal freshness to LLMs).
*   `type`: (e.g., enforcing Diátaxis tags like `tutorial` vs `reference`).
*   `topics`: (Ensures the file is indexed correctly by Meilisearch and Agents).

---

## 4. Share of Model (SoM)

In traditional SEO, marketers measure "Share of Voice" (How much of the front page of Google do you own?). 
In AEO, we measure **Share of Model (SoM)**. 

SoM is the metric tracking how often a specific brand (Railway) is recommended by major LLMs (ChatGPT, Claude, Perplexity) when a user asks an unbranded category question. 
*   *Example Prompt:* "What is the best platform to deploy a Node.js Docker container?"
*   *Measurement:* Run this prompt 50 times a month across 3 different models. If Railway is recommended 15 times, Heroku 20 times, and Render 15 times, your Share of Model is 30%. 
The goal of this 30-Day strategy is to definitively increase Railway's SoM by making the data perfectly machine-readable.

---

## 5. How AI Search Algorithms Work

### Do agents use "Best-First Search" or "PageRank"?
They use a combination of both, depending on the stage:
1. **The Initial Search (PageRank):** Real-time agents (Perplexity, ChatGPT Search) do not crawl the web live. They ping the **Bing Search API** or **Google Search API** in the background. This means traditional SEO (domain authority, PageRank, backlinks) absolutely dictates which URLs the agent decides to look at first.
2. **The Internal Retrieval (Semantic Search):** Once the agent scrapes your URL, it chunks the text and uses **Vector Embeddings**. It mathematically scores which chunks of text are most semantically similar to the user's prompt (Cosine Similarity). This is closer to a "Best-First" heuristic, retrieving the highest-scoring text chunks to feed to the LLM.

### Do they prefer text search over others?
**Yes.** Large Language Models (LLMs) are fundamentally text-prediction engines. 
While they *can* parse complex HTML DOMs, it wastes their context window and dilutes their attention mechanism. They heavily prefer **raw Markdown, plain text, or JSON**. 

---

## 6. Architectural Decision Example: Fumadocs Core

Because AI tools heavily prefer pure markdown text, the frontend frameworks powering documentation are evolving. A major long-term discussion for Railway is whether to migrate from custom scripts to a natively AEO-optimized framework like **Fumadocs core**.

*   **Pros (Why we should add it):**
    *   **Native AEO:** It has out-of-the-box routing for `/llms.txt` and `/llms-full.txt`.
    *   **Automated Page Tree:** It automatically infers the navigation tree from the file system, eliminating the need for heavy, custom git-log subprocesses.
    *   **Agent Search API:** It integrates directly with Orama local search, making it trivial to expose a REST API for agents to query.
*   **Cons (Why it requires discussion):**
    *   **High Migration Cost:** It requires ripping out Railway's brilliant `proxy.ts` content negotiation.
    *   **Component Refactoring:** All custom React layout wrappers and MDX components would need to be re-wired to fit the Fumadocs provider structure.
    *   **Vendor Lock-in:** It ties the documentation pipeline heavily to a specific open-source framework rather than Railway's own internal tooling.
