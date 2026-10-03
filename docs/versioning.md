# Versioning and deprecation policy

> **Status: proposed.** This page states how releases are meant to be numbered and how things get removed. The project has not yet cut
> a release under it (PyPI still carries an old 0.0.5; the working version is 3.0.8), so the maintainer should confirm the points below before
> the first release that relies on them.

binomcikit follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

## What counts as the public API

* every name in `binomcikit.__all__` (the `ci*`, `covp*`, `expl*`, `pconf*`, `err*`, `bayes*` families, the `plot*` functions, `ci()`,
  `limits()`, `interval()`, the planning functions, `diff_interval()` and friends, and the registry in `list_methods()`);
* the **columns** of the tables those functions return, and the meaning of the `LABB`, `UABB` and `ZWI` flags;
* the method names accepted by `ci()`, `limits()`, `interval()` and `diff_interval()`, including their aliases.

Anything starting with an underscore, and everything under `binomcikit.ext`, `binomcikit.ci._fast` or the `*_graph` modules except through the
top-level names, is internal and may change in any release.

## What each kind of release may change

| Release | May contain |
|---|---|
| **Patch** (3.0.8 → 3.0.9) | bug fixes, including fixes that change a returned interval because the old value was wrong (these are listed under **Fixed** in `CHANGELOG.md`), documentation, speed-ups that leave results unchanged to ~1e-12 |
| **Minor** (3.0 → 3.1) | new methods, new functions, new optional arguments with defaults that keep the old behaviour, new columns appended to the end of a table, deprecations, dropping a Python version that has reached end of life |
| **Major** (3 → 4) | removing deprecated names, renaming or reordering columns, changing a default, changing what an existing method name computes |

A change that moves a documented interval by more than the tolerance its tests use (1e-9 for the closed forms, 1e-12 against oracles) is announced
in the changelog even when it is a bug fix.

## Deprecation

A name or argument scheduled for removal first emits a `DeprecationWarning` that says what to use instead and in which version it will be
removed, for **at least one minor release** and never within a patch release. Deprecations are listed under **Deprecated** in the changelog.

## Supported Python and dependency versions

The supported Python versions are the ones in the CI matrix (currently 3.9 to 3.13, see `.github/workflows/ci.yml`); the minimum numpy,
scipy and pandas are the lower bounds in `pyproject.toml`. Dropping a Python version is a minor release. The optional extras (`plots`, `fast`)
follow their own libraries' versions.

## Results that depend on randomness

Methods that draw random numbers (`"boot"`, `"betting"`, `"witting"`) take a `seed`; for a fixed seed, library version and numpy version the table
is reproducible. A change to how the random numbers are consumed is treated as a result-changing change (patch release with a changelog entry if
it fixes a bug, minor release otherwise).
