"""Golden values taken directly from the source paper (Subbiah & Rajeswaran,
SoftwareX 6, 2017), Table 2 — an oracle independent of statsmodels and R.
"""

import pytest
from cases import ALPHA, WALD_N5, N

import binomcikit as b


def test_wald_n5_matches_paper_table2():
    df = b.ciwd(N, ALPHA)
    for x, (lo, hi) in WALD_N5.items():
        assert df.LWD[x] == pytest.approx(lo, abs=5e-4)
        assert df.UWD[x] == pytest.approx(hi, abs=5e-4)


def test_wald_n5_zwi_only_at_boundaries():
    df = b.ciwd(N, ALPHA)
    zwi = {x for x in range(N + 1) if df.LWD[x] == df.UWD[x]}
    assert zwi == {0, N}
