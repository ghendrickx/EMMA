from model._ecotopes_overview import ECOTOPES


class Cell:
    # As the grid also uses Cell-objects, you may want to rename this object;
    # e.g. to Ecotope, or CellEcotope, or CellVariables, or ...?
    # Then, this object can be coupled to the Cell-object in grid.py.

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


# def label_salinity(salinity):
#     if (salinity >= 5.4) & (salinity <= 18):
#         return 'brackish'
#     elif salinity > 18:
#         return 'marine'
#     elif salinity < 5.4:
#         return 'fresh'

# The method below is similar to the above, but less error-prone: Have a look a the if-statements.
# This is just a small detail, though!

def label_salinity(salinity):
    """Determine the label of the salinity-attribute according to the

    :param salinity: salinity [ppm]
    :type salinity: float

    :return: salinity ecotope-label
    :rtype: str
    """
    if salinity > 18:
        return 'marine'
    elif salinity < 5.4:
        return 'fresh'
    else:
        return 'brackish'


cell1 = Cell(salinity = 6, depth1 = 1, hydrodynamics = [0.3, 0.9], depth2 = [7, 5, 300], substratum2 = [200, 30])
cell2 = Cell(salinity = 20, depth1 = 1, hydrodynamics = [0.3, 0.9], depth2 = [7, 5, 300], substratum2 = [200, 30])

cells = [cell1, cell2]

for c in cells:
    c.salinity_label = label_salinity(c.salinity)

print(cell1.salinity_label)

def eco_return(salinity, depth1, hydrodynamics, depth2, substratum2):
    return cell[]
