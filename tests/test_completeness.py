"""Completeness guard: every function exported by the R package must exist in
the Python package (matched case-insensitively), and a representative sample of
the newly added plot functions must construct without error.
"""
import os

import pytest

import binomcikit as b

HERE = os.path.dirname(__file__)
# Vendored list of every function exported by the R package's NAMESPACE, so the
# completeness check is self-contained (works in CI without the R source). It is
# regenerated from reference/rpackage/NAMESPACE by the docs tooling.
R_EXPORTS = os.path.join(HERE, "r_exports.txt")


def _r_exports():
    with open(R_EXPORTS) as fh:
        return {line.strip() for line in fh if line.strip()}


def test_all_r_exports_present():
    exports = _r_exports()
    pynames = {n.lower() for n in dir(b) if not n.startswith("_")}
    missing = sorted(e for e in exports if e.lower() not in pynames)
    assert missing == [], f"Missing {len(missing)} R exports: {missing}"
    assert len(exports) == 305


NEW_PLOTS = [
    lambda: b.plotciall(5, 0.05),
    lambda: b.plotciallg(5, 0.05),
    lambda: b.plotciaall(5, 0.05, 2),
    lambda: b.plotciaallx(2, 5, 0.05, 2),
    lambda: b.plotcicall(5, 0.05, 0.02),
    lambda: b.plotcicallxg(2, 5, 0.05, 0.02),
    lambda: b.plotciba(5, 0.05, 1, 1),
    lambda: b.plotexplawd(5, 0.05, 2, 1, 1, seed=0),
    lambda: b.plotexplcwd(5, 0.05, 0.02, 1, 1, seed=0),
    lambda: b.plotexplba(5, 0.05, 1, 1, 0.5, 0.5, seed=0),
    lambda: b.plotlengthalr(5, 0.05, 2, 1, 1, seed=0),
    lambda: b.plotlengthex(5, 0.05, 0.5, 1, 1, seed=0),
    lambda: b.plotlengthba(5, 0.05, 1, 1, 0.5, 0.5, seed=0),
    lambda: b.plotpcopbiba(5, 0.05, 0.5, 0.5),
    lambda: b.ploterrba(10, 0.05, 0.5, -2, 1, 1),
]


@pytest.mark.parametrize("make", NEW_PLOTS)
def test_new_plots_construct(make):
    from plotnine import ggplot
    assert isinstance(make(), ggplot)


def test_emperical_aliases_match():
    # R spells it "emperical"; both spellings must give identical results.
    import numpy as np
    a = b.empiricalba(5, 0.05, 0.1, 10)
    c = b.empericalba(5, 0.05, 0.1, 10)
    assert np.allclose(a.to_numpy(), c.to_numpy())
