// app/about/page.tsx — credits and attribution.
import type { Metadata } from "next";
import { AboutPage } from "@/components/layout";
import { ui } from "@/components/ui/ui-strings";
import { getAboutPageContent } from "@/lib/content/pages";

export const metadata: Metadata = { title: ui().aboutPage.title };

export default function Page() {
  return <AboutPage {...getAboutPageContent()} />;
}
