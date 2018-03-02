import pandas as pd
from itertools import groupby
import operator
import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import numpy as np
import seaborn as sns
import math

# Reading the rain data from the rain_data.csv file
data = pd.read_csv('rain_data.csv')

# Extracting the rain data for one month
rain_value = pd.DataFrame({'name':data['DISTRICT'],
                            'value':data['DEC']})
                            
# Set index to district name. Helps in merging with map data
rain = rain_value.set_index('name')

# Create figure 
fig, ax = plt.subplots()
# Create a map with the coordinates determined by the Bounding Box tool
m = Basemap(projection='merc',lat_0=54.5, lon_0=-4.36,llcrnrlon=68.1, llcrnrlat= 6.5, urcrnrlon=97.4, urcrnrlat=35.5)
# Draw map boundary and set the color
m.drawmapboundary(fill_color='#46bcec')
# Fill continents and lakes
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
# Draw coast lines
m.drawcoastlines()

# Read india shape data
m.readshapefile('IND_adm_shp/IND_adm2','INDIA')

# Extract data from shape file
# we make a new dataframe which only contains district name and polygon data
map = pd.DataFrame({'name':[area['NAME_2'].upper() for area in m.INDIA_info],
                    'shapes':[Polygon(np.array(shape),True) for shape in m.INDIA]})

# Merging the rain data and map data
# new structure has three columns 'district name','polygon','rain value'
final = pd.merge(map,rain,left_on='name',right_index=True)

shapes = [Polygon(np.array(shape),True) for shape in m.INDIA]

# import color map
cmap = plt.get_cmap('Blues')

pc = PatchCollection(shapes,zorder=2)

# set facecolor according to value in data and colormap
pc.set_facecolor(cmap(final['value'].fillna(0).values))
ax.add_collection(pc)

# Set title for the plot
ax.set_title("DEC")

# Change plot size and font size
plt.rcParams['figure.figsize'] = (8,8)
plt.rcParams.update({'font.size': 20})
plt.show()

# Save plot to file 
plt.savefig('dec.png',bbox_inches='tight')