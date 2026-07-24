"""Tests for the high-level ``ci()`` dispatcher — it must delegate to exactly the
underlying ``ci*`` function, so results are identical."""

import pytest

import binomcikit as bk


def test_dispatch_base_all_x():
    assert bk.ci(n=10, method="wald").equals(bk.ciwd(10, 0.05))
    assert bk.ci(n=10, method="wilson").equals(bk.cisc(10, 0.05))
    assert bk.ci(n=10, method="score").equals(bk.cisc(10, 0.05))
    assert bk.ci(n=10, method="arcsine").equals(bk.cias(10, 0.05))
    assert bk.ci(n=10, method="logit").equals(bk.cilt(10, 0.05))
    assert bk.ci(n=10, method="waldt").equals(bk.citw(10, 0.05))
    assert bk.ci(n=10, method="lr").equals(bk.cilr(10, 0.05))


def test_dispatch_given_x():
    assert bk.ci(3, n=10, method="wald").equals(bk.ciwdx(3, 10, 0.05))
    assert bk.ci(3, n=10, method="wilson").equals(bk.ciscx(3, 10, 0.05))


def test_dispatch_adjusted_and_cc():
    assert bk.ci(n=10, method="wald", h=2).equals(bk.ciawd(10, 0.05, 2))
    assert bk.ci(n=10, method="wald", c=0.5).equals(bk.cicwd(10, 0.05, 0.5))
    assert bk.ci(2, n=10, method="score", h=1).equals(bk.ciascx(2, 10, 0.05, 1))


def test_dispatch_exact_and_bayes():
    assert bk.ci(n=10, method="exact").equals(bk.ciex(10, 0.05, [1.0]))
    assert bk.ci(n=10, method="cp").equals(bk.ciex(10, 0.05, [1.0]))
    assert bk.ci(n=10, method="midp").equals(bk.ciex(10, 0.05, [0.5]))
    assert bk.ci(n=10, method="exact", e=0.5).equals(bk.ciex(10, 0.05, [0.5]))
    assert bk.ci(n=10, method="bayes").equals(bk.ciba(10, 0.05, 1, 1))
    assert bk.ci(n=10, method="jeffreys").equals(bk.ciba(10, 0.05, 0.5, 0.5))


def test_dispatch_agresti_coull():
    from scipy.stats import norm

    h = norm.ppf(1 - 0.05 / 2) ** 2 / 2
    assert bk.ci(n=10, method="agresti-coull").equals(bk.ciawd(10, 0.05, h))


def test_dispatch_errors():
    with pytest.raises(ValueError):
        bk.ci(n=10, method="nope")
    with pytest.raises(ValueError):
        bk.ci(n=10, method="exact", h=2)  # exact has no adjusted variant
    with pytest.raises(ValueError):
        bk.ci(n=10, method="lr", c=0.5)  # LR has no CC variant
    with pytest.raises(ValueError):
        bk.ci(method="wald")  # n is required
