import { isLongInlineCode } from "@/lib/content/inline-code";
import { captionParts } from "@/lib/viz/caption";

const codeClass = (code: string) =>
  isLongInlineCode(code) ? "vz-cap-code vz-cap-code-long" : "vz-cap-code";

/** A step caption with its `code` spans in Mono. React escapes the text; nothing else is parsed. */
export function CaptionText({ text }: { text: string }) {
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
