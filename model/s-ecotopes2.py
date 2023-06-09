import time
start_time = time.time()
eco = {'B2_112s': {'salinity': 'brakish', 'depth1': 'sub-littoral', 'hydrodynamics' : 'low energy' ,'depth2' : 'deep' , 'substratum2' : 'rich in silt'},
       'B2_122f': {'salinity': 'brakish', 'depth1': 'sub-littoral', 'hydrodynamics' : 'low energy', 'depth2' : 'deep', 'substratum2' : 'fine sands'}}

#eco = dict([('B2_112s', dict([('salinity', 'brakish'), ('depth1', 'sub-littoral'), ('hydrodynamics','low energy'), ('depth2', 'deep'), ('substratum2', 'rich in silt')]))],
#            [('B2_122f', ['brakish', 'sub-littoral', 'low energy', 'deep', 'fine sands']))])

cell1 = dict([('salinity', 6), ('depth1', 1), ('hydrodynamics', [0.3, 0.9]), ('depth2', [7, 5, 300]), ('substratum2', [200, 30])])

# Salinity: should later check for salinity fluctuation as well: (4*std/mean)*100%
if (cell1['salinity'] >= 5.4) & (cell1['salinity'] <= 18):
    cell1['salinity'] = 'brakish'
elif cell1['salinity'] > 18:
    cell1['salinity'] = 'marine'
elif cell1['salinity'] < 5.4:
    cell1['salinity'] = 'fresh'

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

#print(eco)
#print(cell1)

#print(eco['B2_112s'] == cell1)

print(eco['B2_122f'] == cell1)
end_time = time.time()
print((end_time-start_time)*10000)