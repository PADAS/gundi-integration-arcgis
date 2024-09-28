import arcgis
import pandas as pd
import geopandas as gpd
from shapely.validation import make_valid

"""
Params:
    SERVER-URL: The AGOL URL
    USERNAME: AGOL Username
    PASSWORD: AGOL Password
    FEATURE-SERVICE-ID: The AGOL unique asset ID 
    TIMECOLUMN: The name of the time column representing the event 'time' 
"""

def sdf_to_gdf(sdf):
    tmp = sdf.copy()
    tmp = tmp[~tmp['SHAPE'].isna()]
    gdf = gpd.GeoDataFrame(tmp, geometry=tmp["SHAPE"], crs=4326).set_index('objectid')
    gdf['geometry'] = gdf['geometry'].apply(lambda x: make_valid(x)) # try to fix any geoemtry issues
    gdf.drop(columns=['Shape__Area', 'Shape__Length', 'SHAPE'], errors='ignore', inplace=True)
    return gdf


gis = arcgis.gis.GIS("SERVER-URL", "USERNAME", "PASSWORD")
points_sdf = gis.content.get("FEATURE-SERVICE-ID").layers[0].query().sdf # todo: support multi-layers
events = sdf_to_gdf(points_sdf)

events["location"] = pd.DataFrame({"longitude": events.geometry.x, "latitude": events.geometry.y}).to_dict(
            "records"
        )
del events["geometry"]

events["time"] = pd.to_datetime(events["TIMECOLUMN"])

events = events.to_dict("records")

# to-do: post events to Gundi based on the action runner status