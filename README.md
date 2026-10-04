# CCC Python course

A free, non-commercial Next.js app that teaches CCC Senior (S1–S5) algorithms in Python 3.8, the
language level of the CCC grader's PyPy. Prose, worked examples, and recorded animated
step-throughs; practice happens outside the app, on WMOJ/DMOJ. See `PRODUCT.md` and `DESIGN.md`
for the full product and design spec, and `AGENTS.md` for the rules every change follows.

**Live site:** _(URL to be filled in)_

## Prerequisites

- **Node**, version pinned in `package.json`'s `engines` field.
- **PyPy 3.8** (for `gen:outputs` and `gen:viz`) — a normal, system-wide install, nothing
  confined to this repo. See `.agents/skills/tool-setup/SKILL.md` for the pinned version, install
  steps, and a one-line check.
- **git** and **gh**, already logged in as usual — nothing here needs a special configuration.

## Commands

```bash
npm ci                   # install dependencies
npm run dev               # next dev
npm run build             # production build
npm run lint              # biome check .
npm run typecheck         # tsc --noEmit
npm run gen:outputs       # regenerate example .out/.err files under PyPy 3.8
npm run gen:viz           # regenerate step-through visual data under PyPy 3.8
```

## Content layout

```
content/
  course.yaml               stages -> modules, in order, each with its title and status
  stages/<stage>/<module>/   module.yaml, module.mdx, example .py/.out/.err, visuals/
  registry/ccc-problems.yaml  the 119 CCC 2014-2026 problems, WMOJ/DMOJ links
  glossary.yaml              terms, each tied to an introducing module
  ui/strings.yaml            all learner-facing UI copy
  style/STYLE-GUIDE.md, house-skeleton.py   voice and code conventions for modules
```

Only `accepted` modules render in production; `gated`/`reviewed` show with a Draft badge in
previews, and `planned`/`drafted` show "Coming soon" with no link.

## Agent guidance

`AGENTS.md` holds the rules every change respects; `.agents/skills/<name>/SKILL.md` holds
triggered, narrower guidance (loaded only when relevant). `CLAUDE.md` just points at `AGENTS.md`;
`.claude/skills` is a symlink to `.agents/skills` so Claude Code sees the same skills.
