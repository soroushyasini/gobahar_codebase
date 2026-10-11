"""Validated ordinary least-squares trends for dated observations."""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class LinearTrend:
    """Slope units follow the input values; the intercept is at the time origin."""

    origin: str
    intercept: float
    slope_per_day: float
    rate_per_year: float
    r_squared: float
    observations: int
    days_per_year: float


def fit_linear_trend(
    dates: Sequence,
    values: Sequence[float],
    *,
    days_per_year: float = 365.25,
) -> LinearTrend:
    """Fit finite observations against elapsed UTC days from the earliest date.

    Gregorian dates are parsed explicitly; convert Jalali dates before calling.
    Missing values/dates raise. Repeated dates count as repeated observations but
    at least two distinct timestamps are required. No unit, LOS/vertical, baseline,
    or sign conversion is applied. The 365.25-day year is a reporting convention.
    This descriptive trend does not establish causation or statistical significance.
    """
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or len(y) < 2 or not np.isfinite(y).all():
        raise ValueError("Provide at least two finite scalar observations.")
    timestamps = pd.DatetimeIndex(pd.to_datetime(dates, utc=True, errors="raise", format="mixed"))
    if len(timestamps) != len(y) or timestamps.isna().any():
        raise ValueError("Dates must match the observations and contain no missing values.")
    if not np.isfinite(days_per_year) or days_per_year <= 0:
        raise ValueError("days_per_year must be finite and positive.")
    origin = timestamps.min()
    x = np.asarray((timestamps - origin).total_seconds(), dtype=float) / 86400.0
    centered_x = x - x.mean()
    denominator = float(centered_x @ centered_x)
    if denominator == 0:
        raise ValueError("At least two distinct timestamps are required.")
    centered_y = y - y.mean()
    slope = float(centered_x @ centered_y / denominator)
    intercept = float(y.mean() - slope * x.mean())
    residuals = y - (intercept + slope * x)
    total = float(centered_y @ centered_y)
    r_squared = 1.0 if total == 0 else 1.0 - float(residuals @ residuals) / total
    return LinearTrend(
        origin=origin.isoformat(),
        intercept=intercept,
        slope_per_day=slope,
        rate_per_year=slope * days_per_year,
        r_squared=r_squared,
        observations=len(y),
        days_per_year=days_per_year,
    )
