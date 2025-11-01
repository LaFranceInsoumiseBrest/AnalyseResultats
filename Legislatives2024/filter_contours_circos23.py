import json

# Transform json input to python objects
with open("/home/llelonqu/Téléchargements/contours-france-entiere-latest-v2.geojson") as input_f:
    feat_collection = json.load(input_f)

features29 = [feat for feat in feat_collection["features"] if feat["properties"]["codeCirconscription"] == "2902" or feat["properties"]["codeCirconscription"] == "2903"]

feat_collection["features"] = features29

with open('Legislatives2024/bureaux_contours/features_circos23.geojson', 'w') as f:
    json.dump(feat_collection, f, ensure_ascii=False, indent=2)


