"""Plotting functions load lazily: ``import binomcikit`` must not import plotnine."""

import subprocess
import sys


def _run(code):
    return subprocess.run(
        [sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True
    )


def test_import_does_not_load_plotnine():
    r = _run("import sys, binomcikit; print('plotnine' in sys.modules)")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "False"


def test_plot_names_resolve_on_first_access():
    r = _run(
        "import sys, binomcikit as bk; f = bk.plotciwd; print(callable(f), 'plotnine' in sys.modules)\n"
        "print(callable(bk.covp.plotcovpwd), 'plotciwd' in bk.__all__)"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == ["True", "True", "True", "True"]


def test_without_plotnine_core_works_and_plot_names_are_absent():
    r = _run(
        "import sys; sys.modules['plotnine'] = None\n"
        "import binomcikit as bk\n"
        "print(bk.ci(n=10, alpha=0.05, method='wilson').shape)\n"
        "print(hasattr(bk, 'plotciwd'), 'plotciwd' in bk.__all__)"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.split("\n")[0] == "(11, 6)"
    assert r.stdout.split("\n")[1] == "False False"
