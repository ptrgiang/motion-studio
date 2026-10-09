---
name: motion-design
description: "Design typography, composition, easing, springs, staging and transitions for motion graphics. Use when a motion film looks generic, lacks hierarchy, has weak timing or needs professional visual and movement polish."
---

# Motion Design

Read [motion-language.md](references/motion-language.md). Design a coherent visual language, then use movement to direct attention and clarify change.

1. Translate reference observations into `style-guide.md`: palette roles, type families and fallbacks, weights, optical sizing, grid, negative space, texture, object classes and movement rules. Check installed fonts and Vietnamese/other requested glyphs; package only redistributable fonts.
2. Assign each animated property a reason. Choose entry, travel, settle and hold phases. Use optical balance rather than coordinates alone; inspect actual letterforms, line breaks and dark/light area.
3. Define reusable motion tokens in frames at the canonical fps: micro interaction, panel, camera, headline, optional character. Record easing/spring parameters, acceptable overshoot and explicit rest states. Test the curve on a representative element before reuse.
4. Stage primary before secondary motion. Keep overlapping actions readable; synchronize when they form one cause-and-effect group and stagger when they reveal hierarchy.
5. Preserve continuity of position, scale, direction and object identity. Prefer meaningful match cuts, reveals, masks or object transformations to a different transition preset for every scene.
6. Inspect moving previews and strips around fast changes; fix unintentional tangencies, velocity discontinuities, accidental collisions, type shimmer and excessive motion blur. Do not smooth out deliberate hard cuts.
7. Hand the engineer explicit values plus reference frames. When polishing a rough cut, report the timestamp, perceptual defect, smallest change and expected visual result.

Use gradients, particles, glass and overshoot only when the concept earns them. Avoid defaulting to giant centered text on a gradient or moving every layer continuously. These are contextual judgments, not a ban on legitimate design techniques.

For executable techniques, read [recipe-catalog.md](references/recipe-catalog.md) and materialize a study with `scripts/recipes.py`. Use its stated purpose to choose and adapt movement, then review both formats.

For HTML techniques, use motion-studio’s `assets/motion-dom.mjs` and `references/dom-production.md`: scalar/vector paths, grapheme-aware kinetic type, shot-local time and beat clock. Adapt the original 15-second demo to a real brief. Measure packaged-font geometry and review phone-size readability; animation helpers do not establish aesthetic quality.

## v1.4 review workflow

Read motion-studio’s references/review-studio.md for the local preview, camera geometry, readability diagnostics and review.py commands. Resolve motion-studio by frontmatter name. Inspect actual exported motion/audio; source or asset changes require a new run and fresh review. Treat machine readability findings as heuristics.

## Showreel revisions

For a studio intro, brand reel or slideshow critique, resolve motion-studio by frontmatter name and read references/showreel-craft.md. Follow the motif/action/camera/reading plan and use executable craft tools when appropriate. Review encoded results; ambient wobble is not narrative motion and a machine pass is not creative approval.
