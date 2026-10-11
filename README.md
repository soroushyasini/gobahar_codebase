# Golbahar subsidence research

Geospatial analysis of land subsidence around Golbahar and the Mashhad plain,
combining InSAR displacement observations with GNSS, groundwater measurements,
land-cover rasters, and infrastructure/critical-site locations.

This repository includes supported Python utilities and the historical notebooks,
data, figures, and reports from the research project. Historical notebooks are
exploratory records with known limitations; see the [code audit](docs/audit.md)
before relying on their results.

## Repository map

```text
src/gobahar/           Tested raster, time-series, and SAFE metadata utilities
tests/                Synthetic regression fixtures and CLI tests
notebooks/            Maintained examples using the package
research/
  land_cover/         Annual land-cover rasters and metro observations
  gnss_insar/         GNSS and InSAR comparison experiments
  groundwater_insar/  Piezometer and InSAR experiments
  infrastructure/    Corridor profiles, shapefiles, and mapping experiments
  critical_sites/    Critical-site coordinates and time-series experiments
  sentinel_metadata/  Sentinel-1 SAFE manifest and original inspection notebook
data/raw/             Ignored local acquisitions; see data/README.md
outputs/              Ignored results from new runs
reports/              Original Persian project time report and interactive HTML
docs/                 Audit, migration guide, and research workflow catalog
requirements/         Tested runtime version constraints
scripts/              Repository validation utilities
.github/              CI, dependency updates, and contribution templates
```

The [migration guide](docs/migration.md) maps every former root directory to its
new location. The original README is preserved as the
[Persian project time report](reports/project_time_report.fa.md); the
[interactive report](reports/project_time_report.html) can be downloaded and opened
in a browser (GitHub's file view does not execute it).

## Setup

Use Python 3.11 or newer. CI exercises Python 3.11 and 3.13 on Linux and 3.13 on
Windows. From the repository root:

```bash
git clone https://github.com/soroushyasini/gobahar_codebase.git
cd gobahar_codebase
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Install the supported code and development tools:

```bash
python -m pip install -c requirements/constraints.txt -e ".[dev]"
gobahar --help
```

For plotting, mapping, and the historical notebooks, add the research extra:

```bash
python -m pip install -c requirements/constraints.txt -e ".[dev,research]"
python -m ipykernel install --user --name gobahar --display-name "Python (gobahar)"
jupyter lab
```

Select the `Python (gobahar)` kernel. Geospatial binary wheels are available for
the tested platforms; systems without compatible wheels may need a managed GDAL
environment. The constraints file records tested direct runtime versions; it is
not a complete transitive lockfile. Research extras declare observed notebook
imports, and do not guarantee that every historical experiment executes unchanged.

## Supported operations

Read orbit pass metadata from the bundled Sentinel-1 manifest:

```bash
gobahar pass-direction research/sentinel_metadata/manifest.safe
```

Sample one or more rasters at points from a CSV or the first worksheet of an XLSX.
For a table with verified longitude/latitude columns:

```bash
gobahar sample --points data/raw/points.csv --x-column longitude --y-column latitude --points-crs EPSG:4326 --raster research/land_cover/LULC_2024_10m.tif --output outputs/point_land_cover.csv
```

Each raster's filename stem becomes an output column. Input columns and row order
are retained. Coordinates are transformed into each raster's actual CRS; sampling
uses the containing pixel without interpolation. Nodata, masked pixels, and points
outside the raster become empty CSV cells. Valid zero values remain zero. The
command refuses to overwrite an existing output or collide with input columns.

Fit a descriptive linear trend to a CSV or XLSX series:

```bash
gobahar trend --input data/raw/observations.csv --date-column date --value-column displacement --unit mm
```

Use unambiguous Gregorian dates such as `2020-01-31`. Dates are interpreted in UTC;
convert Jalali dates explicitly before using this command. Missing/nonfinite data
and series without two distinct timestamps are rejected. JSON output includes
the slope per day, annual rate using 365.25 days/year, intercept at the earliest
date, observation count, and descriptive R-squared. `--days-per-year` changes that
reporting convention. Units, displacement sign, reference epoch, and LOS/vertical
geometry remain the caller's responsibility; this command applies no conversion.

The same operations are available as Python functions:

```python
from gobahar.manifest import read_pass_direction
from gobahar.raster import sample_raster
from gobahar.timeseries import fit_linear_trend
```

See [maintained land-cover sampling](notebooks/land_cover.ipynb) and
[SAFE metadata inspection](notebooks/sentinel_metadata.ipynb) for worked examples.
The land-cover notebook requires an explicit point CRS because historical CRS
assumptions conflict. See the [research catalog](docs/research-workflows.md) for
the remaining notebooks and missing inputs.

## Quality checks

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python scripts/check_notebooks.py
python -m build
```

Tests use small synthetic rasters and dated observations without external APIs or
large radar stacks. CI enforces at least 90% coverage for supported Python code,
validates notebook schemas, and builds/installs a wheel. Historical notebooks are
not executed by CI. New maintained notebooks must have cleared outputs and valid
Python cells. See [CONTRIBUTING.md](CONTRIBUTING.md) for the development process.

## Data and reuse

Bundled research assets remain in their workspaces for provenance and relative
path compatibility. Large InSAR raster stacks are not included. New acquisitions
belong in `data/raw/`, and new results in `outputs/`; both are ignored. Document
CRS, units, date conventions, nodata policy, checksums, and processing lineage
using the [data guidance](data/README.md).

No repository license was present at the audit baseline. Code reuse terms and
third-party dataset redistribution permissions need an explicit owner decision;
this cleanup does not assign a license to either.
