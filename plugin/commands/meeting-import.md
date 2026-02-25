---
name: meeting-import
description: |
  Import Google Meet auto-generated notes from Google Drive into the Obsidian vault.
  Two-phase pipeline: import (pull new notes) and process (review, add CRM/tasks/links).
---

Import new Google Meet notes from Google Drive into your vault.

## Setup (always)

1. Read the obsidian skill: `$VAULT/.local-plugins/fractal-mind/1.0.0/skills/obsidian/SKILL.md`
2. Read the vault constitution: `$VAULT/Meta/CLAUDE.md`
3. Read the Google Meet integration spec: `skills/obsidian/references/google-meet-integration.md`
4. Check if Google Workspace MCP tools are available

**Note:** Replace `$VAULT` with your actual vault path (e.g., `/Users/yourname/Obsidian/Vault` or `/home/yourname/obsidian-vault`).

## Workflow

1. **No argument**: Run Phase 1 (Import) — pull new meeting notes from Google Drive
2. **"process" or "review"**: Run Phase 2 (Process) — review and process imported notes
3. **"status"**: Show import state — how many imported, how many unprocessed
