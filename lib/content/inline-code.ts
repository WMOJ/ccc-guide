// lib/content/inline-code.ts — one rule for every inline code span (lesson prose, RichText strings,
// visual captions). A short span never wraps, so "-3" or "% 5" never splits into two pills.
// A long span (a whole error line such as "NameError: name 'shiping' is not defined")
// may wrap at its spaces, or it pushes a 390 px page sideways.

/** Spans longer than this many characters may wrap; shorter ones never split. */
export const LONG_INLINE_CODE = 24;

export function isLongInlineCode(text: string): boolean {
  return text.length > LONG_INLINE_CODE;
}

type MdNode = {
  type: string;
  value?: string;
  children?: MdNode[];
  data?: { hProperties?: Record<string, unknown> };
};

function walk(node: MdNode): void {
  if (node.type === "inlineCode" && node.value !== undefined && isLongInlineCode(node.value)) {
    node.data = {
      ...node.data,
      hProperties: { ...node.data?.hProperties, className: "code-long" },
    };
  }
  for (const child of node.children ?? []) walk(child);
}

/** Marks long inline code in lesson prose with `class="code-long"` (see globals.css). */
export function remarkLongInlineCode() {
  return (tree: MdNode) => {
    walk(tree);
  };
}
