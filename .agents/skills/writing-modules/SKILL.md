---
name: writing-modules
description: Voice, format, file layout and code conventions for module pages. Load before writing or editing any module.mdx, module.yaml, its example code, or content/ui/strings.yaml.
---

# Writing modules

## Where things go

A module is one page. Its folder `content/stages/<stage>/<id>-<slug>/` holds:

- `module.mdx` — the page body: plain MDX that starts with the first paragraph. **No
  frontmatter** (content:check fails a file that starts with `---`) and **no `<Practice />`
  tag**: the page renders the practice list after the body by itself.
- `module.yaml` — `id`, `status`, `objectives` (shown as "In this module") and `practice`. No
  `title`: the title lives in `content/course.yaml` only and is the page H1.
- `examples/` and `visuals/`, referenced from `module.mdx` by paths relative to the folder.

Splitting a topic means adding a new module (a new course.yaml entry plus its own folder), never
a second `.mdx` file in one folder.

## Read first

- `content/style/STYLE-GUIDE.md` — voice, vocabulary, terminology lock (tied to the glossary),
  banned patterns, sentence-case headings, and the R14 wording rules in full.
- `content/style/house-skeleton.py` — the code conventions every example follows: naming,
  4-space indents, Python 3.8 only.
- The approved teaching-voice sample it cites, for tone and pacing.

## Voice

Warm, plain, second person, short sentences in Stages 0–2. No hype, no clipped fragments, no
judgments about the learner. Use the `avoid-ai-writing` skill (`.agents/skills/avoid-ai-writing/`)
in its `warm` voice and `docs` context on every prose pass — `tools/style/check-style.mjs` runs its
detector over every module page and over `content/ui/strings.yaml` (G-STYLE).

## Format

- Every real module page needs **at least 800 words** of extracted prose (`minProseWords` in
  `tools/style/thresholds.json`; the target range is 800–1,300). Check with
  `npm run style:check -- --words`.
- Stage 3 onward: teach the technique on a worked example you write for teaching — reasoned
  through in steps (shape of the problem → bounds → brute force → insight → code → a Python speed
  note) — **never** on a specific registry problem, and never imply it solves one. The module's
  practice list at the end is the only place a specific CCC problem is named.
- No problem walkthroughs, editorials, solution pages or per-problem hints, ever, and never say
  one exists elsewhere. A practice entry gets at most a one-line `note`, and a DMOJ pick a one-line
  `why`.
- No score targets, cutoffs, medals, CCO qualification, or "Python can't/is too slow" framing.

## Code

- Every shown sample is Python 3.8, matching `content/style/house-skeleton.py`'s conventions.
- A deliberately invalid block is fenced ```` ```python bad38 ```` and must fail at least one of
  ruff/vermin/PyPy 3.8 (G-PY-38); a `bad38` block that passes all three is itself an error.
  Deliberately failing examples show their real traceback.
- File-based examples with a committed `.out`/`.err` are regenerated with `npm run gen:outputs` —
  never hand-edit those files. No example may print wall-clock timings: `.out` must reproduce
  byte for byte, so show a cost as a counted number of operations instead.

## MDX

Prose is MDX: a bare `{`, `}` or `<` starts an expression or a tag, so put code-like text in
backticks. `$…$` math renders through KaTeX; keep it to simple forms like `$10^5$` and prefer
backticked plain forms (`2 * 10^5`, `O(N log N)`) for anything with braces.

## Terms and feature order

Wrap a term in `<Term id="...">` only after its `introducedIn` module in `content/glossary.yaml` —
G-PREREQ checks usage against it via an AST feature scan of the actual code. Judge links: derive
from `content/registry/ccc-problems.yaml` only, never type a URL by hand (see `AGENTS.md`).
