import numpy as np

# Input data
# B2_11s error for np.nan
#cell1 = dict([('salinity', 6), ('depth1', 1), ('hydrodynamics', [1, 0.9]), ('depth2', [np.nan, np.nan, np.nan ]), ('substratum2', [200, 30])])
#B2_122f
cell1 = dict([('salinity', 6), ('depth1', 1), ('hydrodynamics', [0.3, 0.9]), ('depth2', [7, 5, 300]), ('substratum2', [200, 10])])
cell11 = [('salinity', 6), ('depth1', 1), ('hydrodynamics', [0.3, 0.9]), ('depth2', [7, 5, 300]), ('substratum2', [200, 10])]
#B2_122s
cell2 = dict([('salinity', 6), ('depth1', 1), ('hydrodynamics', [0.3, 0.9]), ('depth2', [7, 5, 300]), ('substratum2', [200, 30])])

print(cell1)
# hydrodynamics [linear current velocity, orbital velocity]
# depth2 : [depth [m], duration of flooding [%], frequency of flooding (300-5)[ x /year]]
# substratum2: [median grain size [micro-m], silt percentage [%]]
Salinity = []
# Salinity: should later check for salinity fluctuation as well: (4*std/mean)*100%
def label_salinity(cell):
    if 5.4 <= cell['salinity'] <= 18:
        Salinity.append('brakish')
    elif cell['salinity'] >= 18:
        Salinity.append( 'marine')
    elif cell['salinity'] <= 5.4:
        Salinity.append('fresh')


celllist = [cell1, cell2]

for i in celllist:
    (label_salinity(cell1))
print(Salinity)


# Zone : frequency flooding:
# 0: supra-littoral
# 0.1 - 0.99 : littoral
# 1: sub-littoral

if cell1['depth1'] == 0:
    cell1['depth1'] = 'supra-littoral'
elif cell1['depth1'] == 1:
    cell1['depth1'] = 'sub-littoral'
else:
    cell1['depth1'] = 'littoral'

# Hydrodynamics:
# High > 0.8 m/s if in the sub or littoral zone.
# Low < 0.2 for littoral or sub-littoral
# Stagnant = 0 m/s
# check with ZES

if cell1['hydrodynamics'][0] == 0 and cell1['hydrodynamics'][1] == 0:
        cell1['hydrodynamics'] = 'stagnant'
elif cell1['depth1'] == 'sub-littoral': #or cell1['depth1'] == 'littoral':
    if cell1['hydrodynamics'][0] >= 0.8:
        cell1['hydrodynamics'] = 'high energy'
    elif cell1['hydrodynamics'][0] <= 0.8:
        cell1['hydrodynamics'] = 'low energy'

elif cell1['depth1'] == 'supra-littoral' or cell1['depth1'] == 'littoral':
    if cell1['hydrodynamics'][1] >= 0.2:
        cell1['hydrodynamics'] = 'high energy'
    elif cell1['hydrodynamics'][1] <= 0.2:
        cell1['hydrodynamics'] = 'low energy'


# Depth2:
# Depends on littoral zone,
# depth depends on location in the Netherlands -- Should add later
# duration of flooding: should depend on MLWS and MHWN -- Should add later
# frequency of flooding:

if (cell1['depth1'] == 'sub-littoral') and (cell1['depth2'][0] >= 10):
    cell1['depth2'] = 'very deep'
elif (cell1['depth2'][0] >= 5) and (cell1['depth2'][0] < 10):
    cell1['depth2'] = 'deep'
elif cell1['depth2'][0] < 5:
    cell1['depth2'] = 'shallow'
else:
    cell1['depth2'] = np.nan

if cell1['depth1'] == 'littoral':
    if (cell1['depth2'][1] <= 100) and (cell1['depth2'][1] > 75):
        cell1['depth2'] = 'low littoral'
    elif (cell1['depth2'][1] <= 75) and (cell1['depth2'][1] > 25):
        cell1['depth2'] = 'middle high littoral'
    elif cell1['depth2'][1] < 25:
        cell1['depth2'] = 'high littoral'

if cell1['depth1'] == 'supra-littoral':
    if cell1['depth2'][2] > 300:
        ell1['depth2'] = 'potential pioneer zone'
    elif (cell1['depth2'][2] <= 300) and (cell1['depth2'][2] > 150):
        cell1['depth2'] = 'low salt marsh'
    elif (cell1['depth2'][2] <= 150) and (cell1['depth2'][2] > 50):
        cell1['depth2'] = 'middle salt marsh'
    elif (cell1['depth2'][2] <= 50) and (cell1['depth2'][2] > 5):
        cell1['depth2'] = 'high salt marsh'

# Substratum2:
# If there is a high silt percentage, this overrules the substratum
# Otherwise the grainsize is governing.

if cell1['substratum2'][1] >= 25 :
    cell1['substratum2'] = 'rich in silt'
elif cell1['substratum2'][0] <= 250:
    cell1['substratum2'] = 'fine sands'
elif (cell1['substratum2'][0] <= 2000) and (cell1['substratum2'][0] > 250):
    cell1['substratum2'] = 'coarse sands'
elif cell1['substratum2'][0] > 2000:
    cell1['substratum2'] = 'gravel'
else:
    cell1['substratum2'] = np.nan

#print(cell1)

# ECOTOPES

# def B2_11(data):
#     if not data['salinity'] == 'brakish':
#         return False
#     if not data['depth1'] == 'sub-littoral':
#         return False
#     if not data['hydrodynamics'] == 'high energy':
#         return False
#     if not data['depth2'] == np.nan:
#         return False
#     if not data['substratum2'] == np.nan:
#         return False
#     return 'B2_11'
# print(B2_11(cell1))
#
def B2_11s(data):
    if not data['salinity'] == 'brakish':
        return False
    if not data['depth1'] == 'sub-littoral':
        return False
    if not data['hydrodynamics'] == 'high energy':
        return False
    if not data['depth2'] == nan:
        return False
    if not data['substratum2'] == 'rich in silt':
        return False
    return 'B2_11s'
#print(B2_11s(cell1))

def B2_122s(data):
    if not data['salinity'] == 'brakish':
        return False
    if not data['depth1'] == 'sub-littoral':
        return False
    if not data['hydrodynamics'] == 'low energy':
        return False
    if not data['depth2'] == 'deep':
        return False
    if not data['substratum2'] == 'rich in silt':
        return False
    return 'B2_122s'
#print(B2_122s(cell1))

def B2_122f(data):
    if not data['salinity'] == 'brakish':
        return False
    if not data['depth1'] == 'sub-littoral':
        return False
    if not data['hydrodynamics'] == 'low energy':
        return False
    if not data['depth2'] == 'deep':
        return False
    if not data['substratum2'] == 'fine sands':
        return False
    return 'B2_122f'
#print(B2_122f(cell1))

#print(print(B2_122f(cell1)))
