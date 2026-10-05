# Motion Studio

Seven agent skills for directing, designing, engineering, and reviewing code-rendered motion films. Built for Claude Code with Opus 5.5, with portable `SKILL.md` instructions that other compatible coding agents can also use.

Start from a clear brief and real assets. Develop the story and motion language, render deterministic frames, inspect the actual output, and repair specific defects before delivery.

## Skills

| Skill | Responsibility |
| --- | --- |
| [motion-studio](skills/motion-studio/SKILL.md) | Coordinate production, checkpoints, review gates, and delivery |
| [motion-director](skills/motion-director/SKILL.md) | Brief, concepts, reference analysis, and asset provenance |
| [motion-storyboard](skills/motion-storyboard/SKILL.md) | Narrative beats, states, styleframes, and format-specific layouts |
| [motion-design](skills/motion-design/SKILL.md) | Typography, hierarchy, easing, weight, and continuity |
| [motion-engineer](skills/motion-engineer/SKILL.md) | Seekable frame rendering, source code, and reproducible exports |
| [motion-audio](skills/motion-audio/SKILL.md) | Music, voice, effects, mix, and picture synchronization |
| [motion-review](skills/motion-review/SKILL.md) | Timestamped critique, contact sheets, local repairs, and final QC |

These are workflow roles. Installing the skills does not automatically launch seven agents or change the selected model.

## Install in Claude Code

Clone this repository, then run from its root:

```sh
git clone https://github.com/ptrgiang/motion-studio.git
cd motion-studio
python3 skills/motion-studio/scripts/export_claude.py --destination /absolute/path/to/your-video-project/.claude/skills
```

On Windows, use `python` if that is your Python command and quote paths containing spaces. For a personal installation, pass the full path to your user `.claude/skills` directory instead. The exporter refuses to overwrite existing members of this pack.

Alternatively, copy each complete folder under `skills/` into `.claude/skills/<skill-name>/`. Preserve its references, scripts, and assets. Do not add an extra container directory around the seven skills.

Select Opus 5.5 in your Claude Code session. Invoke:

```text
/motion-studio Create a 15-second English launch film for [product].
Audience: [audience]. Takeaway: [one sentence].
Formats: 16:9 and 9:16.
Use the real product assets in ./assets and inspect ./reference.mp4.
Work autonomously through documented review gates.
Deliver editable source, videos, poster frames, contact sheets,
asset provenance, and a note identifying any incomplete checks.
```

The main skill loads the specialist instructions as needed. Autonomous gates are internal checks; the agent asks for input when a material requirement is unresolved or when you requested a supervised approval.

## Production workflow

1. Establish the idea, product facts, reference, and approved assets.
2. Write the style guide and frame-based shot list; design each aspect ratio explicitly.
3. Build a deterministic composition and inspect representative stills.
4. Render a rough cut; inspect transition frames, watch the movement, and listen to audio.
5. Repair the three highest-impact observed defects and recheck affected sections.
6. Verify the requested formats and deliver the source alongside the exports.

Never invent product screens or metrics. Treat missing required assets as production blockers while continuing feasible planning. A contact sheet cannot establish temporal quality or audio quality, and a successful encode cannot establish artistic quality.

## Included tools

Under `skills/motion-studio/`:

- `scripts/studio.py`: initialize project records, validate the asset/timeline/layout structure, and select review frames.
- `scripts/contact_sheet.py`: generate labeled contact sheets from stills or exact decoded video frames.
- `scripts/export_claude.py`: export all seven skills into Claude Code's directory structure without overwriting existing skills.
- `assets/canvas-starter.html`: generic deterministic Canvas frame-function example.
- `assets/render.mjs`: Playwright capture script with within-runtime seek checks.

Example project initialization:

```sh
python3 skills/motion-studio/scripts/studio.py init /absolute/path/to/new-film
```

Read [the production contract](skills/motion-studio/references/production-contract.md) before filling the draft spec, and [the renderer recipe](skills/motion-studio/references/renderer-recipes.md) before running the starter. The generic sample artwork is a renderer test, not a finished client film.

## Requirements

Reading and planning require a compatible agent. Rendering additionally requires local execution tools:

| Component | Requirement |
| --- | --- |
| Project scripts | Python 3.9+ |
| Contact sheets | Pillow |
| Video extraction and encoding | FFmpeg and ffprobe on PATH |
| Canvas capture | Recent Node.js, project-installed Playwright, and its Chromium browser |
| Optional React video stack | Remotion, with matching pinned package versions |

Dependencies and browser binaries are not bundled. Pin the actual installed versions and preserve the production project's lockfile. The skills do not include model API credentials or force a paid API workflow.

## Validation status

Passed: seven skill format checks, structural validator checks, export and overwrite refusal, still/video contact-sheet generation, and an independent missing-input pre-production exercise.

The Canvas frame function passed a mocked drawing-operation test. **Real Chromium capture and the complete Playwright-to-video pipeline have not been verified**: Chromium was unavailable and its download failed in the authoring environment. FFmpeg testing used a separate fixture, not the Canvas renderer. No actual Opus production session, client film, audio listening review, or professional artistic equivalence has been certified.

See [the exact validation scope](skills/motion-studio/references/validation-status.md). Re-run the actual render and perceptual checks in your production environment before treating an output as final.

## Source and adaptation

Inspired by the supplied article *Motion Engineering: Build a Video Studio Around Opus 5.5*, attributed to `@0xwhrrari`, and its studio diagram. This repository contains an authored workflow adaptation rather than a reproduction of the article. Added policies include explicit role responsibilities, a frame-based production contract, asset checks, bounded repairs, and evidence requirements.

See [source mapping and primary documentation](skills/motion-studio/references/sources.md).
