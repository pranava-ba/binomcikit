"""Generate per-module reference pages under ``docs/reference/``.

Each module gets one page; each public function in it gets a section containing
the 9 documentation elements requested:

  1. what the function is, in plain words        (prose stub - fill by hand)
  2. the maths behind it                          (prose stub)
  3. a simple example                             (prose stub)
  4. the R source snippet                         (auto-extracted)
  5. what the R code does                         (prose stub)
  6. the Python source snippet                    (auto-extracted)
  7. what the Python code does                    (prose stub)
  8. the R -> Py changes                          (auto-filled)
  9. a link back to the mapping table             (auto)

Existing pages are NOT overwritten, so hand-written pages survive re-runs.
The ``.. autofunction::`` directive in each section is what the mapping table's
``{py:func}`` links resolve to, and ``.. module::`` provides the ``{py:mod}``
target.

Run:  ``python tools/gen_reference_pages.py``  (add ``--force`` to overwrite)
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
REFDIR = os.path.join(ROOT, "docs", "reference")
GH = "https://github.com/RajeswaranV/proportion/blob/master/R"
FORCE = "--force" in sys.argv

sys.path.insert(0, SRC)
import binomcikit as bk  # noqa: E402

# reuse the change-note logic from the mapping generator
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gen_r_to_python_mapping import note  # noqa: E402


def module_functions():
    """module -> list of (pyname, obj); and pyname(lower) -> realname."""
    mods = {}
    for m in pkgutil.walk_packages(bk.__path__, bk.__name__ + "."):
        try:
            mod = importlib.import_module(m.name)
        except Exception:
            continue
        for nm, obj in vars(mod).items():
            if nm.startswith("_") or not inspect.isfunction(obj):
                continue
            if obj.__module__ == m.name:  # defined here, not imported
                mods.setdefault(m.name, []).append((nm, obj))
    return mods


def r_defs():
    """lower(rname) -> (file, lineno, rname)."""
    func_re = re.compile(r"^([A-Za-z][A-Za-z0-9_.]*)\s*(?:<-|=)\s*function\s*\(")
    out = {}
    for f in sorted(x for x in os.listdir(RDIR) if x.endswith(".R")):
        with open(os.path.join(RDIR, f), encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                m = func_re.match(line)
                if m:
                    out.setdefault(m.group(1).lower(), (f, i, m.group(1)))
    return out


def extract_r(fname, lineno, maxlines=70):
    """Extract an R function body by brace balancing from its def line."""
    path = os.path.join(RDIR, fname)
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    buf, depth, started = [], 0, False
    for ln in lines[lineno - 1:]:
        buf.append(ln.rstrip("\n"))
        depth += ln.count("{") - ln.count("}")
        if "{" in ln:
            started = True
        if started and depth <= 0:
            break
    truncated = len(buf) > maxlines
    if truncated:
        buf = buf[:maxlines] + ["  # ... (truncated - see the linked source)"]
    return "\n".join(buf)


def extract_py(obj, maxlines=60):
    try:
        src = inspect.getsource(obj)
    except (OSError, TypeError):
        return "# source unavailable"
    lines = src.split("\n")
    if len(lines) > maxlines:
        lines = lines[:maxlines] + ["    # ... (truncated - see the linked source)"]
    return "\n".join(lines)


STUB = "*(to be written)*"

# --------------------------------------------------------------------------- #
# Knowledge base: compose real prose for the repetitive 2xx-6xx families.      #
# --------------------------------------------------------------------------- #
_METHODS = {
    "wd": "Wald (normal-approximation) interval",
    "sc": "Score / Wilson interval",
    "as": "ArcSine (variance-stabilised) interval",
    "lr": "Likelihood-Ratio interval",
    "lt": "Logit-Wald interval",
    "tw": "Wald-T interval",
    "ex": "Exact (Clopper-Pearson / mid-p) interval",
    "ba": "Bayesian credible interval",
    "all": "interval methods",
    "gen": "user-supplied interval limits",
    "sim": "user-supplied limits over simulated p",
}
_BASE_TOKENS = set(_METHODS)
_VARIANT_TEXT = {"": "", "adj": "adjusted ", "cc": "continuity-corrected "}


def _iv_phrase(variant, method):
    """An article-safe noun phrase for the interval / method set."""
    vt = _VARIANT_TEXT[variant]
    if method == "all":
        return f"all {vt}interval methods"
    if method in ("gen", "sim"):
        return _METHODS[method]
    return f"the {vt}{_METHODS[method]}"

# family_key -> (prefix stripped from the numeric name, is_plot, info)
_FAMILY = {
    "covp": {
        "metric": "coverage probability",
        "plain": "the **coverage probability** of {iv} — how often the interval "
                 "actually contains the true proportion, averaged over "
                 "hypothetical values of *p* drawn from a `Beta(a, b)` prior",
        "maths": r"For each simulated *p*, coverage "
                 r"$= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the "
                 r"function reports the mean (`mcp`), minimum (`micp`), "
                 r"RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).",
        "rdoc": "computes the interval limits, simulates 5000 `Beta(a, b)` draws, "
                "sums the binomial mass wherever a draw is covered, and returns "
                "the summary statistics",
        "pydoc": "reuses the 1xx interval limits and the shared `_coverage` engine "
                 "(NumPy `default_rng` for the Beta draws), returning the same "
                 "summary",
    },
    "length": {
        "metric": "expected length",
        "plain": "the **expected length** of {iv} — the average interval width, "
                 "over hypothetical *p* drawn from a `Beta(a, b)` prior",
        "maths": r"Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, "
                 r"summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the "
                 r"$\pm\text{SD}$ band `explLL`/`explUL`.",
        "rdoc": "forms the per-`x` interval widths, averages them over 5000 "
                "`Beta(a, b)` draws, and returns the length summary",
        "pydoc": "reuses the 1xx interval limits and the shared `_expl_series` "
                 "engine, returning the same summary (`explSD` uses `ddof=1` to "
                 "match R's `sd`)",
    },
    "expl": {
        "metric": "expected-length curve",
        "plain": "the per-*p* **expected-length curve** for {iv} — the raw "
                 "`(hp, ew)` values behind the expected-length plots",
        "maths": r"Same expected-length quantity as `length*`, but returned for "
                 r"every simulated *p* rather than summarised.",
        "rdoc": "returns the expected length at each simulated *p* (for plotting)",
        "pydoc": "reuses the shared `_expl_curve` engine, returning a long "
                 "`(hp, ew, method)` frame",
    },
    "pconf": {
        "metric": "p-confidence and p-bias",
        "plain": "the **p-confidence and p-bias** of {iv} — deterministic "
                 "measures (no simulation) of how well the interval's actual "
                 "confidence matches the nominal level, per interior `x`",
        "maths": r"For each interior `x`, two binomial tail probabilities give "
                 r"p-confidence $=100(1-\max\text{tail})$ and "
                 r"p-bias $=100\max(0,\text{tail difference})$.",
        "rdoc": "reads the interval limits and evaluates the two tail "
                "probabilities for every interior `x`, returning `x1`, `pconf`, "
                "`pbias`",
        "pydoc": "reuses the 1xx interval limits and the deterministic "
                 "`_pconf_pbias` engine (`scipy.stats.binom` tails); matches R "
                 "exactly",
    },
    "err": {
        "metric": "error and failure",
        "plain": "the **error and failure** summary of {iv} for a null proportion "
                 "`phi` and threshold `f` — the increase in nominal error "
                 "(`delalp`), long-term power (`theta`) and a pass/fail verdict",
        "maths": r"`delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}"
                 r"\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` "
                 r"excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.",
        "rdoc": "reads the interval limits, sums the binomial mass at the `x` that "
                "exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`",
        "pydoc": "reuses the 1xx interval limits and the deterministic `_error` "
                 "engine; matches R exactly",
    },
}
_PLOT_FAMILY = {  # plot-prefix -> (numeric family key, what it draws)
    "plotcovp": ("covp", "the coverage-probability curve against *p*"),
    "plotexpl": ("expl", "the expected-length curve against *p*"),
    "plotlength": ("length", "the sum-length bar chart"),
    "plotpcopbi": ("pconf", "p-confidence and p-bias against the number of successes"),
    "ploterr": ("err", "the error / long-term-power bars, coloured by pass/fail"),
}

_PARAM_VALUES = {
    "n": "20", "alp": "0.05", "a": "1", "b": "1", "a1": "1", "a2": "1",
    "b1": "1", "b2": "1", "a0": "1", "b0": "1", "t1": "0.9", "t2": "0.97",
    "h": "2", "c": "0.02", "phi": "0.5", "f": "-2", "e": "0.5", "x": "2",
    "th": "0.5", "th0": "0.5", "th1": "0.4", "th2": "0.6", "m": "3",
    "xnew": "1", "sL": "0.1", "sU": "10", "s": "1000", "hp": "[0.2, 0.5, 0.8]",
    "seed": "0",
}


def _parse(pyname, module):
    """Return (family_key, is_plot, variant, method, ci_fn) or None."""
    fam = module.split(".")[1]          # ci / covp / expl / pconf / err / bayes
    name = pyname
    is_plot = name.startswith("plot")
    # strip family prefix to get the method remainder
    strips = {
        "covp": ["plotcovp", "covp"], "err": ["ploterr", "err"],
        "pconf": ["plotpcopbi", "pcopbi"],
        "expl": ["plotexpl", "plotlength", "expl", "length"],
    }
    if fam not in strips:
        return None
    kind = "length"     # default numeric family for expl module
    for pre in strips[fam]:
        if name.startswith(pre):
            rem = name[len(pre):]
            if pre in ("plotexpl", "expl"):
                kind = "expl"
            elif pre in ("plotlength", "length"):
                kind = "length"
            elif fam == "covp":
                kind = "covp"
            elif fam == "pconf":
                kind = "pconf"
            elif fam == "err":
                kind = "err"
            break
    else:
        return None
    # determine variant + method from remainder
    if rem in _BASE_TOKENS:
        variant, method = "", rem
    elif rem and rem[0] == "a" and rem[1:] in _BASE_TOKENS:
        variant, method = "adj", rem[1:]
    elif rem and rem[0] == "c" and rem[1:] in _BASE_TOKENS:
        variant, method = "cc", rem[1:]
    else:
        return None
    ci_fn = "ci" + {"": "", "adj": "a", "cc": "c"}[variant] + method
    return kind, is_plot, variant, method, ci_fn


def _example_call(pyname, obj):
    try:
        sig = inspect.signature(obj)
    except (TypeError, ValueError):
        return f"bk.{pyname}(...)"
    params = [p for p in sig.parameters.values()
              if p.name not in ("self",)]
    needs_ll = any(p.name in ("LL", "UL") for p in params)
    args = []
    for p in params:
        if p.name in ("LL", "UL"):
            args.append(f'wd["{"LWD" if p.name == "LL" else "UWD"}"].values')
        elif p.name == "seed":
            args.append("seed=0")
        else:
            args.append(_PARAM_VALUES.get(p.name, "..."))
    call = f"bk.{pyname}({', '.join(args)})"
    if needs_ll:
        return "wd = bk.ciwd(20, 0.05)\n" + call
    return call


def _compose(pyname, obj, module):
    """Compose (plain, maths, example, rdoc, pydoc) or None to fall back."""
    parsed = _parse(pyname, module)
    if parsed is None:
        return None
    kind, is_plot, variant, method, ci_fn = parsed
    iv = _iv_phrase(variant, method)
    ex = "```python\nimport binomcikit as bk\n" + _example_call(pyname, obj) + "\n```"
    if is_plot:
        numeric_fam, draws = _PLOT_FAMILY[[k for k in _PLOT_FAMILY
                                          if pyname.startswith(k)][0]]
        base_metric = _FAMILY[numeric_fam]["metric"]
        plain = (f"Plots {draws} for {iv} — a visualisation of the "
                 f"corresponding `{base_metric}` numbers.")
        maths = "None; a visualisation of the numeric result."
        rdoc = f"calls the numeric function and draws {draws} with ggplot2"
        pydoc = "builds the equivalent plotnine figure and returns a `ggplot`"
        return plain, maths, ex, rdoc, pydoc
    info = _FAMILY[kind]
    plain = info["plain"].format(iv=iv)
    maths = info["maths"]
    rdoc = info["rdoc"]
    pydoc = info["pydoc"]
    return plain, maths, ex, rdoc, pydoc


def function_section(pyname, obj, rmap):
    mod = obj.__module__
    key = pyname.lower()
    rinfo = rmap.get(key)
    composed = _compose(pyname, obj, mod)
    plain, maths, example, rdoc, pydoc = (composed if composed else
                                          (STUB, STUB, None, STUB, STUB))
    parts = [f"## `{pyname}`\n"]
    parts.append("```{eval-rst}")
    parts.append(f".. autofunction:: {mod}.{pyname}")
    parts.append("```\n")
    parts.append(f"**In plain words** — {plain}\n")
    parts.append(f"**The maths** — {maths}\n")
    parts.append("**Example**\n")
    if example:
        parts.append(example + "\n")
    else:
        parts.append("```python\nimport binomcikit as bk\n"
                     f"# bk.{pyname}(...)   {STUB}\n```\n")
    if rinfo:
        f, ln, rname = rinfo
        parts.append(f"**R source** — [`R/{f}` (line {ln})]({GH}/{f}#L{ln}), "
                     f"function `{rname}`\n")
        parts.append("```r\n" + extract_r(f, ln) + "\n```\n")
        parts.append(f"**What the R code does** — The R function {rdoc}.\n"
                     if composed else f"**What the R code does** — {STUB}\n")
    parts.append(f"**Python source** — `{mod}.{pyname}`\n")
    parts.append("```python\n" + extract_py(obj) + "\n```\n")
    parts.append(f"**What the Python code does** — The Python port {pydoc}.\n"
                 if composed else f"**What the Python code does** — {STUB}\n")
    rname = rinfo[2] if rinfo else pyname
    matched = True
    parts.append(f"**R → Py changes** — {note(rname, matched)}\n")
    parts.append("{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`\n")
    parts.append("---\n")
    return "\n".join(parts)


STUB_MARKER = "<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->"

_FAMILY_BLURB = {
    "covp": "**coverage probability** — how often each interval actually "
            "contains the true proportion, evaluated over hypothetical *p* drawn "
            "from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, "
            "tolerance)",
    "expl": "**expected interval length** — the average width of each interval "
            "over hypothetical *p* drawn from a `Beta(a, b)` prior",
    "pconf": "**p-confidence and p-bias** — deterministic (no-simulation) measures "
             "of how well each interval's actual confidence matches its nominal "
             "level",
    "err": "**error and failure** — for a null proportion `phi` and threshold "
           "`f`, the increase in nominal error, the long-term power, and a "
           "pass/fail verdict for each interval",
}
_VARIANT_BLURB = {
    "base_all": "the **base** interval methods",
    "adj_all": "the **adjusted** (pseudo-count `x+h`, `n+2h`) interval methods",
    "cc_all": "the **continuity-corrected** interval methods (five methods; no "
              "Likelihood-Ratio)",
    "general": "**user-supplied** interval limits (given or simulated *p*)",
    "exact_bayes": "the **Exact** and **Bayesian** intervals",
    "bayes": "the **Bayesian** credible interval",
    "plots": "**plots** of the results (returning plotnine `ggplot` objects)",
}


def _module_intro(mod):
    parts = mod.split(".")
    fam = parts[1] if len(parts) > 1 else ""
    leaf = parts[-1]
    blurb = _FAMILY_BLURB.get(fam)
    if not blurb:
        return f"Module ``{mod}``."
    which = _VARIANT_BLURB.get(leaf, "these methods")
    reuse = ("These functions reuse the confidence-interval limits from the 1xx "
             "`ci` family and feed them through a shared engine, so only the "
             "supplied limits differ between methods. "
             if leaf not in ("plots",) else "")
    return (f"This module computes {blurb}, for {which}. {reuse}"
            "See the {doc}`mapping table </r_to_python_mapping>` for the full "
            "family overview.")


def write_module_page(mod, funcs, rmap):
    dotted = mod
    path = os.path.join(REFDIR, dotted + ".md")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            existing = fh.read()
        # Never overwrite a hand-written page (one without the stub marker).
        if STUB_MARKER not in existing:
            return "skip"
        if not FORCE:
            return "skip"
    short = mod.replace("binomcikit.", "")
    body = [STUB_MARKER + "\n",
            f"# `{short}`\n",
            "```{eval-rst}",
            f".. module:: {mod}",
            "```\n",
            _module_intro(mod) + "\n",
            "```{contents} Functions in this module\n:local:\n:depth: 1\n```\n"]
    for pyname, obj in sorted(funcs, key=lambda t: t[0]):
        body.append(function_section(pyname, obj, rmap))
    text = "\n".join(body).rstrip()
    if text.endswith("---"):          # avoid "document ends with a transition"
        text = text[:-3].rstrip() + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return "write"


def main():
    os.makedirs(REFDIR, exist_ok=True)
    rmap = r_defs()
    mods = module_functions()
    written = skipped = 0
    for mod, funcs in sorted(mods.items()):
        res = write_module_page(mod, funcs, rmap)
        written += res == "write"
        skipped += res == "skip"

    # index page with a toctree of all module pages
    idx = ["# Reference\n",
           "Per-function reference for every module in `binomcikit`. Each "
           "function links back to the {doc}`R → Python mapping table "
           "</r_to_python_mapping>`.\n",
           "```{toctree}\n:maxdepth: 1\n"]
    for mod in sorted(mods):
        idx.append(mod)
    idx.append("```\n")
    with open(os.path.join(REFDIR, "index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(idx))

    print(f"modules: {len(mods)} | pages written: {written} | skipped(existing): {skipped}")


if __name__ == "__main__":
    main()
