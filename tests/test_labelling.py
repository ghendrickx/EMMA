"""
Tests for `labelling.py`.

Author: Gijs G. Hendrickx
"""
from config import config_file
from src import labelling as lab

"""Set configuration file"""
lab.CONFIG = config_file.load_config()

"""TestClasses"""


class TestSalinityCode:
    """Tests for `salinity_code()`."""

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.salinity_code(None, 0)
        assert output == 'x'

    def test_variable(self):
        """Test the ecotope-code determination resulting in 'variable' ('V')."""
        output = lab.salinity_code(10, 3)
        assert output == 'V'

    def test_fresh(self):
        """Test the ecotope-code determination resulting in 'freshwater' ('F')."""
        output = lab.salinity_code(2.5, 0)
        assert output == 'F'

    def test_marine(self):
        """Test the ecotope-code determination resulting in 'marine' ('Z')."""
        output = lab.salinity_code(28, 4)
        assert output == 'Z'

    def test_brackish(self):
        """Test the ecoptope-code determination resulting in 'brackish' ('B')."""
        output = lab.salinity_code(15, 3)
        assert output == 'B'


class TestSubstratum1Code:
    """Tests for `substratum_1_code()`."""

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.substratum_1_code(None)
        assert output == 'x'

    def test_hard(self):
        """Test the ecotope-code determination resulting in 'hard' ('1')."""
        output = lab.substratum_1_code('hard')
        assert output == '1'

    def test_soft(self):
        """Test the ecotope-code determination resulting in 'soft' ('2')."""
        output = lab.substratum_1_code('soft')
        assert output == '2'


class TestDepth1Code:
    """Tests for `depth_1_code()`."""

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.depth_1_code(None)
        assert output == 'x'

    def test_sub_littoral(self):
        """Test the ecotope-code determination resulting in 'sub-littoral' ('1')."""
        output = lab.depth_1_code(2.5)
        assert output == '1'

    def test_littoral(self):
        """Test the ecotope-code determination resulting in 'littoral' ('2')."""
        output = lab.depth_1_code(0)
        assert output == '2'

    def test_supra_littoral(self):
        """Test the ecotope-code determination resulting in 'supra-littoral' ('3')."""
        output = lab.depth_1_code(-2.5)
        assert output == '3'


class TestHydrodynamicsCode:
    """Tests for `hydrodynamics_code()`."""

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.hydrodynamics_code(None, '')
        assert output == 'x'

    def test_sub_littoral_high_energy(self):
        """Test the ecotope-code determination resulting in 'high energy' ('1') for 'sub-littoral' ('1') conditions."""
        output = lab.hydrodynamics_code(.9, '1')
        assert output == '1'

    def test_sub_littoral_low_energy(self):
        """Test the ecotope-code determination resulting in 'low energy' ('2') for 'sub-littoral' ('1') conditions."""
        output = lab.hydrodynamics_code(.7, '1')
        assert output == '2'

    def test_littoral_high_energy(self):
        """Test the ecotope-code determination resulting in 'high energy' ('1') for 'littoral' ('2') conditions."""
        output = lab.hydrodynamics_code(.3, '2')
        assert output == '1'

    def test_littoral_low_energy(self):
        """Test the ecotope-code determination resulting in 'low energy' ('2') for 'littoral' ('2') conditions."""
        output = lab.hydrodynamics_code(.1, '2')
        assert output == '2'

    def test_stagnant(self):
        """Test the ecotope-code determination resulting in 'stagnant' ('3')."""
        output = lab.hydrodynamics_code(0., '')
        assert output == '3'


class TestDepth2Code:
    """Tests for `depth_2_code()`."""

    def test_undefined(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.depth_2_code('1', '', 0., 0., 0)
        assert output == ''

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.depth_2_code('', None, 0., 0., 0)
        assert output == 'x'

    def test_unknown_x(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.depth_2_code('', 'x', 0., 0., 0)
        assert output == 'x'

    def test_sub_littoral_very_deep(self):
        """Test the ecotope-code determination resulting in 'very deep' ('1') for 'sub-littoral' ('1') conditions."""
        output = lab.depth_2_code('2', '1', 11., 0., 0)
        assert output == '1'

    def test_sub_littoral_deep(self):
        """Test the ecotope-code determination resulting in 'deep' ('2') for 'sub-littoral' ('1') conditions."""
        output = lab.depth_2_code('2', '1', 8., 0., 0)
        assert output == '2'

    def test_sub_littoral_shallow(self):
        """Test the ecotope-code determination resulting in 'shallow' ('3') for 'sub-littoral' ('1') conditions."""
        output = lab.depth_2_code('2', '1', 3., 0., 0)
        assert output == '3'

    def test_littoral_low(self):
        """Test the ecotope-code determination resulting in 'low littoral' ('1') for 'littoral' ('2') conditions."""
        output = lab.depth_2_code('2', '2', 0., 1., 0)
        assert output == '1'

    def test_littoral_middle(self):
        """Test the ecotope-code determination resulting in 'middle littoral' ('2') for 'littoral' ('2') conditions."""
        output = lab.depth_2_code('2', '2', 0., .5, 0)
        assert output == '2'

    def test_littoral_high(self):
        """Test the ecotope-code determination resulting in 'high littoral' ('3') for 'littoral' ('2') conditions."""
        output = lab.depth_2_code('2', '2', 0., 0., 0)
        assert output == '3'

    def test_supra_littoral_pioneer(self):
        """Test the ecotope-code determination resulting in 'potential pioneer zone' ('1') for 'supra-littoral' ('3')
        conditions.
        """
        output = lab.depth_2_code('2', '3', 0., 0., 350)
        assert output == '1'

    def test_supra_littoral_low(self):
        """Test the ecotope-code determination resulting in 'low salt marsh' ('2') for 'supra-littoral' ('3')
        conditions.
        """
        output = lab.depth_2_code('2', '3', 0., 0., 300)
        assert output == '2'

    def test_supra_littoral_middle(self):
        """Test the ecotope-code determination resulting in 'middle salt marsh' ('3') for 'supra-littoral' ('3')
        conditions.
        """
        output = lab.depth_2_code('2', '3', 0., 0., 100)
        assert output == '3'

    def test_supra_littoral_high(self):
        """Test the ecotope-code determination resulting in 'high salt marsh' ('4') for 'supra-littoral' ('3')
        conditions.
        """
        output = lab.depth_2_code('2', '3', 0., 0., 20)
        assert output == '4'


class TestSubstratum2Code:
    """Tests for `substratum_2_code()`."""

    def test_undefined(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.substratum_2_code('x', '', 0.)
        assert output == 'x'

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.substratum_2_code(None, '', 0.)
        assert output == 'x'

    def test_hydrodynamics_undefined(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.substratum_2_code('1', 'x', 0.)
        assert output == 'x'

    def test_hydrodynamics_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
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
