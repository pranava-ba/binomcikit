# Migrating from R

`binomcikit` is a complete port of the R package
[`proportion`](https://github.com/RajeswaranV/proportion). If you know the R
package, moving to Python is mostly mechanical — two conventions cover almost
everything:

1. **Names are lower-cased.** R's CamelCase becomes Python lower case:
   `ciWD` → `ciwd`, `PlotcovpWD` → `plotcovpwd`, `hypotestBAF1` → `hypotestbaf1`.
2. **Return types change.** R `data.frame` → pandas `DataFrame`; the `Plot…`
   functions return a [plotnine](https://plotnine.org) `ggplot` instead of a
   ggplot2 object.

A few functions have deliberate differences (bug fixes, or SciPy replacing an R
dependency such as `TeachingDemos::hpd`). The full function-by-function mapping —
every R file, every R function, its Python equivalent, and any changes — is in
the table below.

```{toctree}
:maxdepth: 1

r_to_python_mapping
```

## Reproducibility note

The simulation-based families (`covp*`, `length*`/`expl*`, `emperical*`) draw
hypothetical *p* from `Beta(a, b)`. R uses `stats::rbeta`; Python uses NumPy's
`default_rng`. Because the two RNGs differ, these results match the R package
**in distribution, not draw-for-draw** — every such function takes an optional
`seed=` argument for reproducibility.
