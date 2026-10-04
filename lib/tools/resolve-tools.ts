// lib/tools/resolve-tools.ts — resolves PyPy 3.8, which gen:outputs and gen:viz need, plain from
// the environment: an explicit env var first, then PATH.
// Nothing here is downloaded, pinned, or redirected into a project-local sandbox — install these
// normally (see README.md) and they just work, the same as any other repo.

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

/** The first executable file called `name` on PATH (what `command -v` finds, without a shell). */
function which(name: string): string | null {
  for (const dir of (process.env.PATH ?? "").split(path.delimiter)) {
    if (!dir) continue;
    const candidate = path.join(dir, name);
    try {
      fs.accessSync(candidate, fs.constants.X_OK);
      if (fs.statSync(candidate).isFile()) return candidate;
    } catch {
      // not here, or not executable: keep looking
    }
  }
  return null;
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
