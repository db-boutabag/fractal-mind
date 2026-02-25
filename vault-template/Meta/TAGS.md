# Tag Reference

Tags organize your vault and make it machine-queryable. Use nested hierarchy: `#area/work`, `#status/active`, `#project/name`.

---

## Status Tags (Mutually Exclusive)

Use exactly one status tag per note.

| Tag | Meaning | When to Use |
|-----|---------|------------|
| `#status/inbox` | Unprocessed, needs categorization | Just captured something, not yet organized |
| `#status/active` | Currently working on | In progress, actively engaging |
| `#status/stuck` | Blocked, needs help | Waiting for clarity, resource, or decision |
| `#status/waiting` | Depends on someone/something external | Waiting for feedback, approval, external event |
| `#status/done` | Completed | Finished, shipped, resolved |
| `#status/archived` | No longer relevant | Shelved, deprioritized, historical reference |

---

## Area Tags

Areas are ongoing responsibilities or domains.

- `#area/work` — Work-related, professional
- `#area/growth` — Learning, personal development
- `#area/health` — Physical, mental, emotional health

Add more areas as needed (e.g., `#area/family`, `#area/finance`).

---

## Type Tags

Note type for classification and querying.

| Tag | Meaning |
|-----|---------|
| `#type/meeting` | Meeting notes or agenda |
| `#type/decision` | Decision or decision point |
| `#type/reference` | Reference material or knowledge |
| `#type/daily` | Daily note |
| `#type/weekly-review` | Weekly reflection and planning |
| `#type/project` | Project overview |
| `#type/task` | Task or action item |
| `#type/idea` | Idea or brainstorm |
| `#type/resource` | External resource or reference |

---

## Project Tags

Add new project tags as projects are created. Format: `#project/<project-name>`.

Examples:
- `#project/website-redesign`
- `#project/product-launch`
- `#project/team-onboarding`
- `#project/q2-strategy`

---

## CRM Tags

For relationship intelligence entries.

- `#crm/person` — Individual contact
- `#crm/company` — Company or organization

---

## Custom Tags

Add domain-specific tags as needed:
- `#source/<where-you-found-it>` — Where the information came from
- `#tool/<application>` — Related to a specific tool
- `#context/<situation>` — Contextual information

---

## Query Examples

Common Dataview queries using these tags:

### All Active Items
```dataview
LIST
FROM #status/active
SORT created DESC
```

### Work Items This Week
```dataview
LIST
FROM #area/work AND #status/active
WHERE created >= date(today) - dur(7 days)
```

### Stuck Items Needing Attention
```dataview
LIST
FROM #status/stuck
SORT created
```

### Weekly Reviews
```dataview
LIST
FROM #type/weekly-review
SORT created DESC
LIMIT 5
```

### All Project Items
```dataview
TABLE status, area
FROM #project/*
WHERE status != "archived"
SORT created DESC
```

### Meeting Notes by Month
```dataview
LIST
FROM #type/meeting
SORT created DESC
```

---

## Best Practices

1. **Use status tags consistently** — Every note needs exactly one status
2. **Add area tags** — Helps with filtering by responsibility
3. **Add type tags** — Makes querying and analysis easier
4. **Project tags are dynamic** — Create new ones as projects emerge
5. **Tag during capture, refine during processing** — Start quick, perfect later
6. **Use tags to surface patterns** — Run monthly queries to see what's active vs. stuck
7. **Review TAGS.md monthly** — Add new tags as your vault evolves

---

## Tag Hygiene

### Monthly Audit
Check for:
- Orphaned tags (tags with no notes)
- Misspelled tags (duplicate variations)
- Unused custom tags

### Deprecation
If a tag is no longer useful:
1. Replace all instances with active tag
2. Remove from this reference
3. Note the deprecation in git commit

### Evolution
As your vault grows, tags will evolve. That's okay. Update this file to reflect your actual tagging schema.

---

## Integration with Frontmatter

In your note frontmatter, list tags as an array:

```yaml
---
type: note
status: active
tags: [#area/work, #type/project, #project/website-redesign]
created: 2025-02-25
---
```

Keep this list focused — 2-4 tags per note is typical. Too many tags dilutes the signal.
