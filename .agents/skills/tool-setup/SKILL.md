---
name: tool-setup
description: Check for and install the external tools this repo's gates need (Playwright's Chromium, PyPy 3.8, ruff, vermin) — normal, system-wide installs, nothing confined to the repo. Load before running verify:fast/verify:full for the first time on a machine, or when a gate reports a missing tool.
---

# Tool setup

Everything here is a normal, user-level install on the developer's machine — nothing is
downloaded into the repo, sandboxed, or redirected. Check first; install only what's missing.

## Playwright + Chromium

Needed for `viz:shots` (G-VIZ-SHOTS). Check: `npx playwright --version` should print **1.63.0**
(the pinned `playwright` version in `package.json`).

Install (after `npm ci`, so the pinned `playwright` is present):

```bash
npx playwright install chromium
```

This downloads into Playwright's default user cache (`~/Library/Caches/ms-playwright` on macOS) —
do not set `PLAYWRIGHT_BROWSERS_PATH`. If your shell already exports it (or `RUFF_CACHE_DIR`)
pointing somewhere else, run the gates with `env -u PLAYWRIGHT_BROWSERS_PATH -u RUFF_CACHE_DIR`.

## PyPy 3.8

Needed for `check:python` (G-PY-38/G-PY-RUN), `gen:outputs`, `gen:viz`, `check:viz`, the G-PREREQ
part of `content:check`. Pinned to **PyPy 3.8 v7.3.11**
(Python 3.8.16) — any PyPy build of the 3.8.x line works; PyPy also ships 3.9/3.10 builds, which do
not.

Check: `pypy3.8 --version` (or `$PYPY38 --version`) must print `Python 3.8.x` somewhere in its
output.

Install, a normal user-level install, whichever is easiest on the machine:

- With `uv` (works on macOS arm64, where Homebrew has no 3.8 formula):
  `uv python install pypy-3.8.16-macos-aarch64-none` (pick the matching platform from
  `uv python list --all-versions | grep pypy-3.8`). uv links it as `~/.local/bin/pypy3.8`.
- Otherwise, the official tarball for the 3.8 line from https://pypy.org/download.html, unpacked
  anywhere under the user's home (for example `~/.local/pypy3.8/`).

Then either put its `bin/` on `PATH` as `pypy3.8`, or export `PYPY38=/path/to/pypy3.8/bin/pypy3.8`
(`lib/tools/resolve-tools.ts` checks this env var first, then `pypy3.8`/`pypy3`/`pypy` on `PATH`).

## ruff and vermin

Pinned to **ruff 0.16.8** and **vermin 1.8.0**. Install isolated, via `uv tool` or pipx (both
put the executables in `~/.local/bin`), or `pip install --user`:

```bash
uv tool install ruff==0.16.8 && uv tool install vermin==1.8.0
# or: pipx install ruff==0.16.8 && pipx install vermin==1.8.0
# or: pip install --user ruff==0.16.8 vermin==1.8.0
```

Check: `ruff --version` prints `ruff 0.16.8`; `vermin --version` prints `vermin 1.8.0`. Both
resolve from `RUFF`/`VERMIN` env vars first, else `PATH` (same `lib/tools/resolve-tools.ts`).

## git and gh

Whatever is already on the machine, already logged in as the developer normally is. Nothing
special to install or configure.
