# Which interval should I use?

A living guide, filled in as each method is documented. The short answer for most real work:
**use Wilson (Score)**; reach for the others for specific reasons.

| method | use it when | avoid it when | call |
|---|---|---|---|
| **Wilson (Score)** | **almost always** — the recommended default; small *n*; θ near 0 or 1 | you specifically need an interval centred on p̂, or guaranteed ≥-nominal {term}`coverage` | `bk.ci(n=…)` (it's the default) |
| **Wald** | teaching; a quick baseline; large *n* with {term}`theta` near 0.5 | small *n*; θ near 0 or 1 ({term}`coverage` dips; {term}`zero-width interval`s) | `bk.ci(n=…, method="wald")` |
| **Agresti–Coull** | you want Wald's simplicity *and* reliable coverage | — (a solid general default) | `method="agresti-coull"` |
| **ArcSine** | θ in the interior (≈ 0.2–0.8); a variance-stabilised interval | small counts / θ near 0 or 1 (collapses to a point that excludes the observed value) | `bk.ci(n=…, method="arcsine")` |
| **Logit-Wald** | extreme p̂; you want limits that never leave (0, 1) or collapse; log-odds modelling | you need the *tightest* interval (it runs slightly conservative / wide) | `bk.ci(n=…, method="logit")` |
| **Wald-T** | you want Wald's simple form with a principled small-sample (Student-*t*) fix | θ near 0 or 1 (over-covers heavily) | `bk.ci(n=…, method="waldt")` |
| **Likelihood-ratio** | you want excellent coverage (≈ Wilson) from a principled test-inversion; regulated work | you need a closed-form / fastest interval, or a CC variant (it has none) | `bk.ci(n=…, method="lr")` |
| **Blaker** (exact, *new*) | you want an exact guarantee (coverage ≥ 1 − α) **with less width than Clopper–Pearson** | you need a closed-form / fastest interval | `bk.ci(n=…, method="blaker")` |
| **Clopper–Pearson** (exact) | you must **guarantee** coverage ≥ 1 − α (regulated / safety-critical) | you care about width (Blaker dominates it — same guarantee, narrower) | `bk.ci(n=…, method="exact")` |
| **Mid-P** (exact) | you want most of the exact guarantee with less width | you need the hard ≥-nominal guarantee (Mid-P can dip slightly below) | `bk.ci(n=…, method="midp")` |
| **Bayesian / Jeffreys** | you want a probability statement about θ; excellent coverage (Jeffreys); or the wider Bayesian toolbox | you need a purely frequentist guarantee and won't state a prior | `bk.ci(n=…, method="jeffreys")` |

*(Rows for Blaker and Bootstrap are added as those sub-phases complete.)*

## Decide empirically for **your** case
You don't have to take a rule of thumb on faith. For your specific *n* and {term}`alpha`, compute
the {term}`coverage` and {term}`expected length` of several methods and compare them directly —
that is exactly what the `covp*` and `length*` function families are for (see
{doc}`user_guide/index`). Choosing a method by *measuring* it on your own problem is the whole
point of this package.
