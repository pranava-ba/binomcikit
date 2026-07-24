"""The Plotly plotting layer builds valid figures. Plotly is optional, so skip if absent."""

import pytest

pytest.importorskip("plotly")

import binomcikit as bk  # noqa: E402


def test_plot_ci_builds_figure():
    import plotly.graph_objects as go

    fig = bk.plot_ci(n=20, alpha=0.05, method="wald")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 22  # 21 interval segments + 1 point-estimate trace


def test_plot_coverage_builds_figure():
    import plotly.graph_objects as go

    fig = bk.plot_coverage(n=20, alpha=0.05, methods=("wald", "wilson", "arcsine"))
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 3  # one coverage curve per method


def test_plot_unknown_method_errors():
    with pytest.raises(ValueError):
        bk.plot_ci(n=10, method="nope")


@pytest.mark.parametrize("method", ["exact", "cp", "midp", "lr", "logit", "waldt"])
def test_plot_coverage_supports_all_ported_methods(method):
    import plotly.graph_objects as go

    fig = bk.plot_coverage(n=15, alpha=0.05, methods=(method, "wilson"))
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2
