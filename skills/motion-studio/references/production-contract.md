# Production contract

## Project records
brief.md: objective, audience, truthful claims, format, language, asset requirements and assumptions.
reference-analysis.md: inspected evidence and adopted/excluded traits.
style-guide.md: editable visual/motion rules.
shotlist.md: purpose, states, frame ranges, continuity, exact copy and format overrides.
assets.json: {assets:[{id,path,role,provenance,rights,approved,required}]}; use project-relative file paths; required assets must exist and be approved with known usable rights. Use rights values `user-provided`, `licensed`, `original`, `public-domain`, `unknown` and document the user's supplied scope; labels alone do not establish permission.
spec.json: canonical machine timeline described below.
status.json: gate records, autonomy, source version and next action.
reviews/: observed frames/strips/review notes, never presumed scores.
out/: rendered variants, posters, mixes and qc.json.
src/: editable frame engine.

## Spec version 1
Required top-level: version=1, fps (positive integer), duration_frames (positive integer), seed (integer), formats array, shots array, audio_cues array.
Format: {id,width,height,safe:{top,right,bottom,left}}; use integer pixels, distinct ids and actual composition insets.
Shot: {id,start,end,purpose,entry_state,exit_state,copy,asset_ids,layouts,transitions}.
- start/end integer half-open global frames; ordered contiguous coverage 0..duration_frames.
- layouts: object keyed by each format id. Populate explicit layout decisions; never leave empty/null for production validation.
- transitions: [{start,end}], bounded global ranges inside film; sample consecutive frames around these, not just shot midpoint.
Cue: {id,path,start_frame,duration_frames,source_offset_seconds,gain_db,visual_event_frame,intentional_offset_frames}; default gain=0, offset=0. Ensure cue plus tail fits the film unless intentionally trimmed in plan. Existence checks do not assess sound quality.
assets.json may contain optional assets; shots must reference known ids. Film may have zero assets for original procedural graphics; it may have no audio cues only when silence is intentional or draft status is recorded.

## Gate state
Record pending/passed/blocked per gate, artifact paths, observations, input/spec hash and next action. Missing assets block relevant production gate, not unrelated concept work. Do not mark later gates passed when upstream evidence is stale. Only user-requested supervised gates need approval.

## Resume
Read saved gate status, spec and latest review first. Verify paths and prior commands. Resume from earliest invalidated gate; never rebuild the entire film merely because the conversation compacted.
