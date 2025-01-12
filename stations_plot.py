import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns

def add_north_arrow(ax):
  #print(plt.figsizezzg)
  py =650
  px =1200
  # Draw an arrow with a text "N" above it using annotation
  ax.annotate("N", xy=(px-10, py), fontsize=20, xycoords="figure pixels")
  ax.annotate("",  xy=(px,  py), xytext=(px, py-50),xycoords="figure pixels",
          arrowprops=dict(arrowstyle="-|>", facecolor="black",color="black"))

sns.set(style="whitegrid", palette="pastel", color_codes=True) 
sns.mpl.rc("figure", figsize=(10,6))


shp_path = "/home/ayush/Downloads/hermes_NPL_new_wgs/hermes_NPL_new_wgs_1.shp"
#reading the shape file by using reader function of the shape lib
sf = shp.Reader(shp_path)

print(len(sf.shapes()))
print(sf.records())

def read_shapefile(sf):
    #fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]
#fetching the records from the shape file
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
#converting shapefile data into pandas dataframe
    df = pd.DataFrame(columns=fields, data=records)
#assigning the coordinates
    df = df.assign(coords=shps)
    return df

df = read_shapefile(sf)
print(df.shape)
print(df)    
df=pd.read_csv('~/Downloads/rinex_stations.csv')
def plot_map(sf,df, x_lim = None, y_lim = None, figsize = (15,8)):
    plt.figure(figsize = figsize)
    id=0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')
        #if (x_lim == None) & (y_lim == None):
         #   x0 = np.mean(x)
          #  y0 = np.mean(y)
            #plt.text(x0, y0, id, fontsize=10)
        #id = id+1
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.scatter(df['Lon'].values,df['Lat'].values)    
    for i,site in enumerate(df['Site'].values):
        plt.annotate(site,((df['Lon'].values)[i],(df['Lat'].values)[i]))
    plt.xlabel('Longitude/°E')
    plt.ylabel('Latitude/°N')    
    add_north_arrow(plt)
#calling the function and passing required parameters to plot the full map
plot_map(sf,df)
plt.savefig('Station_location.png')
plt.show()