---
name: step-through-visuals
description: How the recorded step-through visuals and code traces work — the viz spec format, gen:viz, the tracer, and phone-width limits. Load before authoring, editing, or debugging any visual or CodeTrace.
---

# Step-through visuals

Nothing executes in the browser. Every visual and trace is recorded at authoring time under PyPy
3.8 and replayed as static, versioned data (`*.frames.json`, `*.trace.json`) — the first frame is
server-rendered and fully meaningful on its own, with no autoplay.

## Pipeline

- A visual source lives in its module folder (`content/stages/<stage>/<module>/visuals/*.viz.py` for
  the nine library visualizers, or a plain example `.py` for a `CodeTrace`).
- `npm run gen:viz` runs the recorders under PyPy 3.8 (`tools/viz/lib.ts` resolves the interpreter
  via `lib/tools/resolve-tools.ts` — see `AGENTS.md`'s tool prerequisites) and writes the generated
  files deterministically.
- Always regenerate, never hand-edit a generated file.
- By owner rule no agent opens a screenshot. Check a figure by reading its source and frames JSON
  against the limits below and its captions against the prose.

## What a visual must have

Zod-valid data (checked at render time); a caption on every step; a text alternative; behavior
consistent with the shown code; at most `DEFAULT_STEPS` = 200 steps (`tools/viz/lib.ts`,
overridable per visual via `budget:`); and only library components — no ad hoc one-off visual.

## Phone-width and accessibility limits

- Every visual sits in a `Figure` with a caption and a text alternative; step-throughs offer "Read
  the steps as text"; caption regions are `aria-live="polite"`.
- Fully keyboard-operable (play/pause, step, scrub, presets); no flashing; `prefers-reduced-motion`
  turns transitions into snaps or cross-fades.
- State is never shown by color alone.
- Must read at 390×844 (phone), 768×1024, 1440×900 and 1920×1080 — a visual that only reads at
  desktop width is a bug, not a tradeoff.
- Size a preset for a phone: arrays ≤ ~10 cells, grids ≤ ~6×6, graphs/trees ≤ ~9 nodes,
  ≤ ~40 steps per preset.

## Authoring notes

- A visual has one panel (`layout: single`) or exactly two (`layout: row`, stacked on a phone);
  a third quantity goes into a node value (`vz.graph(..., value_label=)`), a caption, or one
  TableViz with a row per quantity. The Zod limits in `lib/viz/schema.ts` cap cells, nodes and
  label lengths; read them before sizing a preset.
- The first step is what renders without JavaScript, so its first panel must draw something with
  text in it: never open on an empty structure (fold "starts
  empty" into the first real change), and give grid cells values, not state alone.
- Schema caps worth knowing before sizing: at most 3 presets per visual, and a `TableViz` at most
  10 rows and 10 columns. At 390 px, a table or grid of about 6 columns with short labels is the
  practical limit; split a longer row into two rows with row heads instead of dropping data.
- Panels are laid out in a 361-unit width, so the real limits are tighter than the
  ~10-cell rule of thumb: an ArrayViz fits 7 short cells (8 measured 368), and a TreeViz with 8 leaves overflows
  (6 fit). Other caps that fail late: at most 2 `ranges` per ArrayViz frame, `valueLabel` at most
  10 characters, and `legendLabels` keys are state names (`frontier`, not `queued`). A TableViz
  `row_title` longer than its column heads collides with them.
- A `CodeTrace` records every executed line, so a whole program easily passes 40 steps a preset:
  trace a slim dedicated file that the module names as the short version instead. Tracer quirk:
  when a `for` variable's next value equals its previous one, the step caption reads "no values
  left"; avoid that input or say so in the prose.
- Width is measured over the union of all presets: one long cell (a placeholder like `(none)`)
  widens every frame, and a TableViz gives every column the widest cell's width. A CodeTrace's
  width comes from its variables panel, not only its code lines: a long `raw` string, a big token
  list, or long function names in the global frame overflow it. Trace a file that reads a few
  tokens, or read with `data = sys.stdin.read().split()` and keep no `raw`.
- Other schema caps: a step caption is at most 320 characters; `legendLabels` values and panel
  titles 24 characters; an ArrayViz `name` 12; a TableViz `colTitle` 12; LineViz at most 10
  intervals and 4 rows per frame, with tick and point labels colliding when closer than about 3
  ticks (use tick 30 on a 0–180 axis). GraphViz draws no self-loops.
- A TreeViz node id must keep the same parent in every frame of
  every preset, so build ids from the path ("0-1-2") and show the number as the label.
- Every recorded visual needs `consistency:` with an example, and the example is re-run on every
  preset's stdin. A static reference table with no program behind it goes inline instead.
- `.trace.yaml` `notes` and `skip` keys name the line that just ran, not the next one; a note on a
  line a preset never runs fails generation, and a note attaches to every preset that runs its
  line, so keep notes preset-neutral. A skip rule fires once and at most 4 are allowed.
- A multi-line comprehension traces as one step with the caption "no values left": use a loop.
- A `.viz.py` sees only its preset's stdin, never the preset id: vary presets through stdin.
- Label a panel once: its `title` in the `.viz.yaml` or the frame's `name=`, not both.
- Preset labels share one tab row: keep each to one or two words, or the page scrolls sideways
  at 390 px.
- A `CodeTrace` shows the whole example file and every line must fit a 390 px phone without
  scrolling: keep traced lines to about 30 characters by
  splitting a statement in two or using shorter local names (keeping a long `raw` string alive
  widens the variables panel instead; see the width note above). Prefer the single-`main()` skeleton for a
  traced file, so the last steps still show the program's own variables.
- Inline `<Diagram viz=… data={{…}}>` data is validated at render time: use
  one-letter state codes (`"d"`, `"c"`, `"m"`), and give its `<Figure>` an `alt` (only the
  `frames=` form inherits the `.viz.yaml`'s `alt`). A mistake shows up as a page error, so load
  the module page after adding one.
- When a state's default legend word does not fit the picture (e.g. `wall` hatching used for a
  chessboard's shaded squares), rename it: `legendLabels: {wall: Shaded square}` in the
  `.viz.yaml` (a `frames=` Diagram inherits it), or `legendLabels={{ wall: "Shaded square" }}` on
  an inline `<Diagram>`.

## Debugging a broken visual

1. Reproduce with `npm run gen:viz -- --scope <module id>` and load the module page before
   touching anything.
2. If the problem is in the data, fix the `.viz.py` source and regenerate — never hand-patch the
   JSON.
3. If the problem is visual only (layout, color, motion), check it from the source and frames JSON
   against the limits above.
