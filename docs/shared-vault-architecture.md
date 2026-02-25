# Shared Vault Architecture — Design & Scaling Guide

This document covers the architectural decisions behind fractal-mind's shared vault, how to use it effectively, and when to consider alternatives as your team grows.

---

## The Shared Vault: What It Is

The shared vault is a **git-synced subfolder** within each team member's personal Obsidian vault (typically `Vault/Shared/`). It contains collaborative knowledge: meeting notes, research, decisions, contact information, and domain-specific reference material.

**Key insight:** It's not a separate vault, and it's not a hosted solution. It's a structured folder that lives inside your personal vault, synced via git, with contribution tracking via frontmatter.

---

## Why Not A Separate Vault?

You might ask: "Why not just use a separate Obsidian vault for team collaboration?"

### Single Vault Advantages

**1. Unified Wikilink Graph**
- Personal and shared content can link freely with `[[wikilinks]]`
- A note about a personal project can reference `[[Shared/CRM/alex-rivera]]` without friction
- Dataview queries can span both personal and shared content in one search
- No manual sync between two wikilink systems

**2. Simpler Backlinks & Graph Visualization**
- Obsidian's graph shows ALL connections across personal and shared
- Orphaned notes are visible regardless of vault boundary
- Context is complete: see how a person connects across both domains

**3. Unified Search**
- Obsidian search (Ctrl/Cmd+Shift+F) finds everything in one place
- No need to context-switch between two vault instances
- Claude Code can read/write both with a single vault path

**4. Single Plugin Configuration**
- Dataview, ClickUp integration, and other plugins configured once
- No duplicate settings management

**5. Single MCP Server Connection**
- One Obsidian REST API connection serves both personal and shared
- Fewer authentication flows to manage
- Single .mcp.json file

### The Trade-off

The cost: your shared folder is **inside** your vault, visible to all tools and searches. Mitigation:
- Use `.gitignore` to prevent accidental private data in Shared/
- Shared/ README and TEAM-SETUP.md document boundaries clearly
- Convention: only shared/team content goes in Shared/

---

## How Wikilinks Work Across Personal & Shared

Wikilinks are **vault-relative paths**. In a single vault, this is straightforward:

```markdown
In a personal note (Projects/brand/messaging.md):
[[Shared/Brand/brand-guidelines]]  # Links to Shared/Brand/brand-guidelines.md

In a shared note (Shared/CRM/alex-rivera.md):
[[../../Projects/Brand/messaging]]  # Links back to personal Projects folder
```

**Best Practice:** Always use relative paths from the note's location, or prefer full vault-relative paths starting from Vault/:

```markdown
# Unambiguous — always works
[[Shared/CRM/alex-rivera]]
[[Projects/Product/roadmap]]
```

### Backlinks Across Boundaries

If you open `Shared/CRM/alex-rivera.md`, the backlinks pane shows:
- All notes (personal or shared) that link to it
- The full relationship graph is intact
- You see the complete context for that contact

This is impossible in a two-vault setup without external tools.

---

## The `added-by` Convention for Contribution Tracking

Every shared file includes an `added-by` frontmatter field to track **who created each shared note**.

```yaml
---
type: meeting
status: active
tags: [type/meeting, area/work]
created: 2025-02-15
added-by: alex-rivera
---

# Engineering Sync — 2025-02-15

...
```

**Why this matters:**
- Git history tracks *edits*, but not the original creator
- `added-by` makes it easy to ask "who started this note?" without git log archaeology
- Useful for:
  - Quick contact if you need context: "Added-by: Jamie Park — ask Jamie about this research"
  - Attribution in shared documents
  - Dataview dashboards: "Notes added by Jamie this month"

**Convention:**
- Use your username or short identifier (e.g., `alex-rivera`, not `Alex Rivera`)
- Auto-import scripts use `added-by: auto-import`
- If you substantially rebuild someone else's note, leave `added-by` as-is (it's not a "last editor" field)

**Dataview Query for Attribution:**

```dataview
LIST
FROM "Shared"
WHERE added-by = "alex-rivera"
SORT created DESC
```

---

## Why Flat Domain Folders (Not PARA in Shared)

The shared vault uses a **flat domain structure**, not PARA:

```
Shared/
├── CRM/
├── Brand/
├── Strategy/
├── Product/
├── Marketing/
├── Engineering/
├── Intel/
├── Meeting-Notes/
├── Docs/
└── Archive/
```

**NOT nested PARA:**
```
Shared/
├── Projects/
│   ├── Brand/
│   ├── Strategy/
│   └── ...
├── Areas/
├── Resources/
└── Archive/
```

### Why Flat Wins for Teams

**1. Shared content is reference, not active work**
- PARA (Projects/Areas/Resources/Archive) works for individual workflows
- Shared content is mostly **reference**: decisions made, research done, people met
- These don't fit naturally into "active work" categories

**2. Domain clarity**
- Domain folders (Brand/, Product/, etc.) make it obvious which team owns each section
- A flat structure reduces cognitive load: "Where is the brand doc?" → "Shared/Brand/"
- Nested PARA adds a layer: "Where is the brand doc?" → "Is it in Projects/Brand or Resources/Brand?"

**3. Team permissions are easier
- Future expansions (Obsidian Sync, other tools) often support folder-level permissions
- Flat domains map to team structure clearly
- "Only Marketing can edit Shared/Marketing/" is simpler to enforce than nested structures

**4. Cross-functional reference is clearer**
- CRM folder is obviously the shared contact database, distinct from personal contacts
- Meeting-Notes/ is clearly shared meeting records, distinct from personal notes
- No ambiguity about whether Archive/ is personal or shared

**5. Simpler onboarding**
- New team members see the domain folders and immediately understand structure
- Flat > nested for clarity in shared contexts

---

## Scaling: Team Size & Sync Mechanism

This architecture works well for **2–5 people**. The git-based sync handles occasional conflicts gracefully, and a single human can resolve merge issues.

### 2–5 People: Git-Sync Works Great

At this scale:
- Conflicts are rare (different team members editing different files)
- When conflicts occur, they're usually easy to resolve (different sections of the same file)
- `shared-sync.sh` with launchd/cron keeps everything in sync
- No external infrastructure needed (git repo on GitHub, GitLab, or self-hosted)
- Cost: free to ~$10/month for private git hosting

**Sync Frequency:** Every 5–15 minutes via launchd/cron is ideal. Fast enough to feel real-time, slow enough to batch changes.

### 5–15 People: Consider Alternatives

As your team grows:

**1. Obsidian Sync (easiest migration)**
- Drop-in replacement for git-sync
- Built-in conflict resolution
- ~$15/month per user
- Works with existing shared vault structure (no changes needed)
- Disadvantage: no offline-first git history

**2. Obsidian Publish + Hub (content-focused)**
- If shared vault is mostly reference/documentation
- Publish selected folders as a team wiki
- ~$20/month + ~$10/month per shared vault
- Downside: read-only for team (can't collab on Publish)

**3. Separate Collaboration Tool**
- Move shared content to Notion, Confluence, or similar
- Obsidian remains personal
- Import/export pipelines to keep content in sync
- More friction than native git-sync

**4. Self-Hosted Git + Sync Daemon**
- Custom sync script deployed on a VPS
- Full control, still free/cheap
- Higher maintenance burden

**Migration Path:**

If you start with git-sync and outgrow it:
1. Stop adding new features to shared vault
2. Choose target platform (likely Obsidian Sync)
3. Export shared vault folder to target platform
4. Gradually migrate teams to read from new platform
5. Archive old shared vault folder as reference

**No data loss:** Since shared vault is just markdown, it's portable. You can export/import to any system.

---

## Operational Considerations

### Merge Conflict Handling

Git-synced vaults can have conflicts if two people edit the same file simultaneously.

**Prevention:**
- Different team members own different domains (Marketing owns Shared/Marketing/, etc.)
- Within a domain, different files for different topics
- Sync frequently (every 5–15 minutes prevents most conflicts)

**If Conflict Occurs:**

```
CONFLICT (content): Merge conflict in Shared/CRM/alex-rivera.md
Automatic merge failed; fix conflicts and then commit the result.
```

Resolution:
1. Open the conflicted file in Obsidian
2. Look for `<<<<<<<` / `=======` / `>>>>>>>` markers
3. Decide which version to keep, delete markers
4. Stage and commit the resolution
5. Push to sync across team

**Better:** Document which person owns edits to shared files, so conflicts are rare.

### Permission Boundaries

**Git + folder permissions (future):**
- Set up GitHub (or other) branch protection rules
- Require PR reviews for Marketing/ changes from marketing team members
- Prevent accidental overwrites

**Current:** Honor by convention. Shared folder README documents boundaries.

### Offline Work

Git sync is **offline-friendly:**
- All files cached locally
- Work offline without friction
- Changes sync when connection returns
- No "sync is pending" notification

This is a major advantage over cloud-only solutions like Obsidian Sync (which requires connectivity to resolve conflicts).

---

## The Added-By Workflow: Example

**Scenario:** Alex Rivera attends a meeting, imports notes into shared vault.

```yaml
# Shared/Meeting-Notes/2025-02-15-product-planning.md
---
type: meeting
status: active
tags: [type/meeting, area/work, project/roadmap]
created: 2025-02-15
added-by: alex-rivera
---

# Product Planning Meeting — 2025-02-15

Attendees: Alex Rivera, Jamie Park, Sam Torres
...
```

**Later:** Jamie Park wants to know who created this and might have context.

- Jamie sees `added-by: alex-rivera` and sends Alex a quick message
- Or runs a Dataview query: "Show me all meeting notes Alex created in the last month"

**Git history** still shows every edit (Jamie added notes, etc.), but `added-by` answers "whose meeting was this?"

---

## Wikilink Graph Example

Personal and shared vaults in one graph:

```
Projects/Brand/messaging.md
  ↓ links to
Shared/Brand/brand-guidelines.md
  ↓ links to
Shared/CRM/alex-rivera.md (external advisor)
  ↓ linked from
Projects/Strategy/Q1-planning.md
  ↓ also links to
Shared/Strategy/market-positioning.md
```

In a two-vault setup, Alex's profile would be isolated in the shared vault, with no direct visibility from your personal strategy note. In this unified approach, all context is immediate.

---

## Best Practices

### DO
- **Keep domains separate:** One person/team owns CRM/, another owns Marketing/
- **Use `added-by` for original author:** Essential for large teams
- **Sync frequently:** Every 5–15 minutes, not daily
- **Wikilink freely:** Link across personal ↔ shared at will
- **Version critical docs:** Use Git history for important decisions
- **Archive regularly:** Move old shared content to Archive/ annually

### DON'T
- **Use Shared/ for personal drafts:** Keep drafts in personal Projects/
- **Mix PARA in Shared/:** Keep domains flat at root level
- **Commit large binaries:** Git + markdown works great; files + PDFs do not
- **Skip the README:** Document Shared/ structure and boundaries clearly
- **Sync constantly:** Every minute is too frequent; log file will explode

---

## Security & Privacy

**By design, shared vault content is visible to everyone with vault access.**

If you need private content:
- Keep it in personal vault (not Shared/)
- Use `.gitignore` to prevent accidental pushes of private files
- Consider encrypting sensitive notes in Shared/ with Git LFS + encryption

**GitHub security:**
- Keep the shared vault repo private
- Grant access only to team members who need it
- Use branch protection rules to prevent accidents

---

## Conclusion

The shared vault architecture works because it:
1. **Unifies context** — personal and shared in one graph
2. **Scales simply** — git sync handles 2–5 people effortlessly
3. **Remains portable** — markdown stays portable if you switch tools
4. **Respects local-first principles** — offline-first, user-owned data

For teams larger than 5–10 people or those needing more formal permissions, migrate to Obsidian Sync or a dedicated collaboration platform. But for small teams, git-synced shared folders are hard to beat.
