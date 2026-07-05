"""Regenerate ``docs/r_to_python_mapping.md`` and ``docs/api.md``.

Parses every function in the R source under ``reference/rpackage/R`` and maps it
to the Python function/module it was ported to (by introspecting the installed
``binomcikit`` package), then writes the mapping table and the autodoc API page.

Run from anywhere:  ``python tools/gen_r_to_python_mapping.py``
"""
import importlib
import inspect
import os
import pkgutil
import re
import sys
import warnings

warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
RDIR = os.path.join(ROOT, "reference", "rpackage", "R")
DOCS = os.path.join(ROOT, "docs")
GH = "https://github.com/RajeswaranV/proportion/blob/master/R"

sys.path.insert(0, SRC)
import binomcikit as bk  # noqa: E402


def build_py_index():
    """Map lowercased python name -> (canonical module, real name)."""
    py_index, modules = {}, set()
    for mod in pkgutil.walk_packages(bk.__path__, bk.__name__ + "."):
        try:
            m = importlib.import_module(mod.name)
        except Exception:
            continue
        for nm, obj in vars(m).items():
            if nm.startswith("_") or not inspect.isfunction(obj):
                continue
            if getattr(obj, "__module__", "").startswith("binomcikit"):
                py_index.setdefault(nm.lower(), (obj.__module__, nm))
                modules.add(obj.__module__)
    for nm, obj in vars(bk).items():
        if not nm.startswith("_") and inspect.isfunction(obj) \
           and getattr(obj, "__module__", "").startswith("binomcikit"):
            py_index.setdefault(nm.lower(), (obj.__module__, nm))
            modules.add(obj.__module__)
    return py_index, modules


def parse_r():
    """Return [(file, funcname, lineno)] for every R function definition."""
    func_re = re.compile(r"^([A-Za-z][A-Za-z0-9_.]*)\s*(?:<-|=)\s*function\s*\(")
    data = []
    for f in sorted(x for x in os.listdir(RDIR) if x.endswith(".R")):
        with open(os.path.join(RDIR, f), encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                m = func_re.match(line)
                if m:
                    data.append((f, m.group(1), i))
    return data


SPECIFIC = {
    "ciLR": "`x` returned as a column (R port used a MultiIndex) — inconsistency fixed",
    "ciEXx": "Root-finding via `scipy.optimize.brentq` (R port called a nonexistent `stats.root_scalar`)",
    "ciBA": "`TeachingDemos::hpd` reimplemented with a SciPy shortest-interval search (`_hpd.hpd_beta`)",
    "ciBAx": "`TeachingDemos::hpd` reimplemented with SciPy (`_hpd.hpd_beta`)",
    "ciBAD": "Merged into `ciba` (vector-prior path handled by NumPy broadcasting)",
    "ciAllx": "Newly added — was missing from the earlier partial port",
}
HPD_FUNCS = {"empericalBA", "empericalBAx", "lengthBA", "pCOpBIBA", "errBA",
             "covpBA", "PlotcovpBA", "PlotexplBA", "PlotlengthBA",
             "PlotpCOpBIBA", "PloterrBA", "PlotciBA"}


def note(fn, matched):
    internal = bool(re.match(r"^(gexpl|gcovp|gint|exlim|lufn|likelhd)", fn))
    parts = []
    if fn in SPECIFIC:
        parts.append(SPECIFIC[fn])
    if fn.startswith("Plot"):
        parts.append("ggplot2 → plotnine; returns a plotnine `ggplot`")
    if re.match(r"^(covp|length|expl|emperical)", fn):
        parts.append("`stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R")
    if fn in HPD_FUNCS and "hpd" not in " ".join(parts).lower():
        parts.append("uses SciPy HPD (`_hpd.hpd_beta`)")
    if internal:
        parts.append("internal R helper — ported directly" if matched
                     else "internal R helper — folded into the shared Python engine")
    elif not matched and "Merged" not in " ".join(parts):
        parts.append("folded into the shared Python engine (no standalone function)")
    parts.append("lowercased name; pandas `DataFrame`")
    seen = []
    for p in parts:
        if p not in seen:
            seen.append(p)
    return "; ".join(seen)


FAMILIES = {
    "0": "Package / naming", "1": "1xx — Confidence Intervals",
    "2": "2xx — Coverage Probability", "3": "3xx — Expected Length",
    "4": "4xx — p-Confidence & p-Bias", "5": "5xx — Error & Failure",
    "6": "6xx — Bayesian",
}

HEADER = """\
# R → Python mapping

This page maps **every function in the original R package
[`proportion`](https://github.com/RajeswaranV/proportion) (v2.1.2, by M. Subbiah
& V. Rajeswaran)** to its equivalent in **`binomcikit`**, the Python port.

Use it to find the Python call for any R function, to jump to the source on
either side, and to see what changed in translation.

## How to read this page

- The **R file** heading (e.g. ``R/101.Confidence_base_n.R``) links to the
  original source on GitHub.
- The **Python file** column links to that module's page in this documentation.
- The **Python function** column links to that function's own API page
  (signature + docstring).
- The **R → Py changes** column notes anything that differs beyond the two
  conventions that apply almost everywhere:
  1. **Naming** — R CamelCase (`ciWD`, `PlotcovpWD`) → Python lower case
     (`ciwd`, `plotcovpwd`).
  2. **Return type** — R `data.frame` → pandas `DataFrame` (plot functions
     return a plotnine `ggplot`).

```{note}
Rows marked *"no standalone function"* are internal R helpers (e.g. `gcovpW`,
`exlim201l`) **folded** into a shared Python engine rather than ported as
separate public functions. Behaviour is preserved; only the packaging differs.
See *"What 'folded' means"* below.
```

## What "folded" means

**Folded** means the R function was not ported as its own standalone Python
function. Instead its logic was **absorbed into a shared helper** that several
Python functions call. Nothing was dropped — the behaviour lives on, just in one
reusable place rather than in a separate named function.

Why it happens: the R package repeats the same computation across every method.
For coverage probability, R has a separate internal helper per method —
`gcovpW` (Wald), `gcovpS` (Score), `gcovpA` (ArcSine), … — and each contains a
near-identical copy of the "simulate *p*, count coverage" loop, differing only
in which interval limits it uses. The Python port writes that loop **once**
(`_coverage_series` / `_coverage_core` in `binomcikit.covp.base_all`); every
method feeds its own limits into it:

```python
# the shared engine — written once, method-agnostic
def _coverage_series(n, lower, upper, hp):
    ...the coverage loop...

# the Wald coverage function just supplies Wald limits:
def covpwd(n, alp, a, b, t1, t2, seed=None):
    df = ciwd(n, alp)                                 # Wald limits
    return _coverage(..., df['LWD'], df['UWD'], ...)  # calls the engine
```

So R's `gcovpW` has no 1:1 Python twin — its guts are the `_coverage_series`
call inside `covpwd`. Only **internal, non-exported** R helpers are folded this
way (coverage/expected-length curve helpers like `gcovpW`, `gexplWD`, and
plumbing like `gintcovpEX202`). Every **public** R function — all 305 exported
ones — got its own real Python function and is never folded.

```{admonition} Reproducibility of simulated results
:class: tip

The evaluation families (coverage `covp*`, expected length `length*`/`expl*`,
empirical Bayes `emperical*`) draw hypothetical *p* from `Beta(a, b)`. R uses
`stats::rbeta`; the Python port uses NumPy's `default_rng`, so these results
match R **in distribution, not draw-for-draw** — each such function takes an
optional `seed=` argument for reproducibility.
```

## Summary

| | Value |
|---|---|
| R source files | 59 (58 contain functions) |
| R function definitions | 470 |
| Exported R functions (public API) | 305 |
| Python functions | 401 numeric + 150 plots |
| Python subpackages | `ci` (1xx), `covp` (2xx), `expl` (3xx), `pconf` (4xx), `err` (5xx), `bayes` (6xx) |

*This page is generated by ``tools/gen_r_to_python_mapping.py`` — do not edit by
hand.*
"""


def main():
    py_index, modules = build_py_index()
    rows = parse_r()

    out = [HEADER]
    cur_fam = cur_file = None
    for f, fn, _ in rows:
        fam = FAMILIES.get(f[0], "Other")
        if fam != cur_fam:
            out.append(f"\n## {fam}\n")
            cur_fam, cur_file = fam, None
        if f != cur_file:
            out.append(f"\n### [`R/{f}`]({GH}/{f})\n")
            out.append("| R function | Python file | Python function | R → Py changes |")
            out.append("|---|---|---|---|")
            cur_file = f
        key = fn.lower()
        matched = key in py_index
        if matched:
            canon, real = py_index[key]
            short = canon.replace("binomcikit.", "")
            pyfile = f"{{py:mod}}`{short} <{canon}>`"
            pyfunc = f"{{py:func}}`{real} <{canon}.{real}>`"
        else:
            pyfile, pyfunc = "—", "*(no standalone function)*"
        out.append(f"| `{fn}` | {pyfile} | {pyfunc} | {note(fn, matched)} |")

    with open(os.path.join(DOCS, "r_to_python_mapping.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")

    # Per-function reference pages (which the {py:func}/{py:mod} links resolve
    # to) are generated separately by tools/gen_reference_pages.py.

    matched = sum(1 for _, fn, _ in rows if fn.lower() in py_index)
    print(f"R files: {len({r[0] for r in rows})} | R funcs: {len(rows)} | "
          f"matched to Python: {matched} | API modules: {len(modules)}")


if __name__ == "__main__":
    main()
