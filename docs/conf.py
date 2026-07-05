"""Sphinx configuration for the binomcikit documentation."""
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "binomcikit"
author = "Vyasa R Rajeswaran, Pranava BA, Justindhas Y"
copyright = "2026, " + author
release = "2.0.9"
version = "2.0.9"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",                 # NumPy-style docstrings (scientific standard)
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx_design",            # cards / grids on the landing page
]

# --- autodoc / autosummary / numpydoc ---------------------------------------
autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
# Heavy runtime deps are mocked so the docs build quickly without the full
# scientific stack; signatures/docstrings still come from the real source.
autodoc_mock_imports = ["numpy", "pandas", "scipy", "plotnine", "statsmodels"]

# --- MyST -------------------------------------------------------------------
myst_enable_extensions = ["colon_fence", "deflist", "dollarmath"]
myst_heading_anchors = 3

# --- intersphinx ------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
}

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# --- HTML / theme -----------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = "binomcikit"
html_static_path = ["_static"]
html_theme_options = {
    "github_url": "https://github.com/pranava-ba/binomcikit",
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "show_prev_next": True,
    "icon_links": [
        {"name": "PyPI", "url": "https://pypi.org/project/binomcikit/",
         "icon": "fa-brands fa-python"},
    ],
    "navigation_with_keys": True,
}
html_context = {
    "github_user": "pranava-ba",
    "github_repo": "binomcikit",
    "github_version": "main",
    "doc_path": "docs",
}

# Keep the build resilient while docstrings are still being filled in.
nitpicky = False
suppress_warnings = ["autodoc", "ref.python", "myst.header"]
