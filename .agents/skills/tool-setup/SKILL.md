---
name: tool-setup
description: Check for and install PyPy 3.8, which gen:outputs and gen:viz need — a normal, system-wide install, nothing confined to the repo. Load before running a generator for the first time on a machine, or when one reports PyPy missing.
---

# Tool setup

Everything here is a normal, user-level install on the developer's machine — nothing is
downloaded into the repo, sandboxed, or redirected. Check first; install only what's missing.

## PyPy 3.8

Needed for `gen:outputs` and `gen:viz`. Pinned to **PyPy 3.8 v7.3.11** (Python 3.8.16) — any PyPy build of the 3.8.x line works; PyPy also ships 3.9/3.10 builds, which do
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

## git and gh

Whatever is already on the machine, already logged in as the developer normally is. Nothing
special to install or configure.
