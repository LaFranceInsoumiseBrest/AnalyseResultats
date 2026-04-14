import pandas as pd
import matplotlib
from collections import defaultdict
from copy import deepcopy

#import geopandas as gpd
import json

options_score = {}
options_geometry = {}
participation = True
# participation_color_map = 'RdYlGn'
participation_color_map = 'brg'

# Brest
score_file = 'brest_delta_inscrits.csv'
geometry_file = 'contoursBV2026Brest.geojson'
output_file = 'delta_inscrits.geojson'
color = 'Purple'


df = pd.read_csv(score_file, dtype='str', sep=';')


# Prétaitement données
# Transformer chaque ligne en élément de dictionnaire avec 
# La clef :  codeCommune + '_' + padding(4chiffre, BV)    (équivalent à codeBureauVote dans feature) 
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
# Rajouter un marqueur pour l'abstention au centrer de la zone ?


# def generate_description(df):
#     title = df['Code BV']
#     stats_bv = ('Inscrits : ' + df['Inscrits'] + '\n' + 'Participation : ' + df['% Votants']  + '\n' + 'Blancs : ' + df['Blancs']).rename('stats_bv')


def delta_to_color(delta, colormap='RdBu', rev=False, percent_offset=0.5, scale=50):
    percentage = delta/scale 
    cmap = matplotlib.colormaps[colormap]
    offset = round(cmap.N * percent_offset)
    if not rev:
        idx_color = min(cmap.N - 1, offset + round((cmap.N - offset) * percentage))
    else:
        idx_color = max(0, round((cmap.N - offset)*((1 - percentage)*100)/100))

    return matplotlib.colors.rgb2hex(cmap(idx_color))



df = df.drop(df[df['Code BV'] == 'Total'].index)
df = df.astype(float).astype(int)
# df['Code BV'] = pd.to_numeric(df['Code BV'])
df = df.set_index('Code BV')
df.at[79, 'Inscrits.delta'] = 0
df.at[105, 'Inscrits.delta'] = 0

df['color'] = pd.to_numeric(df['Inscrits.delta']).map(delta_to_color)
df['des'] = 'Euro 2024 : ' + df['Inscrits.euro'].astype(str)\
            + '\nMunicipales 2026 : ' + df['Inscrits.muni'].astype(str)\
            + '\nDelta : ' + df['Inscrits.delta'].astype(str)

#print(edf)

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


with open(geometry_file) as input_f:
    feat_collection = json.load(input_f)


feat_iterator = iter(feat_collection['features']) 

new_features = []
for feature in feat_iterator:
    codeBV = feature['properties']['BVOTE']
    llieu = feature['properties'].get('LLIEU', None)
    if codeBV in df.index and llieu: 
        name = 'Bureau ' + str(codeBV) + ' - ' + llieu
        umap_option = {'fillColor': df.loc[codeBV]['color'],
                        "fillOpacity" : 0.7,
                        'color': 'Black', 'weight': 1}

        new_prop = {'name': name,
                    'description': df.loc[codeBV]['des'],
                    '_umap_options': umap_option}
    # else:
    #     name = feature['properties']['nomCommune'] + ' - ' + feature['properties']['codeBureauVote'].split('_')[1]
    #     new_prop = {'name': name,
    #                 'description': 'AUCUNE DONNEE INSEE',
    #                 '_umap_options': {'fillColor': 'White',
    #                                 'fillOpacity': 0,
    #                                 'color': 'White', 'weight': 1}}
    
    feature['properties'] = new_prop
    new_features.append(feature)

feat_collection['features'] = new_features

with open(output_file, 'w') as output_f:
    _ = json.dump(feat_collection, output_f, ensure_ascii=False, separators=(',', ':'))