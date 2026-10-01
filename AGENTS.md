<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

## Maintaining this file

Keep it current — fixing what is outdated, wrong or missing here is part of your change, not extra
credit — and keep it **at or under 150 lines**.

⚠️ **Maintenance here is ZERO-SUM.** The budget is the point: a file nobody finishes reading guides
nothing. So the test is never "is this true and useful" (almost everything is) but:

> **Is this worth removing something else to make room for?**

If no, it does not go here. If yes, name what you cut and cut it in the same change — though while the
file is *under* 150 that room already exists, so add freely: spare budget is there to be spent, and a
file that uses it well beats one that leaves it on the table. Where it goes instead:

1. **Has a detectable trigger** ("when editing a table", "when touching the PDF pipeline") → a
   **skill**, loaded only when needed and costing nothing otherwise. This is the default answer.
2. **Broad and unconditional** — every change must respect it, whatever it touches → this file.
3. **Neither** → bloat: delete it, or leave it as a comment beside the code, where a narrow fact stays
   honest longest. A fact with no trigger is not a skill either — never invent one to hold it.

Skills live in `.agents/skills/<name>/SKILL.md`.

## What this is

A free, non-commercial reading course (Next.js 16 App Router) that teaches CCC Senior (S1–S5)
algorithms in **Python 3.8** — the language level of the CCC grader's PyPy. Prose, worked
examples, read-only code, and recorded animated step-throughs; practice happens outside the app,
on WMOJ/DMOJ. No accounts, no scores, no code execution in the app. See `PRODUCT.md` and
`DESIGN.md` for the full product and design spec.

⚠️ **About 80 lessons (Tiers B and C) were rushed** under a reduced process late in the build.
Load the `rushed-content` skill before any content review, audit or QA. **That skill, and this
warning line, are temporary**: delete both together once the owner has fixed or is satisfied with
the rushed lessons. Do not treat `rushed-content` as permanent, and do not grow it into general
content guidance.

## Commands

```bash
npm run dev              # next dev
npm run build            # production build (through scripts/build-lock.mjs)
npm run lint             # biome check .
npm run typecheck        # tsc --noEmit
npm run test:unit        # vitest
npm run verify:fast      # the fast gates (lint, types, unit, schema, style, R14, links, ...)
npm run verify:full      # verify:fast + build + Playwright (e2e, visual, a11y) + link checks
```

`verify:full` must be green before any change is considered done. See the `verifying-changes`
skill for what each gate checks and how the Playwright suites are wired.

## Tool prerequisites

Node version is pinned in `package.json`'s `engines`. Everything else (PyPy 3.8, ruff, vermin,
Playwright's browsers) is a normal, system-wide install — see the `tool-setup` skill for exact
pinned versions, install steps, and a one-line check for each.

## Broad rules every change must respect

- **No agent views images** (owner rule): no reading PNG/JPG screenshots or baselines, no browser
  or computer-use screenshots. Check visuals from text (source, frames JSON, `check:viz`,
  `viz:shots`'s text report); new visual baselines are accepted unseen.
- **Light mode only.** No dark theme, no `prefers-color-scheme: dark`, no `dark:` classes.
- **Every shown code sample is Python 3.8**, because that is what the CCC grader's PyPy runs. A
  deliberately invalid example is labeled "not valid on the CCC grader"; a deliberately failing one
  shows its real traceback. Never show or imply 3.9+ syntax as something the learner can use.
- **Problem links only through the registry** (`content/registry/ccc-problems.yaml`), never a
  hand-typed judge URL: 2021–2026 → WMOJ (preferred), 2014–2020 → DMOJ, CCC 2014–2026 only.
- **No score targets, cutoffs, medals, CCO qualification, or "Python can't/is too slow" framing.**
- **No problem walkthroughs, editorials, solution pages or per-problem hints, anywhere**, and no
  mention that one exists elsewhere. A practice entry gets at most a one-line note.
- **No system or environment setup content**: no OS instructions, online editors, or installing
  Python/PyPy/Thonny.
- **No exercises, quizzes, checkpoints or code execution in the app.** Reading only.
- **Only `accepted` modules render in production.** `gated`/`reviewed` show with a Draft badge in
  previews; `planned`/`drafted` show "Coming soon" with no link.
- **Generated files are never hand-edited**: every example's `.out`/`.err` (from `gen:outputs`),
  every visual's `*.frames.json`/`*.trace.json` (from `gen:viz`), `verified.json` (from
  `links:verify`), and the `<!-- BEGIN/END:nextjs-agent-rules -->` block at the top of this file
  (re-written by `next dev`). Re-run the generator instead of editing the output.

## Content model

- `content/course.yaml`: stages → modules, in order, each with a status.
- `content/stages/<stage>/<module>/`: `module.yaml`, `lessons/*.mdx`, example `.py`/`.out`/`.err`
  files, and a `visuals/` folder of recorder scripts (`.viz.py`) plus their generated output.
- `content/registry/ccc-problems.yaml`: the 119 CCC 2014–2026 problems (WMOJ/DMOJ links, aliases).
- `content/glossary.yaml`, `content/concepts.yaml`: terms and Python features, each with an
  `introducedIn` module id that prerequisite and glossary checks enforce.
- `content/ui/strings.yaml`: all learner-facing UI copy.
- `content/style/STYLE-GUIDE.md` and `house-skeleton.py`: the voice, format and code conventions —
  read before writing or editing any lesson (see the `writing-lessons` skill).
