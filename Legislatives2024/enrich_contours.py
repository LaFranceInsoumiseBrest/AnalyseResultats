import pandas as pd
import matplotlib
from collections import defaultdict

#import geopandas as gpd
import json

options_score = {}
options_geometry = {}

# circos29-23-tour1
# score_file = "bureaux_resultats/29-2-3/circos23-tour1.csv"
# geometry_file = "bureaux_contours/features_circos23_v2.geojson"
# output_file = "results/circos23_tour1.geojson"
# opacity_offset = 0
# opacity_factor = 1.5
# color_UG = "#ff0000" # rouge

# circos29-23-tour2
# score_file = "bureaux_resultats/29-2-3/circos23-tour2.csv"
# geometry_file = "bureaux_contours/features_circos23_v2.geojson"
# output_file = "results/circos23_tour2.geojson"
# opacity_offset = 0
# opacity_factor = 1.5
# color_UG = "#ff0000" # rouge

# dept29-tour1
# score_file = "bureaux_resultats/France/resultats-definitifs-par-bureau-de-vote-tour1.csv"
# geometry_file = "bureaux_contours/features29_v2.geojson"
# output_file = "results/dept29_tour1.geojson"
# opacity_offset = 0
# opacity_factor = 1.5
# color_UG = "Purple"
# options_score["filter"] = ("Code département", "29")

# dept29-tour2
score_file = "bureaux_resultats/France/resultats-definitifs-par-bureau-de-vote-tour2.csv"
geometry_file = "bureaux_contours/features29_v2.geojson"
output_file = "results/dept29_tour2.geojson"
opacity_offset = 0
opacity_factor = 1.5
color_UG = "Purple"
options_score["filter"] = ("Code département", "29")

# Dept 01 test
# score_file = "bureaux_resultats/France/resultats-definitifs-par-bureau-de-vote-tour1.csv"
# geometry_file = "/Users/leolelonquer/Desktop/contours-france-entiere-latest-v2.geojson"
# output_file = "/Users/leolelonquer/Desktop/dept01_tour1.geojson"
# opacity_offset = 0
# opacity_factor = 1.5
# color_UG = "Purple"
# options_score["filter"] = ("Code département", "1")
# options_geometry["filter"] = ("codeDepartement", "01")

# france-tour1
# score_file = "bureaux_resultats/France/resultats-definitifs-par-bureau-de-vote-tour1.csv"
# geometry_file = "/Users/leolelonquer/Desktop/contours-france-entiere-latest-v2.geojson"
# output_file = "/Users/leolelonquer/Desktop/france_tour1.geojson"
# opacity_offset = 0
# opacity_factor = 1.5
# color_UG = "Purple"

# france-tour2
# score_file = "bureaux_resultats/France/resultats-definitifs-par-bureau-de-vote-tour2.csv"
# geometry_file = "/Users/leolelonquer/Desktop/contours-france-entiere-latest-v2.geojson"
# output_file = "/Users/leolelonquer/Desktop/france_tour2.geojson"
# opacity_offset = 0
# opacity_factor = 1.5
# color_UG = "Purple"

color_mapping = {
    "EXG": "#cc0066", # rouge mauve
    "COM": "#993333", # rouge brun
    "FI": "Purple",
    "SOC": "#ff0066", # rose foncé
    "RDG": "#ff3355", # rose
    "VEC": "#00cc00", # vert 
    "DVG": "#ff6666", # rose léger
    "UG": color_UG, # violet ou rouge
    "ECO": "#66ff33", # vert clair
    "REG": "#800000", # marron
    "DIV": "#00ffcc", # cyan
    "REN": "#cdcd0d", # jaune caca d'oie
    "MDM": "#ff9933", # orange
    "HOR": "#0033cc", # bleu marine
    "ENS": "#cdcd0d", # jaune caca d'oie
    "DVC": "#cc9900", # moutarde
    "UDI": "#cc9900",  # moutarde
    "LR": "#000099", # bleu foncé
    "DVD": "#0099ff", # bleu léger
    "DSV": "#6666ff", # bleu violet
    "RN": "#333333", # gris foncé
    "REC": "#000000", # noir
    "UXD": "#000000", # noir
    "EXD": "#000000", # noir
}


# https://matplotlib.org/stable/users/explain/colors/colormaps.html
# colormap_mapping = {
#     "EXG": "Reds",
#     "COM": "Reds",
#     "FI": "Purples",
#     "SOC": "spring",
#     "RDG": "spring",
#     "VEC": "Greens",
#     "DVG": "Oranges",
#     "UG": "Reds",
#     "ECO": "YlGn",
#     "REG": "Wistia",
#     "DIV": "Wistia",
#     "REN": "cividis",
#     "MDM": "cividis",
#     "HOR": "Blues",
#     "ENS": "cividis",
#     "DVC": "cividis",
#     "UDI": "cividis",
#     "LR": "Blues",
#     "DVD": "Blues",
#     "DSV": "Blues",
#     "RN": "Greys",
#     "REC": "Greys",
#     "UXD": "Greys",
#     "EXD": "Greys",
# }




def sort_candidats(line_with_na):
    line = line_with_na.dropna()
    candidats = line.filter(regex=r"^Nom candidat").rename(lambda name: name.replace("Nom candidat ", ""))
    nuances = line.filter(regex=r"^Nuance candidat").rename(lambda name: name.replace("Nuance candidat ", ""))
    voix = line.filter(regex=r"^Voix \d{1,2}$").rename(lambda name: name.replace("Voix ", "")).astype(int)
    voix_pourcent = line.filter(regex=r"^% Voix/inscrits ").rename(lambda name: name.replace("% Voix/inscrits ", ""))
    
    sorted_voix_index = list(voix.sort_values(ascending=False).keys())
    winner_index = sorted_voix_index[0]
    results = []
    for index in sorted_voix_index[:4]:
        results.append(
            " - ".join((nuances[index], candidats[index], voix_pourcent[index], str(voix[index])))
            )
    
    return pd.Series((nuances[winner_index],
                      float(voix_pourcent[winner_index].strip('%').replace(",", ".")),
                      "\n".join(results)), 
                     index=["winner", "winner_percent", "summary_candidats"])
    

def generate_description(df):
    title = (df["Libellé commune"] + " - Bureau " + df["Code BV"]).rename("title")
    stats_bv = ("Inscrits : " + df["Inscrits"] + "\n" + "Participation : " + df["% Votants"]  + "\n" + "Blancs : " + df["Blancs"]).rename("stats_bv")
    stats_candidats = df.apply(sort_candidats, axis=1)
    
    description = pd.concat((stats_candidats, stats_bv), axis=1)[["summary_candidats", "stats_bv"]].agg("\n\n".join, axis=1).rename("description")
    #"\n\n".join((title, stats_candidats["summary_candidats"], stats_bv))
    
    return pd.concat((title, stats_candidats[["winner", "winner_percent"]], description), axis=1)
    

def percentage_to_color(percentage, colormap, rev=False, percent_offset=0.5):
    cmap = matplotlib.colormaps[colormap]
    offset = round(cmap.N * percent_offset)
    if not rev:
        idx_color = min(cmap.N - 1, offset + round((cmap.N - offset) * percentage/100))
    else:
        idx_color = max(0, round((cmap.N - offset)*(100 - percentage)/100))

    return matplotlib.colors.rgb2hex(cmap(idx_color))



# Code département;Libellé département;Code commune;Libellé commune;Code BV;
# Inscrits;Votants;% Votants;Abstentions;% Abstentions;Exprimés;% Exprimés/inscrits;% Exprimés/votants;Blancs;% Blancs/inscrits;% Blancs/votants;Nuls;% Nuls/inscrits;% Nuls/votants;
# Numéro de panneau 1;Nuance candidat 1;Nom candidat 1;Prénom candidat 1;Sexe candidat 1;Voix 1;% Voix/inscrits 1;% Voix/exprimés 1;Elu 1;
# Numéro de panneau 2;Nuance candidat 2;Nom candidat 2;Prénom candidat 2;Sexe candidat 2;Voix 2;% Voix/inscrits 2;% Voix/exprimés 2;Elu 2;
# ...


df = pd.read_csv(score_file, dtype="str", sep=";")

if "filter" in options_score:
    key, value = options_score["filter"]
    df = df.loc[df[key] == value]


# Prétaitement données
# Transformer chaque ligne en élément de dictionnaire avec 
# La clef :  codeCommune + "_" + padding(4chiffre, BV)    (équivalent à codeBureauVote dans feature) 
# les valeurs :

# => Description :
# Brest - Bureau 28
# Mairie Centrale (optionnel si ya)

# UG - Cadalen - 39,87% - 250 voix
# DVC - Larsonneur -  18,18% - 114 voix
# ENS - Bréhier - 18.08% - 113 voix
# RN - Kervella - 16,59% - 104 voix

# Inscrits : 895 - Participation : 71,28% - Blancs : 11

# Couleur : celle du gagnant (avec une intensité ?)
# Contour : ?
# Rajouter un marqueur pour l"abstention au centrer de la zone ?

edf = pd.concat((
    (df["Code commune"].str.zfill(5) + "_" + df["Code BV"].str.zfill(4)).rename("codeBureauVote"),
    df["% Votants"].map(lambda val: float(val.strip('%').replace(",", "."))).rename("Participation"),
    generate_description(df)),
    axis=1).sort_values(by="codeBureauVote").set_index("codeBureauVote")



#pd.unique(pd.melt(df.filter(regex=r"^Nuance candidat")).dropna()["value"])
#array(['ENS', 'DIV', 'ECO', 'DVC', 'RN', 'LR', 'UG', 'REC', 'EXG', 'DSV',
#       'REG', 'EXD'], dtype=object)


# color_spec = defaultdict(lambda:(False, 0.5))
# color_spec["spring"] = (True, 0.5)
# color_spec["Wistia"] = (True, 0.5)
# color_spec["cividis"] = (False, 0.9)

# edf["winner_color"] = edf.apply(lambda s: percentage_to_color(s["winner_percent"], 
#                                                              colormap_mapping[s["winner"]], 
#                                                              rev=color_spec[colormap_mapping[s["winner"]]][0],
#                                                              percent_offset=color_spec[colormap_mapping[s["winner"]]][1]),
#                                 axis=1)


edf["winner_color"] = edf.apply(lambda s: color_mapping[s["winner"]], axis=1)




#print(edf)

# {
#     "type": "FeatureCollection",
#     "crs": {
#         "type": "name",
#         "properties": {
#             "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
#         }
#     },
#     "features": [
#         {
#             "type": "Feature",
#             "properties": {
#                 "codeDepartement": "01",
#                 "nomDepartement": "Ain",
#                 "codeCirconscription": "0104",
#                 "nomCirconscription": "4\u00e8me circonscription",
#                 "codeCommune": "01001",
#                 "nomCommune": "L'Abergement-Cl\u00e9menciat",
#                 "numeroBureauVote": "0001",
#                 "codeBureauVote": "01001_0001",
#                 "id_bv": "01001_1",
#                 "description": "Yololo",
#                 "_umap_options": {
#                     "color": "red"
#                 }
#             },

#             "geometry": {
#                 "type": "Polygon",
#                 "coordinates": [
#                     [
#                         [
#                             4.958121,
#                             46.153159
#                         ],


# if geometry_file.endswith("json"):
with open(geometry_file) as input_f:
    feat_collection = json.load(input_f)
# elif geometry_file.endswith("parquet"):
#     with open(geometry_file) as input_f:
#         feat_collection = json.load(input_f)

feat_iterator = iter(feat_collection["features"]) 
if "filter" in options_geometry:
    key, value = options_geometry["filter"]
    feat_iterator = filter(lambda feat: feat["properties"][key] == value, feat_iterator)

new_features = []
for feature in feat_iterator:
    codeBureauVote = feature["properties"]["codeBureauVote"]
    llieu = feature["properties"].get("llieu", None)
    if codeBureauVote in edf.index: 
        name = edf.loc[codeBureauVote]["title"]
        if llieu:
            name = name + " - " + llieu
        new_prop = {"name": name,
                    "description": edf.loc[codeBureauVote]["description"],
                    "_umap_options": {"fillColor": edf.loc[codeBureauVote]["winner_color"],
                                      "fillOpacity": min(1, opacity_offset + opacity_factor*(edf.loc[codeBureauVote]["winner_percent"])/100),
                                      "color": "White", "weight": 1}}
    else:
        name = feature["properties"]["nomCommune"] + " - " + feature["properties"]["codeBureauVote"].split("_")[1]
        new_prop = {"name": name,
                    "description": "AUCUNE DONNEE INSEE",
                    "_umap_options": {"fillColor": "White",
                                      "fillOpacity": 0,
                                      "color": "White", "weight": 1}}
    
    feature["properties"] = new_prop
    new_features.append(feature)

feat_collection["features"] = new_features

with open(output_file, "w") as output_f:
    _ = json.dump(feat_collection, output_f, ensure_ascii=False, separators=(',', ':'))

    


# # print(edf["color_winner"])









# import numpy as np
# vals = np.linspace(0, 100, num=100)

# print(list(map(lambda x: percentage_to_idx(x, "Wistia", rev=color_spec[colormap_mapping["REG"]][0]), vals)))
# #                                                              percent_offset=color_spec[colormap_mapping[s["winner"]]][1])), vals)))


# import numpy as np
# vals = np.linspace(0, 100, num=100)

# list(map(lambda x: percentage_to_color(x, "Reds"), vals))


# import numpy as np
# vals = np.linspace(0, 100, num=100)

# list(map(lambda idx: matplotlib.colors.rgb2hex(matplotlib.colormaps["Reds"](idx)), list(map(lambda x: percentage_to_idx(x, "Reds"), vals)))
# )





