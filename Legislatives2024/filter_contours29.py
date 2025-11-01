import json

# Transform json input to python objects
with open("/home/llelonqu/Téléchargements/contours-france-entiere-latest-v2.geojson") as input_f:
    feat_collection = json.load(input_f)

features29 = [feat for feat in feat_collection["features"] if feat["properties"]["codeDepartement"] == "29"]

feat_collection["features"] = features29

with open('Legislatives2024/bureaux_contours/features29.geojson', 'w') as f:
    json.dump(feat_collection, f, ensure_ascii=False, indent=2)


