# Glossary

Every technical term used anywhere in these docs is defined here in plain language,
with a tiny example. Terms are hyperlinked throughout the site — click any linked
word to jump here. New terms are added as each method is documented.

:::{glossary}
proportion
  The fraction of {term}`trial`s that turn out to be "successes". Flip a coin 10
  times, get 6 heads → the observed proportion of heads is 6/10 = 0.6. We usually
  want the *true*, unknown proportion, which we call {term}`theta`.

trial
  One repetition of a yes/no experiment — a single coin flip, one patient either
  recovering or not, one manufactured part passing or failing.

Bernoulli trial
  A {term}`trial` with exactly two outcomes, conventionally "success" (1) and
  "failure" (0), where the chance of success is the same every time.

success
  The outcome we are counting. It need not be "good": for a defect rate, a
  "success" is a defective part. What matters is that we count it consistently.

binomial
  The pattern from adding up *n* independent {term}`Bernoulli trial`s: the number
  of successes *x* out of *n*. Written *X* ~ Binomial(*n*, {term}`theta`).

theta
  (θ) The true, unknown {term}`probability` of {term}`success` on one {term}`trial`
  — the number we are trying to estimate. Always between 0 and 1.

probability
  A number between 0 and 1 saying how likely something is: 0 = impossible,
  1 = certain, 0.5 = a fair coin's chance of heads.

random variable
  A quantity whose value depends on chance — e.g. *X*, the number of successes you
  will observe. Uncertain before the experiment, a fixed number after.

estimate
  A single best-guess value for an unknown quantity, computed from data — e.g. the
  observed proportion p̂ = x/n estimates {term}`theta`.

confidence interval
  A *range* of plausible values for {term}`theta`, instead of a single
  {term}`estimate`. A "95% confidence interval" comes from a recipe that, used
  over and over on fresh data, traps the true {term}`theta` about 95% of the time.

confidence level
  The advertised success rate of a {term}`confidence interval` recipe, e.g. 95%.
  Equal to 1 − {term}`alpha`.

alpha
  (α) The allowed error rate of a {term}`confidence interval`: α = 0.05 pairs with
  a 95% {term}`confidence level`. Smaller α → wider, safer intervals.

coverage
  How often a {term}`confidence interval` recipe *actually* traps the true
  {term}`theta`. Ideally this matches the {term}`confidence level`; measuring when
  it does not is a core purpose of this package.

expected length
  The average width (upper minus lower) of a {term}`confidence interval`. Narrower
  is more informative — but not if it costs {term}`coverage`.

quantile
  The value below which a given fraction of a distribution lies. The 0.975 quantile
  of the standard normal (≈ 1.96) is the multiplier behind most 95% intervals.

prior
  In {term}`Bayesian` methods, what you believed about {term}`theta` *before* seeing
  data, written as a distribution (often a {term}`Beta distribution`).

posterior
  Your updated belief about {term}`theta` *after* combining the {term}`prior` with
  the data, via Bayes' rule.

Bayesian
  An approach that treats the unknown {term}`theta` as itself uncertain, described by
  a {term}`prior` that data updates into a {term}`posterior`. The alternative,
  "frequentist", treats {term}`theta` as a fixed unknown constant.

Beta distribution
  A flexible distribution on values between 0 and 1, written Beta(a, b). It is the
  natural {term}`prior` for a {term}`proportion` because the {term}`posterior` is
  again a Beta — which keeps the maths clean.

continuity correction
  A small ± adjustment applied when approximating discrete {term}`binomial` counts by
  a smooth (normal) curve, to improve accuracy for small *n*.

standard error
  How much an {term}`estimate` typically wobbles from sample to sample. For a
  {term}`proportion` p̂ from *n* trials it is √(p̂(1−p̂)/n) — smaller for larger *n*.

critical value
  The {term}`quantile` of a reference curve (usually the normal) that sets how many
  {term}`standard error`s wide an interval reaches. For 95% it is ≈ 1.96.

maximum likelihood estimate
  (MLE) The parameter value that makes the observed data most probable. For a
  {term}`binomial`, the MLE of {term}`theta` is just the observed {term}`proportion` p̂ = x/n.

Agresti–Coull
  A simple repair of the **Wald** interval: add about two successes and two failures to the data
  before applying the Wald formula. It fixes most of Wald's {term}`coverage` problem.

zero-width interval
  (ZWI) A {term}`confidence interval` that has collapsed to a single point — it claims a certainty
  it does not have. Wald produces one at x = 0 and x = n.

aberration
  A confidence limit that behaves badly — e.g. running past a sensible boundary, or moving in the
  wrong direction. binomcikit reports these as the LABB / UABB flags.
:::

---

*This page holds the shared vocabulary; individual method pages add their own terms
and link back here. See the docs convention in {doc}`foundations/index`.*
