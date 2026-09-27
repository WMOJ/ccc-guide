// lib/search — public entry point. `loadSearch()` is client-only (fetches
// /search-index.json and builds MiniSearch); `buildSearchIndex()` is server-only (used by the
// route handler at build time).

export { buildSearchIndex, type SearchIndexEntry } from "./build-index";
export { loadSearch, type SearchEngine, type SearchResult } from "./client";
