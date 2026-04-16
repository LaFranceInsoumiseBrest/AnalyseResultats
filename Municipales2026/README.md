# Installation et exécution

```bash
uv sync
uv run extract_brest_euro.py
```

# Scripts pour le différentiel Inscriptions Euros et Municipales

```bash
extract_brest_euro.py
extract_brest_municipales.py
gen_delta_inscrits_data.py
gen_delta_inscrits_map.py
```

# Script pour le score et la participation

```bash
enrich_contours.py
```

# Nuancier municipales

[Rappel nuances - Elections Municipales 2026 - Publication des candidatures et des résultats des élections en France](https://www.resultats-elections.interieur.gouv.fr/municipales2026/referentiel.html)


# Sources

- [Jeu de données - Elections municipales 2026 - Résultats du premier tour | data.gouv.fr](https://www.data.gouv.fr/datasets/elections-municipales-2026-resultats-du-premier-tour)
    - [Fichier csv](https://www.data.gouv.fr/api/1/datasets/r/)1428132c-ad5e-437e-a928-7c2a254e40eb
- [Jeu de données - Elections municipales 2026 - Résultats du second tour | data.gouv.fr](https://www.data.gouv.fr/datasets/elections-municipales-2026-resultats-du-second-tour)
    - [Fichier csv](https://www.data.gouv.fr/api/1/datasets/r/ac97f1d2-64b3-453e-90e6-485913aabd04 )
- [Jeu de données - Résultats des élections européennes du 9 juin 2024 | data.gouv.fr](https://www.data.gouv.fr/datasets/resultats-des-elections-europeennes-du-9-juin-2024)
    - [Fichier excel](https://www.data.gouv.fr/api/1/datasets/r/1996b2bc-e95a-4481-904f-28d16987fe61)
- [Bureaux de vote de Brest à partir du 01/01/2026 - Aperçu](https://geo.brest-metropole.fr/portal/home/item.html?id=f2c7736e6ab745f4930977a45c301714)
    - [Fichier shapefile](https://echanges.brest-metropole.fr/VIPDU72/GPB/LIM_ADM_BureauxVotePrj_s.zip)
    - [SHP to GeoJSON Converter Online | MyGeodata Cloud](https://mygeodata.cloud/converter/shp-to-geojson)