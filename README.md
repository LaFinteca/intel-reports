# Intelligence Reports

Static HTML intelligence reports, each served at its own unique URL via GitHub Pages.

**Live index:** https://lafinteca.github.io/intel-reports/

### Reports

- [Adult Cyberlocker Research](https://lafinteca.github.io/intel-reports/reports/adult-cyberlocker-research.html)
- [Betsson Intel Brief](https://lafinteca.github.io/intel-reports/reports/betsson-intel-brief.html)
- [Entertainment Investment Firms](https://lafinteca.github.io/intel-reports/reports/entertainment-investment-firms.html)
- [MX iGaming Prospect Brief](https://lafinteca.github.io/intel-reports/reports/mx-igaming-prospect-brief.html)
- [OKTO Brazil Intel Brief](https://lafinteca.github.io/intel-reports/reports/okto-brazil-intel-brief.html)
- [Polymarket Analysis](https://lafinteca.github.io/intel-reports/reports/polymarket-analysis.html)

> This list is a manual mirror — the [live index](https://lafinteca.github.io/intel-reports/) auto-updates, so re-add a line here whenever you add a report (or skip it and rely on the live page).

## How it works

- Every `.html` file inside [`reports/`](reports/) is published at its own URL.
- The [index page](index.html) renders the list from [`reports.json`](reports.json) — a static manifest of every report (name, size, creation date), sorted newest-first. **No GitHub API calls**, so the list never breaks under API rate limits.
- `reports.json` is regenerated automatically: the [Build reports manifest](.github/workflows/build-manifest.yml) Action runs [`scripts/build-manifest.mjs`](scripts/build-manifest.mjs) on every push that touches `reports/**`. To regenerate locally: `node scripts/build-manifest.mjs`.
- Category tags and their colors live in `index.html` (`REPORT_TAGS` / `TAG_COLORS`) — add a line there when a report needs a tag.
- The repo is public, so any report is viewable by anyone who has the URL.

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

## Naming → URL

The filename becomes the URL and the display title on the index:

| File | URL path | Index title |
|------|----------|-------------|
| `pix-market-scan.html` | `/reports/pix-market-scan.html` | Pix Market Scan |
| `bcb-regulatory-2026.html` | `/reports/bcb-regulatory-2026.html` | Bcb Regulatory 2026 |

Use lowercase, hyphen-separated names. Avoid spaces and special characters.

## Notes

- `.nojekyll` disables GitHub's Jekyll processing so files are served exactly as committed.
- Reports are self-contained HTML (inline CSS/JS) — exactly what Claude artifacts produce — so they need no build step.
