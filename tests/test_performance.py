"""
Tests for `src/performance.py`, `Comparison`-object.

Author: Gijs G. Hendrickx
"""
import pytest

from src import performance as pf

# global variables
__XY_LABELS_1 = {
    (0, 0): 'Z2.222f',
    (0, 1): 'Z2.222f',
    (1, 0): 'Z2.222s',
    (1, 1): 'Z2.221s',
}
__XY_LABELS_2 = {
    (0, 0): 'Z2.222f',
    (0, 1): 'Z2.222f',
    (1, 0): 'Z2.221s',
    (1, 1): 'Z2.221s',
}
__XY_LABELS_3 = {
    (0, 0): 'Z2.222f',
    (0, 1): 'Z2.222f',
    (1, 0): 'Z2.22xs',
    (1, 1): 'Z2.221s',
}

# helper functions


def comparison_exec(*data, wild_card=True, level=None, label=False):
    comp = pf.Comparison(*data)
    return comp.exec(level, enable_wild_card=wild_card, specific_label=label)


def n_correct(perf):
    return sum(perf.values())


def n_incorrect(perf):
    return len(perf) - n_correct(perf)


def tuple_correct(perf):
    return n_correct(perf), n_incorrect(perf)


# tests


@pytest.mark.parametrize(
    'out1, out2, correct',
    [
        (__XY_LABELS_1, __XY_LABELS_1, (4, 0)),
        (__XY_LABELS_2, __XY_LABELS_2, (4, 0)),
        (__XY_LABELS_3, __XY_LABELS_3, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, (3, 1)),
        (__XY_LABELS_1, __XY_LABELS_3, (3, 1)),
        (__XY_LABELS_2, __XY_LABELS_3, (3, 1)),
    ]
)
def test_matches(out1, out2, correct):
    out = comparison_exec(out1, out2)
    assert tuple_correct(out) == correct


@pytest.mark.parametrize(
    'out1, out2, wild_card, correct',
    [
        (__XY_LABELS_3, __XY_LABELS_1, True, (4, 0)),
        (__XY_LABELS_3, __XY_LABELS_2, True, (4, 0)),
        (__XY_LABELS_3, __XY_LABELS_1, False, (3, 1)),
        (__XY_LABELS_3, __XY_LABELS_2, False, (3, 1)),
    ]
)
def test_wild_card(out1, out2, wild_card, correct):
    out = comparison_exec(out1, out2, wild_card=wild_card)
    assert tuple_correct(out) == correct


@pytest.mark.parametrize(
    'out1, out2, level, correct',
    [
        (__XY_LABELS_1, __XY_LABELS_2, 6, (3, 1)),
        (__XY_LABELS_1, __XY_LABELS_2, 5, (3, 1)),
        (__XY_LABELS_1, __XY_LABELS_2, 4, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 3, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 2, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 1, (4, 0)),
    ]
)
def test_max_level(out1, out2, level, correct):
    out = comparison_exec(out1, out2, level=level)
    assert tuple_correct(out) == correct


@pytest.mark.parametrize(
    'out1, out2, level, correct',
    [
        (__XY_LABELS_1, __XY_LABELS_2, 0, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 1, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 2, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 3, (4, 0)),
        (__XY_LABELS_1, __XY_LABELS_2, 4, (3, 1)),
        (__XY_LABELS_1, __XY_LABELS_2, 5, (4, 0)),
    ]
)
def test_specific_label(out1, out2, level, correct):
    out = comparison_exec(out1, out2, level=level, label=True)
    assert tuple_correct(out) == correct


@pytest.mark.parametrize(
    'out1, out2, level, label, error',
    [
        (__XY_LABELS_1, __XY_LABELS_1, -1, False, ValueError),
        (__XY_LABELS_1, __XY_LABELS_2, 6, True, ValueError),
    ]
)
def test_errors(out1, out2, level, label, error):
    with pytest.raises(error):
        comparison_exec(out1, out2, level=level, label=label)
