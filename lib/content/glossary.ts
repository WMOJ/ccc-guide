// lib/content/glossary.ts — loads content/glossary.yaml into GlossaryTermView[].
import fs from "node:fs";
import path from "node:path";
import { parse } from "yaml";
import { getCourse } from "./course";
import { glossarySchema } from "./schemas";
import type { GlossaryTermView } from "./types";

type GlossaryTermEntry = ReturnType<typeof glossarySchema.parse>["terms"][number];

const REAL_FILE = path.join(process.cwd(), "content", "glossary.yaml");

function readTerms(file: string): GlossaryTermEntry[] {
  if (!fs.existsSync(file)) return [];
  return glossarySchema.parse(parse(fs.readFileSync(file, "utf8"))).terms;
}

// Cached per process in production only: `next dev` re-reads the file on every call, so an edit
// to content/glossary.yaml shows up without restarting the dev server.
const CACHE = process.env.NODE_ENV === "production";
let cached: GlossaryTermView[] | null = null;

export function getGlossaryTerms(): GlossaryTermView[] {
  if (CACHE && cached) return cached;
  cached = readTerms(REAL_FILE)
    .map((t) => ({
      id: t.id,
      term: t.term,
      definition: t.definition,
      introducedIn: t.introducedIn ? resolveIntroducedIn(t.introducedIn) : undefined,
    }))
    .sort((a, b) => a.term.localeCompare(b.term));
  return cached;
}

export function getGlossaryTerm(id: string): GlossaryTermView | null {
  return getGlossaryTerms().find((t) => t.id === id) ?? null;
}

/**
 * A module id → the module that introduces a term. Links to the module when it is readable in
 * this build; otherwise names it without a link.
 */
function resolveIntroducedIn(moduleId: string): GlossaryTermView["introducedIn"] {
  for (const stage of getCourse().stages) {
    const m = stage.modules.find((mm) => mm.id === moduleId);
    if (m) return { moduleId, title: m.title, href: m.href };
  }
  return undefined;
}
