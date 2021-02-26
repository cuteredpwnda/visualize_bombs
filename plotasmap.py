import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import utm
import re
import folium
import folium.plugins

#read the data
df = pd.read_csv('data/uebersichtslisteBombenfunde2017.csv', sep=';')

# rename Koordinate1 and Koordinate2 to match what they are:
df.rename(columns = {'Koordinate1': 'easting', 'Koordinate2': 'northing'}, inplace=True)

#rewrite with . instead of ,
for col in ['easting', 'northing']:
    df[col] = pd.to_numeric(df[col].apply(lambda x: re.sub(',' , '.', str(x))))
    
#clean zeroes in diffrent df
df_clean = df[df.easting != 0.00]

#clean nan
df_clean = df_clean.replace(np.nan, 'unbekannt', regex=True)

#fix wrong coordinates (too long, wrong decimal point probably)
df_clean['easting'] = df_clean['easting'].apply(lambda x: round(x/10,2) if (x >= 1000000) else x)
df_clean['northing'] = df_clean['northing'].apply(lambda x: round(x/10,2) if (x > 10000000) else x)


# create a new column:

df_clean['(easting, northing)'] = list(zip(df_clean['easting'], df_clean['northing']))

#create lists for easy access
easting = df_clean['easting'].values.tolist()
northing = df_clean['northing'].values.tolist()

debug = False
# debug prints, max and mins
if (debug == True):
    print('min, max easting')
    print(df_clean['easting'].min())
    print(df_clean['easting'].max())
    print('min, max northing')
    print(df_clean['northing'].min())
    print(df_clean['northing'].max())

#convert to lat/lon and int
# 32, U is roughly west germany
latlon_list = []
for i in range(len(easting)):
    latlon_list.append(utm.to_latlon(int(round(easting[i])), int(round(northing[i])), 32, 'U'))
    
df_clean['(lat,lon) WGS84'] = latlon_list

df_clean['lat WGS84'], df_clean['lon WGS84'] = zip(*df_clean['(lat,lon) WGS84'])

#print(df_clean)

# find the map center
lon_center = (df_clean['lon WGS84'].min()+df_clean['lon WGS84'].max())/2
lat_center = (df_clean['lat WGS84'].min()+df_clean['lat WGS84'].max())/2

# load map
map = folium.Map(location = [lat_center,lon_center],
                    tiles='openstreetmap',
                    zoom_start = 9)

#merge bombdata
df_clean['bombdata'] =  'Herkunft: ' + df_clean['Herkunft'] + ', Gewicht: ' + df_clean['Gewicht'].astype(str) + ', Bombentyp: ' + df_clean['Bombentyp']
print(df_clean['bombdata'])


# add markers
for idx, row in df_clean.iterrows():
    folium.Marker(location = [row['lat WGS84'], row['lon WGS84']], popup=row['Herkunft']).add_to(map)

# add buffers/exlosive radii

map.save("map.html")