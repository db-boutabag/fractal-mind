# Vault Constitution

## Owner

{{Your Name}}

---

## Structure

The vault is organized using the **PARA** system (Projects, Areas, Resources, Archive) with domain-specific subfolders.

**Top-level folders:**
- `Inbox/` — Zero-friction captures, to be processed
- `Projects/` — Personal non-work projects only
- `Areas/` — Ongoing responsibilities
- `Resources/` — Reference material and knowledge base
- `Archive/` — Completed or shelved items
- `Daily/` — Daily notes and periodic reviews
- `Templates/` — Note templates
- `Meta/` — Vault constitution and settings (this file, TAGS.md)
- `Shared/` — All work content — git-synced team folder

**Routing rule:** All work/team content → `Shared/`. `Projects/` is reserved for personal non-work projects only.

**Shared/ domain subfolders:**
- `CRM/` — Shared relationship intelligence (People, Companies)
- `Brand/` — Brand identity, guidelines, voice, strategy
- `Strategy/` — Business plans, positioning, thesis
- `Product/` — Features, specifications, UX, testing
- `Marketing/` — Campaigns, outreach, content, user acquisition
- `Engineering/` — Architecture, infrastructure, tech decisions
- `Ops/` — Operations, sprint plans, team cadence
- `Intel/` — Competitive research, market landscape
- `Meeting-Notes/` — Meeting notes (`Internal/` for team, `External/` for outside calls)
- `Docs/` — Shared documents
- `Archive/` — Completed shared work

---

## Rules

### File Naming
- **Lowercase kebab-case** for all files: `my-project-name.md`
- **Daily notes:** `YYYY-MM-DD.md` (e.g., `2025-02-25.md`)
- **Weekly reviews:** `YYYY-Www-review.md` (e.g., `2025-W08-review.md`)
- **Clear, descriptive names** that stand alone

### Frontmatter
Every note must have frontmatter with at minimum:
```yaml
---
type: note|task|project|idea|meeting|journal|resource
status: inbox|active|stuck|waiting|done|archived
tags: []
created: YYYY-MM-DD
---
```

Optional extended fields:
- `area` — Area of responsibility
- `next-step` — Next action (for active items)
- `waiting-on` — What/who you're waiting for
- `due` — Due date (YYYY-MM-DD)
- `energy` — Energy level required
- `related` — Related note references

### Content Rules
- **One idea per note** when possible — easier to link and reference
- **Always add next-step** for actionable items
- **Use [[wikilinks]]** for internal connections — builds knowledge graph
- **Use tags with nested hierarchy:** `#area/work`, `#project/name`, `#status/active`
- **Date format:** Always YYYY-MM-DD
- **When in doubt:** Put it in Inbox/ — process later

### Shared Vault
If using the shared vault:
- **Every shared file** requires `added-by` in frontmatter: `added-by: yourname`
- This tracks who created each file; git history tracks subsequent edits
- Don't rename Shared/ or its structure — wikilinks depend on it
- Shared content is accessible from personal notes via wikilinks

---

## Vault Constitution

**My approach to this vault:**

1. **Bias toward action over asking questions** — Capture first, organize second
2. **Keep notes concise** — Expand later if needed
3. **Surface stuck items and next-steps prominently** — Make progress visible
4. **Link everything** — Connections reveal patterns
5. **Regular maintenance** — Weekly reviews, monthly audits
6. **Treat this as a thinking tool** — Not a filing system

---

## Preferences & Customization

### Editor Settings
- Display markdown preview by default
- Enable spell check
- Use word wrap

### Plugins
- **Dataview** — For dynamic queries and dashboards
- **Obsidian REST API** — For MCP integration (optional)
- **Daily Notes** — For daily note creation
- **Templates** — For template insertion
- **Quick Switcher** — For fast note navigation

### Keyboard Shortcuts
Configure these for efficiency:
- Create daily note
- Insert template
- Open Vault command palette

---

## Workflows

### Capture Workflow
1. Brain dump or quick note → Inbox/
2. Decide: type, area, tags
3. Add minimal frontmatter
4. Link to related notes
5. Process Inbox weekly

### Inbox Processing
1. Read Inbox/ files
2. Add/refine frontmatter
3. Move to appropriate folder
4. Add wikilinks
5. Set next-step for actionable items

### Periodic Notes
1. **Daily notes:** Morning intention-setting, evening reflection
2. **Weekly reviews:** Summarize week, surface patterns, plan next week
3. Check these weekly for patterns and progress

### Query & Synthesis
1. Use Dataview for structured queries
2. Check TAGS.md for common tag patterns
3. Use search to follow connection trails
4. Synthesize findings into new notes

### Maintenance
1. **Monthly:** Audit Inbox, mark stuck items, scan for broken links
2. **Quarterly:** Review Archive, surface any items to revisit
3. **Ongoing:** Keep frontmatter current, update tags as patterns emerge

---

## Tag Reference

See `Meta/TAGS.md` for the full tag system. Key principle: flat hierarchy with nested namespaces (`#area/work`, `#status/active`, `#project/name`).

---

## Contact & Collaboration

If this is a shared vault, see `Shared/TEAM-SETUP.md` for collaboration guidelines.

---

## Last Updated

{{date-updated}}
