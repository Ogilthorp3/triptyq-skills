---
name: docx-xml-editor
description: |
  Edit existing .docx files stored in SharePoint/OneDrive by directly manipulating OOXML in the Rube remote sandbox. Use this skill when the file already exists in SharePoint and needs surgical edits — adding sections, fixing text, inserting hyperlinks, updating data — without recreating the document from scratch.

  Triggers: "edit the memo in SharePoint", "add a section to the existing doc", "update the Word file on SharePoint", "fix the text in the docx", "add hyperlinks to the sources", "insert a competition section into the memo", "update the date in the memo".

  DO NOT use this skill to create a new .docx from scratch (use Anthropic's docx skill + docx-js instead), or when the file is local on Claude's machine (use Anthropic's docx skill + unpack.py instead).
---

See full implementation and documentation at:
https://github.com/Ogilthorp3/docx-xml-editor

The SKILL.md with complete workflow is in that repo at `/SKILL.md`.

## Quick decision guide

| Scenario | Use |
|----------|-----|
| Creating a new .docx from scratch | Anthropic docx skill (docx-js) |
| File is on Claude's local machine | Anthropic docx skill (unpack.py) |
| **File is in SharePoint/OneDrive** | **This skill** |
| **Editing existing memo or report** | **This skill** |
| **Adding hyperlinks to existing doc** | **This skill** |

## Triptyq SharePoint Infrastructure

- **Drive ID**: `b!wPs8sWIq70Kt7RsL80wFKBqB2HWWzZdAnhoakfwfYIWRgc_-ZgmSTLpthkkQlSJu`
- **Memo folder**: `/03_Occasions Invest/02_Deal Flow/[###]_[Company]/From Triptyq/`
- **Upload tool**: `ONE_DRIVE_ONEDRIVE_UPLOAD_FILE` via Rube with `conflict_behavior: "replace"`
- **Download tool**: `ONE_DRIVE_DOWNLOAD_FILE` via Rube — returns `content.s3url`
