"""Génère Executive_Report.pdf (4 pages) à partir des CSV et des figures."""
import json
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "Documentation" / "figures"
kpi = pd.read_csv(ROOT / "Data/kpi_summary.csv")
recs = json.loads((ROOT / "Data/recommendations.json").read_text(encoding="utf-8"))

NAVY, GOLD = colors.HexColor("#1F3A5F"), colors.HexColor("#B08D57")
H1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=22, leading=28, textColor=NAVY, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=14, textColor=NAVY, spaceBefore=10, spaceAfter=4)
B = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=13.5, spaceAfter=5)
S = ParagraphStyle("s", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=colors.grey)


def img(name, w=16):
    from PIL import Image as PI
    iw, ih = PI.open(FIG / name).size
    return Image(str(FIG / name), width=w * cm, height=w * cm * ih / iw)


def footer(c, d):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.grey)
    c.drawString(2 * cm, 1.2 * cm, "Luxury Intelligence Platform — analyse pédagogique, pas un conseil en investissement")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"{d.page}")
    c.restoreState()


k = kpi.set_index("company")
story = [
    Paragraph("Luxury Intelligence Platform", H1),
    Paragraph("Benchmark stratégique LVMH · Hermès · Kering — Executive report", ParagraphStyle("t", parent=B, fontSize=11, leading=15, textColor=GOLD)),
    Spacer(1, 8),
    Paragraph("Question centrale", H2),
    Paragraph("Quels groupes de luxe créent le plus de valeur, et quelles tendances façonneront le secteur ?", B),
    Paragraph("Synthèse en 15 secondes", H2),
]
tbl = [["", "LVMH", "Hermès", "Kering"],
       ["CA 2025 (M€)"] + [f"{k.revenue_2025_meur[c]:,.0f}".replace(",", " ") for c in ["LVMH", "Hermès", "Kering"]],
       ["Croissance organique 2025"] + [f"{k.organic_growth_2025_pct[c]:+.0f} %" for c in ["LVMH", "Hermès", "Kering"]],
       ["Marge opérationnelle 2025"] + [f"{k.op_margin_2025_pct[c]:.1f} %" for c in ["LVMH", "Hermès", "Kering"]],
       ["TCAM du CA 2021-2025"] + [f"{k.revenue_cagr_21_25_pct[c]:+.1f} %" for c in ["LVMH", "Hermès", "Kering"]],
       ["CA par employé (k€)"] + [f"{k.revenue_per_employee_2025_keur[c]:.0f}" for c in ["LVMH", "Hermès", "Kering"]],
       ["Momentum", "RALENTIT", "GAGNE", "DÉCROCHE"]]
t = Table(tbl, colWidths=[5.5 * cm, 3.6 * cm, 3.6 * cm, 3.6 * cm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                       ("FONTNAME", (0, 0), (-1, -1), "Helvetica"), ("FONTSIZE", (0, 0), (-1, -1), 9),
                       ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                       ("GRID", (0, 0), (-1, -1), .4, colors.lightgrey),
                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F3EC")])]))
story += [t, Spacer(1, 6),
          Paragraph("Hermès gagne (croissance et marge), LVMH ralentit mais reste très rentable et diversifié, "
                    "Kering décroche sous l'effet de la contre-performance de Gucci. "
                    "<i>Momentum = règle simple et explicite : GAGNE si croissance organique ≥ 5 % et marge ≥ 2021 ; "
                    "DÉCROCHE si ≤ −5 % ; sinon RALENTIT.</i>", B),
          img("01_revenue_index.png", 14), PageBreak(),
          Paragraph("1. Croissance et rentabilité", H2),
          Paragraph("Hermès a multiplié son chiffre d'affaires par 1,8 depuis 2021 (TCAM +15,5 %) alors que LVMH progresse de +5,9 % par an "
                    "et que Kering recule. La marge opérationnelle d'Hermès (41,1 %) est de 19 points supérieure à celle de LVMH (22,0 %). "
                    "Chez LVMH, 59 % de la baisse du résultat opérationnel courant 2025 (−1 816 M€) provient du change (−1 065 M€).", B),
          img("02_growth.png", 13.5), img("03_margin.png", 13.5), PageBreak(),
          Paragraph("2. Intelligence géographique", H2),
          Paragraph("L'Asie hors Japon pèse 42 % des ventes d'Hermès contre 26 % chez LVMH (30 % chez Kering en 2024). "
                    "La part de la zone recule de 2 points chez les deux premiers en 2025. L'Europe est la seule région de LVMH sans amélioration au S2 (−1 % sur l'année). "
                    "Les Amériques progressent chez Hermès (+12 % à taux constants) alors que les États-Unis sont stables chez LVMH (0 %).", B),
          img("04_geography.png", 14),
          Paragraph("Limite : les définitions régionales diffèrent entre groupes (cf. Documentation/methodology.md).", S),
          Paragraph("3. Segments d'activité", H2),
          Paragraph("Les segments à surveiller : Distribution sélective LVMH (+4 %, ROC +28 %), Montres & Joaillerie (+5 % au S2), "
                    "Maroquinerie-Sellerie Hermès (+13 %), Bottega Veneta (+3 %). À l'inverse : Gucci (−19 %), Vins & Spiritueux (−5 %).", B),
          img("05_segments.png", 13.5), PageBreak(),
          Paragraph("4. Recommandations stratégiques", H2)]
for r in recs:
    story += [Paragraph(f"<b>Observation.</b> {r['observation']}", B),
              Paragraph(f"<b>Recommandation.</b> <font color='#8a6a2f'>{r['recommendation']}</font>", B), Spacer(1, 4)]
story += [Paragraph("Méthodologie et limites", H2),
          Paragraph("Sources : présentations de résultats annuels 2025 de LVMH et Hermès, rapport d'activité 2024 de Kering, communiqués annuels 2021-2025. "
                    "Kering 2025 est publié en activités poursuivies (2024 retraité : CA 16 874 M€, ROC 2 440 M€) ; le TCAM 2021-2025 de Kering mélange donc deux périmètres. "
                    "Les croissances comparées sont organiques (LVMH), à taux constants (Hermès) ou comparables (Kering) : définitions proches mais non identiques. "
                    "Les effectifs LVMH 2021-2022 sont à recouper.", S)]

SimpleDocTemplate(str(ROOT / "Executive_Report.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=1.8 * cm, bottomMargin=2 * cm, title="Luxury Intelligence Platform — Executive Report",
                  author="Luxury Intelligence Platform").build(story, onFirstPage=footer, onLaterPages=footer)
print("Executive_Report.pdf OK")
