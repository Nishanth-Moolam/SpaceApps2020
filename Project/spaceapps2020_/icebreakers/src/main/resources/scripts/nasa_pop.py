from osgeo import  gdal
import numpy as np
from math import floor

# nasa population density data
fp = 'gpw_v4_population_density_rev11_2020_2pt5_min.tif'
ds = gdal.Open(fp)

band1 = ds.ReadAsArray()

# example coords
lat, lon = 80.610295, -47.073086


def convert_latlong(lat, lon, w = 8640, h = 4320):
    '''
    takes in lattitude and longitude of the location, outputs pop density
    '''
    x = ((w/360.0) * (180 + lon))
    y = ((h/180.0) * (90 - lat))

    return floor(y),floor(x) 


x,y =  (convert_latlong(lat, lon))

print (band1[x][y])