class Cell:
    def __init__(self, salinity, depth1, hydrodynamics, depth2, substratum2):
        self.salinity = salinity
        self.depth1 = depth1
        self.hydrodynamics = hydrodynamics
        self.depth2 = depth2
        self.substratum2 = substratum2

        self.salinity_label = None

def label_salinity(salinity):
    if (salinity >= 5.4) & (salinity <= 18):
        return 'brackish'
    elif salinity > 18:
        return 'marine'
    elif salinity < 5.4:
        return 'fresh'

cell1 = Cell(salinity = 6, depth1 = 1, hydrodynamics = [0.3, 0.9], depth2 = [7, 5, 300], substratum2 = [200, 30])
cell2 = Cell(salinity = 20, depth1 = 1, hydrodynamics = [0.3, 0.9], depth2 = [7, 5, 300], substratum2 = [200, 30])

cells = [cell1, cell2]

for c in cells:
    c.salinity_label = label_salinity(c.salinity)

print(cell1.salinity_label)
print(cell2.salinity_label)

#def eco_return(salinity, depth1, hydrodynamics, depth2, substratum2):
#    return cell[]