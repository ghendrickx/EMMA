"""
Tests for `src/performance.py`.

Author: Gijs G. Hendrickx
"""
import pytest

from src import performance as pf

"""pytest.fixtures"""


@pytest.fixture
def xy_labels_1():
    """Ecotope-data with three types of ecotopes without the use of wild cards (i.e., 'x')."""
    return {
        (0, 0): 'Z2.222f',
        (0, 1): 'Z2.222f',
        (1, 0): 'Z2.222s',
        (1, 1): 'Z2.221s',
    }


@pytest.fixture
def xy_labels_2():
    """Ecotope-data with two types of ecotopes without the use of wild cards (i.e., 'x')."""
    return {
        (0, 0): 'Z2.222f',
        (0, 1): 'Z2.222f',
        (1, 0): 'Z2.221s',
        (1, 1): 'Z2.221s',
    }


@pytest.fixture
def xy_labels_3():
    """Ecotope-data with three types of ecotopes with the use of wild cards (i.e., 'x')."""
    return {
        (0, 0): 'Z2.222f',
        (0, 1): 'Z2.222f',
        (1, 0): 'Z2.22xs',
        (1, 1): 'Z2.221s',
    }


"""helper functions"""


def comparison_exec(*data, level=None):
    comp = pf.Comparison(*data)
    return comp.exec(level)


def n_correct(perf):
    return sum(perf.values())


def n_incorrect(perf):
    return len(perf) - n_correct(perf)


def tuple_correct(perf):
    return n_correct(perf), n_incorrect(perf)


"""TestClasses"""


class TestPerformance:
    """Tests for `Comparison`."""

    """perfect matches"""

    def test_full_perfect_match_1(self, xy_labels_1):
        out = comparison_exec(xy_labels_1, xy_labels_1)
        assert tuple_correct(out) == (4, 0)

    def test_full_perfect_match_2(self, xy_labels_2):
        out = comparison_exec(xy_labels_2, xy_labels_2)
        assert tuple_correct(out) == (4, 0)

    def test_full_perfect_match_3(self, xy_labels_3):
        out = comparison_exec(xy_labels_3, xy_labels_3)
        assert tuple_correct(out) == (4, 0)

    """imperfect matches"""

    def test_full_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2)
        assert tuple_correct(out) == (3, 1)

    def test_full_match_1_3(self, xy_labels_1, xy_labels_3):
        out = comparison_exec(xy_labels_1, xy_labels_3)
        assert tuple_correct(out) == (3, 1)

    def test_full_match_2_3(self, xy_labels_2, xy_labels_3):
        out = comparison_exec(xy_labels_2, xy_labels_3)
        assert tuple_correct(out) == (3, 1)

    """wild card usage"""

    def test_full_match_w_wild_card_1(self, xy_labels_3, xy_labels_1):
        out = comparison_exec(xy_labels_3, xy_labels_1)
        assert tuple_correct(out) == (4, 0)

    def test_full_match_w_wild_card_2(self, xy_labels_3, xy_labels_2):
        out = comparison_exec(xy_labels_3, xy_labels_2)
        assert tuple_correct(out) == (4, 0)

    def test_full_match_wo_wild_card_1(self, xy_labels_3, xy_labels_1):
        comp = pf.Comparison(xy_labels_3, xy_labels_1)
        out = comp.exec(None, enable_wild_card=False)
        assert tuple_correct(out) == (3, 1)

    def test_full_match_wo_wild_card_2(self, xy_labels_3, xy_labels_2):
        comp = pf.Comparison(xy_labels_3, xy_labels_2)
        out = comp.exec(None, enable_wild_card=False)
        assert tuple_correct(out) == (3, 1)

    def test_full_match_w_diff_wild_card_1(self, xy_labels_3, xy_labels_1):
        comp = pf.Comparison(xy_labels_3, xy_labels_1, wild_card='o')
        out = comp.exec(None, enable_wild_card=True)
        assert tuple_correct(out) == (3, 1)

    def test_full_match_w_diff_wild_card_2(self, xy_labels_3, xy_labels_2):
        comp = pf.Comparison(xy_labels_3, xy_labels_2, wild_card='o')
        out = comp.exec(None, enable_wild_card=True)
        assert tuple_correct(out) == (3, 1)

    """performance with max. level"""

    def test_level_6_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2, level=6)
        assert tuple_correct(out) == (3, 1)

    def test_level_5_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2, level=5)
        assert tuple_correct(out) == (3, 1)

    def test_level_4_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2, level=4)
        assert tuple_correct(out) == (4, 0)

    def test_level_3_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2, level=3)
        assert tuple_correct(out) == (4, 0)

    def test_level_2_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2, level=2)
        assert tuple_correct(out) == (4, 0)

    def test_level_1_match_1_2(self, xy_labels_1, xy_labels_2):
        out = comparison_exec(xy_labels_1, xy_labels_2, level=1)
        assert tuple_correct(out) == (4, 0)

    """performance specific label"""

    def test_label_6_match_1_2(self, xy_labels_1, xy_labels_2):
        comp = pf.Comparison(xy_labels_1, xy_labels_2)
        out = comp.exec(5, specific_label=True)
        assert tuple_correct(out) == (4, 0)

    def test_label_5_match_1_2(self, xy_labels_1, xy_labels_2):
        comp = pf.Comparison(xy_labels_1, xy_labels_2)
        out = comp.exec(4, specific_label=True)
        assert tuple_correct(out) == (3, 1)

    def test_label_4_match_1_2(self, xy_labels_1, xy_labels_2):
        comp = pf.Comparison(xy_labels_1, xy_labels_2)
        out = comp.exec(3, specific_label=True)
        assert tuple_correct(out) == (4, 0)

    def test_label_3_match_1_2(self, xy_labels_1, xy_labels_2):
        comp = pf.Comparison(xy_labels_1, xy_labels_2)
        out = comp.exec(2, specific_label=True)
        assert tuple_correct(out) == (4, 0)

    def test_label_2_match_1_2(self, xy_labels_1, xy_labels_2):
        comp = pf.Comparison(xy_labels_1, xy_labels_2)
        out = comp.exec(1, specific_label=True)
        assert tuple_correct(out) == (4, 0)

    def test_label_1_match_1_2(self, xy_labels_1, xy_labels_2):
        comp = pf.Comparison(xy_labels_1, xy_labels_2)
        out = comp.exec(0, specific_label=True)
        assert tuple_correct(out) == (4, 0)

    """error-testing"""

    def test_error_negative_level(self, xy_labels_1):
        comp = pf.Comparison(xy_labels_1, xy_labels_1)
        with pytest.raises(ValueError):
            comp.exec(-1)
        comp.exec(10)

    def test_error_invalid_index(self, xy_labels_1):
        comp = pf.Comparison(xy_labels_1, xy_labels_1)
        with pytest.raises(ValueError):
            comp.exec(6, specific_label=True)
        comp.exec(6)
