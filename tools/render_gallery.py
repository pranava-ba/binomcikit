"""Render a curated set of binomcikit plots to PNGs for the docs gallery.

Run:  python tools/render_gallery.py
Writes to docs/_static/gallery/. The PNGs are committed so Read the Docs can
serve them without running the (heavy) plotting stack at build time.
"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")
os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import binomcikit as bk  # noqa: E402

OUT = os.path.join(ROOT, "docs", "_static", "gallery")
os.makedirs(OUT, exist_ok=True)

# (filename, callable, caption) — curated across all six families
PLOTS = [
    ("ci_all", lambda: bk.plotciall(20, 0.05),
     "Confidence intervals — all six base methods for x = 0..20"),
    ("ci_all_faceted", lambda: bk.plotciallg(20, 0.05),
     "The same, faceted by method"),
    ("ci_wald", lambda: bk.plotciwd(20, 0.05),
     "Wald intervals (a single method)"),
    ("ci_bayes", lambda: bk.plotciba(20, 0.05, 1, 1),
     "Bayesian credible intervals — quantile vs HPD"),
    ("ci_all_x", lambda: bk.plotciallx(7, 20, 0.05),
     "All methods for a single observed count, x = 7 of 20"),
    ("covp_all", lambda: bk.plotcovpall(15, 0.05, 1, 1, 0.9, 0.97, seed=0),
     "Coverage probability of all base methods against p"),
    ("covp_wald", lambda: bk.plotcovpwd(15, 0.05, 1, 1, 0.9, 0.97, seed=0),
     "Wald coverage vs the nominal 1 - alpha line"),
    ("covp_bayes", lambda: bk.plotcovpba(15, 0.05, 1, 1, 0.9, 0.97, 0.5, 0.5, seed=0),
     "Bayesian coverage — quantile and HPD intervals"),
    ("expl_all", lambda: bk.plotexplall(15, 0.05, 1, 1, seed=0),
     "Expected interval length of all base methods"),
    ("length_all", lambda: bk.plotlengthall(15, 0.05, 1, 1, seed=0),
     "Sum of interval lengths by method"),
    ("pconf_all", lambda: bk.plotpcopbiall(20, 0.05),
     "p-confidence and p-bias across methods"),
    ("err_all", lambda: bk.ploterrall(20, 0.05, 0.5, -2),
     "Error and long-term power by method, coloured by pass/fail"),
]


def main():
    captions = {}
    for name, make, caption in PLOTS:
        fig = make()
        fig.save(os.path.join(OUT, name + ".png"),
                 width=7, height=4.2, dpi=96, verbose=False)
        captions[name] = caption
        print("rendered", name + ".png")
    print(f"\n{len(PLOTS)} gallery images written to {OUT}")


if __name__ == "__main__":
    main()
