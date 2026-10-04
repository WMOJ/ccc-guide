// lib/content/types.ts — canonical view-model types for the presentational page components
// (brief §7 seam: W1 owns this file; W2's components/layout/props.ts re-exports from here).
// These are the shapes the content loaders in lib/content/ produce and every
// `app/**/page.tsx` passes straight through to its presentational component.
import type { ReactNode } from "react";
import type { Judge } from "../registry/judge-url";

/** Module lifecycle. */
export type ModuleStatus = "planned" | "drafted" | "gated" | "reviewed" | "accepted";

export type { Judge };

export interface ModuleLink {
  /** Map ID, e.g. `M4.3`, `C.3`; also the read-state key. */
  id: string;
  /** From course.yaml — the module's only title (page H1, course map, sidebar, search). */
  title: string;
  /** null when the module is not readable (planned/drafted, not visible in this build, or no
   * module.mdx on disk). */
  href: string | null;
  status: ModuleStatus;
}

/** A readable module as a plain link (prev/next, the home page's continue block). */
export interface ModuleNavLink {
  id: string;
  title: string;
  href: string;
}

export interface StageLink {
  /** `s0`…`s7`, `c`. */
  id: string;
  /** Display number: "0"…"7", "C". */
  number: string;
  title: string;
  /** One-line goal from course.yaml. Never score/payoff wording. */
  goal?: string;
  /** `/learn#stage-<id>`. */
  href: string;
  modules: ModuleLink[];
}

/** One registry problem as rendered anywhere (ProblemLink, Practice, /problems). */
export interface ProblemView {
  /** Registry id = judge slug, e.g. `ccc23s1`. */
  id: string;
  year: number;
  level: "J" | "S";
  number: number;
  title: string;
  judge: Judge;
  /** From judgeUrl() only. */
  url: string;
  /**
   * Set when this reference is a Junior alias of a Senior problem: renders
   * "2022 J4 (same problem as 2022 S2)". Holds the canonical (Senior) label parts.
   */
  sameAs?: { year: number; level: "J" | "S"; number: number };
  /** Modules that list this problem in their practice list (/problems "Taught in"). */
  taughtIn?: { id: string; title: string; href: string | null }[];
}

export interface PracticeItemView {
  problem: ProblemView;
  note?: string;
  /** Required for some DMOJ entries. */
  why?: string;
}

export interface TocItem {
  id: string;
  text: string;
}

export interface CourseNav {
  stages: StageLink[];
  /** Stage and module the page belongs to (sidebar expansion and current row). */
  currentStageId: string;
  currentModuleId: string;
}

export interface ModulePageProps {
  module: ModuleLink & {
    objectives: string[];
    readingMinutes: number;
    toc: TocItem[];
    /** The compiled module.mdx body. */
    body: ReactNode;
  };
  stage: StageLink;
  /** The module's practice list, rendered after the body (empty → no section). */
  practice: PracticeItemView[];
  nav: {
    /** Previous readable module in course order (crossing stages); null at the start. */
    prev: ModuleNavLink | null;
    /** Next readable module in course order; null → the closing block links the course map. */
    next: ModuleNavLink | null;
  };
  courseNav: CourseNav;
}

export interface CourseMapPageProps {
  stages: StageLink[];
}

export interface HomePageProps {
  stages: StageLink[];
  /** Every readable module in course order, so the continue block can find "next unread". */
  moduleOrder: ModuleNavLink[];
}

export interface ProblemsPageProps {
  /** Grouped by year, descending; within a year Junior then Senior, by number. */
  years: { year: number; problems: ProblemView[] }[];
}

export interface GlossaryTermView {
  id: string;
  term: string;
  /** Plain text or small rendered MDX. */
  definition: ReactNode;
  /** The module that introduces the term; href is null when it is not readable in this build. */
  introducedIn?: { moduleId: string; title: string; href: string | null };
}

export interface GlossaryPageProps {
  terms: GlossaryTermView[];
}

export interface ProsePageProps {
  /** /start and /about: compiled MDX or authored markup. */
  title: string;
  lede?: string;
  body: ReactNode;
}

// SearchPage takes no props: it reads ?q= and the static index on the client.
