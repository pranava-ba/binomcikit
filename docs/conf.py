"""Sphinx configuration for the binomcikit documentation."""
import os
import sys

# Make the package importable for autodoc (src/ layout).
sys.path.insert(0, os.path.abspath("../src"))

project = "binomcikit"
author = "Vyasa R Rajeswaran, Pranava BA, Justindhas Y"
copyright = "2026, " + author
release = "0.0.5"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",     # Google/NumPy-style docstrings
    "sphinx.ext.viewcode",     # "[source]" links for Python
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",      # render $...$ / $$...$$ math
]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_default_options = {"members": True, "undoc-members": True}

# Heavy runtime deps are mocked so the docs build without a full scientific
# stack; signatures and docstrings still come from the real source.
autodoc_mock_imports = ["numpy", "pandas", "scipy", "plotnine", "statsmodels"]

myst_enable_extensions = ["colon_fence", "deflist", "dollarmath"]
myst_heading_anchors = 3

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
}

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_title = "binomcikit"

# Avoid failing the build on the many auto-generated cross-references while the
# API pages are still docstring-only.
nitpicky = False
suppress_warnings = ["autodoc", "ref.python"]
