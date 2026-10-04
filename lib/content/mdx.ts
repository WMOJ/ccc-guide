// lib/content/mdx.ts — compiles one module's module.mdx to a React element. Runs
// `@mdx-js/mdx` `evaluate()` in RSC with the fixed component map; unknown components fail the
// build (see lib/content/mdx-components.tsx).
import fs from "node:fs";
import path from "node:path";
import { evaluate } from "@mdx-js/mdx";
import type { ReactElement } from "react";
import * as runtime from "react/jsx-runtime";
import rehypeKatex from "rehype-katex";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { remarkFigureNumbers } from "../viz/remark-figure-numbers";
import { remarkLongInlineCode } from "./inline-code";
import { createMdxComponents } from "./mdx-components";
import { remarkFencedCode } from "./remark-fenced-code";
import { MODULE_BODY_FILE } from "./slug";

export interface CompiledModule {
  body: ReactElement;
  raw: string;
}

/** Compiles `moduleDir/module.mdx` to a rendered React element. */
export async function compileModule(moduleDir: string): Promise<CompiledModule> {
  const raw = fs.readFileSync(path.join(moduleDir, MODULE_BODY_FILE), "utf8");

  const { default: Content } = await evaluate(raw, {
    ...runtime,
    remarkPlugins: [
      remarkGfm,
      remarkMath,
      remarkFencedCode,
      remarkLongInlineCode,
      remarkFigureNumbers,
    ],
    rehypePlugins: [rehypeSlug, rehypeKatex],
  });

  const components = createMdxComponents({ moduleDir });
  const body = Content({ components }) as ReactElement;

  return { body, raw };
}
