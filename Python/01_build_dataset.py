"""Construit les tables du modèle de données (Data/*.csv).

Toutes les valeurs sont saisies à partir des sources citées dans la colonne `source`.
Montants en millions d'euros (M€). Les valeurs marquées 'to_verify' sont à recouper
avant publication (voir Documentation/data_dictionary.md).
"""
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "Data"
OUT.mkdir(exist_ok=True)

# ---------- 1. Groupe : chiffres clés 2021-2025 ----------
# organic = croissance organique (LVMH) / taux de change constants (Hermès) / comparable (Kering)
rows = [
    ("LVMH", 2021, 64215, 17151, 12036, 175647, 36.0, "LVMH comm. 27/01/2022 ; effectif URD (to_verify)"),
    ("LVMH", 2022, 79184, 21055, 14084, 196006, 17.0, "LVMH comm. 26/01/2023 ; effectif URD (to_verify)"),
    ("LVMH", 2023, 86153, 22802, 15174, 213268, 13.0, "LVMH comm. 25/01/2024"),
    ("LVMH", 2024, 84683, 19571, 12550, 215637, 1.0, "LVMH Résultats annuels 2025.pdf (p.22-23)"),
    ("LVMH", 2025, 80807, 17755, 10878, 211552, -1.0, "LVMH Résultats annuels 2025.pdf (p.15-23)"),
    ("Hermès", 2021, 8982, 3530, 2445, 17595, 42.0, "Hermès comm. 18/02/2022"),
    ("Hermès", 2022, 11602, 4697, 3367, 19686, 23.0, "Hermès comm. 17/02/2023"),
    ("Hermès", 2023, 13427, 5650, 4311, 22037, 21.0, "Hermès comm. 09/02/2024"),
    ("Hermès", 2024, 15170, 6150, 4603, 25185, 15.0, "Hermès Résultats annuels 2025.pdf (p.22-24)"),
    ("Hermès", 2025, 16002, 6569, 4524, 26494, 9.0, "Hermès Résultats annuels 2025.pdf (p.2, 22-24)"),
    ("Kering", 2021, 17645, 5017, 3176, 42811, None, "Kering Document financier 2022"),
    ("Kering", 2022, 20351, 5589, 3614, 47227, 9.0, "Kering Document financier 2022"),
    ("Kering", 2023, 19566, 4746, 2983, 48964, -2.0, "Kering comm. 08/02/2024"),
    ("Kering", 2024, 17194, 2554, 1133, 47000, None, "Kering Rapport d'activité 2024.pdf (p.9, 73) - base publiée"),
    ("Kering", 2025, 14675, 1631, 72, 43731, -10.0,
     "Kering comm. 10/02/2026 (activités poursuivies ; 2024 retraité : CA 16 874 / ROC 2 440)"),
]
g = pd.DataFrame(rows, columns=[
    "company", "year", "revenue_meur", "recurring_op_income_meur",
    "net_income_group_meur", "employees", "organic_growth_pct", "source"])
g["op_margin_pct"] = (g.recurring_op_income_meur / g.revenue_meur * 100).round(1)
g["net_margin_pct"] = (g.net_income_group_meur / g.revenue_meur * 100).round(1)
g["revenue_per_employee_keur"] = (g.revenue_meur / g.employees * 1000).round(0)
g = g.sort_values(["company", "year"]).reset_index(drop=True)
g["revenue_growth_pct"] = (g.groupby("company").revenue_meur.pct_change() * 100).round(1)
# Kering 2025 : croissance publiée calculée sur la base 2024 retraitée (16 874)
mask = (g.company == "Kering") & (g.year == 2025)
g.loc[mask, "revenue_growth_pct"] = round((14675 / 16874 - 1) * 100, 1)
g.to_csv(OUT / "fact_group_financials.csv", index=False)

# ---------- 2. Segments ----------
DS = "Distribution sélective (Sephora, DFS…)"
seg = [
    ("LVMH", 2024, "Mode & Maroquinerie", 41060, 15230), ("LVMH", 2025, "Mode & Maroquinerie", 37770, 13209),
    ("LVMH", 2024, "Vins & Spiritueux", 5862, 1356), ("LVMH", 2025, "Vins & Spiritueux", 5358, 1016),
    ("LVMH", 2024, "Parfums & Cosmétiques", 8418, 671), ("LVMH", 2025, "Parfums & Cosmétiques", 8174, 727),
    ("LVMH", 2024, "Montres & Joaillerie", 10577, 1546), ("LVMH", 2025, "Montres & Joaillerie", 10486, 1514),
    ("LVMH", 2024, DS, 18262, 1385), ("LVMH", 2025, DS, 18348, 1780),
    ("Kering", 2024, "Gucci", 7650, None), ("Kering", 2025, "Gucci", 5992, 966),
    ("Kering", 2024, "Saint Laurent", 2881, 593), ("Kering", 2025, "Saint Laurent", 2643, 529),
    ("Kering", 2024, "Bottega Veneta", 1713, 255), ("Kering", 2025, "Bottega Veneta", 1706, 267),
    ("Kering", 2024, "Autres Maisons", 3221, -9), ("Kering", 2025, "Autres Maisons", 2900, -112),
    ("Hermès", 2025, "Maroquinerie-Sellerie", 7070, None), ("Hermès", 2025, "Vêtement et Accessoires", 4525, None),
    ("Hermès", 2025, "Soie et Textiles", 964, None), ("Hermès", 2025, "Autres métiers Hermès", 2055, None),
    ("Hermès", 2025, "Parfum et Beauté", 489, None), ("Hermès", 2025, "Horlogerie", 549, None),
    ("Hermès", 2025, "Autres produits", 349, None),
]
s = pd.DataFrame(seg, columns=["company", "year", "segment", "revenue_meur", "recurring_op_income_meur"])
s["op_margin_pct"] = (s.recurring_op_income_meur / s.revenue_meur * 100).round(1)
growth25 = {
    ("LVMH", "Mode & Maroquinerie"): -5, ("LVMH", "Vins & Spiritueux"): -5, ("LVMH", "Parfums & Cosmétiques"): 0,
    ("LVMH", "Montres & Joaillerie"): 3, ("LVMH", DS): 4,
    ("Kering", "Gucci"): -19, ("Kering", "Saint Laurent"): -6, ("Kering", "Bottega Veneta"): 3,
    ("Kering", "Autres Maisons"): -6,
    ("Hermès", "Maroquinerie-Sellerie"): 13, ("Hermès", "Vêtement et Accessoires"): 6,
    ("Hermès", "Soie et Textiles"): 5, ("Hermès", "Autres métiers Hermès"): 11,
    ("Hermès", "Parfum et Beauté"): -8, ("Hermès", "Horlogerie"): -2, ("Hermès", "Autres produits"): 6,
}
s["organic_growth_2025_pct"] = [
    growth25.get((c, sg)) if y == 2025 else None for c, y, sg in zip(s.company, s.year, s.segment)]
s["source"] = "Présentations résultats annuels 2025 (LVMH p.19-22, Hermès p.18, Kering comm. 10/02/2026)"
s.to_csv(OUT / "fact_segments.csv", index=False)

# ---------- 3. Géographie (régions harmonisées) ----------
geo = [
    ("LVMH", 2025, "Europe", 26), ("LVMH", 2025, "Amériques", 26), ("LVMH", 2025, "Japon", 8),
    ("LVMH", 2025, "Asie-Pacifique (hors Japon)", 26), ("LVMH", 2025, "Autres", 14),
    ("LVMH", 2024, "Europe", 25), ("LVMH", 2024, "Amériques", 25), ("LVMH", 2024, "Japon", 9),
    ("LVMH", 2024, "Asie-Pacifique (hors Japon)", 28), ("LVMH", 2024, "Autres", 13),
    ("Hermès", 2025, "Europe", 25), ("Hermès", 2025, "Amériques", 19), ("Hermès", 2025, "Japon", 10),
    ("Hermès", 2025, "Asie-Pacifique (hors Japon)", 42), ("Hermès", 2025, "Autres", 4),
    ("Hermès", 2024, "Europe", 24), ("Hermès", 2024, "Amériques", 19), ("Hermès", 2024, "Japon", 9),
    ("Hermès", 2024, "Asie-Pacifique (hors Japon)", 44), ("Hermès", 2024, "Autres", 4),
    ("Kering", 2024, "Europe", 29), ("Kering", 2024, "Amériques", 24), ("Kering", 2024, "Japon", 8),
    ("Kering", 2024, "Asie-Pacifique (hors Japon)", 30), ("Kering", 2024, "Autres", 9),
]
ge = pd.DataFrame(geo, columns=["company", "year", "region", "share_pct"])
notes = {
    "LVMH": "'Amériques' = États-Unis uniquement (le reste des Amériques est dans 'Autres')",
    "Hermès": "Europe = France + Europe hors France ; Autres = Moyen-Orient",
    "Kering": "Europe = Europe de l'Ouest ; Amériques = Amérique du Nord ; 2025 non disponible",
}
ge["definition_note"] = ge.company.map(notes)
ge["revenue_meur_est"] = [
    round(sh / 100 * g[(g.company == c) & (g.year == y)].revenue_meur.iloc[0])
    for c, y, sh in zip(ge.company, ge.year, ge.share_pct)]
ge.to_csv(OUT / "fact_geography.csv", index=False)

hg = pd.DataFrame(
    [("France", 1575, 9), ("Europe (hors France)", 2362, 11), ("Japon", 1591, 14),
     ("Asie-Pacifique (hors Japon)", 6702, 5), ("Amériques", 3075, 12), ("Autres (Moyen-Orient)", 697, 15)],
    columns=["region_native", "revenue_meur", "growth_cc_pct"])
hg.insert(0, "company", "Hermès")
hg.insert(1, "year", 2025)
hg.to_csv(OUT / "fact_geography_hermes_native_2025.csv", index=False)

lg = pd.DataFrame(
    [("États-Unis", -3, 0, 3, 1, 0), ("Japon", -1, -28, -13, -5, -12),
     ("Asie (hors Japon)", -11, -6, 2, 1, -4), ("Europe", 2, -1, -2, -2, -1)],
    columns=["region", "Q1_2025", "Q2_2025", "Q3_2025", "Q4_2025", "FY_2025"])
lg.insert(0, "company", "LVMH")
lg.to_csv(OUT / "fact_geography_lvmh_organic_2025.csv", index=False)

# ---------- 4. Dimensions ----------
pd.DataFrame({
    "company": ["LVMH", "Hermès", "Kering"],
    "positioning": ["Conglomérat diversifié (75+ Maisons)", "Modèle intégré ultra-premium",
                    "Mode & maroquinerie concentrée (Gucci)"],
    "color": ["#B08D57", "#E87722", "#1F3A5F"]}).to_csv(OUT / "dim_company.csv", index=False)
pd.DataFrame({
    "region": ["Europe", "Amériques", "Japon", "Asie-Pacifique (hors Japon)", "Autres"],
    "sort": [1, 2, 3, 4, 5]}).to_csv(OUT / "dim_region.csv", index=False)
print("OK ->", sorted(p.name for p in OUT.glob("*.csv")))
