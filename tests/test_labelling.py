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

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.salinity_code(None, 0, 30)
        assert output == 'x'

    def test_variable(self):
        """Test the ecotope-code determination resulting in 'variable' ('V')."""
        output = lab.salinity_code(10, 0, 30)
        assert output == 'V'

    def test_fresh(self):
        """Test the ecotope-code determination resulting in 'freshwater' ('F')."""
        output = lab.salinity_code(2.5, 2, 3)
        assert output == 'F'

    def test_marine(self):
        """Test the ecotope-code determination resulting in 'marine' ('Z')."""
        output = lab.salinity_code(28, 27, 30)
        assert output == 'Z'

    def test_brackish(self):
        """Test the ecoptope-code determination resulting in 'brackish' ('B')."""
        output = lab.salinity_code(15, 8, 20)
        assert output == 'B'


class TestSubstratum1Code:

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

    def test_unknown(self):
        """Test the ecotope-code determination when insufficient data is available."""
        output = lab.depth_1_code(None)
        assert output == 'x'

    def test_sub_littoral(self):
        """Test the ecotope-code determination resulting in 'sub-littoral' ('1')."""
        output = lab.depth_1_code(1.)
        assert output == '1'

    def test_littoral(self):
        """Test the ecotope-code determination resulting in 'littoral' ('2')."""
        output = lab.depth_1_code(.4)
        assert output == '2'

    def test_supra_littoral(self):
        """Test the ecotope-code determination resulting in 'supra-littoral' ('3')."""
        output = lab.depth_1_code(0.)
        assert output == '3'


class TestHydrodynamicsCode:

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

    def test_undefined(self):
        output = lab.depth_2_code('1', '', 0., 0., 0)
        assert output == ''

    def test_unknown(self):
        output = lab.depth_2_code('', None, 0., 0., 0)
        assert output == 'x'

    def test_unknown_x(self):
        output = lab.depth_2_code('', 'x', 0., 0., 0)
        assert output == 'x'

    def test_sub_littoral_deep(self):
        output = lab.depth_2_code('2', '1', 11., 0., 0)
        assert output == '1'

    def test_sub_littoral_intermediate(self):
        output = lab.depth_2_code('2', '1', 8., 0., 0)
        assert output == '2'

    def test_sub_littoral_shallow(self):
        output = lab.depth_2_code('2', '1', 3., 0., 0)
        assert output == '3'

    def test_littoral_low(self):
        output = lab.depth_2_code('2', '2', 0., 1., 0)
        assert output == '1'

    def test_littoral_middle(self):
        output = lab.depth_2_code('2', '2', 0., .5, 0)
        assert output == '2'

    def test_littoral_high(self):
        output = lab.depth_2_code('2', '2', 0., 0., 0)
        assert output == '3'

    def test_supra_littoral_pioneer(self):
        output = lab.depth_2_code('2', '3', 0., 0., 350)
        assert output == '1'

    def test_supra_littoral_low(self):
        output = lab.depth_2_code('2', '3', 0., 0., 300)
        assert output == '2'

    def test_supra_littoral_middle(self):
        output = lab.depth_2_code('2', '3', 0., 0., 100)
        assert output == '3'

    def test_supra_littoral_high(self):
        output = lab.depth_2_code('2', '3', 0., 0., 20)
        assert output == '4'


class TestSubstratum2Code:

    def test_undefined(self):
        output = lab.substratum_2_code('x', '', 0.)
        assert output == 'x'

    def test_unknown(self):
        output = lab.substratum_2_code(None, '', 0.)
        assert output == 'x'

    def test_hydrodynamics_undefined(self):
        output = lab.substratum_2_code('1', 'x', 0.)
        assert output == 'x'

    def test_hydrodynamics_unknown(self):
        output = lab.substratum_2_code('1', None, 0.)
        assert output == 'x'

    def test_hard_low_energy(self):
        output = lab.substratum_2_code('1', '2', 0.)
        assert output == '1'

    def test_hard_high_energy(self):
        output = lab.substratum_2_code('1', '1', 0.)
        assert output == '2'

    def test_grains_unknown(self):
        output = lab.substratum_2_code('2', '', None)
        assert output == 'x'

    def test_soft_silt(self):
        output = lab.substratum_2_code('2', '', 20)
        assert output == 's'

    def test_soft_fines(self):
        output = lab.substratum_2_code('2', '', 100)
        assert output == 'f'

    def test_soft_sand(self):
        output = lab.substratum_2_code('2', '', 2000)
        assert output == 'z'

    def test_soft_gravel(self):
        output = lab.substratum_2_code('2', '', 3000)
        assert output == 'g'
