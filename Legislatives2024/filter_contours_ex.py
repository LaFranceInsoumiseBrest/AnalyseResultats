import json

# Transform json input to python objects
#feat_collection = json.loads("/home/llelonqu/Téléchargements/contours-france-entiere-latest-v2.geojson")
with open("Legislatives2024/bureaux_contours/exemple.geojson") as input_f:
    feat_collection = json.load(input_f)


features01 = [feat for feat in feat_collection["features"] if feat["properties"]["codeDepartement"] == "01"]

feat_collection["features"] = features29

with open('Legislatives2024/bureaux_contours/features01_test.json', 'w') as f:
    json.dump(feat_collection, f, ensure_ascii=False, indent=4)


