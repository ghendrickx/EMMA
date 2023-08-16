"""
Performance of EMMA with respect to existing ecotope-maps.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import logging

import numpy as np

_LOG = logging.getLogger(__name__)


class Comparison:

    def __init__(self, measurements: dict, predictions: dict, **kwargs) -> None:
        # initiate required arguments
        self._measurements = measurements
        self._predictions = predictions

        # initiate optional arguments
        self.wild_card = kwargs.get('wild_card', 'x')

        # non-overlapping data
        if not all(k in measurements for k in predictions):
            _LOG.warning('Not all (x,y)-coordinates in `predictions` are present in `measurements`')
        if not all(k in predictions for k in measurements):
            _LOG.warning('Not all (x,y)-coordinates in `measurements` are present in `predictions`')

    @property
    def measurements(self) -> dict:
        return self._measurements

    @property
    def predictions(self) -> dict:
        return self._predictions

    def exec(self, level: int, **kwargs) -> dict:
        # optional arguments
        label: int = kwargs.get('specific_label')
        enable_wild_card: bool = kwargs.get('enable_wild_card', True)

        # check validity optional arguments
        if label is not None and not (0 <= label <= 5):
            msg = f'Ecotope-labels consists of five (5) items; ' \
                f'specific label comparison at {label} is out of range'
            raise ValueError(msg)

        # check validity `level`-argument
        if level > 5:
            msg = f'Maximum level of comparison is 5 (full comparison); {level} given'
            raise ValueError(msg)

        # filter data: only matching (x,y)-coordinates
        filtered = [(k, v, self.predictions[k]) for k, v in self.measurements.items() if k in self.predictions]

        # unpack filtered data
        xy, data, model = zip(*filtered)

        # decompose labels
        data = np.array(data).view('U1').reshape(len(data), -1)
        model = np.array(model).view('U1').reshape(len(model), -1)

        # remove dot from labels
        data = np.delete(data, 2, axis=1)
        model = np.delete(model, 2, axis=1)

        # compare labels
        wild_card = self.wild_card if enable_wild_card else False
        if label is None:
            result = np.all((data[:, :level] == model[:, :level]) | (data[:, :level] == wild_card), axis=1)
        else:
            result = (data[:, label] == model[:, label]) | (data[:, label] == wild_card)

        # return spatial performance
        return {k: v for k, v in zip(xy, result)}
