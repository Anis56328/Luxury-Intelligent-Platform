# Luxury Intelligence Platform

Strategic analysis of three global luxury leaders:
- LVMH
- Hermès
- Kering

> **Live dashboard** : activer GitHub Pages (Settings → Pages → `main` / `/docs`) puis ouvrir `docs/index.html`.

## Objective

Provide executive insights on growth, profitability,
geographical performance and business segments.

## Technologies

- Python (pandas, matplotlib, reportlab)
- HTML / JavaScript / Chart.js (interactive dashboard in `docs/`)
- CSV (star-schema data model in `Data/`)

## Business Questions

- Which luxury group grows the fastest?
- Which region drives performance?
- Which business segments create the most value?
- What strategic actions should executives prioritize?

## Key findings (FY2025)

| | LVMH | Hermès | Kering |
|---|---|---|---|
| Revenue | €80.8bn | €16.0bn | €14.7bn |
| Organic / constant-currency growth | −1 % | +9 % | −10 % |
| Operating margin | 22.0 % | 41.1 %\* | 11.1 % |
| Revenue CAGR 2021-25 | +5.9 % | +15.5 % | −4.5 %\*\* |
| Revenue per employee | €382k | €604k | €336k |

\*Hermès publishes 41.0 % (rounding: 6,569 / 16,002 = 41.05 %). \*\*Kering 2025 is on a continuing-operations basis (see `Documentation/methodology.md`).

- **Who wins?** Hermès: highest growth *and* a margin ~19 pts above LVMH.
- **Who slows?** LVMH: −1 % organic, and 59 % of its 2025 operating-profit decline (−€1,065m of −€1,816m) comes from FX — see `Documentation/fx_effect_explained.md`.
- **Who falls behind?** Kering: Gucci (−19 %, 41 % of sales) drives the group decline.
- **Where to watch?** Asia ex-Japan lost 2 pts of sales share at both LVMH (26 %) and Hermès (42 %); Japan diverges (LVMH −12 % vs Hermès +14 %).

## Deliverables

| # | Deliverable | Location |
|---|---|---|
| 1 | Executive Dashboard (KPIs, filters Year / Company) | `docs/index.html` |
| 2 | Luxury Growth Analysis | `Documentation/figures/01-03`, `docs/index.html` |
| 3 | Geographic Intelligence | `Documentation/figures/04`, `docs/index.html` |
| 4 | Business Segments Analysis | `Documentation/figures/05`, `docs/index.html` |
| 5 | Luxury CEO Dashboard (who wins / slows / where to invest / which market) | `docs/index.html` (top block) |
| + | Strategic Recommendations | `Data/recommendations.json`, `Executive_Report.pdf` |

## Repository structure

```
Luxury-Intelligence-Platform
│
├── Data/            # CSV tables (facts + dimensions), KPIs, scorecard, recommendations
├── Python/          # 01 dataset · 02 analysis · 03 dashboard · 04 report
├── Documentation/   # data_dictionary, methodology, verification_log, fx_effect_explained, pitch_5min, figures/
├── docs/            # interactive HTML dashboard (GitHub Pages)
├── screenshots/     # dashboard screenshots
├── Executive_Report.pdf
└── README.md
```

## Reproduce

```bash
pip install -r requirements.txt
bash run_all.sh
```

## Data quality

15 key figures were checked against the source PDFs (`Documentation/verification_log.md`).
Sources: official results presentations (LVMH & Hermès FY2025, Kering 2024 activity report) and annual press releases 2021-2025.
Limits are listed in `Documentation/methodology.md`. Educational analysis — not investment advice.

## Outcome

An executive dashboard designed to support strategic decision-making.
