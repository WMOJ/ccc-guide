// /dev/viz: the visual gallery. Previews and local builds only; 404 in
// production through the shared dev guard.
import type { Metadata } from "next";
import { VizGallery } from "@/components/viz/gallery/VizGallery";
import { notFoundOutsideDevPreview } from "@/lib/content/dev-guard";

export const metadata: Metadata = { title: "Visual gallery", robots: { index: false } };

export default async function VizGalleryPage() {
  notFoundOutsideDevPreview();
  return <VizGallery />;
}
