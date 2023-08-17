"""
This visualisation-function is used in the examples, which transforms the results and creates a scatter-plot with the
ecotopes, i.e., an ecotope-map.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import matplotlib.pyplot as plt

from src import _globals as glob


def create_figure(results: glob.TypeXYLabel) -> None:
    """Create a figure displaying the ecotope-map.

    :param results: mapped ecotope-data
    :type results: src._globals.TypeXYLabel
    """
    # re-structure results
    ecotopes = dict()
    for k, v in results.items():
        if v in ecotopes:
            ecotopes[v]['x'].append(k[0])
            ecotopes[v]['y'].append(k[1])
        else:
            ecotopes[v] = {'x': [k[0]], 'y': [k[1]]}

    # plot ecotopes
    for k, v in ecotopes.items():
        plt.scatter(v['x'], v['y'], label=k, s=1)

    # figure formatting
    plt.xlabel('x-coordinates')
    plt.ylabel('y-coordinates')
    plt.legend()

    # show figure
    plt.show()
