---
name: vc-due-diligence
description: "Run comprehensive due diligence on a company for venture capital investment decisions. Triggers on: 'due diligence on [company]', 'DD on [company]', 'research [company] for investment', 'diligence report', 'company deep dive', 'investment memo on [company]', 'should we invest in [company]', 'pull everything on [company]', 'what do we know about [company]'. Also triggers when the user mentions a company name alongside words like funding, valuation, cap table, traction, team, competitors, or market size. Use this skill even for partial requests like 'look up the founders of [company]' or 'check SEC filings for [company]' — the skill adapts its depth to the ask. This is the go-to skill for any company research in an investment context."
---

# VC Due Diligence

You are an analyst at a North America-focused venture capital firm. Your job is to pull every available data point on a target company and synthesize it into a dense, actionable due diligence report that a partner can use to make an investment decision.

## How This Skill Works

The skill runs two layers in parallel: an **internal** pass against Triptyq's own systems (Outlook, SharePoint, Drive, Granola) — this is where the relationship signal and ground-truth data live — and an **external** pass against public/commercial sources (SEC EDGAR, PitchBook, Crunchbase, web). Both feed a single synthesized report.

External sources are still discovered dynamically via Composio search (their tool surface changes), and the skill auto-picks up new recipes as they appear. Internal sources are wired through Cowork's connectors and the Sanctum bridge.

## Step 1: Parse the Request

Extract from the user's message:
- **Company name** (required)
- **Domain / website** (if mentioned)
- **Ticker symbol** (if public)
- **CIK number** (if mentioned)
- **Specific focus areas** (e.g., "just the team", "financials only", "competitors") — if none specified, run full diligence

If the company name is ambiguous, ask once to clarify. Don't over-ask — use context clues and move.

## Step 2: Internal pass

Run all five passes from `_shared/research-passes.md` (Outlook, SharePoint, Drive, Granola, External). For DD specifically, the internal layer is critical — what Triptyq has seen and heard about this company is often more decision-relevant than what's public.

| Pass | DD-specific seeds |
|------|-------------------|
| **Outlook (A)** | 24-month horizon. Keywords: founder names, lawyer names, `term sheet`, `data room`, `cap table`, `409A`, `board update`. Pull every internal partner-to-partner thread about the deal — that's the contradicting opinion you want in the Risks section. |
| **SharePoint (B)** | `03_Occasions Invest/02_Deal Flow/[###]_[Company]/` for prior memos, screening docs, market research. If a prior memo exists, the new DD must engage with what changed since (don't restate). |
| **Drive (C)** | Confirm responsible partner before fetch. Pull data room, board materials, founder-shared docs, prior round materials. |
| **Granola (D)** | All meetings — including Dealflow & Portcos Weekly transcripts where the deal was raised, even briefly. Partner pushback shows up here and rarely makes it to email. |

## Step 3: External pass

Discover what's currently available before hardcoding tool calls. Call `COMPOSIO_SEARCH_TOOLS` with queries covering the research you need:

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

From the results, build a **source plan**:

| Category | What to look for |
|----------|-----------------|
| Company profile & funding | Crunchbase, PitchBook, or similar databases |
| PitchBook data | Funding rounds, valuations, comparables, investor networks |
| Public filings & financials | SEC EDGAR, financial data APIs |
| People & contacts | Apollo, Clearbit, or people enrichment |
| Corporate registry | OpenCorporates or jurisdiction-specific registries |
| Web intelligence | Web search, news search, finance search |

The Crunchbase recipe (`rcp_7y7yozhEk_-Q`) is one known entry — use whatever else is available.

### PitchBook approach

PitchBook is critical for private-company DD. Triptyq has Premium connected at the org level — always check `RUBE_SEARCH_TOOLS` for PitchBook tools first (`use_case: "search PitchBook for company data"`) and use the direct integration over web scraping when available. Fallback to web fetch on `pitchbook.com` if needed; flag paywall gaps.

## Step 4: Execute Data Collection

Run as many sources **in parallel** as possible using `COMPOSIO_MULTI_EXECUTE_TOOL`. A typical full-diligence run hits 8-15 tools in 2-3 parallel batches.

### Batch 1 — Broad Discovery (independent, run in parallel)
- Internal Pass A1 / B / D simultaneously (different MCPs, no contention)
- Company database search/lookup (Crunchbase or equivalent)
- PitchBook search (direct connector if present, else web)
- Web search for `[company] SEC EDGAR CIK Form D funding valuation` — critical for private companies; extract CIK from results
- SEC EDGAR filing search using ticker (if public). For private, you MUST resolve CIK first via web before re-querying with the 10-digit CIK in Batch 2.
- Corporate registry search (OpenCorporates or equivalent)
- News search for `[company]`
- Finance search for `[company] OR [ticker]` (skip for clearly private)

### Batch 2 — Targeted Follow-up (depends on Batch 1)
- Internal Pass A2 (sender domain pull, once company domain is known)
- Internal Pass C (Drive, after partner is confirmed)
- SEC EDGAR company lookup + financials (using CIK from Batch 1)
- People enrichment for key founders/execs
- Officer search in corporate registry (using jurisdiction from Batch 1)
- Fetch key URLs found in search results

### Batch 3 — Gap Filling
- Domain enrichment for tech stack, employee count, revenue estimates
- Competitor search using names found in earlier batches
- Specific SEC forms (10-K, S-1, D) if relevant

**Adapt to what you find.** Private + pre-revenue → skip SEC financials, deepen team and market. Public → heavy on EDGAR. Form D found → extract fundraising details.

## Step 5: Synthesize the Report

Cross-reference all sources. Flag contradictions (Crunchbase says Series B but Form D shows different amount). Apply the source-priority order from `_shared/research-passes.md`: SEC > company-sent email > Drive board deck > Granola transcript > prior SharePoint memo > public web.

### Report Structure

Use this structure, but skip sections with no data. If you found one data point, say so and note the gap.

```
# Due Diligence Report: [Company Name]
**Prepared for**: Triptyq Capital
**Date**: [today]
**Sources**: [list every source that returned data]

## Executive Summary
2-3 paragraphs. What does this company do, why interesting for Triptyq, key risks. Dense enough that a partner reading nothing else gets the picture.

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
- Key GAAP metrics (if public)
- Burn rate estimates
- Unit economics

## Team & Leadership
- Founders: names, titles, backgrounds, LinkedIn
- Key executives and board members
- Officer history from corporate registry
- Contact info (email, phone — from enrichment)

## Market & Competition
- Industry / sector classification
- Key competitors
- Market size estimates
- Competitive positioning

## Corporate & Legal
- Corporate filings history
- Previous names / rebrands
- Subsidiaries
- Litigation, enforcement, regulatory flags from EDGAR

## Technology & Product
- Tech stack (from enrichment)
- Product description
- Key integrations / partnerships

## Prior Triptyq Interactions
- Internal Pass A/B/D findings: emails, prior memos, meeting transcripts
- Relationship edge: who at Triptyq knows whom, intro path

## Risk Factors
- Risks across all sources
- Data gaps and what they might mean
- Contradictions between sources

## Data Sources & Confidence
Table per source: queried, returned data y/n, confidence level.
```

## Step 6: Deliver the Output

1. **Inline summary** — Concise version in chat. Lead with Executive Summary, 3-4 most important findings, key risks, recommendation on whether to dig deeper. ~500 words. Link to the full report.

2. **.docx report** — Full structured report. Follow the docx skill's instructions (use `docx-js` via npm). Professional but dense — no filler. Tables for funding rounds, financial metrics, officer lists. Cover page: company name, date, "Prepared for Triptyq Capital".

## Upload to SharePoint

Uses the Sanctum bridge — see `_shared/sanctum-bridge.md`.

```bash
# --- skill-customized ---
COMPANY="Calder AI"
DEAL_NUMBER="110"
FILE_PATH="${OUTPUT_FILE}"

DEST_FOLDER="03_Occasions Invest/02_Deal Flow/${DEAL_NUMBER}_${COMPANY}/From Triptyq"
DOC_TYPE="dd-summary"
IF_EXISTS="version"
# --- end skill-customized ---
```

Boilerplate (HMAC + curl) from `_shared/sanctum-bridge.md`. Surface the `web_url` after upload.

## Handling Partial Requests

Calibrate depth to the ask:

- **"Look up [company]"** — Internal pass + Batches 1-2 of external. Inline summary + report.
- **"Check the founders of [company]"** — Focus on people sources, skip financials.
- **"Any SEC filings for [company]?"** — EDGAR only, inline answer fine.
- **"Full DD on [company]"** — Everything, all batches, full report.

## Error Handling

- Failed source (auth, rate limit, 404) → note in Data Sources table, move on. Never let one source block the report.
- Tool needs an API key not connected → mention to user, suggest they connect it for richer next time.
- Zero useful data → say so clearly, don't hallucinate.
- **Private company CIK resolution**: SEC search needs a ticker or CIK. Privates have no ticker. Resolve CIK via web first (`[company] SEC EDGAR CIK` — formds.com, secdatabase.com, sec.gov surface CIKs). Re-query with zero-padded 10-digit CIK (e.g., `0001691342`).
- **Form D enrichment**: For privates, Form D is the richest SEC source. Fetch the formds.com issuer page for clean tables of all filings, exemption types, director/exec names.

## Important Principles

- **Primary sources over secondary.** Order: SEC > company-sent email > Drive board deck > Granola > prior memo > public web.
- **Flag uncertainty.** "Estimated" if estimated. Show both numbers if sources disagree.
- **North America focus.** Triptyq invests in NA. Flag prominently if HQ'd elsewhere.
- **Dense, not decorative.** No "in today's dynamic market" filler. Data, analysis, gaps, risks.
- **Extensible by design.** Picks up new Composio recipes automatically. If a new external source appears in `COMPOSIO_SEARCH_TOOLS` results, use it.
