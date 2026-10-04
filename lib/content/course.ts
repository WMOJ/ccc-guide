// lib/content/course.ts — the course structure loader.
//
// Reads content/course.yaml. For every module, checks whether it has been authored on disk: a directory named `<id>-…` under
// stages/<stageDir>/ holding module.yaml (status, objectives, practice) and module.mdx (the page
// body). A module is readable only when its status is visible in this build and module.mdx
// exists; anything else renders as "Coming soon" with no link.
import fs from "node:fs";
import path from "node:path";
import { parse } from "yaml";
import { visibleStatuses } from "./env";
import { type CourseStageEntry, courseSchema, moduleFileSchema } from "./schemas";
import { MODULE_BODY_FILE, stageDirName } from "./slug";
import type { ModuleLink, ModuleNavLink, ModuleStatus, StageLink } from "./types";

const CONTENT_ROOT = path.join(process.cwd(), "content");

function readCourseYaml(): CourseStageEntry[] {
  const file = path.join(CONTENT_ROOT, "course.yaml");
  if (!fs.existsSync(file)) return [];
  const raw = fs.readFileSync(file, "utf8");
  const data = courseSchema.parse(parse(raw));
  return data.stages;
}

/** The module's directory: the folder under its stage whose name starts with `<id>-` and holds a
 * module.yaml. Only the id prefix matters, so a course.yaml title can change without renaming the
 * folder. */
function findModuleDir(stageId: string, stageTitle: string, moduleId: string): string | null {
  const stageDir = path.join(CONTENT_ROOT, "stages", stageDirName(stageId, stageTitle));
  if (!fs.existsSync(stageDir)) return null;
  for (const entry of fs.readdirSync(stageDir, { withFileTypes: true })) {
    if (entry.isDirectory() && entry.name.startsWith(`${moduleId}-`)) {
      const dir = path.join(stageDir, entry.name);
      if (fs.existsSync(path.join(dir, "module.yaml"))) return dir;
    }
  }
  return null;
}

function buildModuleLink(
  stageId: string,
  stageTitle: string,
  entry: { id: string; title: string; status: ModuleStatus },
): ModuleLink {
  const dir = findModuleDir(stageId, stageTitle, entry.id);
  // An authored module's own module.yaml status is the working status (authors move it through
  // drafted -> gated -> reviewed); course.yaml's copy only matters for unauthored modules.
  // content:check (G-SCHEMA) keeps the two in agreement wherever "accepted" is involved.
  let status: ModuleStatus = entry.status;
  let hasBody = false;
  if (dir) {
    const moduleYamlPath = path.join(dir, "module.yaml");
    status = moduleFileSchema.parse(parse(fs.readFileSync(moduleYamlPath, "utf8"))).status;
    hasBody = fs.existsSync(path.join(dir, MODULE_BODY_FILE));
  }

  const visible = visibleStatuses().includes(status);
  const href = visible && hasBody ? `/learn/${stageId}/${encodeURIComponent(entry.id)}` : null;

  return { id: entry.id, title: entry.title, href, status };
}

export function getCourse(): { stages: StageLink[] } {
  const stages: StageLink[] = readCourseYaml().map((entry) => ({
    id: entry.id,
    number: entry.number,
    title: entry.title,
    goal: entry.goal,
    href: `/learn#stage-${entry.id}`,
    modules: entry.modules.map((m) => buildModuleLink(entry.id, entry.title, m)),
  }));
  return { stages };
}

export function getStage(stageId: string): StageLink | null {
  return getCourse().stages.find((s) => s.id === stageId) ?? null;
}

export function getModule(stageId: string, moduleId: string): ModuleLink | null {
  const stage = getStage(stageId);
  return stage?.modules.find((m) => m.id === moduleId) ?? null;
}

/** A module's objectives and raw practice-list ids, read from its module.yaml (empty when unauthored). */
export function getModuleAuthoredData(
  stageId: string,
  moduleId: string,
): {
  objectives: string[];
  practice: { id: string; note?: string; why?: string }[];
  dir: string | null;
} {
  for (const entry of readCourseYaml()) {
    if (entry.id !== stageId) continue;
    const moduleEntry = entry.modules.find((m) => m.id === moduleId);
    if (!moduleEntry) continue;
    const dir = findModuleDir(stageId, entry.title, moduleId);
    if (!dir) return { objectives: [], practice: [], dir: null };
    const moduleData = moduleFileSchema.parse(
      parse(fs.readFileSync(path.join(dir, "module.yaml"), "utf8")),
    );
    return {
      objectives: moduleData.objectives,
      practice: moduleData.practice,
      dir,
    };
  }
  return { objectives: [], practice: [], dir: null };
}

/** Every readable `[stage]/[module]` pair (for generateStaticParams). */
export function getAllModuleRouteParams(): { stage: string; module: string }[] {
  const out: { stage: string; module: string }[] = [];
  for (const stage of getCourse().stages) {
    for (const m of stage.modules) {
      if (m.href) out.push({ stage: stage.id, module: m.id });
    }
  }
  return out;
}

/** Every readable module, in course order across stages (prev/next and the home page's
 * "Continue where you left off"). */
export function getModuleOrder(): ModuleNavLink[] {
  const out: ModuleNavLink[] = [];
  for (const stage of getCourse().stages) {
    for (const m of stage.modules) {
      if (m.href) out.push({ id: m.id, title: m.title, href: m.href });
    }
  }
  return out;
}
