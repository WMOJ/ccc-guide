// validateVisualText(text, kind): Zod validation of one visual data file's contents, used by the
// runtime loader (components/viz/load.ts). No JSX, no Next imports.
import path from "node:path";
import { parse as parseYaml } from "yaml";
import type { ZodType } from "zod";
import { framesFileSchema, traceFileSchema, traceYamlSchema, vizYamlSchema } from "./schema";

export type VisualFileKind = "frames" | "trace" | "viz-yaml" | "trace-yaml";

export type VisualValidation =
  | { ok: true; kind: VisualFileKind; path: string; data: unknown }
  | { ok: false; kind: VisualFileKind | null; path: string; errors: string[] };

const SCHEMAS: Record<VisualFileKind, ZodType> = {
  frames: framesFileSchema,
  trace: traceFileSchema,
  "viz-yaml": vizYamlSchema,
  "trace-yaml": traceYamlSchema,
};

/** Validate text as the given kind (used by the runtime loader). */
export function validateVisualText(
  text: string,
  kind: VisualFileKind,
  file = "<text>",
): VisualValidation {
  let raw: unknown;
  try {
    raw = kind === "frames" || kind === "trace" ? JSON.parse(text) : parseYaml(text);
  } catch (err) {
    return { ok: false, kind, path: file, errors: [`cannot parse: ${(err as Error).message}`] };
  }
  const result = SCHEMAS[kind].safeParse(raw);
  if (!result.success) {
    return {
      ok: false,
      kind,
      path: file,
      errors: result.error.issues.map((i) => `${i.path.join(".") || "(root)"}: ${i.message}`),
    };
  }
  const errors: string[] = [];
  if (kind === "frames" || kind === "trace") {
    const stem = path.basename(file).replace(/\.(frames|trace)\.json$/, "");
    const id = (result.data as { id: string }).id;
    if (file !== "<text>" && id !== stem)
      errors.push(`id "${id}" must equal the file name "${stem}"`);
  }
  if (errors.length > 0) return { ok: false, kind, path: file, errors };
  return { ok: true, kind, path: file, data: result.data };
}
