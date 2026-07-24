# Which interval should I use?

A living guide, filled in as each method is documented. The short answer for most real work:
**use Wilson (Score)**; reach for the others for specific reasons.

| method | use it when | avoid it when | call |
|---|---|---|---|
| **Wald** | teaching; a quick baseline; large *n* with {term}`theta` near 0.5 | small *n*; θ near 0 or 1 ({term}`coverage` dips; {term}`zero-width interval`s) | `bk.ci(n=…, method="wald")` |
| **Agresti–Coull** | you want Wald's simplicity *and* reliable coverage | — (a solid general default) | `method="agresti-coull"` |

*(Rows for Wilson, ArcSine, Logit, Wald-T, Likelihood-ratio, Exact / Mid-P, Bayesian, Blaker and
Bootstrap are added as those sub-phases complete.)*

## Decide empirically for **your** case
You don't have to take a rule of thumb on faith. For your specific *n* and {term}`alpha`, compute
the {term}`coverage` and {term}`expected length` of several methods and compare them directly —
that is exactly what the `covp*` and `length*` function families are for (see
{doc}`user_guide/index`). Choosing a method by *measuring* it on your own problem is the whole
point of this package.
