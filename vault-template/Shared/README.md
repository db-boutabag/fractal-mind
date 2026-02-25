# Shared Vault

This folder contains shared Obsidian content for team collaboration. All files are tracked in git and synchronized across team members' vaults.

---

## Structure

```
Shared/
├── CRM/                    # Relationship intelligence (People, Companies)
│   ├── People/
│   └── Companies/
├── Brand/                  # Brand identity, guidelines, positioning
├── Strategy/               # Business plans, thesis, fundraising
├── Product/                # Features, specs, UX decisions
├── Marketing/              # Campaigns, outreach, content strategy
├── Engineering/            # Architecture, infrastructure, tech decisions
├── Intel/                  # Competitive research, market landscape
├── Meeting-Notes/          # Shared meeting notes
├── Docs/                   # Ad-hoc shared documents
└── Archive/                # Completed or shelved shared work
```

---

## Conventions

### Frontmatter

Every shared file must include `added-by` in its frontmatter to track who created it:

```yaml
---
type: note
status: active
tags: [area/work]
created: 2025-02-25
added-by: yourname
---
```

**Why:** Git history tracks subsequent edits, but `added-by` makes authorship clear at a glance.

### Naming

- Files: `lowercase-kebab-case.md`
- Dates: `YYYY-MM-DD` format
- Clear, descriptive names that work standalone

### Linking

Use wikilinks to connect shared notes to each other and to personal vault notes:
- `[[alex-rivera]]` — Link to a person
- `[[product-roadmap]]` — Link to a doc
- `[[Q2-strategy]]` — Link to a project

Wikilinks work seamlessly across personal and shared content.

---

## Collaboration Guidelines

1. **Check before creating** — Search existing files to avoid duplication
2. **Add to Shared/ if it benefits the team** — Not everything needs to be shared; default to personal
3. **Keep it current** — Update shared notes when information changes
4. **Run monthly audits** — Archive completed work, clean up orphaned files
5. **Pull before you push** — Always sync before making changes (handled by auto-sync if enabled)
6. **Communicate changes** — Let the team know about significant updates
7. **Respect ownership** — Don't modify someone else's `added-by` field

---

## Dataview Dashboards

The Shared/ folder includes Dataview queries for common analytics:
- **People by company** — See all contacts organized by where they work
- **Needs followup** — Contacts not contacted in 90+ days
- **By relationship type** — Collaborators, advisors, investors, etc.
- **Active projects** — All shared projects in progress

Run these queries to surface insights about team relationships and work status.

---

## Auto-Sync Setup

If your team has enabled git auto-sync, changes in Shared/ are automatically committed and pushed every N minutes. See `TEAM-SETUP.md` for configuration details.

---

## Merging Conflicts

Git conflicts are rare but can happen when two people edit the same file simultaneously. If you see a conflict:

1. Pull the latest version: `git pull origin main`
2. Open the conflicted file in your editor
3. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
4. Manually resolve (usually just keeping both versions)
5. Commit the resolution

The team lead can help if this happens.

---

## Wikilink Behavior

Wikilinks work across your entire vault. When you link from personal notes to Shared/:
- Personal note → Shared note: Works great, creates connection
- Shared note → Personal note: Works, but creates tight coupling (use sparingly)

Prefer linking FROM shared content TO personal (many team members can share links to one person's research).

---

## Important Notes

- **Don't rename Shared/** — Wikilinks from personal notes depend on this path
- **Don't reorganize subfolders** — Coordinate with the team before structural changes
- **Don't commit directly** — Use the UI to make changes; auto-sync handles the commit
- **Shared/ is not for personal stuff** — Keep it focused on team-valuable content
- **Archive aggressively** — Move completed work to Archive/ monthly

---

## Next Steps

1. Read `TEAM-SETUP.md` for full setup and sync instructions
2. Review the domain folder guidelines for your area
3. Check existing notes to understand the team's conventions
4. Start creating!

---

## Questions?

See `TEAM-SETUP.md` or ask your vault steward.
