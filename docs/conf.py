"""Sphinx configuration for the binomcikit documentation."""
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "binomcikit"
author = "Vyasa R Rajeswaran, Pranava BA, Justindhas Y"
copyright = "2026, " + author
release = "3.0.8"
version = "3.0.8"

extensions = [
    "myst_nb",                  # MyST markdown + executable {code-cell} blocks (includes myst_parser)
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",                 # NumPy-style docstrings (scientific standard)
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx_design",            # cards / grids on the landing page
]

# --- MyST-NB (executable docs) ----------------------------------------------
# Code written in ```{code-cell} blocks runs at build time, so the outputs shown
# in the docs are generated from the real package and can never drift from it.
# Plain ```python blocks are left as static snippets. Requires binomcikit to be
# importable in the build env (installed editable locally; `pip install .` on RTD).
nb_execution_mode = "auto"          # run pages that have code cells and no stored output
nb_execution_timeout = 120
nb_execution_raise_on_error = True  # a broken example fails the build (catches drift)
nb_merge_streams = True

# --- autodoc / autosummary / numpydoc ---------------------------------------
autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
# binomcikit itself is installed in the build env (so MyST-NB can execute real
# code), which brings numpy / scipy / pandas. Only the *optional* plotting and
# test-only stacks are mocked for autodoc of the plot modules.
autodoc_mock_imports = ["plotnine", "plotly", "statsmodels", "numba"]

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

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",      # MyST-NB parses plain MyST markdown *and* executable pages
    ".ipynb": "myst-nb",
}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# --- HTML / theme -----------------------------------------------------------
# Furo: a collapsible left-sidebar nav (hamburger on mobile) with a deliberately
# minimal top bar — the section navigation lives in the sidebar, not the header.
html_theme = "furo"
html_title = "binomcikit"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]
# No "Edit this page" / "View source" links in the article header.
html_show_sourcelink = False
html_theme_options = {
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#1f6feb",
        "color-brand-content": "#1f6feb",
    },
    "dark_css_variables": {
        "color-brand-primary": "#58a6ff",
        "color-brand-content": "#58a6ff",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/pranava-ba/binomcikit",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/binomcikit/",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 448 512">
                    <path d="M439.8 200.5c-7.7-30.9-22.3-54.2-53.4-54.2h-40.1v47.4c0 36.8-31.2 67.8-66.8 67.8H172.7c-29.2 0-53.4 25-53.4 54.3v101.8c0 29 25.2 46 53.4 54.3 33.8 9.9 66.3 11.7 106.8 0 26.9-7.8 53.4-23.5 53.4-54.3v-40.7H226.2v-13.6h160.2c31.1 0 42.6-21.7 53.4-54.2 11.2-33.5 10.7-65.7 0-108.8zM286.2 404c11.1 0 20.1 9.1 20.1 20.3 0 11.3-9 20.4-20.1 20.4-11 0-20.1-9.2-20.1-20.4.1-11.3 9.1-20.3 20.1-20.3zM167.8 107.5c-31.1 0-42.6 21.7-53.4 54.2-11.2 33.5-10.7 65.7 0 108.8 7.7 30.9 22.3 54.2 53.4 54.2h40.1v-47.4c0-36.8 31.2-67.8 66.8-67.8h106.8c29.2 0 53.4-25 53.4-54.3V57.4c0-29-25.2-46-53.4-54.3-33.8-9.9-66.3-11.7-106.8 0C147.9 11 121.4 26.6 121.4 57.4v40.7h106.9v13.6H68.1c-31.1 0-42.6 21.7-53.4 54.2z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

# Keep the build resilient while docstrings are still being filled in.
nitpicky = False
suppress_warnings = ["autodoc", "ref.python", "myst.header"]
