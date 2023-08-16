"""
Performance of EMMA with respect to existing ecotope-maps.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging

import numpy as np
import typing

from src.processing import __TYPE_XY_LABEL

_LOG = logging.getLogger(__name__)


# TODO: Translation from polygon data to model's grid points
def polygon2grid(polygon, grid) -> __TYPE_XY_LABEL:
    """Project polygon data (i.e., ecotope-map(s)) to model's grid points for comparison.

    :param polygon: polygon data
    :param grid: model's grid points

    :type polygon:
    :type grid:

    :return: gridded data
    :rtype: dict
    """


class Comparison:
    """Compare ecotope-map(s) considered as ground-truth to the map(s) as predicted by `EMMA` from hydrodynamic model
    results.
    """
    __TYPE_XY_LABEL = __TYPE_XY_LABEL

    def __init__(self, data: __TYPE_XY_LABEL, model: __TYPE_XY_LABEL, **kwargs) -> None:
        """Both `data` and `model` must be formatted as follows: (x,y)-coordinates as key, and the ecotope-label as
        value (`str`). This corresponds with the formatting of the returned `dict` by `map_ecotopes()` (from
        `src.processing`).
        >>> data = {
        ...     (0, 0): 'Z2.222f',
        ... }

        :param data: ground-truth ecotope-labels
        :param model: predicted ecotope-labels
        :param kwargs: optional arguments
            wild_card: wild-card character in ecotope-labels, defaults to 'x'

        :type data: dict[tuple[float, float], str]
        :type model: dict[tuple[float, float], str]
        :type kwargs: optional
            wild_card: str
        """
        # initiate required arguments
        self._data = data
        self._model = model

        # initiate optional arguments
        self.wild_card: str = kwargs.get('wild_card', 'x')

        # non-overlapping data
        if not all(k in data for k in model):
            _LOG.warning('Not all (x,y)-coordinates in `model` are present in `data`')
        if not all(k in model for k in data):
            _LOG.warning('Not all (x,y)-coordinates in `data` are present in `model`')

    @property
    def data(self) -> __TYPE_XY_LABEL:
        """
        :return: ground-truth ecotope-labels
        :rtype: dict[tuple[float, float], str]
        """
        return self._data

    @property
    def model(self) -> __TYPE_XY_LABEL:
        """
        :return: predicted ecotope-labels
        :rtype: dict[tuple[float, float], str]
        """
        return self._model

    def exec(self, level: int, **kwargs) -> typing.Dict[typing.Tuple[float, float], bool]:
        """Execute the comparison up to a given level of detail. This level of detail reflects the number of label-
        components (i.e., letters or numbers) to assess, starting from the left. Note that this excludes any dots (.) in
        the labels. In case the `specific_label` is enabled, `level` reflects the index of the label-component to
        assess. Thus, with `specific_label` disabled (default), the labels are assessed as `label[:level]`; and with
        `specific_label` enabled, the labels are assessed as `label[level]`.

        Ecotope-labels may contain wild cards (default: 'x'), which may represent any letter or number of the ecotope-
        label. Thus, 'Z2.222f' and 'Z2.222x' are considered a match. This type of assessment can be disabled by setting
        the optional argument `enable_wild_card=False` (default: True).

        :param level: level of assessment
        :param kwargs: optional arguments
            enable_wild_card: the wild card character reflects a match, defaults to True
            specific_label: assess a specific label only (defined by `level`), defaults to False

        :type level: int
        :type kwargs: optional
            enable_wild_card: bool
            specific_label: bool

        :return: spatial distribution of matching ecotope-labels
        :rtype: dict[tuple[float, float], bool]

        :raises ValueError: if `level` exceeds ecotope-label components (if `specific_label=True`)
        :raises ValueError: if `level` is negative
        :raises AssertionError: if (x,y)-coordinates, ground-truth ecotope-labels, and predicted ecotope-labels have
            mismatching sizes
        """
        # optional arguments
        enable_wild_card: bool = kwargs.get('enable_wild_card', True)
        specific_label: bool = kwargs.get('specific_label', False)

        # check validity `level`-argument
        if specific_label and not (0 <= level <= 5):
            msg = f'Ecotope-labels consists of six (6) items; ' \
                f'specific label comparison at {level} is out of range'
            raise ValueError(msg)
        if level < 0:
            msg = f'Level of comparison must be positive, negative value given: {level}'
            raise ValueError(msg)
        if level > 5:
            _LOG.debug(f'Maximum level of comparison is five (5) (full comparison); {level} given')

        # filter and pack data: only (x,y)-coordinates present in data
        filtered = [(k, v, self.model[k]) for k, v in self.data.items() if k in self.model]

        # unpack filtered data
        xy, data, model = zip(*filtered)
        assert len(xy) == len(data) == len(model), \
            f'Sizes of (x,y)-coordinates, ground-truth ecotope-labels, and predicted ecotope-labels must be equal; ' \
            f'respective sizes are {len(xy)}, {len(data)}, and {len(model)}'

        # decompose labels
        data = np.array(data).view('U1').reshape(len(data), -1)
        model = np.array(model).view('U1').reshape(len(model), -1)

        # remove dot from labels (if present)
        data = data[:, ~np.all(data == '.', axis=0)]
        model = model[:, ~np.all(model == '.', axis=0)]

        # append empty string to match label-sizes (if required)
        if data.shape < model.shape:
            data = np.append(data, np.empty((len(data), 1), dtype=str), axis=1)
        elif data.shape > model.shape:
            model = np.append(model, np.empty((len(model), 1), dtype=str), axis=1)

        # compare labels
        wild_card = self.wild_card if enable_wild_card else False
        if specific_label:
            result = np.all((data[:, :level] == model[:, :level]) | (data[:, :level] == wild_card), axis=1)
        else:
            result = (data[:, level] == model[:, level]) | (data[:, level] == wild_card)

        # return spatial performance
        return {k: v for k, v in zip(xy, result)}
