import pandas as pd
import matplotlib
import matplotlib.colors
from copy import deepcopy
import json

tour1_file = "brest-2026-municipales-bv-tour1.csv"
tour2_file = "brest-2026-municipales-bv-tour2.csv"
geometry_file = "contoursBV2026Brest.geojson"
output_file = "brest_diff_participation.geojson"

# Colormap divergent : rouge = baisse, vert = hausse
colormap = "PuOr"
max_diff = 10  # points de pourcentage max pour l'échelle de couleur


def parse_percent(val):
    """Convertit '62,09 %' ou '65,11%' en float."""
    return float(str(val).strip().rstrip('%').strip().replace(',', '.'))


def load_participation(csv_file):
    df = pd.read_csv(csv_file, dtype="str", sep=";")
    code_bv = (df["Code commune"].str.zfill(5) + "_" + df["Code BV"].str.strip().str.zfill(4)).rename("codeBureauVote")
    participation = df["% Votants"].map(parse_percent).rename("participation")
    inscrits = df["Inscrits"].rename("inscrits")
    votants = df["Votants"].rename("votants")
    return pd.concat((code_bv, participation, inscrits, votants), axis=1).set_index("codeBureauVote")


def diff_to_color(diff, max_diff=20):
    cmap = matplotlib.colormaps[colormap]
    normalized = (diff + max_diff) / (2 * max_diff)
    normalized = max(0.0, min(1.0, normalized))
    idx = round(normalized * (cmap.N - 1))
    return matplotlib.colors.rgb2hex(cmap(idx))


# Chargement des données
t1 = load_participation(tour1_file)
t2 = load_participation(tour2_file)

# Fusion sur l'index commun
merged = t1.join(t2, lsuffix="_t1", rsuffix="_t2", how="inner")
merged["diff"] = merged["participation_t2"] - merged["participation_t1"]

print(f"Bureaux de vote traités : {len(merged)}")
print(f"Différence moyenne : {merged['diff'].mean():.2f} pts")
print(f"Min : {merged['diff'].min():.2f} pts — Max : {merged['diff'].max():.2f} pts")

# Chargement du geojson
with open(geometry_file) as f:
    feat_collection = json.load(f)

new_features = []
for feature in feat_collection["features"]:
    codeBV = str(feature["properties"]["DEPCO"]) + "_" + str(feature["properties"]["BVOTE"]).zfill(4)
    llieu = feature["properties"].get("LLIEU", None)

    if codeBV in merged.index:
        row = merged.loc[codeBV]
        diff = row["diff"]
        p1 = row["participation_t1"]
        p2 = row["participation_t2"]

        sign = "+" if diff >= 0 else ""
        name = f"Bureau {feature['properties']['BVOTE']}"
        if llieu:
            name = f"{name} - {llieu}"

        description = (
            f"Tour 1 : {p1:.2f}%\n"
            f"Tour 2 : {p2:.2f}%\n"
            f"Différence : {sign}{diff:.2f} pts\n\n"
            f"Inscrits T1 : {row['inscrits_t1']}  |  Votants T1 : {row['votants_t1']}\n"
            f"Inscrits T2 : {row['inscrits_t2']}  |  Votants T2 : {row['votants_t2']}"
        )

        fill_color = diff_to_color(diff, max_diff=max_diff)

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
