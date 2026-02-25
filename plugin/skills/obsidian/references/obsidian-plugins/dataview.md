# Dataview Query Language (DQL) Reference

Complete guide to using Dataview in your Obsidian vault with fractal-mind.

## Overview

Dataview is a powerful query engine for Obsidian that lets you search, filter, and organize notes based on their frontmatter and content. It's essential for building dashboards, tracking projects, and discovering insights in your vault.

**Key Capabilities:**
- Query notes by type, status, tags, dates
- Build dynamic lists, tables, and calendars
- Group and sort results
- Calculate summaries (count, sum, average)
- Embed results in notes
- Live updates as vault changes

## Installation

1. Open Obsidian
2. Go to Settings → Community Plugins → Browse
3. Search for "Dataview"
4. Install and enable

Enable JavaScript queries (optional but recommended):
Settings → Dataview → Enable inline JavaScript queries

## DQL Basics

### Query Structure

Most Dataview queries follow this pattern:

```dataview
<TYPE>
FROM <SOURCE>
WHERE <CONDITION>
SORT <FIELD> [ASC/DESC]
GROUP BY <FIELD>
LIMIT <NUMBER>
```

**Types:**
- `LIST` — unordered list of results
- `TABLE` — table with specified columns
- `TASK` — task view (for task items)
- `CALENDAR` — calendar heatmap

### Simple Example

```dataview
LIST
FROM #status/active
```

Shows all notes tagged with `#status/active` as a list.

## Source Types (FROM)

Specify where to search:

### By Folder

```dataview
LIST
FROM "Projects"
```

Queries all notes in Projects/ folder (including subfolders).

### By Tag

```dataview
LIST
FROM #area/work
```

Queries all notes with `#area/work` tag.

### By Link

```dataview
LIST
FROM [[project-alpha]]
```

Queries all notes that link to `[[project-alpha]]`.

### Combine Multiple Sources

```dataview
LIST
FROM #status/active OR #status/stuck
```

Union: notes with either tag.

```dataview
LIST
FROM "Projects" AND #area/work
```

Intersection: notes in Projects folder AND tagged with area/work.

## Filtering (WHERE)

Filter results based on conditions:

### Equality

```dataview
LIST
FROM "Projects"
WHERE status = "active"
```

All active projects (uses frontmatter `status` field).

### Inequality

```dataview
LIST
FROM #type/task
WHERE status != "done"
```

All incomplete tasks.

### Comparison

```dataview
LIST
FROM "Projects"
WHERE due < date(today)
```

All overdue items.

```dataview
LIST
FROM #type/project
WHERE created > date("2024-01-01")
```

All projects created after Jan 1.

### Checking for Fields

```dataview
LIST
FROM "Projects"
WHERE next-step
```

All notes that have a `next-step` field.

```dataview
LIST
FROM "Projects"
WHERE !waiting-on
```

All notes that DON'T have `waiting-on` field.

### Contains (Text Matching)

```dataview
LIST
FROM "Projects"
WHERE contains(tags, "project/alpha")
```

Notes where tags array contains "project/alpha".

```dataview
LIST
FROM "Projects"
WHERE contains(lower(type), "task")
```

Notes where type contains "task" (case-insensitive).

### Multiple Conditions

```dataview
LIST
FROM #type/project
WHERE status = "active" AND area = "work" AND !stuck
```

Projects that are active, work-related, and not stuck.

## Sorting (SORT)

Order results by field:

```dataview
LIST
FROM #status/active
SORT created DESC
```

Most recently created active items first.

```dataview
LIST
FROM #type/project
SORT due ASC
```

Projects by due date (soonest first).

### Multi-field Sort

```dataview
LIST
FROM #type/task
SORT area ASC, due ASC
```

Sort by area first, then by due date within each area.

## Grouping (GROUP BY)

Group results by field values:

```dataview
LIST
FROM #type/task
GROUP BY area
```

Group tasks by their `area` field:
```
Area: Work
- Task 1
- Task 2

Area: Growth
- Task 3
- Task 4
```

### With Sorting

```dataview
LIST
FROM #status/active
SORT created DESC
GROUP BY area
```

Group by area, with most recently created items first within each group.

## Limiting (LIMIT)

Restrict number of results:

```dataview
LIST
FROM #status/active
LIMIT 10
```

Show only first 10 active items.

## Columns in Tables

Use `TABLE` to show specific fields:

```dataview
TABLE type, status, due
FROM "Projects"
```

Shows table with columns: type, status, due date.

### Rename Columns

```dataview
TABLE created as "Date Created", status as "Status"
FROM "Projects"
```

### Calculated Columns

```dataview
TABLE created as "Created", today - created as "Days Old"
FROM #type/note
```

## Calendar View

Visualize dates in calendar format:

```dataview
CALENDAR created
FROM #type/daily
```

Shows each daily note on calendar by creation date.

```dataview
CALENDAR due
FROM #type/task
WHERE status != "done"
```

Shows all incomplete tasks on calendar by due date.

## Common Vault Queries

These are useful queries for managing your vault:

### Active Work

Show all currently active items:

```dataview
TABLE type, status, created, next-step
FROM "Projects"
WHERE status = "active"
SORT created DESC
```

### Stuck or Blocked

All items needing help:

```dataview
LIST
FROM ""
WHERE status = "stuck" OR status = "waiting"
SORT created DESC
```

### Tasks Due This Week

```dataview
LIST
FROM #type/task
WHERE due >= date(today) AND due <= date(today) + dur(7 days) AND status != "done"
SORT due ASC
```

### Recent Captures

Last 20 notes created:

```dataview
LIST
FROM "Inbox"
SORT created DESC
LIMIT 20
```

### Meetings This Week

```dataview
LIST
FROM #type/meeting
WHERE created >= date(today) - dur(7 days)
SORT created DESC
```

### Notes by Area

Group all active work by life area:

```dataview
LIST
FROM ""
WHERE status = "active"
SORT area ASC
GROUP BY area
```

### Items Needing Next-Steps

All actionable items without a next-step defined:

```dataview
LIST
FROM ""
WHERE type = "task" OR type = "project"
WHERE !next-step
```

### Project Progress

Show all projects with key results:

```dataview
TABLE objective, key-results
FROM #type/project
WHERE status != "archived"
SORT created DESC
```

### Waiting On Others

Items dependent on external action:

```dataview
TABLE waiting-on, due
FROM ""
WHERE status = "waiting"
SORT due ASC
```

### Archive Cleanup

Find old archived items (candidates for deletion):

```dataview
LIST
FROM ""
WHERE status = "archived" AND created < date(today) - dur(365 days)
SORT created DESC
```

### CRM Dashboard

All contacts with recent interactions:

```dataview
TABLE company, relationship, last-contact
FROM #crm/person
WHERE last-contact
SORT last-contact DESC
LIMIT 20
```

### Energy Tracking

Show high-energy work available:

```dataview
LIST
FROM ""
WHERE energy = "high" AND status = "active"
SORT area ASC
GROUP BY area
```

## Embedding Queries in Notes

Insert Dataview results directly into notes using code blocks:

### In a Dashboard Note

Create `Meta/Dashboard.md`:

````markdown
# Dashboard

## Active Projects

```dataview
LIST
FROM #type/project
WHERE status = "active"
SORT created DESC
```

## This Week's Tasks

```dataview
TABLE due, next-step
FROM #type/task
WHERE status != "done"
AND due >= date(today)
AND due < date(today) + dur(7 days)
SORT due ASC
```

## Meetings This Week

```dataview
LIST
FROM #type/meeting
WHERE created >= date(today) - dur(7 days)
SORT created DESC
```

## Notes by Area

```dataview
LIST
FROM ""
WHERE status = "active"
SORT area ASC
GROUP BY area
```
````

### In Project Notes

Track project status in project notes:

````markdown
# Project Alpha

Objective: Build new feature
Status: active

## Related Tasks

```dataview
TABLE due, status
FROM #project/alpha
WHERE type = "task"
SORT due ASC
```

## Team Members

```dataview
LIST
FROM #crm/person
WHERE contains(related, "project/alpha")
```
````

## Date Functions

Work with dates in queries:

```dataview
date(today)              # Today's date
date("2024-02-25")       # Specific date
date(today) + dur(7 days)     # Add duration
date(today) - dur(1 month)    # Subtract duration
today                    # Shorthand for date(today)
```

### Examples

```dataview
LIST
FROM ""
WHERE due < date(today)
```

Overdue items.

```dataview
LIST
FROM ""
WHERE created >= date(today) - dur(7 days)
```

Notes created in last 7 days.

## Operators

### Logical

- `AND` — both conditions true
- `OR` — at least one condition true
- `NOT` — condition is false (use `!` shorthand)

### Comparison

- `=` — equal
- `!=` — not equal
- `<` — less than
- `>` — greater than
- `<=` — less than or equal
- `>=` — greater than or equal

### Functions

- `contains(array, value)` — array contains value
- `startswith(text, prefix)` — text starts with prefix
- `endswith(text, suffix)` — text ends with suffix
- `lower(text)` — convert to lowercase
- `upper(text)` — convert to uppercase
- `length(array)` — count items in array
- `count()` — count results in group

## Advanced Examples

### Status Report

Show progress across all active projects:

```dataview
TABLE objective, key-results, status
FROM #type/project
WHERE status = "active"
SORT created DESC
```

### Weekly Review Data

Pull data for weekly review note:

```dataview
TABLE created as "Date", type, status, next-step
FROM ""
WHERE created >= date(today) - dur(7 days)
SORT created DESC
```

### Workload Analysis

Count items by status and area:

```dataview
LIST
FROM ""
WHERE status = "active" OR status = "stuck"
SORT area ASC
GROUP BY area
```

### Decision Log

Find all decisions made:

```dataview
LIST
FROM #type/decision
SORT created DESC
```

### Learning Path

Curate learning resources by topic:

```dataview
LIST
FROM "Resources"
WHERE contains(tags, "learning/...")
SORT created DESC
```

## Tips and Tricks

### Use Spaces Around Operators

```dataview
LIST
FROM ""
WHERE status = "active" AND area = "work"  # Good
```

### Case Sensitivity

Field names are case-sensitive:
```dataview
WHERE status = "active"   # Works
WHERE Status = "active"   # Breaks (if field is lowercase)
```

### Null/Missing Values

Fields that don't exist in a note are `null`:
```dataview
WHERE !next-step    # Notes without next-step field
WHERE next-step     # Notes with next-step field
```

### Test in Console

Dataview has a query console for debugging:
1. Open Command Palette (Cmd+P)
2. Run "Dataview: Open Query Console"
3. Test queries before embedding in notes

### Reference Current Note Fields

In a note, reference that note's fields:

```dataview
LIST
FROM [[project-alpha]]
WHERE assignee = this.created
```

(Advanced — use with caution)

## Performance Considerations

Large queries can be slow. Optimize:

```dataview
# Good — limits to folder
LIST
FROM "Projects"
WHERE status = "active"

# Bad — scans entire vault
LIST
WHERE status = "active"
```

For vault-wide queries, use tags:

```dataview
# Good — uses tag index
LIST
FROM #status/active

# OK but slower
LIST
WHERE status = "active"
```

## Troubleshooting

**"No results found"**
- Check field names match frontmatter exactly
- Verify source (FROM clause) is correct
- Test with simpler query first
- Use Dataview console to debug

**"Query syntax error"**
- Check quotes are straight quotes, not smart quotes
- Verify boolean logic (AND/OR precedence)
- Check date format: `date("YYYY-MM-DD")`

**"Query is slow"**
- Reduce scope with FROM clause (use folder or tag)
- Add WHERE conditions to filter early
- Avoid full-vault scans

**Results showing `null` values**
- Note doesn't have that field
- Field name doesn't match exactly (case-sensitive)
- Frontmatter formatting is invalid

## More Resources

- **Obsidian Skill:** `SKILL.md` — how queries fit in workflow
- **Conventions:** `conventions.md` — field definitions and naming
- **Official Docs:** [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- **Query Assistant:** In Obsidian, go to Dataview plugin settings for query examples

## Quick Reference Card

```
LIST FROM "folder"        # List from folder
LIST FROM #tag            # List from tag
LIST FROM [[link]]        # List linking to note
TABLE col1, col2 FROM ... # Table with columns
TASK FROM ...             # Task list
CALENDAR field FROM ...   # Calendar view

WHERE status = "active"   # Filter by field
WHERE !field              # Missing field
WHERE field > date(...)   # Date comparison
WHERE contains(arr, val)  # Array contains

SORT field ASC/DESC       # Order results
GROUP BY field            # Group results
LIMIT 10                  # Max results
```
