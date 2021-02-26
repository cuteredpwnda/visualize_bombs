import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Proj, transform
import utm
import re

#read the data
df = pd.read_csv('data/uebersichtslisteBombenfunde2017.csv', sep=';')

# rename Koordinate1 and Koordinate2 to match what they are:
df.rename(columns = {'Koordinate1': 'Latitude', 'Koordinate2': 'Longitude'}, inplace=True)

#rewrite with . instead of ,
for col in ['Latitude', 'Longitude']:
    df[col] = pd.to_numeric(df[col].apply(lambda x: re.sub(',' , '.', str(x))))
    
#clean zeroes in diffrent df
df_clean = df[df.Latitude != 0.00]

#fix wrong coordinates (too long, wrong decimal point probably)
df_clean['Latitude'] = df_clean['Latitude'].apply(lambda x: round(x/10,2) if (x >= 1000000) else x)
df_clean['Longitude'] = df_clean['Longitude'].apply(lambda x: round(x/10,2) if (x >= 1000000) else x)
# twice, because at least one coordinate seems to be wrong by 2 decimal points
df_clean['Longitude'] = df_clean['Longitude'].apply(lambda x: round(x/10,2) if (x >= 1000000) else x)

debug = False
# debug prints, max and mins
if (debug == True):
    print('min, max Latitude')
    print(df_clean['Latitude'].astype(int).min())
    print(df_clean['Latitude'].min())
    print(df_clean['Latitude'].astype(int).max())
    print(df_clean['Latitude'].max())
    print('min, max Longitude')
    print(df_clean['Longitude'].astype(int).min())
    print(df_clean['Longitude'].min())
    print(df_clean['Longitude'].astype(int).max())
    print(df_clean['Longitude'].max())

# create a new column:
df_clean['Latitude, Longitude (as UTM)'] = list(zip(df_clean['Latitude'], df_clean['Longitude']))
column_latlon = df_clean['Latitude, Longitude (as UTM)']
print('Latitude, Longitude (as UTM): ')
print(column_latlon)

#convert to lat/lon and int
# 32, U is west germany

print(df_clean)


# find the map boundaries
#BBox = (df_clean.Latitude.min(), df_clean.Latitude.max(),
#            df_clean.Longitude.min(), df_clean.Longitude.max())

# load map
#bomb_map = plt.imread('data/map.png')