"""Property-based tests (Hypothesis) for the base confidence-interval methods.

Complements the oracle (statsmodels) and golden (paper) tests with invariants
that must hold for ALL valid inputs, not just the sampled grid.
"""

import pytest

pytest.importorskip("hypothesis")
from hypothesis import given, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

import binomcikit as b  # noqa: E402

# (function, lower-col, upper-col) — base, all-x methods, each symmetric in x.
BASE = [
    (b.ciwd, "LWD", "UWD"),
    (b.cisc, "LSC", "USC"),
    (b.cias, "LAS", "UAS"),
    (b.cilt, "LLT", "ULT"),
    (b.citw, "LTW", "UTW"),
    (b.cilr, "LLR", "ULR"),
]
ALP = 0.05
EPS = 1e-6


@given(n=st.integers(min_value=2, max_value=60))
@settings(max_examples=25, deadline=None)
def test_limits_bounded_and_ordered(n):
    for fn, lo, hi in BASE:
        df = fn(n, ALP)
        L = df[lo].to_numpy(dtype=float)
        U = df[hi].to_numpy(dtype=float)
        assert (L >= -EPS).all(), fn.__name__
        assert (U <= 1 + EPS).all(), fn.__name__
        assert (L <= U + EPS).all(), fn.__name__


@given(n=st.integers(min_value=2, max_value=60))
@settings(max_examples=25, deadline=None)
def test_palindrome_symmetry(n):
    # For methods symmetric in x, L(x) == 1 - U(n - x).
    for fn, lo, hi in BASE:
        df = fn(n, ALP)
        L = df[lo].to_numpy(dtype=float)
        U = df[hi].to_numpy(dtype=float)
        assert L == pytest.approx(1 - U[::-1], abs=1e-5), fn.__name__
