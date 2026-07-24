// Inserts Open Graph / Twitter Card <meta> tags into index.html and every
// report/digest, so sharing a link (Slack, etc.) shows a rich preview with
// the site's branded image instead of a bare link.
//
// Idempotent: skips any file that already has an og:image tag, so it's safe
// to re-run after adding new reports/digests.
//
// Run:  node scripts/add-og-tags.mjs

import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const SITE = "https://lafinteca.github.io/intel-reports";
const IMAGE = `${SITE}/assets/og-image.png`;
const DEFAULT_DESC = "LaFinteca Marketing &amp; Research Office — intelligence report.";
const INDEX_DESC = "Market, merchant &amp; risk intelligence briefings, and the weekly Industry Digest — compiled by LaFinteca MRO.";

function targets() {
  const files = [{ path: "index.html", url: "" }];
  for (const dir of ["reports", "digests"]) {
    for (const name of readdirSync(dir).filter((f) => /\.html?$/i.test(f))) {
      files.push({ path: join(dir, name), url: `${dir}/${name}` });
    }
  }
  return files;
}

function tagBlock(title, desc, url) {
  return [
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="LaFinteca MRO">',
    `<meta property="og:title" content="${title}">`,
    `<meta property="og:description" content="${desc}">`,
    `<meta property="og:image" content="${IMAGE}">`,
    `<meta property="og:url" content="${SITE}/${url}">`,
    '<meta name="twitter:card" content="summary_large_image">',
    `<meta name="twitter:title" content="${title}">`,
    `<meta name="twitter:description" content="${desc}">`,
    `<meta name="twitter:image" content="${IMAGE}">`,
  ].map((l) => "  " + l).join("\n");
}

let updated = 0, skipped = 0;
for (const { path, url } of targets()) {
  const html = readFileSync(path, "utf8");
  if (html.includes('property="og:image"')) { skipped++; continue; }

  const titleMatch = html.match(/<title>([\s\S]*?)<\/title>/i);
  if (!titleMatch) { console.log(`SKIP (no <title>): ${path}`); skipped++; continue; }
  const title = titleMatch[1].trim();
  const desc = url === "" ? INDEX_DESC : DEFAULT_DESC;

  const block = tagBlock(title, desc, url);
  const out = html.replace(/<\/head>/i, `${block}\n</head>`);
  writeFileSync(path, out);
  updated++;
  console.log(`Added OG tags: ${path}`);
}
console.log(`\n${updated} updated, ${skipped} skipped (already had og:image or no <title>).`);
