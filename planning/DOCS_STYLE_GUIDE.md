# binomcikit Documentation — Authoring & Style Guide

**Goal: the finished docs should read like a *book* that teaches binomial-proportion inference from
zero to research level — not a reference manual.** A curious beginner should be able to start at page
one and, chapter by chapter, understand *what* every method does, *why* it is built that way, and *how*
to use it — with worked examples they can run and self-check quizzes to test themselves.

This guide is the **single source of truth for how every docs page is written.** Pair it with
`planning/DOCS_CHECKLIST.md` (status, backlog, build/preview commands). If the two ever disagree, this
guide wins on *style*, the checklist wins on *what to build next*.

---

## 1. Voice & audience

- **Primary reader:** a numerate person who has *not* studied probability. Assume curiosity and
  arithmetic, nothing more. Never assume prior stats knowledge without a link to where it's explained.
- **Secondary reader:** a practitioner who wants the formula, the trade-offs, and the API fast.
  Serve them with **progressive disclosure** (see §3) — they skim the top and open the dropdowns.
- **Voice:** plain, warm, direct. Short sentences. Active voice. Explain, don't lecture. It's fine to
  say "this is the honest weakness" or "this is the whole point." Never hand-wave — if you state a
  number, it should be reproducible.
- **British spelling** to match the existing pages (*visualise, stabilising, behaviour*).

---

## 2. The book's structure (the table of contents we are building toward)

The five sidebar groups map to the book's parts. Every new page belongs to exactly one.

| Part (sidebar group) | What it is | Page type (§4) |
|---|---|---|
| **Start here** | install; **Foundations** — probability from zero | Concept pages |
| **Guides** | choosing a method; evaluating intervals; the Bayesian toolbox; the access layer; **Tutorials**; **Cookbook** | Tutorials, Cookbook, Concept |
| **Methods** | one page per interval | Method pages |
| **The maths** | *Methods & Mathematics* — the deep "why" | Theory deep-dives |
| **Reference** | API, glossary, migrating from R | (generated / glossary) |

New groups to add as content grows: a **Tutorials** and a **Cookbook** toctree group in `index.md`.

---

## 3. Universal conventions (apply to *every* page)

1. **Progressive disclosure — always intuition first.** Plain words → symbols defined → formula →
   `:::{dropdown}` derivation. The top of the page is readable with zero maths.
2. **Link every technical term to the glossary** with `` {term}`name` `` on first use on the page. If the
   term isn't in `docs/glossary.md`, **add it** (plain definition + tiny example, cross-linked).
3. **Examples are executed, not typed.** Use MyST-NB `` ```{code-cell} python `` blocks so the numbers
   are computed from the real package at build time and can never drift. Seed anything stochastic. (See
   `DOCS_CHECKLIST.md` §4 for the required front matter.) Plain `` ```python `` = a static, non-run snippet.
4. **Figures** where they clarify — generate a PNG with the plot engine and embed via `{figure}` with a
   caption that says *what to look at*. Don't plot inside code-cells (plotting libs aren't in the doc env).
5. **Every page cross-links:** "New here? → Foundations", "Deeper maths → the relevant Theory page",
   and sibling links. No dead ends.
6. **End matter:** a "Terms used on this page" `:::{admonition}` box, and — for concept/theory/tutorial
   pages — a **Check yourself** quiz (§5).
7. **Build gate:** a page isn't done until `sphinx -b html -W` is clean *and* it's been eyeballed in the
   live preview.

---

## 4. Page types and their templates

There are five page types. Each has a required skeleton (copy-paste versions in §6).

### A. Concept page — **the per-topic template** ★
Every **term / idea** (coverage, a confidence interval, the binomial, p-confidence, a prior, …) is
taught with these five parts, **in this order**:

1. **In words** — a plain-English explanation with a concrete mental picture. No symbols yet.
2. **The symbols** — a table naming every symbol used, in plain language, *before* they appear in a
   formula.
   ```
   | Symbol | Reads as | Means |
   |---|---|---|
   | $\theta$ | "theta" | the true, unknown success rate |
   | $\hat p$ | "p-hat" | the observed proportion, x/n |
   ```
3. **The definition (with the symbols)** — the formal statement/formula in a `$$…$$` block, then one
   line unpacking each symbol (link each to the glossary).
4. **Examples — 2 or 3, varied.** Different regimes so the idea is seen from several angles (e.g. a
   middling case, a boundary case, a large-*n* case). **Prefer executed `{code-cell}` examples** that
   compute and show the result; at least one should be hand-checkable by the reader.
5. **Check yourself** — a short quiz (2–4 questions) with each answer hidden in a `{dropdown}` (§5).

> A concept page can be short. The point is that *every* new idea gets all five parts — words, symbols,
> definition, varied examples, quiz — so nothing is introduced without being pinned down and tested.

### B. Method page (one per interval)
Keep the established **two cores**, enriched:
- **Use it** — import & call; a params table (plain + formal); the return schema; a worked example
  (executed); recipes (`plot_ci`, `compare`, adjusted/CC variants); gotchas.
- **Understand it** — *In words* → *The symbols* → *The formula* (each symbol a `{term}` link) →
  `:::{dropdown}` derivation → *When it works / fails* (with a coverage figure) → *Relatives* →
  references. Then a **Check yourself** quiz and the "Terms used" box.
- The method page's *Understand it* should embed the concept template (§A) for its central new idea.

### C. Theory deep-dive (*Methods & Mathematics*)
A chapter, not a snippet. Intuition → the maths built up step by step → an *executed* n = 5 worked
example → a figure → how it connects to the methods → **Check yourself** → references. Model page:
`docs/theory/02_normal_approximation.md`.

### D. Tutorial (task-oriented, narrative)
A single realistic scenario, start to finish. **Structure:** the situation & the data → the question →
choosing a method (with reasoning) → running it (executed) → **reading the output** in plain words →
a figure → **how to report it** → "what could go wrong". Warm, second-person ("suppose you ran…").
Each tutorial ends with a **Try it yourself** variation (a mini exercise + dropdown solution).

### E. Cookbook recipe (short, copy-paste)
One task, one answer, minimal prose. **Structure:** *Problem* (one line) → *Recipe* (an executed code
block) → *Result* (what it means, 1–2 sentences) → *See also* links. A cookbook page collects many such
recipes. No quiz needed.

---

## 5. Quiz mechanics — "Check yourself"

Every concept, theory, and tutorial page ends with a self-check. Use **colon-fenced** dropdowns
(`:::{dropdown}`), not backtick ones — a hidden answer will often contain a ```` ```python ```` block,
and a backtick dropdown wrapping a backtick code block closes early and breaks the build. Colon and
backtick fences nest cleanly.

````markdown
## Check yourself

**Q1.** You observe 0 successes in 20 trials. What does the Wald interval give, and why is that a problem?

:::{dropdown} Show answer
`[0, 0]` — a {term}`zero-width interval`. The standard error √(p̂q̂/n) is 0 when p̂ = 0, so the interval
collapses to a point and claims perfect certainty from data that is perfectly consistent with θ ≈ 0.1.
:::

**Q2.** For n = 40, x = 10, compute p̂ by hand, then check it.

:::{dropdown} Show answer
p̂ = 10/40 = **0.25**.
```python
bk.point_estimate(10, 40, "mle")   # -> 0.25
```
:::
````

Quiz-writing rules:
- 2–4 questions, escalating: one recall, one "compute it", one "why / interpret".
- At least one question should be **checkable with a `{code-cell}`** the reader can run.
- Answers are complete (a full sentence + the number), not just "0.25".
- Keep them honest and useful — a quiz tests understanding, it is not decoration.

---

## 6. Copy-paste skeletons

### Concept page skeleton
````markdown
# <Concept name>

## In words
<plain-English explanation with a concrete picture — no symbols>

## The symbols
| Symbol | Reads as | Means |
|---|---|---|
| $\theta$ | theta | <plain meaning, link to {term}> |

## Definition
$$ <formula> $$
where <unpack each symbol, each a {term} link>.

## Examples
```{code-cell} python
import binomcikit as bk
<example 1 — a middling case>
```
```{code-cell} python
<example 2 — a boundary / contrasting case>
```
<optional example 3 — a large-n or different-alpha case>

## Check yourself
**Q1.** …
```{dropdown} Show answer
…
```

:::{admonition} Terms used on this page
:class: seealso
{term}`…` · {term}`…`
:::
````

### Tutorial skeleton
````markdown
# <Task, phrased as a goal>

**The situation.** <scenario + the data>

**The question.** <what we want to know>

## Choosing a method
<reasoning + the pick, link to Choosing a method>

## Running it
```{code-cell} python
import binomcikit as bk
<the analysis>
```

## Reading the result
<plain-English interpretation of the numbers>

## How to report it
> <a sentence you could paste into a report>

## Try it yourself
<a variation to attempt>
```{dropdown} Solution
<worked>
```
````

(Executable pages also need the `jupytext`+`kernelspec` front matter — `DOCS_CHECKLIST.md` §4.)

---

## 7. A fully worked example of the concept template — "Coverage"

This is the standard to match. Note all five parts.

> ### In words
> When we say an interval is "95%", we are **not** saying "there's a 95% chance the truth is in *this*
> interval." We're describing the *procedure*: if you repeated the whole experiment many times, about
> 95% of the intervals it produces would contain the true rate. **Coverage** is the actual fraction
> that do. A good method's coverage stays close to the 95% it promises; a bad one's drifts below it.
>
> ### The symbols
> | Symbol | Reads as | Means |
> |---|---|---|
> | $\theta$ | theta | the true success rate (fixed, unknown) |
> | $[L(x), U(x)]$ | "L to U" | the interval the method returns for count $x$ |
> | $1-\alpha$ | one minus alpha | the *nominal* (promised) level, e.g. 0.95 |
>
> ### Definition
> $$ \text{Coverage}(\theta) \;=\; \sum_{x=0}^{n} \mathbf{1}\!\left[L(x) \le \theta \le U(x)\right]\; \binom{n}{x}\theta^{x}(1-\theta)^{n-x}. $$
> For each possible count $x$, check whether the interval $[L(x),U(x)]$ traps $\theta$; weight by how
> likely that $x$ is under $\theta$; add up. A method *achieves nominal coverage* if this is ≥ $1-\alpha$.
>
> ### Examples
> ```{code-cell} python
> import binomcikit as bk
> bk.covpwd(20, 0.05, a=1, b=1, t1=0.93, t2=0.97, seed=0)[["mcp", "micp"]]  # Wald: mean & min coverage
> ```
> ```{code-cell} python
> bk.coverage_curve(20, method="wilson")["coverage"].agg(["mean", "min"]).round(3)  # Wilson holds up better
> ```
>
> ### Check yourself
> **Q1.** A method reports mean coverage 0.998 at n = 20. Is that good?
> ```{dropdown} Show answer
> Not necessarily — it's *over*-covering. Coverage far above nominal means the intervals are wider than
> they need to be (conservative), like Clopper–Pearson. The ideal is *close to* 0.95, not far above.
> ```

---

## 8. Quality bar (a page is "book quality" when…)
- A total beginner understands the **In words** section with zero maths.
- Every symbol is defined **before** it appears in a formula.
- There are **2–3 varied, executed examples**, at least one hand-checkable.
- There is a **Check yourself** quiz with hidden, complete answers.
- Every technical term links to the glossary; every "see also" resolves.
- `-W` build is clean and it's been viewed in the live preview.

When in doubt, ask: *would this belong in a well-written textbook chapter?* If not, deepen it.
