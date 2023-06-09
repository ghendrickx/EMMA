import numpy as np
from _ecotopes_overview import ECOTOPES

# Input data
# B2_11s
#B2_122f
cell1 = dict([('salinity', 6), ('depth1', 1), ('hydrodynamics', [0.3, 0.9]), ('depth2', [7, 5, 300]), ('substratum2', [200, 10])])
#print(cell1)
#B2_122s
cell2 = dict([('salinity', 20), ('depth1', 1), ('hydrodynamics', [0.3, 0.9]), ('depth2', [7, 5, 300]), ('substratum2', [200, 30])])
celllist = [cell1, cell2]
celllist_label = [[] for _ in range(len(celllist))]

def label_salinity(cell, cell_label):
    """
    Determines label of salinity
    :param: cell: salinity [ppm]
    :type: dict

    :return: salinity label
    :rtype: dict
    """
    if cell['salinity'] is None:
        cell_label.append(None)
    elif (cell['salinity'] >= 5.4) & (cell['salinity'] <= 18):
        cell_label.append('brackish')
    elif cell['salinity'] > 18:
        cell_label.append('marine')
    elif cell['salinity'] < 5.4:
        cell_label.append('fresh')

def label_depth1(cell, cell_label):
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
    if cell['depth1'] is None:
        cell_label.append(None)
    elif cell['depth1'] == 0:
        cell_label.append('supra-littoral')
    elif cell['depth1'] == 1:
        cell_label.append('sub-littoral')
    else:
        cell_label.append('littoral')

def label_hydrodynamics(cell, cell_label):
    """
    Determines label of hydrodynamics
    :param cell: hydrodynamics [m/s] [linear current velocity, orbital velocity]
    :type: dict

    :return: hydrodynamics label
    :rtype: dict
    """
    if cell['hydrodynamics'] is None:
        cell_label.append( None)
    elif cell['hydrodynamics'][0] == 0 and cell['hydrodynamics'][1] == 0:
        cell_label.append('stagnant')
    elif cell['depth1'] == 'sub-littoral': #or cell1['depth1'] == 'littoral':
        if cell['hydrodynamics'][0] >= 0.8:
            cell_label.append('high energy')
    elif cell['hydrodynamics'][0] <= 0.8:
        cell_label.append('low energy')

    elif cell['depth1'] == 'supra-littoral' or cell['depth1'] == 'littoral':
        if cell['hydrodynamics'][1] >= 0.2:
            cell_label.append('high energy')
    elif cell['hydrodynamics'][1] <= 0.2:
        cell_label.append('low energy')

def label_depth2(cell, cell_label):
    """"
    Determines label of depth2
    TODO: Should depend on location in the Netherlands
    TODO: Duration of flooding should depend on MLWS and MHWN
    [depth [m], duration of flooding [%], frequency of flooding (300-5)[ x /year]]
    :param: cell: depth2
    :type: dict

    :return: depth2 label
    :rtype: dict
    """
    if cell['depth1'] is None:
        cell['depth1'] = None
    elif (cell['depth1'] == 'sub-littoral') and (cell['depth2'][0] >= 10):
        cell_label.append('very deep')
    elif (cell['depth2'][0] >= 5) and (cell['depth2'][0] < 10):
        cell_label.append('deep')
    elif cell['depth2'][0] < 5:
        cell_label.append('shallow')

    elif cell['depth1'] == 'littoral':
        if (cell['depth2'][1] <= 100) and (cell['depth2'][1] > 75):
            cell_label.append('low littoral')
        elif (cell['depth2'][1] <= 75) and (cell['depth2'][1] > 25):
            cell_label.append('middle high littoral')
        elif cell['depth2'][1] < 25:
            cell_label.append('high littoral')

    elif cell['depth1'] == 'supra-littoral':
        if cell['depth2'][2] > 300:
            cell_label.append('potential pioneer zone')
        elif (cell['depth2'][2] <= 300) and (cell['depth2'][2] > 150):
            cell_label.append('low salt marsh')
        elif (cell['depth2'][2] <= 150) and (cell['depth2'][2] > 50):
            cell_label.append('middle salt marsh')
        elif (cell['depth2'][2] <= 50) and (cell['depth2'][2] > 5):
            cell_label.append('high salt marsh')

def label_substratum2(cell, cell_label):
    """
    Determines label of substratum2
    :param: cell: substratum2 [median grain size [micro-m], silt percentage [%]]
    :type: dict

    :return: substratum2 label
    :rtype: dict
    """
    if cell['substratum2'] is None:
        cell_label.append(None)
    elif cell['substratum2'][1] >= 25:
        cell_label.append('rich in silt')
    elif cell['substratum2'][0] <= 250:
        cell_label.append('fine sands')
    elif (cell['substratum2'][0] <= 2000) and (cell['substratum2'][0] > 250):
        cell_label.append('coarse sands')
    elif cell['substratum2'][0] > 2000:
        cell_label.append('gravel')


for i in range(len(celllist)):
   label_salinity(celllist[i], celllist_label[i])
   label_depth1(celllist[i], celllist_label[i] )
   label_hydrodynamics(celllist[i], celllist_label[i])
   label_depth2(celllist[i], celllist_label[i])
   label_substratum2(celllist[i], celllist_label[i])

def label_ecotope(celllist_labels):
    labels = []
    celllist_label = [tuple(l) for l in celllist_labels]
    celllist_labels = tuple(celllist_label)

    for i in range(len(celllist_label)):
        celllist_labels = tuple(celllist_label[i])
        try:
            label = ECOTOPES[celllist_label[i]]
            labels.append(label)
        except:
            label = "BXX_XXX"
            labels.append(label)
    print(labels)

print(celllist)
print(celllist_label)
label_ecotope(celllist_label)