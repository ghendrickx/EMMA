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


class Comparison:

    __TYPE_XY_LABEL = __TYPE_XY_LABEL

    def __init__(self, data: __TYPE_XY_LABEL, model: __TYPE_XY_LABEL, **kwargs) -> None:
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
        return self._data

    @property
    def model(self) -> __TYPE_XY_LABEL:
        return self._model

    def exec(self, level: int, **kwargs) -> typing.Dict[typing.Tuple[float, float], bool]:
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
