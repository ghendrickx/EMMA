"""
Performance of EMMA with respect to existing ecotope-maps.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging

import numpy as np

_LOG = logging.getLogger(__name__)


# TODO: Translation from polygon data to model's grid points
def polygon2grid(polygon, grid) -> dict: pass


class Comparison:
    def __init__(self, data: dict, model: dict, **kwargs) -> None:

        # initiate required arguments
        self._data = data
        self._model = model

        # initiate optional arguments
        self.wild_card = kwargs.get('wild_card', 'x')

        # non-overlapping data
        if not all(k in data for k in model):
            _LOG.warning('Not all (x,y)-coordinates in `model` are present in `data`')
        if not all(k in model for k in data):
            _LOG.warning('Not all (x,y)-coordinates in `data` are present in `model`')

    @property
    def data(self) -> dict:
        return self._data

    @property
    def model(self) -> dict:
        return self._model

    def exec(self, level: int, **kwargs) -> dict:
        # optional arguments
        label: int = kwargs.get('specific_label')
        enable_wild_card: bool = kwargs.get('enable_wild_card', True)

        # check validity optional arguments
        if label is not None and not (0 <= label <= 6):
            msg = f'Ecotope-labels consists of six (6) items; ' \
                f'specific label comparison at {label} is out of range'
            raise ValueError(msg)

        # check validity `level`-argument
        if level < 0:
            msg = f'Level of comparison must be positive, negative value given: {level}'
            raise ValueError(msg)
        if level > 6:
            msg = f'Maximum level of comparison is six (6) (full comparison); {level} given'
            raise ValueError(msg)

        # filter data: only matching (x,y)-coordinates
        filtered = [(k, v, self.model[k]) for k, v in self.data.items() if k in self.model]

        # unpack filtered data
        xy, data, model = zip(*filtered)

        # decompose labels
        data = np.array(data).view('U1').reshape(len(data), -1)
        model = np.array(model).view('U1').reshape(len(model), -1)

        # remove dot from labels (if present)
        data = data[:, ~np.all(data == '.', axis=0)]
        model = model[:, ~np.all(model == '.', axis=0)]

        # compare labels
        wild_card = self.wild_card if enable_wild_card else False
        if label is None:
            result = np.all((data[:, :level] == model[:, :level]) | (data[:, :level] == wild_card), axis=1)
        else:
            result = (data[:, label] == model[:, label]) | (data[:, label] == wild_card)

        # return spatial performance
        return {k: v for k, v in zip(xy, result)}
