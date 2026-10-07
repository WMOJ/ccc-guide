# Agent Guide

## What this is

A free, non-commercial, all-in-one reading course (Next.js 16 App Router) that takes a complete
beginner from their first line of code to everything they need to compete at the highest level of
the CCC Senior contest (S1–S5), in **Python 3.8** — the language level of the CCC grader's PyPy.
Prose, worked examples, read-only code, and recorded animated step-throughs; practice happens
outside the app, on WMOJ/DMOJ. No accounts, no scores, no code execution in the app.

## Commands

```bash
npm run dev              # next dev
npm run build            # production build (through scripts/build-lock.mjs)
npm run lint             # biome check .
npm run typecheck        # tsc --noEmit
npm run gen:outputs      # regenerate every example's .out/.err under PyPy 3.8
npm run gen:viz          # regenerate every visual's frames/trace JSON under PyPy 3.8
npm run content:status   # rebuild ledger.generated.md from each module.yaml's status
```

## Tool prerequisites

Node version is pinned in `package.json`'s `engines`. PyPy 3.8 (for the generators) is a normal,
system-wide install.

## Broad rules every change must respect

- **No agent views images** (owner rule): no reading PNG/JPG screenshots, no browser or
  computer-use screenshots, and no scripts, npm commands or tooling that render screenshots or
  images to look at. Check visuals from text (source and frames JSON).
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
  and every visual's `*.frames.json`/`*.trace.json` (from `gen:viz`). Re-run the generator
  instead of editing the output.

## Content model

A module and its page are one thing: each module is one reading page at `/learn/<stage>/<module>`
(body, then its practice list). A module is never split into sub-pages and has no prerequisite
list.

- `content/course.yaml`: stages → modules, in order, each with a `status` and a `title` — its only
  title (page H1, course map, sidebar, search).
- `content/stages/<stage>/<id>-<slug>/`: `module.yaml` (`id`, `status`, `objectives`, `practice`),
  `module.mdx` (the page body: plain MDX, no frontmatter, no `<Practice />` — the page renders
  practice), example `.py`/`.out`/`.err` files, and a `visuals/` folder of recorder scripts
  (`.viz.py`) plus their generated output. The folder is found by its `<id>-` prefix alone.
- `content/registry/ccc-problems.yaml`: the 119 CCC 2014–2026 problems (WMOJ/DMOJ links, aliases).
- `content/glossary.yaml`: terms, each with the `introducedIn` id of the module that first uses it.
- `content/ui/strings.yaml`: all learner-facing UI copy.
- `content/style/STYLE-GUIDE.md` and `house-skeleton.py`: the voice, format and code conventions —
  read before writing or editing any module.

## Maintaining this file

Keep it current — fixing what is outdated, wrong or missing here is part of your change, not extra
credit — and keep it **at or under 150 lines**. Update it the moment you notice anything in it is
stale, without waiting to be asked; the same goes for every project skill in `.agents/skills/`.

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
