---
name: deal-screening
description: |
  Quick first-look screening of a deal for Triptyq Capital's weekly pipeline review. Use this skill for initial deal assessment before committing to full due diligence. Triggers on "screen this deal", "first look at [company]", "should we take a meeting", "quick assessment", "pipeline review", "does this fit our thesis", "is this worth a deeper look", or when a new company enters the pipeline and needs a go/no-go for the next partners meeting. Lighter than vc-due-diligence — this is the 15-minute filter, not the 2-hour deep dive.
---

# Triptyq Capital — Deal Screening

## Purpose

The weekly Dealflow & Portcos meeting needs a fast, structured way to assess new deals. This skill produces a 1-page screening memo that answers one question: should we spend time on this?

## The Three Gates

Every deal must pass three gates to proceed. If it fails any gate, it's a pass (with a note on why).

### Gate 1: Thesis Fit
Does this connect to entertainment × spatial computing × AI?
- Direct fit: the company builds in one of these verticals
- Adjacent fit: infrastructure that enables these verticals (data, tools, platforms)
- No fit: interesting but outside our mandate

### Gate 2: Team Signal
Do the founders have an unfair advantage?
- Prior exits (especially to FAANG or strategic acquirers)
- Deep domain expertise (not just "worked at Google for 2 years")
- Relationship to Triptyq network (Denis, Jaron, portfolio founders, LPs)
- Repeat founders vs first-time

### Gate 3: Deal Economics
Is the math reasonable?
- Stage vs valuation (seed at $20M = fine, seed at $500M = needs exceptional justification)
- Round structure (lead investor quality, allocation available)
- Geography (North America preferred, Singapore/international = extra diligence)

## Output Format (1 Page)

```
DEAL SCREENING: [Company Name]
Date: [today]  |  Source: [who referred]  |  Screened by: [partner]

THESIS FIT:     [DIRECT / ADJACENT / NO FIT]
TEAM SIGNAL:    [STRONG / MODERATE / WEAK]
DEAL ECONOMICS: [ATTRACTIVE / FAIR / STRETCH]

VERDICT: [TAKE THE MEETING / WATCH / PASS]

What they do: [2 sentences max]
Why now: [1 sentence — market timing or catalyst]
Team: [founder names + most impressive credential each, 1 line per founder]
Round: [stage, amount, valuation, lead if known]
Thesis connection: [1-2 sentences linking to entertainment × spatial × AI]
Key question: [the single most important thing to validate in a first meeting]
Red flag: [if any — jurisdiction, conflict, valuation, missing info]
```

## Research (15-Minute Mode)

Run the **fast subset** of `_shared/research-passes.md`. This is the 15-minute filter, not the 2-hour deep dive.

| Pass | Screening seeds |
|------|-----------------|
| **Outlook (A)** | A1 only — broad sweep on company name, 6-month horizon. Skip the sender-domain pull unless A1 surfaces a direct email from the company. Have we seen this deal before? Is there an intro path? |
| **SharePoint (B)** | Quick check whether a `[###]_<Company>` folder already exists. If yes, the deal isn't new — note that and route to whoever opened it. |
| **Drive (C)** | Skip — at screening stage, there's no signed MNDA yet, no board materials. |
| **Granola (D)** | Skip — no meetings yet. |
| **External (E)** | Web search: 2-3 queries (company + founders + funding history). Crunchbase / PitchBook quick check via the same tools `vc-due-diligence` uses, but pull only top-line: amount raised, latest valuation, lead investor. |

Do NOT read legal docs, pull SEC filings, or analyze cap tables at this stage. That's for the `vc-due-diligence` skill after the screening passes.

## After Screening

Three paths depending on the verdict:

**TAKE THE MEETING** — Open a deal folder on SharePoint and file the screening doc. Use the Sanctum bridge:

```bash
# --- skill-customized ---
COMPANY="Calder AI"
DEAL_NUMBER="111"                        # claim next available number; ask user to confirm
FILE_PATH="${OUTPUT_FILE}"               # the 1-page screening .docx or .pdf

DEST_FOLDER="03_Occasions Invest/02_Deal Flow/${DEAL_NUMBER}_${COMPANY}/From Triptyq"
DOC_TYPE="screening-note"
IF_EXISTS="version"
# --- end skill-customized ---
```

Boilerplate (HMAC + curl) from `_shared/sanctum-bridge.md`. The bridge auto-creates the deal folder and `From Triptyq/` subfolder via `create_folder_if_missing: true`. Note: `From Co/` will need to be created separately when company-supplied materials arrive — either run a second bridge upload to that path with the first incoming file, or call `sharepoint.folder` once that action ships in the bridge.

**WATCH** — Note the company in the next partners meeting agenda. Don't open a folder. Revisit in 2-4 weeks via `partners-meeting-prep`.

**PASS** — Record the reason in Affinity. No SharePoint folder. The screening doc is not filed; it lives in the conversation as a record.

## Partners Meeting Integration

The screening output is designed to be read aloud in 60 seconds at the weekly meeting. Charles or whoever is presenting can scan it and hit the key points without reading a full memo. The `partners-meeting-prep` skill pulls all this week's screening verdicts into agenda item 2 automatically.

## Deal Number Claiming

Sequential `[###]` numbers are shared firm-wide and conflict-prone. Don't auto-claim. Pattern:

1. From Pass B, find the highest existing number in `02_Deal Flow/`.
2. Propose the next one to the user: _"This screen is for Calder AI. Highest existing deal-flow folder is 110. I'll claim 111 — confirm before I create the folder."_
3. Only after explicit confirmation, run the bridge upload.

This avoids two partners screening different deals and both grabbing the same number.
