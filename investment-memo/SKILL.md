---
name: Triptyq — Investment Memo
description: |
  Write Triptyq Capital investment memos with conviction-driven storytelling, Sid Lee-inspired design, and red brand identity. Use this skill whenever someone asks to write an investment memo, deal memo, IC memo, due diligence summary, or any investment recommendation document. Also triggers on "write up the deal", "memo for the partners", "document this opportunity", "prepare for IC", or when someone has gathered deal materials and needs to turn them into a decision document. This is the canonical way Triptyq writes investment memos — always use it, even for quick deal summaries or one-pagers.
---

# Triptyq Capital — Investment Memo Skill

## Philosophy

Information is like maple syrup: much better when distilled and reduced. Every word must earn its place. This is caveman-style storytelling — primal, direct, conviction-forward. If a sentence doesn't advance the conviction, mitigate a risk, or prove the relationship edge, it gets cut.

We write like Marc Andreessen thinks: start with why this is inevitable, prove the team can execute, show the math works, be honest about risks but frame the mitigants, then make the call. No hedging. No filler. No "it remains to be seen." Have a point of view.

The formatting matters as much as the words — the team values beautiful, readable documents. Think Sid Lee: editorial, clean, bold typography, justified text. The memo should feel like a brand piece, not a spreadsheet.

## Before Writing

### Step 1: Gather Everything

Before writing a single word, exhaust every internal source. The best memos are built on information asymmetry — the relationship story, the data room details, the partner meeting history are what make a Triptyq memo different.

Run **all five passes** from `_shared/research-passes.md` (Outlook, SharePoint, Drive, Granola, External). For an investment memo specifically:

| Pass | Skill-specific seeds |
|------|---------------------|
| **Outlook (A)** | Search company name + founder names + lawyer names. Time horizon: 24 months. Keywords for A3: `term sheet`, `data room`, `cap table`, `409A`, `board update`, `lead investor`, founder name, lawyer name. Pull every legal forward, every internal partner commentary thread. |
| **SharePoint (B)** | Look in `03_Occasions Invest/02_Deal Flow/[###]_[Company]/` for existing drafts, From Co/ legal docs, From Triptyq/ partner notes, market research. |
| **Drive (C)** | Confirm partner; pull data room exports, board decks, founder-shared docs. Down-load PDFs through `pdf` skill for inline summarization. |
| **Granola (D)** | All meetings mentioning the company. Particularly Dealflow & Portcos Weekly transcripts where the deal was discussed — partner pushback and unresolved questions live there. |
| **External (E)** | PitchBook, Crunchbase, SEC EDGAR (if applicable), founder LinkedIn, news. Run `vc-due-diligence` first if external diligence depth isn't already covered. |

Also useful for memo work specifically and not currently bridged:
- **iMessage**: If there's a personal relationship with a founder, check text history for informal context, technical discussions, in-person meetings.
- **Affinity CRM**: Meeting summaries and notetaker transcripts (still Composio-mediated).
- **Apple Mail attachments via AppleScript**: Fall-through when the Outlook MCP can't extract a specific attachment.

The research phase isn't optional. The relationship story, the data room details, the partner meeting history — these are what make a Triptyq memo different from a generic VC writeup.

### Step 2: Identify the Narrative Arc

Every great memo answers five questions in order:

1. **Why is this inevitable?** (The macro thesis — why this market, why now)
2. **Who is building it?** (The team — exits, relationships, unfair advantages)
3. **How big can it get?** (The math — TAM to decacorn path)
4. **What could go wrong?** (Risks — honest, with mitigants)
5. **Why us?** (Triptyq's edge — relationship, access, thesis fit)

The thesis connection to entertainment, spatial computing, and AI must be explicit. If the deal doesn't connect to Triptyq's thesis, say so.

## Document Structure

The memo should be 6-8 pages. Cover page + 7 core sections. For complex deals (e.g., crowded markets, unusual competitive dynamics, or when third-party research independently validates the thesis), up to 3 optional sections may be added between Risks and Recommendation. If you're adding sections, apply the maple syrup test first — every section must earn its place.

### Cover Page
- Triptyq logo (centered, from `assets/triptyq-logo-color.png` in this skill's directory)
- "INVESTMENT MEMO" (split: INVESTMENT in black, MEMO in red)
- Company name and tagline
- Key facts grid: Round, New Money, Pre-Money, Total Round, Lead, Recommendation
- "STRICTLY CONFIDENTIAL" footer with date

### Section 1: The Conviction (1 page)
- Open with a pull quote that captures the thesis in one line
- Why this market is inevitable — not "interesting," inevitable
- The bottleneck or insight the company addresses
- Why this maps to Triptyq's thesis (entertainment x spatial x AI)
- End with the thesis statement in bold red italics

### Section 2: The Company (0.5-1 page)
- One paragraph: what they are, where incorporated, founding date, team pedigree summary
- The pipeline or product in numbered steps (keep to 4-5 max)
- Tech stack validation (one line — production-grade or not)

### Section 3: The Team (1-1.5 pages)
- Pull quote about the jockeys
- Founder entries: Name in red bold, then credentials in one dense sentence each. Lead with exits, not titles.
- Data room evidence: cite specific documents (IP assignments, CIIAAs, advisor agreements) that prove commitment
- "Our Edge" subsection: The relationship story. How we got into this deal. Personal connections, in-person meetings, trust signals. This is what makes Triptyq's memo different.

### Section 4: The Market (1 page)
- Pull quote from an industry leader
- Macro signal paragraph (recent raises, industry events, inflection points)
- Market sizing table with sources cited below in small italic grey
- Source names in the citation line must be **hyperlinked to the specific article** that contains the data — not the homepage. Verify the URL loads before inserting it. Never fabricate an article path.
- "Decacorn Path" with 3 numbered reasons showing the math

### Section 5: Terms & Cap Table (1 page)
- Terms table (compact — combine rows where possible)
- Ownership table (post-money, simplified)
- One paragraph on key observations. Flag concerns but keep it tight.

### Section 6: Risks & Mitigants (0.5-1 page)
- Three-column table: Risk | Concern | Mitigant
- Red header row. 5 risks max. Each cell is 1-2 sentences.
- No paragraph after the table unless there's something the table can't capture.

### Section 7: Recommendation (0.5-1 page)
- Verdict box with red border: "VERDICT: STRONG PROCEED" (or appropriate call)
- One sentence recommendation below
- Short paragraph with the conviction summary — use periods, not commas. Punchy.
- "Why Us" subsection — 2-3 sentences on access and relationship
- Closing pull quote
- Red rule + "END OF MEMO"

### Optional Section A: Competition (insert between Risks and Recommendation)
Use when the market is crowded or when a perceived competitor needs to be explicitly addressed.
- Open with a pull quote that reframes the competitive narrative
- 1-2 punchy setup paragraphs
- 3-column competitor table: Competitor | What They Do | Why It's Not Us
  - Red header row, alternating F5F5F5/WHITE rows
  - Max 5 competitors. Column widths: ~2200, ~3680, ~3480 DXA
  - Be honest about real threats. Distinguish perceived from actual.
- Close with 1 paragraph on what the real moat is
- Apply maple syrup test: if the Risks table already covers it, skip this section

### Optional Section B: SWOT (insert after Competition or after Risks)
Use when the investment decision is complex and IC needs a fast-scan framework.
- Beautiful 2×2 table, full content width (9360 DXA), two equal columns (4680 each)
- Header rows: STRENGTHS (RED `C8102E`), WEAKNESSES (dark `2D2D2D`), OPPORTUNITIES (near-black `1A1A1A`), THREATS (grey `666666`) — all white text
- Body rows: alternating WHITE/F5F5F5 per quadrant
- 4-5 Georgia bullet lines per quadrant (em-dash `—` prefix, 17pt, line 280)
- No prose around the table. The table speaks.

### Optional Section C: External Validation (insert after Recommendation)
Use when a tier-1 research house independently reached the same conclusion as the memo.
- Only include if the research was published BEFORE or independently of your memo — never post-hoc rationalization
- Open with a pull quote stating the timeline clearly (e.g., "PitchBook published 4 months before we wrote this.")
- Map the research findings directly to the company: what did they call, and how does it match?
- A validation table works well: Research Finding | How Company Delivers It | Verdict (checkmark)
- Close by stating why independent convergence matters for the investment decision
- Include the source as a clickable hyperlink

## Design Specification

Read the docx skill before generating. Use `docx-js` (npm `docx`) to build the .docx programmatically.

### Brand Tokens

| Token | Value | Usage |
|-------|-------|-------|
| RED | `C8102E` | Headings, pull quotes, accent text, table headers, page rules |
| BLACK | `1A1A1A` | Title text |
| DARK | `2D2D2D` | Body text |
| MEDIUM | `666666` | Secondary text |
| LIGHT | `999999` | Captions, sources, footer text |
| VERY_LIGHT | `F5F5F5` | Table cell backgrounds |

### Typography

- **Body**: Georgia, 21 half-pts, DARK, justified
- **H1**: Arial, 26 half-pts, bold, RED, all caps, letter-spacing 80, red underline rule (8pt)
- **H2**: Arial, 22 half-pts, bold, BLACK
- **Pull quotes**: Georgia, 24 half-pts, italic, RED, left border 16pt RED, indented 600 DXA
- **Tables**: Arial headers (16-18), Georgia body (16-18), RED header fill, WHITE text
- **Sources**: Georgia, 16 half-pts, italic, LIGHT
- **Cover title**: Arial, 56 half-pts, bold — INVESTMENT in BLACK, MEMO in RED

### Layout

- US Letter (12240 x 15840 DXA), 1-inch margins
- Body always `AlignmentType.JUSTIFIED`
- Line spacing: 300 (body), 340 (pull quotes)
- Header: "TRIPTYQ CAPITAL" red bold + company + CONFIDENTIAL, red bottom rule
- Footer: centered red page numbers with em-dash flanks
- Cover: 16pt RED rules framing content, logo centered
- Tables: DXA widths only (never percentages), `ShadingType.CLEAR`, cell margins 80/140

### Critical docx-js Rules
- Never use `\n` — separate Paragraphs
- Never use unicode bullets — use LevelFormat
- PageBreak inside Paragraph
- ImageRun requires `type: "png"`
- Set page size explicitly (defaults to A4)
- Validate after generation, convert to PDF for preview

## Writing Style

### Do
- Write like you're telling a friend why you're excited about a deal
- Use periods. Short sentences. Punchy.
- Let tables speak — don't repeat what a table already shows
- Cite data room documents as evidence
- Use "we" for Triptyq's perspective
- Include market sources below tables in small italic text

### Don't
- Hedge ("it remains to be seen", "time will tell")
- Repeat information across sections
- Use three sentences where one will do
- Write bio paragraphs that read like LinkedIn profiles
- Add optional sections without first applying the maple syrup test — they must earn their place
- Use "widely regarded as" — let credentials speak
- Fabricate source article URLs — verify every link loads before inserting it

### The Maple Syrup Test
After drafting, read every paragraph and ask: "If I cut this, does the memo lose something essential?" If no, cut it. If yes, can you say it in fewer words?

## Recommendation Verdicts

- **STRONG PROCEED** — Generational opportunity, in thesis, relationship edge, move now
- **PROCEED** — Good deal, manageable risks, worth the allocation
- **CONDITIONAL PROCEED** — Proceed if specific conditions are met
- **WATCH** — Interesting but missing key element, revisit later
- **PASS** — Not in thesis, or risks outweigh opportunity

## After Writing

### New Memo
1. Validate the .docx using `python scripts/office/validate.py`
2. Convert to PDF: `soffice --headless --convert-to pdf doc.docx --outdir ./` (LibreOffice on Claude's local machine)
3. Screenshot key pages and verify formatting
4. Deliver both .docx and .pdf
5. Upload to SharePoint via the Sanctum bridge — see "Upload to SharePoint" below.

### Editing an Existing Memo in SharePoint
This workflow is for surgical OOXML edits to a memo already in SharePoint — adding sections, fixing data, inserting hyperlinks. Use the `triptyq-sharepoint-docx-editor` skill for the download/unpack/edit/repack flow. The final upload back to SharePoint goes through the Sanctum bridge with `if_exists: "version"` so SharePoint preserves version history.

## Upload to SharePoint

Uses the Sanctum bridge — see `_shared/sanctum-bridge.md` for the full env contract, error codes, and MCP variant.

```bash
# --- skill-customized ---
COMPANY="Calder AI"                      # common name, not legal entity
DEAL_NUMBER="110"                        # from SharePoint search; ask user if new
FILE_PATH="${OUTPUT_FILE}"               # the .docx generated by docx-js

DEST_FOLDER="03_Occasions Invest/02_Deal Flow/${DEAL_NUMBER}_${COMPANY}/From Triptyq"
DOC_TYPE="investment-memo"
IF_EXISTS="version"
# --- end skill-customized ---
```

The boilerplate (HMAC sign + curl) lives in `_shared/sanctum-bridge.md` — copy it under the skill-customized block above. After upload, surface the `web_url` to the user.

## Reference Files

- `references/memo-template.md` — Quick-reference template with section patterns and example pull quotes
- `assets/triptyq-logo-color.png` — Official Triptyq Capital logo (color, PNG, 8192x2057)
