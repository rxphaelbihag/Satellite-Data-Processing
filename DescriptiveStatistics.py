import os
import netCDF4 as nc
import numpy as np
import xarray as xr

file_path_Chla = r"C:\Users\Mary Grace Bihag\Desktop\Bayot Files\Grade 12\RES 3\Sardine Research\QGIS\Masking Chl-A (2012-2022)\Masked Chl-A"
file_path_SST = r"C:\Users\Mary Grace Bihag\Desktop\Bayot Files\Grade 12\RES 3\Sardine Research\QGIS\Masking SST (2012-2022)\Masked SST"

# get the file names inside a folder
def get_file_names(folder_path):
    """
    Function that gets the file names of all the files inside a folder.
    Returns a list 
    """

    file_names = []

    # Iterate through each item in the folder
    for item in os.listdir(folder_path):

        # Check if the item is a file (not a directory)
        if os.path.isfile(os.path.join(folder_path, item)):
            file_names.append(item)
    return file_names

def get_average(file_path):
    """ Function that only gets the mean of an nc file """
    average_data = []
    files = get_file_names(file_path)

    for file in files:
        ds = nc.Dataset(f"{file_path}\{file}")
        file_names = file.split("_")
        name = f"{file_names[2]}"
        avg = (ds.variables['Band1'][:]).mean()
        average_data.append([name, avg])
    
    return(average_data)

def get_bins_num(file_path):
    """ Function that only gets the number of bins of an nc file """
    bins_num = []
    files = get_file_names(file_path)

    for file in files:
        ds = nc.Dataset(f"{file_path}\{file}")
        file_names = file.split("_")
        name = f"{file_names[2]}"
        bin = (ds.data_bins)
        bins_num.append([name, bin])
    
    return(bins_num)

def get_min_max(file_path):
    """ Function that only gets the min and max of an nc file -> [name, min, max] """
    minmax = []
    files = get_file_names(file_path)

    for file in files:
        ds = nc.Dataset(f"{file_path}\{file}")
        file_names = file.split("_")
        name = f"{file_names[2]}"
        min = (ds.data_minimum)
        max = (ds.data_maximum)
        minmax.append([name, min, max])
    
    return(minmax)

def get_std(file_path):
    """ Function that only gets the standard deviation of an nc file """
    std_list = []
    files = get_file_names(file_path)

    for file in files:
        ds = (xr.open_dataset(f"{file_path}\{file}"))['Band1']
        file_names = file.split("_")
        name = f"{file_names[2]}"
        std = (ds.std())
        std_list.append([name, std])

def master(file_path, variable, datesimplified=True):
    """
    This function gets all the necessary statistics of an nc file:
        - mean (float)
        - minimum value (float)
        - maximum value (float)
        - standard deviation (float)
        - range of values 
        - upper quartile (float)
        - lower quartile (float)
        - number of bins (float) but actually is just an int
    
    """
    master_list = [['var-date', 'mean', 'min', 'max', 'std', 'range','qUpper', 'qLower', 'bin']] # initial element as headers
    
    files = get_file_names(file_path)
    q=(.25,.75)
    month_name = {
                    "01": "January",
                    "02": "February",
                    "03": "March",
                    "04": "April",
                    "05": "May",
                    "06": "June",
                    "07": "July",
                    "08": "August",
                    "09": "September",
                    "10": "October",
                    "11": "November",
                    "12": "December"
                }
    for file in files:
        pre_ds = xr.open_dataset(f"{file_path}\{file}") # opening the nc file
        ds = pre_ds['Band1'] # only reading the band of the variable
        
        file_names = file.split("_")
        if not datesimplified:
            name = f"{variable}-{file_names[2]}"
        else:
            year = file_names[2][0:4]
            month = month_name[str(file_names[2][4:6])]
            name = f"{month} {year}"

        avg = ds.mean().values
        min = ds.min().values
        max = ds.max().values
        std = ds.std().values
        range=  ds.max().values - ds.min().values
        qUpper = ds.quantile(q[1]).values
        qLower = ds.quantile(q[0]).values
        ds_nc = nc.Dataset(f"{file_path}\{file}")
        bin = (ds_nc.data_bins)
        master_list.append([name, float(avg), float(min), float(max), float(std), 
                            range, float(qUpper), float(qLower), float(bin)])
    print('Done')
    return(master_list)


"""Running the Master Function"""

chla_master = master(file_path_Chla, 'chla', True)
sst_master = master(file_path_SST, 'sst', True)


chla_master_array = np.array(chla_master)
sst_master_array = np.array(sst_master)

np.savetxt(r"C:\Users\Mary Grace Bihag\Desktop\Bayot Files\Grade 12\RES 3\Sardine Research\QGIS\new_data\chla-master-2012-2022.csv", chla_master_array, delimiter=",", fmt="%s")
np.savetxt(r"C:\Users\Mary Grace Bihag\Desktop\Bayot Files\Grade 12\RES 3\Sardine Research\QGIS\new_data\sst-master-2012-2022.csv", sst_master_array, delimiter=",", fmt="%s")