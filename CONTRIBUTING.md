# Contributing to binomcikit

Thanks for helping. This page is the short version of how the project works; the conventions it points to are written down in
`planning/ROADMAP.md` (sections 5–7).

## Set up

```bash
git clone https://github.com/pranava-ba/binomcikit.git
cd binomcikit
pip install -e ".[dev]"          # tests, ruff, black, mypy, pre-commit, plotnine and numba
pre-commit install               # optional: runs ruff and black before each commit
```

## Before you open a pull request

Run the same checks CI runs:

```bash
pytest -q                                           # the whole suite (about a minute)
ruff check .
black --check src tests
mypy src/binomcikit                                 # config in pyproject.toml
cd docs && PYTHONPATH=../src python -m sphinx -W -b html . _build/html   # docs must build with no warnings
```

CI also enforces a coverage floor (`--cov-fail-under`, currently 80%) and a weekly benchmark check
(`python benchmarks/regression_check.py` fails when a tracked call gets more than 2x slower).

## What a new or changed method needs

* **An independent oracle.** A test that compares the result with something that was not written from the same
  idea: another library (statsmodels, scipy, R), published values, or a defining property such as "the limit solves the
  score equation". Check that the oracle computes the *same* convention before trusting it (for example, scipy's two-sided
  exact p-value is not the equal-tailed one).
* **A look at the source.** Implement from the paper's text or a documented reference implementation, not from a summary of it, and
  say in the docstring where the formula comes from. If a primary source is paywalled, say which sources you used instead.
* **Numerical care.** Use the log-likelihood (never raw `pmf`) inside root-finding, find an endpoint by bracketing (`brentq`), not by
  minimising `abs(f)`, and try the function at `n = 10^5` and `10^6` to catch underflow.
* **Docs.** A method gets a page with a "Use it" and an "Understand it" part (copy `docs/methods/wald.md`), its terms linked to
  `docs/glossary.md`, and an entry in `CHANGELOG.md`. The docs build is a hard gate.
* **Reuse the shared engine.** Coverage, expected length, p-confidence and error all come from the common metric engine; do not
  re-implement them per method.

## Style

`ruff` (F and I rules) and `black` with line length 100; the config is in `pyproject.toml`. Match the surrounding code: the legacy modules
mirror the R package's structure on purpose.

## Reporting a bug

Open an issue with the smallest call that shows it, the output you expected and what you got, and your versions
(`python -c "import binomcikit, numpy, scipy, pandas; print(binomcikit.__version__, numpy.__version__, scipy.__version__, pandas.__version__)"`).
A wrong interval is most useful with a reference value and where it comes from.

## Licence

binomcikit is GPL-3.0 (inherited from the R package it ports). By contributing you agree your contribution is licensed under the same terms.
