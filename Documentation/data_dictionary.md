# Dictionnaire de données & sources

Montants en **millions d'euros (M€)**. Exercice = année civile.

## Sources

| Source | Utilisée pour | Fiabilité |
|---|---|---|
| `LVMH – Résultats annuels 2025.pdf` (27/01/2026) | LVMH 2024-2025 : ventes, ROC, résultat net, segments, géographie, change | ✅ Document fourni |
| `Hermès – Présentation des résultats annuels 2025.pdf` (12/02/2026) | Hermès 2024-2025 : CA, ROC, géographie, métiers, effectifs 2025 | ✅ Document fourni |
| `Kering – Rapport d'activité 2024.pdf` | Kering 2024 : CA, ROC, effectifs, géographie, segments | ✅ Document fourni |
| Communiqués annuels des 3 groupes (2021-2025, publics) | Historique 2021-2023 ; Kering 2025 (publié 10/02/2026) | ✅ Sources officielles recoupées |
| Données d'effectifs LVMH 2021-2022 | `employees` | ⚠️ `to_verify` — à recouper dans l'URD LVMH |

## `fact_group_financials.csv` (1 ligne = entreprise × année)

| Colonne | Définition |
|---|---|
| `revenue_meur` | Chiffre d'affaires publié |
| `recurring_op_income_meur` | Résultat opérationnel courant (ROC) |
| `net_income_group_meur` | Résultat net part du Groupe |
| `employees` | Effectif fin de période (Kering 2024 : 47 000 arrondi) |
| `organic_growth_pct` | LVMH : organique · Hermès : taux de change constants · Kering : comparable |
| `op_margin_pct` | ROC / CA (calculé) |
| `revenue_growth_pct` | Variation publiée N / N-1 (calculée) |
| `revenue_per_employee_keur` | CA / effectif (calculé) |

## `fact_segments.csv`
Segments tels que publiés. **Sephora n'est pas isolé** : LVMH le publie dans « Distribution sélective » (avec DFS, Le Bon Marché).
Hermès : seul le CA 2025 par métier est disponible dans les documents fournis ; Kering : Gucci, Saint Laurent, Bottega Veneta, Autres Maisons.

## `fact_geography.csv` — régions harmonisées

| Groupe | Correspondance |
|---|---|
| LVMH | Europe ; **Amériques = États-Unis seulement** ; Japon ; Asie hors Japon ; Autres (14 %, contient le reste des Amériques) |
| Hermès | Europe = France + Europe hors France ; Amériques ; Japon ; Asie-Pacifique hors Japon ; Autres = Moyen-Orient |
| Kering | Europe = Europe de l'Ouest ; Amériques = Amérique du Nord ; **2024 uniquement** |

Les parts sont arrondies par les émetteurs (somme = 100 %). `revenue_meur_est` = part × CA (estimation).
