import numpy as np
import pytest

from gobahar.timeseries import fit_linear_trend


def test_unsorted_known_slope_preserves_units_sign_and_intercept():
    trend = fit_linear_trend(["2020-01-11", "2020-01-01", "2020-01-06"], [-15, 5, -5])
    assert trend.origin == "2020-01-01T00:00:00+00:00"
    assert trend.intercept == pytest.approx(5)
    assert trend.slope_per_day == pytest.approx(-2)
    assert trend.rate_per_year == pytest.approx(-730.5)
    assert trend.r_squared == pytest.approx(1)
    assert trend.observations == 3


def test_subdaily_timestamps_and_explicit_year_convention():
    trend = fit_linear_trend(["2020-01-01T00:00Z", "2020-01-01T12:00Z"], [0, 1], days_per_year=365)
    assert trend.slope_per_day == pytest.approx(2)
    assert trend.rate_per_year == pytest.approx(730)


def test_constant_series_is_an_exact_fit():
    trend = fit_linear_trend(["2020-01-01", "2020-01-02"], [7, 7])
    assert trend.rate_per_year == 0
    assert trend.r_squared == 1


def test_repeated_dates_with_distinct_timestamps_are_observations():
    trend = fit_linear_trend(["2020-01-01", "2020-01-01", "2020-01-02"], [0, 0, 2])
    assert trend.observations == 3
    assert trend.slope_per_day == pytest.approx(2)


@pytest.mark.parametrize(
    "dates,values",
    [
        (["2020-01-01"], [1]),
        (["2020-01-01", "2020-01-02"], [1, np.nan]),
        (["2020-01-01", "2020-01-02"], [1, np.inf]),
        (["2020-01-01", "2020-01-02"], [[1], [2]]),
        (["2020-01-01"], [1, 2]),
        (["2020-01-01", None], [1, 2]),
        (["2020-01-01", "invalid"], [1, 2]),
        (["2020-01-01", "2020-01-01"], [1, 2]),
    ],
)
def test_invalid_or_degenerate_series_raises(dates, values):
    with pytest.raises(ValueError):
        fit_linear_trend(dates, values)


@pytest.mark.parametrize("days", [0, -365, np.nan, np.inf])
def test_invalid_year_convention_raises(days):
    with pytest.raises(ValueError, match="days_per_year"):
        fit_linear_trend(["2020-01-01", "2020-01-02"], [1, 2], days_per_year=days)
