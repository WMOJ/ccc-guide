"use client";

import { useReadState } from "@/lib/read-state";
import { RichTitle } from "./RichTitle";

export interface ContinueModule {
  id: string;
  title: string;
  href: string;
}

export interface ContinueBlockProps {
  /** Every readable module in course order. */
  modules: ContinueModule[];
  labels: { continueLabel: string; startLabel: string };
}

/** The folded tape flag: where you stopped (ui-design skill → Continue where you left off). */
function Flag() {
  return (
    <svg aria-hidden="true" viewBox="0 0 20 20" width={20} height={20} className="shrink-0">
      <path d="M5 2.75v14.5" stroke="var(--color-ink)" strokeWidth={1.5} strokeLinecap="round" />
      <path
        d="M5.75 3.25h9.5l-2.5 3.5 2.5 3.5h-9.5z"
        fill="var(--color-check)"
        stroke="var(--color-ink)"
        strokeWidth={1.5}
        strokeLinejoin="round"
      />
    </svg>
  );
}

/**
 * "Continue where you left off": the next unread module after the most recently read one. The
 * server renders the start state; the client swaps text inside a fixed-height block.
 */
export function ContinueBlock({ modules, labels }: ContinueBlockProps) {
  const rs = useReadState();
  let target: ContinueModule | undefined = modules[0];
  let resumed = false;
  if (rs.ready) {
    const map = rs.all();
    let latest = -1;
    let latestAt = "";
    modules.forEach((m, i) => {
      const at = Object.hasOwn(map, m.id) ? map[m.id] : undefined;
      if (at && at >= latestAt) {
        latestAt = at;
        latest = i;
      }
    });
    if (latest >= 0) {
      resumed = true;
      target =
        modules.slice(latest + 1).find((m) => !Object.hasOwn(map, m.id)) ??
        modules.find((m) => !Object.hasOwn(map, m.id)) ??
        modules[latest];
    }
  }
  if (!target) return null;
  return (
    <div className="flex min-h-[5.5rem] items-center gap-4 border border-rule bg-paper-sunk px-5 py-4">
      <Flag />
      <div className="min-w-0">
        <p className="text-ink-2 text-small">
          {resumed ? labels.continueLabel : labels.startLabel}
        </p>
        <a
          href={target.href}
          className="group mt-0.5 flex flex-wrap items-baseline gap-x-2 text-ui"
        >
          <span className="text-ink-3 text-small tnum">{target.id}</span>
          <span className="font-bold text-blueline underline decoration-1 underline-offset-[0.2em] group-hover:text-blueline-deep group-hover:decoration-2">
            <RichTitle text={target.title} />
          </span>
        </a>
      </div>
    </div>
  );
}
