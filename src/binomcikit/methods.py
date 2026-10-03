"""Registry of the extended confidence-interval methods.

One ``MethodSpec`` per method is the single source of truth for: the user-facing name and
aliases, the limits-table columns, the coverage guarantee, whether the method is randomised
or sequence-based, and how expensive it is. :func:`binomcikit.ci`, the plotting layer and the
access layer (``compare`` / ``recommend`` / ``coverage_curve`` ...) all read this registry, so
adding a method here makes it available everywhere -- and hence under the whole metric engine
(coverage, expected length, p-confidence/p-bias, error) -- with no per-method wiring.

Use :func:`describe` / :func:`list_methods` to browse it programmatically.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass, field

import pandas as pd

from .ext import adjusted, betting, bounds, closed_form, exact, likelihood, pires


@dataclass(frozen=True)
class MethodSpec:
    """Metadata + callables for one extended method."""

    key: str
    label: str
    family: str
    lo: str
    hi: str
    fn: Callable[..., pd.DataFrame]
    fnx: Callable[..., pd.DataFrame]
    guarantee: str  # "exact" | "anytime" | "exact-randomized" | "local" | "approximate"
    ref: str
    aliases: tuple[str, ...] = ()
    defaults: dict = field(default_factory=dict)
    cost: str = (
        "closed-form"  # "closed-form" | "vectorised-root" | "per-row-root" | "global" | "simulation"
    )
    deterministic: bool = True  # False => depends on an RNG (even if seeded)
    max_n: int | None = None  # practical upper limit for table-building planners

    def table(self, n: int, alpha: float, **params) -> pd.DataFrame:
        """The full ``(n+1)``-row limits table, with ``params`` overriding the defaults."""
        return self.fn(n, alpha, **self._kwargs(params))

    def row(self, x: int, n: int, alpha: float, **params) -> pd.DataFrame:
        """A single-``x`` row."""
        return self.fnx(x, n, alpha, **self._kwargs(params))

    def accepts(self) -> set[str]:
        """Names of the optional keyword parameters the method takes."""
        sig = inspect.signature(self.fn)
        return {p for p in list(sig.parameters)[2:]}

    def _kwargs(self, params: dict) -> dict:
        bad = set(params) - self.accepts()
        if bad:
            raise ValueError(
                f"method {self.key!r} does not take {sorted(bad)}; it accepts {sorted(self.accepts())}"
            )
        return {**self.defaults, **params}


_SPECS = [
    MethodSpec(
        "pratt",
        "Pratt",
        "closed-form approximation of exact",
        "LPRA",
        "UPRA",
        closed_form.ciprat,
        closed_form.cipratx,
        "approximate",
        "Pratt 1968, JASA 63",
    ),
    MethodSpec(
        "cloglog",
        "Complementary log-log",
        "transformed Wald",
        "LCLL",
        "UCLL",
        closed_form.cicloglog,
        closed_form.cicloglogx,
        "approximate",
        "R `binom` (cloglog link)",
        aliases=("c-log-log",),
    ),
    MethodSpec(
        "arcsine-shifted",
        "Arcsine, 3/8-shifted centre",
        "transformed Wald",
        "LASH",
        "UASH",
        closed_form.ciarcsineshift,
        closed_form.ciarcsineshiftx,
        "approximate",
        "Anscombe 1948 shift; DescTools `BinomCI` / DBCI `arcsine`",
        aliases=("arcsine-3/8", "arcsine-dbci"),
    ),
    MethodSpec(
        "probit",
        "Probit",
        "transformed Wald",
        "LPRB",
        "UPRB",
        closed_form.ciprobit,
        closed_form.ciprobitx,
        "approximate",
        "R `binom` (probit link)",
    ),
    MethodSpec(
        "modified-wilson",
        "Modified Wilson",
        "score (boundary-repaired)",
        "LMWS",
        "UMWS",
        closed_form.cimodwilson,
        closed_form.cimodwilsonx,
        "approximate",
        "Brown, Cai & DasGupta 2001",
        aliases=("mod-wilson", "modwilson"),
    ),
    MethodSpec(
        "modified-jeffreys",
        "Modified Jeffreys",
        "Bayesian (boundary-repaired)",
        "LMJF",
        "UMJF",
        closed_form.cimodjeffreys,
        closed_form.cimodjeffreysx,
        "approximate",
        "Brown, Cai & DasGupta 2001",
        aliases=("mod-jeffreys", "modjeffreys"),
    ),
    MethodSpec(
        "poisson",
        "Garwood (Poisson)",
        "rare-event approximation",
        "LPOI",
        "UPOI",
        closed_form.cipoisson,
        closed_form.cipoissonx,
        "approximate",
        "Garwood 1936, Biometrika 28",
        aliases=("garwood",),
    ),
    MethodSpec(
        "freeman-tukey",
        "Freeman-Tukey",
        "variance-stabilised",
        "LFTK",
        "UFTK",
        closed_form.cifreemantukey,
        closed_form.cifreemantukeyx,
        "approximate",
        "Freeman & Tukey 1950; Miller 1978",
        aliases=("ft", "double-arcsine"),
        cost="vectorised-root",
    ),
    MethodSpec(
        "soc",
        "Second-order corrected",
        "Edgeworth-corrected score",
        "LSOC",
        "USOC",
        closed_form.cisoc,
        closed_form.cisocx,
        "approximate",
        "Cai 2005, JSPI 131 (via binGroup)",
        aliases=("second-order-corrected",),
    ),
    MethodSpec(
        "hoeffding",
        "Hoeffding",
        "concentration bound",
        "LHOE",
        "UHOE",
        bounds.cihoeffding,
        bounds.cihoeffdingx,
        "exact",
        "Hoeffding 1963, JASA 58",
    ),
    MethodSpec(
        "chernoff",
        "Chernoff-KL",
        "concentration bound",
        "LKLC",
        "UKLC",
        bounds.cikl,
        bounds.ciklx,
        "exact",
        "Chernoff 1952; Garivier & Cappe 2011",
        aliases=("kl", "chernoff-kl", "kl-ucb"),
        cost="vectorised-root",
    ),
    MethodSpec(
        "bernstein",
        "Bernstein",
        "concentration bound",
        "LBRN",
        "UBRN",
        bounds.cibernstein,
        bounds.cibernsteinx,
        "exact",
        "Bernstein 1924; Boucheron et al. 2013",
    ),
    MethodSpec(
        "empirical-bernstein",
        "Empirical Bernstein",
        "concentration bound",
        "LEBN",
        "UEBN",
        bounds.ciempbern,
        bounds.ciempbernx,
        "exact",
        "Maurer & Pontil 2009, COLT Thm 4",
        aliases=("emp-bern", "maurer-pontil"),
    ),
    MethodSpec(
        "cressie-read",
        "Cressie-Read (lam=2/3)",
        "power divergence",
        "LCRD",
        "UCRD",
        likelihood.cicressieread,
        likelihood.cicressiereadx,
        "approximate",
        "Cressie & Read 1984, JRSS-B 46",
        aliases=("cr", "power-divergence"),
        defaults={"lam": 2.0 / 3.0},
        cost="vectorised-root",
    ),
    MethodSpec(
        "lr-star",
        "Higher-order LR (r*)",
        "higher-order likelihood",
        "LLRS",
        "ULRS",
        likelihood.cilrstar,
        likelihood.cilrstarx,
        "approximate",
        "Barndorff-Nielsen 1986; Brazzale, Davison & Reid 2007",
        aliases=("rstar", "r-star"),
        cost="vectorised-root",
    ),
    MethodSpec(
        "sterne",
        "Sterne",
        "exact (probability-ordered)",
        "LSTE",
        "USTE",
        exact.cisterne,
        exact.cisternex,
        "exact",
        "Sterne 1954; Duembgen 2021 (arXiv:2111.12937)",
        aliases=("minlike",),
        cost="per-row-root",
        max_n=20000,
    ),
    MethodSpec(
        "bsc",
        "Blyth-Still-Casella",
        "exact (shortest)",
        "LBSC",
        "UBSC",
        exact.cibsc,
        exact.cibscx,
        "exact",
        "Casella 1986; Blyth & Still 1983",
        aliases=("blyth-still-casella", "casella"),
        cost="global",
        max_n=2000,
    ),
    MethodSpec(
        "olc",
        "Optimal locally correct",
        "locally correct",
        "LOLC",
        "UOLC",
        exact.ciolc,
        exact.ciolcx,
        "local",
        "Garthwaite, Moustafa & Elfadaly 2024, Scand. J. Stat. 51",
        aliases=("locally-correct", "optimal-locally-correct"),
        cost="per-row-root",
        max_n=50000,
    ),
    MethodSpec(
        "witting",
        "Witting (u=1/2)",
        "randomised exact",
        "LWIT",
        "UWIT",
        exact.ciwitting,
        exact.ciwittingx,
        "exact-randomized",
        "Witting 1985, Beispiel 2.106; Stevens 1950, Biometrika 37",
        aliases=("stevens",),
        defaults={"u": 0.5},
        cost="vectorised-root",
    ),
    MethodSpec(
        "coverage-adjusted",
        "Coverage-adjusted CP (Thulin)",
        "adjusted exact",
        "LGCP",
        "UGCP",
        adjusted.cigcp,
        adjusted.cigcpx,
        "approximate",
        "Thulin 2014, Scand. J. Statist. 41 (arXiv:1204.5894)",
        aliases=("thulin", "gcp", "adjusted-cp"),
        defaults={"r": 1.0, "kind": "prior"},
        cost="per-row-root",
        max_n=3000,
    ),
    MethodSpec(
        "uniform-noise-wilson",
        "U(-1/2,1/2)-noise Wilson",
        "randomised smoothing",
        "LUNW",
        "UUNW",
        adjusted.ciunifwilson,
        adjusted.ciunifwilsonx,
        "approximate",
        "Thulin 2014 (arXiv:1402.6536)",
        aliases=("unif-wilson",),
        defaults={"seed": 0},
        deterministic=False,
    ),
    MethodSpec(
        "split-wilson",
        "Split-sample Wilson",
        "randomised smoothing",
        "LSPW",
        "USPW",
        adjusted.cisplitwilson,
        adjusted.cisplitwilsonx,
        "approximate",
        "Decrouez & Hall 2014; Thulin 2014",
        aliases=("split-sample-wilson", "decrouez-hall"),
        defaults={"seed": 0},
        deterministic=False,
    ),
    MethodSpec(
        "score-cc",
        "Score + continuity (Newcombe)",
        "score (continuity-corrected)",
        "LSCC",
        "USCC",
        pires.ciscorecc,
        pires.ciscoreccx,
        "approximate",
        "Newcombe 1998 (method 4); Pires & Amado 2008 (IV)",
        aliases=("wilson-cc", "newcombe-cc"),
    ),
    MethodSpec(
        "wald-i",
        "Wald-I (exact boundary rows)",
        "Wald variants",
        "LWDI",
        "UWDI",
        pires.ciwaldi,
        pires.ciwaldix,
        "approximate",
        "Vollset 1993; Pires & Amado 2008 (VII)",
    ),
    MethodSpec(
        "wald-i-cc",
        "Wald-I + continuity",
        "Wald variants",
        "LWIC",
        "UWIC",
        pires.ciwaldicc,
        pires.ciwaldiccx,
        "approximate",
        "Pires & Amado 2008 (VIII)",
    ),
    MethodSpec(
        "wald-recentred",
        "Recentred Wald-I",
        "Wald variants",
        "LWRC",
        "UWRC",
        pires.ciwaldrec,
        pires.ciwaldrecx,
        "approximate",
        "Brown, Cai & DasGupta 2002; Pires & Amado 2008 (IX)",
        aliases=("wald-rec",),
    ),
    MethodSpec(
        "wald-recentred-cc",
        "Recentred Wald-I + continuity",
        "Wald variants",
        "LWRK",
        "UWRK",
        pires.ciwaldreccc,
        pires.ciwaldrecccx,
        "approximate",
        "Pires & Amado 2008 (X)",
        aliases=("wald-rec-cc",),
    ),
    MethodSpec(
        "analytic-percentile",
        "Analytic percentile bootstrap",
        "bootstrap (exact law)",
        "LBTP",
        "UBTP",
        pires.cibootp,
        pires.cibootpx,
        "approximate",
        "Pires & Amado 2008 (XI)",
        aliases=("boot-analytic",),
    ),
    MethodSpec(
        "analytic-percentile-cc",
        "Analytic percentile bootstrap + cc",
        "bootstrap (exact law)",
        "LBPC",
        "UBPC",
        pires.cibootpcc,
        pires.cibootpccx,
        "approximate",
        "Pires & Amado 2008 (XII)",
        aliases=("boot-analytic-cc",),
    ),
    MethodSpec(
        "analytic-bcp",
        "Analytic bias-corrected percentile",
        "bootstrap (exact law)",
        "LBCP",
        "UBCP",
        pires.cibcp,
        pires.cibcpx,
        "approximate",
        "Pires & Amado 2008 (XIII)",
        aliases=("boot-bcp-analytic",),
    ),
    MethodSpec(
        "analytic-bcp-cc",
        "Analytic bias-corrected percentile + cc",
        "bootstrap (exact law)",
        "LBCC",
        "UBCC",
        pires.cibcpcc,
        pires.cibcpccx,
        "approximate",
        "Pires & Amado 2008 (XIV)",
        aliases=("boot-bcp-analytic-cc",),
    ),
    MethodSpec(
        "arcsine-anscombe",
        "Arcsine-cc-Anscombe",
        "variance-stabilised",
        "LANS",
        "UANS",
        pires.ciarcsineans,
        pires.ciarcsineansx,
        "approximate",
        "Pires & Amado 2008 (XVII); Anscombe 1948",
        aliases=("arcsine-cc-anscombe",),
    ),
    MethodSpec(
        "mixture",
        "Mixture CS (Beta(1/2,1/2))",
        "anytime-valid",
        "LMIX",
        "UMIX",
        betting.cimixture,
        betting.cimixturex,
        "anytime",
        "Robbins 1970; Howard, Ramdas, McAuliffe & Sekhon 2021",
        aliases=("mixture-cs", "beta-binomial-mixture"),
        cost="vectorised-root",
    ),
    MethodSpec(
        "normal-mixture",
        "Normal-mixture CS",
        "anytime-valid",
        "LNMX",
        "UNMX",
        betting.cinormalmix,
        betting.cinormalmixx,
        "anytime",
        "Robbins 1970; Howard et al. 2021",
        aliases=("normal-mixture-cs",),
    ),
    MethodSpec(
        "betting",
        "Hedged betting",
        "betting (derandomised)",
        "LBET",
        "UBET",
        betting.cibetting,
        betting.cibettingx,
        "exact",
        "Waudby-Smith & Ramdas 2024, JRSS-B 86",
        aliases=("hedged", "hedged-betting", "waudby-smith-ramdas"),
        cost="simulation",
        deterministic=False,
        max_n=1500,
    ),
]

REGISTRY: dict[str, MethodSpec] = {s.key: s for s in _SPECS}
_ALIAS: dict[str, str] = {a: s.key for s in _SPECS for a in (s.key, *s.aliases)}


def lookup(name: str) -> MethodSpec | None:
    """The spec for a method name or alias (case-insensitive), or ``None`` if unknown here."""
    key = _ALIAS.get(str(name).lower().strip())
    return REGISTRY[key] if key else None


def list_methods(family: str | None = None) -> pd.DataFrame:
    """A table of every extended method: label, family, coverage guarantee, cost, reference."""
    rows = [
        {
            "method": s.key,
            "label": s.label,
            "family": s.family,
            "guarantee": s.guarantee,
            "cost": s.cost,
            "reference": s.ref,
        }
        for s in _SPECS
        if family is None or family.lower() in s.family.lower()
    ]
    return pd.DataFrame(rows)


def describe(name: str) -> dict:
    """Everything the registry knows about one method, as a plain dict."""
    s = lookup(name)
    if s is None:
        raise ValueError(f"unknown extended method {name!r}; see list_methods()")
    return {
        "key": s.key,
        "label": s.label,
        "family": s.family,
        "guarantee": s.guarantee,
        "cost": s.cost,
        "deterministic": s.deterministic,
        "parameters": {k: v for k, v in s.defaults.items()},
        "accepts": sorted(s.accepts()),
        "aliases": list(s.aliases),
        "reference": s.ref,
        "columns": (s.lo, s.hi),
    }
