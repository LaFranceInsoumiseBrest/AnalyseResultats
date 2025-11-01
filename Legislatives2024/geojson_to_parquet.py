#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 13:03:42 2025

@author: leolelonquer
"""

import geopandas as gpd
contours = gpd.read_file("~/Desktop/contours-france-entiere-latest-v2.geojson")


contours.to_parquet("~/Desktop/contours-france-entiere-latest-v2.geoparquet")