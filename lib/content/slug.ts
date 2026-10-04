// lib/content/slug.ts — filesystem naming helpers for content/ and tests/fixtures/content/
// (layout: stages/<sN-name>/<ModuleId-slug>/; module folders are found by their `<id>-` prefix
// alone, in lib/content/course.ts).

/** The page body's file name inside a module directory. Plain MDX with no frontmatter: the title
 * lives in course.yaml, objectives and practice in module.yaml. Plain data, so the Node-run gates
 * (scripts/gates/content-check.ts) can import it too. */
export const MODULE_BODY_FILE = "module.mdx";

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "") // strip accents
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/** `s0`, "Orientation and tooling" -> `s0-orientation-and-tooling` */
export function stageDirName(stageId: string, title: string): string {
  return `${stageId}-${slugify(title)}`;
}
