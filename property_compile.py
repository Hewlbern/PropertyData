# import requests
import json



# import matplotlib.pyplot as plt
# import seaborn as sns

# from pandasdmx import Request
# from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
import pandas as pd
import numpy as np
import geopandas as gpd


import geopy.distance


import time

import csv

# import sys, os
# from sqlalchemy import create_engine

# import pymssql
# import sqlalchemy as db

# from functools import reduce

# import folium # map rendering library
# from sklearn.neighbors import NearestNeighbors




property_data_set = pd.read_csv('prop_data_set.csv')

shape_file_trains = "./shapefile/ptv_metro_train_station.shp"

trains_shape = gpd.read_file(shape_file_trains)


mwarp=property_data_set


# cartesian product so we get all combinations
dfdist = (mwarp.assign(foo=1).merge(trains_shape.assign(foo=1), on="foo")
    # calc distance in km between each suburb and each train station
     .assign(km=lambda dfa: dfa.apply(lambda r: 
                                      geopy.distance.geodesic(
                                          (r["LATITUDE"],r["LONGITUDE"]), 
                                          (r["lat"],r["lon"])).km, axis=1))
    # reduce number of columns to make it more digestable
     .loc[:,["postcode","address_street_full","STOP_ID","STOP_NAME","km"]]
    # sort so shortest distance station from a suburb is first
     .sort_values(["postcode","suburb","km"])
    # good practice
     .reset_index(drop=True)
)
# finally pick out stations nearest to suburb
# this can easily be joined back to source data frames as postcode and STOP_ID have been maintained
dfnearest = dfdist.groupby(["postcode","suburb"])\
    .agg({"STOP_ID":"first","STOP_NAME":"first","km":"first"}).reset_index()

# print(dfnearest.to_string(index=False))

dfnearest.to_csv("distances_station")
print(dfnearest)