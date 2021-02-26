import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Proj, transform
import utm
import re

#read the data
df = pd.read_csv('data/uebersichtslisteBombenfunde2017.csv', sep=';')
df.head()
#print(df)

#rewrite with . instead of ,
for col in ['Koordinate1', 'Koordinate2']:
    df[col] = pd.to_numeric(df[col].apply(lambda x: re.sub(',' , '.', str(x))))
#print(df)

#clean zeroes in diffrent df
df_clean = df[df.Koordinate1 != 0.00]

#convert to lat/lon and int
# 32, U is west germany
print(df_clean['Koordinate1'].astype(int))
df_clean.apply(utm.to_latlon(df_clean['Koordinate1'].astype(int), df_clean['Koordinate2'].astype(int), 32, 'U'))

# find the map boundaries
BBox = (df_clean.Koordinate1.min(), df_clean.Koordinate1.max(),
            df_clean.Koordinate2.min(), df_clean.Koordinate2.max())

# load map
bomb_map = plt.imread('data/map.png')