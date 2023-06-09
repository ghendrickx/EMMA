import pandas as pd

cell1 = pd.read_excel (r'C:\Users\Soesja\Documents\Hydraulic Engineering jaar 1\Master thesis\data\dataopzet.xlsx')
print(cell1)

def label_salinity(x):
    if x < 5.4:
        return 'fresh'
    elif (x >= 5.4) & (x <= 18):
        return 'brakish'
    elif x > 18:
        return 'marine'

def label_depth1(x):
    if x == 0:
        return 'supra-littoral'
    elif x == 1:
        return 'sub-littoral'
    else:
        return 'littoral'

def label_hydrodynamics(x, depth1):
    if x[0] == 0 and x[1] == 0:
        return 'stagnant'
    elif depth1 == 'sub-littoral':
        if x[0] >= 0.8:
            return 'high energy'
    elif x[0] <= 0.8:
        return 'low energy'


cell1['Salinity'] = cell1['salinity'].apply(label_salinity)
cell1['Depth1'] = cell1['depth1'].apply(label_depth1)
#cell1['Hydrodynamics'] = cell1['hydrodynamics'].apply(lambda x: label_hydrodynamics(x, depth1= cell1['depth1']))

print(cell1)

def Ecotope(x):
    if x['Salinity'] == 'brakish':
        return 'B2_122f'

#cell1['Ecotope'] = cell1['Salinity'].apply(Ecotope)

df2 = cell1.loc[(cell1['Salinity'] == 'brakish') & (cell1['Depth1'] == 'sub-littoral')]
print(df2)