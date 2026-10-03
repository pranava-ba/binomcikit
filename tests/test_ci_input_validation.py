"""Every ``ci*`` function rejects bad arguments with a clear error instead of returning nonsense.

Each function repeats the same input contract (n, alpha, x, and the h / c / e / a / b extras), and
almost no other test exercises the rejection branches. The bad values below are applied one at a time
to a good call, so a function that silently accepts one of them fails here.
"""

import inspect

import pytest

import binomcikit as bk
from binomcikit import _ci_pkg

NAMES = sorted(n for n in _ci_pkg.__all__ if n.startswith("ci") and not n.startswith("plot"))
GOOD = {
    "x": 2,
    "n": 8,
    "alp": 0.05,
    "h": 2,
    "c": 0.05,
    "e": [0.5],
    "a": 1,
    "b": 1,
    "B": 50,
    "seed": 1,
}
# (parameter, bad value): each should be rejected
BAD = [
    ("n", None),
    ("n", 0),
    ("n", -3),
    ("alp", None),
    ("alp", -0.1),
    ("alp", 1.5),
    ("x", -1),
    ("x", 99),
    ("h", None),
    ("h", -1),
    ("c", None),
    ("c", -0.2),
    ("e", [1.5]),
    ("e", [-0.2]),
    ("a", None),
    ("a", -1),
    ("b", -1),
]


def _kwargs(fn):
    params = inspect.signature(fn).parameters
    return {k: GOOD[k] for k in params if k in GOOD}


@pytest.mark.parametrize("name", NAMES)
def test_good_call_works(name):
    fn = getattr(bk, name)
    assert fn(**_kwargs(fn)) is not None


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("param,bad", BAD)
def test_bad_argument_is_rejected(name, param, bad):
    fn = getattr(bk, name)
    kwargs = _kwargs(fn)
    if param not in kwargs:
        pytest.skip(f"{name} has no parameter {param!r}")
    kwargs[param] = bad
    with pytest.raises((ValueError, TypeError)):
        fn(**kwargs)


# The R reference only enforces ``c <= 1/(2n)`` in ciCSC and ciCAll (the other continuity-corrected functions
# check only ``c >= 0``); binomcikit mirrors that, so the upper bound is tested for exactly those.
@pytest.mark.parametrize("name", ["cicsc", "cicscx", "cicall", "cicallx"])
def test_score_family_enforces_the_continuity_upper_bound(name):
    fn = getattr(bk, name)
    kwargs = _kwargs(fn)
    kwargs["c"] = 5.0
    with pytest.raises(ValueError, match="1/"):
        fn(**kwargs)


@pytest.mark.parametrize("name", NAMES)
def test_whole_number_float_n_behaves_like_an_int(name):
    """``n = 8.0`` (what pandas and numpy often hand over) works like ``n = 8``, or is rejected with a ValueError."""
    fn = getattr(bk, name)
    base = _kwargs(fn)
    as_float = dict(base, n=8.0)
    try:
        got = fn(**as_float)
    except ValueError:
        return  # documented rejection (e.g. the exact family insists on an integer)
    want = fn(**base)
    assert got.equals(want)


@pytest.mark.parametrize(
    "name", [n for n in NAMES if "n" in inspect.signature(getattr(bk, n)).parameters]
)
def test_fractional_n_is_rejected(name):
    fn = getattr(bk, name)
    kwargs = _kwargs(fn)
    kwargs["n"] = 8.5
    with pytest.raises(ValueError):
        fn(**kwargs)
