---
name: investment-memo
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

Before writing a single word, exhaust every source available. The best memos are built on information asymmetry. Check all of these:

- **Email** (Outlook): Search for the company name, founder names, lawyer names. Look for legal docs, term sheets, data room invitations, internal forwards with partner commentary.
- **SharePoint**: Search for the company — there's likely a deal folder under `03_Occasions Invest/02_Deal Flow/`. Look for existing drafts, partner meeting notes, market research.
- **Meeting notes** (Granola): Query for the company and founder names. Check the Dealflow & Portcos Weekly meetings for internal discussion.
- **Affinity**: Check for CRM meeting summaries and notetaker transcripts.
- **iMessage**: If there's a personal relationship with a founder, check text history for informal context, technical discussions, in-person meetings.
- **Data room** (Brightflag or equivalent): If there's a data room, catalog every document. The IP assignments, advisor agreements, 409A valuations, share certificates, and corporate filings tell a story the deck never will.
- **Apple Mail attachments**: Use AppleScript to find and save email attachments locally if the Outlook API can't download them directly.

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

The memo should be 6-8 pages. Cover page + 7 sections. No more, no less. If you need more space, you're not distilling enough.

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
- Add sections beyond the 7-section structure
- Use "widely regarded as" — let credentials speak

### The Maple Syrup Test
After drafting, read every paragraph and ask: "If I cut this, does the memo lose something essential?" If no, cut it. If yes, can you say it in fewer words?

## Recommendation Verdicts

- **STRONG PROCEED** — Generational opportunity, in thesis, relationship edge, move now
- **PROCEED** — Good deal, manageable risks, worth the allocation
- **CONDITIONAL PROCEED** — Proceed if specific conditions are met
- **WATCH** — Interesting but missing key element, revisit later
- **PASS** — Not in thesis, or risks outweigh opportunity

## After Writing

1. Validate the .docx
2. Convert to PDF for preview
3. Screenshot key pages and verify formatting
4. Deliver both .docx and .pdf
5. Save to SharePoint deal folder if access is available

## Reference Files

- `references/memo-template.md` — Quick-reference template with section patterns and example pull quotes
- `assets/triptyq-logo-color.png` — Official Triptyq Capital logo (color, PNG, 8192x2057)
