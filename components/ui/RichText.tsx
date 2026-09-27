import type { ReactNode } from "react";
import { isLongInlineCode } from "@/lib/content/inline-code";
import { captionParts } from "@/lib/viz/caption";

const codeClass = (code: string) =>
  isLongInlineCode(code) ? "inline-code code-long" : "inline-code";

/**
 * A short content string from YAML or an MDX attribute (an objective, a glossary definition, a
 * code caption, a practice note) with its `backtick` spans rendered as inline code, styled like
 * inline code in lesson prose (`.inline-code`). React escapes the text; nothing else is parsed
 * (P6-D24: these strings used to show their backticks as literal characters).
 */
export function RichText({ text }: { text: string }): ReactNode {
  if (!text.includes("`")) return text;
  return (
    <>
      {captionParts(text).map((p, i) =>
        p.code ? (
          // biome-ignore lint/suspicious/noArrayIndexKey: parts of one fixed string
          <code key={i} className={codeClass(p.text)}>
            {p.text}
          </code>
        ) : (
          p.text
        ),
      )}
    </>
  );
}
