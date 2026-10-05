---
name: motion-storyboard
description: "Create motion-film shot lists, storyboards, styleframes, animatics and format-aware layouts. Use to turn an approved brief into purposeful scenes with frame ranges, readable copy and visual continuity."
---

# Motion Storyboard

Read [story-and-layout.md](references/story-and-layout.md). Turn the brief into a sequence of information gains before choosing transitions.

1. Read brief, reference analysis and approved assets. Write shotlist.md with id, integer start/end frames, purpose, what viewer learns, entry state, exit state, focal object, exact copy, asset ids, movement, audio cue and format overrides.
2. Keep one primary focal event per beat. Give each meaningful state enough visible stable time to be understood. Measure reading holds from actual word count and audience; reserve entrance/exit separately. Do not use a word-count formula as proof that a phone viewer can read it.
3. Preserve object identity across shots with continuity ids, screen-space anchors and explicit z-order. Map states like SEARCH→RESULT→DETAIL only when the real product supports them.
4. Draw styleframes for opening, proof, hardest transition and final state at each requested format. Establish type scale, margins, contrast and spatial relationships before detailed animation.
5. Update spec.json using the project's canonical schema. Use contiguous non-overlapping frame ranges for story beats; if the design needs visual overlap, model it inside transitions, not conflicting narrative ranges. Validate duration and cues.
6. Create an animatic with flat shapes/stills to inspect story and pacing. Revise the sequence if it feels confusing even with effects removed. Hand frame timing and continuity contract to `motion-design` and `motion-engineer`.

Never approve a shot only because it looks impressive. Remove or combine a shot that contributes no new information, purposeful emotion or resolution.
