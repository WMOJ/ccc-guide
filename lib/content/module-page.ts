// lib/content/module-page.ts — assembles one module page's full data: the compiled module.mdx
// body, reading time, table of contents, objectives, the resolved practice list (rendered after
// the body), and prev/next navigation across every readable module in course order.
import { getCourse, getModuleAuthoredData, getModuleOrder } from "./course";
import { compileModule } from "./mdx";
import { readingMinutes } from "./reading-time";
import { resolvePracticeItem } from "./registry";
import { extractToc } from "./toc";
import type { ModulePageProps } from "./types";

export async function getModulePageData(
  stageId: string,
  moduleId: string,
): Promise<ModulePageProps | null> {
  const { stages } = getCourse();
  const stage = stages.find((s) => s.id === stageId);
  const moduleLink = stage?.modules.find((m) => m.id === moduleId);
  if (!stage || !moduleLink?.href) return null;

  const { objectives, practice: rawPractice, dir } = getModuleAuthoredData(stageId, moduleId);
  if (!dir) return null;

  const practice = rawPractice.map((p) => resolvePracticeItem(p.id, { note: p.note, why: p.why }));
  const { body, raw: rawMdx } = await compileModule(dir);

  const order = getModuleOrder();
  const index = order.findIndex((m) => m.id === moduleId);

  return {
    module: {
      ...moduleLink,
      objectives,
      readingMinutes: readingMinutes(rawMdx),
      toc: extractToc(rawMdx),
      body,
    },
    stage,
    practice,
    nav: {
      prev: index > 0 ? (order[index - 1] ?? null) : null,
      next: index >= 0 ? (order[index + 1] ?? null) : null,
    },
    courseNav: { stages, currentStageId: stageId, currentModuleId: moduleId },
  };
}
