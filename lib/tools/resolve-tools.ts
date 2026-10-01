// lib/tools/resolve-tools.ts — resolves the external tools the authoring-time gates need
// (PyPy 3.8, ruff, vermin), plain from the environment: an explicit env var first, then PATH.
// Nothing here is downloaded, pinned, or redirected into a project-local sandbox — install these
// normally (see README.md) and they just work, the same as any other repo.

import { execFileSync } from "node:child_process";

function which(name: string): string | null {
  try {
    const found = execFileSync("command", ["-v", name], {
      shell: "/bin/sh",
      encoding: "utf8",
    }).trim();
    return found || null;
  } catch {
    return null;
  }
}

function firstOnPath(names: string[]): string | null {
  for (const name of names) {
    const found = which(name);
    if (found) return found;
  }
  return null;
}

/**
 * Resolves PyPy 3.8: the `PYPY38` env var if set, else `pypy3.8` / `pypy3` / `pypy` on PATH.
 * Verifies the resolved binary really is Python 3.8.x (PyPy also ships 3.9/3.10 builds that would
 * otherwise silently pass). Throws with an install hint if nothing suitable is found.
 */
export function resolvePypy38(): string {
  const candidate = process.env.PYPY38 || firstOnPath(["pypy3.8", "pypy3", "pypy"]);
  if (!candidate) {
    throw new Error(
      "PyPy 3.8 not found. Set PYPY38=/path/to/pypy3.8, or install it and put it on PATH " +
        "(e.g. `uv python install pypy3.8`, or download from https://pypy.org/download.html — pick " +
        "the 3.8 line, since PyPy also ships 3.9/3.10 builds; see the tool-setup skill).",
    );
  }
  const version = execFileSync(candidate, ["-c", "import sys; print(sys.version)"], {
    encoding: "utf8",
  });
  if (!/\b3\.8\.\d+\b/.test(version)) {
    throw new Error(
      `${candidate} is not Python 3.8.x (reported: ${version.trim()}). The CCC grader runs PyPy 3.8; ` +
        "set PYPY38 to a 3.8 interpreter explicitly.",
    );
  }
  return candidate;
}

/** True if a usable PyPy 3.8 is available, without throwing — for tests that skip instead of failing. */
export function hasPypy38(): boolean {
  try {
    resolvePypy38();
    return true;
  } catch {
    return false;
  }
}

/** Like resolvePypy38, but returns "" instead of throwing — for optional, best-effort checks. */
export function resolvePypy38Quiet(): string {
  try {
    return resolvePypy38();
  } catch {
    return "";
  }
}

/** Resolves `ruff`: the `RUFF` env var if set, else `ruff` on PATH. Pinned version: see README.md. */
export function resolveRuff(): string {
  const candidate = process.env.RUFF || which("ruff");
  if (!candidate) {
    throw new Error(
      "ruff not found. Set RUFF=/path/to/ruff, or install it (pipx install ruff / pip install ruff) " +
        "and put it on PATH. See README.md for the pinned version.",
    );
  }
  return candidate;
}

/** Resolves `vermin`: the `VERMIN` env var if set, else `vermin` on PATH. Pinned version: see README.md. */
export function resolveVermin(): string {
  const candidate = process.env.VERMIN || which("vermin");
  if (!candidate) {
    throw new Error(
      "vermin not found. Set VERMIN=/path/to/vermin, or install it (pipx install vermin / pip install " +
        "vermin) and put it on PATH. See README.md for the pinned version.",
    );
  }
  return candidate;
}

/** True if `ruff` is resolvable, without throwing — for tests that skip instead of failing. */
export function hasRuff(): boolean {
  try {
    resolveRuff();
    return true;
  } catch {
    return false;
  }
}

/** True if `vermin` is resolvable, without throwing — for tests that skip instead of failing. */
export function hasVermin(): boolean {
  try {
    resolveVermin();
    return true;
  } catch {
    return false;
  }
}
