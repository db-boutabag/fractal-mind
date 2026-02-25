# Setup Guide

Complete instructions for setting up fractal-mind with Obsidian and optional MCP connections.

## Prerequisites

- **Obsidian** (free version is fine) — [Download](https://obsidian.md)
- **Claude Code** — Requires Anthropic API access
- **Git** (for shared vault collaboration, optional)

## Step 1: Vault Directory Setup

Create your vault directory and initialize the structure:

```bash
# Create vault directory
mkdir -p ~/Obsidian/Vault

# (Or use existing vault)
cd ~/Obsidian/Vault
```

Or copy the contents of the `vault-template/` folder from the fractal-mind repo into your vault.

## Step 2: Copy the fractal-mind Plugin

Copy the plugin from the repository into your vault:

```bash
cp -r plugin/ ~/Obsidian/Vault/.local-plugins/fractal-mind/1.0.0/
```

Your structure should look like:
```
~/Obsidian/Vault/
├── .local-plugins/
│   └── fractal-mind/
│       └── 1.0.0/
│           ├── skills/
│           ├── commands/
│           └── CONNECTORS.md
├── Inbox/
├── Projects/
├── Areas/
├── Daily/
├── Templates/
├── Meta/
└── ... (other vault structure)
```

## Step 3: Update Vault Configuration

Edit your vault's `Meta/CLAUDE.md` to customize for your vault:

```markdown
# Vault Constitution

## Owner
[Your Name]

## Structure
[Verify the PARA structure matches your setup]

## Preferences
[Adjust based on your workflow]
```

Also review `Meta/TAGS.md` and add any custom tags you want to use.

## Step 4: (Optional) Set Up External Connectors

For full setup instructions on all external tool integrations (Obsidian REST API, ClickUp, Slack, Google Workspace, HubSpot), see `CONNECTORS.md` in the plugin root.

The sections below cover the most common integrations inline.

## Step 5: (Optional) Set Up Obsidian REST API for MCP

The Obsidian REST API community plugin enables API-enhanced features like indexed search, live queries, and app integration.

### Install the Plugin

1. Open Obsidian
2. Go to **Settings → Community Plugins → Browse**
3. Search for "Obsidian REST API"
4. Install and enable the plugin

### Configure MCP

Create a `.mcp.json` file in your vault root (or use `.mcp.json.example` as a template):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "$OBSIDIAN_API_KEY",
        "OBSIDIAN_VAULT_DIR": "/path/to/your/vault"
      }
    }
  }
}
```

### Generate API Key

1. In Obsidian, open **Obsidian REST API** plugin settings
2. Generate a new API key
3. Store it in your environment:

```bash
# Add to ~/.zshrc or ~/.bashrc (don't commit to git)
export OBSIDIAN_API_KEY="your-key-here"
```

### Verify Connection

Test in Claude Code:
```
/obsidian show me all active projects
```

If the obsidian MCP server is available, you should get a fast, indexed response.

## Step 6: (Optional) Set Up Google Workspace MCP for Meeting Import

The Google Workspace MCP enables pulling Google Meet auto-generated notes into your vault.

### Install and Configure

```bash
# Will be installed via uvx when needed
# Configure MCP:
```

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tools", "drive", "docs", "--read-only"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "$GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET": "$GOOGLE_OAUTH_CLIENT_SECRET"
      }
    }
  }
}
```

### Set Up OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Drive and Google Docs APIs
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials JSON
6. Set environment variables:

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
```

### Complete OAuth Flow

When you first run `/meeting-import`, you'll be prompted to complete the OAuth consent flow in your browser. This gives fractal-mind read-only access to your Google Drive.

Once complete, meeting notes will be imported automatically.

## Step 7: (Optional) Set Up ClickUp MCP for Task Management

For bidirectional syncing between vault notes and ClickUp tasks:

```json
{
  "mcpServers": {
    "clickup": {
      "command": "uvx",
      "args": ["mcp-clickup"],
      "env": {
        "CLICKUP_API_KEY": "$CLICKUP_API_KEY"
      }
    }
  }
}
```

Generate a ClickUp API key in ClickUp Settings → Apps → API, then:

```bash
export CLICKUP_API_KEY="your-key"
```

## Step 8: (Optional) Set Up Slack MCP for Thread Capture

For capturing Slack threads into vault notes:

```json
{
  "mcpServers": {
    "slack": {
      "command": "uvx",
      "args": ["mcp-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "$SLACK_BOT_TOKEN",
        "SLACK_SIGNING_SECRET": "$SLACK_SIGNING_SECRET"
      }
    }
  }
}
```

Create a Slack app, generate tokens, then:

```bash
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_SIGNING_SECRET="your-secret"
```

## Step 9: (Optional) Set Up Shared Vault for Team Collaboration

To enable git-synced team collaboration:

```bash
# Create Shared folder as git repo
mkdir -p ~/Obsidian/Vault/Shared
cd ~/Obsidian/Vault/Shared
git init

# Or clone existing shared vault
git clone https://github.com/<your-org>/obsidian-shared.git Shared
```

Configure auto-sync with `shared-vault-scripts/shared-sync.sh`:

```bash
# Edit the script to set your SHARED_DIR path
./shared-sync.sh --dry-run  # Test first

# Add to launchd (macOS) for automatic syncing
# See shared-vault-scripts/shared-sync.sh for full instructions
```

See `docs/shared-vault-architecture.md` for detailed team setup.

## Step 10: (Optional) Enable Git Backup

Back up your personal vault to Git (exclude secrets):

```bash
cd ~/Obsidian/Vault

# Initialize git repo (if not already)
git init

# Create .gitignore
cat > .gitignore << EOF
.mcp.json
*.secret
*.key
.env
.DS_Store
Meta/memory/
node_modules/
.obsidian/workspace
.obsidian/plugins/
EOF

# Initial commit
git add .
git commit -m "Initial vault setup"

# Add remote and push
git remote add origin https://github.com/<your-org>/obsidian-vault.git
git push -u origin main
```

Then periodically:
```bash
cd ~/Obsidian/Vault
git add -A
git commit -m "Daily backup: $(date +%Y-%m-%d)"
git push
```

Or use `shared-vault-scripts/shared-sync.sh` adapted for personal vault.

## Step 11: Test Your Setup

1. Open Claude Code in your vault:
```bash
cd ~/Obsidian/Vault
claude-code
```

2. Test the `/obsidian` skill:
```
/obsidian hello, I just had a thought about improving our meeting notes process
```

3. Check that:
   - A note was created in Inbox/
   - It has proper frontmatter
   - The skill read your CLAUDE.md and TAGS.md

4. If MCP is set up, test:
```
/obsidian show me all active projects
```

Should return indexed results if Obsidian MCP is available.

## Customization

### Add Custom Domain Folders

Edit your vault structure by updating `CLAUDE.md` and creating new domains under `Shared/`:

```bash
mkdir -p ~/Obsidian/Vault/Shared/custom-domain
```

Then update CLAUDE.md to reflect the new structure.

### Modify Templates

Copy the template files to your Templates/ folder and customize:

```bash
cp -r vault-template/Templates/* ~/Obsidian/Vault/Templates/
```

Edit them to match your workflow.

### Extend Skills

Skills are in `.local-plugins/fractal-mind/1.0.0/skills/`. You can:
- Create new skills (e.g., `planning/`, `research/`)
- Add new commands (e.g., `project-launch.md`)
- Modify existing workflows

Tell Claude Code about changes via the `/obsidian` skill.

## Troubleshooting

**"$VAULT not recognized"**
- Update your commands to use your actual vault path
- Or set `VAULT=/path/to/your/vault` in your environment

**Obsidian MCP not working**
- Verify the REST API plugin is installed and enabled in Obsidian
- Check that `OBSIDIAN_API_KEY` environment variable is set
- Confirm vault directory in `.mcp.json` matches your vault path
- Restart Claude Code

**Google Meet import not working**
- Verify Google Workspace MCP is installed (`uvx workspace-mcp --help`)
- Check OAuth credentials are set and valid
- Complete the OAuth flow if prompted
- Verify Google Drive folder ID is correct in `google-meet-integration.md`

**Shared vault sync failing**
- Ensure git is installed and you have GitHub access
- Check that you have write permissions to the shared repo
- Review merge conflicts using git tools
- Restart the sync daemon

## Next Steps

1. **Start capturing:** Use `/obsidian` to capture your first thoughts
2. **Process inbox:** Run "Process inbox" weekly to stay organized
3. **Create periodic notes:** Set up daily and weekly review notes
4. **Build your CRM:** Use `/crm` to track important relationships
5. **Set up team collaboration:** If working with others, enable shared vault

## More Resources

- **Vault Conventions:** `references/conventions.md`
- **Dataview Queries:** `references/obsidian-plugins/dataview.md`
- **ClickUp Sync:** `references/obsidian-plugins/clickup-integration.md`
- **Google Meet Import:** `references/google-meet-integration.md`
- **Shared Vault Architecture:** `docs/shared-vault-architecture.md`
- **MCP Guide:** `CONNECTORS.md`
