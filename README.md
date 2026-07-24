# Intelligence Reports

Static HTML intelligence reports and the weekly Industry Digest, each served at its own unique URL via GitHub Pages. The live index lists both in a two-column layout — **Reports** on the left, **Industry Digest** on the right.

**Live index:** https://lafinteca.github.io/intel-reports/

### Reports

- [Adult Cyberlocker Research](https://lafinteca.github.io/intel-reports/reports/adult-cyberlocker-research.html)
- [Betsson Intel Brief](https://lafinteca.github.io/intel-reports/reports/betsson-intel-brief.html)
- [Entertainment Investment Firms](https://lafinteca.github.io/intel-reports/reports/entertainment-investment-firms.html)
- [MX iGaming Prospect Brief](https://lafinteca.github.io/intel-reports/reports/mx-igaming-prospect-brief.html)
- [OKTO Brazil Intel Brief](https://lafinteca.github.io/intel-reports/reports/okto-brazil-intel-brief.html)
- [Polymarket Analysis](https://lafinteca.github.io/intel-reports/reports/polymarket-analysis.html)
- [Praxis Tech Intelligence Brief](https://lafinteca.github.io/intel-reports/reports/praxis-tech-intelligence-brief.html)
- [Prediction Markets Vertical Assessment](https://lafinteca.github.io/intel-reports/reports/prediction-markets-vertical.html)
- [Compliance Workload Report](https://lafinteca.github.io/intel-reports/reports/compliance-workload-report.html) — *Internal*
- [Conduit Intelligence Update](https://lafinteca.github.io/intel-reports/reports/conduit-intelligence-update-2026-07.html)
- [Easygo Group Intelligence Brief](https://lafinteca.github.io/intel-reports/reports/easygo-group-intelligence-brief.html)
- [Brazino777 Mexico Intel Report](https://lafinteca.github.io/intel-reports/reports/brazino777-mx-intel-report.html)

### Industry Digest

- [Friday Fintech Digest — 17 Jul 2026](https://lafinteca.github.io/intel-reports/digests/friday-fintech-digest-2026-07-17.html)
- [Friday Fintech Digest — 24 Jul 2026](https://lafinteca.github.io/intel-reports/digests/friday-fintech-digest-2026-07-24.html)

> These lists are a manual mirror — the [live index](https://lafinteca.github.io/intel-reports/) auto-updates, so re-add a line here whenever you add a report or issue (or skip it and rely on the live page).

## How it works

- Every `.html` file inside [`reports/`](reports/) or [`digests/`](digests/) is published at its own URL.
- The [index page](index.html) renders both lists from static manifests — [`reports.json`](reports.json) and [`digests.json`](digests.json) — each a JSON array of `{ name, size, creation date }`, sorted newest-first. **No GitHub API calls**, so the lists never break under API rate limits.
- Both manifests regenerate automatically: the [Build manifests](.github/workflows/build-manifest.yml) Action runs [`scripts/build-manifest.mjs`](scripts/build-manifest.mjs) on every push that touches `reports/*.html` or `digests/*.html`. To regenerate locally: `node scripts/build-manifest.mjs`.
- Category tags and their colors (Reports panel only) live in `index.html` (`REPORT_TAGS` / `TAG_COLORS`) — add a line there when a report needs a tag.
- The repo is public, so any report or digest issue is viewable by anyone who has the URL.

## Add a report

1. Save your report's HTML into `reports/` with a descriptive, URL-friendly name:
   ```
   reports/dindix-competitive-q2.html
   ```
2. Commit and push:
   ```bash
   git add reports/dindix-competitive-q2.html
   git commit -m "Add Dindix competitive Q2 report"
   git push
   ```
3. Wait ~1 minute for GitHub Pages to rebuild. The report is then live at:
   ```
   https://lafinteca.github.io/intel-reports/reports/dindix-competitive-q2.html
   ```
   and appears automatically on the index.

## Add a digest issue

Same flow, into `digests/` instead — name it with the issue date so it sorts and displays cleanly:
```
digests/friday-fintech-digest-2026-07-24.html
```
The index strips a trailing `-YYYY-MM-DD` from the display title (the date already shows in its own column), so the issue above appears as **"Friday Fintech Digest."** Commit, push, and it appears on the Industry Digest panel within ~1 minute.

## Link previews (Slack, etc.)

Every page carries Open Graph / Twitter Card `<meta>` tags pointing at [`assets/og-image.png`](assets/og-image.png) — a static, branded image (a simplified rendition of the site header) so pasting any report/digest link into Slack shows a rich preview instead of a bare link.

After adding a new report or digest, run:
```bash
node scripts/add-og-tags.mjs
```
It's idempotent — it only touches files that don't already have an `og:image` tag, so it's safe to run anytime. `og:title` comes from each file's own `<title>`; the description is a fixed, generic line (per-file descriptions would need per-template extraction across too many different report designs to be worth automating).

## Naming → URL

The filename becomes the URL and the display title on the index:

| File | URL path | Index title |
|------|----------|-------------|
| `pix-market-scan.html` | `/reports/pix-market-scan.html` | Pix Market Scan |
| `bcb-regulatory-2026.html` | `/reports/bcb-regulatory-2026.html` | Bcb Regulatory 2026 |
| `friday-fintech-digest-2026-07-17.html` | `/digests/friday-fintech-digest-2026-07-17.html` | Friday Fintech Digest |

Use lowercase, hyphen-separated names. Avoid spaces and special characters.

## Notes

- `.nojekyll` disables GitHub's Jekyll processing so files are served exactly as committed.
- Reports and digest issues are self-contained HTML (inline CSS/JS) — exactly what Claude artifacts produce — so they need no build step.
