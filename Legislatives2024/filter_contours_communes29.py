import json

# Transform json input to python objects
with open("/Users/leolelonquer/Downloads/communes-50m.geojson") as input_f:
    feat_collection = json.load(input_f)

features29 = [feat for feat in feat_collection["features"] if feat["properties"]["departement"] == "29"]

feat_collection["features"] = features29
# feat_collection["features"]["properties"] = {}

with open('Legislatives2024/results/communes29.geojson', 'w') as f:
    json.dump(feat_collection, f, ensure_ascii=False, separators=(',', ':'))


