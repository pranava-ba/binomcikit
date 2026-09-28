---
name: binomcikit-access-layer-docs
description: >-
  Use when adding, changing, or documenting a binomcikit access-layer function
  (a user-facing helper in src/binomcikit/access.py — e.g. pvalue/reject,
  sample_size/power, compare, recommend — that is a convenience built ON TOP of
  the CI engine, not itself a new confidence-interval method). Signals: "add a
  helper to access.py", "document pvalue/sample_size/power", "new access-layer
  function", working in access.py or docs/access_layer.md.
---

# binomcikit — document an access-layer function

Access-layer functions (`access.py`) are a *different* documentation shape
from CI methods: no coverage figure, no dedicated `docs/methods/<x>.md` page,
no `docs/method_selection.md` row — they get a **section inside
`docs/access_layer.md`**. Confusing the two shapes is the main failure mode:
copying `docs/methods/wald.md`'s structure here produces a page nobody links
to and a figure the function doesn't need.

**REQUIRED BACKGROUND:** if this function IS a new CI method (produces
`(lower, upper)` limits for an x), use `binomcikit-subphase` instead — this
skill is only for helpers built on top of existing methods.

## 1. Where it goes
Add a new `## <Verb-ish heading> — \`func_a\`, \`func_b\`` section to
`docs/access_layer.md`, after the existing sections, before the final
"Terms used on this page" admonition. Don't create a new file.

## 2. The section shape (copy this, not a method page)
Look at the `pvalue`/`reject` or `sample_size`/`power` sections in
`docs/access_layer.md` for a live example. The recipe:

1. **If genuinely new vs. R `proportion`** (true for most access-layer
   additions — R has no equivalent usability layer), open with:
   ```
   :::{admonition} New in binomcikit
   :class: important
   **Not part of R `proportion`.** <why R doesn't have this — cite the paper's
   own stated scope/rationale if `planning/ROADMAP.md` §3.5 gives one>.
   :::
   ```
2. One line in italics framing the question the function answers ("*Is
   `theta0` a plausible value...*"), then a runnable code block with 2-4 calls
   showing realistic inputs and their actual output values (run the code,
   don't guess numbers — wrong numbers in docs are worse than none).
3. A short prose paragraph explaining the mechanism in plain terms and any
   guarantee it has (e.g. "guaranteed by construction to agree with `bk.ci`").
4. **One `:::{admonition}` per genuinely surprising behavior**, `:class:
   warning` for a real gotcha, `:class: note` for an expected-but-non-obvious
   design choice (e.g. deliberately not matching some other library's
   convention). Skip this if there's nothing surprising — don't manufacture
   one.
5. If the function excludes some methods (e.g. the bootstrap family — most
   access-layer functions that search over `alpha` or `n` do, since a
   stochastic CI has no well-defined single answer to search against), say so
   and say why in one sentence.

## 3. Glossary + footer
- Add any new technical term to `docs/glossary.md` (same `:::{glossary}`
  block, plain-language definition, tiny example, cross-linked with `{term}`).
- Extend the page's final `Terms used on this page` admonition with the new
  terms — don't leave a second, separate footer.

## 4. Also touch
- `README.md`'s "🧰 Access layer" `<details>` block — one bullet.
- `src/binomcikit/__init__.py` — add to both the `from .access import (...)`
  block and the `_ACCESS` list (alphabetical within each).
- If it changes the total interval-method count claim ("Thirteen confidence-
  interval methods..."), it doesn't — access-layer functions aren't methods,
  don't touch that count.

## 5. Verify
```bash
cd docs && PYTHONPATH=../src python -m sphinx -b html . _build/x -W && cd .. && rm -rf docs/_build/x
```
Clean `-W` build (undefined `{term}` links and broken refs are hard errors).
Re-read the rendered admonitions once — a warning/note box that states the
obvious reads as noise; delete it rather than keep it for the checklist.

## Common mistakes
- Writing a `docs/methods/<name>.md` page for something that isn't a CI
  method — wrong shape, orphaned page.
- Hand-typing example output instead of running the code — this package's
  whole ethos is verified numbers; don't be the first unverified one.
- An admonition box for something not actually surprising (dilutes the ones
  that matter).
