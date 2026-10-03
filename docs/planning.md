---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Planning: sample size, width and power

Everything you would reach for **PASS (NCSS)** or **SAS `PROC POWER`** to do for a *single* proportion — written
from their published documentation and checked against their published numbers. All of it works for **every** interval
method in binomcikit, not just the five or six the commercial tools offer.

| Question | Function | Commercial equivalent |
|---|---|---|
| How many subjects for a CI of a given width? | `bk.sample_size(width, p0=…, plug_in="continuous")` | PASS Ch. 115 · SAS `HALFWIDTH` |
| …with one-sided *distance*, dropout? | `sides="upper"/"lower"`, `dropout=`, `details=True` | PASS |
| How likely is a trial of n to hit that width? | `bk.prob_width(n, p, halfwidth, method=…)` | SAS `PROBWIDTH` |
| How many to be **assured** of the width? | `bk.sample_size_assurance(halfwidth, assurance, p)` | — |
| Average width at a true p? | `bk.expected_width(n, p)` | `binGroup::binWidth` |
| Power / n for an exact or z test? | `bk.power_test`, `bk.sample_size_test` | SAS `ONESAMPLEFREQ TEST=EXACT/Z/ADJZ` |
| Equivalence (TOST)? | `bk.power_equivalence`, `bk.sample_size_equivalence` | SAS `TEST=EQUIV_*` |
| Zero-failure / success-run plan? | `bk.sample_size_upper_bound(p_max, confidence, failures)` | reliability / ISO 2859-type plans |
| Bayesian sample size? | `bk.sample_size_bayes(length, "alc" / "woc")` | Joseph–Wolfson–du Berger |

## Sample size for a confidence interval — and a convention that matters

PASS plans at a **real-valued** plug-in proportion ($x=P\,n$ need not be an integer). The original `sample_size`
rounded $x$ to a whole number, which is a slightly different plan; `plug_in="continuous"` reproduces PASS exactly.
Here is PASS Chapter 115, Example 1 (exact Clopper–Pearson, 95%, two-sided) — every one of the **15** published sample sizes
reproduced:

```{code-cell} python
import binomcikit as bk

pass_published = {  # (target width, planned proportion) -> N, as printed by PASS
    (0.04, 0.1): 914, (0.04, 0.2): 1585, (0.04, 0.3): 2065, (0.04, 0.4): 2353, (0.04, 0.5): 2449,
    (0.06, 0.1): 417, (0.06, 0.2): 715,  (0.06, 0.3): 928,  (0.06, 0.4): 1056, (0.06, 0.5): 1098,
    (0.10, 0.1): 158, (0.10, 0.2): 264,  (0.10, 0.3): 341,  (0.10, 0.4): 387,  (0.10, 0.5): 402,
}
rows = []
for (w, p), n_pass in pass_published.items():
    rows.append({
        "width": w, "p": p, "PASS": n_pass,
        "binomcikit (continuous)": bk.sample_size(w, 0.05, p, method="exact", plug_in="continuous"),
        "binomcikit (rounded x)": bk.sample_size(w, 0.05, p, method="exact", plug_in="nearest"),
    })
import pandas as pd
df = pd.DataFrame(rows)
print("continuous matches PASS:", (df.PASS == df["binomcikit (continuous)"]).sum(), "of", len(df),
      "|  rounded-x matches:", (df.PASS == df["binomcikit (rounded x)"]).sum(), "of", len(df))
df.head(6)
```

The printed limits and the dropout-inflated enrolment match too:

```{code-cell} python
bk.sample_size(0.04, 0.05, 0.1, method="exact", plug_in="continuous", details=True, dropout=0.20)
```

PASS prints `0.081 – 0.121` and an enrolment of 1 143 for a 20% dropout.

## How likely is it to work? (`prob_width`, assurance)

Planning at a plug-in proportion says the width is met *if* the data come out at $p$. They will not. `prob_width` is the exact
probability — summed over every possible $x$ — that your realised interval has half-width at most the target:

```{code-cell} python
n_plug = bk.sample_size(0.10, 0.05, 0.3, method="wilson", plug_in="continuous")   # full width 0.10 => half-width 0.05
print("plug-in plan: n =", n_plug)
print("probability a trial of that size actually achieves half-width 0.05:",
      round(bk.prob_width(n_plug, 0.3, 0.05, method="wilson"), 3))

n_assured = bk.sample_size_assurance(0.05, assurance=0.90, p=0.3, method="wilson")
print("n that makes it 90% likely:", n_assured,
      " -> probability", round(bk.prob_width(n_assured, 0.3, 0.05, method="wilson"), 3))
```

The probability **saw-tooths** in $n$ (a discrete interval changes in jumps), so the search returns the *smallest* $n$ that
reaches the target — SAS's convention; `lookahead=k` additionally demands it hold for the next $k$ sizes.

## Power and sample size of a test

The **exact test** uses SAS's critical values — each tail filled with as much probability as fits within $\alpha/2$ — which is exactly
inverting the Clopper–Pearson interval, so `power_test` and the CI-duality `power` agree to 15 digits:

```{code-cell} python
print("exact-test power  :", round(bk.power_test(50, 0.5, 0.7), 6))
print("via CI duality    :", round(bk.power(50, 0.5, 0.7, method="exact"), 6))
print("n for 80% power   :", bk.sample_size_test(0.80, 0.5, 0.7))
print("z test (enumerated)  :", round(bk.power_test(50, 0.5, 0.7, test="z"), 4))
print("z test (SAS normal formula):", round(bk.power_test(50, 0.5, 0.7, test="z", method="normal"), 4))
```

For a non-inferiority or superiority margin $\delta$, test against the shifted null: `null = p0 - delta` (or `p0 + delta`) with
`alternative="greater"`.

### Equivalence (TOST)

```{code-cell} python
print("TOST (exact) power, n=100, margins [0.4, 0.6], truth 0.5:", round(bk.power_equivalence(100, 0.4, 0.6, 0.5), 3))
print("n for 80% power:", bk.sample_size_equivalence(0.80, 0.4, 0.6, 0.5))
```

## Zero-failure plans (reliability, medical-device verification, acceptance sampling)

*How many items must I test, with no more than `f` failures, to prove the defect rate is below $p$ at confidence $C$?*

```{code-cell} python
for p, c in [(0.01, 0.95), (0.001, 0.95), (0.05, 0.90)]:
    print(f"p < {p:<6} at {int(c*100)}% confidence, 0 failures: n = {bk.sample_size_upper_bound(p, c)}"
          f"   (rule of three: {3/p:.0f})")
print("allowing 1 failure at p<0.05, 90%:", bk.sample_size_upper_bound(0.05, 0.90, failures=1))
```

## Bayesian sample size

With a Beta prior the data are beta-binomial *before* you see them, so you can ask for the **average length** ({term}`average length criterion`, ALC) or the
**worst-outcome** length (WOC) of the credible interval to meet a target. An informative prior buys fewer trials:

```{code-cell} python
print("flat prior          ALC n:", bk.sample_size_bayes(0.12, "alc", 1.0, 1.0))
print("prior near 10%      ALC n:", bk.sample_size_bayes(0.12, "alc", 2.0, 18.0))
print("flat prior          WOC n:", bk.sample_size_bayes(0.12, "woc", 1.0, 1.0))
```

## Understand it

* **Why "continuous"?** PASS substitutes $\hat p=P$ directly into the interval formula; the exact interval then uses the beta
  quantiles with the real-valued shape $r=Pn$. Rounding $r$ changes the width by a few trials' worth — that is the whole 7-of-15
  discrepancy the original `sample_size` had.
* **One-sided intervals** use $\alpha$ rather than $\alpha/2$ and a *distance* ($U-\hat p$ or $\hat p-L$) instead of a width.
* **Discreteness.** Power of an exact test is not monotone in $n$: adding a trial can *lose* power because a critical value jumps. Every
  search here returns the first $n$ that attains the target; read the neighbours before committing (`lookahead=`).
* **SAS's TOST formula** writes $z_\alpha$ for the *negative* $\alpha$-quantile; with the usual positive $z_{1-\alpha}$ the sign flips.

## References

NCSS PASS, *Chapter 115: Confidence Intervals for One Proportion* · SAS/STAT, *The POWER Procedure* (ONESAMPLEFREQ) ·
Newcombe (1998), *Stat. Med.* 17 · Joseph, Wolfson & du Berger (1995), *Stat. Med.* 14 · Garthwaite et al. (2024).
