# Google Meet Integration — Automated Note Import Pipeline

Complete specification for importing Google Meet auto-generated notes into your Obsidian vault via the `/meeting-import` skill.

## Overview

Fractal-mind includes a two-phase pipeline for importing and processing Google Meet meeting notes from Google Drive:

1. **Phase 1 (Import/Capture):** Automatically pull new meeting notes from your configured Drive folder, save them to the vault with minimal processing, mark as "to-review"
2. **Phase 2 (Process/Review):** Manually review imported notes, identify CRM entries and action items, update with links and metadata

This design prioritizes:
- **Zero friction capture** — get notes into the vault fast
- **Human review** — don't auto-create CRM entries without confirmation (transcription errors are common)
- **Deduplication** — state tracking ensures no duplicate imports
- **Safety** — all proposals wait for confirmation before execution

## Architecture

```
Google Drive (Meeting Notes Folder)
    ↓
Google Workspace MCP (list_drive_items, get_doc_as_markdown)
    ↓
Import State Tracking (JSON)
    ↓
Obsidian Vault (Shared/Meeting-Notes/)
    ↓
Phase 1: Import (status: to-review)
    ↓
Phase 2: Process (propose CRM, tasks, links)
    ↓
User Confirmation
    ↓
Vault Update (status: active, added links, created tasks)
```

## Phase 1: Import (Capture)

Automatically pull new meeting notes from Google Drive and save to vault.

### Prerequisites

- Google Workspace MCP configured (see `setup.md`)
- Google Drive folder ID for meeting notes configured
- OAuth flow completed and authenticated

### Process

1. **Verify MCP Availability**
   - Check if Google Workspace MCP tools are available
   - If not available, inform user and suggest checking MCP config
   - Exit gracefully if unavailable

2. **Load Import State**
   - Read `meeting-import-state.json` from vault root
   - Extract list of previously imported document IDs
   - Extract last check timestamp

3. **List Drive Folder**
   - Use Google Workspace MCP: `list_drive_items` in configured folder
   - Get document IDs, names, and creation timestamps
   - Filter for Google Docs only (mime type `application/vnd.google-apps.document`)

4. **Find New Documents**
   - Compare current documents against state file
   - Identify documents not yet imported
   - Sort by creation date (oldest first)

5. **Import Each New Document**
   For each new document:

   a. **Fetch Content**
   - Use Google Workspace MCP: `get_doc_as_markdown`
   - Extract full document content as markdown
   - Preserve formatting, headings, lists, tables

   b. **Parse Metadata**
   - Extract meeting title (from Drive doc name)
   - Extract creation date
   - Generate creation timestamp
   - Capture source Google Docs URL

   c. **Identify Components**
   - Look for transcript section (often at end)
   - Separate structured content from raw transcript
   - Extract attendees if mentioned in header
   - Look for agenda items, action items, notes

   d. **Create Vault Note**
   - Generate filename: `YYYY-MM-DD-meeting-title.md`
   - Write frontmatter with metadata (see schema below)
   - Structure content: Summary, Notes, Attendees, Action Items, Transcript (collapsed)
   - Add source link to original Google Doc
   - Preserve all original content

   e. **Store Transcript**
   - Extract full transcript if present
   - Store in collapsed callout: `> [!transcript]- Full Transcript`
   - Preserves for later review without cluttering note

   f. **Update State File**
   - Add document ID to imported list with timestamp
   - Mark as `"processed": false`
   - Save updated state file

6. **Report Results**
   - List files created with paths
   - Count of new imports
   - State file timestamp updated
   - Suggest running Phase 2 with `/meeting-import process`

### Import Frontmatter Schema

```yaml
---
type: meeting
status: to-review
tags: [type/meeting, area/work, source/google-meet]
created: YYYY-MM-DD
added-by: auto-import
source-doc: https://docs.google.com/document/d/{DOC_ID}
attendees: ["Name 1", "Name 2"]
next-step: "Review and process this meeting note"
---
```

**Fields:**
- `type: meeting` — identifies as meeting note
- `status: to-review` — awaiting human review before processing
- `tags` — includes `source/google-meet` for tracking
- `created` — date note was created in Drive
- `added-by: auto-import` — tracks automatic import
- `source-doc` — link back to original Google Doc for reference
- `attendees` — list of people mentioned in meeting
- `next-step` — reminds user to review

### Example Imported Note

```markdown
---
type: meeting
status: to-review
tags: [type/meeting, area/work, source/google-meet]
created: 2024-02-25
added-by: auto-import
source-doc: https://docs.google.com/document/d/1ABC123XYZ/edit
attendees: ["Alex Rivera", "Jamie Park", "Sam Torres"]
next-step: "Review and process this meeting note"
---

# Project Alpha Review — 2024-02-25

**Original:** [View in Google Drive](https://docs.google.com/document/d/1ABC123XYZ/edit)

## Attendees

- Alex Rivera
- Jamie Park
- Sam Torres

## Meeting Summary

[Structured notes from meeting]

## Agenda Items

1. Status update on phase 1
   - On track, no blockers
2. Discussion of timeline
   - Possible acceleration in Q2
3. Resource planning
   - Need approval for engineering team growth

## Action Items

- Alex: Finalize phase 1 scope by EOW
- Jamie: Schedule design review
- Sam: Prepare resource budget

## Notes

[Full notes section from original Google Doc]

> [!transcript]- Full Transcript
> Auto-generated transcript goes here...
> [Full transcript preserved for reference]
```

## Phase 2: Process (Review)

Manually review imported notes and propose CRM entries, action items, and links.

### Process

1. **Find Unprocessed Imports**
   - Query vault for notes with `status: to-review` AND `source/google-meet` tag
   - Sort by created date (oldest first)
   - List notes waiting for review

2. **For Each Note to Review**

   a. **Analyze Content**
   - Read note title and content
   - Extract attendees from frontmatter and body
   - Identify action items and owners
   - Look for project/topic mentions
   - Check for decisions or commitments made

   b. **Cross-Reference CRM**
   - Look up each mentioned person in vault CRM
   - Note existing relationships
   - Flag new people not in CRM

   c. **Cross-Reference Projects**
   - Search vault for mentions of projects/initiatives discussed
   - Identify related active projects
   - Look for connections to areas of responsibility

   d. **Propose Changes (IMPORTANT: Wait for Confirmation)**

   **Propose CRM Entries:**
   ```
   NEW CONTACT - Jamie Park
   - Role: Product Lead (from meeting)
   - Company: Meridian Labs
   - Relationship: Collaborator
   - Source: google-meet
   - Next Step: Add to contact list

   Create: Shared/CRM/People/jamie-park.md
   ```

   **Never** auto-create CRM entries. Present proposals and wait for user:
   - "Create this contact?" (yes/no/skip)
   - Flag name uncertainties (transcription errors common)
   - Cross-check against existing contacts for duplicates

   **Propose Action Items:**
   ```
   ACTION ITEM
   - "Finalize phase 1 scope"
   - Owner: Alex Rivera
   - Due: EOW (2024-02-28)
   - Related: [[project-alpha]]

   Create ClickUp task? (yes/no/skip)
   ```

   Wait for confirmation before creating external tasks.

   **Propose Wikilinks:**
   ```
   SUGGEST LINKS
   - [[project-alpha]] (mentioned: "phase 1 scope")
   - [[meridian-labs]] (attendee from this company)
   - [[design-review]] (action item: "schedule design review")
   ```

   Review and confirm before adding.

   e. **Execute Confirmed Changes**
   - Create new CRM entries only with confirmation
   - Create ClickUp tasks only with confirmation
   - Add wikilinks as proposed
   - Update note frontmatter:
     - `status: active` (from `to-review`)
     - Keep `source/google-meet` tag
     - Add `next-step` with action items
   - Update state file: `"processed": true`
   - Add linked person/company references to body

3. **Report Summary**
   - Count of proposals made
   - Count of confirmations received
   - Count of CRM entries created
   - Count of tasks created
   - Count of notes updated

### Safety Rails (Critical)

**Never Auto-Create Without Confirmation:**
- Transcription errors are common in auto-generated notes
- User must review and confirm all CRM entries
- Proposing is safe; executing requires confirmation

**Fuzzy-Match Names:**
- Before proposing new CRM entry, search existing contacts
- Check for similar names (might be duplicate)
- Flag suspicious spellings
- Ask user: "Is this the same as [existing contact]?"

**Cross-Reference Against CRM:**
```
Meeting mentions: "John Smith from Apex Studio"
Existing CRM: "jon-smith.md" at Apex Studio
Proposal: "Is this the same person? Link instead of creating new?"
```

**Validate Email/Contact Info:**
- Extract email addresses if mentioned
- Cross-check against existing contacts
- Flag discrepancies for user review

**Avoid Hallucination:**
- Only create what's explicitly mentioned in the note
- Don't infer relationships not stated
- Ask user: "Should I create a task for [implied action]?"

## State File Management

State tracking prevents duplicate imports and tracks processing progress.

### Schema

```json
{
  "imported": {
    "1ABC123XYZ": {
      "imported_at": "2024-02-25T14:32:10Z",
      "vault_path": "Shared/Meeting-Notes/2024-02-25-project-alpha-review.md",
      "processed": false,
      "title": "Project Alpha Review"
    },
    "2DEF456UVW": {
      "imported_at": "2024-02-25T15:45:22Z",
      "vault_path": "Shared/Meeting-Notes/2024-02-25-budget-planning.md",
      "processed": true,
      "title": "Budget Planning"
    }
  },
  "last_check": "2024-02-25T16:00:00Z"
}
```

**Fields:**
- `imported` — map of document IDs to import records
- `imported_at` — ISO timestamp when imported
- `vault_path` — where note was saved
- `processed` — whether Phase 2 review is complete
- `title` — meeting title for reference
- `last_check` — timestamp of last import run

### File Location

Store at vault root: `meeting-import-state.json`

Add to `.gitignore` if tracking import state locally (optional).

## Graceful Degradation

**Google Workspace MCP Unavailable:**
- Check MCP config in `.mcp.json`
- Verify OAuth credentials are set
- If not available, inform user:
  ```
  Google Workspace MCP not available.
  To use meeting import:
  1. Ensure workspace-mcp is installed
  2. Check GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET environment variables
  3. Complete OAuth flow when prompted
  ```
- Offer to help with setup (link to `setup.md`)
- Exit gracefully

**No New Documents:**
- Check state file
- If all documents already imported, report:
  ```
  No new meeting notes found.
  Last import: 2024-02-25 at 16:00
  Current meeting notes in Drive: 15 total, 15 already imported
  ```
- Offer to re-process existing unreviewed notes

**Partial Failure:**
- Import documents that succeeded
- Report documents that failed with reasons
- Update state file with successful imports
- Ask user to check failed documents and retry

**OAuth Expired:**
- If Google API returns auth error
- Prompt user to re-authorize
- Provide clear instructions for OAuth flow
- Link to setup guide

## Configuration

### Drive Folder ID

The meeting notes folder must be configured in the skill.

Edit `skills/obsidian/SKILL.md` or provide as parameter:

```
/meeting-import --drive-folder=<YOUR_DRIVE_FOLDER_ID>
```

**Find Your Folder ID:**
1. Open Google Drive folder
2. Look at URL: `https://drive.google.com/drive/folders/{FOLDER_ID}`
3. Copy the folder ID

**Do NOT commit real folder IDs to repository.** Use placeholder: `<YOUR_DRIVE_FOLDER_ID>`

### Filtering

Import only documents matching patterns:
- By name: only import docs with "meeting" in title
- By date: only import docs from last 7 days
- By owner: only import docs owned by yourself

Configure in skill parameters.

## Dataview Queries

Useful Dataview queries for meeting notes in your vault:

**All unprocessed Google Meet imports:**
```dataview
list
from #source/google-meet
where status = "to-review"
sort created desc
```

**All processed Google Meet imports:**
```dataview
list
from #source/google-meet
where status = "active"
sort created desc
```

**Meetings from specific person:**
```dataview
list
from #type/meeting
where contains(attendees, "Jamie Park")
sort created desc
```

**Action items from meetings:**
```dataview
task
from #type/meeting
where !completed
sort created desc
```

Embed these in a dashboard note for quick access.

## Troubleshooting

**"Google Workspace MCP not available"**
- Verify MCP installed: `uvx workspace-mcp --help`
- Check `.mcp.json` config
- Confirm environment variables set
- Complete OAuth flow if needed

**"Drive folder not found"**
- Verify folder ID is correct
- Check you have access to the folder
- Verify OAuth permissions include Drive read access

**"Transcript extraction failing"**
- Some meeting formats don't include transcripts
- Review raw note in Google Drive
- Manually extract transcript if needed
- File issue with details

**"Duplicate detection not working"**
- Check `meeting-import-state.json` is in vault root
- Verify state file is valid JSON
- Try deleting state file to reset (will re-import all)

**"Proposed CRM entries have wrong names"**
- Check original Google Doc for accuracy
- Google Meet transcription sometimes mangles names
- Always review fuzzy-matched names before confirming
- Update contact info manually if needed

## Examples

### Example: Successful Import

```
Running Phase 1: Import
Found 3 new meeting notes in Drive folder

Importing: Project Alpha Review
  → Saved to: Shared/Meeting-Notes/2024-02-25-project-alpha-review.md
  → Status: to-review
  → Attendees: 3 people
  → Has transcript

Importing: Budget Planning Meeting
  → Saved to: Shared/Meeting-Notes/2024-02-25-budget-planning.md
  → Status: to-review
  → Attendees: 2 people
  → Has transcript

Importing: Weekly Standup
  → Saved to: Shared/Meeting-Notes/2024-02-25-weekly-standup.md
  → Status: to-review
  → Attendees: 5 people
  → Has transcript

Summary: 3 notes imported, 0 already in vault
Run "/meeting-import process" to review and process these notes.
```

### Example: Successful Process

```
Running Phase 2: Process

Reviewing: Project Alpha Review
Found 3 people to add to CRM:
  - Jamie Park (Product Lead, Meridian Labs) — NEW
  - Alex Rivera (Engineer, Meridian Labs) — EXISTS: alex-rivera.md
  - Sam Torres (Designer, Meridian Labs) — NEW

Fuzzy-match check: No existing contacts with similar names

Propose CRM entries:
  ✓ Create jamie-park.md
  ✓ Create sam-torres.md
  ✓ Link to alex-rivera.md (already exists)

Found action items:
  ✓ "Finalize phase 1 scope" — assigned to Alex Rivera, due EOW

Propose ClickUp task? (yes/no/skip)

Found project mentions:
  ✓ "project-alpha" — link existing [[project-alpha]]

Proposed wikilinks:
  ✓ [[project-alpha]]
  ✓ [[meridian-labs]]

Waiting for confirmation...

[User confirms all]

Creating CRM entries...
  ✓ jamie-park.md created
  ✓ sam-torres.md created
  ✓ Created ClickUp task ENG-234
  ✓ Added wikilinks to meeting note
  ✓ Updated status: active

Summary: 2 CRM entries created, 1 task created, 3 links added
Note status updated to "active"
```

## Integration with Shared Vault

For team collaboration, import notes to `Shared/Meeting-Notes/`:

- All imported notes have `added-by: auto-import`
- Team members can review and edit imported notes
- Git history tracks who updated what
- Link to shared CRM entries in `Shared/CRM/People/`

## Next Steps

1. Set up Google Workspace MCP (see `setup.md`)
2. Configure drive folder ID
3. Run `/meeting-import` to import phase
4. Run `/meeting-import process` to review and update
5. Notes become active with CRM and task links
6. Review process weekly to stay current

## Reference

- **Setup Guide:** `setup.md` — MCP configuration
- **Obsidian Skill:** `SKILL.md` — Core vault management
- **Conventions:** `conventions.md` — Note structure and naming
- **MCP Connectors:** `CONNECTORS.md` — External tool setup
