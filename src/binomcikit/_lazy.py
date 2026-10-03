"""Lazy loading of the optional plotting functions.

Importing ``plotnine`` costs roughly a quarter of a second, which users who only want numbers
should not pay at ``import binomcikit``. Each family package keeps a ``name -> module`` table of its
plotting functions and resolves them here, on first attribute access (PEP 562).
"""

import importlib
import importlib.util
import sys


def plotting_available():
    """Whether plotnine (the ``[plots]`` extra) is installed -- checked without importing it."""
    return importlib.util.find_spec("plotnine") is not None


def resolve(package, table, name):
    """Import the module holding plot function ``name`` and cache the function on ``package``."""
    module = table.get(name)
    if module is None:
        raise AttributeError(f"module {package!r} has no attribute {name!r}")
    try:
        value = getattr(importlib.import_module(module, package), name)
    except ImportError as exc:  # plotnine missing: same signal as any absent attribute
        raise AttributeError(
            f"{name!r} needs the optional plotting dependencies (pip install binomcikit[plots])"
        ) from exc
    sys.modules[package].__dict__[name] = value
    return value
