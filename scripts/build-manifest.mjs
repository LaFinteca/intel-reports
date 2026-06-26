// Generates reports.json — a static index of every report in reports/.
// Each entry: { name, size (bytes), created (ISO, from the file's first git commit) }.
// Sorted newest-first. The site reads this instead of the GitHub API, so the
// report list never breaks under API rate limits.
//
// Run:  node scripts/build-manifest.mjs
// Requires full git history (in CI, checkout with fetch-depth: 0).

import { execFileSync } from "node:child_process";
import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const DIR = "reports";
const OUT = "reports.json";

const files = readdirSync(DIR).filter((f) => /\.html?$/i.test(f));

const entries = files.map((name) => {
  const path = join(DIR, name);
  const size = statSync(path).size;

  // Creation date = the OLDEST commit that ADDED this file.
  // execFileSync (argv array, no shell) so a filename can never inject.
  let created = null;
  try {
    const log = execFileSync(
      "git",
      ["log", "--diff-filter=A", "--format=%cI", "--", path],
      { encoding: "utf8" }
    ).trim();
    const lines = log.split("\n").filter(Boolean);
    if (lines.length) created = lines[lines.length - 1]; // oldest = the add
  } catch {
    /* fall through to mtime */
  }
  // Fallback for a file not yet committed (e.g. local dry run).
  if (!created) created = statSync(path).mtime.toISOString();

  return { name, size, created };
});

entries.sort((a, b) => {
  const tb = Date.parse(b.created) || 0;
  const ta = Date.parse(a.created) || 0;
  if (tb !== ta) return tb - ta; // newest first
  return a.name.localeCompare(b.name); // stable tie-break for same-commit batches
});

writeFileSync(OUT, JSON.stringify(entries, null, 2) + "\n");
console.log(`Wrote ${OUT} with ${entries.length} report(s):`);
for (const e of entries) console.log(`  ${e.created.slice(0, 10)}  ${e.name}`);
