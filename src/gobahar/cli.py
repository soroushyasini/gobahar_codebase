"""Explicit file-based entry points for supported research operations."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from xml.etree.ElementTree import ParseError

import pandas as pd
from pyproj.exceptions import ProjError
from rasterio.errors import RasterioError

from gobahar.manifest import read_pass_direction
from gobahar.raster import sample_raster
from gobahar.timeseries import fit_linear_trend


def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path)
    raise ValueError("Input table must be .csv or .xlsx (first worksheet).")


def _sample(args: argparse.Namespace) -> None:
    table = _read_table(args.points)
    coordinates = table[[args.x_column, args.y_column]].to_numpy(dtype=float)
    names = [path.stem for path in args.raster]
    if len(set(names)) != len(names) or set(names).intersection(table.columns):
        raise ValueError("Raster stems must be unique and must not overwrite input columns.")
    for path in args.raster:
        table[path.stem] = sample_raster(
            path, coordinates, points_crs=args.points_crs, band=args.band
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects input files and historical results from replacement.
    with args.output.open("x", encoding="utf-8", newline="") as handle:
        table.to_csv(handle, index=False)
    print(f"Saved {len(table)} rows to {args.output}")


def _trend(args: argparse.Namespace) -> None:
    table = _read_table(args.input)
    trend = fit_linear_trend(
        table[args.date_column], table[args.value_column], days_per_year=args.days_per_year
    )
    print(json.dumps({**asdict(trend), "value_unit": args.unit}, indent=2, allow_nan=False))


def main(argv: list[str] | None = None) -> int:
    """Return a process status; invalid inputs produce concise stderr diagnostics."""
    parser = argparse.ArgumentParser(description="Golbahar geospatial research utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)
    sample = subparsers.add_parser("sample", help="Sample raster pixels at table coordinates")
    sample.add_argument("--points", required=True, type=Path)
    sample.add_argument("--x-column", required=True)
    sample.add_argument("--y-column", required=True)
    sample.add_argument("--points-crs", required=True, help="Authoritative CRS, e.g. EPSG:4326")
    sample.add_argument("--raster", nargs="+", type=Path, required=True)
    sample.add_argument("--band", type=int, default=1)
    sample.add_argument(
        "--output", required=True, type=Path, help="New CSV path; never overwritten"
    )
    trend = subparsers.add_parser("trend", help="Fit a dated series; keep its units and sign")
    trend.add_argument("--input", required=True, type=Path)
    trend.add_argument("--date-column", required=True)
    trend.add_argument("--value-column", required=True)
    trend.add_argument("--unit", required=True, help="Label for input units, e.g. mm")
    trend.add_argument("--days-per-year", type=float, default=365.25)
    direction = subparsers.add_parser("pass-direction", help="Read Sentinel-1 manifest pass")
    direction.add_argument("manifest", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "sample":
            _sample(args)
        elif args.command == "trend":
            _trend(args)
        else:
            print(read_pass_direction(args.manifest))
    except (OSError, ValueError, KeyError, ParseError, ProjError, RasterioError) as error:
        parser.exit(2, f"gobahar: {error}\n")
    return 0
