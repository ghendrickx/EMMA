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


def substratum_1_code(substratum_type: str) -> str:
    """Determine ecotope-code in the category 'substratum 1'.

    :param substratum_type: hard or soft substratum
    :type substratum_type: str

    :return: substratum 1 code
    :rtype: str
    """
    # substratum 1 component unknown
    if substratum_type is None:
        return 'x'

    # soft substratum
    elif substratum_type == 'soft':
        return '2'

    # hard substratum
    return '1'


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


def hydrodynamics_code(velocity: float, code_depth_1: str) -> str:
    """Determine ecotope-code in the category 'hydrodynamic'.

    :param velocity: flow velocity [m/s]
    :param depth: ecotope-code of 'depth 1'

    :type velocity: float
    :type depth: str

    :return: hydrodynamics code
    :rtype: str
    """
    # hydrodynamic unknown component
    if velocity is None:
        return 'x'

    # no flow: stagnant
    elif velocity == 0:
        return '3'

    # sub-littoral flow
    elif code_depth_1 == '1':
        return '1' if velocity > .8 else '2'

    # littoral flow
    return '1' if velocity > .2 else '2'


def depth_2_code(code_substratum_1: str, code_depth_1: str, depth: float, inundated: float, frequency: int) -> str:
    """Determine ecotope-code in the category 'depth 2'.

    :param code_substratum_1: ecotope-code of 'substratum 1'
    :param code_depth_1: ecotope-code of 'depth 1'
    :param depth: water depth [m]
    :param inundated: temporal percentage of inundation [-]
    :param frequency: annual frequency of flooding [n/yr]

    :type code_substratum_1: str
    :type code_depth_1: str
    :type depth: float
    :type inundated: float
    :type frequency: int

    :return: depth 2 code
    :rtype: str
    """
    # hard substratum: no depth 2 label/code
    if code_substratum_1 == '1':
        return ''

    # depth 2 unknown component
    if code_depth_1 in (None, 'x'):
        return 'x'

    # sub-littoral: water depth
    elif code_depth_1 == '1':
        if depth >= 10:
            return '1'
        elif depth < 5:
            return '3'
        return '2'

    # littoral: inundation time
    elif code_depth_1 == '2':
        if inundated > .75:
            return '1'
        elif inundated < .25:
            return '3'
        return '2'

    # supra-littoral: flood frequency
    elif code_depth_1 == '3':
        if frequency > 300:
            return '1'
        elif frequency > 150:
            return '2'
        elif frequency > 50:
            return '3'
        return '4'

    # raise error
    else:
        raise NotImplementedError


def substratum_2_code(code_substratum_1: str, code_hydrodynamics: str, grain_size: float) -> str:
    """Determine ecotope-code in the category 'substratum 2'.

    :param grain_size: median grain size [um]
    :type grain_size: float

    :return: substratum 2 code
    :rtype: str
    """
    # substratum 2 component unknown
    if code_substratum_1 in (None, 'x'):
        return 'x'

    # hard substratum
    elif code_substratum_1 == '1':
        if code_hydrodynamics in (None, 'x'):
            return 'x'
        elif code_hydrodynamics == '1':
            return '2'
        return '1'

    # soft substratum
    elif code_substratum_1 == '2':
        if grain_size is None:
            return 'x'
        elif grain_size <= 25:
            return 's'
        elif grain_size <= 250:
            return 'f'
        elif grain_size <= 2000:
            return 'z'
        return 'g'
