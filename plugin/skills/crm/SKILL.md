# CRM Relationship Intelligence Skill

## Philosophy

This skill is **not** a comprehensive contact database. That belongs in your external CRM (HubSpot, Salesforce, etc.).

This **is** relationship intelligence: tracking people and companies you want to maintain meaningful relationships with. Not bulk contacts or cold outreach lists.

**Includes:**
- People you've met, want to meet, or collaborate with
- Advisors, investors, partners, collaborators
- Anyone with strategic value to your work

**Excludes:**
- Bulk contact databases
- Cold outreach lists
- One-off transactional contacts

---

## Vault Path

Set your vault path as an environment variable:
```
VAULT=/path/to/your/vault
```

All CRM files live in `$VAULT/Shared/CRM/` (or `$VAULT/CRM/` if not using a shared vault).

---

## CRM Structure

```
Shared/CRM/                (or CRM/ if personal)
  People/                  # One file per person
    alex-rivera.md
    jamie-park.md
    sam-torres.md
  Companies/               # One file per company
    meridian-labs.md
    apex-studio.md
    northlight-materials.md
  _views/                  # Dataview dashboards
    people-by-company.md
    needs-followup.md
    by-relationship-type.md
```

---

## Frontmatter Specs

### Person

```yaml
---
type: person
name: "Full Name"
company: "[[company-name]]"
role: Job Title
source: how-you-met
relationship: type-of-relationship
tags: [crm/person]
created: YYYY-MM-DD
last-contact: YYYY-MM-DD
next-step: "next action"
---
```

**Fields:**
- `name`: Full name (exactly as they introduce themselves)
- `company`: Wikilink to their company
- `role`: Current job title
- `source`: how you met (conference, warm-intro, cold-outreach, existing-network, online, etc.)
- `relationship`: type of relationship (collaborator, advisor, potential-customer, investor, friend, vendor, etc.)
- `created`: date you added them
- `last-contact`: date of last meaningful interaction
- `next-step`: what you should do next to maintain the relationship

### Company

```yaml
---
type: company
name: "Company Name"
industry: Industry
tags: [crm/company]
created: YYYY-MM-DD
---
```

---

## Workflows

### 1. Add Contact

Create a new person or company entry.

**Trigger:** User says "add contact", "add person", "add company", or describes someone/company they want to track

**Process:**
1. Ask clarifying questions if needed:
   - Full name
   - Company (if person)
   - Role (if person)
   - How you met
   - Type of relationship
2. Determine filename: `firstname-lastname.md` (lowercase, kebab case)
3. Create file in appropriate folder (People/ or Companies/)
4. Write frontmatter with all fields
5. Add context in body (how you know them, why they matter, interesting details)
6. Link to company if applicable
7. Report what was created

**Rules:**
- Never create entries without asking first
- One file per person, one file per company
- Always confirm before writing

### 2. Log Interaction

Update someone's last-contact and add context about the interaction.

**Trigger:** User says "log interaction", "mark contacted", "follow up with", or describes reaching out to someone

**Process:**
1. Find the person's file
2. Update `last-contact` to today's date
3. Add a dated entry in the body: `- [YYYY-MM-DD]: Brief note about the interaction`
4. Update `next-step` if there's a follow-up action
5. Report the update

### 3. Lookup

Find and summarize a contact's information.

**Trigger:** User asks "who is...", "tell me about...", or searches for someone

**Process:**
1. Search for the person or company
2. Read their file
3. Summarize: name, company, role, how you know them, last contact, next-step
4. Show related people/companies
5. Provide context from the body
6. Report last interaction date

### 4. Query

Structured searches across your relationships.

**Common queries:**
- "Who needs a followup?" — find contacts with `last-contact` more than 3 months ago
- "Show contacts from [company]" — filter by company
- "Who's a [relationship type]?" — filter by relationship type
- "People I met at [source]" — filter by source
- "Contacts with no next-step" — find contacts needing attention

**Process:**
1. Parse the query intent
2. Build appropriate Dataview filter
3. Return results with summary
4. Highlight actionable items

### 5. Maintain

Keep your CRM healthy.

**Maintenance tasks:**
- Stale contacts (no interaction in 6+ months)
- Missing fields (incomplete entries)
- Broken wikilinks (deleted companies)
- Duplicates (same person in multiple files)
- Orphaned entries (people with no associated company)

**Process:**
1. Scan the CRM folder
2. Identify issues
3. Report findings with suggestions
4. Ask before making changes

---

## Example Entries

### Person — Alex Rivera

File: `Shared/CRM/People/alex-rivera.md`

```yaml
---
type: person
name: "Alex Rivera"
company: "[[meridian-labs]]"
role: Product Manager
source: conference
relationship: collaborator
tags: [crm/person]
created: 2024-02-15
last-contact: 2025-02-20
next-step: "Discuss partnership opportunity next month"
---

Met Alex at Tech Summit in San Francisco. They're building data infrastructure at Meridian Labs. Strong product thinking, interested in our ecosystem play.

**Interaction Log:**
- [2025-02-20]: Coffee chat about partnership roadmap. Positive signals on the Q2 initiative.
- [2025-01-10]: Phone call — discussed mutual connections at Apex Studio
- [2024-12-05]: Initial conversation at conference afterparty
```

### Person — Jamie Park

File: `Shared/CRM/People/jamie-park.md`

```yaml
---
type: person
name: "Jamie Park"
company: "[[apex-studio]]"
role: Design Lead
source: warm-intro
relationship: advisor
tags: [crm/person]
created: 2024-06-10
last-contact: 2025-01-15
next-step: "Schedule quarterly design review"
---

Design advisor and trusted collaborator. Introduced by Sam Torres. Passionate about accessible design and systems thinking.

**Interaction Log:**
- [2025-01-15]: Design review session — feedback on component library
- [2024-11-20]: Monthly advisor check-in
```

### Company — Meridian Labs

File: `Shared/CRM/Companies/meridian-labs.md`

```yaml
---
type: company
name: "Meridian Labs"
industry: Data Infrastructure
tags: [crm/company]
created: 2024-02-15
---

Series B data infrastructure company. Strong technical team, building event streaming platform. Contact: [[alex-rivera]].
```

---

## Rules & Behaviors

- **Ask before creating:** Never add a contact without user confirmation
- **Frontmatter first:** Data lives in frontmatter, context lives in body
- **Wikilinks for relationships:** Link people to companies and related people
- **Dates as YYYY-MM-DD:** Consistent date format across all entries
- **Interaction log:** Keep dated entries in the body for relationship history
- **Next-step is critical:** Always set a next-step for follow-up actions
- **One file per person:** No duplicate entries, ever
- **Regular maintenance:** Schedule monthly CRM audits to surface stale relationships

---

## API-Enhanced Features

When Obsidian MCP is available:
- Search across all CRM entries
- Offer to open notes in the Obsidian app
- Support complex Dataview queries
- Integrate with Slack for contact cards

Graceful degradation when not available — all workflows work filesystem-only.
