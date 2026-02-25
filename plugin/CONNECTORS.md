# External Tool Connectors

This guide covers setting up integrations between fractal-mind and external tools via MCP (Model Context Protocol). All integrations are optional — the plugin works standalone with filesystem-only access.

## Overview

The fractal-mind plugin can enhance its capabilities by connecting to external tools:

- **Obsidian REST API** — Vault search and live read/write (unlocks indexed search)
- **ClickUp** — Task management with bidirectional sync
- **Slack** — Thread capture and search
- **Google Workspace** — Google Meet note auto-import (requires OAuth)
- **HubSpot** — CRM bridge for syncing relationships to external CRM

All integrations use environment variables for API keys. Never commit real credentials to your repo.

## Setup: Environment Variables

Create a `.env` file in your vault root (it's in `.gitignore`):

```bash
# .env (DO NOT COMMIT THIS FILE)

# Obsidian REST API
export OBSIDIAN_API_KEY="your-api-key-here"

# Google Workspace OAuth
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"

# ClickUp
export CLICKUP_API_KEY="your-api-key"

# Slack
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-signing-secret"

# HubSpot
export HUBSPOT_PRIVATE_APP_TOKEN="your-token"
```

Then load these in your Claude Code session:

```bash
source /path/to/your/vault/.env
claude code
```

Or, if using `.mcp.json`, the variables are loaded automatically (see below).

## 1. Obsidian REST API

Enables indexed search and live read/write access to your vault. Powers the Query workflow and makes Dataview queries much faster.

### Setup

1. **Install the plugin in Obsidian:**
   - Open Obsidian > Settings > Community Plugins
   - Search for "REST API"
   - Install and enable the plugin

2. **Get your API key:**
   - In Obsidian Settings > REST API, copy the API key
   - Save it: `export OBSIDIAN_API_KEY="<your-key>"`

3. **Configure MCP:**
   - Copy the example config: `cp plugin/.mcp.json.example /path/to/your/vault/.mcp.json`
   - Edit `.mcp.json` and set `OBSIDIAN_API_KEY` to your key (or use the environment variable)
   - Verify `.mcp.json` is in `.gitignore`

### Capabilities Unlocked

- Indexed full-text search (much faster than filesystem walk)
- Dataview query execution
- Live note access (read/write with Obsidian app sync)
- Embedding live query results in notes

### Example Usage

With Obsidian MCP enabled:

```
/obsidian

Query: "What am I stuck on?"
→ Claude searches your vault via REST API and returns results with backlinks
```

---

## 2. ClickUp

Connect to your ClickUp workspace for bidirectional task sync. Create tasks from vault notes, log activity, and bring task updates back into Obsidian.

### Setup

1. **Get your API key:**
   - In ClickUp > Settings > Apps > API, create a personal API token
   - Copy the token: `export CLICKUP_API_KEY="<token>"`

2. **Configure MCP:**
   - Add to `.mcp.json`:
   ```json
   "clickup": {
     "command": "uvx",
     "args": ["mcp-clickup"],
     "env": {
       "CLICKUP_API_KEY": "$CLICKUP_API_KEY"
     }
   }
   ```

3. **Link notes to ClickUp tasks:**
   - In your note frontmatter, add: `clickup: https://app.clickup.com/t/<TASK_ID>`
   - Claude can then read task details, update status, log time

### Conventions

Use the `clickup` frontmatter field to link notes to tasks:

```yaml
---
type: task
status: active
clickup: https://app.clickup.com/t/YOUR_TASK_ID
tags: [#project/marketing]
created: 2025-02-25
---
```

When you capture an actionable item, Claude can propose creating a ClickUp task. After confirmation, it links the note.

### Capabilities Unlocked

- View task details (status, assignee, due date, description)
- Update task status and add comments from Obsidian
- Log time to tasks from notes
- Query: "Show me tasks due this week"
- Bidirectional sync (update in ClickUp → read in Obsidian, update in Obsidian → push to ClickUp)

---

## 3. Slack

Capture Slack threads and bring important conversations into your vault. Link threads to Obsidian notes for continuity.

### Setup

1. **Create a Slack App:**
   - Go to https://api.slack.com/apps
   - Create a new app, choose "From scratch"
   - Name it (e.g., "fractal-mind-capture")

2. **Get credentials:**
   - In your app settings, go to Basic Information and copy:
     - Bot Token (starts with `xoxb-`): `export SLACK_BOT_TOKEN="<token>"`
     - Signing Secret: `export SLACK_SIGNING_SECRET="<secret>"`

3. **Configure MCP:**
   - Add to `.mcp.json`:
   ```json
   "slack": {
     "command": "uvx",
     "args": ["mcp-slack"],
     "env": {
       "SLACK_BOT_TOKEN": "$SLACK_BOT_TOKEN",
       "SLACK_SIGNING_SECRET": "$SLACK_SIGNING_SECRET"
     }
   }
   ```

4. **Set permissions:**
   - Go to OAuth & Permissions > Scopes
   - Add: `channels:history`, `channels:read`, `users:read`, `chat:write`
   - Install the app to your workspace

### Capabilities Unlocked

- Search Slack conversations by keyword
- Import a thread as a note in your vault
- Link Slack conversations to notes for context
- Capture important decisions/discussions before they're lost in the stream

---

## 4. Google Workspace

Auto-import Google Meet notes from Google Drive. Works with the Meeting Import workflow (`/meeting-import`).

### Setup

1. **Install Google Workspace MCP:**
   ```bash
   uvx workspace-mcp --tools drive docs --read-only
   ```

2. **Configure OAuth:**
   - First run will open a browser for OAuth consent
   - You'll authorize Claude to access Google Drive and Docs
   - Credentials are cached locally

3. **Get OAuth credentials (optional, for automated setup):**
   - Go to Google Cloud Console
   - Create a new project
   - Enable Drive and Docs APIs
   - Create OAuth 2.0 credentials (Desktop app)
   - Copy Client ID and Secret:
     - `export GOOGLE_OAUTH_CLIENT_ID="<id>"`
     - `export GOOGLE_OAUTH_CLIENT_SECRET="<secret>"`

4. **Configure in .mcp.json:**
   ```json
   "google-workspace": {
     "command": "uvx",
     "args": ["workspace-mcp", "--tools", "drive", "docs", "--read-only"],
     "env": {
       "GOOGLE_OAUTH_CLIENT_ID": "$GOOGLE_OAUTH_CLIENT_ID",
       "GOOGLE_OAUTH_CLIENT_SECRET": "$GOOGLE_OAUTH_CLIENT_SECRET"
     }
   }
   ```

5. **Set up a Google Drive folder for meeting notes:**
   - Create a folder in your Google Drive (e.g., "Meeting Notes")
   - Share the folder ID with fractal-mind (see Meeting Import workflow)

### Capabilities Unlocked

- Auto-import Google Meet auto-generated notes from Drive
- Two-phase process: import (pull new notes) and process (review and add context)
- CRM entries proposed from meeting transcripts
- Action items extracted and linked to tasks

### Important: OAuth Flow

Google Workspace MCP uses OAuth for authentication. On first run:

1. Claude will open your browser to Google's consent screen
2. Click "Allow" to authorize Claude to access Drive/Docs
3. The token is cached locally (see `~/.cache/` or similar)
4. No need to re-authorize on subsequent runs

**Never commit OAuth tokens or credentials to your repo.**

---

## 5. HubSpot

Sync relationship intelligence from your vault to HubSpot (or vice versa). Useful if your team uses HubSpot as your single source of truth for CRM.

### Setup

1. **Get your HubSpot API key:**
   - In HubSpot > Settings > Integrations > Private Apps
   - Create a new private app
   - Grant scopes: `crm.objects.contacts.read`, `crm.objects.contacts.write`, `crm.objects.companies.read`, `crm.objects.companies.write`
   - Copy the token: `export HUBSPOT_PRIVATE_APP_TOKEN="<token>"`

2. **Configure MCP:**
   - Add to `.mcp.json`:
   ```json
   "hubspot": {
     "command": "uvx",
     "args": ["mcp-hubspot"],
     "env": {
       "HUBSPOT__PRIVATE_APP_TOKEN": "$HUBSPOT_PRIVATE_APP_TOKEN"
     }
   }
   ```

3. **Link vault CRM to HubSpot:**
   - In your person/company frontmatter, add HubSpot contact ID:
   ```yaml
   hubspot-contact-id: "1234567890"
   ```

### Capabilities Unlocked

- Query: "Show me all contacts from Meridian Labs in HubSpot"
- Sync: Update a contact in vault, push changes to HubSpot
- Propose: When adding a new contact, check HubSpot first to avoid duplicates
- Bridge: Keep vault CRM in sync with HubSpot as single source of truth

---

## .mcp.json Configuration

The example `.mcp.json` includes Obsidian and Google Workspace. Add other connectors as needed:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "$OBSIDIAN_API_KEY"
      }
    },
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tools", "drive", "docs", "--read-only"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "$GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET": "$GOOGLE_OAUTH_CLIENT_SECRET"
      }
    },
    "clickup": {
      "command": "uvx",
      "args": ["mcp-clickup"],
      "env": {
        "CLICKUP_API_KEY": "$CLICKUP_API_KEY"
      }
    },
    "slack": {
      "command": "uvx",
      "args": ["mcp-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "$SLACK_BOT_TOKEN",
        "SLACK_SIGNING_SECRET": "$SLACK_SIGNING_SECRET"
      }
    },
    "hubspot": {
      "command": "uvx",
      "args": ["mcp-hubspot"],
      "env": {
        "HUBSPOT_PRIVATE_APP_TOKEN": "$HUBSPOT_PRIVATE_APP_TOKEN"
      }
    }
  }
}
```

Load environment variables before launching Claude Code:

```bash
source /path/to/your/vault/.env
claude code
```

Claude will automatically load all MCP servers from `.mcp.json`.

---

## Graceful Degradation

If an MCP server isn't available or fails to connect:

- Obsidian REST API missing → Claude falls back to filesystem walk (slower, but functional)
- ClickUp missing → `/obsidian` still works; task creation is just manual
- Google Workspace missing → Meeting import unavailable; user is informed clearly
- Other tools missing → Feature gracefully disabled with explanation

The plugin never requires any external tool. It's designed to enhance, not depend.

---

## Security Best Practices

1. **Never commit `.mcp.json` or `.env`** — Both are in `.gitignore` by default
2. **Use environment variables** — Don't hardcode credentials anywhere
3. **Rotate keys regularly** — Treat API keys like passwords
4. **Use read-only access when possible** — Google Workspace example uses `--read-only`
5. **Scope permissions narrowly** — Only grant the scopes each tool needs
6. **Monitor API usage** — Watch for unexpected activity on your accounts

---

## Troubleshooting

### "MCP server not found" or "Command failed"

- Verify the MCP package is installed: `uvx <mcp-package-name> --help`
- Check that your `.mcp.json` syntax is valid (use a JSON linter)
- Ensure environment variables are set: `echo $OBSIDIAN_API_KEY`

### OAuth fails on Google Workspace

- Delete cached credentials: `rm -rf ~/.cache/` (or equivalent on your OS)
- Re-run the workflow and complete the OAuth flow again
- Check that Google Cloud app has Drive and Docs APIs enabled

### "Permission denied" errors

- Verify API token/key is correct
- Check that the token has appropriate scopes/permissions
- Regenerate the token if unsure

### Obsidian REST API not responding

- Verify the plugin is running in Obsidian (should show green status in settings)
- Check that Obsidian is running and vault is open
- Verify API key matches the one in the plugin settings

---

## What's Next

1. Start with **Obsidian REST API** — it unlocks the most useful features
2. Add **Google Workspace** if you use Google Meet for meetings
3. Connect **ClickUp** if you want bidirectional task sync
4. Connect **HubSpot** or **Slack** as needed
5. Check the skill documentation for workflow-specific guidance

For detailed workflow instructions, see:
- `plugin/skills/obsidian/SKILL.md` — Core vault workflows
- `plugin/skills/crm/SKILL.md` — Relationship intelligence
- `plugin/skills/obsidian/references/google-meet-integration.md` — Meeting import deep dive
