---
name: obsidian
description: |
  Digital brain management via Obsidian vault. Use this skill whenever the user wants to:
  capture thoughts, ideas, or notes; process their inbox; create or update daily/weekly notes;
  query their vault; organize or restructure notes; or perform vault maintenance.
---

Launch the Obsidian digital brain skill. Read the core files, then handle the user's request.

## Setup (always — read these in parallel)

1. Read the skill: `$VAULT/.local-plugins/fractal-mind/1.0.0/skills/obsidian/SKILL.md`
2. Read the vault constitution: `$VAULT/Meta/CLAUDE.md`
3. Read the tag reference: `$VAULT/Meta/TAGS.md`
4. If obsidian MCP tools are available, enable API-enhanced features. Otherwise use filesystem-only mode.

**Note:** Replace `$VAULT` with your actual vault path (e.g., `/Users/yourname/Obsidian/Vault` or `/home/yourname/obsidian-vault`).

## Load on demand (only when the workflow needs them)

- **Creating notes** → read `references/conventions.md` for templates and naming rules
- **Dataview queries** → read `references/obsidian-plugins/dataview.md` for DQL syntax

## Workflow

Determine the workflow from user input:
- **User shares thoughts/ideas/brain dump** → Capture workflow
- **"Process inbox" or "organize"** → Inbox Processing workflow
- **"Daily note" or "weekly review"** → Periodic Notes workflow
- **Questions about vault contents** → Query workflow
- **"Fix", "clean", "audit", "scan"** → Maintenance workflow
- **"Import meetings" or "pull meeting notes"** → Meeting Import workflow
