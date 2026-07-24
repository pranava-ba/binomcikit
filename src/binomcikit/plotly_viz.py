"""Interactive Plotly visualizations (optional — requires ``binomcikit[plots]``).

This is the forward plotting path — the migration target away from plotnine. Plotly
renders in notebooks, the Streamlit app, and (embedded via QtWebEngine) the desktop
GUI. Plotly is imported **lazily**, so the core package never depends on it; calling a
plot function without plotly installed raises a clear, actionable error.

Functions return a ``plotly.graph_objects.Figure`` — display with ``fig.show()``,
embed with ``st.plotly_chart(fig)``, or save with ``fig.write_html(...)``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from ._accel import coverage_series
from .ci import cias, ciba, ciblaker, ciex, cilr, cilt, cisc, citw, ciwd


def _exact(e):
    """Adapt the exact family (which takes a list of ``e`` values) to the
    ``fn(n, alpha)`` shape the plotting layer expects, at a fixed ``e``."""

    def _f(n, alpha):
        return ciex(n, alpha, [e])

    return _f


def _bayes(a, b):
    """Adapt the Bayesian credible interval (which takes prior ``a``, ``b``) to
    the ``fn(n, alpha)`` shape, at a fixed prior. Uses the equal-tailed quantile
    limits, which are directly comparable to the frequentist intervals."""

    def _f(n, alpha):
        return ciba(n, alpha, a, b)

    return _f


# method name -> (all-x limits function, lower col, upper col, display label)
_METHODS = {
    "wald": (ciwd, "LWD", "UWD", "Wald"),
    "wilson": (cisc, "LSC", "USC", "Wilson"),
    "score": (cisc, "LSC", "USC", "Wilson"),
    "arcsine": (cias, "LAS", "UAS", "ArcSine"),
    "logit": (cilt, "LLT", "ULT", "Logit"),
    "waldt": (citw, "LTW", "UTW", "Wald-T"),
    "lr": (cilr, "LLR", "ULR", "Likelihood-ratio"),
    "blaker": (ciblaker, "LBK", "UBK", "Blaker"),
    "exact": (_exact(1.0), "LEX", "UEX", "Clopper-Pearson"),
    "cp": (_exact(1.0), "LEX", "UEX", "Clopper-Pearson"),
    "clopper-pearson": (_exact(1.0), "LEX", "UEX", "Clopper-Pearson"),
    "midp": (_exact(0.5), "LEX", "UEX", "Mid-P"),
    "mid-p": (_exact(0.5), "LEX", "UEX", "Mid-P"),
    "bayes": (_bayes(1.0, 1.0), "LBAQ", "UBAQ", "Bayesian (flat)"),
    "bayesian": (_bayes(1.0, 1.0), "LBAQ", "UBAQ", "Bayesian (flat)"),
    "jeffreys": (_bayes(0.5, 0.5), "LBAQ", "UBAQ", "Jeffreys"),
}


def _go():
    try:
        import plotly.graph_objects as go
    except ImportError as exc:  # pragma: no cover - exercised only without plotly
        raise ImportError(
            "plotting requires plotly — install it with:  pip install binomcikit[plots]"
        ) from exc
    return go


def _limits(method, n, alpha):
    key = str(method).lower().strip()
    if key not in _METHODS:
        raise ValueError(
            f"plot method {method!r} not supported yet; choose from {sorted(set(_METHODS))}"
        )
    fn, lo, hi, label = _METHODS[key]
    df = fn(n, alpha)
    return df[lo].to_numpy(dtype=float), df[hi].to_numpy(dtype=float), label


def plot_ci(n: int, alpha: float = 0.05, method: str = "wald"):
    """Interval plot: the confidence interval for every ``x = 0..n``.

    Returns a ``plotly.graph_objects.Figure``. Each horizontal bar is the interval
    for that ``x``; the dot marks the point estimate p̂ = x/n.
    """
    go = _go()
    lower, upper, label = _limits(method, n, alpha)
    x = np.arange(n + 1)
    fig = go.Figure()
    for xi, lo, hi in zip(x, lower, upper):
        fig.add_trace(
            go.Scatter(
                x=[lo, hi],
                y=[xi, xi],
                mode="lines",
                line=dict(color="#3366cc", width=6),
                showlegend=False,
                hovertemplate=f"x={xi}<br>[%{{x:.3f}}]<extra></extra>",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=x / n,
            y=x,
            mode="markers",
            name="p̂ = x/n",
            marker=dict(color="black", size=7, symbol="diamond"),
        )
    )
    conf = int(round((1 - alpha) * 100))
    fig.update_layout(
        title=f"{label} {conf}% confidence interval (n={n})",
        xaxis_title="proportion θ",
        yaxis_title="successes x",
        xaxis=dict(range=[-0.02, 1.02]),
        template="simple_white",
    )
    return fig


def plot_coverage(
    n: int,
    alpha: float = 0.05,
    methods: Sequence[str] | str = ("wald", "wilson"),
    points: int = 500,
):
    """Coverage-probability curves vs the true proportion θ, for several methods.

    The dashed line is the nominal level 1 − α. A method whose curve dips below it
    is under-covering — this is the figure that exposes Wald's weakness. Returns a
    ``plotly.graph_objects.Figure``.
    """
    go = _go()
    if isinstance(methods, str):
        methods = (methods,)
    hp = np.linspace(1e-4, 1 - 1e-4, points)
    fig = go.Figure()
    for m in methods:
        lower, upper, label = _limits(m, n, alpha)
        cp = coverage_series(n, lower, upper, hp)
        fig.add_trace(go.Scatter(x=hp, y=cp, mode="lines", name=label))
    fig.add_hline(
        y=1 - alpha,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"nominal {1 - alpha:.2f}",
        annotation_position="bottom right",
    )
    fig.update_layout(
        title=f"Coverage probability vs θ (n={n})",
        xaxis_title="true proportion θ",
        yaxis_title="coverage probability",
        yaxis=dict(range=[max(0.0, 1 - 3 * alpha), 1.005]),
        template="simple_white",
    )
    return fig
