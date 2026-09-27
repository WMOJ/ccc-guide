---
name: step-through-visuals
description: How the recorded step-through visuals and code traces work — the viz spec format, gen:viz/check:viz, the tracer, and phone-width limits. Load before authoring, editing, or debugging any visual or CodeTrace.
---

# Step-through visuals

Nothing executes in the browser. Every visual and trace is recorded at authoring time under PyPy
3.8 and replayed as static, versioned data (`*.frames.json`, `*.trace.json`) — the first frame is
server-rendered and fully meaningful on its own, with no autoplay.

## Pipeline

- A visual source lives next to its lesson (`content/stages/<stage>/<module>/visuals/*.viz.py` for
  the nine library visualizers, or a plain example `.py` for a `CodeTrace`).
- `npm run gen:viz` runs the recorders under PyPy 3.8 (`tools/viz/lib.ts` resolves the interpreter
  via `lib/tools/resolve-tools.ts` — see `AGENTS.md`'s tool prerequisites) and writes the generated
  files deterministically.
- `npm run check:viz` (G-VIZ) re-runs generation and fails on any diff, so a hand-edited generated
  file is caught immediately — always regenerate, never hand-edit.
- `npm run viz:shots` captures the Playwright screenshots G-VISUAL compares against baselines.
- The tracer itself (`tools/viz/trace.py`) is exercised directly by
  `tests/unit/viz/tracer.test.ts` (skipped with a visible reason when PyPy 3.8 isn't available).

## What G-VIZ checks

Zod-valid data; `gen:viz` regenerates with **no diff**; a caption on every step; a text
alternative present; the visual's declared behavior stays consistent with the shown code; size and
step budgets (`DEFAULT_BYTES` = 150,000 bytes, `DEFAULT_STEPS` = 200 in `tools/viz/lib.ts`, both
overridable per visual via `budget:`); and only library components are used — no ad hoc one-off
visual.

## Phone-width and accessibility limits

- Every visual sits in a `Figure` with a caption and a text alternative; step-throughs offer "Read
  the steps as text"; caption regions are `aria-live="polite"`.
- Fully keyboard-operable (play/pause, step, scrub, presets); no flashing; `prefers-reduced-motion`
  turns transitions into snaps or cross-fades.
- State is never shown by color alone.
- Checked at 390×844 (phone), 768×1024, 1440×900, plus a 1920×1080 smoke (G-VISUAL, G-PAGE) — a
  visual that only reads at desktop width is a bug, not a tradeoff.

## Debugging a broken visual

1. Reproduce with `npm run check:viz -- --scope <module id>` before touching anything.
2. If the diff is in the data, fix the `.viz.py` source and regenerate — never hand-patch the
   JSON.
3. If the diff is visual only (layout, color, motion), it is a G-VISUAL baseline question — see the
   `verifying-changes` skill.
