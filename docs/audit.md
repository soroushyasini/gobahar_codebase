# Repository and code audit

Audit date: 2026-10-11. Baseline: `b002bfa` on `main`.

## Scope and baseline

Inventory and static inspection covered all 18 primary notebooks across six
research areas, including imports, raster sampling, coordinate conversion,
regression, baseline adjustment, calendar conversion, and online queries. This
was followed by targeted synthetic regression tests and bundled-asset smoke checks.
Historical notebooks were not executed as complete workflows; their external
inputs, hidden state, and scientific assumptions prevent that claim.

The baseline had 320 tracked files, approximately 101.7 MiB of working-tree
content, 18 primary notebooks, and 18 duplicate notebook checkpoints. There was
no dependency specification, installable Python package, test suite, CI,
contributor guide, or repository license. The README was a Persian project time
report rather than a code entry point. Five primary notebooks contained a total
of 11 saved exception outputs; these are evidence of past failures, not a fresh
execution result.

## Findings ranked by impact

### High: land-cover pixel indices are transposed

Evidence: the final `extract_raster_values` implementation in
`research/land_cover/Untitled.ipynb` assigns `col, row = src.index(x, y)` and reads
`data[row, col]`. Rasterio returns `(row, col)`. On the bundled rectangular rasters
(1272 rows by 1729 columns), this can sample the wrong pixel or misclassify a valid
point as outside. The earlier sampling implementation in that notebook does not
make this particular indexing mistake, but is replaced later in notebook state.

Resolution: the supported `gobahar.raster.sample_raster` and maintained land-cover
notebook use correct pixel lookup. Tests use asymmetric values on a rectangular
grid, so a transposition cannot accidentally pass. Historical code and outputs
are preserved and remain unvalidated.

### High: CRS assumptions disagree and some mismatches only produce a warning

Evidence: the land-cover notebook declares point coordinates as EPSG:32641;
coordinate notebooks use EPSG:32640; infrastructure variants also declare 32643.
In `research/infrastructure/multi_line_aprch.ipynb`, a corridor routine reprojects
its vector to 32640, logs a raster CRS mismatch, then samples with unchanged vector
x/y values. Other line routines use `line.length` as meters without checking the
source CRS or its units. These are correctness risks, not naming/style issues.

Bundled-data check: `Metro-Subsidence.xlsx` contains 441 points. Using its X/Y
columns against `LULC_2024_10m.tif`, EPSG:32640 gives **441 finite samples**, while
EPSG:32641 gives **441 missing samples**. All eight bundled TIFFs declare EPSG:4326
and have shape 1272 × 1729. The spatial overlap strongly suggests the old zone-41
assumption is wrong; it does not substitute for authoritative point metadata.

Resolution: the supported sampler requires an explicit point CRS and transforms
coordinates to each raster's actual CRS. It rejects a missing raster CRS. The
maintained notebook requires the researcher to configure the source CRS.
Open: confirm original coordinate metadata and migrate corridor workflows with
an explicit projected distance CRS and source-to-raster transformation.

### High: GNSS/InSAR comparisons have unresolved units and displacement geometry

Evidence: `research/gnss_insar/finale.ipynb` describes an input as centimeters,
contains a commented-out centimeters-to-millimeters multiplication, then labels
later comparisons in millimeters. Several variants apply different normalization
or reference-baseline steps. A vertical GNSS component and an InSAR displacement
series cannot be assumed to represent the same measurement geometry.

Open: verify actual input units, LOS versus vertical convention, acquisition
geometry, reference epoch, and the intended comparison before regenerating
figures. The audit establishes inconsistent code/documentation, not that a
specific reported scientific value is wrong by a known factor. The new trend
utility preserves caller units/sign and performs no undocumented conversion.

### High: a shared date interval does not guarantee shared baseline observations

Evidence: `research/gnss_insar/finale.ipynb` chooses the maximum of the two minimum
dates as `start_date`, then indexes both series at exactly that date with
`.iloc[0]`. If only one series has an observation on the selected date, the other
selection is empty and raises. Empty overlapping periods are also not checked.

Open: define a scientific policy for aligning asynchronous observations and
baseline interpolation/tolerance. Extract and test that policy before migrating
the comparison workflow. Do not silently choose an interpolation method.

### Medium: the original manifest lookup uses the wrong namespace

Evidence: `research/sentinel_metadata/manifest_proc.ipynb` searches for `safe:pass`
in `http://www.esa.int/safe/sentinel-1.0`. The bundled manifest stores the value in
`s1:pass` in the Sentinel-1 extension namespace ending in `/sentinel-1`. The original
lookup dereferences `.text` without checking for a missing element.

Resolution: the supported parser uses the correct extension namespace and rejects
missing, unknown, or conflicting values. A fixture models nested SAFE orbit
metadata and proves the generic SAFE namespace is rejected. The bundled manifest
successfully returns `DESCENDING`.

### Medium: the 2020 land-cover raster is omitted

Evidence: `research/land_cover/Untitled.ipynb` manually lists 2017–2019 and
2021–2024 despite a tracked `LULC_2020_10m.tif` being present.

Resolution: the maintained notebook discovers all `LULC_*_10m.tif` inputs and
processes all eight bundled years. It refuses to overwrite existing columns or
an existing output file.

### Medium: notebook state and duplicated variants obscure reproducibility

Evidence: names such as `Untitled`, `finale`, `backup_old`, `ver_2`, and `improbed`
coexist without a declared canonical workflow. Some cells rely on variables from
earlier experiments. Calendar-conversion helpers and plotting loops are repeated;
some cells install dependencies or invoke Unix-specific shell commands. The two
`conv.ipynb` conversion experiments are identical. Required external radar stacks
are absent, and a conversion notebook refers to an absent `cord.xlsx`.

Resolution: the workflow catalog names all original notebooks and input limits;
the package and maintained examples establish a supported entry point. Historical
workspaces remain intact for relative paths and provenance. Open: migrate the
remaining analyses one scientific operation at a time, after reconciling inputs.

### Medium: missing-data handling and annual-rate conventions vary

Evidence: multiple legacy helpers catch every exception, return `None`/NaN, or
silently drop date/value failures. Raster sampling variants do not consistently
mask nodata. Annualization uses both 365 and 365.25 days, with inconsistent early
rounding. A missing raster sample can therefore become a valid-looking result
without a clear rejection or diagnostic policy.

Resolution: supported sampling preserves nodata/masks/outside cells as NaN and
valid zero as zero. The trend utility rejects missing/nonfinite data, requires
two distinct timestamps, and reports a documented configurable year convention.
Open: reconcile legacy calendar-cleaning and exclusion policies before using
historical groundwater/critical-site rates for comparisons.

### Medium: online queries need a controlled execution policy

Evidence: infrastructure variants contact Overpass using both HTTP and HTTPS;
one `requests.get` call has no timeout. The more developed variant adds retries
but still creates one future per point and stores network error text alongside
feature results. HTML outputs also depend on external map assets.

Open: use HTTPS, explicit timeouts, bounded work queues, cache/provenance metadata,
and typed failure results in a future migrated enrichment pipeline. CI does not
execute online research jobs or contact OSM.

### Medium: dataset provenance and reuse terms are undocumented

Evidence: source data, derived tables, maps, figures, archives, and reports were
mixed without a dataset manifest. No license was declared at the baseline.

Resolution: `data/README.md` defines required provenance and scientific metadata;
new raw data and outputs are ignored. The layout separates supported code,
maintained examples, historical workspaces, and reports. Open: the owner must
choose code licensing and establish dataset rights. No license or dataset rights
were invented by this cleanup.

## Changes and preservation

- Six workspaces moved to descriptive `research/` paths; root reports moved to
  `reports/`. All **296 retained research/report files** were verified against
  their baseline Git blob hashes. Internal filenames were retained. The remaining
  retained original file, `.gitignore`, was intentionally updated for the new layout.
- Removed **23 disposable files**: 18 notebook checkpoints, three office lock
  files, one temporary file, and one debug log. Git history retains them.
- Added the `src/` package, CLI, tested runtime constraints, maintained notebooks,
  behavioral tests, packaging, developer docs, and quality automation.
- Added `.gitignore`, `.gitattributes`, and `.editorconfig` conventions to keep
  generated state out of future changes and source formatting portable.

## Validation record

Local verification uses a fresh Windows virtual environment, Python 3.13.13,
and the direct runtime versions in `requirements/constraints.txt`.

| Check | Result |
| --- | --- |
| Editable installation | Passed |
| Regression tests | 50 passed |
| Supported package coverage, including branches | 98.92%, with 90% enforced minimum |
| Ruff lint and formatting | Passed after formatting |
| Notebook schema validation | 20 passed (18 historical, two maintained) |
| Sequential Python-cell execution of maintained notebooks | Passed |
| Bundled raster sampling | All eight TIFFs passed known pixel-center comparisons |
| Bundled SAFE metadata | `DESCENDING` |
| Source distribution and wheel build | Passed; wheel smoke check repeated after final source changes |

The land-cover notebook smoke run processed 441 rows and eight years under the
historical zone-41 assumption and correctly reported all samples missing. A
separate zone-40 check demonstrated full spatial overlap. These are software and
spatial-consistency checks, not a validated publication dataset. The sequential
cell check executes Python source in order; it is not a Jupyter UI/kernel test.

The local machine could not resolve `files.pythonhosted.org`; dependency installation
and isolated builds used the Tsinghua PyPI mirror through a process-local override.
No machine-specific index configuration was committed. Rasterio/affine emit a
dependency deprecation warning during synthetic fixture construction; tests pass.

CI exercises Linux Python 3.11/3.13 and Windows Python 3.13, checks coverage and
notebook structure, builds a distribution, and smoke-tests the installed wheel.
Its run status must be checked on the pull request before merging.

## Remaining validation boundaries

This audit does not certify historical scientific conclusions, execute all legacy
notebooks, validate absent InSAR stacks, perform penetration testing, or guarantee
that the dependency graph has no advisories. Runtime constraints pin tested direct
versions; transitive and research dependencies are not completely locked. The
90% coverage gate applies to supported package code, not historical notebooks.

## Reference checks

Raster lookup and masking follow the official [Rasterio dataset API](https://rasterio.readthedocs.io/en/stable/api/rasterio.io.html)
and [sampling API](https://rasterio.readthedocs.io/en/stable/api/rasterio.sample.html).
The Sentinel-1 pass element is documented in the official
[Sentinel-1 Product Specification](https://sentinels.copernicus.eu/documents/247904/1877131/Sentinel-1-Product-Specification-18052021.pdf).
Packaging follows the [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).
