"use client";

import { useReadState } from "@/lib/read-state";
import { ReadCell } from "./ReadCell";

/** A read cell bound to read state (sidebar, course map). Server render: unread. */
export function LiveReadCell({ moduleId, readLabel }: { moduleId: string; readLabel: string }) {
  const rs = useReadState();
  const read = rs.ready && rs.isRead(moduleId);
  return (
    <>
      <ReadCell read={read} />
      {read ? <span className="sr-only">{readLabel}</span> : null}
    </>
  );
}
