# Product

<!-- A few inferences are marked "Inferred". -->

## Platform

web

## Users

**One learner, a secondary-school student, who has never written a line of code.** They read on a laptop at a desk after school, for 20 to 60 minutes at a time, over many months (Inferred from the 104-module scope and "months of study"). A phone is the second device: a module started on the laptop is sometimes finished on the bus or in bed, so phones must be comfortable, not just functional.

The learner's job on a module page is to **understand one idea well enough to use it on a real problem later**: read the explanation, look at the example code and its output, step through the animation until the idea clicks, then leave the app to practise on an online judge. They come back to the course map to find where they stopped.

Secondary readers (not designed for, but present): the Manager (a parent or mentor figure who built the course and reviews it on preview links) and reviewers checking the content.

## Product Purpose

A free, non-commercial reading course that takes the learner from zero programming to the algorithms needed for every level of the **CCC Senior** contest (S1 to S5), in **Python 3.8** (the language level of the CCC grader's PyPy).

It teaches with prose, worked examples, read-only Python code, input and output panels, and a large number of animated step-throughs and code traces recorded at authoring time. Practice happens **outside** the app, on WMOJ and DMOJ, through a short list of real CCC problems at the end of each module.

Success is quiet: the learner keeps coming back, reads a module to the end, understands it, and goes to practise. There are no scores, streaks or dashboards to measure it.

## Positioning

The only course that goes from "never programmed" to CCC Senior S5 **in Python 3.8 specifically**, and that shows every program actually running (line-by-line traces and algorithm step-throughs replayed from real PyPy 3.8 runs) instead of describing it. Every shown output was produced by running the shown code; every problem link is derived from a verified registry.

## Operating Context

- **Reading sessions**, long-form: a module is one page of about 800 to 1,300 words plus code and visuals. Scale: 104 modules across stages 0 to 7 plus a contest-skills track C.
- **Leaving and returning**: the learner copies code into their own editor (copy button) and opens judge problems in new tabs. "Mark as read" and "Continue where you left off" are the only state, held in one localStorage key.
- **Surfaces and their modes** (Impeccable modes):

  | Route | Surface | Mode |
  |---|---|---|
  | `/` | Home: what the course is, how to use it, continue, stage overview | Read (a docs index is Read, not Persuade) |
  | `/start` | Getting started: how practice works on the judges, what the CCC is | Read |
  | `/learn` | Course map: stages → modules, read marks, "Coming soon" | Read, with light Operate wayfinding |
  | `/learn/[stage]/[module]` | **Module page** (the core surface): objectives, the reading, then its practice list. Old `/learn/[stage]/[module]/[slug]` links redirect here | Read |
  | `/problems` | All 119 registry problems by year and level, with judge links and "taught in" backlinks | Read, reference table |
  | `/search` and the header dialog | Full search | Operate |
  | `/glossary` | Terms, each linked to its introducing module | Read, reference |
  | `/about` | Credits, CEMC attribution, judge acknowledgements, "this app is free" | Read |
  | 404 | Friendly not-found with links back | Read |
  | `/dev/viz` | Visual gallery, previews only | Internal |

## Capabilities and Constraints

- **Reading only.** No code execution, no editor, no in-browser Python, no judge, no grading, no exercises, quizzes, checkpoints, predict-the-output or answer boxes. "Try it" suggestions are prose only.
- **Client interactivity is limited to five features:** search, mark-as-read, visual players, copy-code button, mobile navigation toggle. Everything else is server-rendered; hints and spoilers use native `<details>`.
- **Light mode only.** `color-scheme: light`; no dark theme, no `prefers-color-scheme: dark`, no `dark:` classes.
- **No score targets** of any kind: no target scores, cutoffs, ceilings, medals, CCO qualification, percentiles, "full marks" as a goal, or "Python can't / is too slow".
- **No problem walkthroughs, editorials, solution pages or per-problem hints**, and no mention that one exists anywhere. A practice entry carries at most a one-line note and, for some DMOJ entries, a one-line "why".
- **No system or environment setup content**: no OS instructions, online editors, or installing Python, PyPy or Thonny.
- **Problem links only through the registry**: CCC 2014–2026 only; 2021–2026 → WMOJ (preferred), 2014–2020 → DMOJ. Crossovers render as "2022 J4 (same problem as 2022 S2)".
- **Python 3.8 only** in every shown code sample. Deliberately invalid examples carry a "not valid on the CCC grader" label; deliberately failing programs show their real traceback.
- **Visuals come only from the in-house library** (nine visualizers, a shared player, scenes), fed by data recorded under PyPy 3.8. Nothing executes in the browser; the first frame is server-rendered and fully meaningful; no autoplay.
- **Draft states**: previews show `gated`/`reviewed` modules with a Draft badge; `planned`/`drafted` modules show "Coming soon" with no link. Production shows only `accepted`.
- **All learner-facing UI copy** lives in `content/ui/strings.yaml`.
- **Stack**: Next.js 16 App Router, all pages static; Tailwind 4 `@theme` tokens; Shiki with one custom light theme; Motion inside visuals only; self-hosted WOFF2 fonts; no remote assets at runtime.
- **Open (undecided) facts**: the learner-facing product name is not decided in any project document. Until the Manager sets it in `ui/strings.yaml`, the header wordmark reads from that file and design work uses the neutral working title "CCC Python Course" (Inferred placeholder).

## Brand Commitments

- Tone: **calm, encouraging, focused.** Teaching prose is warm and plain, with no AI-writing tells (see `content/style/STYLE-GUIDE.md`).
- The CCC and its problems belong to the CEMC (University of Waterloo). The app is not affiliated with the CEMC and must not look like an official CEMC product; attribution (CC BY-NC 4.0) lives on `/about`. (The "not official" framing is Inferred from the copyright constraint.)
- The app is free; nothing may charge for access to past contests.
- No logo or identity assets exist. None may be invented that imitate CEMC, WMOJ or DMOJ marks; judges are named in text badges only (Inferred).

## Evidence on Hand

- Course structure: module IDs and titles (score lines and any "Contest payoff" framing are never surfaced in the app).
- Registry: 119 CCC 2014–2026 problems (`content/registry/ccc-problems.yaml`).
- There are **no** testimonials, user counts, results, outcomes or endorsements, and none may be fabricated.

## Product Principles

1. **The page is for reading.** Every screen serves comprehension of one idea at a time; chrome recedes, the module column leads.
2. **Show it running, never claim it.** Outputs, traces and animations come from real runs; nothing checkable is typed by hand.
3. **Steady, not pressuring.** No scores, streaks, targets or urgency; the only progress signal is a quiet "read" mark the learner sets.
4. **Practice lives on the judges.** The app teaches and points; it never solves, hints, or grades.
5. **Trust through precision.** Correct Python 3.8, correct links, pixel-careful layout; a beginner should never have to wonder whether the page is wrong.

## Accessibility & Inclusion

- **WCAG 2.2 AA** throughout: visible focus, adequate target sizes (24 px minimum, 44 px for primary touch targets on phones), skip link, logical headings, code blocks scroll inside themselves.
- Visuals: every one in a `Figure` with caption and text alternative; step-throughs offer "Read the steps as text"; caption regions are `aria-live="polite"`; players are fully keyboard-operable; no flashing, no motion without a user action; `prefers-reduced-motion` turns transitions into snaps or cross-fades.
- State in visuals is never shown by colour alone (colour-blind safe, readable in greyscale).
- Viewports supported: 390×844, 768×1024, 1440×900, plus a 1920×1080 smoke.
- Reader is an absolute beginner and a teenager: plain words in UI copy, no jargon in labels, every term defined on first use.
