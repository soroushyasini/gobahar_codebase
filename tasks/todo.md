# Modernization tasks

## 1. Baseline audit
- [x] Inventory tracked files, primary notebooks, imports, and saved failures.
- [x] Inspect sampling, temporal regression, and manifest routines.
- [x] Record decisions before implementation in `plan.md`.
Verification: inspect the baseline Git tree and notebook code cells.
Dependencies: none.

## 2. Research layout
- [x] Move six workspaces and two root reports to documented destinations.
- [x] Remove tracked checkpoint/temporary/lock/log artifacts.
- [x] Verify every retained original file has the same content hash.
Verification: compare baseline blob hashes with the migration mapping.
Dependencies: 1. Files: research workspaces, reports, migration guide.

## 3. Supported raster sampling
- [x] Explicit source CRS is transformed to each raster's actual CRS.
- [x] Row/column ordering, outside cells, nodata, and valid zero are tested.
- [x] A maintained land-cover notebook uses the shared sampler.
Verification: synthetic rectangular GeoTIFF tests and bundled land-cover smoke run.
Dependencies: 2. Files: raster module, regression tests, maintained notebook.

## 4. Supported temporal and metadata operations
- [x] Fit dated finite observations with a documented 365.25-day year convention.
- [x] Reject degenerate dates and invalid input rather than silently dropping rows.
- [x] Parse pass direction from the proper Sentinel-1 namespace with clear errors.
Verification: known-slope, malformed-input, namespace, and CLI tests.
Dependencies: 2. Files: timeseries/manifest modules, CLI, tests.

## 5. Developer workflow
- [x] Editable installation, wheel build, lint/format, and tests pass.
- [x] CI validates supported code and notebook structure without network/data jobs.
- [x] README, contribution guide, migration guide, and audit explain limitations.
Verification: fresh virtual environment, wheel install, CLI smoke checks, diff review.
Dependencies: 3 and 4. Files: packaging, CI, developer and audit documentation.

## Checkpoint: handoff
- [x] Local quality gates pass and results are recorded in the audit.
- [ ] Reviewable commits are pushed and a pull request is attached.
- [x] Remaining scientific/data-governance work is explicitly documented.
