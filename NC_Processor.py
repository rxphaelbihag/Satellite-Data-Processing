import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from netCDF4 import Dataset
import os
import datetime


def transform_date(date_str):
    year = int(date_str[:4])
    month = int(date_str[4:])
    date_obj = datetime.date(year, month, 1)
    return date_obj.strftime('%b-%Y')


def create_graphs(folder_path=None, output_path=None, category=None, limit=None, colorbar=False):
    if folder_path == None:
        return print("Folder Path not specified")
    
    if category == None:
        return print("Category not specified. Must be either 'chla' or 'sst'.")
    
    if limit == None:
        return print("Limit not specified. Must be an integer or 'all'.")
    elif limit == 'none':
        limit = 999999

    # getting the first file of the folder to serve as basis
    filenames = os.listdir(folder_path)
    basis_file = f"{folder_path}/{filenames[0]}"
    basis_nc = Dataset(basis_file, 'r')

    files_count = len(filenames)

    lat = basis_nc.variables['lat'][:]
    lon = basis_nc.variables['lon'][:]
    basis_nc.close()

    projection = 'mill'
    lon_min, lon_max = lon.min(), lon.max()
    lat_min, lat_max = lat.min(), lat.max()
    plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    

    map = Basemap(projection=projection, llcrnrlon=lon_min, 
                urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max)

    map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') 

    spacing = 0.4
    parallels = np.arange(lat_min,lat_max, spacing)
    meridians = np.arange(lon_min,lon_max, spacing)
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=8)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=8)
    
    lons,lats= np.meshgrid(lon,lat)
    x,y = map(lons,lats) 
    
    annotations = {'Dipolog City': [123.328484, 8.524918],
                   'Sindangan': [123.0114, 8.2334], 
                   'Labason': [122.535164, 8.028969], 
                   'Siocon': [122.1973, 7.6636]}
    for place in annotations:
        xi, yi = map(annotations[place][0], annotations[place][1])
        plt.plot(xi, yi, marker='o', markersize=2.5, color='red', linestyle='None')
        ax.annotate(place,
                    xy=(xi, yi), xycoords='data',
                    xytext=map(annotations[place][0]+0.03, annotations[place][1]-0.01),
                    horizontalalignment='left',
                    verticalalignment='top',fontsize=9)

    counter = 0
    for filename in filenames:
        if filename[-2:] == "nc" and counter != limit:
            counter += 1

            focus_file = f"{folder_path}/{filename}"
            focus_nc = Dataset(focus_file, 'r')
            
            data = focus_nc.variables['Band1']
            
            ax.autoscale(False)
            if category == 'sst':
                plt.suptitle('Sea Surface Temperature', fontsize=18)
                vmin = 25
                vmax = 33
                date = filename[11:17]
            elif category == 'chla':
                plt.suptitle('Chlorophyll-a Concentration', fontsize=18)
                vmin = 0
                vmax = 10
                date = filename[12:18]
            
            variable_data = map.pcolor(x,y,data[:,:], cmap='viridis', vmin=vmin, vmax=vmax)

            if colorbar:
                cb = map.colorbar(variable_data,"bottom", size="5%", pad="10%")
                if category == 'sst':
                    cb.set_label('SST ($\mathregular{°C}$)')
                elif category == 'chla':
                    cb.set_label('Chlorophyll-a ($\mathregular{mg/m^3}$)')
            
            os.makedirs(f"{output_path}\{category}", exist_ok=True)

            plt.title(transform_date(date), fontsize=10)
            plt.savefig(f"{output_path}\{category}\{category}_{date}.png", dpi=200, bbox_inches='tight', pad_inches=0.2)
            print("DONE", counter, "out of", files_count)

create_graphs(folder_path="Masked\Masked Chl-A", output_path="Output", category='chla', limit='all', colorbar=True)