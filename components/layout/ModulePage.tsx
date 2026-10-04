import "katex/dist/katex.min.css";
import { Practice } from "@/components/content/Practice";
import type { ModulePageProps } from "@/components/layout/props";
import { DraftBadge } from "@/components/ui/Badge";
import { RichText } from "@/components/ui/RichText";
import { RichTitle } from "@/components/ui/RichTitle";
import { fmt, ui } from "@/components/ui/ui-strings";
import { isDraftStatus } from "@/lib/content/env";
import { Breadcrumb } from "./Breadcrumb";
import { ClosingTitleBlock } from "./ClosingTitleBlock";
import { OnThisPage } from "./OnThisPage";
import { SiteFrame } from "./SiteFrame";
import { TitleBlockStrip } from "./TitleBlock";
import { h1Class, minorClass } from "./type-styles";

/** The module page: one module, read top to bottom, practice at the end (DESIGN.md → Layout →
 * Reading page order). */
export function ModulePage({ module, stage, practice, nav, courseNav }: ModulePageProps) {
  const s = ui();
  return (
    <SiteFrame current="learn" courseNav={courseNav}>
      <div className="flex gap-12">
        <article className="min-w-0 flex-1">
          <Breadcrumb
            items={[
              { label: s.nav.courseMap, href: "/learn" },
              {
                label: `${fmt(s.nav.stage, { n: stage.number })}: ${stage.title}`,
                href: stage.href,
              },
            ]}
          />
          <header className="mt-4 max-w-(--measure)">
            <h1 className={h1Class}>
              <RichTitle text={module.title} />
            </h1>
            <TitleBlockStrip
              cells={[
                { label: s.module.stage, value: stage.number },
                { label: s.module.module, value: module.id },
                {
                  label: s.module.readingTime,
                  value: fmt(s.module.minutes, { n: module.readingMinutes }),
                },
              ]}
              extra={
                isDraftStatus(module.status) ? <DraftBadge label={s.status.draft} /> : undefined
              }
            />
          </header>
          {module.objectives.length > 0 ? (
            <section aria-labelledby="objectives" className="mt-8 max-w-(--measure)">
              <h2 id="objectives" className={minorClass}>
                {s.module.objectives}
              </h2>
              <ul className="mt-2 list-disc space-y-1 pl-6 text-body leading-(--text-body--line-height) marker:text-ink-3">
                {module.objectives.map((o) => (
                  <li key={o}>
                    <RichText text={o} />
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
          <div className="prose-sheet mt-10">{module.body}</div>
          {practice.length > 0 ? (
            <div className="mt-12 max-w-(--measure)">
              <Practice items={practice} />
            </div>
          ) : null}
          <ClosingTitleBlock moduleId={module.id} nav={nav} />
        </article>
        <OnThisPage items={module.toc} />
      </div>
    </SiteFrame>
  );
}
