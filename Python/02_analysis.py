"""Analyse stratégique LVMH / Hermès / Kering.

Produit : Data/kpi_summary.csv, Data/ceo_scorecard.csv, Data/recommendations.json
          Documentation/figures/*.png
Lancer : python 01_build_dataset.py && python 02_analysis.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA, FIG = ROOT / "Data", ROOT / "Documentation" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

COL = {"LVMH": "#B08D57", "Hermès": "#E87722", "Kering": "#1F3A5F"}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})

g = pd.read_csv(DATA / "fact_group_financials.csv")
seg = pd.read_csv(DATA / "fact_segments.csv")
geo = pd.read_csv(DATA / "fact_geography.csv")
cos = ["LVMH", "Hermès", "Kering"]


def cagr(a, b, n):
    return ((b / a) ** (1 / n) - 1) * 100


# ---------- KPI summary ----------
rows = []
for c in cos:
    d = g[g.company == c].set_index("year")
    rows.append({
        "company": c,
        "revenue_2025_meur": d.revenue_meur[2025],
        "revenue_cagr_21_25_pct": round(cagr(d.revenue_meur[2021], d.revenue_meur[2025], 4), 1),
        "roc_cagr_21_25_pct": round(cagr(d.recurring_op_income_meur[2021], d.recurring_op_income_meur[2025], 4), 1),
        "growth_2025_pct": d.revenue_growth_pct[2025],
        "organic_growth_2025_pct": d.organic_growth_pct[2025],
        "op_margin_2025_pct": d.op_margin_pct[2025],
        "op_margin_change_vs_2021_pts": round(d.op_margin_pct[2025] - d.op_margin_pct[2021], 1),
        "net_margin_2025_pct": d.net_margin_pct[2025],
        "employees_2025": d.employees[2025],
        "headcount_change_2025_pct": round((d.employees[2025] / d.employees[2024] - 1) * 100, 1),
        "revenue_per_employee_2025_keur": d.revenue_per_employee_keur[2025],
    })
kpi = pd.DataFrame(rows)
kpi.to_csv(DATA / "kpi_summary.csv", index=False)


# ---------- Scorecard CEO : qui gagne / qui ralentit ----------
def status(r):
    if r.organic_growth_2025_pct >= 5 and r.op_margin_change_vs_2021_pts >= 0:
        return "GAGNE"
    if r.organic_growth_2025_pct <= -5:
        return "DÉCROCHE"
    return "RALENTIT"


kpi["momentum"] = kpi.apply(status, axis=1)
kpi[["company", "organic_growth_2025_pct", "op_margin_2025_pct", "op_margin_change_vs_2021_pts",
     "revenue_cagr_21_25_pct", "momentum"]].to_csv(DATA / "ceo_scorecard.csv", index=False)

# ---------- Chiffres dérivés pour les recommandations ----------
lv = g[g.company == "LVMH"].set_index("year")
fx_share = round(1065 / (19571 - 17755) * 100)          # LVMH p.21 : effet de change / baisse totale du ROC
gap_pts = round(g[(g.company == "Hermès") & (g.year == 2025)].op_margin_pct.iloc[0]
                - lv.op_margin_pct[2025], 1)
s25 = seg[seg.year == 2025]
gucci_share = round(s25[s25.segment == "Gucci"].revenue_meur.iloc[0] / g[(g.company == "Kering") & (g.year == 2025)].revenue_meur.iloc[0] * 100)
lv_seg = s25[s25.company == "LVMH"].set_index("segment")
asia = geo[(geo.region == "Asie-Pacifique (hors Japon)")].pivot(index="company", columns="year", values="share_pct")

recs = [
    {"observation": f"Hermès croît de {kpi.set_index('company').organic_growth_2025_pct['Hermès']:.0f}% à taux constants en 2025 quand LVMH recule de 1% (organique) et Kering de 10% (comparable).",
     "recommendation": "Renforcer l'allocation vers les positions ultra-premium / clientèle haut de gamme, moins sensibles au cycle (benchmark : modèle Hermès)."},
    {"observation": f"L'écart de marge opérationnelle Hermès – LVMH est de {gap_pts:.0f} pts (41,1% vs 22,0%) ; {fx_share}% de la baisse du ROC LVMH 2025 vient du change (−1 065 M€ sur −1 816 M€).",
     "recommendation": "Piloter séparément la performance sous-jacente et l'effet devises ; renforcer la couverture de change et l'ajustement des prix par zone."},
    {"observation": f"L'Asie hors Japon pèse {asia.loc['Hermès', 2025]:.0f}% des ventes Hermès et {asia.loc['LVMH', 2025]:.0f}% de LVMH, en recul de 2 pts chez les deux groupes vs 2024.",
     "recommendation": "Accélérer CRM et clienteling digital en Asie et suivre le taux de rétention des clients locaux ; suivre l'évolution trimestrielle de la zone (LVMH Asie hors Japon : −4% en 2025, +1% au T4)."},
    {"observation": "Le Japon est à −12% organique chez LVMH en 2025 mais +14% (taux constants) chez Hermès ; États-Unis stables à 0% chez LVMH et +12% chez Hermès (Amériques).",
     "recommendation": "Marchés à surveiller : Japon (écart de performance LVMH/Hermès à expliquer) et États-Unis (stabilité à confirmer sur 2026)."},
    {"observation": f"Chez LVMH, la Distribution sélective progresse de +4% (ROC +28%, marge {lv_seg.loc['Distribution sélective (Sephora, DFS…)','op_margin_pct']:.0f}%) tandis que Mode & Maroquinerie recule de 5% (marge {lv_seg.loc['Mode & Maroquinerie','op_margin_pct']:.0f}%).",
     "recommendation": "Où investir : prioriser Sephora et Montres & Joaillerie (S2 +5%) ; protéger la marge de Mode & Maroquinerie, qui génère ~72% du ROC des activités (hors holding et éliminations)."},
    {"observation": f"Gucci pèse encore {gucci_share}% du CA Kering en 2025 (−19% comparable) alors que Bottega Veneta progresse de +3% et Saint Laurent maintient 20% de marge.",
     "recommendation": "Réduire la dépendance à une marque unique : accélérer Saint Laurent / Bottega Veneta et le redressement de Gucci avant toute expansion de capacité."},
    {"observation": "Le CA par employé atteint 604 k€ chez Hermès contre 382 k€ chez LVMH et 336 k€ chez Kering ; Hermès recrute (+5%) quand LVMH (−2%) et Kering (−7%) réduisent leurs effectifs.",
     "recommendation": "Maintenir l'investissement dans l'artisanat et la capacité de production (24 maroqueries) : la productivité est le moteur de la marge."},
]
(DATA / "recommendations.json").write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------- Graphiques ----------
# 1. Indice de CA base 100 (2021)
fig, ax = plt.subplots(figsize=(8, 4.5))
for c in cos:
    d = g[g.company == c].set_index("year").revenue_meur
    ax.plot(d.index, d / d[2021] * 100, marker="o", lw=2.5, color=COL[c], label=c)
    ax.annotate(f"{d[2025]/d[2021]*100:.0f}", (2025, d[2025] / d[2021] * 100), xytext=(6, 0),
                textcoords="offset points", color=COL[c], fontweight="bold")
ax.axhline(100, color="grey", lw=.8)
ax.set_title("Chiffre d'affaires, indice base 100 (2021)", loc="left", fontweight="bold")
ax.set_xticks(range(2021, 2026)); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(FIG / "01_revenue_index.png", dpi=160); plt.close(fig)

# 2. Croissance annuelle publiée
fig, ax = plt.subplots(figsize=(8, 4.5))
w = .27
for i, c in enumerate(cos):
    d = g[(g.company == c) & (g.year >= 2022)]
    ax.bar(d.year + (i - 1) * w, d.revenue_growth_pct, w, color=COL[c], label=c)
ax.axhline(0, color="black", lw=.8)
ax.set_title("Croissance annuelle du CA (publiée, %) — Qui croît le plus vite ?", loc="left", fontweight="bold")
ax.set_xticks(range(2022, 2026)); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(FIG / "02_growth.png", dpi=160); plt.close(fig)

# 3. Marge opérationnelle
fig, ax = plt.subplots(figsize=(8, 4.5))
for c in cos:
    d = g[g.company == c].set_index("year").op_margin_pct
    ax.plot(d.index, d, marker="o", lw=2.5, color=COL[c], label=c)
    ax.annotate(f"{d[2025]:.1f}%", (2025, d[2025]), xytext=(6, 0), textcoords="offset points", color=COL[c], fontweight="bold")
ax.set_title("Marge opérationnelle courante (%)", loc="left", fontweight="bold")
ax.set_xticks(range(2021, 2026)); ax.legend(frameon=False); ax.set_ylim(0, 48)
fig.tight_layout(); fig.savefig(FIG / "03_margin.png", dpi=160); plt.close(fig)

# 4. Géographie (2025 ; Kering 2024)
order = ["Europe", "Amériques", "Japon", "Asie-Pacifique (hors Japon)", "Autres"]
pal = ["#5B7DB1", "#B08D57", "#C0504D", "#E87722", "#9AA5B1"]
pv = pd.concat([geo[(geo.company == "LVMH") & (geo.year == 2025)], geo[(geo.company == "Hermès") & (geo.year == 2025)],
                geo[(geo.company == "Kering") & (geo.year == 2024)]]).pivot(index="company", columns="region", values="share_pct")
pv = pv.loc[["LVMH", "Hermès", "Kering"], order]
fig, ax = plt.subplots(figsize=(8, 4.2))
left = pd.Series(0, index=pv.index)
for r, p in zip(order, pal):
    ax.barh(pv.index, pv[r], left=left, color=p, label=r)
    for i, v in enumerate(pv[r]):
        ax.text(left.iloc[i] + v / 2, i, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    left += pv[r]
ax.invert_yaxis(); ax.grid(False)
ax.set_yticks(range(3)); ax.set_yticklabels(["LVMH 2025", "Hermès 2025", "Kering 2024*"])
ax.set_title("Répartition géographique du CA", loc="left", fontweight="bold")
ax.legend(ncol=5, frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(.5, -.08))
fig.text(.01, .01, "*Kering 2025 non disponible dans les sources ; Amériques = États-Unis chez LVMH.", fontsize=7, color="grey")
fig.tight_layout(); fig.savefig(FIG / "04_geography.png", dpi=160); plt.close(fig)

# 5. Segments : croissance 2025 vs marge
d5 = s25.dropna(subset=["organic_growth_2025_pct", "op_margin_pct"])
fig, ax = plt.subplots(figsize=(8, 4.8))
for _, r in d5.iterrows():
    ax.scatter(r.organic_growth_2025_pct, r.op_margin_pct, s=r.revenue_meur / 18, color=COL[r.company], alpha=.75, edgecolor="white")
    ax.annotate(r.segment.split(" (")[0], (r.organic_growth_2025_pct, r.op_margin_pct), fontsize=7.5, xytext=(5, 5), textcoords="offset points")
ax.axvline(0, color="grey", lw=.8)
ax.set_xlabel("Croissance organique 2025 (%)"); ax.set_ylabel("Marge opérationnelle 2025 (%)")
ax.set_title("Segments : croissance vs rentabilité (taille = CA)", loc="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG / "05_segments.png", dpi=160); plt.close(fig)

print(kpi.to_string(index=False))
print("figures:", sorted(p.name for p in FIG.glob("*.png")))
