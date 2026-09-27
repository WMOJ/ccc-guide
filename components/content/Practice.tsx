import { ArrowUpRight } from "lucide-react";
import type { PracticeItemView } from "@/components/layout/props";
import { JudgeBadge } from "@/components/ui/Badge";
import { RichText } from "@/components/ui/RichText";
import { fmt, ui } from "@/components/ui/ui-strings";
import { judgeName, problemLabel } from "./problem-label";

/**
 * A module's practice list (plan §4.6.4, DESIGN.md → Practice list). No status, checkboxes,
 * scores or hints. Renders nothing when the list is empty.
 */
export function Practice({
  items,
  headingId = "practice",
}: {
  items: PracticeItemView[];
  headingId?: string;
}) {
  if (items.length === 0) return null;
  // Worded by count and by the judges actually listed (P6-D34).
  function practiceIntro(list: PracticeItemView[]): string {
    const judges = [...new Set(list.map((i) => i.problem.judge))];
    const [first] = judges;
    const only = judges.length === 1 && first ? judgeName(first) : null;
    if (list.length === 1 && only) return fmt(s.introOne, { judge: only });
    if (only) return fmt(s.introOneJudge, { judge: only });
    return s.introBothJudges;
  }
  const s = ui().practice;
  return (
    <section data-exhibit="" data-ui="" aria-labelledby={headingId}>
      <h2
        id={headingId}
        className="font-bold text-headline text-ink leading-(--text-headline--line-height) tracking-(--text-headline--letter-spacing)"
      >
        {s.heading}
      </h2>
      <p className="mt-2 text-ink-2 text-small">{practiceIntro(items)}</p>
      <ol className="mt-4 border-rule border-t">
        {items.map(({ problem: p, note, why }) => (
          <li
            key={`${p.id}-${p.level}${p.number}`}
            className="grid grid-cols-1 gap-x-4 gap-y-1 border-rule border-b px-2 py-3 sm:grid-cols-[5.5rem_minmax(0,1fr)]"
          >
            <span className="pt-px font-semibold text-ink text-ui tnum">{problemLabel(p)}</span>
            <div className="min-w-0 text-ui">
              <a
                href={p.url}
                target="_blank"
                rel="noopener noreferrer"
                data-plain=""
                className="font-semibold text-blueline underline decoration-1 underline-offset-[0.2em] hover:text-blueline-deep hover:decoration-2"
              >
                {p.title}
                <span className="sr-only"> {fmt(s.opensOn, { judge: judgeName(p.judge) })}</span>
              </a>{" "}
              <span className="inline-flex items-center gap-0.5 whitespace-nowrap align-baseline">
                <JudgeBadge judge={p.judge} />
                <ArrowUpRight aria-hidden="true" size={14} strokeWidth={2} className="text-ink-3" />
              </span>
              {p.sameAs ? (
                <span className="ml-1.5 whitespace-nowrap text-ink-2 text-small">
                  {fmt(s.sameAs, { label: problemLabel(p.sameAs) })}
                </span>
              ) : null}
              {note ? (
                <p className="mt-1 text-ink-2 text-small">
                  <RichText text={note} />
                </p>
              ) : null}
              {why ? (
                <p className="mt-0.5 text-ink-3 text-small">
                  <span className="font-semibold">{s.why}</span> <RichText text={why} />
                </p>
              ) : null}
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
