"""The access / usability layer: data input, point estimates, posteriors,
curve accessors, and the compare / recommend helpers."""

import pytest

import binomcikit as b


def test_from_data_and_from_counts():
    assert b.from_data([1, 0, 1, 1, 0]) == (3, 5)
    assert b.from_data([True, False, True]) == (2, 3)
    assert b.from_counts(3, 20) == (3, 20)
    with pytest.raises(ValueError):
        b.from_data([1, 2, 0])  # not 0/1
    with pytest.raises(ValueError):
        b.from_counts(21, 20)  # x > n


def test_point_estimate_variants():
    assert b.point_estimate(5, 20, "mle") == 0.25
    # a flat prior lifts x = 0 off zero; Jeffreys lifts it more than Laplace does not here
    assert b.point_estimate(0, 20, "mle") == 0.0
    assert b.point_estimate(0, 20, "laplace") == pytest.approx(1 / 22, abs=1e-9)
    # Agresti-Coull point estimate matches (x + z^2/2)/(n + z^2)
    z2 = 1.959963984540054**2
    assert b.point_estimate(3, 20, "ac") == pytest.approx((3 + z2 / 2) / (20 + z2), abs=1e-6)
    with pytest.raises(ValueError):
        b.point_estimate(3, 20, "nope")


def test_posterior_summary_and_intervals():
    post = b.posterior(3, 20, a=1, b=1)
    assert post["a_post"] == 4 and post["b_post"] == 18
    assert post["mean"] == pytest.approx(4 / 22, abs=1e-9)
    lo_h, hi_h = post["hpd_interval"]
    lo_q, hi_q = post["quantile_interval"]
    # HPD is the shortest credible interval => never wider than the quantile one
    assert (hi_h - lo_h) <= (hi_q - lo_q) + 1e-9
    assert b.prior("jeffreys") == (0.5, 0.5)


def test_coverage_and_length_curves():
    cc = b.coverage_curve(20, "wilson", points=150)
    assert list(cc.columns) == ["theta", "coverage"]
    assert len(cc) == 150 and cc["coverage"].between(0, 1).all()
    lc = b.length_curve(20, "wald", points=150)
    assert list(lc.columns) == ["theta", "expected_length"]
    assert (lc["expected_length"] >= 0).all()


def test_compare_orders_by_width_and_covers_all_methods():
    df = b.compare(3, 20)
    assert list(df.columns) == ["method", "lower", "upper", "width"]
    # sorted ascending by width
    assert df["width"].is_monotonic_increasing
    # every default method appears
    assert len(df) == 10
    assert (df["width"] >= 0).all()


def test_recommend_puts_an_adequate_method_first_by_length():
    df = b.recommend(20, by="length")
    assert "adequate" in df.columns
    # the top-ranked method by length must be one that is not badly under-covering
    assert bool(df.iloc[0]["adequate"]) is True
    # Wald / ArcSine are narrow but under-cover -> must NOT be the recommendation
    assert df.iloc[0]["method"] not in {"Wald", "ArcSine"}


def test_recommend_by_min_coverage_favours_exact():
    df = b.recommend(20, by="min_coverage")
    # an exact method (guaranteed coverage) should top the min-coverage ranking
    assert df.iloc[0]["method"] in {"Clopper-Pearson", "Blaker"}
    assert df.iloc[0]["min_coverage"] >= 1 - 0.05 - 1e-9


def test_ci_still_matches_manual_from_data_path():
    x, n = b.from_data([1, 0, 1, 1, 0, 0, 1, 0])
    assert b.ci(x, n=n, method="wilson").equals(b.ciscx(x, n, 0.05))
