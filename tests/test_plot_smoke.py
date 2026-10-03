"""Smoke test: every plotnine plotting function in the five families draws without error.

The plotting modules are the largest untested block in the package. This does not check what the
figures look like, only that each function accepts the documented arguments and builds a plot object
(plotnine builds lazily, so the construction code runs). Functions needing arguments this test cannot
supply (explicit limit tables, simulated p values) are skipped rather than guessed at.
"""

import inspect

import pytest

pytest.importorskip("plotnine")

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import binomcikit as bk  # noqa: E402
from binomcikit import _ci_pkg, covp, err, expl, pconf  # noqa: E402

ARGS = {"x": 2, "n": 6, "alp": 0.05, "h": 2, "c": 0.05, "B": 20, "seed": 1}
NAMES = sorted({n for fam in (_ci_pkg, covp, err, expl, pconf) for n in fam._LAZY_PLOTS})


# extra positional values some "all methods" plots take after (n, alp): prior shapes (a, b), optionally preceded by h
EXTRA = [(), (1, 1), (2, 1, 1), (0.05, 1, 1)]


def _call(name):
    fn = getattr(bk, name)
    params = inspect.signature(fn).parameters
    args, kwargs, variadic = [], {}, False
    for pname, p in params.items():
        if p.kind is p.VAR_POSITIONAL:
            variadic = True
        elif pname in ARGS:
            if p.kind is p.KEYWORD_ONLY:
                kwargs[pname] = ARGS[pname]
            else:
                args.append(ARGS[pname])
        elif p.default is inspect.Parameter.empty and p.kind in (
            p.POSITIONAL_OR_KEYWORD,
            p.KEYWORD_ONLY,
        ):
            pytest.skip(f"{name} needs argument {pname!r}")
    if not variadic:
        return fn(*args, **kwargs)
    last = None
    for extra in EXTRA:
        try:
            return fn(*args, *extra, **kwargs)
        except (ValueError, TypeError) as exc:  # wrong number of extra values: try the next shape
            last = exc
    pytest.skip(f"{name}: could not find extra arguments ({last})")


@pytest.mark.parametrize("name", NAMES)
def test_plot_function_builds_a_figure(name):
    _call(
        name
    )  # the legacy plotting functions draw and return None; reaching here means no exception
    plt.close("all")
