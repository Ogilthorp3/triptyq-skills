---
name: partners-meeting-prep
description: |
  Prepare the weekly Triptyq Capital partners meeting (Dealflow & Portcos Weekly). Use this skill to generate the agenda, pipeline update, portfolio status, and compte-rendu template. Triggers on "prep the partners meeting", "weekly meeting agenda", "dealflow update", "portco weekly", "Sunday meeting prep", "prepare for our weekly", "meeting prep for Charles/Guillaume/Bert", or any reference to the recurring Dealflow & Portcos Weekly meeting. Also use for generating the compte-rendu (meeting minutes) after the meeting.
---

# Triptyq Capital — Partners Meeting Prep

## Meeting Context

The Dealflow & Portcos Weekly is the core operating rhythm of Triptyq Capital. Held every Sunday/Monday with Charles, Guillaume, Bert, and Elisabeth. The meeting covers new deal flow, portfolio updates, CRM hygiene, and action items.

## Before the Meeting

### Data Sources to Pull

Run the short, time-windowed version of `_shared/research-passes.md`. The horizon for this skill is **last 7 days** — this is a weekly tempo skill, not a deep dive.

| Pass | Meeting-prep seeds |
|------|--------------------|
| **Outlook (A)** | 7-day horizon. Pull anything new across the pipeline: founder emails, intros, term sheets, investor updates. No company filter — this is the firehose for the week. |
| **SharePoint (B)** | `03_Occasions Invest/03_Partners Meeting (weekly)/[Year]/[Month FR]/` for the previous week's compte-rendu and tracker. Action items from last week feed agenda item 6. |
| **Drive (C)** | Skip unless a specific portco has new board materials worth surfacing. |
| **Granola (D)** | Pull last week's partners meeting transcript for follow-up tracking and to confirm what was decided. |

Plus partners-meeting-specific sources not in the standard helper:
- **Affinity CRM**: Deals updated in the last 7 days, new companies added, status changes.
- **Calendar**: Upcoming meetings with founders, LPs, conferences this week.

### Generate Agenda

```
DEALFLOW & PORTCOS WEEKLY
[Date] | [Time]
Participants: Charles, Guillaume, Bert, Elisabeth

1. OPEN MIC (5 min)
   - Quick wins, blockers, announcements

2. NEW DEAL FLOW ([count] new this week)
   [For each new company, run the deal-screening skill output:]
   - [Company] | [Source] | [Verdict: MEET/WATCH/PASS]

3. PIPELINE STATUS UPDATES
   [For each deal with activity this week:]
   - [Company] | [Status change] | [Next step] | [Owner]

4. PORTFOLIO UPDATES
   [For each portco with news:]
   - [Company] | [Update] | [Action needed?]

5. CRM & PROCESS
   - Affinity hygiene: [count] companies missing data
   - Follow-ups overdue: [list]

6. ACTION ITEMS FROM LAST WEEK
   [Pull from previous compte-rendu]
   - [Item] | [Owner] | [Status: DONE/IN PROGRESS/OVERDUE]

7. NEXT WEEK PREVIEW
   - Key meetings scheduled
   - Deadlines approaching
```

## After the Meeting (Compte-Rendu)

Generate meeting minutes in French (the team operates bilingually but internal notes are typically in French).

### File Naming Convention
- `Compte-rendu_reunion_[date].docx` or `Compte-rendu_partners_meeting.docx`
- Pipeline tracker: `Triptyq_Partners_Meeting_[Date].xlsx`

## Upload to SharePoint

Uses the Sanctum bridge — see `_shared/sanctum-bridge.md`.

```bash
# --- skill-customized ---
MEETING_DATE="2026-04-27"                # ISO format
YEAR="${MEETING_DATE:0:4}"
# Map month number to French short name
case "${MEETING_DATE:5:2}" in
  01) MONTH_FR="Jan";;   02) MONTH_FR="Fév";;
  03) MONTH_FR="Mars";;  04) MONTH_FR="Avril";;
  05) MONTH_FR="Mai";;   06) MONTH_FR="Juin";;
  07) MONTH_FR="Juillet";; 08) MONTH_FR="Août";;
  09) MONTH_FR="Sept";;  10) MONTH_FR="Oct";;
  11) MONTH_FR="Nov";;   12) MONTH_FR="Déc";;
esac

FILE_PATH="${OUTPUT_FILE}"
DEST_FOLDER="03_Occasions Invest/03_Partners Meeting (weekly)/${YEAR}/${MONTH_FR}/${MEETING_DATE}"
DOC_TYPE="partners-meeting"
IF_EXISTS="version"
# --- end skill-customized ---
```

Boilerplate (HMAC + curl) from `_shared/sanctum-bridge.md`. The bridge will auto-create the year/month/date subfolders if they don't exist (`create_folder_if_missing: true` is the default in the helper). Surface `web_url` after upload.

For the pipeline xlsx, run the same upload with the same `DEST_FOLDER` and `DOC_TYPE="partners-meeting"`.

## Integration with Other Skills

- New deals → run `deal-screening` for each
- Deal progressing to diligence → trigger `vc-due-diligence`
- Deal ready for IC → trigger `triptyq-investment-memo`
- All outputs upload via the Sanctum bridge with the right `doc_type`
