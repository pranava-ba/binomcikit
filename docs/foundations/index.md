# Foundations — start here (no maths required)

**What you'll learn:** enough to follow every other page in these docs — what a
proportion is, what a confidence interval really means, and why there are so many
methods. **What you need to know first:** nothing. If a word looks technical, it is a
link — click it to jump to the {doc}`../glossary`.

:::{note}
New to statistics? Read this page top to bottom, then go to the Wald method page, and
follow the guided path from there.
:::

## 1. What are we even measuring?

Suppose you flip a coin 10 times and see 6 heads. The **{term}`proportion`** of heads
is 6/10 = 0.6. But you don't really care about *this* handful of flips — you care about
the coin's *true* tendency to land heads, a number we call **{term}`theta`** (theta).
We can never see θ directly; we can only *estimate* it from data.

Each flip is a **{term}`trial`** with two outcomes, a **{term}`Bernoulli trial`**.
Counting the **{term}`success`es** across *n* trials gives a **{term}`binomial`** count.

## 2. Why a single number isn't enough

The observed proportion p̂ = x/n is an **{term}`estimate`**, but it is almost never
*exactly* θ. With only 10 flips, 6 heads is very compatible with a fair coin (θ = 0.5)
*and* with a biased one (θ = 0.65). So instead of one number we report a **range** of
plausible values: a **{term}`confidence interval`**.

## 3. What "95% confidence" actually means

A 95% confidence interval is not "θ is 95% likely to be in here." It is a *recipe*: if
you repeated the whole experiment many times and built an interval each time, about 95%
of those intervals would contain the true θ. That 95% is the **{term}`confidence level`**
(= 1 − **{term}`alpha`**). How often a recipe *actually* hits that target is its
**{term}`coverage`** — and, surprisingly, many popular recipes miss it.

## 4. Why there are so many methods

Different recipes trade off two things:
- **{term}`coverage`** — does it trap θ as often as advertised?
- **{term}`expected length`** — how wide (and therefore how useful) is it?

No single method wins on both for every *n* and θ, especially for small samples or when
θ is near 0 or 1. That tension is the whole subject — and this package lets you *measure*
it, not just take a method on faith.

## 5. Two ways of thinking (frequentist vs Bayesian)

Most methods here treat θ as a fixed unknown and ask "what values are compatible with my
data?" The **{term}`Bayesian`** methods instead start from a **{term}`prior`** belief and
update it with data into a **{term}`posterior`**. Both are supported; both are explained.

---

## How these docs are organised

Every method and every metric has **two pages**, so you can pick the depth you need:

- **Use it** — how to call the function: the signature, each argument in plain and formal
  terms, what comes back, and copy-pasteable examples.
- **Understand it** — the idea first (a coin-flip story), then the formula with *every
  symbol defined*, where it comes from, when it works, and when it fails.

Supporting these:
- the {doc}`../glossary` defines **every** technical word and is linked everywhere;
- collapsible "for the curious" boxes hold the heavier maths, so beginners can skip them
  and experts can expand them;
- worked examples use numbers small enough to check by hand.

*Prerequisites: none. Everything builds from this page.*
