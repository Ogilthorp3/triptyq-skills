---
name: lp-update-writer
description: |
  Write LP update letters and quarterly reports for Triptyq Capital fund investors. Use this skill whenever someone needs to draft an LP letter, quarterly update, annual report, fund performance summary, or any communication to limited partners. Triggers on "LP update", "quarterly letter", "write to our LPs", "investor update", "fund update", "report to investors", "LP letter", or when portfolio metrics need to be packaged for fund investors. Also use for Fund II fundraising updates to prospective LPs.
---

# Triptyq Capital — LP Update Writer

## Philosophy

LP updates are trust-building documents. They should be honest, concise, and demonstrate that the GPs are thoughtful stewards of capital. Write like a partner talking to a trusted advisor over coffee — direct, no fluff, no spin. Bad news delivered clearly builds more trust than good news delivered vaguely.

## Before Writing

### Gather Data

Run the relevant passes from `_shared/research-passes.md`. LP updates rely heavily on internal sources — public sources are rarely useful here.

| Pass | LP-update seeds |
|------|-----------------|
| **Outlook (A)** | Last 90 days. Search for `board update`, `monthly update`, `investor update` from each portco's domain. This is the raw material for the Portfolio Highlights section — pull the latest from each company. |
| **SharePoint (B)** | `02b_Fund II (2025)/02_FINANCIAL/` for fund financials, NAV, capital called/deployed. `03_Occasions Invest/01_Portco/[##]_[Company]/` for each portco's latest financial reports. |
| **Drive (C)** | Run for any portco where the GP receiving the latest board deck is the writer. Confirm partner before fetch. |
| **Granola (D)** | Recent board meeting transcripts for material milestones or risks. |

Plus LP-specific sources not in the standard helper:
- **Affinity CRM**: Pull deal flow metrics (companies reviewed, meetings taken, term sheets, investments made).
- **Calendar**: Check upcoming events, conferences, LP meetings to mention in the Outlook section of the letter.

### Determine the Update Type

| Type | Cadence | Length | Audience |
|------|---------|--------|----------|
| Quarterly letter | Q1/Q2/Q3/Q4 | 2-3 pages | All LPs |
| Annual report | Year-end | 5-8 pages | All LPs |
| Fundraising update | As needed | 1-2 pages | Prospective LPs |
| Deal announcement | Per investment | 1 page | All LPs |
| Ad hoc update | As needed | 1 page | Select LPs |

## Document Structure (Quarterly Letter)

### Opening (2-3 sentences)
- Quarter context and market environment (one line)
- Fund performance headline (one line)
- Tone-setting statement

### Portfolio Highlights
For each active portco, 2-3 sentences covering:
- Key milestone or traction metric from the quarter
- What's next
- Any concerns or support needed

### New Investments (if any)
- Company name, what they do, why we invested (3-4 sentences each)
- Thesis connection to entertainment × spatial × AI

### Fund Metrics Table
| Metric | Current | Prior Quarter |
|--------|---------|---------------|
| Fund Size | | |
| Capital Called | | |
| Capital Deployed | | |
| # Portfolio Companies | | |
| Realized / Unrealized Value | | |
| TVPI / DPI | | |

### Deal Flow Summary
- Companies reviewed, meetings taken, term sheets received
- Pipeline health and sector trends

### Outlook
- Market perspective (2-3 sentences)
- Team updates, upcoming conferences, LP events

### Closing
- Thank you, availability for calls, next reporting date

## Design

Follow the `triptyq-investment-memo` brand tokens: RED (`C8102E`), Georgia body, Arial headers, justified text. Triptyq logo on page 1. Use the `docx` skill for generation.

## Tone

- First person plural ("we")
- Bilingual consideration: Triptyq LPs include French-speaking Quebecois investors. Offer to write in French if requested.
- Honest about challenges — "Company X is behind plan on revenue but ahead on product" beats silence.
- Specific over vague — "Revenue grew 40% QoQ to $180K MRR" beats "strong momentum continues".

## Upload to SharePoint

LP update folder convention is being confirmed with Charles — current default is `02b_Fund II (2025)/02_FINANCIAL/02_DECK/`, but for LP-only correspondence Charles may want a dedicated `LP/` subfolder. Ask before bulk uploads.

Uses the Sanctum bridge — see `_shared/sanctum-bridge.md`.

```bash
# --- skill-customized ---
QUARTER="2026-Q1"                                # or "2025-annual", "fundii-fundraise", etc.
FILE_PATH="${OUTPUT_FILE}"

DEST_FOLDER="02b_Fund II (2025)/02_FINANCIAL/02_DECK"   # CONFIRM with Charles
DOC_TYPE="lp-update"
IF_EXISTS="version"
# --- end skill-customized ---
```

Boilerplate (HMAC + curl) from `_shared/sanctum-bridge.md`. After upload, surface the `web_url`. For LP letters, also offer to draft the email body that delivers the link to the LP list — but do not send automatically.
