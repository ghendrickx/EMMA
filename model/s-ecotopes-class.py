from model._ecotopes_overview import ECOTOPES

class CellData:
    def __init__(self, salinity, depth1, hydrodynamics, depth2, substratum2):
        self.salinity = salinity
        self.depth1 = depth1
        self.hydrodynamics = hydrodynamics
        self.depth2 = depth2
        self.substratum2 = substratum2

        self.salinity_label = None
        self.depth1_label = None
        self.hydrodynamics_label = None
        self.depth2_label = None
        self.substratum2_label = None

        self._ecotope = None

    @property
    def ecotope_labels(self):
        """The collection of labels used to look-up the ecotope in the ECOTOPES-overview.

        :return: collection of ecotope-labels
        :rtype: tuple(str)
        """
        return (
            self.salinity_label, self.depth1_label, self.hydrodynamics_label, self.depth2_label, self.substratum2_label
        )

    @property
    def ecotope(self):
        """The ecotope of the cell based on the cell's abiotic characteristics.

        :return: ecotope
        :rtype: str
        """
        if self._ecotope is None:
            # this additional if-statement is included so you don't have to re-determine the ecotope everytime you
            # access it, only the first time, when it is still undefined.
            self._ecotope = ECOTOPES.get(self.ecotope_labels, 'undefined')

        return self._ecotope

def label_salinity(salinity):
    #Should add the variability
    """Determine the label of the salinity-attribute according to the

    :param salinity: salinity [ppm]
    :type salinity: float

    :return: salinity label
    :rtype: str
    """
    if salinity is None:
        return None
    elif salinity > 18:
        return 'marine'
    elif salinity < 5.4:
        return 'fresh'
    else:
        return 'brackish'

def label_depth1(depth1):
    """Determine the label of the salinity-attribute according to the

    :param depth1: frequency of flooding
        0 = supra-littoral
        0.1 - 0.99 = littoral
        1 = sub-littoral

    :type depth1: float

    :return: depth1 label
    :rtype: str
    """
    if depth1 is None:
        return None
    elif depth1 == 0:
        return 'supra-littoral'
    elif depth1 == 1:
        return 'sub-littoral'
    else:
        return 'littoral'

def label_hydrodynamics(hydrodynamics):
    """Determine the label of the hydrodynamics-attribute

    :param hydrodynamics: [linear current velocity, orbital velocity]
    :type hydrodynamics: list

    :return: hydrodynamics label
    :rtype: str
    """
    if hydrodynamics[0] is None:
        return None
    elif hydrodynamics[1] is None:
        return None
    elif hydrodynamics[0] == 0 and hydrodynamics[1] == 0:
        return 'stagnant'

    elif c.depth1_label == 'sub-littoral':
        if hydrodynamics[0] >= 0.8:
            return 'high energy'
        elif hydrodynamics[0] <= 0.8:
            return 'low energy'

    elif c.depth1_label == 'supra-littoral' or c.depth1_label == 'littoral':
        if hydrodynamics[1] >= 0.2:
            return 'high energy'
        elif hydrodynamics[1] <= 0.2:
            return 'low energy'

def label_depth2(depth2): # Should c.depth1_label be input?
    """Determine the label of the depth2-attribute

    :param depth2: [depth [m], duration of flooding [%], frequency of flooding (300-5)[ x /year]]
    :type depth2: list

    Note: Should depend on location in the Netherlands, should depend on MLWS and MHWN


    :return: hydrodynamics label
    :rtype: str
    """
    if c.depth1_label is None:
        return None
    elif depth2[0] is None:
        return None
    elif depth2[1] is None:
        return None
    if c.depth1_label == 'sub-littoral':
        if depth2[0] >= 10:
            return 'very deep'
        elif depth2[0] < 5:
            return 'shallow'
        else:
            return 'deep'

    elif c.depth1_label == 'littoral':
        if depth2[1] < 25:
            return 'high littoral'
        if depth2[1] > 75:
            return 'low littoral'
        else:
            return 'middle high littoral'

    else:
        if depth2[2] > 300:
            return 'potential pioneer zone'
        elif depth2[2] <= 300 and depth2[2] > 150:
            return 'low salt marsh'
        elif depth2[2] <= 150 and depth2[2] > 50:
            return 'middle salt marsh'
        else:
            return 'high salt marsh'

def label_substratum2(substratum2):
    """Determine the label of the substratum2-attribute according to the

    :param substratum2: [median grainsize (micro-m), silt percentage (%)]
    :type salinity: list

    :return: substratum2 label
    :rtype: str
    """
    if substratum2[0] is None:
        return None
    elif substratum2[1] is None:
        return None
    elif substratum2[1] >= 25:
        return 'rich in silt'
    elif substratum2[0] <= 250:
        return 'fine sands'
    elif substratum2[0] > 2000:
        return 'gravel'
    else:
        return 'coarse sands'


cell1 = CellData(salinity = 6, depth1 = 0, hydrodynamics = [0, 0.5], depth2 = [7, 5, 300], substratum2 = [200, 10])
cell2 = CellData(salinity = 20, depth1 = 0.8, hydrodynamics = [0, 0], depth2 = [7, 5, 300], substratum2 = [200, 30])
cell3 = CellData(salinity = 5, depth1 = 1, hydrodynamics = [0.3, 0.9], depth2 = [7, 5, 300], substratum2 = [200, 30])

cells = [cell1, cell2, cell3]
#
for c in cells:
    c.salinity_label = label_salinity(c.salinity)
    c.depth1_label = label_depth1(c.depth1)
    c.hydrodynamics_label = label_hydrodynamics(c.hydrodynamics)
    c.depth2_label = label_depth2(c.depth2)
    c.substratum2_label = label_substratum2(c.substratum2)
# #
# print('cell1:', cell1.salinity_label, cell1.depth1_label, cell1.hydrodynamics_label, cell1.depth2_label, cell1.substratum2_label)
# cell1 = (cell1.salinity_label, cell1.depth1_label, cell1.hydrodynamics_label, cell1.depth2_label, cell1.substratum2_label)
# # >>> brackish marine
# print('cell2:', cell2.salinity_label, cell2.depth1_label, cell1.hydrodynamics_label, cell1.depth2_label, cell1.substratum2_label)
# print('cell3:', cell3.salinity_label, cell3.depth1_label, cell3.hydrodynamics_label, cell3.depth2_label, cell3.substratum2_label)

# def check(dict, cell):
#     cell
#     try:
#         label = dict[cell]
#     except:
#         label = "BXX_XXX"
#     return label
#print(check(ECOTOPES, cell1))

# The method below will do something similar to the above, but than all grouped in a method. However, you will loose the
# Cell-object, which is deleted once the method has been completed. There are many ways to keep the Cell-object though:
# 1. return the Cell-object instead of its ecotope-property [easy-fix];
# 2. store every newly created Cell-object, which is to be coded within the Cell-object (see grid.py > Cell) [advanced].

def label_ecotope(salinity, depth1, hydrodynamics, depth2, substratum2):
    cell = CellData(salinity=salinity, depth1=depth1, hydrodynamics=hydrodynamics, depth2=depth2, substratum2=substratum2)
    cell.salinity_label = label_salinity(cell.salinity)
    cell.depth1_label = label_depth1(cell.depth1)
    cell.hydrodynamics_label = label_hydrodynamics(cell.hydrodynamics)
    cell.depth2_label = label_depth2(cell.depth2)
    cell.substratum2 = label_substratum2(cell.substratum2)
    cell_labels = (cell.salinity_label, cell.depth1_label, cell.hydrodynamics_label, cell.depth2_label, cell.substratum2_label)
    print(cell_labels)
    try:
       label = ECOTOPES[cell_labels]
    except:
      print("NO MATCH")
      label = "BXX_XXX"
    return label

print(label_ecotope( 18, 1, [0, 0], [7, 5, 300], [200, 10]))
