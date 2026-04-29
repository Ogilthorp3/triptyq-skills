---
name: portfolio-monitoring
description: |
  Monitor Triptyq Capital portfolio companies and generate status dashboards. Use this skill to check on portco health, flag issues, track milestones, prep for board meetings, or generate a portfolio overview. Triggers on "how are our portcos doing", "portfolio update", "check on [company]", "board meeting prep for [company]", "portfolio dashboard", "portco status", "any red flags in the portfolio", "runway check", or when someone needs a consolidated view of portfolio company activity and health.
---

# Triptyq Capital — Portfolio Monitoring

## Portfolio Companies

Check `03_Occasions Invest/01_Portco/` on SharePoint for the current list. As of early 2026, the portfolio includes 14+ companies across Fund I.

## Monitoring Cadence

| Check | Frequency | Source |
|-------|-----------|--------|
| Email activity | Weekly | `_shared/research-passes.md` Pass A |
| News mentions | Weekly | `_shared/research-passes.md` Pass E (web) |
| Financial updates | Monthly/Quarterly | Pass B (SharePoint portco folders) |
| Board meetings | Per schedule | Calendar + Pass D (Granola) |
| Runway / burn | Quarterly | Financial reports in SharePoint |
| Milestone tracking | Ongoing | Affinity + email |

## Single Company Check

When someone asks "how is [company] doing?", run the relevant subset of `_shared/research-passes.md`:

| Pass | Portco-monitoring seeds |
|------|-------------------------|
| **Outlook (A)** | 30-day horizon. A1 by company name, A2 by company domain. Keywords: `monthly update`, `board update`, `customer win`, `hiring`, `runway`. |
| **SharePoint (B)** | `03_Occasions Invest/01_Portco/[##]_[Company]/` — latest documents in their portco folder. |
| **Drive (C)** | Confirm responsible partner before fetch. Pull recent board decks. |
| **Granola (D)** | Recent meetings involving the company. |
| **External (E)** | Quick web search: news, product launches, hiring spikes/drops on LinkedIn. |

Plus Affinity for CRM notes and interaction history (still Composio-mediated).

Output a 1-paragraph status with: last contact date, latest milestone, any concerns, next scheduled touchpoint.

## Portfolio Dashboard

When someone asks for the full portfolio overview, run the single-company check **in parallel** across every portco. Aggregate results into the dashboard format below.

### For Each Company
```
[Company Name] | [Status: GREEN/YELLOW/RED]
Last contact: [date]
Latest update: [1 sentence]
Key metric: [revenue, users, or milestone]
Next touchpoint: [board meeting, check-in, or deadline]
Flag: [any concern, or "none"]
```

### Traffic Light System
- **GREEN**: On track, regular communication, no concerns
- **YELLOW**: Behind on a milestone, communication gap >30 days, or minor concern
- **RED**: Runway <6 months, founder conflict, missed targets, or material risk

### Aggregate Metrics
- Total portfolio value (if available)
- Companies by status (GREEN/YELLOW/RED count)
- Average days since last contact
- Upcoming board meetings this month

## Board Meeting Prep

When prepping for a specific company's board meeting:

1. Pull all documents from their SharePoint folder (Pass B)
2. Search email for founder correspondence (last 90 days, Pass A)
3. Pull recent board materials from Drive (Pass C — confirm partner)
4. Granola transcripts of previous board meetings (Pass D)
5. Quick web search for competitive landscape changes (Pass E)
6. Generate a 1-page brief: company status, key metrics, discussion topics, questions to ask.

## Upload to SharePoint

Uses the Sanctum bridge — see `_shared/sanctum-bridge.md`.

```bash
# --- skill-customized ---
COMPANY="Calder AI"
PORTCO_NUMBER="03"                       # from the existing portco folder; never auto-increment
FILE_PATH="${OUTPUT_FILE}"

DEST_FOLDER="03_Occasions Invest/01_Portco/${PORTCO_NUMBER}_${COMPANY}"
DOC_TYPE="portco-status"
IF_EXISTS="version"
# --- end skill-customized ---
```

Boilerplate (HMAC + curl) from `_shared/sanctum-bridge.md`. Surface the `web_url` after upload.

For the full portfolio dashboard (cross-portco overview), file under `03_Occasions Invest/01_Portco/` directly with `DOC_TYPE="portco-status"` and a filename like `Portfolio_Dashboard_2026-Q1.xlsx`.
