# Journal de vérification des chiffres (contrôle dans les PDF sources)

Contrôle réalisé en recherchant chaque chiffre dans le texte des 3 PDF fournis. Les numéros sont des **pages du fichier PDF** (le rapport Kering imprime des numéros décalés de 2 pages : p.73 imprimée = p.75 du PDF).

| # | Entreprise | Chiffre vérifié | Page(s) PDF | Statut |
|---|---|---|---|---|
| 1 | LVMH | Ventes 2025 = 80 807 M€ (2024 : 84 683) | 16, 19, 23 | ✅ |
| 2 | LVMH | Résultat opérationnel courant 2025 = 17 755 M€ | 21-23 | ✅ |
| 3 | LVMH | Effet de change sur le ROC = −1 065 M€ | 21 | ✅ |
| 4 | LVMH | Évolution organique du ROC = −740 M€ | 21 | ✅ |
| 5 | LVMH | Résultat net part du Groupe = 10 878 M€ | 23 | ✅ |
| 6 | LVMH | Dette nette fin 2025 = 6 857 M€ | 27 | ✅ |
| 7 | LVMH | Cash flow disponible = 11 333 M€ | 26 | ✅ |
| 8 | Hermès | CA 2025 = 16 002 M€ | 15, 18, 22 | ✅ |
| 9 | Hermès | Résultat opérationnel courant = 6 569 M€ ; marge publiée 41,0 % | 22, 24 | ✅ |
| 10 | Hermès | 26 494 collaborateurs | 2 | ✅ |
| 11 | Hermès | Asie-Pacifique hors Japon : 42 % (44 % en 2024) | 16 | ✅ |
| 12 | Hermès | Trésorerie nette retraitée = 12 773 M€ | 29 | ✅ |
| 13 | Kering | CA 2024 = 17 194 M€ ; ROC = 2 554 M€ | 11, 75 | ✅ |
| 14 | Kering | 47 000 collaborateurs | 11 | ✅ |
| 15 | Kering | Gucci = 7 650 M€ de CA 2024 | 75 | ✅ |

**15 lignes, 18 valeurs retrouvées.**

## Écarts à connaître
- **Marge Hermès** : le PDF publie **41,0 %** ; le dataset calcule 6 569 / 16 002 = 41,05 % arrondi à **41,1 %**. Écart d'arrondi (Hermès calcule probablement sur des montants non arrondis). À dire si on te le demande.
- **Pas dans tes PDF** (sources externes, à vérifier si besoin) : historique 2021-2023, Kering 2025, effectifs LVMH 2021-2022, croissance organique des années passées.
