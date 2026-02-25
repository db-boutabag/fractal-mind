# Team Shared Vault Setup

Complete guide for setting up and maintaining a git-synced shared Obsidian vault for team collaboration.

---

## Prerequisites

Before starting, ensure you have:

- **Obsidian** installed (free, obsidian.md)
- **Git** installed (`git --version` to verify)
- **GitHub or GitLab access** to `<your-github-org>/<your-repo>` (shared vault repo)
- **Dataview plugin** installed in Obsidian (optional but recommended)
- **GitHub CLI** (`gh`) installed (optional, makes auth easier)
- **macOS, Linux, or Windows** with a terminal

---

## Step 1: Clone the Shared Vault Repository

The team maintains a git repository for the shared vault. You'll clone it into your personal Obsidian vault as the `Shared/` folder.

### 1.1 Navigate to Your Vault Directory

Open Terminal and go to your Obsidian vault root:

```bash
cd /path/to/your/vault
```

**Example:**
```bash
cd ~/Obsidian/MyVault
```

### 1.2 Clone the Shared Vault Repository

Clone the shared vault repo as the `Shared/` subfolder:

```bash
git clone https://github.com/<your-github-org>/<your-repo>.git Shared
```

**Example:**
```bash
git clone https://github.com/mycompany/shared-vault.git Shared
```

### 1.3 Verify the Clone

You should now have:
```
/path/to/your/vault/
├── Inbox/
├── Projects/
├── Shared/  ← Just cloned
│   ├── CRM/
│   ├── Brand/
│   ├── Strategy/
│   └── ...
└── ...
```

Verify the clone in Obsidian: open File Explorer in the left sidebar. You should see Shared/ as a folder with subfolders like CRM/, Brand/, etc.

---

## Step 2: Configure Shared Vault Sync

### 2.1 Auto-Sync with Git (macOS)

If you want automatic git syncing, set up a launchd script that runs every 5 minutes.

**Create the plist file:**

```bash
cat > ~/Library/LaunchAgents/com.yourcompany.shared-sync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourcompany.shared-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/your/vault/shared-vault-scripts/shared-sync.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>/var/tmp/shared-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/var/tmp/shared-sync.err</string>
</dict>
</plist>
EOF
```

**Customize the path:**

Replace `/path/to/your/vault/shared-vault-scripts/shared-sync.sh` with your actual vault path.

**Load the plist:**

```bash
launchctl load ~/Library/LaunchAgents/com.yourcompany.shared-sync.plist
```

**Verify:**

```bash
launchctl list | grep shared-sync
```

You should see `com.yourcompany.shared-sync` listed.

### 2.2 Manual Sync (All Platforms)

If you prefer manual syncing or use Windows/Linux, just run this command periodically:

```bash
cd /path/to/your/vault/Shared && git pull origin main && git push origin main
```

Or use a shell alias for convenience:

```bash
alias sync-vault='cd /path/to/your/vault/Shared && git pull && git push'
```

Then run `sync-vault` whenever you want to sync.

### 2.3 Auto-Sync with Git (Linux)

Create a cron job instead of launchd:

```bash
crontab -e
```

Add this line:

```cron
*/5 * * * * /path/to/your/vault/shared-vault-scripts/shared-sync.sh >> /tmp/shared-sync.log 2>&1
```

This runs the sync script every 5 minutes.

### 2.4 Auto-Sync with Git (Windows)

Use Windows Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task: "Shared Vault Sync"
3. Trigger: "Repeat every 5 minutes"
4. Action: `Start a program` → PowerShell script that runs the bash script

Or use WSL (Windows Subsystem for Linux) and follow the Linux instructions above.

---

## Step 3: Folder Guide

Understand what goes in each shared folder.

### CRM/

Shared relationship intelligence. One file per person, one per company.

**Subfolders:**
- `People/` — Individual contacts
- `Companies/` — Company/organization details
- `_views/` — Dataview dashboards (people by company, needs followup, etc.)

**When to add:** Anyone the team should know about. Collaborators, advisors, partners, customers.

**Frontmatter example:**
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
added-by: yourname
---
```

### Brand/

Brand identity and guidelines. Logos, colors, tone, positioning, content strategy.

**Typical files:**
- Brand guidelines
- Brand positioning statement
- Logo usage rules
- Tone and voice guide
- Content strategy

### Strategy/

High-level business strategy, positioning, business plan.

**Typical files:**
- Company mission/vision
- Quarterly business reviews
- Funding strategy and notes
- Market positioning
- Long-term roadmap

### Product/

Product specifications, features, UX decisions, testing notes.

**Typical files:**
- Product roadmap
- Feature specs
- UX decisions and rationale
- Testing notes
- Technical architecture

### Marketing/

Campaigns, outreach strategy, landing pages, user acquisition.

**Typical files:**
- Campaign plans
- User acquisition strategy
- Content calendar
- Launch checklists
- Analytics and performance notes

### Engineering/

Architecture, infrastructure, deployment, tech decisions.

**Typical files:**
- Architecture decisions
- Infrastructure notes
- Deployment procedures
- Tech debt tracking
- Build/release procedures

### Intel/

Competitive research, market landscape, industry trends.

**Typical files:**
- Competitive analysis
- Market research
- Pricing intelligence
- Trend analysis
- Industry news summaries

### Ops/

Operations, sprint plans, team cadence, processes.

**Typical files:**
- Sprint plans and retrospectives
- Team cadence documents
- Operational playbooks
- Process documentation
- Resource allocation

### Meeting-Notes/

Shared meeting notes, organized by audience:

```
Meeting-Notes/
├── Internal/    # Team syncs, standups, internal reviews
└── External/    # Calls with partners, customers, vendors
```

**Naming:** `YYYY-MM-DD-topic.md`

**Routing rule:**
- Internal team meetings → `Internal/`
- Calls with anyone outside the team → `External/`

**Frontmatter:**
```yaml
---
type: meeting
status: active
tags: [type/meeting]
created: 2025-02-25
added-by: yourname
---
```

### Docs/

Ad-hoc shared documents that don't fit in domain folders.

**Examples:**
- One-time decision docs
- RFP responses
- Grant applications
- Miscellaneous shared content

### Archive/

Completed or shelved shared work. Move items here when they're no longer active.

---

## Step 4: Frontmatter Conventions

Every shared file must have `added-by` in frontmatter to track who created it.

### Standard Template

```yaml
---
type: note
status: active
tags: [area/work]
created: 2025-02-25
added-by: yourname
---
```

### Extended Template (for richer notes)

```yaml
---
type: note
status: active
tags: [area/work, project/name]
created: 2025-02-25
added-by: yourname
next-step: "What's the next action?"
related: [[related-note]]
---
```

**Why `added-by`?**

Git history shows edits, but not original authorship. `added-by` makes it clear who created the file, useful for asking questions or giving credit.

---

## Step 5: Sharing Documents from Personal to Shared

If you create a note in your personal vault that should be shared:

1. **Move the file** to the appropriate Shared/ subfolder
2. **Add `added-by: yourname`** to frontmatter
3. **Update any wikilinks** that break (rare, but check)
4. **Commit to git**: The auto-sync will pick it up, or run manual sync
5. **Notify the team** if it's a significant addition

Example workflow:

```bash
# Create/edit in personal vault
# Then move to Shared/
mv ~/Obsidian/MyVault/Projects/Brand/brand-guidelines.md \
   ~/Obsidian/MyVault/Shared/Brand/brand-guidelines.md

# Edit frontmatter to add added-by: yourname
# Run sync
cd ~/Obsidian/MyVault/Shared && git add . && git commit -m "Add brand guidelines" && git push
```

---

## Step 6: Dataview Dashboards

The Shared/ folder may include Dataview queries for analytics. These are `.md` files that run DQL (Dataview Query Language).

**Example: People by Company**

```dataview
TABLE company, role, last-contact
FROM "Shared/CRM/People"
WHERE company
GROUP BY company
```

**To use:**

1. Install **Dataview plugin** in Obsidian if not already installed
2. Open a `.md` file with a dataview code block:
   ````
   ```dataview
   TABLE ...
   ```
   ````
3. The query will render automatically as a table

**Common queries for shared vault:**

- **People by company** — See all team contacts at each organization
- **Needs followup** — Contacts not contacted in 90+ days
- **By relationship type** — Collaborators, advisors, etc.
- **Active projects** — All shared projects in progress
- **Recent updates** — Files created/modified in the last week

---

## Step 7: Merge Conflicts

Conflicts happen when two people edit the same file simultaneously. Git prevents data loss by marking conflicts.

### Identifying a Conflict

When you pull and there's a conflict:

```
Auto-merging Shared/Brand/guidelines.md
CONFLICT (content): Merge conflict in Shared/Brand/guidelines.md
Automatic merge failed; fix conflicts and then commit the result.
```

### Resolving a Conflict

1. **Open the conflicted file** in your editor
2. **Look for conflict markers:**
   ```
   <<<<<<< HEAD
   Your version of the text
   =======
   Their version of the text
   >>>>>>> <branch-name>
   ```
3. **Choose which version to keep** (or combine both):
   - Keep yours: Delete their section (between `=======` and `>>>>>>>`)
   - Keep theirs: Delete your section (between `<<<<<<<` and `=======`)
   - Combine: Keep both, remove markers
4. **Remove all conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)
5. **Stage and commit:**
   ```bash
   cd /path/to/your/vault/Shared
   git add .
   git commit -m "Resolve merge conflict in guidelines.md"
   git push origin main
   ```

**Best practice:** Communicate with your teammate about what happened so you don't lose important information.

---

## Important Notes

### Don't Rename Shared/

The `Shared/` folder name is hard-coded in wikilinks throughout your personal vault. Renaming it breaks all links. Leave it as-is.

### Wikilink Behavior

Wikilinks work seamlessly across personal and shared content:
- Personal note → Shared note: ✓ Works great
- Shared note → Personal note: ✓ Works, but creates tight coupling (use sparingly)

Example:
```markdown
In personal vault: [[alex-rivera]] links to Shared/CRM/People/alex-rivera.md
In shared note: [[alex-rivera]] links to the same file
```

### Sync Frequency

- **Auto-sync every 5 minutes:** Changes are usually synced within 5 minutes
- **Check manually before important changes:** If you're about to make critical edits, run a manual sync first
- **Pull before big changes:** Always `git pull` before doing significant work to avoid conflicts

### Merge Conflict Prevention

- **Divide by area:** Each team member "owns" a domain folder (Brand, Product, etc.)
- **Communicate changes:** Let team members know if you're editing shared files
- **Small, frequent commits:** Avoid large changes to the same file simultaneously

---

## Troubleshooting

### "Permission denied" when cloning

You might not have GitHub access. Ask your team lead to add you to the repository.

```bash
# Verify access:
gh repo view <your-github-org>/<your-repo>
```

### Auto-sync not working

1. **Verify the plist is loaded:**
   ```bash
   launchctl list | grep shared-sync
   ```

2. **Check the log:**
   ```bash
   tail -f /var/tmp/shared-sync.log
   ```

3. **Reload the plist:**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.yourcompany.shared-sync.plist
   launchctl load ~/Library/LaunchAgents/com.yourcompany.shared-sync.plist
   ```

### Wikilinks show "unresolved"

This means Obsidian can't find the link target. Check:
- Is the file name spelled correctly?
- Is the file in Shared/? (wikilinks work across personal and shared)
- Run `Obsidian: Rebuild graph` from the command palette

### Files keep reverting to old versions

You might be experiencing sync conflicts. Try:

```bash
cd /path/to/your/vault/Shared
git status
```

If files show as modified but you didn't edit them, run:

```bash
git pull origin main --rebase
```

---

## Next Steps

1. **Verify clone:** Open Obsidian and confirm Shared/ appears in the file explorer
2. **Set up auto-sync:** Follow Step 2 for your operating system
3. **Read the README:** Open `Shared/README.md` for an overview
4. **Review domain folders:** Get familiar with what goes in each folder
5. **Add yourself to CRM:** Create a People entry so the team knows who you are
6. **Make a test edit:** Create a small file in a domain folder, sync, verify it appears for teammates

---

## Getting Help

- **Technical issues:** Ask your vault steward or team lead
- **Questions about content:** Check the relevant domain folder's README
- **Git questions:** See the troubleshooting section above or ask a teammate
- **Want to improve this guide?** Submit a PR to the repo!

---

## Optional: Git Mirror Sync

If you want to mirror specific personal vault files into Shared/ automatically, create a `mirror.conf` file:

```bash
# mirror.conf
# Format: /path/in/personal/vault /path/in/shared/vault

/path/to/your/vault/Areas/Company/quarterly-reviews.md Shared/Strategy/quarterly-reviews.md
```

Then the sync script will mirror these files automatically. Consult your vault steward for details.
