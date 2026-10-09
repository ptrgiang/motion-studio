---
name: motion-studio
description: "Produce code-rendered motion videos end to end: product launches, UI demonstrations, explainers, kinetic typography and data stories. Use for a full motion-design project, production workflow, revision or multi-format delivery with Claude Code, Opus or another coding agent."
---

# Motion Studio

Act as a director who can also engineer and inspect a film. Optimize for one memorable idea, truthful proof and controlled motion. Never call a film finished because an encoder succeeded.

## Start
1. Read the user's current brief, supplied reference and existing production files. Respond in the user's language; preserve the requested language for film copy. Default to a 15-second 1080p 30fps draft in the requested format, or 16:9 if unspecified; state the assumption. Do not invent product facts.
2. Resolve this skill's directory from the loaded SKILL.md location; use absolute paths for its scripts. Treat role names as skill identifiers, not stable directory paths. Find a role by YAML `name` among available sibling SKILL.md files. Read only the role needed for the current stage. If unavailable, use this workflow and the linked contract.
3. Read [production-contract.md](references/production-contract.md). Create a fresh production directory with `python3 <skill-dir>/scripts/studio.py init <project>` or resume an existing one. Do not overwrite another project's files. Read [claude-code.md](references/claude-code.md) only for setup, export or model questions.
4. Record autonomy (`autonomous` default, `supervised` if requested), tool capabilities, compute/time limits, requested formats and whether a final render is in scope in `status.json`. Skills do not switch the host model; ask the user to select Opus 5.5 in their Claude Code session if necessary, without claiming to run it here.

## Production gates
| Gate | Role to read | Required evidence | Exit condition |
|---|---|---|---|
| G1 | motion-director | brief.md, assets.json, reference-analysis.md | Claims sourced; required real assets exist; direction chosen |
| G2 | motion-storyboard, then motion-design | style-guide.md, shotlist.md, spec.json, styleframes | Clear story; every shot justified; format layouts and reading holds defined |
| G3 | motion-engineer | editable source, render command, representative frames | Fonts/media loaded; arbitrary frame seeks stable; design approved internally |
| G4 | motion-audio, then motion-review | cue sheet, rough cut, beat and transition contact sheets | Both picture and sound observed; defects timestamped |
| G5 | motion-review with responsible role | revisions and re-rendered evidence | Fix highest-impact three defects; verify before/after; repeat boundedly |
| G6 | motion-engineer, motion-review | per-format exports/posters, qc.json, delivery.md | All requested deliverables exist and visual, audio, technical checks passed |

Treat gates as documented internal checks in autonomous mode; show useful evidence without stopping for six approvals. Pause only for a material unresolved requirement (missing truthful asset, contradictory brief, unavailable licensed music) or if the user explicitly requested approval at that gate. Advance independent work while blocked. Do not pause simply because the article said "approve". Never publish externally without authorization.

## Production rules
- Use exact product UI/screens, approved logo and sourced metrics. If unavailable, omit unsupported claims or label a temporary placeholder and report the blocker; do not deliver a plausible fake.
- Maintain one canonical spec with integer frame ranges `[start,end)`, one fps and explicit audio cues. Use seconds for human notes only. Validate with `studio.py validate <project>`.
- Choose the smallest renderer that handles the actual film. Pillow suits procedural 2D graphic pieces; Canvas suits browser graphics; Remotion suits reusable React/UI/media scenes; use another engine only after checking its real CLI/API. Do not assume tools mentioned in an article are installed.
- Make stills at each beat, plus consecutive frames around fast transitions. A contact sheet cannot prove temporal quality or sound. Watch the rough cut and listen at least once; report any inspection capability that was unavailable.
- Follow [quality-contract.md](references/quality-contract.md). Repair factual errors, readability and continuity before ornament. Limit ordinary aesthetic repair to three cycles; unresolved blockers remain blockers, never silently downgrade to final.
- Design each aspect ratio with explicit layout overrides, not a center crop. Reuse story and assets; adjust pacing only when justified and update spec.
- Save checkpoints after each gate: completed artifacts, observations, defects, next action. Invalidate downstream evidence when upstream copy, fps, asset, style or timing changes.
- Deliver editable source, exact dependency versions/lockfile, reproducible commands, asset provenance, final videos, poster, per-format reviews and remaining limitations. Separate requested drafts from verified finals.

## Executable pipeline
Read [pipeline.md](references/pipeline.md) before execution. Use `doctor.py` to check the chosen engine. `pipeline.py demo <new-project>` creates original procedural sample inputs; `pipeline.py run <project> --engine pillow|canvas|dom --run-id <version>` validates, mixes audio, renders each layout, encodes, verifies, and produces review evidence. Use sample art only to test the toolchain. Customize the project's composition for a real brief.

Treat `technical_pass_review_pending` as a rendered draft. Inspect actual contact sheets, phone posters, transition clips and full film, listen to required audio, and record defects before marking any creative gate passed. Canonical audio mode and cues live only in spec.json; reject a second audio-cues.json.

## Bundled tools
- `studio.py init/validate/samples`: create production documents, check spec/assets, select beat/transition review frames. See `--help`.
- `contact_sheet.py`: assemble timestamped stills or extract selected frames from a local video; requires Pillow and FFmpeg for video input. Inspect the resulting image.
- `export_claude.py --destination <project>/.claude/skills`: install by frontmatter name; inspect `--update --dry-run` before upgrading. Updates require a saved baseline, protect local edits and create a backup. Preserve earlier installations manually when they have no baseline. Export is not installation into the user's other account.
- `assets/pillow_composition.py`, `assets/canvas-starter.html` and `assets/render.mjs`: copy into a project as a minimal deterministic renderer. Read [renderer-recipes.md](references/renderer-recipes.md). The sample is a generic graphic, never a finished product film.

## Validation
Read [validation-status.md](references/validation-status.md) before claiming that bundled rendering was tested end to end. Re-run missing production checks in the target environment.

## Sources and boundaries
Read [sources.md](references/sources.md) for article-to-workflow mapping and primary references. The article motivates the system; the extra design defaults and thresholds are this studio's adjustable operating policy, not claims about universal designer practice. Do not guarantee human-level taste, virality or automatic perfection.

## v1.2 motion library and calibration

Use motion-design’s `scripts/recipes.py` and recipe catalog for six editable, seekable Pillow techniques. Use motion-review’s `scripts/benchmark.py` for blind still/video calibration with media hashes and pending perceptual scores. Treat samples as studies; choose and adapt the technique to the brief before production.

## v1.3 DOM production

Read [dom-production.md](references/dom-production.md) for real local UI capture, packaged fonts, named event timing, original SFX and the 15-second functional-app promo. Use explicit `dom` engine selection. Keep render hashes and perceptual review evidence separate.

## v1.4 preview and bound review

Read [review-studio.md](references/review-studio.md) to inspect a rendered run in the local preview studio, focus captured UI with deterministic camera transforms, examine readability warnings and record per-format observations bound to exact inputs/export bytes. Use review.py import/assess/compare after actual inspection. Never inherit approval after inputs change.
