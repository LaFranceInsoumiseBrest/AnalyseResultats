#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 02:28:35 2025

@author: leolelonquer
"""
import json


with open("bureaux_contours/LIM_ADM_BureauxVote_s.geojson") as input_f:
    feat_collection_brest = json.load(input_f)



bureaux_brest = {}
for feature in feat_collection_brest["features"]:
    codeBureauVote = feature["properties"]["DEPCO"] + "_" + str(feature["properties"]["BVOTE"]).rjust(4, "0")
    LLIEU = feature["properties"]["LLIEU"]
    feature["properties"] = {"codeBureauVote": codeBureauVote,
                             "llieu": LLIEU}
    bureaux_brest[codeBureauVote] = (feature["geometry"], LLIEU)
    
with open("bureaux_contours/brest_contours.geojson", "w") as output_f:
    _ = json.dump(feat_collection_brest, output_f, ensure_ascii=False, indent=2)



# with open("bureaux_contours/features_circos23_v1.geojson") as input_f:
#     feat_collection_circos = json.load(input_f)

# for feature in filter(lambda feat: feat["properties"]["nomCommune"] == "Brest", feat_collection_circos["features"]):
#     codeBureauVote = feature["properties"]["codeBureauVote"]
    
#     feature["geometry"], feature["properties"]["llieu"] = bureaux_brest[codeBureauVote]
    
# with open("bureaux_contours/features_circos23_v2.geojson", "w") as output_f:
#     _ = json.dump(feat_collection_circos, output_f, ensure_ascii=False, indent=2)




with open("bureaux_contours/features29_v1.geojson") as input_f:
    feat_collection_dept29 = json.load(input_f)

for feature in filter(lambda feat: feat["properties"]["nomCommune"] == "Brest", feat_collection_dept29["features"]):
    codeBureauVote = feature["properties"]["codeBureauVote"]
    
    feature["geometry"], feature["properties"]["llieu"] = bureaux_brest[codeBureauVote]
    
with open("bureaux_contours/features29_v2.geojson", "w") as output_f:
    _ = json.dump(feat_collection_dept29, output_f, ensure_ascii=False, indent=2)