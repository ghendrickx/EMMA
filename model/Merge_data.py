import xarray as xr
import numpy as np
import pandas as pd
from ecotope_label_functions import label_salinity
import matplotlib.pyplot as plt
from xarray import DataArray

## Open dataset 0
data0 = xr.open_dataset('FlowFM_0000_map.nc', engine='netcdf4')
##  Put salinity in dataframe
df0_salinity = data0['sa1'].to_dataframe()
#print(df0_salinity.head(10))
#df0_salinity['sa1'] = df0_salinity.astype({df0_salinity['sa1'] :'float'})

df0_salinity_max = df0_salinity.groupby(['nFlowElem'])['sa1'].max()
df0_salinity_min = df0_salinity.groupby(['nFlowElem'])['sa1'].min()
df0_salinity_mean = df0_salinity.groupby(['nFlowElem'])['sa1'].mean()
#print(dfm0_salinity_mean)

df0_salinity_mmm = pd.concat([df0_salinity_min, df0_salinity_max, df0_salinity_mean], axis=1)
df0_salinity_mmm.columns =['sa1_min', 'sa1_max', 'sa1_mean']
print(df0_salinity_mmm)

#print(len(dfm0_salinity1))

## apply label in list
# list = []
# list.append(dfm0_salinity1.apply(label_salinity, axis=1))
#print(list)

## apply label in dataframe
df0_salinity_mmm['sa1_label'] = df0_salinity_mmm.apply(label_salinity, axis=1)
#dfm0_salinity1_sample.apply(lambda row: label_salinity(row['sa1']), axis = 1)
print(df0_salinity_mmm)


# make sample size
# dfm0_salinity1_sample = dfm0_salinity1.sample(frac=0.1, replace=True, random_state=1)

## Put depth in dataframe
#df0_depth = data0['s1'].to_dataframe()
#df0_depth.apply(label_depth1, axis=1)
#print(df0_depth.head(5))

## Plot salinity
# plt.figure()
# plt.scatter(dfm0['FlowElem_xcc'], dfm0['FlowElem_ycc'], c=dfm0['sa1'], s = 0.1)
# plt.show()

## Open dataset 1
# data1 = xr.open_dataset('FlowFM_0001_map.nc', engine='netcdf4')
## Put salinity in dataframe
# df1_salinity = data1['sa1'].to_dataframe()

## Open dataset 2
# data2 = xr.open_dataset('FlowFM_0002_map.nc', engine='netcdf4')
## Put salinity in dataframe
# df2_salinity = data2['sa1'].to_dataframe()

## Merge dataframe salinity from 1, 2 and 3
# dftotal = pd.concat([df0_salinity, df1_salinity, df2_salinity], ignore_index=True)

#print(dftotal)