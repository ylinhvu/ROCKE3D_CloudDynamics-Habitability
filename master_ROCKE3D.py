import urllib
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from netCDF4 import Dataset

def download_ROCKE3D(dimension,user_dir,searchfor,exclude):
    # Scrape list of netCDF files from ROCKE-3D website
    url = 'https://portal.nccs.nasa.gov/GISS_modelE/ROCKE-3D/publication-supplements/Climates_of_Warm_Earth_like_Planets_I/'+dimension
    print('Searching in: ' + url)
    print('Downloading to: ' + user_dir)
    tables = pd.read_html(url,header=0, skiprows=2, keep_default_na=False)
    table = tables[2]
    
    # Filter files
    new_table = table['Parent Directory']
    for filters in searchfor:
        new_table = new_table[new_table.str.contains(filters)]
    for filters in exclude:
        new_table = new_table[~new_table.str.contains(filters)]
    filenames = new_table.tolist()
    
    # Download
    for idx, file in enumerate(filenames):
        download_url = url + file
        print('Downloading: ' + file + ' (' + str(idx+1) + '/' + str(len(filenames)) + ')')
        urllib.request.urlretrieve(download_url, user_dir+file)
    
def open_ROCKE3D(path, filename, var):
    """
    This function opens and plots ROCKE-3D netCDF files
    
    Inputs:
    path - directory where model outputs are kept e.g. 'C:/Users/ylinh/OneDrive - UW/Exoplanetary Atmospheres/AIJ/'
    filename - filename is str form, could also be a list of strings
    var - variable name in .nc file. note: this means you have to open the .nc file and figure out the variable name (e.g. 'tsurf')
    Outputs: 
    var1 - variable data in an array
    latGrid - latitude in meshgrid
    longrid - longitudes in meshgrid
    
    """
    
    # Open data
    data = Dataset(path + filename,'r')
    
    # Import lat/lon coordinates and turn them into a meshgrid for plotting
    lat = np.array(data['lat'])
    lon = np.array(data['lon'])
    lonGrid, latGrid = np.meshgrid(lon, lat)
    
    # Opens variable and converts it to an array
    var1 = np.array(data[var])
    
    # Plotting
    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.grid(True)
    c1 = ax.contourf(lonGrid, latGrid, var1, levels=np.linspace(np.min(var1), np.max(var1),1000), cmap='Spectral_r')
    fig.colorbar(c1,label=(data[var].long_name +' ('+ data[var].units+')'), orientation="horizontal")
    ax.coastlines()
    ax.set_title(data[var].long_name)
    
    data.close()
    
#     return var1, latGrid, lonGrid

def open_zonal_ROCKE3D(path, filename, var):
    """
    This function opens and plots ROCKE-3D netCDF files
    
    Inputs:
    path - directory where model outputs are kept e.g. 'C:/Users/ylinh/OneDrive - UW/Exoplanetary Atmospheres/AIJ/'
    filename - filename is str form, could also be a list of strings
    var - variable name in .nc file. note: this means you have to open the .nc file and figure out the variable name (e.g. 'tsurf')
    Outputs: 
    var1 - variable data in an array
    latGrid - latitude in meshgrid
    longrid - longitudes in meshgrid
    
    """
    
    # Open data
    data = Dataset(path + filename,'r')
    
    # Import lat/lon coordinates and turn them into a meshgrid for plotting
    plm = np.array(data['plm'])
    lon = np.array(data['lon'])
    lonGrid, plmGrid = np.meshgrid(lon, plm)
    
    # Opens variable and converts it to an array
    var1 = np.array(data[var])
    var1 = np.average(var1,axis=1)
    
    return var1, lonGrid, plmGrid

def diff_ROCKE3D(path, file1, file2, var):
    """
    This function makes difference maps of ROCKE-3D model output with one constant variable
    
    Inputs:
    path - directory where model outputs are kept e.g. 'C:/Users/ylinh/OneDrive - UW/Exoplanetary Atmospheres/AIJ/'
    file1 - filename is str form, could also be a list of strings
    file2 - second filename for differencing
    var - variable name in .nc file. note: this means you have to open the .nc file and figure out the variable name (e.g. 'tsurf')
    
    Optional output: plots
    
    """
    data1 = Dataset(path + file1,'r')
    data2 = Dataset(path + file2,'r')

    lat = np.array(data1['lat'])
    lon = np.array(data1['lon'])
    lonGrid, latGrid = np.meshgrid(lon, lat)

    var1 = np.array(data1[var])
    var2 = np.array(data2[var])
    var_diff = var2 - var1

#     fig = plt.figure(figsize=(12,6))
#     ax = plt.axes(projection=ccrs.PlateCarree())
#     ax.grid(True)
#     c1 = ax.contourf(lonGrid, latGrid, var_diff, levels=np.linspace(np.min(var_diff), np.max(var_diff),1000), cmap='Spectral_r')
#     fig.colorbar(c1,label=(data2[var].long_name+' - '+data1[var].long_name+
#                            ' ('+ data1[var].units+')'), orientation="horizontal")
#     ax.coastlines()
#     ax.set_title(data1[var].long_name+' DIFFERENCE')
    
    return var_diff, latGrid, lonGrid

def diff_var_ROCKE3D(path, file1, var1, var2):
    """
    This function makes difference maps of ROCKE-3D model output with two different variables
    
    Inputs:
    path - directory where model outputs are kept e.g. 'C:/Users/ylinh/OneDrive - UW/Exoplanetary Atmospheres/AIJ/'
    file1 - filename is str form, could also be a list of strings
    var1 - variable name in .nc file. note: this means you have to open the .nc file and figure out the variable name (e.g. 'tsurf')
    var2 - second variable
    
    Optional output: plots
    
    """
    data = Dataset(path + file1,'r')

    lat = np.array(data['lat'])
    lon = np.array(data['lon'])
    lonGrid, latGrid = np.meshgrid(lon, lat)

    var_a = np.array(data[var1])
    var_b = np.array(data[var2])
    var_diff = var_b - var_a

    if data[var1].units != data[var2].units:
        print('Caution: var1 and var2 do not share units!')
    else: 
        pass
    if not np.any(var_diff) == True:
        print('Error: var2 - var1 equals zero! They are probably empty')
        return
    else:
        pass

#     fig = plt.figure(figsize=(12,6))
#     ax = plt.axes(projection=ccrs.PlateCarree())
#     ax.grid(True)
#     c1 = ax.contourf(lonGrid, latGrid, var_diff, levels=np.linspace(np.min(var_diff), np.max(var_diff),1000), cmap='Spectral_r')
#     fig.colorbar(c1,label=(data[var2].long_name+' - '+data[var1].long_name+
#                            ' ('+ data[var1].units+')'), orientation="horizontal")
#     ax.coastlines()
#     ax.set_title(data[var1].long_name+' VS '+data[var2].long_name)
    
    return var_diff, latGrid, lonGrid

def ratio_var_ROCKE3D(path, file1, var1, var2):
    """
    This function makes ratio maps of ROCKE-3D model output with two different variables
    
    Inputs:
    path - directory where model outputs are kept e.g. 'C:/Users/ylinh/OneDrive - UW/Exoplanetary Atmospheres/AIJ/'
    file1 - filename is str form, could also be a list of strings
    var1 - variable name in .nc file. note: this means you have to open the .nc file and figure out the variable name (e.g. 'tsurf')
    var2 - second variable, 
    
    Optional output: plots
    
    """
    data = Dataset(path + file1,'r')

    lat = np.array(data['lat'])
    lon = np.array(data['lon'])
    lonGrid, latGrid = np.meshgrid(lon, lat)

    var_a = np.array(data[var1])
    var_b = np.array(data[var2])
    var_diff = var_b / var_a

    if data[var1].units != data[var2].units:
        print('Caution: var1 and var2 do not share units!')
    else: 
        pass
    if not np.any(var_diff) == True:
        print('Error: var2 - var1 equals zero! They are probably empty')
        return 
    else:
        pass

#     fig = plt.figure(figsize=(12,6))
#     ax = plt.axes(projection=ccrs.PlateCarree())
#     ax.grid(True)
#     c1 = ax.contourf(lonGrid, latGrid, var_diff, levels=np.linspace(np.min(var_diff), np.max(var_diff),1000), cmap='Spectral_r')
#     fig.colorbar(c1,label=(data[var2].long_name+'/'+data[var1].long_name+
#                            ' ('+ data[var1].units+')'), orientation="horizontal")
#     ax.coastlines()
#     ax.set_title(data[var1].long_name+'-'+data[var2].long_name+' Ratio')
    
    return var_diff, latGrid, lonGrid