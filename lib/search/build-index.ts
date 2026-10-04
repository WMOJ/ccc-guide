// lib/search/build-index.ts — builds the static search index entries: every
// readable module, every glossary term, every registry problem. Server-only (reads content from
// disk via lib/content). Consumed by app/search-index.json/route.ts at build time.
import { getCourse, getModuleAuthoredData } from "../content/course";
import { getGlossaryTerms } from "../content/glossary";
import { getAllProblems } from "../content/registry";
import { plainTitle } from "../content/title";

export interface SearchIndexEntry {
  kind: "module" | "term" | "problem";
  id: string;
  title: string;
  label: string;
  snippet?: string;
  /** Downloaded and indexed but never shown or stored on results: a module's objectives, so a
   * name that only appears there (e.g. "coordinate compression") still finds the module. */
  keywords?: string;
  href: string;
}

export function buildSearchIndex(): SearchIndexEntry[] {
  const entries: SearchIndexEntry[] = [];

  for (const stage of getCourse().stages) {
    for (const m of stage.modules) {
      if (!m.href) continue;
      const { objectives } = getModuleAuthoredData(stage.id, m.id);
      entries.push({
        kind: "module",
        id: m.id,
        title: plainTitle(m.title),
        label: m.id,
        keywords: objectives.length > 0 ? plainTitle(objectives.join(" ")) : undefined,
        href: m.href,
      });
    }
  }

  for (const term of getGlossaryTerms()) {
    entries.push({
      kind: "term",
      id: term.id,
      title: term.term,
      label: term.term.charAt(0).toUpperCase(),
      snippet: typeof term.definition === "string" ? term.definition : undefined,
      href: `/glossary#${term.id}`,
    });
  }

  for (const problem of getAllProblems()) {
    entries.push({
      kind: "problem",
      id: problem.id,
      title: problem.title,
      label: `${problem.year} ${problem.level}${problem.number}`,
      href: problem.url,
    });
  }

  return entries;
}
