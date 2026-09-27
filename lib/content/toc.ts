// lib/content/toc.ts — a lesson's on-page table of contents: every level-2 heading (the lesson
// title itself is level-1; objectives, then sections that each introduce one idea).
// Ids come from github-slugger, the same slugger rehype-slug uses for the rendered heading ids, so
// TOC links always match (apostrophes, "I/O" and `bisect_left` in headings broke anchors before).
import GithubSlugger from "github-slugger";
import type { TocItem } from "./types";

export function extractToc(mdxBody: string): TocItem[] {
  const items: TocItem[] = [];
  const slugger = new GithubSlugger();
  for (const line of mdxBody.split("\n")) {
    const m = line.match(/^##\s+(.+?)\s*$/);
    if (!m?.[1]) continue;
    // Drop Markdown markers (inline-code backticks, emphasis) but keep underscores inside names.
    const text = m[1].replace(/`/g, "").replace(/\*+|(^|\s)_+|_+(\s|$)/g, "$1$2");
    items.push({ id: slugger.slug(text), text });
  }
  return items;
}
