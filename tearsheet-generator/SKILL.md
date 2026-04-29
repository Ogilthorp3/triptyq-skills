---
name: tearsheet-generator
description: |
  Generate branded Triptyq Capital company tearsheets — concise one-page company profiles for pipeline review and LP presentations. Use this skill when someone needs a tearsheet, one-pager, company snapshot, deal card, or quick company profile. Triggers on "tearsheet for [company]", "one-pager on [company]", "company snapshot", "deal card", "quick profile of [company]", "make a tearsheet", or when a company summary is needed for a deck, LP meeting, or pipeline review. Lighter than an investment memo — this is the business card of a deal.
---

# Triptyq Capital — Tearsheet Generator

## What Is a Tearsheet

A single-page branded document that gives anyone the full picture of a company in 60 seconds. Used for pipeline reviews, LP meetings, conference prep, and sharing deals with co-investors.

## Research

Run the relevant passes from `_shared/research-passes.md`. For a tearsheet specifically:

| Pass | Tearsheet seeds |
|------|-----------------|
| **Outlook (A)** | 12-month horizon. A1 broad sweep, then A2 by sender domain once you have it. A3 keywords: `investor update`, `monthly update`, `board update`. Extract per email: latest revenue/ARR, headcount, round status, customer wins, founder asks. |
| **SharePoint (B)** | Search for prior tearsheets, memos, DD docs on this company. If a `[###]_<Company>` deal folder exists, **use that deal number** for the upload destination — never auto-claim a new one. |
| **Drive (C)** | Confirm responsible partner before fetch. Pull recent board decks; dedupe against Outlook attachments by filename + last-modified. |
| **Granola (D)** | Skip unless a tearsheet update is being driven by a specific recent meeting. |
| **External (E)** | Last layer, brief. Company website, Crunchbase/PitchBook, recent news. Internal data wins on conflicts. |

This is meant to be a 5–10 minute exercise, not a deep dive. If you find yourself reading legal docs or analyzing cap tables, you're in `vc-due-diligence` territory — escalate.

## Tearsheet Layout (Single Page)

Build with docx-js. Triptyq brand tokens (RED C8102E, Georgia body, Arial headers, justified). Logo top-left.

```
[TRIPTYQ LOGO]                              [Date]

═══════════════════════════════════════════
[COMPANY NAME]
[Tagline / one-line description]
═══════════════════════════════════════════

SNAPSHOT                         ROUND
─────────                        ─────
Sector: [vertical]               Stage: [seed/A/B]
Founded: [year]                  Raising: [$amount]
HQ: [city, country]              Valuation: [$pre-money]
Employees: [count]               Lead: [investor]
Website: [url]                   Close: [target date]

WHAT THEY DO
[3-4 sentences. Product, market, differentiation. Dense.]

TEAM
[Founder 1] — [credential]
[Founder 2] — [credential]
[Key hire if notable]

TRACTION
[2-3 bullet points: revenue, users, partnerships, milestones]

THESIS FIT
[2 sentences: how this connects to entertainment × spatial × AI]

TRIPTYQ EDGE
[1-2 sentences: relationship, access, or strategic value we bring]

KEY RISK
[1 sentence: the single biggest concern]

─────────────────────────────────────────
VERDICT: [SCREENING / DILIGENCE / IC-READY / INVESTED / PASS]
─────────────────────────────────────────
CONFIDENTIAL — Triptyq Capital
```

## Design Rules

- ONE PAGE MAXIMUM. If it doesn't fit on one page, you're not distilling enough.
- Two-column layout for Snapshot + Round (use table with no borders)
- Company name in large bold black, tagline in red italic
- Red top and bottom rules
- Verdict bar at the bottom with status

## Batch Mode

When generating tearsheets for multiple companies (e.g., for an LP meeting or pipeline review), run them in parallel and compile into a single multi-page document with page breaks between each.

## Resolving the deal number

The destination folder uses the `[###]_[Company]` convention. Before uploading, the skill must know the right number:

1. **If the user gave the deal number** (e.g. "tearsheet for Calder AI, deal 110") — use it.
2. **If the user didn't** — search the existing Deal Flow folder. Once `sharepoint.search` is live on the bridge, this is automated. Until then, ask the user: _"Which deal-flow number does this map to? (e.g. 110_Calder AI). If this is a new deal, I'll claim the next available number."_
3. **For a brand-new deal** without an assigned number, ask the user to claim one before generating the tearsheet — don't guess. The numbered folder is shared across the firm and conflicts have to be resolved manually.

For batch tearsheets that aren't tied to a single deal (LP meeting prep, conference packs), use the LP/deck destination instead — see Filing below.

## Filing

Single-deal tearsheet: `03_Occasions Invest/02_Deal Flow/[###]_[Company]/From Triptyq/`

Batch tearsheet (LP meeting, pipeline review, conference): `02b_Fund II (2025)/02_FINANCIAL/02_DECK/` _(confirm with Charles before bulk uploads here)_

## Upload to SharePoint

Uses the Sanctum bridge — see `_shared/sanctum-bridge.md` for the full env contract, error codes, and MCP variant.

```bash
# --- skill-customized ---
COMPANY="Calder AI"                      # common name, not legal entity
DEAL_NUMBER="110"                        # resolved per "Resolving the deal number" above
FILE_PATH="${OUTPUT_FILE}"               # the .docx generated by docx-js

DEST_FOLDER="03_Occasions Invest/02_Deal Flow/${DEAL_NUMBER}_${COMPANY}/From Triptyq"
DOC_TYPE="tearsheet"
IF_EXISTS="version"
# --- end skill-customized ---

# Boilerplate below is identical across skills — see _shared/sanctum-bridge.md.
set -euo pipefail
: "${CF_ACCESS_ID:?missing — see _shared/sanctum-bridge.md}"
: "${CF_ACCESS_SECRET:?missing — see _shared/sanctum-bridge.md}"
: "${SHAREPOINT_HMAC_SECRET:?missing — see _shared/sanctum-bridge.md}"
BASE="${SANCTUM_BRIDGE_BASE:-https://bridge.nepveu.name}"

BODY=$(jq -nc \
  --arg folder "$DEST_FOLDER" \
  --arg name "$(basename "$FILE_PATH")" \
  --arg b64 "$(base64 -w0 "$FILE_PATH")" \
  --arg dt "$DOC_TYPE" \
  --arg co "$COMPANY" \
  --arg ifx "$IF_EXISTS" \
  '{folder_path:$folder, filename:$name, content_b64:$b64,
    metadata:{doc_type:$dt, company:$co}, create_folder_if_missing:true,
    if_exists:$ifx}')

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
NONCE=$(uuidgen)
BODY_HASH=$(printf '%s' "$BODY" | sha256sum | cut -d' ' -f1)
TO_SIGN=$(printf '%s\n%s\nPOST\n/sharepoint/upload\n%s' "$TS" "$NONCE" "$BODY_HASH")
SIG=$(printf '%s' "$TO_SIGN" \
  | openssl dgst -sha256 -hmac "$SHAREPOINT_HMAC_SECRET" -hex \
  | awk '{print $2}')

RESP=$(curl -sS -w '\n%{http_code}' -X POST "$BASE/sharepoint/upload" \
  -H "CF-Access-Client-Id: $CF_ACCESS_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_SECRET" \
  -H "Authorization: SanctumHMAC v1" \
  -H "X-Sanctum-Module: sharepoint" \
  -H "X-Sanctum-Timestamp: $TS" \
  -H "X-Sanctum-Nonce: $NONCE" \
  -H "X-Sanctum-Signature: $SIG" \
  -H "Content-Type: application/json" \
  --data "$BODY")

CODE=$(printf '%s' "$RESP" | tail -n1)
JSON=$(printf '%s' "$RESP" | sed '$d')

if [[ "$CODE" != "200" ]]; then
  echo "Upload failed ($CODE): $JSON" >&2
  exit 1
fi

WEB_URL=$(printf '%s' "$JSON" | jq -r '.web_url')
echo "Tearsheet uploaded → $WEB_URL"
```

After upload, surface the `web_url` to the user with a one-line confirmation. Don't summarize what's in the tearsheet — they have the link.
