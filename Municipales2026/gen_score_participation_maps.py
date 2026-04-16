import pandas as pd
import matplotlib
from collections import defaultdict
from copy import deepcopy

#import geopandas as gpd
import json

options_score = {}
options_geometry = {}
participation = True
# participation_color_map = "RdYlGn"
participation_color_map = "brg"


# Brest tour1
# score_file = "brest-2026-municipales-bv-tour1.csv"
# geometry_file = "contoursBV2026Brest.geojson"
# output_file = "brest_tour1.geojson"
# opacity_offset = 0
# opacity_factor = 1.5

# Brest tour2
score_file = "brest-2026-municipales-bv-tour2.csv"
geometry_file = "contoursBV2026Brest.geojson"
output_file = "brest_tour2.geojson"
opacity_offset = 0
opacity_factor = 1.5


# https://matplotlib.org/stable/users/explain/colors/colormaps.html
color_mapping = {
  "LEXG": "#8B0000",   # Rouge sang (extrême-gauche)
  "LFI": "#CC0033",    # Rouge vif (La France Insoumise)
  "LCOM": "#CC0000",   # Rouge pur (Parti communiste)
  "LSOC": "#E75480",   # Rose foncé (Parti socialiste)
  "LVEC": "#2E8B57",   # Vert forêt (Les Écologistes)
  "LUG": "#f79502",    # Orange (union gauche)
  "LDVG": "#F06292",   # Rose clair (divers gauche)
  "LECO": "#4CAF50",   # Vert moyen (écologiste)
  "LREG": "#9E9E9E",   # Gris moyen (régionaliste)
  "LDIV": "#BDBDBD",   # Gris clair (divers)
  "LREN": "#FFEB3B",   # Jaune vif (Renaissance)
  "LMDM": "#FF8F00",   # Orange ambré (MoDem)
  "LHOR": "#FF6D00",   # Orange vif (Horizons)
  "LUDI": "#29B6F6",   # Bleu ciel (UDI)
  "LUC": "#90CAF9",    # Bleu pâle (union centre)
  "LDVC": "#B0BEC5",   # Gris bleuté (divers centre)
  "LLR": "#283593",    # Bleu indigo (Les Républicains)
  "LUD": "#0D47A1",    # Bleu foncé (union droite)
  "LDVD": "#1565C0",   # Bleu marine (divers droite)
  "LDSV": "#4A148C",   # Violet foncé (droite souverainiste)
  "LUDR": "#311B92",   # Indigo profond (union droites)
  "LRN": "#000000",    # Noir (Rassemblement National)
  "LREC": "#1A1A8C",   # Bleu très sombre (Reconquête)
  "LUXD": "#0D0D5C",   # Bleu quasi-noir (union extrême-droite)
  "LEXD": "#050520"    # Noir bleuté (extrême-droite)
}

def sort_candidats(line_with_na):
    line = line_with_na.dropna()
    candidats = line.filter(regex=r"^Nom candidat").rename(lambda name: name.replace("Nom candidat ", ""))
    nuances = line.filter(regex=r"^Nuance liste").rename(lambda name: name.replace("Nuance liste ", ""))
    voix = line.filter(regex=r"^Voix \d{1,2}$").rename(lambda name: name.replace("Voix ", "")).astype(float).astype(int)
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

# Couleur : celle du gagnant avec une intensité
# Contour : ?

edf = pd.concat((
    (df["Code commune"].str.zfill(5) + "_" + df["Code BV"].str.zfill(4)).rename("codeBureauVote"),
    df["% Votants"].map(lambda val: float(val.strip('%').replace(",", "."))).rename("Participation"),
    generate_description(df)),
    axis=1).sort_values(by="codeBureauVote").set_index("codeBureauVote")

edf["winner_color"] = edf.apply(lambda s: color_mapping[s["winner"]], axis=1)


# {
#     'type': 'FeatureCollection',
#     'features': [
#         {
#             'type': 'Feature',
#             'geometry': {
#                 'bbox': [ -4.467799026052708, 48.40590695198066, -4.4542968121928235, 48.411793859916486 ],
#                 'type': 'Polygon',
#                 'coordinates': [ [ [ -4.456571978753705, 48.4116504213112 ], [ -4.456106163989778, 48.411265523324005 ], [ -4.456036567875838, 48.41122350843274 ], [ -4.455299202570836, 48.41118662802181 ], [ -4.45499238483136, 48.411024512342124 ], [ -4.454406489954987, 48.411204236266755 ], [ -4.4543477920733645, 48.411168336360824 ], [ -4.454193350176426, 48.41106638992977 ], [ -4.455128576045424, 48.41042942917826 ], [ -4.455775788240711, 48.410002226319676 ], [ -4.4563119427945095, 48.40966719837544 ], [ -4.456463344265997, 48.4095725908546 ], [ -4.456698251387081, 48.409404955737635 ], [ -4.458742969603161, 48.4080882459214 ], [ -4.461515695566452, 48.40630362361585 ], [ -4.462079966070214, 48.40740553453414 ], [ -4.462572296182224, 48.40729955803299 ], [ -4.462795784735131, 48.407689245747164 ], [ -4.464240536916852, 48.407319345155834 ], [ -4.464233768923311, 48.40730557812081 ], [ -4.4640095997742355, 48.4068967934188 ], [ -4.464952050556808, 48.40664302781563 ], [ -4.465240022789354, 48.40705434656084 ], [ -4.465246347025203, 48.40706181301747 ], [ -4.467867919285589, 48.40639052314131 ], [ -4.467887262137548, 48.40706892895477 ], [ -4.467853965211186, 48.407621716250084 ], [ -4.467959722137905, 48.40877124222982 ], [ -4.4674416954919325, 48.40882275054214 ], [ -4.464076340846234, 48.40970700308105 ], [ -4.464048872156363, 48.40971421961876 ], [ -4.459635003444118, 48.4108571347554 ], [ -4.457778153048349, 48.41132965100535 ], [ -4.457262456077244, 48.41152300969446 ], [ -4.457239005475826, 48.41150325925802 ], [ -4.456931373644152, 48.41158406525831 ], [ -4.456571978753705, 48.4116504213112 ] ] ] },
#             'properties': {
#                 'DEPCO': '29019',
#                 'LIEUV': 'GS KERBERN',
#                 'LLIEU': 'GS KERBERNARD',
#                 'TITRE': 'Bureau n° 58 - GROUPE SCOLAIRE KERBERNARD',
#                 'BVOTE': 58,
#                 'CANTO': 5,
#                 'DT_VIGUEUR': '2025-12-31T23:00:00.000Z',
#                 'TITRE2': 'GROUPE SCOLAIRE KERBERNARD',
#                 'SHAPE_AREA': 279359.021381,
#                 'SHAPE_LEN': 2855.9283909
#             }
#         },


# if geometry_file.endswith("json"):
with open(geometry_file) as input_f:
    feat_collection = json.load(input_f)
# elif geometry_file.endswith("parquet"):
#     with open(geometry_file) as input_f:
#         feat_collection = json.load(input_f)

if participation:
    feat_collection2 = deepcopy(feat_collection)

def color_and_write_feature_collection(feat_collection, criterion="Nuance"):
    feat_iterator = iter(feat_collection["features"]) 
    if "filter" in options_geometry:
        key, value = options_geometry["filter"]
        feat_iterator = filter(lambda feat: feat["properties"][key] == value, feat_iterator)

    new_features = []
    for feature in feat_iterator:
        codeBureauVote = str(feature["properties"]["DEPCO"]) + "_" + str(feature["properties"]["BVOTE"]).zfill(4)
        llieu = feature["properties"].get("LLIEU", None)
        if codeBureauVote in edf.index: 
            name = edf.loc[codeBureauVote]["title"]
            if llieu:
                name = name + " - " + llieu

            if criterion == "Nuance":
                umap_option = {"fillColor": edf.loc[codeBureauVote]["winner_color"],
                               "fillOpacity": min(1, opacity_offset + opacity_factor*(edf.loc[codeBureauVote]["winner_percent"])/100),
                               "color": "Black", "weight": 1}
            elif criterion == "Participation":
                umap_option =  {"fillColor": percentage_to_color(edf.loc[codeBureauVote]["Participation"], 
                                                                 participation_color_map, rev=False, percent_offset=0.3),
                                "fillOpacity" : 0.8,
                                "color": "Black", "weight": 1}

            new_prop = {"name": name,
                        "description": edf.loc[codeBureauVote]["description"],
                        "_umap_options": umap_option}
        else:
            name = feature["properties"]["TITRE"]
            new_prop = {"name": name,
                        "description": "AUCUNE DONNEE INSEE",
                        "_umap_options": {"fillColor": "White",
                                        "fillOpacity": 0,
                                        "color": "White", "weight": 1}}
        
        feature["properties"] = new_prop
        new_features.append(feature)

    feat_collection["features"] = new_features

    out = output_file
    if criterion == "Participation":
        name, extension = output_file.split(".")
        out = name + "_participation." + extension

    with open(out, "w") as output_f:
        _ = json.dump(feat_collection, output_f, ensure_ascii=False, separators=(',', ':'))


color_and_write_feature_collection(feat_collection)
if participation:
    color_and_write_feature_collection(feat_collection2, criterion="Participation")
