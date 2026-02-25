---
name: crm
description: |
  Relationship intelligence via Obsidian vault. Use this skill whenever the user wants to:
  add or update contacts, log interactions, look up people or companies, query relationships,
  or maintain the CRM index.
---

Launch the CRM relationship intelligence skill. Read the core files, then handle the user's request.

## Setup (always — read these in parallel)

1. Read the skill: `$VAULT/.local-plugins/fractal-mind/1.0.0/skills/crm/SKILL.md`
2. Read the vault constitution: `$VAULT/Meta/CLAUDE.md`
3. Read the CRM conventions: `skills/crm/references/conventions.md`

**Note:** Replace `$VAULT` with your actual vault path (e.g., `/Users/yourname/Obsidian/Vault` or `/home/yourname/obsidian-vault`).

## Workflow

Determine the workflow from user input:
- **"I met..." or "Add contact"** → Add Contact workflow
- **"Log interaction" or "Follow up with"** → Log Interaction workflow
- **"Who is..." or "Tell me about"** → Lookup workflow
- **"Show me..." or "Find contacts"** → Query workflow
- **"Clean up", "audit", "find duplicates"** → Maintenance workflow
