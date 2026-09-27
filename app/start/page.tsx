// app/start/page.tsx — how the course and practice work.
import type { Metadata } from "next";
import { StartPage } from "@/components/layout";
import { ui } from "@/components/ui/ui-strings";
import { getStartPageContent } from "@/lib/content/pages";

export const metadata: Metadata = { title: ui().startPage.title };

export default function Page() {
  return <StartPage {...getStartPageContent()} />;
}
