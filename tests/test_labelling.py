"""
Tests for `src/labelling.py`.

Author: Gijs G. Hendrickx
"""
import pytest

from config import config_file
from src import labelling as lab

"""Set configuration file"""
lab.glob.LABEL_CONFIG = config_file.load_config('emma.json')

"""TestClasses"""


@pytest.mark.parametrize(
    'mean, std, label',
    [
        (None, 0, 'x'),
        (10, 3, 'v'),
        (2.5, 0, 'f'),
        (28, 4, 'z'),
        (15, 3, 'b'),
    ]
)
def test_salinity_label(mean, std, label):
    """Test labelling of Salinity."""
    out = lab.salinity_code(mean, std)
    assert out.lower() == label


@pytest.mark.parametrize(
    'key, label',
    [
        (None, 'x'),
        ('hard', 1),
        ('soft', 2),
    ]
)
def test_substratum1_label(key, label):
    """Test labelling of Substratum 1."""
    out = lab.substratum_1_code(key)
    assert out.lower() == str(label)


# TODO: Add tests that implement `mlws` and `mhwn`.
@pytest.mark.parametrize(
    'depth, mlws, mhwn, label',
    [
        (None, None, None, 'x'),
        (2.8, None, None, 1),
        (0, None, None, 2),
        (-2.5, None, None, 3),
    ]
)
def test_depth1_label(depth, mlws, mhwn, label):
    """Test labelling of Depth 1."""
    out = lab.depth_1_code(depth, mlws, mhwn)
    assert out.lower() == str(label)


@pytest.mark.parametrize(
    'velocity, depth1, label',
    [
        (None, '', 'x'),
        (.75, 1, 1),
        (.65, 1, 2),
        (.75, 2, 1),
        (.65, 2, 2),
        (0, '', 3),
    ]
)
def test_hydrodynamics_label(velocity, depth1, label):
    """Test labelling of Hydrodynamics."""
    out = lab.hydrodynamics_code(velocity, str(depth1))
    assert out.lower() == str(label)


@pytest.mark.parametrize(
    'sub1, depth1, depth, inundated, frequency, label',
    [
        (1, '', 0, 0, 0, ''),
        ('', 'x', 0, 0, 0, 'x'),
        (2, 1, 35, 0, 0, 1),
        (2, 1, 13, 0, 0, 2),
        (2, 1, 3, 0, 0, 3),
        (2, 2, 0, 1, 0, 1),
        (2, 2, 0, .5, 0, 2),
        (2, 2, 0, 0, 0, 3),
        (2, 3, 0, 0, 350, 1),
        (2, 3, 0, 0, 300, 2),
        (2, 3, 0, 0, 100, 3),
        (2, 3, 0, 0, 20, 4),
    ]
)
def test_depth2_label(sub1, depth1, depth, inundated, frequency, label):
    out = lab.depth_2_code(str(sub1), str(depth1), depth, inundated, frequency)
    assert out.lower() == str(label)


class TestSubstratum2Code:
    """Tests for `substratum_2_code()`."""

    def test_undefined(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.substratum_2_code('x', '', 0.)
        assert output == 'x'

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        # noinspection PyTypeChecker
        output = lab.substratum_2_code(None, '', 0.)
        assert output == 'x'

    def test_hydrodynamics_undefined(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.substratum_2_code('1', 'x', 0.)
        assert output == 'x'

    def test_hydrodynamics_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        # noinspection PyTypeChecker
        output = lab.substratum_2_code('1', None, 0.)
        assert output == 'x'

    def test_hard_low_stone_wood(self):
        """Test the ecotope-code determination resulting in 'stond/wood' ('2') for 'hard substratum' ('1') and 'low
        energy' ('2') conditions.
        """
        output = lab.substratum_2_code('1', '2', 0.)
        assert output == '1'

    def test_hard_stagnant_stone_wood(self):
        """Test the ecotope-code determination resulting in 'stond/wood' ('2') for 'hard substratum' ('1') and
        'stagnant' ('3') conditions.
        """
        output = lab.substratum_2_code('1', '3', 0.)
        assert output == '1'

    def test_hard_peat(self):
        """Test the ecotope-code determination resulting in 'peat' ('2') for 'hard substratum' ('1') and 'high energy'
        ('2') conditions.
        """
        output = lab.substratum_2_code('1', '1', 0.)
        assert output == '2'

    def test_grains_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        # noinspection PyTypeChecker
        output = lab.substratum_2_code('2', '', None)
        assert output == 'x'

    def test_soft_silt(self):
        """Test the ecotope-code determination resulting in 'silt' ('s') for 'soft substratum' ('2')."""
        output = lab.substratum_2_code('2', '', 20)
        assert output == 's'

    def test_soft_fines(self):
        """Test the ecotope-code determination resulting in 'fine sand' ('f') for 'soft substratum' ('2')."""
        output = lab.substratum_2_code('2', '', 100)
        assert output == 'f'

    def test_soft_sand(self):
        """Test the ecotope-code determination resulting in 'coarse sand' ('z') for 'soft substratum' ('2')."""
        output = lab.substratum_2_code('2', '', 2000)
        assert output == 'z'

    def test_soft_gravel(self):
        """Test the ecotope-code determination resulting in 'gravel' ('g') for 'soft substratum' ('2')."""
        output = lab.substratum_2_code('2', '', 3000)
        assert output == 'g'
