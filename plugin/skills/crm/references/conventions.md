# CRM Naming & Frontmatter Conventions

## Naming Rules

**People:**
- Format: `firstname-lastname.md`
- All lowercase, kebab-case
- Examples:
  - `alex-rivera.md`
  - `jamie-park.md`
  - `sam-torres.md`

**Companies:**
- Format: `company-name.md`
- All lowercase, kebab-case
- Examples:
  - `meridian-labs.md`
  - `apex-studio.md`
  - `northlight-materials.md`

**Dataview Views:**
- Prefix with underscore: `_people-by-company.md`, `_needs-followup.md`

---

## Frontmatter Fields

### Person Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `person` |
| `name` | string | yes | Full name as they introduce themselves |
| `company` | wikilink | no | Link to company: `[[company-name]]` |
| `role` | string | no | Current job title |
| `source` | string | yes | How you met them |
| `relationship` | string | yes | Type of relationship |
| `tags` | array | yes | Must include `crm/person` |
| `created` | date | yes | When you added them (YYYY-MM-DD) |
| `last-contact` | date | no | Last meaningful interaction (YYYY-MM-DD) |
| `next-step` | string | no | Next action to maintain relationship |
| `expertise` | string | no | What they're expert in |
| `intro-path` | string | no | Who introduced you (if applicable) |

### Company Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `company` |
| `name` | string | yes | Company legal name |
| `industry` | string | no | Industry or sector |
| `tags` | array | yes | Must include `crm/company` |
| `created` | date | yes | When you added them (YYYY-MM-DD) |

---

## Source Values

How you know someone:

- `conference` — Met at a conference or event
- `warm-intro` — Introduced by mutual connection
- `cold-outreach` — Initiated contact directly
- `existing-network` — Long-standing relationship
- `online` — Met through internet (Twitter, LinkedIn, etc.)
- `advisor-intro` — Introduced by advisor
- `professional` — Through professional engagement

---

## Relationship Values

Type of relationship:

- `collaborator` — Active work together
- `advisor` — Trusted advisor or mentor
- `potential-customer` — Prospective customer
- `existing-customer` — Current customer
- `investor` — Investor or potential investor
- `friend` — Personal friend
- `vendor` — Service/product provider
- `partner` — Strategic partner
- `mentor` — Mentor/teacher
- `peer` — Professional peer
- `investor-network` — Part of investor network

---

## Example Entries

### Person Entry — Alex Rivera

**File:** `Shared/CRM/People/alex-rivera.md`

```yaml
---
type: person
name: "Alex Rivera"
company: "[[meridian-labs]]"
role: Product Manager
source: conference
relationship: collaborator
expertise: "data infrastructure, product strategy"
intro-path: null
tags: [crm/person]
created: 2024-02-15
last-contact: 2025-02-20
next-step: "Discuss partnership opportunity next month"
---

Met Alex at Tech Summit in San Francisco where they were speaking about data infrastructure patterns.

## Why They Matter
Strong product thinking. Interested in ecosystem partnership. Could be valuable collaborator on next-gen platform work.

## Interaction Log

- [2025-02-20]: Coffee chat about partnership roadmap. Positive signals on Q2 initiative. Wants to loop in their CTO.
- [2025-01-10]: Phone call — discussed mutual connections at Apex Studio
- [2024-12-05]: Initial conversation at conference afterparty

## Related
- [[meridian-labs]] (their company)
- [[sam-torres]] (mutual contact)
```

### Person Entry — Jamie Park

**File:** `Shared/CRM/People/jamie-park.md`

```yaml
---
type: person
name: "Jamie Park"
company: "[[apex-studio]]"
role: Design Lead
source: warm-intro
relationship: advisor
expertise: "systems design, accessibility, design ops"
intro-path: "[[sam-torres]]"
tags: [crm/person]
created: 2024-06-10
last-contact: 2025-01-15
next-step: "Schedule Q1 design review session"
---

Design advisor introduced by Sam Torres. Deep systems thinking and accessibility expertise. Monthly check-ins have been invaluable.

## Why They Matter
Trusted design advisor. Provides strategic guidance on component library and design ops maturity.

## Interaction Log

- [2025-01-15]: Design review session — feedback on v2 component library. Suggested new accessibility audit process.
- [2024-11-20]: Monthly advisor check-in — discussed design team scaling
- [2024-10-15]: Initial introduction call
```

### Person Entry — Sam Torres

**File:** `Shared/CRM/People/sam-torres.md`

```yaml
---
type: person
name: "Sam Torres"
company: "[[northlight-materials]]"
role: CEO
source: warm-intro
relationship: peer
expertise: "manufacturing, scaling, operations"
intro-path: null
tags: [crm/person]
created: 2024-08-22
last-contact: 2025-02-18
next-step: "Catch up on fundraising plans"
---

CEO at Northlight Materials. Met through industry network. Strong operations expertise and thinking.

## Why They Matter
Peer operator in adjacent space. Great source of perspective on scaling challenges.

## Interaction Log

- [2025-02-18]: Lunch — discussed Series B strategies and team building
- [2025-01-20]: Phone catch-up about market conditions
- [2024-12-10]: Introduction call
```

### Company Entry — Meridian Labs

**File:** `Shared/CRM/Companies/meridian-labs.md`

```yaml
---
type: company
name: "Meridian Labs"
industry: "Data Infrastructure"
tags: [crm/company]
created: 2024-02-15
---

Series B data infrastructure company. Building event streaming platform. Strong technical team, founder-led.

## Key People
- [[alex-rivera]] — Product Manager

## Contacts
- alex-rivera

## Strategic Relevance
Potential partnership opportunity on ecosystem integrations.
```

### Company Entry — Apex Studio

**File:** `Shared/CRM/Companies/apex-studio.md`

```yaml
---
type: company
name: "Apex Studio"
industry: "Design & Strategy"
tags: [crm/company]
created: 2024-06-10
---

Design and strategy consultancy. Known for systems thinking and accessibility-first approach.

## Key People
- [[jamie-park]] — Design Lead

## Contacts
- jamie-park

## Strategic Relevance
Design advisor support. Partnership potential for design system work.
```

### Company Entry — Northlight Materials

**File:** `Shared/CRM/Companies/northlight-materials.md`

```yaml
---
type: company
name: "Northlight Materials"
industry: "Advanced Materials"
tags: [crm/company]
created: 2024-08-22
---

Advanced materials manufacturing company. Focused on sustainable composites and industrial applications.

## Key People
- [[sam-torres]] — CEO

## Contacts
- sam-torres

## Strategic Relevance
Peer operator. Source of insights on scaling operations and team building in capital-intensive industries.
```

---

## Dataview Query Examples

### Find All People Needing Followup

```dataview
TABLE last-contact, next-step
FROM "Shared/CRM/People"
WHERE date(now) - date(last-contact) > dur(90 days)
SORT last-contact
```

### Show People by Company

```dataview
TABLE company, role, last-contact
FROM "Shared/CRM/People"
WHERE company
GROUP BY company
SORT company
```

### People by Relationship Type

```dataview
TABLE company, role, last-contact
FROM "Shared/CRM/People"
WHERE relationship = "collaborator"
SORT last-contact DESC
```

### Companies with Contact Info

```dataview
TABLE industry, created
FROM "Shared/CRM/Companies"
SORT created DESC
```

---

## Tips

- **Frontmatter carries the data:** All structured info goes in YAML
- **Body carries the context:** Use body for stories, interaction history, why they matter
- **Wikilinks for relationships:** Always link people to companies and related people
- **Dated interactions:** Keep a log in the body with `[YYYY-MM-DD]: Note` format
- **Next-step is critical:** Always set a clear next action
- **Monthly audits:** Run a CRM maintenance check monthly to surface stale contacts
