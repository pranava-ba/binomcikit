"""The optional numba fast-path must agree with the numpy fallback to full
precision, so results never depend on whether ``binomcikit[fast]`` is installed."""

import numpy as np
import pytest

pytest.importorskip("numba")

from binomcikit import _accel  # noqa: E402


def _wilsonish_limits(n):
    x = np.arange(n + 1)
    p = x / n
    half = 1.96 * np.sqrt(np.maximum(p * (1 - p), 1e-9) / n) + 0.5 / n
    return np.clip(p - half, 0, 1), np.clip(p + half, 0, 1)


def test_numba_kernel_matches_numpy():
    assert _accel.HAS_NUMBA
    rng = np.random.default_rng(0)
    for n in (50, 300):
        lower, upper = _wilsonish_limits(n)
        hp = np.sort(rng.beta(1, 1, 4000))
        got = _accel._coverage_numba(
            n, np.ascontiguousarray(lower), np.ascontiguousarray(upper), hp
        )
        want = _accel._coverage_numpy(n, lower, upper, hp)
        assert np.allclose(got, want, atol=1e-9, rtol=0), f"n={n}"


def test_dispatch_picks_numba_and_matches():
    # 6000 * 401 = 2.4M cells >= threshold -> numba path is chosen
    rng = np.random.default_rng(1)
    n = 400
    lower, upper = _wilsonish_limits(n)
    hp = np.sort(rng.beta(1, 1, 6000))
    got = _accel.coverage_series(n, lower, upper, hp)
    want = _accel._coverage_numpy(n, lower, upper, hp)
    assert np.allclose(got, want, atol=1e-9, rtol=0)
