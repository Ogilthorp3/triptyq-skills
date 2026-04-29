# Sanctum Bridge — skill helper

This file is consumed by every Triptyq skill that needs to push artifacts to SharePoint (or any other Sanctum-bridged destination). It is the single source of truth for how skills talk to the bridge. Do not hardcode endpoint URLs or auth headers in individual skills — reference this helper instead.

> **Skill authors:** copy the relevant snippet below into your skill's "Upload to SharePoint" section, parameterizing only `DEST_FOLDER`, `DOC_TYPE`, and `IF_EXISTS`. Everything else stays as-is.

## Environment contract

The Claude sandbox must have the following env vars available before any bridge call. They are populated by Cowork from the user's secret store; skills don't ask the user for them.

| Variable                    | Purpose                                              |
|-----------------------------|------------------------------------------------------|
| `CF_ACCESS_ID`              | Cloudflare Access service token id                   |
| `CF_ACCESS_SECRET`          | Cloudflare Access service token secret               |
| `SHAREPOINT_HMAC_SECRET`    | HMAC signing key, scoped to the SharePoint module    |
| `SANCTUM_BRIDGE_BASE`       | Defaults to `https://bridge.nepveu.name`             |

If any of the first three is missing, the bridge call will 401. Skills should check and fail loudly with a pointer back to this helper, rather than silently producing a half-uploaded file.

## Destination allowlist

The SharePoint module rejects writes outside the canonical roots defined in `triptyq-skills/sharepoint-structure.yaml`. The Triptyq tenant uses Charles's existing structure — skills must use these exact paths (case and accents matter):

- `01_Gestion Triptyq/...`                              — fund ops, legal, HR, branding
- `02b_Fund II (2025)/...`                              — Fund II fundraising materials
- `03_Occasions Invest/01_Portco/...`                   — active portfolio companies
- `03_Occasions Invest/02_Deal Flow/...`                — pipeline / pre-investment deals
- `03_Occasions Invest/03_Partners Meeting/...`         — weekly partners meeting artifacts
- `03_Occasions Invest/Other/...`                       — PitchBook, market & fund research

Anything else returns `403 destination_not_allowed`. If a skill needs a new root, add it to `sharepoint-structure.yaml` and bump its `version`. Don't try to bypass it.

## Destination patterns by doc_type

Skills resolve their concrete `folder_path` from these templates before calling the bridge. The bridge does NOT resolve templates — it just enforces that the resolved path falls under an allowed root.

| doc_type            | folder_path template                                                          |
|---------------------|-------------------------------------------------------------------------------|
| `investment-memo`   | `03_Occasions Invest/02_Deal Flow/{numbered_company}/From Triptyq`            |
| `tearsheet`         | `03_Occasions Invest/02_Deal Flow/{numbered_company}/From Triptyq`            |
| `dd-summary`        | `03_Occasions Invest/02_Deal Flow/{numbered_company}/From Triptyq`            |
| `screening-note`    | `03_Occasions Invest/02_Deal Flow/{numbered_company}/From Triptyq`            |
| `company-doc`       | `03_Occasions Invest/02_Deal Flow/{numbered_company}/From Co`                 |
| `partners-meeting`  | `03_Occasions Invest/03_Partners Meeting/{year}/{month_fr}/{date_iso}`        |
| `portco-status`     | `03_Occasions Invest/01_Portco/{numbered_company}`                            |
| `lp-update`         | `02b_Fund II (2025)/02_FINANCIAL/02_DECK` _(confirm with Charles)_            |
| `market-research`   | `03_Occasions Invest/Other/Pitchbook/Market`                                  |
| `fund-research`     | `03_Occasions Invest/Other/Pitchbook/Funds`                                   |
| `legal-doc`         | `01_Gestion Triptyq/...` _(skill picks subfolder per the filing skill)_       |

**Token resolvers** (skill responsibility):

- `{numbered_company}` — `[###]_[Company Name]`. Skill must search Deal Flow / Portco for an existing folder by company name; if none, claim the next available sequential number. Common name only — never legal entity.
- `{year}` — 4-digit year (e.g. `2026`)
- `{month_fr}` — French month: `Jan`, `Fév`, `Mars`, `Avril`, `Mai`, `Juin`, `Juillet`, `Août`, `Sept`, `Oct`, `Nov`, `Déc`
- `{date_iso}` — `YYYY-MM-DD`

## Upload action — bash invocation

This is the canonical snippet. Skills paste it under an "## Upload to SharePoint" heading and customize only the marked variables.

```bash
# --- skill-customized ---
# Skill resolves concrete path from the template in "Destination patterns
# by doc_type" before calling. Example for a tearsheet on Calder AI (deal #110):
DEST_FOLDER="03_Occasions Invest/02_Deal Flow/110_Calder AI/From Triptyq"
DOC_TYPE="tearsheet"                   # see doc_type vocabulary below
IF_EXISTS="version"                    # version | overwrite | rename | fail
FILE_PATH="${OUTPUT_FILE}"
# --- end skill-customized ---

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
  --arg ifx "$IF_EXISTS" \
  '{folder_path:$folder, filename:$name, content_b64:$b64,
    metadata:{doc_type:$dt}, create_folder_if_missing:true,
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
echo "Uploaded → $WEB_URL"
```

## MCP-tool invocation (claude.ai custom connector)

When Claude is running in claude.ai chat (not the sandbox), call the MCP tool directly instead of curl:

```
sharepoint.upload(
  folder_path="03_Occasions Invest/02_Deal Flow/110_Calder AI/From Triptyq",
  filename="investment-memo-v3.docx",
  content_b64=...,
  metadata={"doc_type": "investment-memo"},
  if_exists="version"
)
```

Returns the same `{drive_item_id, web_url, version, etag}` shape.

## doc_type vocabulary

Pin a `doc_type` on every upload so SharePoint search and views can filter cleanly. Skills should pick from this list:

| doc_type              | Used by skill(s)                          |
|-----------------------|-------------------------------------------|
| `investment-memo`     | triptyq-investment-memo                   |
| `tearsheet`           | tearsheet-generator                       |
| `dd-summary`          | vc-due-diligence                          |
| `lp-update`           | lp-update-writer                          |
| `partners-meeting`    | partners-meeting-prep                     |
| `portco-status`       | portfolio-monitoring                      |
| `screening-note`      | deal-screening                            |
| `meeting-notes`       | (manual / Granola exports)                |
| `legal-doc`           | legal:* skills                            |

Adding a new value? Add it here and to `triptyq-skills/sharepoint-structure.yaml` in the same PR.

## `if_exists` semantics

| Value       | Behavior                                                  | When to use                          |
|-------------|-----------------------------------------------------------|--------------------------------------|
| `version`   | SharePoint native versioning, returns new version number  | Default — memos, tearsheets          |
| `overwrite` | Replaces the file, no version history                     | Auto-generated dashboards            |
| `rename`    | Appends `-1`, `-2`, ... to filename                       | When versions should be siblings     |
| `fail`      | Returns 409 if the file exists                            | Final/signed docs that should be immutable |

## Error reference

| Code | Meaning                              | Skill response                       |
|------|--------------------------------------|--------------------------------------|
| 401  | CF Access token missing/invalid      | Stop — env not set up. Tell user.    |
| 403  | `destination_not_allowed`            | Stop — destination off allowlist.    |
| 403  | `hmac_failed`                        | Stop — secret rotation likely needed.|
| 409  | `file_exists` (only with `if_exists=fail`) | Up to skill — usually surface to user. |
| 413  | Body too large (>250MB)              | Skill should split or compress.      |
| 429  | Graph rate limit                     | Retry with exponential backoff (helper handles this). |
| 5xx  | Bridge or Graph error                | Retry once, then surface to user.    |

## Manifest sync

This file is regenerated nightly by `triptyq-skills/scripts/sync-bridge-manifest.py` from `bridge.nepveu.name/_manifest`. Do not hand-edit the auto-generated sections (marked `<!-- AUTO -->` ... `<!-- /AUTO -->`). The narrative sections above (intro, allowlist, doc_type vocab, error reference) are hand-maintained.

<!-- AUTO -->
<!-- Populated by sync-bridge-manifest.py: full action list, request/response schemas -->
<!-- /AUTO -->
