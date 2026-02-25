#!/usr/bin/env python3
"""
fractal-mind vault initialization script.

Creates the full PARA folder structure with domain subfolders, Daily/, Templates/,
and Meta/ directories. Populates templates and vault constitution files.

Default vault path: ~/Obsidian/Vault
Custom path: pass as --vault-path argument
Optional shared vault setup: pass --shared flag
"""

import argparse
import os
import sys
from pathlib import Path


def create_directory_structure(vault_path, create_shared=False):
    """Create the complete vault directory structure."""
    vault = Path(vault_path)
    vault.mkdir(parents=True, exist_ok=True)

    # PARA structure
    para_folders = ["Inbox", "Projects", "Areas", "Resources", "Archive"]
    for folder in para_folders:
        (vault / folder).mkdir(exist_ok=True)

    # Daily, Templates, Meta
    (vault / "Daily").mkdir(exist_ok=True)
    (vault / "Templates").mkdir(exist_ok=True)
    (vault / "Meta").mkdir(exist_ok=True)

    # Optional Shared/ structure
    if create_shared:
        shared_domains = [
            "CRM",
            "Brand",
            "Strategy",
            "Product",
            "Marketing",
            "Engineering",
            "Ops",
            "Intel",
            "Docs",
            "Archive",
        ]
        for domain in shared_domains:
            (vault / "Shared" / domain).mkdir(parents=True, exist_ok=True)
        # Meeting-Notes with Internal/External subfolders
        (vault / "Shared" / "Meeting-Notes" / "Internal").mkdir(parents=True, exist_ok=True)
        (vault / "Shared" / "Meeting-Notes" / "External").mkdir(parents=True, exist_ok=True)

    return vault


def write_claude_md(vault_path):
    """Write vault constitution file."""
    content = """# Vault Constitution

## Owner
{{Your Name}}

## Structure
- PARA folders: Inbox/, Projects/, Areas/, Resources/, Archive/
- Projects/ is for personal non-work projects only
- Shared/ — All work content, git-synced team folder (optional)
- Daily notes in Daily/
- Templates in Templates/
- Meta files in Meta/

## Rules
- Date format: YYYY-MM-DD
- File names: lowercase-kebab-case
- Every note must have frontmatter with at minimum: type, status, tags, created
- One idea per note when possible
- Always add next-step for actionable items
- Use [[wikilinks]] for connections
- Tags use nested hierarchy: #area/work, #project/name, #status/active
- When unsure where a note goes, put it in Inbox/
- Shared vault files require added-by in frontmatter to track contributions

## Tag Reference
See Meta/TAGS.md for the full tag list.

## Preferences
- Bias toward action over asking questions
- Keep notes concise — expand later if needed
- Surface stuck items and next-steps prominently
"""
    (Path(vault_path) / "Meta" / "CLAUDE.md").write_text(content)


def write_tags_md(vault_path):
    """Write tag reference file."""
    content = """# Tag Reference

## Status (mutually exclusive)
- #status/inbox — unprocessed
- #status/active — currently working on
- #status/stuck — blocked, needs help
- #status/waiting — depends on someone/something external
- #status/done — completed
- #status/archived — no longer relevant

## Areas
- #area/work
- #area/growth
- #area/health

## Types
- #type/meeting
- #type/decision
- #type/reference
- #type/daily
- #type/weekly-review

## Projects
Add new project tags as projects are created:
- #project/<project-name>

## CRM
- #crm/person
- #crm/company
"""
    (Path(vault_path) / "Meta" / "TAGS.md").write_text(content)


def write_daily_template(vault_path):
    """Write daily note template."""
    content = """---
type: journal
status: active
tags: [type/daily]
created: {{date:YYYY-MM-DD}}
---

# {{date:dddd, MMMM DD, YYYY}}

## Focus Today
-

## Captures
-

## Done Today
-

## Reflections
-
"""
    (Path(vault_path) / "Templates" / "daily.md").write_text(content)


def write_meeting_template(vault_path):
    """Write meeting note template."""
    content = """---
type: meeting
status: active
tags: [type/meeting]
created: {{date:YYYY-MM-DD}}
---

# {{title}}

## Attendees
-

## Agenda
-

## Notes
-

## Action Items
-
"""
    (Path(vault_path) / "Templates" / "meeting.md").write_text(content)


def write_note_template(vault_path):
    """Write standard note template."""
    content = """---
type: note
status: inbox
tags: []
created: {{date:YYYY-MM-DD}}
---

# {{title}}

"""
    (Path(vault_path) / "Templates" / "note.md").write_text(content)


def write_project_template(vault_path):
    """Write project template."""
    content = """---
type: project
status: active
tags: [type/project]
created: {{date:YYYY-MM-DD}}
---

# {{title}}

## Objective
-

## Key Results
-

## Open Questions
-

## Log
-
"""
    (Path(vault_path) / "Templates" / "project.md").write_text(content)


def write_weekly_review_template(vault_path):
    """Write weekly review template."""
    content = """---
type: journal
status: active
tags: [type/weekly-review]
created: {{date:YYYY-MM-DD}}
---

# Week Review — {{date:YYYY-[W]ww}}

## Accomplishments
-

## Open Threads
-

## Stuck/Blocked
-

## Patterns Noticed
-

## Next Week Priorities
-
"""
    (Path(vault_path) / "Templates" / "weekly-review.md").write_text(content)


def main():
    parser = argparse.ArgumentParser(
        description="Initialize fractal-mind vault structure and templates"
    )
    parser.add_argument(
        "--vault-path",
        type=str,
        default=os.path.expanduser("~/Obsidian/Vault"),
        help="Path to vault root (default: ~/Obsidian/Vault)",
    )
    parser.add_argument(
        "--shared",
        action="store_true",
        help="Create optional Shared/ structure for team collaboration",
    )

    args = parser.parse_args()

    try:
        # Create directory structure
        vault = create_directory_structure(args.vault_path, args.shared)
        print(f"✓ Created vault structure at: {vault}")

        # Write template files
        write_claude_md(args.vault_path)
        print("✓ Created Meta/CLAUDE.md")

        write_tags_md(args.vault_path)
        print("✓ Created Meta/TAGS.md")

        write_daily_template(args.vault_path)
        print("✓ Created Templates/daily.md")

        write_meeting_template(args.vault_path)
        print("✓ Created Templates/meeting.md")

        write_note_template(args.vault_path)
        print("✓ Created Templates/note.md")

        write_project_template(args.vault_path)
        print("✓ Created Templates/project.md")

        write_weekly_review_template(args.vault_path)
        print("✓ Created Templates/weekly-review.md")

        if args.shared:
            print("✓ Created Shared/ structure")

        print(f"\nVault initialized successfully at: {vault}")
        print("\nNext steps:")
        print("1. Open your vault in Obsidian")
        print("2. Customize Meta/CLAUDE.md with your vault's constitution")
        print("3. Review Meta/TAGS.md and add custom tags as needed")
        print("4. Start capturing notes in Inbox/")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
