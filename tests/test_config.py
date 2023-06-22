"""
Tests for `config_file.py`.

Author: Gijs G. Hendrickx
"""
from config.config_file import load_config

"""TestClasses"""


class TestLoadConfig:
    """Tests for `load_config()`."""

    def setup_method(self):
        """Initialise with default configuration."""
        self.config = load_config()

    def test_keys(self):
        """Test if all required key-words are in the configuration file: depth 1."""
        keys = list(self.config.keys())
        for k in ('salinity', 'depth-1', 'hydrodynamics', 'depth-2', 'substratum-2'):
            assert k in keys

    def test_keys_salinity(self):
        """Test if all required key-words for the 'salinity'-key are in the configuration file: depth 2."""
        keys = list(self.config['salinity'].keys())
        for k in ('variable', 'fresh', 'marine'):
            assert k in keys

    def test_keys_depth_1(self):
        """Test if all required key-words for the 'depth 1'-key are in the configuration file: depth 2."""
        keys = list(self.config['depth-1'].keys())
        for k in ('low-water', 'high-water'):
            assert k in keys

    def test_keys_hydrodynamics(self):
        """Test if all required key-words for the 'hydrodynamics'-key are in the configuration file: depth 2."""
        keys = list(self.config['hydrodynamics'].keys())
        for k in ('stagnant', 'sub-littoral', 'littoral'):
            assert k in keys

    def test_keys_depth_2(self):
        """Test if all required key-words for the 'depth 2'-key are in the configuration file: depth 2."""
        keys = list(self.config['depth-2'].keys())
        for k in ('sub-littoral', 'littoral', 'supra-littoral'):
            assert k in keys

    def test_keys_substratum_2(self):
        """Test if all required key-words for the 'substratum 2'-key are in the configuration file: depth 2."""
        keys = list(self.config['substratum-2'].keys())
        for k in ('soft',):
            assert k in keys

    def test_keys_depth_2_sub_littoral(self):
        """Test if all required key-words for the 'sub-littoral'-key in the 'depth 2'-key are in the configuration file:
        depth 3."""
        keys = list(self.config['depth-2']['sub-littoral'].keys())
        for k in ('depth-upper', 'depth-lower', 'low-water'):
            assert k in keys

    def test_keys_depth_2_littoral(self):
        """Test if all required key-words for the 'littoral'-key in the 'depth 2'-key are in the configuration file:
        depth 3."""
        keys = list(self.config['depth-2']['littoral'].keys())
        for k in ('inundation-upper', 'inundation-lower'):
            assert k in keys

    def test_keys_depth_2_supra_littoral(self):
        """Test if all required key-words for the 'supra-littoral'-key in the 'depth 2'-key are in the configuration
        file: depth 3."""
        keys = list(self.config['depth-2']['supra-littoral'].keys())
        for k in ('frequency-1', 'frequency-2', 'frequency-3'):
            assert k in keys
