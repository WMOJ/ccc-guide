// lib/content/pages.tsx — /start and /about prose (plan §4.10). The copy lives in
// content/ui/strings.yaml (startPage, aboutPage) with the rest of the UI copy, so G-STYLE checks it;
// this file only turns it into headed sections. Rules for that copy: no local system/environment
// setup content (C21), no score targets or CCO/medal wording (R14), no walkthroughs or
// per-problem hints (C20).
import { Fragment } from "react";
import { getUiStrings, type UiStrings } from "./strings";
import type { ProsePageProps } from "./types";

type ProsePageStrings = UiStrings["startPage"];

function toProsePage({ title, lede, sections }: ProsePageStrings): ProsePageProps {
  const body = (
    <>
      {sections.map((s) => (
        <Fragment key={s.heading}>
          <h2>{s.heading}</h2>
          {s.paragraphs.map((p) => (
            <p key={p}>{p}</p>
          ))}
        </Fragment>
      ))}
    </>
  );
  return { title, lede, body };
}

export function getStartPageContent(): ProsePageProps {
  return toProsePage(getUiStrings().startPage);
}

export function getAboutPageContent(): ProsePageProps {
  return toProsePage(getUiStrings().aboutPage);
}
