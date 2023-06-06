import xarray as xr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from Compare_maps_2 import polygon_xy

# Un-# this for opening the data

# # partitions_0 = 10
# # partitions_1_start = 10
# # partitions_1_stop = 16
# #data0 = [xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_000{i}_map.nc', engine='netcdf4') for i in range(partitions_0)]
# #data1 = [xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_00{i}_map.nc', engine='netcdf4') for i in range(partitions_1_start, partitions_1_stop)]
#
# # Open dataset, should be more efficient
#
# #data0 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0000_map.nc', engine='netcdf4')
# data1 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0001_map.nc', engine='netcdf4')
# data2 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0002_map.nc', engine='netcdf4')
# data3 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0003_map.nc', engine='netcdf4')
# data4 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0004_map.nc', engine='netcdf4')
# data5 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0005_map.nc', engine='netcdf4')
# data6 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0006_map.nc', engine='netcdf4')
# data7 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0007_map.nc', engine='netcdf4')
# data8 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0008_map.nc', engine='netcdf4')
# data9 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0009_map.nc', engine='netcdf4')
# data10 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0010_map.nc', engine='netcdf4')
# data11 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0011_map.nc', engine='netcdf4')
# data12 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0012_map.nc', engine='netcdf4')
# data13 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0013_map.nc', engine='netcdf4')
# data14 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0014_map.nc', engine='netcdf4')
# data15 = xr.open_dataset(f'C:\\Users\\Soesja\\Documents\\EcotopePrediction\\Output_Gijs\\map_output\\WS13_new_04_0015_map.nc', engine='netcdf4')
#
# # Put depth in dataset
# #df0_depth = data0['waterdepth'].to_dataframe()
# df1_depth = data1['waterdepth'].to_dataframe()
# df2_depth = data2['waterdepth'].to_dataframe()
# df3_depth = data3['waterdepth'].to_dataframe()
# df4_depth = data4['waterdepth'].to_dataframe()
# df5_depth = data5['waterdepth'].to_dataframe()
# df6_depth = data6['waterdepth'].to_dataframe()
# df7_depth = data7['waterdepth'].to_dataframe()
# df8_depth = data8['waterdepth'].to_dataframe()
# df9_depth = data9['waterdepth'].to_dataframe()
# df10_depth = data10['waterdepth'].to_dataframe()
# df11_depth = data11['waterdepth'].to_dataframe()
# df12_depth = data12['waterdepth'].to_dataframe()
# df13_depth = data13['waterdepth'].to_dataframe()
# df14_depth = data14['waterdepth'].to_dataframe()
# df15_depth = data15['waterdepth'].to_dataframe()
# df_depth = pd.concat(
#     [df1_depth, df2_depth, df3_depth, df4_depth, df5_depth, df6_depth, df7_depth, df8_depth, df9_depth,
#      df10_depth, df11_depth, df12_depth, df13_depth, df14_depth, df15_depth])
#
# df1_salinity = data1['sa1'].to_dataframe()
# df2_salinity = data2['sa1'].to_dataframe()
# df3_salinity = data3['sa1'].to_dataframe()
# df4_salinity = data4['sa1'].to_dataframe()
# df5_salinity = data5['sa1'].to_dataframe()
# df6_salinity = data6['sa1'].to_dataframe()
# df7_salinity = data7['sa1'].to_dataframe()
# df8_salinity = data8['sa1'].to_dataframe()
# df9_salinity = data9['sa1'].to_dataframe()
# df10_salinity = data10['sa1'].to_dataframe()
# df11_salinity = data11['sa1'].to_dataframe()
# df12_salinity = data12['sa1'].to_dataframe()
# df13_salinity = data13['sa1'].to_dataframe()
# df14_salinity = data14['sa1'].to_dataframe()
# df15_salinity = data15['sa1'].to_dataframe()
#
# df_salinity = pd.concat(
#    [df1_salinity, df2_salinity, df3_salinity, df4_salinity, df5_salinity, df6_salinity, df7_salinity,
#     df8_salinity, df9_salinity, df10_salinity, df11_salinity, df12_salinity, df13_salinity, df14_salinity,
#     df15_salinity])
#
# # df0_hydrodynamics_y = data0['ucy'].to_dataframe()
# # df0_hydrodynamics_x = data0['ucx'].to_dataframe()
# df1_hydrodynamics_y = data1['ucy'].to_dataframe()
# df1_hydrodynamics_x = data1['ucx'].to_dataframe()
# df2_hydrodynamics_y = data2['ucy'].to_dataframe()
# df2_hydrodynamics_x = data2['ucx'].to_dataframe()
# df3_hydrodynamics_y = data3['ucy'].to_dataframe()
# df3_hydrodynamics_x = data3['ucx'].to_dataframe()
# df4_hydrodynamics_y = data4['ucy'].to_dataframe()
# df4_hydrodynamics_x = data4['ucx'].to_dataframe()
# df5_hydrodynamics_y = data5['ucy'].to_dataframe()
# df5_hydrodynamics_x = data5['ucx'].to_dataframe()
# df6_hydrodynamics_y = data6['ucy'].to_dataframe()
# df6_hydrodynamics_x = data6['ucx'].to_dataframe()
# df7_hydrodynamics_y = data7['ucy'].to_dataframe()
# df7_hydrodynamics_x = data7['ucx'].to_dataframe()
# df8_hydrodynamics_y = data8['ucy'].to_dataframe()
# df8_hydrodynamics_x = data8['ucx'].to_dataframe()
# df9_hydrodynamics_y = data9['ucy'].to_dataframe()
# df9_hydrodynamics_x = data9['ucx'].to_dataframe()
# df10_hydrodynamics_y = data10['ucy'].to_dataframe()
# df10_hydrodynamics_x = data10['ucx'].to_dataframe()
# df11_hydrodynamics_y = data11['ucy'].to_dataframe()
# df11_hydrodynamics_x = data11['ucx'].to_dataframe()
# df12_hydrodynamics_y = data12['ucy'].to_dataframe()
# df12_hydrodynamics_x = data12['ucx'].to_dataframe()
# df13_hydrodynamics_y = data13['ucy'].to_dataframe()
# df13_hydrodynamics_x = data13['ucx'].to_dataframe()
# df14_hydrodynamics_y = data14['ucy'].to_dataframe()
# df14_hydrodynamics_x = data14['ucx'].to_dataframe()
# df15_hydrodynamics_y = data15['ucy'].to_dataframe()
# df15_hydrodynamics_x = data15['ucx'].to_dataframe()
#
#
# df_hydrodynamics_x = pd.concat(
#     [df1_hydrodynamics_x, df2_hydrodynamics_x, df3_hydrodynamics_x, df4_hydrodynamics_x,
#      df5_hydrodynamics_x, df6_hydrodynamics_x, df7_hydrodynamics_x, df8_hydrodynamics_x, df9_hydrodynamics_x,
#      df10_hydrodynamics_x, df11_hydrodynamics_x, df12_hydrodynamics_x, df13_hydrodynamics_x, df14_hydrodynamics_x,
#      df15_hydrodynamics_x])
#
# df_hydrodynamics_y = pd.concat(
#     [df1_hydrodynamics_y, df2_hydrodynamics_y, df3_hydrodynamics_y, df4_hydrodynamics_y,
#      df5_hydrodynamics_y, df6_hydrodynamics_y, df7_hydrodynamics_y, df8_hydrodynamics_y, df9_hydrodynamics_y,
#      df10_hydrodynamics_y, df11_hydrodynamics_y, df12_hydrodynamics_y, df13_hydrodynamics_y, df14_hydrodynamics_y,
#      df15_hydrodynamics_y])
#
# Save as pickles
# df_depth.to_pickle("df_depth.pkl")
# df_salinity.to_pickle("df_salinity.pkl")
# df_hydrodynamics_x.to_pickle("df_hydrodynamics_x.pkl")
# df_hydrodynamics_y.to_pickle("df_hydrodynamics_y.pkl")

# # Open pickles
df_depth = pd.read_pickle("df_depth.pkl")
df_salinity = pd.read_pickle("df_salinity.pkl")
df_hydrodynamics_x = pd.read_pickle("df_hydrodynamics_x.pkl")
df_hydrodynamics_y = pd.read_pickle("df_hydrodynamics_y.pkl")

def label_salinity(cell):
    """
    Determines label of salinity
    :param: cell: salinity [ppm]
    :type: dict

    :return: salinity label
    :rtype: dict
    """
    if cell['sa1_mean'] is None:
        return None
    elif cell['sa1_max'] - cell['sa1_min'] > cell['sa1_mean']:
        return 'variable'
    elif cell['sa1_mean'] >= 5.4 and cell['sa1_mean'] <= 18:
        return 'brackish'
    elif cell['sa1_mean'] > 18:
        return 'marine'
    elif cell['sa1_mean'] < 5.4:
        return 'fresh'

def label_salinity_code(cell):
    """
    Determines label of salinity
    :param: cell: salinity [ppm]
    :type: dict

    :return: salinity label
    :rtype: dict
    """
    if cell['sa1_mean'] is None:
        return None
    elif cell['sa1_max'] - cell['sa1_min'] > cell['sa1_mean']:
        return 'V'
    elif cell['sa1_mean'] >= 5.4 and cell['sa1_mean'] <= 18:
        return 'B'
    elif cell['sa1_mean'] > 18:
        return 'Z'
    elif cell['sa1_mean'] < 5.4:
        return 'F'

def label_depth1(cell):
    """"
    Determines label of depth1, based on the frequency of flooding
    0: supra-littoral
    0.1 - 0.99 : littoral
    1: sub-littoral
    :param cell: depth1 ['m']
    :type cell: dict

    :return: dict with depth1 label
    :rtype: dict
    """
    if cell['rol_average_min'] is None:
        return None
    elif cell['rol_average_max'] is None:
        return None
    elif cell['rol_average_min'] == 1 and cell['rol_average_max'] == 1:
        return 'sub-littoral'
    elif cell['rol_average_min'] == 0 and cell['rol_average_max'] == 0:
        return 'supra-littoral'
    else:
        return 'littoral'

def label_depth1_code(cell):
    """"
    Determines label of depth1, based on the frequency of flooding
    0: supra-littoral
    0.1 - 0.99 : littoral
    1: sub-littoral
    :param cell: depth1 ['m']
    :type cell: dict

    :return: dict with depth1 label
    :rtype: dict
    """
    if cell['rol_average_min'] is None:
        return None
    elif cell['rol_average_max'] is None:
        return None
    elif cell['rol_average_min'] == 1 and cell['rol_average_max'] == 1:
        return '1'
    elif cell['rol_average_min'] == 0 and cell['rol_average_max'] == 0:
        return '3'
    else:
        return '2'

def label_hydrodynamics(velocity, depth):
    """
    Determines label of hydrodynamics
    :param cell: hydrodynamics [m/s] [linear current velocity, orbital velocity]
    :type: dict

    :return: hydrodynamics label
    :rtype: dict
    """
    if velocity is None:
        return None
    elif velocity == 0:
        return 'stagnant'
    elif depth == 'sub-littoral': #or cell1['depth1'] == 'littoral':
        if velocity >= 0.8:
            return 'high energy'
        elif velocity <= 0.8:
            return 'low energy'

    elif depth == 'supra-littoral' or depth == 'littoral':
        if velocity >= 0.2:
            return 'high energy'
        elif velocity <= 0.2:
            return 'low energy'

def label_hydrodynamics_code(velocity, depth):
    """
    Determines label of hydrodynamics
    :param cell: hydrodynamics [m/s] [linear current velocity, orbital velocity]
    :type: dict

    :return: hydrodynamics label
    :rtype: dict
    """
    if velocity is None:
        return None
    if velocity == 0:
        return '3'
    elif depth == 'sub-littoral': #or cell1['depth1'] == 'littoral':
        if velocity >= 0.8:
            return '1'
        elif velocity <= 0.8:
            return '2'

    elif depth == 'supra-littoral' or depth == 'littoral':
        if velocity >= 0.2:
            return '1'
        elif velocity <= 0.2:
            return '2'

def label_depth2(depth1_label, depth, duration, frequency):
    """"
    Determines label of depth2
    TODO: Should depend on location in the Netherlands
    TODO: Duration of flooding should depend on MLWS and MHWN
    [depth [m], duration of flooding [%], frequency of flooding (300-5)[ x /year]]
    :param: cell: depth2
    :type: dict
    TODO: frequency per year is now defined as per 10 days.
    :return: depth2 label
    :rtype: dict
    """
    if depth1_label is None:
        return None
    elif depth1_label == 'sub-littoral':
        if depth >= 10:
            return 'very deep'
        elif depth >= 5 and depth < 10:
            return 'deep'
        elif depth < 5:
            return 'shallow'

    elif depth1_label == 'littoral':
        if duration <= 100 and duration > 75:
            return 'low littoral'
        elif duration <= 75 and duration > 25:
            return 'middle high littoral'
        elif duration < 25:
            return 'high littoral'

    elif depth1_label == 'supra-littoral':
        if frequency > 8.2:
            return 'potential pioneer zone'
        elif frequency <= 8.2 and frequency > 4.1:
            return 'low salt marsh'
        elif frequency <= 4.1 and frequency > 1.37:
            return 'middle salt marsh'
        elif frequency <= 1.37: # and frequency > 0.14:
            return 'high salt marsh'

def label_depth2_code(depth1_label, depth, duration, frequency):
    """"
    Determines label of depth2
    TODO: Should depend on location in the Netherlands
    TODO: Duration of flooding should depend on MLWS and MHWN
    [depth [m], duration of flooding [%], frequency of flooding (300-5)[ x /year]]
    :param: cell: depth2
    :type: dict
    TODO: frequency per year is now defined as per 10 days.
    :return: depth2 label
    :rtype: dict
    """
    if depth1_label is None:
        return None
    elif depth1_label == 'sub-littoral':
        if depth >= 10:
            return '1'
        elif depth >= 5 and depth < 10:
            return '2'
        elif depth < 5:
            return '3'

    elif depth1_label == 'littoral':
        if duration <= 100 and duration > 75:
            return '1'
        elif duration <= 75 and duration > 25:
            return '2'
        elif duration < 25:
            return '3'

    elif depth1_label == 'supra-littoral':
        if frequency > 8.2:
            return '1'
        elif frequency <= 8.2 and frequency > 4.1:
            return '2'
        elif frequency <= 4.1 and frequency > 1.37:
            return '3'
        elif frequency <= 1.37: # and frequency > 0.14:
            return '4'

def label_substratum2(grainsize):
    """
    Determines label of substratum2
    :param: cell: substratum2 [median grain size [micro-m], silt percentage [%]]
    :type: dict

    :return: substratum2 label
    :rtype: dict
    TODO: add silt percentage
    """
    if grainsize is None:
        return None
    elif grainsize >= 25:
        return 'rich in silt'
    elif grainsize <= 250:
        return 'fine sands'
    elif grainsize <= 2000:
        return 'coarse sands'
    elif grainsize > 2000:
        return 'gravel'

def label_substratum2_code(grainsize):
    """
    Determines label of substratum2
    :param: cell: substratum2 [median grain size [micro-m], silt percentage [%]]
    :type: dict

    :return: substratum2 label
    :rtype: dict
    TODO: add silt percentage
    """
    if grainsize is None:
        return None
    elif grainsize <= 25:
        return 's'
    elif grainsize <= 250:
        return 'f'
    elif grainsize <= 2000: # and grainsize > 250:
        return 'z'
    elif grainsize > 2000:
        return 'g'

## Salinity
def process_salinity(df_salinity):
    '''
    :param df_salinity: dataframe with sa1 in per layer, in time, per gridpoint
    :return: dataframe with sa1_min, sa1_max, sa1_mean, sa1 label
    '''
    # Take average over the depth-layers
    df_salinity = pd.DataFrame(df_salinity.groupby(['FlowElem_xcc', 'FlowElem_ycc', 'time'])['sa1'].mean())
    # Take max, min and mean in time per grid-point
    df_salinity_max = df_salinity.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['sa1'].max()
    df_salinity_min = df_salinity.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['sa1'].min()
    df_salinity_mean = df_salinity.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['sa1'].mean()

    # Combine in one dataframe
    df_salinity_mmm = pd.concat([df_salinity_min, df_salinity_max, df_salinity_mean], axis=1)
    df_salinity_mmm.columns =['sa1_min', 'sa1_max', 'sa1_mean']

    ## Apply salinity label function in dataframe
    df_salinity_mmm['sa1_label'] = df_salinity_mmm.apply(label_salinity, axis=1)
    df_salinity_mmm['sa1_code'] = df_salinity_mmm.apply(label_salinity_code, axis=1)
    df_labels = pd.DataFrame().assign(sa1_label=df_salinity_mmm['sa1_label'], sa1_code=df_salinity_mmm['sa1_code'])

    return df_labels

## Depth1
def process_depth1(df_labels, df_depth):
    '''
    :param df_depth: dataframe with waterdepth in time, per gridpoint
    :return: dataframe with depth label per gridpoint
    '''
    # Add column with 1 for flood, 0 for dry, per gridpoint, in time
    df_depth['bool'] = (df_depth['waterdepth'] > 0)*1
    # Take rolling average to determine change in flood or dry
    df_depth['rol_average'] = df_depth['bool'].rolling(2).mean()
    # Determine min and max values of rolling average
    df_depth_flood = pd.DataFrame(df_depth.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['rol_average'].agg('min'))
    df_depth_flood = df_depth_flood.rename(columns={"rol_average": 'rol_average_min'})
    df_depth_flood['rol_average_max'] = df_depth.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['rol_average'].agg('max')
    # Apply label function
    df_depth_flood['depth1_label'] = df_depth_flood.apply(label_depth1, axis=1)
    df_depth_flood['depth1_code'] = df_depth_flood.apply(label_depth1_code,axis=1)

    df_labels['depth1_label'] = df_depth_flood['depth1_label']
    df_labels['depth1_code'] = df_depth_flood['depth1_code']

    return df_labels

## Hydrodynamics
def process_hydrodynamics(df_labels, df_hydrodynamics_x, df_hydrodynamics_y):

    # Combine x and y column
    df_hydrodynamics = pd.concat([df_hydrodynamics_x, df_hydrodynamics_y['ucy']], axis=1)
    # Calculate flow velocity in flow direction
    df_hydrodynamics['uca'] = np.sqrt(df_hydrodynamics['ucy']**2 + df_hydrodynamics['ucx']**2)
    df_hydrodynamics = df_hydrodynamics.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['uca'].max().to_frame()
    # Apply hydrodynamics label
    df_labels = pd.concat([df_hydrodynamics, df_labels], axis=1)
    df_labels['hydrodynamic_label'] = df_labels.apply(lambda x: label_hydrodynamics(x['uca'], x['depth1_label']), axis=1)
    df_labels['hydrodynamic_code'] = df_labels.apply(lambda x: label_hydrodynamics_code(x['uca'], x['depth1_label']), axis=1)
    return df_labels

## Depth2
def process_depth2(df_labels, df_depth):
    ## Compute frequency of flooding
    # New dataframe with only coordinates and minimum of rolling average
    df_depth2 = pd.DataFrame(df_depth)
    df_depth2_freq = df_depth2
    df_depth2_freq = df_depth2_freq.drop(columns= ['bool', 'waterdepth'])
    df_depth2_freq = df_depth2_freq.set_index(['FlowElem_xcc', 'FlowElem_ycc'], append=True)

    # Count how many times the rolling average is 0.5
    df_depth2_freq['rol_average_half'] = (df_depth2_freq['rol_average'] == 0.5)*1
    df_depth2_freq = df_depth2_freq.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['rol_average_half'].sum()
    df_depth2_freq = df_depth2_freq.to_frame()
    df_depth2_freq.columns = (['frequency'])
    df_depth2_freq = (df_depth2_freq['frequency']*0.5).astype(int)
    df_depth2_freq = df_depth2_freq.to_frame()
    # PROBEREN MET MEAN

    ## Compute duration of flooding
    df_depth2_1 = df_depth2.drop(columns= ['rol_average', 'waterdepth'])
    df_depth2_1['count'] = 1
    df_depth2_dur_len = df_depth2_1.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['count'].sum()
    df_depth2_dur_count = df_depth2_1.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['bool'].sum()
    df_depth2_duration = pd.concat([df_depth2_dur_count, df_depth2_dur_len], axis=1)
    df_depth2_duration['duration'] = df_depth2_duration['bool'] / df_depth2_duration['count']
    df_depth2_duration.drop(['bool', 'count'], axis=1, inplace=True)

    # Combine dataframes
    df_depth2_label = df_depth2_freq.join(df_depth2_duration)
    df_labels = df_labels.join(df_depth2_label)
    df_waterdepth = df_depth.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['waterdepth'].mean()
    df_labels = df_labels.join(df_waterdepth)

    # Apply depth2 label
    df_labels['depth2_label'] = df_labels.apply(lambda x: label_depth2(x['depth1_label'], x['waterdepth'], x['duration'], x['frequency']), axis=1)
    df_labels['depth2_code'] = df_labels.apply(lambda x: label_depth2_code(x['depth1_label'], x['waterdepth'], x['duration'], x['frequency']), axis=1)
    return df_labels

## Substratum2
def process_substratum2(df_labels, df_hydrodynamics_x, df_hydrodynamics_y):
    # Set parameters
    psi = 0.03
    C = 50 # [m^1/2/s]

    delta = 1.58


    # Combine x and y column
    df_hydrodynamics = pd.concat([df_hydrodynamics_x, df_hydrodynamics_y['ucy']], axis=1)
    # Calculate flow velocity in flow direction
    df_hydrodynamics['uca'] = np.sqrt(df_hydrodynamics['ucy']**2 + df_hydrodynamics['ucx']**2)
    df_hydrodynamics = df_hydrodynamics.groupby(['FlowElem_xcc', 'FlowElem_ycc'])['uca'].median().to_frame()
    # Determine grainsize with Shields without loop
    df_labels['grainsize'] = (abs(df_hydrodynamics['uca'])**2/(psi*delta*C**2))*1000000

    # Apply label function
    df_labels['substratum2_label'] = df_labels.apply(lambda x: label_substratum2(x['grainsize']), axis=1)
    df_labels['substratum2_code'] = df_labels.apply(lambda x: label_substratum2_code(x['grainsize']), axis=1)
    df_labels = df_labels.drop(columns= ['duration', 'grainsize', 'frequency'])
    return df_labels

# # Run all functions

df_labels = process_salinity(df_salinity)
df_labels = process_depth1(df_labels, df_depth)
df_labels = process_hydrodynamics(df_labels, df_hydrodynamics_x, df_hydrodynamics_y)
df_labels = process_depth2(df_labels, df_depth)
df_labels = process_substratum2(df_labels, df_hydrodynamics_x, df_hydrodynamics_y)
df_labels['CODE'] = df_labels['sa1_code'] + '2.' + df_labels['depth1_code'] + df_labels['hydrodynamic_code'] + df_labels['depth2_code'] + df_labels['substratum2_code']

df_labels = df_labels.reset_index()
df_labels = df_labels.loc[df_labels['FlowElem_xcc'] > 30000]
df_labels = df_labels.loc[df_labels['FlowElem_xcc'] < 80000]
df_labels = df_labels.loc[df_labels['FlowElem_ycc'] > 372000]
df_labels = df_labels.loc[df_labels['FlowElem_ycc'] < 888000]

df_labels.to_pickle("df_labels.pkl")

# Open pickles
df_labels = pd.read_pickle("df_labels.pkl")

#Set index equal to x and y
df_labels.set_index(['FlowElem_xcc', 'FlowElem_ycc'], inplace=True)
polygon_xy.set_index(['FlowElem_xcc', 'FlowElem_ycc'], inplace=True)

#drop labels of model
df_labels = df_labels.drop(['uca', 'sa1_label', 'depth1_label', 'hydrodynamic_label', 'depth2_label', 'substratum2_label',  'waterdepth'], axis=1)
polygon_xy['ZES_CODE'] = np.where(polygon_xy['ZES_CODE'] == 'overig', np.NaN, polygon_xy['ZES_CODE'])
# split RWS code into separate columns
polygon_xy['RWS_Sa'] = polygon_xy['ZES_CODE'].str[0]
polygon_xy['RWS_d1'] = polygon_xy['ZES_CODE'].str[3]
polygon_xy['RWS_h'] = polygon_xy['ZES_CODE'].str[4]
polygon_xy['RWS_d2'] = polygon_xy['ZES_CODE'].str[5]
polygon_xy['RWS_sub'] = polygon_xy['ZES_CODE'].str[6]

# Move g,f from d2 to sub
polygon_xy['RWS_sub'] = np.where(polygon_xy['RWS_d2'] == 'f', 'f', polygon_xy['RWS_sub'])
polygon_xy['RWS_sub'] = np.where(polygon_xy['RWS_d2'] == 'g', 'g', polygon_xy['RWS_sub'])
polygon_xy['RWS_sub'] = np.where(polygon_xy['RWS_d2'] == 'x', np.NaN, polygon_xy['RWS_sub'])

polygon_xy['RWS_sub'] = np.where(polygon_xy['RWS_sub'].isna(), 'x', polygon_xy['RWS_sub'])
# Remove f, g from d2
polygon_xy['RWS_d2'] = np.where(polygon_xy['RWS_d2'] == 'f',  np.NaN, polygon_xy['RWS_d2'])
polygon_xy['RWS_d2'] = np.where(polygon_xy['RWS_d2'] == 'g',  np.NaN, polygon_xy['RWS_d2'])

# combine columns with codes
compare = pd.concat([df_labels, polygon_xy], axis=1)
#compare.rename(columns= {'CODE': 'model_code', 'code' : 'RWS_code'}, inplace=True)

def compare_sa_with_x(df):
    if df['RWS_Sa'] == df['sa1_code'] or df['RWS_Sa'] == 'x' or df['RWS_Sa'] is None:
        return True
    else:
        return False

def compare_d1_with_x(df):
    if df['RWS_d1'] == df['depth1_code'] or df['RWS_d1'] == 'x' or df['RWS_d1'] is None:
        return True
    else:
        return False
def compare_hydrodynamics_with_x(df):
    if df['RWS_h'] == df['hydrodynamic_code'] or df['RWS_h'] == 'x' or df['RWS_h'] is None:
        return True
    else:
        return False
def compare_d2_with_x(df):
    if df['RWS_d2'] == df['depth2_code']: #or df['RWS_d2'] == 'x' or df['RWS_d2'] is None:
        return True
    else:
        return False

def compare_substratum2_with_x(df):
    if df['RWS_sub'] == df['substratum2_code']:
        return True
    #elif df['RWS_sub'] == 'x':
    #     return True
    # elif df['RWS_sub'] is None:
    #     return True
    else:
         return False

compare['compare_sa'] = compare.apply(compare_sa_with_x, axis=1)
compare['compare_d1'] = compare.apply(compare_d1_with_x, axis=1)
compare['compare_h'] = compare.apply(compare_hydrodynamics_with_x, axis=1)
compare['compare_d2'] = compare.apply(compare_d2_with_x, axis=1)
compare['compare_sub'] = compare.apply(compare_substratum2_with_x, axis=1)

# #Plot the true or false values of all variables, and plot RWS or model
palette = {'0': 'C0', '1': 'C1', '2': 'C2', '3': 'C3', '4': 'C4', 'Z': 'C5', 'V': 'C6', 'B': 'C7', 'g': 'C8', 'z': 'C9', 'f': 'C10', 's': 'C11', 'x': 'C99', 'h': 'C13'}
palette_TF = {True: 'mediumseagreen', False: 'lightcoral'} # hue_order=['True', 'False'],
## hue_order=['1', '2', '3', '4', '0', 'x'] # d2
# # # polygon_xy RWS_Sa RWS_d1 RWS_h RWS_d2 RWS_sub
# # # df_labels sa1_code, depth1_code hydrodynamic_code depth2_code substratum2_code CODE
# # # compare compare_sa, compare_d1, compare_h, compare_d2, compare_sub
sns.scatterplot(x='FlowElem_xcc', y='FlowElem_ycc', data=df_labels, hue='substratum2_code', hue_order=['s', 'f ', 'g', 'z' 'h', 'x'], palette=palette, s=4)
plt.legend(loc=2, prop={'size': 15})
plt.title('Substratum 2 model')
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.show()

# # Print and compare performance true or false plots
# print('sa1', compare['compare_sa'].value_counts())
# print('d1', compare['compare_d1'].value_counts())
# print('h', compare['compare_h'].value_counts())
#print('d2', compare['compare_d2'].value_counts())
print('sub', compare['compare_sub'].value_counts())

# plt.subplot(231)
# plt.title('Salinity performance')
# plt.ylim(0,50000)
# plt.bar(['True', 'False'], compare['compare_sa'].value_counts(), width=0.5, color=['mediumseagreen', 'lightcoral'])
# plt.subplot(232)
# plt.title('Depth 1 performance')
# plt.bar(['True', 'False'], compare['compare_d1'].value_counts(), width=0.5, color=['mediumseagreen', 'lightcoral'])
# plt.subplot(233)
# plt.title('Hydrodynamics performance')
# plt.bar(['True', 'False'], compare['compare_h'].value_counts(), width=0.5, color=['mediumseagreen', 'lightcoral'])
# plt.subplot(234)
# plt.title('Depth 2 performance')
# plt.bar(['True', 'False'], compare['compare_d2'].value_counts(), width=0.5, color=['mediumseagreen', 'lightcoral'])
# plt.subplot(235)
# plt.title('Substratum performance')
# plt.bar(['True', 'False'], compare['compare_sub'].value_counts(), width=0.5, color=['mediumseagreen', 'lightcoral'])
# plt.show()


# ## Plot overview map
#
# # make list of all unique ecotopes
# df_colors = df_labels['CODE'].unique()
# # Give different colors to found ecotopes
# rgb_values = sns.color_palette("hls", len(df_colors))
# color_map = dict(zip(df_colors, rgb_values))
# plt.figure()
# sns.scatterplot(x='FlowElem_xcc', y='FlowElem_ycc', data=df_labels, hue='CODE', s=4, legend=None)
# #plt.legend(loc=2, prop={'size': 5})
# plt.title('Ecotopes in Western Scheldt by RWS')
# plt.xlabel('x [m]')
# plt.ylabel('y [m]')
# plt.show()