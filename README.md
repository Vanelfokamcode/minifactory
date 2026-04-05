# MiniFactory

## C'est quoi ce projet

Je simule une Data Factory industrielle en local — le genre de pipeline qu'on trouve chez des boîtes.

L'idée : prendre une vraie source de données publique, l'ingérer, la stocker, la transformer, et répondre à une vraie question métier avec un dashboard. chaque décision est justifiée.

## La question métier

> "Quelles marques alimentaires ont le plus grand nombre de produits contenant des additifs, et quelle est la nature de ces additifs ?"

C'est la question qu'un analyste marketing poserait chez un acteur de l'agroalimentaire. Elle est claire, mesurable, et elle oriente toutes les décisions du pipeline.

## La source de données

**Open Food Facts** — base collaborative mondiale des produits alimentaires.
- Format : CSV compressé (~0.9 Go compressé, ~9 Go décompressé)
- Source : https://world.openfoodfacts.org/data
- ~180 colonnes, millions de produits

Pourquoi cette source : données réelles, sales, incomplètes — exactement ce qu'on trouve en production.

## Les colonnes qu'on garde et pourquoi

Sur ~180 colonnes disponibles, on en garde ~10. Le reste est ignoré.

| Colonne | Pourquoi |
|---|---|
| `code` | Clé primaire du produit |
| `product_name` | Nom lisible du produit |
| `brands_tags` | Marque normalisée (slug propre, pas la saisie brute) |
| `countries_en` | Pour filtrer sur un pays si besoin |
| `additives_n` | Nombre d'additifs — répond à "combien ?" |
| `additives_tags` | Liste des additifs — répond à "lesquels ?" |
| `nutriscore_grade` | Qualité nutritionnelle globale (A à E) |
| `nova_group` | Degré de transformation industrielle (1 à 4) |
| `completeness` | Score de complétude de la fiche — pour filtrer les lignes inutilisables |

### Pourquoi Nova Group ?

Nova classe les aliments par degré de transformation :
- **1** = brut (pomme, lait entier)
- **2** = ingrédient culinaire (beurre, farine)
- **3** = transformé (fromage, conserves)
- **4** = ultra-transformé (nuggets, sodas, plats préparés)

Deux marques peuvent avoir le même nombre d'additifs mais des profils très différents — l'une en Nova 3 (additifs de conservation), l'autre en Nova 4 (ultra-transformation). Sans Nova Group, on rate cette nuance.

### Pourquoi Nutriscore ?

Un produit peut avoir beaucoup d'additifs et un bon Nutriscore, ou peu d'additifs et un mauvais. C'est une deuxième dimension qui évite les conclusions trop rapides.

### Pourquoi `brands_tags` et pas `brands` ?

`brands` c'est la saisie brute des contributeurs — on peut avoir "Danone", "danone", "DANONE" pour la même marque. `brands_tags` c'est la version normalisée en slug (`en:danone`). On travaille toujours sur la donnée normalisée en RAW, et on nettoie en staging.

## Le pipeline

```
Source (Open Food Facts CSV)
    ↓
Ingestion Python → DuckDB (raw)
    ↓
Transformation dbt (staging → marts)
    ↓
Dashboard HTML
```

*(sections à compléter au fur et à mesure)*

## Ce que j'apprends

*(à remplir au fur et à mesure)*
