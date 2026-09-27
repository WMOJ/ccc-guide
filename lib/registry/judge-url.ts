// lib/registry/judge-url.ts — the ONLY place in the app that builds a judge URL.
// No other file may embed a wmoj.ca or dmoj.ca URL (G-LINK-FMT, and a grep lint for
// raw judge domains outside this file, tools/lint/no-raw-judge-urls.mjs).
//
// - 2021-2026 -> WMOJ: https://wmoj.ca/problems/<slug> (plural, no trailing slash)
// - 2014-2020 -> DMOJ: https://dmoj.ca/problem/<slug>/ (singular, trailing slash)
// - Any year outside 2014-2026 -> throws. This is not a placeholder: 2026 is the final year the
//   app will ever link.

export type Judge = "wmoj" | "dmoj";

export const CCC_MIN_YEAR = 2014;
export const CCC_MAX_YEAR = 2026;
const WMOJ_MIN_YEAR = 2021;

export function judgeForYear(year: number): Judge {
  if (!Number.isInteger(year) || year < CCC_MIN_YEAR || year > CCC_MAX_YEAR) {
    throw new RangeError(
      `judgeForYear: year ${year} is outside the supported CCC range ${CCC_MIN_YEAR}-${CCC_MAX_YEAR} (this is a permanent limit, not a placeholder).`,
    );
  }
  return year >= WMOJ_MIN_YEAR ? "wmoj" : "dmoj";
}

/** Builds the judge URL for a registry problem slug. The only function allowed to do this. */
export function judgeUrl(slug: string, year: number): string {
  const judge = judgeForYear(year);
  if (judge === "wmoj") {
    return `https://wmoj.ca/problems/${slug}`;
  }
  return `https://dmoj.ca/problem/${slug}/`;
}

// Judge home/sign-up URLs deliberately do NOT live here: they go through <JudgeLink> and
// content/registry/external-links.yaml (ids "wmoj-home", "wmoj-signup", "dmoj-home",
// "dmoj-signup") via lib/content/registry.ts's getExternalLink() — one source, so fixing a
// broken URL never means finding a second copy. This file only ever builds a *problem* URL.

/** Derives a slug from level/number/year: `ccc<YY><j|s><N>`, e.g. ccc23s1. */
export function deriveSlug(year: number, level: "J" | "S", number: number): string {
  const yy = String(year % 100).padStart(2, "0");
  return `ccc${yy}${level.toLowerCase()}${number}`;
}
