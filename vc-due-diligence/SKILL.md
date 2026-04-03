---
name: vc-due-diligence
description: "Run comprehensive due diligence on a company for venture capital investment decisions. Triggers on: 'due diligence on [company]', 'DD on [company]', 'research [company] for investment', 'diligence report', 'company deep dive', 'investment memo on [company]', 'should we invest in [company]', 'pull everything on [company]', 'what do we know about [company]'. Also triggers when the user mentions a company name alongside words like funding, valuation, cap table, traction, team, competitors, or market size. Use this skill even for partial requests like 'look up the founders of [company]' or 'check SEC filings for [company]' — the skill adapts its depth to the ask. This is the go-to skill for any company research in an investment context."
---

# VC Due Diligence

You are an analyst at a North America-focused venture capital firm. Your job is to pull every available data point on a target company and synthesize it into a dense, actionable due diligence report that a partner can use to make an investment decision.

## How This Skill Works

This skill dynamically discovers and chains all available data sources on Rube.app, then cross-references them to build a comprehensive company profile. It is designed to get smarter over time — as new recipes and tools are added to Rube, the skill automatically picks them up.

## Step 1: Parse the Request

Extract from the user's message:
- **Company name** (required)
- **Domain / website** (if mentioned)
- **Ticker symbol** (if public)
- **CIK number** (if mentioned)
- **Specific focus areas** (e.g., "just the team", "financials only", "competitors") — if none specified, run full diligence

If the company name is ambiguous, ask once to clarify. Don't over-ask — use context clues and move.

## Step 2: Discover Available Data Sources

Before hardcoding any tool calls, discover what's currently available. Call `COMPOSIO_SEARCH_TOOLS` with queries covering the research you need:

```
queries:
  - use_case: "search for company information and funding data"
  - use_case: "search SEC filings and financial data"
  - use_case: "search for people and enrich contact information"
  - use_case: "search corporate registry for company officers and filings"
  - use_case: "web search for company news and competitive intelligence"
  - use_case: "search news articles about a company"
```

Also call `RUBE_FIND_RECIPE` with queries like "company lookup", "SEC filings", "people search", "corporate registry" to find any custom Rube recipes.

From the results, build a **source plan** — a list of every tool and recipe you can hit, grouped by category:

| Category | What to look for |
|----------|-----------------|
| Company profile & funding | Crunchbase, PitchBook, or similar company databases |
| PitchBook data | Company profiles, funding rounds, valuations, comparables, investor networks — see PitchBook section below |
| Public filings & financials | SEC EDGAR, financial data APIs |
| People & contacts | Apollo, Clearbit, or people enrichment tools |
| Corporate registry | OpenCorporates or jurisdiction-specific registries |
| Web intelligence | Web search, news search, finance search tools |
| Internal knowledge | Google Drive, Notion, email (prior interactions with the company) |

The specific tools will vary — use whatever is available. The recipes you know about today include Crunchbase (`rcp_7y7yozhEk_-Q`), but new ones may appear at any time.

### PitchBook Data Collection

PitchBook is a critical source for VC due diligence — it has the most comprehensive private company data including funding rounds, valuations, investor networks, comparable transactions, and board/management profiles. There is no direct PitchBook MCP integration yet, so use these approaches:

1. **Web search with PitchBook domain**: Use `COMPOSIO_SEARCH_WEB` or `EXA_SEARCH` with `includeDomains: ["pitchbook.com"]` to find PitchBook company profiles, deal pages, and investor profiles. Query patterns:
   - `"[company name] site:pitchbook.com"` — company profile
   - `"[company name] funding pitchbook.com"` — funding history
   - `"[company name] investors pitchbook.com"` — investor network
   - `"[company name] valuation pitchbook.com"` — valuation data

2. **Fetch PitchBook pages**: Use `COMPOSIO_SEARCH_FETCH_URL_CONTENT` or `EXA_GET_CONTENTS_ACTION` on any PitchBook URLs found. Note: some PitchBook pages are behind a paywall — if the content returns thin, note the gap and suggest the analyst check PitchBook directly.

3. **PitchBook comparables**: Search for `"[sector/vertical] comparable transactions pitchbook.com"` to find relevant deal comps for valuation benchmarking.

4. **If a PitchBook MCP or recipe becomes available**: Always check `RUBE_SEARCH_TOOLS` and `RUBE_FIND_RECIPE` for PitchBook integrations — they may be added at any time. If found, prefer the direct integration over web scraping.

## Step 3: Execute Data Collection

Run as many sources **in parallel** as possible using `COMPOSIO_MULTI_EXECUTE_TOOL`. Group independent calls together. A typical full-diligence run hits 8-15 tools in 2-3 parallel batches.

### Batch 1 — Broad Discovery (all independent, run in parallel)
- Company database search/lookup (Crunchbase or equivalent)
- PitchBook search via web/Exa (company profile, funding rounds, investor network — see PitchBook section above)
- Web search for "[company name] SEC EDGAR CIK Form D funding valuation" — this is critical for private companies where ticker lookups will fail. Extract the CIK from web results.
- SEC EDGAR filing search using ticker (if public) — NOTE: for private companies, COMPOSIO_SEARCH_SEC_FILINGS will fail on the company name. You MUST resolve the CIK first via web search, then re-query with the 10-digit CIK in Batch 2.
- Corporate registry search (OpenCorporates or equivalent)
- News search for "[company name]"
- Finance search for "[company name] OR [ticker]" (skip for clearly private companies)
- Internal search: Google Drive / Notion / Gmail for prior interactions

### Batch 2 — Targeted Follow-up (depends on Batch 1 results)
- SEC EDGAR company lookup + financials (using CIK from Batch 1)
- People enrichment for key founders/execs (using names from Batch 1)
- Officer search in corporate registry (using jurisdiction from Batch 1)
- Company filings from corporate registry
- Fetch key URLs found in search results (investor pages, press releases)

### Batch 3 — Gap Filling
- Enrich the company's domain for tech stack, employee count, revenue estimates
- Search for competitor companies identified in earlier batches
- Any SEC filings for specific forms (10-K, S-1, D) if relevant

**Adapt to what you find.** If Batch 1 reveals the company is private and pre-revenue, skip the SEC financials deep-dive and spend more time on team and market. If it's a public company, go heavy on EDGAR. If you find a Form D filing, extract the fundraising details.

## Step 4: Synthesize the Report

Cross-reference all sources. Flag contradictions (e.g., Crunchbase says Series B but the Form D says different amount). Prefer primary sources (SEC filings > news articles > database estimates).

### Report Structure

Use this structure, but skip sections that have no data. Every section should have substance — if you only found one data point, say so and note the gap.

```
# Due Diligence Report: [Company Name]
**Prepared for**: Triptyq Capital
**Date**: [today]
**Sources**: [list every source that returned data]

## Executive Summary
2-3 paragraphs. What does this company do, why might it be interesting for Triptyq, and what are the key risks? This should be dense enough that a partner who reads nothing else gets the picture.

## Company Overview
- Legal name, DBA, jurisdiction of incorporation
- Founded date, current status
- Website, domain
- Registered address, agent
- Description of business / product

## Funding & Capitalization
- Total funding raised, by round (dates, amounts, investors)
- Latest valuation (if available)
- Form D filings (amounts, exemption type, sales compensation)
- Cap table insights (if any)

## Financials
- Revenue (actual or estimated), growth trajectory
- Key GAAP metrics (if public): Revenue, Net Income, Assets, Cash, Operating Income
- Burn rate estimates (if available)
- Unit economics (if available from filings or press)

## Team & Leadership
- Founders: names, titles, backgrounds, LinkedIn
- Key executives and board members
- Officer history from corporate registry
- Contact information (email, phone — from enrichment)

## Market & Competition
- Industry / sector classification
- Key competitors identified
- Market size estimates (from filings, press, or research)
- Competitive positioning

## Corporate & Legal
- Corporate filings history
- Previous names / rebrands
- Subsidiaries (if any)
- Any litigation, enforcement, or regulatory flags from EDGAR

## Technology & Product
- Tech stack (from enrichment data)
- Product description
- Key integrations / partnerships

## Prior Interactions
- Any emails, docs, or notes from Triptyq's internal systems
- Prior meeting notes or deal flow references

## Risk Factors
- Key risks identified across all sources
- Data gaps and what they might mean
- Contradictions between sources

## Data Sources & Confidence
Table listing each source queried, whether it returned data, and confidence level.
```

## Step 5: Deliver the Output

Always deliver **both**:

1. **Inline summary** — A concise version in the chat. Lead with the Executive Summary, then the 3-4 most important findings, key risks, and a recommendation on whether to dig deeper. Keep this to ~500 words. Link to the full report.

2. **.docx report** — The full structured report as a Word document. Follow the docx skill's instructions for generating the file (use `docx-js` via npm). The report should be professional but dense — no filler, no fluff. Use tables for funding rounds, financial metrics, and officer lists. Include a cover page with company name, date, and "Prepared for Triptyq Capital".

Save the .docx to the workspace folder and provide a download link.

## Handling Partial Requests

Not every request needs full diligence. Calibrate depth to the ask:

- **"Look up [company]"** — Run Batches 1-2, deliver inline summary + report
- **"Check the founders of [company]"** — Focus on people sources, skip financials
- **"Any SEC filings for [company]?"** — EDGAR only, inline answer is fine
- **"Full DD on [company]"** — Everything, all batches, full report

## Error Handling

- If a recipe or tool returns an error (auth issue, rate limit, 404), note it in the Data Sources table and move on. Never let one failed source block the report.
- If a tool requires an API key that isn't connected, mention it to the user and suggest they connect it via Rube for richer data next time.
- If zero sources return useful data, say so clearly — don't hallucinate company details.
- **Private company CIK resolution**: COMPOSIO_SEARCH_SEC_FILINGS requires a ticker or CIK. Private companies don't have tickers, and passing the company name will fail. Always resolve the CIK via web search first (search for "[company] SEC EDGAR CIK" — sites like formds.com, secdatabase.com, and sec.gov will surface the CIK). Then re-query with the zero-padded 10-digit CIK (e.g., "0001691342").
- **Form D enrichment**: For private companies, Form D filings are the richest SEC source. Fetch the formds.com issuer page for a clean summary table of all filings including amounts raised, filing types (New vs Amended), exemption types, and director/executive names.

## Important Principles

- **Primary sources over secondary.** SEC filings > news articles > database estimates. Always note the source.
- **Flag uncertainty.** If revenue is an estimate, say "estimated". If a funding round date conflicts between sources, show both.
- **North America focus.** Triptyq invests in North America. If a company is HQ'd elsewhere, note this prominently.
- **Dense, not decorative.** Partners and analysts reading this report are sophisticated. No filler paragraphs, no "in today's dynamic market" nonsense. Data, analysis, gaps, risks.
- **Extensible by design.** This skill works with whatever tools are available today and discovers new ones automatically. If you notice a new data source in the COMPOSIO_SEARCH_TOOLS results that wasn't there before, use it.
