# Vault Conventions

This document defines naming rules, frontmatter standards, and templates for the fractal-mind vault.

## Naming Rules

**File Names:**
- Lowercase with hyphens: `my-note-name.md`, `project-alpha-proposal.md`
- No spaces or special characters
- Descriptive but concise
- Prefer nouns that describe the content

**Folder Names:**
- Top-level folders: Title Case (`Inbox`, `Projects`, `Areas`, `Archive`)
- Domain subfolders: lowercase (`brand`, `strategy`, `product`, `marketing`, `meetings`, `ops`)
- Meta folders: Title Case (`Meta`, `Templates`, `Daily`, `Shared`)

**Date-Based Files:**
- Daily notes: `YYYY-MM-DD.md` (e.g., `2024-02-25.md`)
- Weekly reviews: `YYYY-Www-review.md` (e.g., `2024-W08-review.md`)
- Monthly summaries: `YYYY-MM-summary.md`

**Examples:**
- `quarterly-okr-review.md` (good)
- `Q1_OKR_Review.md` (bad — spacing, capitalization)
- `project-alpha-wireframes.md` (good)
- `alpha_wireframes_draft.md` (bad — unclear)
- `customer-interview-alice.md` (good)
- `Interview - Alice.md` (bad — spaces, special chars)

## Frontmatter Field Definitions

Every note should include a frontmatter block at the top:

```yaml
---
type: note
status: active
tags: []
created: 2024-02-25
---
```

### Core Fields (Required)

| Field | Type | Description | Values |
|-------|------|-------------|--------|
| type | string | What kind of note | note, task, project, idea, meeting, journal, resource, decision |
| status | string | Current state | inbox, active, stuck, waiting, done, archived |
| tags | array | Flat-hierarchy tags | See tag conventions section |
| created | date | Creation date | YYYY-MM-DD format |

### Extended Fields (Recommended for specific types)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| area | string | Life area this belongs to | work, growth, health |
| next-step | string | Next action or priority | "Schedule follow-up", "Review feedback" |
| waiting-on | string | What's blocking progress | "Alex's decision", "Design approval" |
| due | date | Due date if time-sensitive | 2024-03-15 |
| energy | string | Energy cost to complete | high, medium, low |
| related | array | Related note links | [[note1]], [[note2]] |
| added-by | string | Who added to shared vault | firstname (for shared vault tracking) |

### Type-Specific Fields

**Project notes:**
```yaml
---
type: project
objective: "Clear statement of what success looks like"
key-results: ["Result 1", "Result 2", "Result 3"]
---
```

**Task notes:**
```yaml
---
type: task
due: 2024-03-10
priority: high
assignee: "Name or team"
---
```

**Meeting notes:**
```yaml
---
type: meeting
attendees: ["Person 1", "Person 2"]
date: 2024-02-25
next-step: "What needs to happen next"
---
```

## Note Templates

### Standard Note

Use for general information capture, reference material, thoughts.

```markdown
---
type: note
status: active
tags: []
created: {{date}}
---

# {{title}}

## Overview

[Brief description of what this is about]

## Key Points

- Point 1
- Point 2
- Point 3

## Related Notes

- [[related-note-1]]
- [[related-note-2]]
```

### Project

Use for active projects, initiatives, goals.

```markdown
---
type: project
status: active
tags: [project/name, area/work]
created: {{date}}
objective: "What we're trying to accomplish"
key-results:
  - "Result 1"
  - "Result 2"
  - "Result 3"
next-step: "Next action or phase"
---

# {{title}}

## Objective

[Clear statement of what success looks like]

## Key Results

1. [Measurable result 1]
2. [Measurable result 2]
3. [Measurable result 3]

## Open Questions

- Question 1?
- Question 2?

## Log

### [Date]
- Update 1
- Update 2

### [Date]
- Update 3

## Related Notes

- [[stakeholder-notes]]
- [[technical-spec]]
- [[design-brief]]
```

### Meeting

Use for meeting notes, discussions, conversations.

```markdown
---
type: meeting
status: active
tags: [type/meeting, area/work]
created: {{date}}
attendees:
  - Person 1
  - Person 2
next-step: "What needs to happen next"
---

# {{title}}

**Date:** {{date}}
**Attendees:** {{attendees}}

## Agenda

- Topic 1
- Topic 2
- Topic 3

## Notes

### Topic 1

[Discussion summary and decisions]

### Topic 2

[Discussion summary and decisions]

## Action Items

- [ ] Action for Person 1
- [ ] Action for Person 2

## Next Meeting

- Date: [when]
- Agenda: [what to discuss]
```

### Daily Note

Use for daily planning, reflections, quick captures.

```markdown
---
type: journal
status: active
tags: [type/daily]
created: {{date}}
---

# {{date}} — Daily Note

## Focus Today

What's the main priority?

1. Task 1
2. Task 2
3. Task 3

## Captures

### Morning
- Thought 1
- Thought 2

### Throughout Day
- Observation 1
- Idea 1

## Done Today

- [x] Completed task 1
- [x] Completed task 2

## Reflections

What went well? What was hard? What did I learn?
```

### Weekly Review

Use for weekly reflections and planning.

```markdown
---
type: journal
status: done
tags: [type/weekly-review]
created: {{date}}
---

# Week of [Start Date] — Weekly Review

## Accomplishments

What did I accomplish this week?

- Accomplishment 1
- Accomplishment 2
- Accomplishment 3

## Open Threads

What's in progress but not done?

- Thread 1
- Thread 2

## Stuck / Blocked

What's stuck? What do I need help with?

- Item 1
- Item 2

## Patterns Noticed

What themes or patterns showed up?

- Pattern 1
- Pattern 2

## Next Week Priorities

1. Priority 1
2. Priority 2
3. Priority 3

## Related Notes

- [[project-name]]
- [[area-name]]
```

## CLAUDE.md Template

Your vault constitution — define rules and structure for Claude Code.

```markdown
# Vault Constitution

## Owner

{{owner}}

## Structure

**PARA Folders:**
- **Inbox/** — Zero-friction captures (process regularly)
- **Projects/** — Active work organized by domain
  - brand/
  - strategy/
  - product/
  - marketing/
  - meetings/
  - ops/
- **Areas/** — Ongoing responsibilities
  - work/
  - growth/
  - health/
- **Resources/** — Reference material and learning
- **Archive/** — Completed, shelved, or deprecated items

**Special Folders:**
- **Daily/** — Daily notes (YYYY-MM-DD.md)
- **Templates/** — Note templates
- **Meta/** — Vault-wide configuration (CLAUDE.md, TAGS.md)
- **Shared/** — Git-synced team collaboration folder (optional)

## Rules

**Dates:**
- Always use YYYY-MM-DD format for dates

**File Names:**
- lowercase-kebab-case for all file names
- No spaces, no special characters, no capital letters
- Descriptive but concise

**Frontmatter:**
- Every note must have: type, status, tags, created
- Minimum values: `type: note`, `status: inbox`, `tags: []`, `created: YYYY-MM-DD`
- Extended fields as needed: area, next-step, waiting-on, due, energy, related

**Linking:**
- Use [[wikilinks]] for all internal connections
- Links should have context (explain why you're linking)
- One idea per note when possible

**Tags:**
- Flat hierarchy using forward slash: #area/work, #project/name, #status/active
- Don't create nested tag folders — just prefix with category

**Defaults:**
- When unsure where a note belongs, put it in Inbox/ (process later)
- Bias toward action — capture first, refine later
- Surface next-step prominently for all actionable items

**Shared Vault** (if using):
- All shared files require `added-by` in frontmatter to track contributions
- Use Git history for tracking edits

## Preferences

**Principles:**
- Capture > perfection — get ideas saved, improve later
- Speed > features — fast capture is better than slow refinement
- Context > structure — meaningful links matter more than perfect hierarchy
- Action > planning — next-step is the most important field

**Behavior Expectations:**
- Process Inbox/ at least weekly
- Review and update active items regularly
- Create daily notes for important days
- Weekly reviews every Sunday (or custom day)
- Archive completed items and old drafts regularly

## Tag Reference

See **Meta/TAGS.md** for the complete tag taxonomy and definitions.

## Customization

To modify this vault:
1. Update this file with new rules or structure changes
2. Tell Claude Code the change via the `/obsidian` skill
3. Claude will handle migrations and updates
```

## TAGS.md Template

Complete reference of all tags used in your vault.

```markdown
# Tag Reference

This is the authoritative tag taxonomy for the vault. All tags must follow these conventions.

## Status Tags (Mutually Exclusive)

Use exactly one status tag per note to track its state.

- **#status/inbox** — Unprocessed captures, needs categorization
- **#status/active** — Currently working on this, in progress
- **#status/stuck** — Blocked, waiting on something external, needs help
- **#status/waiting** — Depends on someone else's action or decision
- **#status/done** — Completed, finished
- **#status/archived** — No longer relevant, shelved, or deprecated

## Area Tags

Life area this note belongs to. One or more per note.

- **#area/work** — Professional work, job-related projects
- **#area/growth** — Learning, skill development, personal growth
- **#area/health** — Physical health, fitness, wellness, nutrition

Add custom areas as needed (e.g., #area/family, #area/side-projects)

## Type Tags

What kind of information this note contains.

- **#type/meeting** — Meeting notes or discussion records
- **#type/decision** — Decision log or decision record
- **#type/reference** — Reference material, templates, guidelines
- **#type/daily** — Daily note or daily journal entry
- **#type/weekly-review** — Weekly reflection or review
- **#type/idea** — Ideas, brainstorms, explorations
- **#type/resource** — External resource or learning material

## Project Tags

Scope tags for specific projects. Create new ones as projects emerge.

- **#project/name** — Associate notes with named projects
- Example: #project/landing-page, #project/api-redesign, #project/q1-planning

## Source Tags

Where a note came from.

- **#source/google-meet** — From Google Meet auto-import
- **#source/slack** — Captured from Slack
- **#source/email** — From email capture
- **#source/external** — From external source (web article, etc.)

## CRM Tags

For relationship intelligence notes.

- **#crm/person** — Person in contact list
- **#crm/company** — Company in contact list
- **#crm/pending** — Contact info to be processed

## Suggested New Tags

As your vault grows, you might add:
- **#priority/high**, **#priority/medium**, **#priority/low** — for priority tracking
- **#client/name** — for client-specific notes
- **#skill/name** — for skill or capability notes
- **#tool/name** — for tool configuration or how-to notes

When adding new tags, update this file so Claude Code knows about them.

## Tag Usage Rules

- A note can have multiple tags
- Tags are for discovery and filtering, not structure
- Don't use tags to replace folder structure
- Review tags quarterly for cleanup
- Archive or delete unused tags

## Dataview Query Examples

Search for tags in your vault using Dataview:

```dataview
list
where tags
group by tags
```

Or search Obsidian:
`tag:#status/active` finds all active notes
`tag:#area/work` finds work-related notes
`tag:#project/name` finds notes tied to a specific project
```

---

## Migration from Other Systems

If migrating from Notion, Roam, or another system:

1. Export to markdown
2. Place files in Inbox/
3. Run `/obsidian` with "process inbox"
4. Claude will apply frontmatter and move to correct locations
5. Review and update links afterward

## Reference

- **Setup Guide:** `references/setup.md`
- **Dataview Syntax:** `references/obsidian-plugins/dataview.md`
- **ClickUp Integration:** `references/obsidian-plugins/clickup-integration.md`
- **Google Meet Import:** `references/google-meet-integration.md`
