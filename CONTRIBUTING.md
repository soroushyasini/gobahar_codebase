# Contributing

Use a short-lived branch with one concern per commit. Describe the problem,
resulting behavior, and validation in the pull request. See the root README for
environment setup. Run all quality commands listed there before review.

## Code and notebooks

Reusable logic belongs in `src/gobahar/`; maintained notebooks in `notebooks/`
should configure inputs and call those helpers. Avoid package installation cells,
working-directory changes, absolute machine paths, duplicate implementations,
and exception handlers that hide bad inputs. Ruff defines formatting/import style.
Clear maintained notebook outputs and execution counts before committing.

`research/` contains historical experiments and reference artifacts. Preserve
them while migrating useful behavior to supported code. Do not mass-reformat
historical notebook JSON or silently regenerate published figures/tables.

## Scientific changes

State source/destination CRS, axis order, measurement units, date calendar,
timezone, nodata policy, displacement sign, reference epoch, and LOS/vertical
geometry when relevant. Do not infer a CRS from a file name or another notebook.
For distance/buffer operations, use an appropriate projected CRS with verified
units. For categorical rasters, preserve category values without bilinear mixing.

Regression tests should use known-answer synthetic data: rectangular rasters to
catch transposition, different source/raster CRSs, nodata and edge points, or dated
series with known rates. A schema check or a successful plot is not scientific
validation. Describe remaining assumptions in the audit or a focused issue.

## Data, dependencies, and reports

Keep local input stacks in `data/raw/` and new outputs in `outputs/`. Record run
configuration, input checksums, dependency versions, and provenance before sharing
a result. Never commit credentials, notebook checkpoints, office lock files, or
temporary artifacts. Keep shapefile sidecars together during any move.

Declare runtime dependencies in `pyproject.toml`, keep tested direct versions in
`requirements/constraints.txt`, and verify upgrades individually. The `research`
extra is for exploratory dependencies; the default package should stay focused.
CI actions use commit SHAs. Dependabot can propose reviewed dependency updates.

The project has no declared reuse license. An owner must choose code terms and
verify dataset rights before a release that promises third-party reuse.
