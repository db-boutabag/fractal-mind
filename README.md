# fractal-mind — A Second Brain Architecture for Obsidian + Claude Code

An open-source architecture for building a structured second brain in Obsidian, powered by Claude Code. Capture, organize, query, and maintain your thinking with AI-assisted workflows.

## What This Is

**fractal-mind** is not a pre-built app. It's a carefully designed architecture plus a Claude Code plugin that makes AI dramatically more useful with your Obsidian vault.

- **Architecture:** PARA-based folder structure, frontmatter-first notes, wikilink graph, domain-specific skills
- **Claude Code plugin:** AI workflows for capture, inbox processing, periodic notes, queries, vault maintenance, and meeting imports
- **Shared vault:** Optional git-synced team folder for collaboration via simple git sync
- **Integration-ready:** Connect to ClickUp, Slack, Google Workspace, HubSpot, and other tools via MCP

The core insight: LLMs are only as good as the context you give them. Most people interact with Claude or ChatGPT with zero persistent context — every session starts from scratch. **fractal-mind** gives Claude structured access to your thinking, projects, relationships, and decisions. The result is an AI assistant that actually knows what you're working on, who you know, what you've decided, and what's next.

## Why This Matters

Knowledge workers drown in context switching. You're juggling:
- Tasks scattered across email, Slack, and various tools
- Decisions made but not recorded
- Relationships to nurture, tracked nowhere
- Ideas that vanish because you didn't capture them fast enough
- Meetings where the important stuff was said but never written down
- Questions that could be answered if you could search your own brain

Obsidian solves the capture and search problem. **fractal-mind** adds the AI layer: Claude Code can read your vault, understand your structure, synthesize context, and help you work *with* your brain, not against it.

### What Changes When You Have This

1. **Capture becomes frictionless.** Tell Claude an idea, a decision, a meeting insight, and it goes into your vault in the right place with the right connections — no decision fatigue.

2. **Your vault becomes queryable.** "What did I decide about the product roadmap?" "Who do I know in supply chain?" "What's blocking me right now?" — Claude searches and synthesizes.

3. **Relationships stay warm.** Structured CRM data means Claude can remind you who needs followup, surface connections you didn't realize, suggest introductions.

4. **Time back in your day.** No more searching for scattered notes. No more "I know I captured this somewhere." No more reinventing decisions.

5. **Better decisions faster.** When decisions are recorded with context, Claude can surface precedent, contradict you with data, and help you avoid repeating mistakes.

## Architecture Overview

### Folder Structure

The vault uses **PARA** (Projects, Areas, Resources, Archive) with domain-based subfolders under Projects:

```
YourVault/
├── Inbox/              # Zero-friction captures (process regularly)
├── Projects/           # Active work — organized by domain
│   ├── Brand/
│   ├── Strategy/
│   ├── Product/
│   ├── Marketing/
│   ├── Meetings/
│   └── Ops/
├── Areas/              # Ongoing responsibilities (don't expire)
│   ├── Work/
│   ├── Growth/
│   └── Health/
├── Resources/          # Reference material
├── Archive/            # Completed or shelved items
├── Daily/              # Daily notes (YYYY-MM-DD.md)
├── Templates/          # Note templates
├── Meta/               # CLAUDE.md (constitution), TAGS.md (reference)
├── Shared/             # Git-synced team folder (optional)
│   ├── CRM/
│   ├── Brand/
│   ├── Strategy/
│   ├── Product/
│   ├── Marketing/
│   ├── Engineering/
│   ├── Intel/
│   ├── Meeting-Notes/
│   ├── Docs/
│   └── Archive/
└── .local-plugins/     # Claude Code plugin
    └── fractal-mind/1.0.0/
```

### Frontmatter-First Design

Every note carries machine-readable metadata in YAML frontmatter:

```yaml
---
type: note|task|project|idea|meeting|journal|resource
status: inbox|active|stuck|waiting|done|archived
tags: []
created: YYYY-MM-DD
---
```

This makes your vault queryable. Claude can find "all active projects due this week" or "all stuck items waiting on someone else" in seconds.

### Wikilink Graph

Notes link to each other via `[[wikilinks]]`. These connections build a knowledge graph that Claude can traverse. When you capture something new, Claude adds links to related existing notes automatically.

### Skills-Based Plugin Architecture

The fractal-mind plugin operates via slash commands (`/obsidian`, `/crm`, `/meeting-import`) that invoke different skills:

1. **Obsidian skill** — Core vault management
   - **Capture:** Take raw thoughts/ideas and turn them into structured notes
   - **Inbox Processing:** Batch-process unorganized captures into the right folders
   - **Periodic Notes:** Daily notes, weekly reviews, reflections
   - **Query:** Natural language search and synthesis
   - **Maintenance:** Vault health, orphan detection, broken links, stale items
   - **Meeting Import:** Pull Google Meet notes automatically (two-phase review pipeline)

2. **CRM skill** — Relationship intelligence
   - One file per person, one per company
   - Track: who you know, how you met, last contact, next steps
   - Queries: who needs followup, contacts by company, by source
   - Linked to your main vault notes

3. **External integrations** — Via MCP
   - Obsidian REST API (vault search, read/write)
   - ClickUp (task management, bidirectional sync)
   - Slack (thread capture and search)
   - Google Workspace (meeting notes auto-import)
   - HubSpot (CRM bridge for larger contact databases)

## Quick Start

### Step 1: Clone the Repo

```bash
git clone https://github.com/YOUR_ORG/fractal-mind.git
cd fractal-mind
```

### Step 2: Create Your Vault

Create a new Obsidian vault or use an existing one. Copy the vault template into it:

```bash
cp -r vault-template/* /path/to/your/vault/
```

This sets up your folder structure, templates, and Meta files.

### Step 3: Install the Plugin

Copy the plugin into your vault:

```bash
cp -r plugin/ /path/to/your/vault/.local-plugins/fractal-mind/1.0.0/
```

### Step 4: (Optional) Set Up Obsidian MCP

If you want Claude to have indexed search and live read/write access to your vault, install the Obsidian REST API community plugin and configure MCP:

```bash
# In your vault, install the REST API plugin (search for "REST API" in community plugins)
# Then copy the example config and fill in your API key:
cp plugin/.mcp.json.example /path/to/your/vault/.mcp.json
```

Edit `.mcp.json` and set `OBSIDIAN_API_KEY` to your plugin's API key (found in the plugin's settings).

See `plugin/CONNECTORS.md` for full setup instructions for all integrations.

### Step 5: (Optional) Set Up Shared Vault

If you're working with a team, set up the git-synced shared folder. See `vault-template/Shared/TEAM-SETUP.md` for detailed instructions.

### Step 6: Launch the Plugin

Open Claude Code in your vault directory:

```bash
cd /path/to/your/vault
claude code
```

Then type:

```
/obsidian
```

Claude will read your vault structure, understand your configuration, and ask what you need. Try:

- **Capture:** "I had an idea for a new feature in the product: smarter defaults in the settings panel"
- **Inbox Processing:** "Process my inbox"
- **Query:** "What am I waiting on from other people?"
- **Daily Note:** "Create my daily note"
- **Maintenance:** "Scan for orphaned notes"

## How the Plugin Works

### The Workflow System

When you invoke `/obsidian`, the plugin:

1. **Reads your vault constitution** (`Meta/CLAUDE.md`) — understands your name, preferred structure, and rules
2. **Reads your tag reference** (`Meta/TAGS.md`) — knows your tag taxonomy
3. **Analyzes your request** — determines which workflow you need (Capture, Inbox, Periodic Notes, Query, Maintenance, or Meeting Import)
4. **Executes the workflow** — reads conventions, creates/edits notes, adds wikilinks, reports results

Everything is driven by the `CLAUDE.md` file in your Meta folder. Customize it and the plugin adapts to your setup.

### Capture Workflow

You tell Claude an idea, decision, or brain dump. It:

1. **Assesses** the input (single idea, multiple items, task, project, or scattered thoughts)
2. **Determines destination** (which folder? Inbox/ if unsure)
3. **Creates frontmatter** (type, status, tags, created date, wikilinks)
4. **Adds context** (body content, next-step, connections to existing notes)
5. **Reports** what was created and where

Example: You say "I need to redesign the pricing page and I'm not sure whether to A/B test it first."

Claude creates:
- File: `Projects/Product/redesign-pricing-page.md`
- Frontmatter with type=project, status=active, tags=[#project/pricing, #type/decision]
- Body with the decision question
- Link to related notes about pricing strategy
- Next-step: "Decide: A/B test or full rollout?"

### Inbox Processing Workflow

You say "Process my inbox" and Claude:

1. **Lists** all files in `Inbox/`
2. **For each file:** reads it, determines the right category, adds proper frontmatter, moves to correct folder
3. **Adds wikilinks** to related existing notes
4. **Reports** what was moved and why

### Periodic Notes Workflow

**Daily notes:** Claude creates `Daily/YYYY-MM-DD.md` with:
- Template structure (Focus Today, Captures, Done Today, Reflections)
- Links to all active projects (via Dataview query)
- Yesterday's unfinished items that rolled over
- Priorities for today

**Weekly reviews:** Claude creates `Daily/YYYY-Www-review.md` with:
- Summary of the week's work
- Patterns noticed
- Stuck items
- Next week priorities

### Query Workflow

You ask questions about your vault. Claude:

1. **Parses intent** ("What am I stuck on?", "Who do I need to reconnect with?", "Show me all decisions made this month")
2. **Searches your vault** (filesystem or via Obsidian MCP if available)
3. **Synthesizes answers** with citations and wikilinks
4. **Connects dots** across projects, people, and decisions

### Maintenance Workflow

You say "Scan for broken links" or "Find stale active notes" and Claude:

1. **Audits** your vault for common problems
2. **Reports** orphaned notes, broken wikilinks, notes with missing frontmatter, active items that haven't been touched in months
3. **Proposes fixes** and waits for your approval

### Meeting Import Workflow

Claude can pull Google Meet auto-generated notes from Google Drive and import them into your Shared vault. Two-phase process:

**Phase 1 (Import):** Fetch new meeting notes from Drive, save with `status: to-review`

**Phase 2 (Process):** Analyze notes, propose CRM entries, action items, wikilinks; wait for your confirmation before executing

Full details in `plugin/CONNECTORS.md` and `plugin/skills/obsidian/references/google-meet-integration.md`.

## The CRM Skill

Type `/crm` to access relationship intelligence:

- **Add Contact:** Create a person or company entry
- **Log Interaction:** Record when you last connected
- **Lookup:** Search for a contact and see context
- **Query:** "Who haven't I talked to in 3 months?", "Contacts from Meridian Labs"
- **Maintain:** Find stale contacts, missing fields, duplicates

The CRM is not a replacement for HubSpot or Salesforce. It's relationship intelligence: people and companies you want to maintain meaningful relationships with. It stays in your Shared vault and connects to your main vault notes via wikilinks.

## Shared Vault Architecture

The optional `Shared/` folder is a git-synced subdirectory within your vault. It enables team collaboration:

- **CRM/** — Shared relationship intelligence
- **Brand/**, **Strategy/**, **Product/**, etc. — Domain folders for shared team knowledge
- **Meeting-Notes/** — Captured meeting notes (with auto-import from Google Meet)
- **Docs/** — Ad-hoc shared documents
- **Archive/** — Completed shared items

Every file includes `added-by` in frontmatter to track contributions. Git history tracks edits.

Why a subfolder instead of a separate vault? Wikilinks work seamlessly across personal and shared content. You can link a personal project to a shared brand document without friction.

Full setup instructions in `vault-template/Shared/TEAM-SETUP.md`.

## Customization

### Add Your Own Domain Folders

Edit `Meta/CLAUDE.md` and add domains under `Projects/`:

```yaml
## Structure
- Projects/ uses domain subfolders: Brand/, Strategy/, Product/, Marketing/, Meetings/, Ops/, **NewDomain/**
```

Then create the folder:

```bash
mkdir /path/to/your/vault/Projects/NewDomain
```

Claude will recognize it automatically next time you use the plugin.

### Modify Your Vault Constitution

Edit `Meta/CLAUDE.md` to change:
- Your name (so Claude personalizes interactions)
- Structure rules (add/remove domains, change archive policy)
- Preferred date format or naming conventions
- Integration preferences (which external tools are enabled)

### Extend the Skills

The plugin is in `plugin/skills/obsidian/` and `plugin/skills/crm/`. You can:
- Read the skill files to understand the architecture
- Add new workflows (e.g., a journaling workflow, or a weekly planning workflow)
- Customize the frontmatter schema to fit your needs
- Add new commands (e.g., `/weekly-plan`, `/retrospective`)

## External Tool Connections

The plugin can integrate with external tools via MCP. See `plugin/CONNECTORS.md` for full setup instructions:

- **Obsidian REST API** — Indexed search and live read/write
- **ClickUp** — Task management with bidirectional sync
- **Slack** — Thread capture and search
- **Google Workspace** — Google Meet note auto-import
- **HubSpot** — CRM bridge for scaling beyond personal relationships

All integrations are optional. The plugin works standalone with filesystem-only access.

## Requirements

- **Obsidian** (free) — Note-taking and vault management
- **Claude Code** — Requires Anthropic API key (free trial available)
- **Git** (optional) — For shared vault sync
- **Obsidian REST API plugin** (optional, free) — For MCP-enhanced features
- **Dataview plugin** (optional, free) — For live queries in notes
- **Google Workspace OAuth** (optional) — For meeting note auto-import

## Philosophy

This architecture is built on a few core principles:

1. **Own your data.** Your vault lives on your machine. No cloud lock-in.

2. **Structure enables intelligence.** Frontmatter, wikilinks, and naming conventions make your vault machine-readable. Claude can help because it can *understand* your vault.

3. **Friction kills capture.** The easier it is to dump thoughts into Inbox/, the more you'll actually capture. Processing happens later.

4. **One idea per note.** Small, focused notes link better and reuse better than monolithic documents.

5. **Bias toward action.** Don't ask permission. Propose and execute. Surface next-steps relentlessly.

6. **Graceful degradation.** The plugin works with filesystem-only access. MCP tools enhance it but aren't required.

7. **Human in the loop.** Claude proposes, you approve (especially for CRM entries, external task creation, and decisions).

## Contributing

This is an open-source template. Contributions welcome:

- Report bugs via issues
- Suggest workflows or skills
- Share your customizations
- Improve documentation

See the repo's CONTRIBUTING guidelines for details.

## License

MIT. See LICENSE for details.

---

## Next Steps

1. **Read the plugin documentation:** `plugin/skills/obsidian/SKILL.md`
2. **Set up your vault:** Run the provided Python bootstrap script or copy the template manually
3. **Customize CLAUDE.md:** Add your name, favorite domains, rules
4. **Start capturing:** `/obsidian` and tell Claude an idea
5. **Optional: Set up integrations** via `plugin/CONNECTORS.md`
6. **Optional: Set up team collaboration** via `vault-template/Shared/TEAM-SETUP.md`

Good luck building your second brain.
