# Claude Code setup

## Compatibility
Use standard SKILL.md frontmatter with name and description, plus local references/scripts/assets. The skills contain no proprietary host-only tool calls and no hardcoded Claude API credentials. agents/openai.yaml is optional UI metadata that Claude Code does not need. The skills require a coding environment capable of local execution for rendering; a text-only chat can plan but cannot honestly claim rendered/inspected film output.

## Export
Run `python3 <motion-studio-dir>/scripts/export_claude.py --destination /path/to/video-project/.claude/skills` from the personal-skills checkout environment. The script resolves siblings by frontmatter names, so reconciled folder names do not matter. It refuses missing members and blind overwrites. For a manifest-managed installation, --update --dry-run shows changes and --update creates a backup while protecting local edits; old unmanaged installations require a preserved manual migration. Transfer these seven exported directories to the user's project when their machine is different; exporting here does not install files on their computer.
Alternatively copy each entire skill directory under `.claude/skills/<frontmatter-name>/` (project) or `~/.claude/skills/<frontmatter-name>/` (personal). Preserve scripts, assets and references. Do not place all seven beneath an extra container level. Never overwrite existing CLAUDE.md or settings.

## Invoke
Select Opus 5.5 using the actual model picker in Claude Code; the skill cannot force a model, plan tier or API permission. Invoke `/motion-studio` and give product/audience, one takeaway, duration, formats, assets and reference. Examples:
- `/motion-studio Make a 15-second English launch film in 16:9 and 9:16 using ./assets real UI and ./reference.mp4. Work autonomously through documented review gates. Deliver source, contact sheets, poster and verified videos.`
- `/motion-review Review this cut; report timestamped evidence and fix the three largest defects.`

## Environment
For bundled Canvas starter: recent Node.js, Python 3, FFmpeg/ffprobe, Pillow, project-installed Playwright plus its Chromium browser. Pin actual package/browser versions and lockfile; do not imply these are bundled. Remotion is an optional alternate stack, not a mandatory dependency. Windows users can run commands in PowerShell with quoted paths or a WSL project; verify FFmpeg is on PATH.

Primary docs: https://code.claude.com/docs/en/skills (checked 2026-10-05). Re-check current installation/model behavior if it changes.

## v1.1 runtime
Pillow pipeline: Python 3.10+, Pillow, FFmpeg and ffprobe. Canvas adds Node.js, pinned Playwright 1.62.1 and Chromium. Run doctor.py for availability; it never downloads dependencies. Use pipeline.py demo then run to exercise both ratios with original audio. For a real brief, replace the sample composition and validate assets before rendering.
