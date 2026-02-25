# Obsidian Vault Management Skill

This skill enables structured interaction with your Obsidian vault as a digital brain powered by Claude Code. It supports capture, organization, querying, and maintenance workflows.

**Vault path:** `VAULT=/path/to/your/vault`

## Vault Structure

The fractal-mind architecture uses PARA (Projects, Areas, Resources, Archive) folders with domain organization:

```
YourVault/
├── Inbox/              # Zero-friction captures — process regularly
├── Projects/           # Active work — organized by domain
│   ├── Brand/
│   ├── Strategy/
│   ├── Product/
│   ├── Marketing/
│   ├── Meetings/
│   └── Ops/
├── Areas/              # Ongoing responsibilities
│   ├── Work/
│   ├── Growth/
│   └── Health/
├── Resources/          # Reference material
├── Archive/            # Completed or shelved items
├── Daily/              # Daily notes (YYYY-MM-DD.md)
├── Templates/          # Note templates
├── Meta/               # CLAUDE.md (vault constitution), TAGS.md (tag reference)
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
    └── fractal-mind/
        └── 1.0.0/
            ├── skills/
            ├── commands/
            └── CONNECTORS.md
```

## Workflows

### 1. Capture

User shares thoughts, ideas, brain dumps, or quick notes.

**Process:**
1. Assess the input: Is it a single idea, multiple ideas, a task, project, or brain dump?
2. For each idea:
   - Determine type (note, task, project, idea, journal, resource)
   - Determine destination folder
   - Choose a clear filename (use user's language as title)
   - Select appropriate tags
   - Identify connections to existing notes
3. Write frontmatter + content using conventions
4. Add wikilinks to related existing notes
5. If clearly actionable, ask about creating external task (ClickUp or similar)
6. Report what was created, where, what it links to

**Rules:**
- Bias toward action, speed over perfection
- Inbox/ is the safe default if unsure
- One idea per note when possible
- Always include next-step for actionable items
- Split brain dumps into individual notes
- Use user's language in titles

### 2. Inbox Processing

Process unorganized notes from Inbox/ and apply structure.

**Process:**
1. List all files in Inbox/
2. For each file:
   - Read the content
   - Determine category, type, and destination
   - Add/update frontmatter (type, status, tags, created)
   - Move to correct folder with appropriate filename
   - Add wikilinks to related notes
3. Report summary of processed items

**Rules:**
- Check for duplicates before moving
- Preserve creation date if present
- Add next-step if actionable

### 3. Periodic Notes

Daily notes, weekly reviews, and reflections.

**Daily Notes:**
- Path: `Daily/YYYY-MM-DD.md`
- Use the daily template
- Scan vault for active projects and notes
- Populate Focus Today section with current priorities
- Include Captures section for quick capture during the day

**Weekly Reviews:**
- Path: `Daily/YYYY-Www-review.md`
- Use the weekly review template
- Summarize the week's accomplishments
- Surface patterns, themes, stuck items
- Generate next week's priorities
- Identify anything needing follow-up or escalation

**Open-ended Reflections:**
- Listen for actionable items, completed work, workload concerns
- Create appropriate notes or update existing ones
- Surface next-steps prominently

### 4. Query

Natural language search and synthesis across vault content.

**Process:**
1. Parse user's intent
2. Search vault for relevant notes
3. Synthesize answer from found content
4. Cite sources with wikilinks
5. Offer follow-up actions (create task, add to weekly review, etc.)

**Common Queries:**
- What's currently active?
- What's stuck or blocked?
- What connects to [topic]?
- What did I do this week?
- Progress on [project]?

**Enhancement:** With MCP server available, use indexed search endpoint for more powerful queries.

### 5. Maintenance

Vault health and cleanup.

**Scanning:**
- Orphan notes: linked from nowhere, no outgoing links
- Broken links: reference notes that don't exist
- Duplicates: similar notes that could be merged
- Stale active notes: marked active but untouched for >2 weeks
- Tag audit: unused tags, inconsistent tag hierarchies
- Missing frontmatter: notes without proper metadata

**Actions:**
- Merge duplicates
- Archive stale items
- Fix broken links
- Consolidate tags
- Clean up orphaned resources

### 6. Meeting Import

Google Meet → Obsidian via two-phase pipeline (requires Google Workspace MCP).

See `references/google-meet-integration.md` for full specification.

**Phase 1 (Import):**
1. Pull new meeting notes from configured Google Drive folder
2. Save to `Shared/Meeting-Notes/` with `status: to-review`
3. Store transcript in collapsed callout
4. Update import state file

**Phase 2 (Process):**
1. Find notes with `status: to-review` and `source/google-meet` tag
2. PROPOSE (not execute):
   - CRM entries for mentioned people
   - Action items/ClickUp tasks
   - Wikilinks to vault notes
3. Wait for confirmation
4. Execute approved changes

## Frontmatter Specification

Every note in the vault should include frontmatter with at minimum: type, status, tags, created.

```yaml
---
type: note|task|project|idea|meeting|journal|resource
status: inbox|active|stuck|waiting|done|archived
tags: []
created: YYYY-MM-DD
---
```

**Extended frontmatter fields:**

| Field | Type | Example | Usage |
|-------|------|---------|-------|
| type | string | note, task, project, idea, meeting, journal, resource | Categorizes the note |
| status | string | inbox, active, stuck, waiting, done, archived | Current state |
| tags | array | [area/work, project/alpha, type/decision] | Flat tag hierarchy |
| created | date | 2024-02-25 | Creation date (YYYY-MM-DD) |
| area | string | work, growth, health | Life area |
| next-step | string | "Schedule follow-up call" | Next actionable step |
| waiting-on | string | "Alex's feedback" | What's blocking progress |
| due | date | 2024-03-15 | Due date if time-sensitive |
| energy | string | high, medium, low | Energy cost to complete |
| related | array | [[note1]], [[note2]] | Related notes |
| added-by | string | yourname | For shared vault contribution tracking |

**Rules:**
- Dates always in YYYY-MM-DD format
- type and status are required
- tags should use flat hierarchy with forward slash: #area/work, #project/name, #status/active
- next-step should be filled for all actionable items
- One idea per note when possible

## Linking and Connections

**Wikilinks:** Use internal wikilinks for all connections within vault
```markdown
[[note-name]]
[[folder/note-name]]
[[note-name|display text]]
```

**External Links:** Use markdown links for external references
```markdown
[Display Text](https://example.com)
```

**Linking Strategy:**
- Prefer linking to existing notes over creating new ones
- Link bidirectionally when relevant (if A links to B, B should reference A)
- Use meaningful link context: don't just drop a link, explain the connection
- Create index notes or query pages for conceptual clusters

## Tag Conventions

Tags use a flat hierarchy with forward slashes (not nested folders):

**Status Tags** (mutually exclusive):
- `#status/inbox` — unprocessed
- `#status/active` — currently working on
- `#status/stuck` — blocked, needs help
- `#status/waiting` — depends on external person/thing
- `#status/done` — completed
- `#status/archived` — no longer relevant

**Area Tags:**
- `#area/work` — professional projects
- `#area/growth` — learning, development
- `#area/health` — fitness, wellness, nutrition

**Type Tags:**
- `#type/meeting` — meeting notes
- `#type/decision` — decision records
- `#type/reference` — reference material
- `#type/daily` — daily note
- `#type/weekly-review` — weekly reflection
- `#type/idea` — ideas and brainstorms

**Project Tags:**
- `#project/<project-name>` — scope tags for specific projects
- Create new project tags as needed

**Source Tags:**
- `#source/google-meet` — from Google Meet import
- `#source/slack` — from Slack capture
- `#source/email` — from email

**CRM Tags:**
- `#crm/person` — person in contact list
- `#crm/company` — company in contact list

## Behaviors and Principles

**Response Patterns:**
- Always check CLAUDE.md first for vault-specific rules
- Always report what was done (file created, moved, updated)
- Provide summary of changes at the end

**Philosophy:**
- Capture > perfection — get ideas captured, refine later
- Reduce decision fatigue — offer defaults, sensible suggestions
- Surface next-step prominently — actionable items first
- Graceful degradation — work with or without MCP, filesystem-first

**Data Integrity:**
- Never delete files without confirmation
- Always preserve user's original text (edit in-place, don't rewrite)
- Maintain timestamps (don't update created date on existing notes)
- Check for duplicates before creating new notes

## API-Enhanced Workflows

When the Obsidian MCP server is available:

**Search Enhancement:**
- Use indexed search endpoint for faster, more powerful vault queries
- Support fuzzy matching and advanced filters
- Return ranked results with relevance scores

**Read/Write Operations:**
- Use MCP endpoints to read/write notes instead of filesystem
- Benefit from Obsidian's real-time validation
- Support Obsidian plugin constraints (e.g., no files in root)

**Live App Integration:**
- Offer to open notes in Obsidian app
- Update sidebar and view on file changes
- Support tag/link autocomplete

**Dataview Queries:**
- Execute live DQL queries (requires Dataview plugin)
- Embed results in notes dynamically
- Generate dashboard queries

**Graceful Degradation:**
- If MCP unavailable: fall back to filesystem access
- If Dataview unavailable: generate query syntax for manual execution
- If app not running: continue with file operations

## Configuration and Prerequisites

**Required:**
- Obsidian (free version OK)
- Local vault directory with standard structure
- Claude Code access

**Optional but Recommended:**
- Obsidian REST API community plugin (for MCP server)
- Dataview community plugin (for live queries)
- Google Workspace MCP (for meeting import)
- ClickUp MCP (for task creation)

**Customization:**
- Modify vault structure in CLAUDE.md
- Add domain subfolders under Projects/
- Define custom tags in TAGS.md
- Extend templates in Templates/ folder
- Add MCP connections for external tools

See `references/setup.md` for full setup instructions and `references/conventions.md` for templates and naming rules.
