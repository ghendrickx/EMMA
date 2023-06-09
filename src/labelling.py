"""
Labelling of ecotopes.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""


def salinity_code(salinity_mean: float, salinity_min: float, salinity_max: float) -> str:
    """Determine ecotope-code in the category 'salinity'.

    :param salinity_mean: temporal mean salinity [psu]
    :param salinity_min: temporal minimum salinity [psu]
    :param salinity_max: temporal maximum salinity [psu]

    :type salinity_mean: float
    :type salinity_min: float
    :type salinity_max: float

    :return: salinity code
    :rtype: str
    """
    # salinity component unknown
    if salinity_mean is None:
        return 'x'

    # salinity label: variable
    if salinity_max - salinity_min > salinity_mean:
        return 'V'

    # salinity label: fresh
    elif salinity_mean < 5.4:
        return 'F'

    # salinity label: marine
    elif salinity_mean > 18:
        return 'Z'

    # salinity label: brackish
    return 'B'


def depth_1_code(inundated: float) -> str:
    """Determine ecotope-code in the category 'depth 1'.

    :param inundated: temporal percentage of inundation [-]
    :type inundated: float

    :return: depth 1 code
    :rtype: str
    """
    # depth 1 component unknown
    if inundated is None:
        return 'x'

    # always inundated: sub-littoral
    elif inundated == 1:
        return '1'

    # always drained: supra-littoral
    elif inundated == 0:
        return '3'

    # periodically inundated: littoral
    return '2'
