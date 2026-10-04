// lib/content/title.ts — course.yaml titles may name Python code in backticks
// ("Values, types, variables and `print`"). components/ui/RichTitle.tsx renders those spans as
// inline code; plainTitle is the same title for places that only take text.

/** The title as plain text, for attributes, labels, `<title>` and the search index. */
export function plainTitle(text: string): string {
  return text.replace(/`([^`]+)`/g, "$1");
}
