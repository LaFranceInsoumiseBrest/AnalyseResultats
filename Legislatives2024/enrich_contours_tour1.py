import pandas as pd
import matplotlib
from collections import defaultdict

#import geopandas as gpd
import json

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
    stats_bv = ("Inscrits : " + df["Inscrits"] + " - " + "Participation : " + df["% Votants"]  + " - " + "Blancs : " + df["Blancs"]).rename("stats_bv")
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
df = pd.read_csv("bureaux_resultats/29-2-3/circos23-tour1.csv", dtype="str", sep=";")



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
    (df["Code commune"] + "_" + df["Code BV"].str.zfill(4)).rename("codeBureauVote"),
    df["% Votants"].map(lambda val: float(val.strip('%').replace(",", "."))).rename("Participation"),
    generate_description(df)),
    axis=1).sort_values(by="codeBureauVote").set_index("codeBureauVote")



#pd.unique(pd.melt(df.filter(regex=r"^Nuance candidat")).dropna()["value"])
#array(['ENS', 'DIV', 'ECO', 'DVC', 'RN', 'LR', 'UG', 'REC', 'EXG', 'DSV',
#       'REG', 'EXD'], dtype=object)

# https://matplotlib.org/stable/users/explain/colors/colormaps.html
color_mapping = {
    "EXG": "Reds",
    "COM": "Reds",
    "SOC": "spring",
    "RDG": "spring",
    "VEC": "Greens",
    "DVG": "Oranges",
    "UG": "Reds",
    "ECO": "YlGn",
    "REG": "Wistia",
    "DIV": "Wistia",
    "REN": "cividis",
    "MDM": "cividis",
    "HOR": "Purples",
    "ENS": "cividis",
    "DVC": "cividis",
    "UDI": "cividis",
    "LR": "Blues",
    "DVD": "Blues",
    "DSV": "Blues",
    "RN": "Greys",
    "REC": "Greys",
    "UXD": "Greys",
    "EXD": "Greys",
}

color_spec = defaultdict(lambda:(False, 0.5))
color_spec["spring"] = (True, 0.5)
color_spec["Wistia"] = (True, 0.5)
color_spec["cividis"] = (False, 0.9)

edf["winner_color"] = edf.apply(lambda s: percentage_to_color(s["winner_percent"], 
                                                             color_mapping[s["winner"]], 
                                                             rev=color_spec[color_mapping[s["winner"]]][0],
                                                             percent_offset=color_spec[color_mapping[s["winner"]]][1]),
                                axis=1)

print(edf)

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


with open("bureaux_contours/features_circos23_v2.geojson") as input_f:
    feat_collection = json.load(input_f)



for feature in feat_collection["features"]:
    codeBureauVote = feature["properties"]["codeBureauVote"]
    llieu = feature["properties"].get("llieu", None)
    name = edf.loc[codeBureauVote]["title"]
    if llieu:
        name = name + " - " + llieu
    feature["properties"] = {"name": name,
                             "description": edf.loc[codeBureauVote]["description"],
                             "_umap_options": {"fillColor": edf.loc[codeBureauVote]["winner_color"],
                                               "fillOpacity": min(1, 0.3 + (edf.loc[codeBureauVote]["winner_percent"])/100),
                                               "color": "Purple"}}
    

with open("results/circos23_tour1.geojson", "w") as output_f:
    _ = json.dump(feat_collection, output_f, ensure_ascii=False, separators=(',', ':'))

    


# # print(edf["color_winner"])









# import numpy as np
# vals = np.linspace(0, 100, num=100)

# print(list(map(lambda x: percentage_to_idx(x, "Wistia", rev=color_spec[color_mapping["REG"]][0]), vals)))
# #                                                              percent_offset=color_spec[color_mapping[s["winner"]]][1])), vals)))


# import numpy as np
# vals = np.linspace(0, 100, num=100)

# list(map(lambda x: percentage_to_color(x, "Reds"), vals))


# import numpy as np
# vals = np.linspace(0, 100, num=100)

# list(map(lambda idx: matplotlib.colors.rgb2hex(matplotlib.colormaps["Reds"](idx)), list(map(lambda x: percentage_to_idx(x, "Reds"), vals)))
# )





