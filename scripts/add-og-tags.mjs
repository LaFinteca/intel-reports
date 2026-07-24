// Inserts Open Graph / Twitter Card <meta> tags into new digest issues, so
// pasting a digest link (Slack, etc.) shows a rich preview with a branded
// image instead of a bare link.
//
// Scope: digests/*.html ONLY — the report center (index.html) and
// reports/*.html intentionally do not get link-preview images.
//
// Each issue needs its own OG image (the "Week N" title is baked into the
// image). Generate it first:
//   python3 scripts/generate-og-image.py --week "Week 31" \
//     --intro "Fintech, payments & LatAm intelligence. Curated weekly." \
//     --out assets/og-digest-week-31.jpg
// then add a line for the issue below in DIGEST_META before running this
// script.
//
// Idempotent: skips any file that already has an og:image tag.
//
// Run:  node scripts/add-og-tags.mjs

import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const SITE = "https://lafinteca.github.io/intel-reports";
const DESC = "Fintech, payments &amp; LatAm intelligence. Curated weekly.";

// filename (in digests/) -> { week, image }
const DIGEST_META = {
  "friday-fintech-digest-2026-07-17.html": { week: "Week 29", image: "og-digest-week-29.jpg" },
  "friday-fintech-digest-2026-07-24.html": { week: "Week 30", image: "og-digest-week-30.jpg" },
};

function tagBlock(title, desc, image, url) {
  return [
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="LaFinteca MRO">',
    `<meta property="og:title" content="${title}">`,
    `<meta property="og:description" content="${desc}">`,
    `<meta property="og:image" content="${SITE}/assets/${image}">`,
    `<meta property="og:url" content="${SITE}/${url}">`,
    '<meta name="twitter:card" content="summary_large_image">',
    `<meta name="twitter:title" content="${title}">`,
    `<meta name="twitter:description" content="${desc}">`,
    `<meta name="twitter:image" content="${SITE}/assets/${image}">`,
  ].map((l) => "  " + l).join("\n");
}

let updated = 0, skipped = 0;
for (const name of readdirSync("digests").filter((f) => /\.html?$/i.test(f))) {
  const path = join("digests", name);
  const html = readFileSync(path, "utf8");
  if (html.includes('property="og:image"')) { skipped++; continue; }

  const meta = DIGEST_META[name];
  if (!meta) { console.log(`SKIP (no DIGEST_META entry): ${path}`); skipped++; continue; }

  const title = `Weekly Industry Digest · ${meta.week} — LaFinteca MRO`;
  const block = tagBlock(title, DESC, meta.image, `digests/${name}`);
  const out = html.replace(/<\/head>/i, `${block}\n</head>`);
  writeFileSync(path, out);
  updated++;
  console.log(`Added OG tags: ${path}`);
}
console.log(`\n${updated} updated, ${skipped} skipped (already had og:image or no DIGEST_META entry).`);
