import arcgis
import geopandas as gpd
from shapely.validation import make_valid


def sdf_to_gdf(sdf):
    tmp = sdf.copy()
    tmp = tmp[~tmp['SHAPE'].isna()]
    gdf = gpd.GeoDataFrame(tmp, geometry=tmp["SHAPE"], crs=4326).set_index('objectid')
    gdf['geometry'] = gdf['geometry'].apply(lambda x: make_valid(x)) # try to fix any geoemtry issues
    gdf.drop(columns=['Shape__Area', 'Shape__Length', 'SHAPE'], errors='ignore', inplace=True)
    return gdf


gis = arcgis.gis.GIS("SERVER-URL", "USERNAME", "PASSWORD")
points_sdf = gis.content.get("FEATURE-SERVICE-ID").layers[0].query().sdf # todo: support multi-layers
points_gdf = sdf_to_gdf(points_sdf)

# todo: convert gdf to events
