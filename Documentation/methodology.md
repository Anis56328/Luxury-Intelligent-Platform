# Méthodologie & limites

## Questions business → indicateurs
| Question | Indicateur | Où |
|---|---|---|
| Qui croît le plus vite ? | TCAM du CA 2021-2025, croissance annuelle, croissance organique/cc | `kpi_summary.csv` |
| Qui crée le plus de valeur ? | Marge opérationnelle courante, marge nette, CA par employé | `kpi_summary.csv` |
| Quelle région tire la performance ? | Part du CA par région, croissance trimestrielle (LVMH) | `fact_geography*.csv` |
| Quels segments créent le plus de valeur ? | Marge de segment × croissance 2025 | `fact_segments.csv` |
| Que prioriser ? | Scorecard « momentum » + recommandations | `ceo_scorecard.csv`, `recommendations.json` |

## Règle de momentum (transparente)
`GAGNE` si croissance organique 2025 ≥ 5 % **et** marge ≥ niveau 2021 ; `DÉCROCHE` si ≤ −5 % ; sinon `RALENTIT`.
C'est un choix de lecture, modifiable dans `Python/02_analysis.py`.

## Limites à connaître (à mentionner en entretien)
1. **Périmètre Kering 2025** : publié en activités poursuivies (cession de Kering Beauté). 2024 retraité = CA 16 874 M€ / ROC 2 440 M€ ;
   le dataset conserve la base *publiée* 2024 (17 194 / 2 554) pour 2021-2024. Le TCAM 2021-2025 mélange donc deux périmètres.
2. **Définitions de croissance** : organique (LVMH), taux constants (Hermès), comparable (Kering) — proches mais non strictement identiques.
3. **Géographie** : définitions régionales différentes (Amériques = États-Unis chez LVMH) ; Kering 2025 absent des sources utilisées.
4. **Segments** : Sephora non isolé chez LVMH ; segments Hermès disponibles pour 2025 uniquement.
5. **Effectifs LVMH 2021-2022** à recouper (`to_verify`).
6. **Recommandations** : lecture analytique de données publiques, pas un conseil en investissement.

## Chiffres clés vérifiables dans les PDF fournis
- LVMH : ventes 80 807 M€ (−5 % publié, −1 % organique), ROC 17 755 M€ (−9 %), effet de change sur ROC −1 065 M€ (p.21-22).
- Hermès : CA 16 002 M€ (+9 % cc), ROC 6 569 M€, marge 41,0 % (p.15, 22).
- Kering 2024 : CA 17 194 M€, ROC 2 554 M€, Gucci 7 650 M€ (p.73).
