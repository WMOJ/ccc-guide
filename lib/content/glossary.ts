// lib/content/glossary.ts — loads content/glossary.yaml (+ the fixture's, non-production) into
// GlossaryTermView[].
import fs from "node:fs";
import path from "node:path";
import { parse } from "yaml";
import { getCourse } from "./course";
import { getBuildEnv } from "./env";
import { glossarySchema } from "./schemas";
import type { GlossaryTermView } from "./types";

type GlossaryTermEntry = ReturnType<typeof glossarySchema.parse>["terms"][number];

const REAL_FILE = path.join(process.cwd(), "content", "glossary.yaml");
const FIXTURE_FILE = path.join(process.cwd(), "tests", "fixtures", "content", "glossary.yaml");

function readTerms(file: string): GlossaryTermEntry[] {
  if (!fs.existsSync(file)) return [];
  return glossarySchema.parse(parse(fs.readFileSync(file, "utf8"))).terms;
}

let cached: GlossaryTermView[] | null = null;

export function getGlossaryTerms(): GlossaryTermView[] {
  if (cached) return cached;
  const terms = [...readTerms(REAL_FILE)];
  if (getBuildEnv() !== "production") terms.push(...readTerms(FIXTURE_FILE));
  cached = terms
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
 * `<moduleId>/<lessonSlug>` → the lesson that introduces a term. Links to the lesson when it is
 * readable in this build; otherwise names the module without a link.
 */
function resolveIntroducedIn(lessonId: string): GlossaryTermView["introducedIn"] {
  const moduleId = lessonId.split("/")[0] ?? "";
  for (const stage of getCourse().stages) {
    const m = stage.modules.find((mm) => mm.id === moduleId);
    if (!m) continue;
    const lesson = m.href ? m.lessons.find((l) => l.id === lessonId) : undefined;
    return lesson
      ? { lessonId, moduleId, title: lesson.title, href: lesson.href }
      : { lessonId, moduleId, title: m.title, href: null };
  }
  return undefined;
}
