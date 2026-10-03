---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Extended exact, optimal and guaranteed intervals

Intervals whose coverage is guaranteed by *construction*, plus the criterion (`locally_correct`) for judging
the rest. All of them see the data only through `(x, n)`, so they feed the full {doc}`evaluation suite
<../evaluating_intervals>`.

| `method=` | Guarantee | In one line | Cost |
|---|---|---|---|
| `"sterne"` | {term}`exact interval` | accept the *most probable* outcomes first (Sterne's probability ordering) — shorter than Clopper–Pearson, not equal-tailed | per-row root |
| `"bsc"` | {term}`exact interval` | Blyth–Still–Casella: Clopper–Pearson shrunk until coverage touches 1 − α — the interval StatXact reports | global, ~O(n²) |
| `"olc"` | {term}`locally correct` | the shortest equal-tailed interval whose coverage averages to 1 − α/2 between spikes (Garthwaite et al. 2024) | per-row root, n ≤ 50 000 |
| `"coverage-adjusted"` | min coverage ≥ 1 − α′ | Clopper–Pearson at an *adjusted* level α′ so the **mean** coverage is 1 − α (Thulin 2014) | scalar root |
| `"witting"` (`"stevens"`) | {term}`randomised interval` — **exactly** 1 − α | the only interval that is not {term}`conservative` anywhere; costs a coin flip | vectorised root |
| `"hoeffding"`, `"chernoff"`, `"bernstein"`, `"empirical-bernstein"` | {term}`concentration inequality` | no asymptotics, valid at every n — wide, but unconditional | closed form / root |

## Use it

```{code-cell} python
import binomcikit as bk

bk.compare(3, 20, methods=["exact", "blaker", "sterne", "bsc", "olc", "wilson", "coverage-adjusted"])
```

Notice the ordering: the guaranteed intervals (`sterne`, `bsc`) are visibly shorter than Clopper–Pearson, and
the {term}`locally correct` OLC interval shorter still — at the price of not guaranteeing coverage at every θ.

### Audit any interval with `locally_correct`

```{code-cell} python
for m in ["exact", "midp", "olc", "wilson", "jeffreys"]:
    r = bk.locally_correct(20, 0.05, m)
    print(f"{m:9s} locally correct: {str(r['locally_correct']):5s}  worst cycle average {r['min_average']:.4f}  (target {r['target']}) ")
```

That reproduces Garthwaite, Moustafa & Elfadaly's published finding: Clopper–Pearson and Mid-P pass, **Wilson
does not**. The `cycles` table inside the result shows *where* an interval falls short:

```{code-cell} python
cyc = bk.locally_correct(20, 0.05, "wilson")["cycles"]
cyc[cyc.average < 0.975 - 1e-9].round(4).head()
```

### Randomised: exactly 1 − α

```{code-cell} python
import numpy as np, scipy.stats as st

def witting_coverage(n, a, theta, draws=121):
    k = np.arange(n + 1)
    pm = st.binom.pmf(k, n, theta)
    tot = 0.0
    for u in (np.arange(draws) + 0.5) / draws:
        w = bk.ciwitting(n, a, u=u)
        tot += pm[(w.LWIT.to_numpy() < theta) & (theta < w.UWIT.to_numpy())].sum()
    return tot / draws

for th in (0.1, 0.5, 0.9):
    print(f"theta={th}: Witting/Stevens coverage = {witting_coverage(10, 0.05, th):.3f}   (nominal 0.950)")
```

## Understand it

**Sterne / Blyth–Still–Casella.** For each hypothesised θ an *acceptance region* is a set of outcomes with
total probability ≥ 1 − α. Clopper–Pearson builds it from the two tails; **Sterne** instead collects the most
probable outcomes first, which is the *smallest* such set. The interval is every θ whose acceptance region contains the
observed x. Because the regions have minimal size, the intervals are shortest on average (`sterne` and `bsc` have
the same total length at n = 20 — see the cell below — and both are about 6% shorter than Clopper–Pearson); the
construction is computed exactly (Dümbgen 2021), with no grid.

```{code-cell} python
s = bk.ci(n=20, alpha=0.05, method="sterne"); cp = bk.ci(n=20, alpha=0.05, method="exact")
print("Dümbgen's published example n=20, x=5: (0.104, 0.475)  ->  ours", tuple(s.iloc[5][["LSTE", "USTE"]].astype(float).round(3)))
print("total length  Sterne", round(float((s.USTE - s.LSTE).sum()), 4), " Clopper–Pearson", round(float((cp.UEX - cp.LEX).sum()), 4))
```

**OLC.** A {term}`locally correct` interval has average coverage ≥ 1 − α/2 over every {term}`coverage cycle`.
Garthwaite et al. solve, from the top down, $\frac{1}{u_i-u_{i-1}}\int_{u_{i-1}}^{u_i}P(X\ge i\mid p)\,dp=1-\alpha/2$
and mirror it for the lower tail. The integral has a closed form in incomplete beta functions, so each limit is one scalar
root. **All 540 limits of the paper's published tables (n = 1…30, 95% and 99%) are reproduced to 5·10⁻⁵.**

**Coverage adjustment.** Clopper–Pearson at level α′ ≥ α has mean coverage
$C(\alpha')=\sum_x \mathrm{BB}(x)\,[I_{U_x}-I_{L_x}]$ under a Beta weight (BB = beta-binomial pmf, $I$ = regularised
incomplete beta); α′ solves $C(\alpha')=1-\alpha$. With a *posterior* weight α′ is found per observed x.

:::{admonition} A published table is not an oracle for its own rounding
:class: note
Thulin's Table 1 lists α′ for the uniform-prior correction. Integrating his definition numerically shows **our**
α′ gives mean coverage 0.95000000, whereas the printed values give 0.95008–0.95010: the table was produced with
a ~1e-4 bisection tolerance. We assert agreement with the table to 4e-4 *and* exactness against the definition.
:::

**Concentration intervals** invert a non-asymptotic tail bound (Hoeffding, Chernoff-KL, Bernstein, empirical Bernstein), so
their coverage is ≥ 1 − α at every n and θ — useful for machine-learning and safety-critical work where "about 95%" is
not enough. They are {term}`conservative`: the {doc}`betting intervals <betting>` are the variance-adaptive way to be tighter.

## References

Sterne (1954), *Biometrika* 41 · Dümbgen (2021), arXiv:2111.12937 · Casella (1986), *Canad. J. Statist.* 14 ·
Blyth & Still (1983), *JASA* 78 · Garthwaite, Moustafa & Elfadaly (2024), *Scand. J. Statist.* 51 ·
Thulin (2014), *Scand. J. Statist.* 41 · Witting (1985); Stevens (1950), *Biometrika* 37 · Hoeffding (1963) ·
Maurer & Pontil (2009), COLT.
