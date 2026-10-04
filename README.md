# CCC Python course

A free, non-commercial Next.js app that teaches CCC Senior (S1–S5) algorithms in Python 3.8, the
language level of the CCC grader's PyPy. Prose, worked examples, and recorded animated
step-throughs; practice happens outside the app, on WMOJ/DMOJ. See `PRODUCT.md` and `DESIGN.md`
for the full product and design spec, and `AGENTS.md` for the rules every change follows.

**Live site:** _(URL to be filled in)_

## Prerequisites

- **Node**, version pinned in `package.json`'s `engines` field.
- **PyPy 3.8**, **ruff**, **vermin**, and **Playwright's browsers** — all normal, system-wide
  installs, nothing confined to this repo. See `.agents/skills/tool-setup/SKILL.md` for exact
  pinned versions, install steps, and a one-line check for each.
- **git** and **gh**, already logged in as usual — nothing here needs a special configuration.

## Commands

```bash
npm ci                   # install dependencies
npm run dev               # next dev
npm run build             # production build
npm run verify:fast       # lint, typecheck, unit tests, and every content gate
npm run verify:full       # verify:fast + production build + Playwright (e2e, visual, a11y)
```

See the `verifying-changes` and `content-gates` skills (`.agents/skills/`) for what each gate
checks and how to debug a failure.

## Content layout

```
content/
  course.yaml               stages -> modules, in order, each with its title and status
  stages/<stage>/<module>/   module.yaml, module.mdx, example .py/.out/.err, visuals/
  registry/ccc-problems.yaml  the 119 CCC 2014-2026 problems, WMOJ/DMOJ links
  glossary.yaml, concepts.yaml  terms and Python features, each tied to an introducing module
  ui/strings.yaml            all learner-facing UI copy
  style/STYLE-GUIDE.md, house-skeleton.py   voice and code conventions for modules
```

Only `accepted` modules render in production; `gated`/`reviewed` show with a Draft badge in
previews, and `planned`/`drafted` show "Coming soon" with no link.

## Agent guidance

`AGENTS.md` holds the rules every change respects; `.agents/skills/<name>/SKILL.md` holds
triggered, narrower guidance (loaded only when relevant). `CLAUDE.md` just points at `AGENTS.md`;
`.claude/skills` is a symlink to `.agents/skills` so Claude Code sees the same skills.
