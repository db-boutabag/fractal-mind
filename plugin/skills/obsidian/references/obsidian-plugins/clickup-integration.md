# ClickUp Integration Guide

Complete guide to linking Obsidian vault notes with ClickUp tasks for bidirectional task management.

## Overview

The ClickUp integration creates a bridge between your Obsidian vault and ClickUp task management:

- **Link notes to tasks:** Add ClickUp task URLs in note frontmatter
- **Bidirectional sync:** Keep vault notes and ClickUp tasks in sync
- **Auto-create tasks:** Propose ClickUp tasks when processing vault notes
- **Status mapping:** Sync status between vault and ClickUp
- **Deduplication:** Prevent creating duplicate tasks

This lets you maintain context in Obsidian while keeping external stakeholders in sync via ClickUp.

## Linking: Frontmatter Convention

Add a `clickup` field to any vault note to link it to a ClickUp task:

```yaml
---
type: task
status: active
tags: [area/work]
created: 2024-02-25
clickup: https://app.clickup.com/t/ABC123456
---
```

The `clickup` field should contain the full ClickUp task URL.

### Finding ClickUp Task URL

1. Open ClickUp task
2. Click task title to open in full view
3. Look at the URL bar: `https://app.clickup.com/t/{TASK_ID}`
4. Copy the full URL
5. Add to note frontmatter

### Automatic Linking

When creating a task from the `/obsidian` skill:

1. User confirms creating a ClickUp task
2. Claude Code creates task via ClickUp MCP
3. ClickUp returns task URL
4. Claude adds URL to vault note's `clickup` field
5. Link is permanent

## Status Mapping

Keep vault notes and ClickUp tasks synchronized using a consistent status mapping:

| Obsidian Status | ClickUp Status | Meaning |
|-----------------|----------------|---------|
| inbox | Backlog | Unprocessed |
| active | To Do, In Progress | Currently working |
| stuck | Stuck | Blocked, needs help |
| waiting | Waiting | Depends on external action |
| done | Done | Completed |
| archived | Cancelled | No longer relevant |

### Mapping Rules

**Direction: Vault → ClickUp**
- When updating note status in vault, propose updating ClickUp task
- Wait for confirmation before changing external task

**Direction: ClickUp → Vault**
- Periodically sync ClickUp status back to vault notes
- Check for completed ClickUp tasks (status = "done")
- Update vault notes: `status: done`
- Note in comment: "Synced from ClickUp: [task name]"

**Manual Override**
- If vault and ClickUp diverge, vault is source of truth
- Reason: Vault is closest to user's actual work
- Update ClickUp to match vault status when conflicts occur

## Bidirectional Sync Protocol

Keep vault notes and ClickUp tasks in sync with this protocol:

### Sync Direction: Vault → ClickUp

When user updates a vault note:

1. **Check for `clickup` field**
   ```yaml
   clickup: https://app.clickup.com/t/ABC123456
   ```
   If present, note is linked.

2. **Detect Changes**
   - Status changed
   - Next-step updated
   - Description modified
   - New tags added
   - Due date changed

3. **Propose Sync**
   ```
   SYNC DETECTED:
   Vault: status = "active" | next-step = "Review feedback"
   ClickUp: status = "to do" | comment = "Review feedback"

   Sync to ClickUp? (yes/no/skip)
   ```

4. **Execute if Confirmed**
   - Update ClickUp task via MCP
   - Update description from `next-step`
   - Update status mapping
   - Add comment: "Updated from vault: [timestamp]"
   - Preserve external comments

### Sync Direction: ClickUp → Vault

Periodically sync ClickUp changes back to vault:

1. **Query ClickUp for Updated Tasks**
   - Find tasks linked from vault notes
   - Check last sync timestamp
   - Identify recently changed tasks

2. **For Each Changed Task**
   - Find corresponding vault note (via `clickup` field)
   - Compare status in ClickUp vs vault
   - Check if completed (status = "done")

3. **Propose Updates**
   ```
   SYNC FROM CLICKUP:
   Task: ENG-234 "Finalize specs"
   ClickUp Status: Done (completed 2024-02-25)
   Vault Status: active

   Update vault to status = "done"? (yes/no/skip)
   ```

4. **Execute if Confirmed**
   - Update vault note: `status: done`
   - Add timestamp: `completed: 2024-02-25`
   - Add comment in note: "Completed in ClickUp"
   - Mark completed

### Sync Frequency

- **Manual:** User can run `/obsidian sync-clickup` anytime
- **Periodic:** Daily check for completed tasks
- **On-demand:** When creating tasks or updating status

## Deduplication Protocol

Before creating a ClickUp task, check for existing tasks to prevent duplicates.

### Process

1. **Extract Task Intent**
   - Parse action item from note
   - Create search query: "Finalize project spec"

2. **Search ClickUp**
   ```
   Query: "Finalize project spec"
   Results:
   - ENG-234: "Finalize project specifications" (active, Jamie Park)
   - ENG-189: "Project spec v1" (done, Alex Rivera)
   ```

3. **Evaluate Matches**
   - Exact match → Link to existing task
   - Close match → Ask user: "Is this the same as ENG-234?"
   - No match → Create new task

4. **Link or Create**

   **Link Option:**
   ```
   Found existing task: ENG-234 "Finalize project specifications"
   Link to this task? (yes/no/create-new)
   ```
   If yes: add `clickup: https://...ENG-234` to note

   **Create Option:**
   ```
   Creating new ClickUp task:
   Title: "Finalize project spec"
   Description: "From vault note: [link to note]"
   Assignee: [suggest from note context]
   Due: [extract from note if present]
   List: [suggest based on area/project tag]
   ```

### Dedup Queries

Effective search patterns:

```
"Finalize spec"           # Title keyword search
"project-alpha"           # Project name
"Jamie Park"              # Assignee name
"#tag/name"               # Tag-based search
```

ClickUp MCP should support fuzzy matching — activate to catch near-duplicates.

## Creating Tasks from Vault Notes

When processing vault content, propose ClickUp tasks:

### Action Item Detection

Identify actionable items in vault notes:

```
Note: "Need to schedule design review with Jamie"
Action Item: "Schedule design review"
Owner: Jamie (implied)

Propose ClickUp task?
```

### Task Creation Proposal

Present proposal for confirmation:

```
CREATE CLICKUP TASK

Title: "Schedule design review"
Description: "From meeting note: Project Alpha Review"
Due Date: (unset)
Assignee: Jamie Park
List: Projects/Product (from note location)
Priority: (unset)
Tags: [project/alpha, type/meeting]

Create this task? (yes/no/edit)
```

Allow editing before creating.

### Link to Vault Note

After creating task, add link to vault note:

1. Get task URL from ClickUp MCP response
2. Add to note frontmatter: `clickup: https://...`
3. Add comment in task: "Related note: [vault note link]"
4. Report success: "Created ENG-234, linked from vault"

## Handling Status Changes

When vault status changes, update ClickUp task accordingly:

### Status Update Flow

1. **User updates vault note**
   ```yaml
   ---
   status: done  # Changed from "active"
   ---
   ```

2. **Detect change**
   - Old value: active
   - New value: done
   - Note has `clickup` field

3. **Propose sync**
   ```
   Status changed: active → done

   Update ClickUp task ENG-234 to "Done"? (yes/no)
   ```

4. **Execute if confirmed**
   - Call ClickUp MCP to update status
   - Map vault status to ClickUp: "done" → "Done"
   - Add comment in task: "Marked done in vault"

### Handling Conflicts

If vault and ClickUp status diverge:

1. **Detect conflict**
   ```
   Vault: status = "done"
   ClickUp: status = "In Progress"
   ```

2. **Resolve**
   ```
   CONFLICT DETECTED:
   Vault marks this task as done, but ClickUp shows in progress.

   Options:
   a) Trust vault (update ClickUp to done)
   b) Trust ClickUp (update vault to active)
   c) Skip sync
   ```

   Recommend: "Trust vault (it's closest to actual work)"

## Special Considerations

### Obsidian-Only Fields

Some vault fields don't map to ClickUp:

- `energy` — personal energy cost (not in ClickUp)
- `area` — life area (custom field in ClickUp if enabled)
- `waiting-on` — who it depends on (maps to ClickUp comment)

When syncing, preserve these in vault note only.

### ClickUp-Only Fields

ClickUp has fields not in vault:

- Custom fields (ClickUp workspace specific)
- Priority level
- Time tracking/estimates
- Assignee team
- Recurring schedules

When viewing ClickUp task, display these in note context without storing in frontmatter.

### Private vs. Shared Tasks

- **Personal vault notes** → Create private ClickUp tasks
- **Shared vault notes** → Create shared/team ClickUp tasks
- Tag with `added-by` in vault for contribution tracking

### Orphaned Links

If ClickUp task is deleted externally:

1. Vault note still has `clickup` field pointing to deleted task
2. Next sync attempt fails
3. Offer to remove link: "ClickUp task no longer exists. Remove link? (yes/no)"
4. Clean up vault note

## Example Workflow

### Scenario: Weekly Review

1. **User runs `/obsidian weekly review`**
2. Review includes action items:
   ```
   Action Items
   - Design review with Jamie (from meeting)
   - Implement API endpoints (technical work)
   - Prepare proposal (strategic)
   ```

3. **Claude detects action items**
   ```
   Propose creating ClickUp tasks for 3 action items?

   Task 1: "Design review with Jamie"
   → Search ClickUp: Found existing ENG-234
   → Link instead of creating? (yes/no)
   ```

4. **User confirms**
   - Link to ENG-234 (already exists)
   - Create "Implement API endpoints"
   - Create "Prepare proposal"

5. **Tasks created in ClickUp**
   ```
   Created: ENG-235 "Implement API endpoints"
   Created: BIZ-167 "Prepare proposal"
   All tasks include comment linking back to vault note
   ```

6. **Vault notes updated**
   ```yaml
   ---
   type: meeting
   status: active
   clickup: https://app.clickup.com/t/ENG234 (for design review)
   related:
     - [[project-alpha]]
     - [[engineering-backlog]]
   ---
   ```

7. **Ongoing sync**
   - When ENG-234 completed in ClickUp, vault note updated
   - When user marks vault task done, ClickUp updated
   - Status stays in sync

## Configuration

### ClickUp MCP Setup

See `setup.md` for complete MCP configuration.

Requires:
- ClickUp MCP installed via `uvx`
- `CLICKUP_API_KEY` environment variable
- Read/write access to ClickUp workspace

### Workspace Configuration

Configure which ClickUp workspace/lists to target:

In `.mcp.json`:
```json
{
  "mcpServers": {
    "clickup": {
      "command": "uvx",
      "args": ["mcp-clickup"],
      "env": {
        "CLICKUP_API_KEY": "$CLICKUP_API_KEY",
        "CLICKUP_WORKSPACE_ID": "$CLICKUP_WORKSPACE_ID"
      }
    }
  }
}
```

### List Mapping

Map vault domains to ClickUp lists:

```yaml
# In vault CLAUDE.md or custom config:
clickup_mapping:
  "Projects/Brand": "Brand/Backlog"
  "Projects/Product": "Product/Backlog"
  "Projects/Engineering": "Engineering/Backlog"
  "Inbox": "Backlog/Uncategorized"
```

Default: Create in "Backlog" if no mapping exists.

## Troubleshooting

**"ClickUp MCP not available"**
- Verify MCP installed: `uvx mcp-clickup --help`
- Check `CLICKUP_API_KEY` environment variable
- Verify API key is valid in ClickUp settings
- Check workspace ID

**"Task not found in ClickUp"**
- Task may be archived or deleted
- Search ClickUp manually to verify
- Remove `clickup` field from vault note if task is gone
- Create new task if needed

**"Deduplication not working"**
- Check search is returning results
- Try exact task title in ClickUp to verify it exists
- Fuzzy matching may need tuning
- Manual review before creating: always ask user

**"Status not syncing"**
- Verify status mapping is correct (see table above)
- Check ClickUp task actually has that status
- Try manual sync: `/obsidian sync-clickup`
- Check MCP logs for errors

**"Link is broken"**
- ClickUp URLs change with task IDs
- Always use full task URL, not custom URL
- Verify task still exists before assuming link is broken

## Best Practices

1. **Always confirm before creating external tasks**
   - Propose, don't execute
   - Let user review task details
   - Allow editing before creating

2. **Use dedup protocol consistently**
   - Search before creating
   - Ask about close matches
   - Link to existing when possible

3. **Keep status in sync**
   - Update ClickUp when vault changes
   - Check for ClickUp completions regularly
   - Resolve conflicts in favor of vault

4. **Include context in links**
   - Add comments in ClickUp linking to vault
   - Add frontmatter in vault linking to ClickUp
   - Both sides should know about the relationship

5. **Archive together**
   - When task is done in ClickUp, mark done in vault
   - When archiving in vault, archive in ClickUp
   - Keep both sides clean

## Integration with Obsidian Workflows

**In Capture workflow:**
- User shares an action item
- Check if it exists in ClickUp (dedup)
- Propose creating task with confirmation

**In Inbox Processing workflow:**
- Find actionable items in Inbox/
- Ask about creating ClickUp tasks
- Link vault notes to tasks

**In Periodic Notes workflow:**
- Extract action items from weekly review
- Propose tasks for next week
- Sync status for completed items

**In Query workflow:**
- Search both vault and ClickUp
- Show items stuck in one system but not the other
- Highlight sync conflicts

## More Resources

- **Setup Guide:** `setup.md` — MCP configuration
- **Obsidian Skill:** `SKILL.md` — core vault workflows
- **Conventions:** `conventions.md` — frontmatter schema
- **ClickUp API:** [ClickUp API Documentation](https://clickup.com/api)
- **MCP Guide:** `CONNECTORS.md` — external tool setup
