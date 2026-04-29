# Triptyq research passes — shared helper

Canonical research pattern used by every Triptyq skill that needs to gather information about a company (portco, deal, or prospect). Skills reference this helper instead of duplicating the pass logic.

> **Skill authors:** in your skill's "Research" section, list the skill-specific search seeds (queries, keywords, time windows, what data points to extract) and reference this helper for the mechanics. Don't duplicate the tool-call boilerplate.

## Why this exists

Three reasons. First, internal sources have ground-truth data — the public web has guesses. Second, every Triptyq skill needs roughly the same passes (Outlook, SharePoint, Drive) but with different keywords and time horizons. Third, dedup logic across sources is non-trivial and shouldn't be re-implemented per skill.

## Pass A — Outlook (Microsoft 365)

Three sub-passes, in this order. Each builds on what the previous one returned.

**A1 — Broad sweep by company name.** Catches anything mentioning the company, including third-party intros and forwarded threads.
```
outlook_email_search(query="<Company Name>", limit=25)
```
For substantive hits, fetch full content with `read_resource(<uri>)`.

**A2 — Sender-domain pull.** Once A1 surfaces an email from the company, extract the sender's domain (e.g. `@calder.ai`) and pull everything from that domain over the relevant horizon. This is where investor updates, board decks, term sheets, and round materials live.
```
outlook_email_search(sender="@<company-domain>", afterDateTime="<horizon>", limit=50)
```
Default horizons: tearsheet/screening = 12 months; portfolio monitoring = 6 months; partners meeting prep = 7 days; due diligence = 24 months.

**A3 — Keyword pulls scoped to company.** Catches updates forwarded by co-investors, intros from non-company addresses, etc. Common keywords: `"investor update"`, `"monthly update"`, `"board update"`, `"term sheet"`, `"data room"`. Vary per skill.
```
outlook_email_search(query="<keyword> <Company Name>", limit=10)
```

**What to extract per Outlook hit:** sender, subject, date, attachment names (download with `read_resource` if relevant), and the data points the calling skill cares about (revenue figure, headcount, raise status, partnership announcement, founder ask, risk flag).

## Pass B — SharePoint

Pull existing Triptyq work first so you don't duplicate or contradict it.
```
sharepoint_search(query="<Company Name>", limit=10)
sharepoint_folder_search(name="<Company Name>")
```

If a `[###]_<Company>` deal folder exists, **the deal number is canonical** — the calling skill must use it for its upload destination, not a fresh number. From `From Triptyq/` pull any prior memos, tearsheets, or DD docs and treat them as the previous verdict / thesis. Don't restate differently without a reason.

## Pass C — Google Drive (board materials, founder shares)

**Step C1 — identify the responsible partner.** Each Triptyq partner has their own Google account where their portcos share materials. Read `_shared/partners.yaml` for the partner → `google_account` map. If a `partner_portfolio.yaml` mapping exists in `triptyq-skills/`, look the company up there. Otherwise ask the user: _"This portco — Bert's, Charles's, or Guillaume's?"_

**Step C2 — confirm Drive auth.** Drive MCP has no `whoami` tool, so confirmation is by explicit user prompt:
> _"Drive needs to be authenticated as `<google_account>` to access this portco's materials. Confirm before I fetch."_

If the user can't confirm or auth is wrong, halt with: _"Re-authenticate Drive as `<google_account>` (Settings → Connectors → Google Drive → reconnect), or hand this off to the responsible partner to run."_

**Step C3 — fetch.**
```
search_files(query="<Company Name>")           # decks, founder docs, term sheets
list_recent_files()                            # latest dropped board materials
get_file_metadata(<file_id>)                   # confirm partner share / freshness
```
Per file:
- Google Docs / Sheets / Slides → `read_file_content(<file_id>)` returns text inline.
- PDFs / external decks → `download_file_content(<file_id>)` writes the binary; pipe through the `pdf` skill (text extract) or `pptx` skill (slide content) to summarize.

**Guillaume's account is currently TBD** in `partners.yaml`. When the user identifies a portco as his, ask for the address at runtime and offer to update `partners.yaml`.

## Pass D — Granola (meeting transcripts)

If the conversation involves a company we've met with, Granola transcripts are richer than any email summary.
```
query_granola_meetings(<Company Name>)
list_meetings(...)        # if you need to scope by date / attendee
get_meeting_transcript(<meeting_id>)
```
Common signal in transcripts that doesn't show up elsewhere: founder's own framing of risks, real revenue numbers said out loud, partner pushback, off-the-record competitive intel.

## Pass E — External (web, Crunchbase, PitchBook, EDGAR)

Skill-specific. Fill gaps the internal sources didn't cover. Cross-check public claims against what you found in Outlook / Drive — when they disagree, internal data wins. The `vc-due-diligence` skill drives this pass hardest; lighter skills (`tearsheet`, `deal-screening`) hit it last and briefly.

Common external sources, with the tool to use:
- General web search via `WebSearch` or Composio's `COMPOSIO_SEARCH_WEB`
- PitchBook via Triptyq's Premium connector if connected, else `WebFetch` of `pitchbook.com` URLs (paywalled hits return thin content — note the gap)
- SEC EDGAR via `COMPOSIO_SEARCH_SEC_FILINGS` (resolve CIK first via web search for private companies)
- Crunchbase recipe `rcp_7y7yozhEk_-Q` if still wired

## Dedup

Materials often arrive across multiple passes — a board deck shows up as an Outlook attachment AND a Drive file AND a SharePoint copy. Before extracting, dedupe by:

1. **Filename + last-modified date**, OR
2. **(sender, subject, date) tuple** for emails specifically.

Carry through one canonical reference per artifact in the synthesis.

## What "ground truth" means

When sources disagree, prefer in this order: SEC filing > company-sent email > Drive board deck > Granola transcript > SharePoint past memo > public web. Always note the source for each claim in the output, so the partner reviewing it can audit fast.
