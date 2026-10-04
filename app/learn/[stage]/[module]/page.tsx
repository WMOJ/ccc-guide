// app/learn/[stage]/[module]/page.tsx — the module page: one module, read top to bottom, with its
// practice list at the end (brief §7 thin wiring).
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ModulePage } from "@/components/layout";
import { getAllModuleRouteParams, getModule } from "@/lib/content/course";
import { getModulePageData } from "@/lib/content/module-page";
import { plainTitle } from "@/lib/content/title";

export const dynamicParams = false;

export function generateStaticParams() {
  return getAllModuleRouteParams();
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ stage: string; module: string }>;
}): Promise<Metadata> {
  const { stage, module } = await params;
  const m = getModule(stage, module);
  return m ? { title: `${plainTitle(m.title)} · ${m.id}` } : {};
}

export default async function Page({
  params,
}: {
  params: Promise<{ stage: string; module: string }>;
}) {
  const { stage, module } = await params;
  const data = await getModulePageData(stage, module);
  if (!data) notFound();
  return <ModulePage {...data} />;
}
