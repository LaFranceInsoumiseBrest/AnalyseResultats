import pandas as pd
import matplotlib
import matplotlib.colors
from copy import deepcopy
import json

euro_file = "brest-2024-euro-bv.csv"
muni_file = "brest-2026-municipales-bv-tour1.csv"
geometry_file = "contoursBV2026Brest.geojson"
output_file = "brest_diff_score_euro.geojson"

# Colormap divergent : rouge = baisse, vert = hausse
colormap = "seismic"
max_diff = 20  # points de pourcentage max pour l'échelle de couleur


def parse_percent(val):
    """Convertit '62,09 %' ou '65,11%' en float."""
    return float(str(val).strip().rstrip('%').strip().replace(',', '.'))


def load_score(csv_file, rank):
    df = pd.read_csv(csv_file, dtype="str", sep=";")
    code_bv = (df["Code commune"].str.zfill(5) + "_" + df["Code BV"].str.strip().str.zfill(4)).rename("codeBureauVote")
    score_fi = df[f"% Voix/inscrits {rank}"].map(parse_percent).rename("score_fi")
    voix_fi = df[f"Voix {rank}"].astype(float).astype(int).rename("voix_fi")

    inscrits = df["Inscrits"].rename("inscrits")
    votants = df["Votants"].rename("votants")
    return pd.concat((code_bv, score_fi, voix_fi, inscrits, votants), axis=1).set_index("codeBureauVote")


def diff_to_color(diff, max_diff=20, reverse=False):
    cmap = matplotlib.colormaps[colormap]
    normalized = (diff + max_diff) / (2 * max_diff)
    normalized = max(0.0, min(1.0, normalized))
    idx = round(normalized * (cmap.N - 1))
    if reverse:
        idx = cmap.N - idx
    return matplotlib.colors.rgb2hex(cmap(idx))


# Chargement des données
euro = load_score(euro_file, 4)
muni = load_score(muni_file, 2)

# Fusion sur l'index commun
merged = muni.join(euro, lsuffix="_muni", rsuffix="_euro", how="inner")
merged["diff_score"] = merged["score_fi_muni"] - merged["score_fi_euro"]
merged["diff_voix"] = merged["voix_fi_muni"] - merged["voix_fi_euro"]

print(f"Bureaux de vote traités : {len(merged)}")
print(f"Différence moyenne : {merged['diff_score'].mean():.2f} pts")
print(f"Min : {merged['diff_score'].min():.2f} pts — Max : {merged['diff_score'].max():.2f} pts")

# Chargement du geojson
with open(geometry_file) as f:
    feat_collection = json.load(f)

new_features = []
for feature in feat_collection["features"]:
    codeBV = str(feature["properties"]["DEPCO"]) + "_" + str(feature["properties"]["BVOTE"]).zfill(4)
    llieu = feature["properties"].get("LLIEU", None)

    if codeBV in merged.index:
        row = merged.loc[codeBV]
        diff = row["diff_score"]
        s1 = row["score_fi_euro"]
        s2 = row["score_fi_muni"]

        sign = "+" if diff >= 0 else ""
        name = f"Bureau {feature['properties']['BVOTE']}"
        if llieu:
            name = f"{name} - {llieu}"

        description = (
            f"Score FI Euro : {s1:.2f}%\n"
            f"Score FI Muni : {s2:.2f}%\n"
            f"Différence : {sign}{diff:.2f} pts\n\n"
            f"Euro :\nInscrits : {row['inscrits_euro']} ; Voix FI : {row['voix_fi_euro']}\n"
            f"Muni :\nInscrits : {row['inscrits_muni']} ; Voix FI : {row['voix_fi_muni']}"

        )

        fill_color = diff_to_color(diff, max_diff=max_diff, reverse=True)

        umap_option = {
            "fillColor": fill_color,
            "fillOpacity": 0.75,
            "color": "Black",
            "weight": 1
        }
        new_prop = {"name": name, "description": description, "_umap_options": umap_option}
    else:
        name = feature["properties"]["TITRE"]
        new_prop = {
            "name": name,
            "description": "AUCUNE DONNEE",
            "_umap_options": {"fillColor": "White", "fillOpacity": 0, "color": "White", "weight": 1}
        }

    feature["properties"] = new_prop
    new_features.append(feature)

feat_collection["features"] = new_features

with open(output_file, "w") as f:
    json.dump(feat_collection, f, ensure_ascii=False, separators=(',', ':'))

print(f"Fichier généré : {output_file}")
