# Changelog

## 0.1.0 — Unreleased

### Added
- Installable Python utilities and CLI for CRS-aware raster sampling, dated-series
  trends, and validated Sentinel-1 orbit pass metadata.
- Regression tests, coverage gate, Linux/Windows CI, dependency update automation,
  contribution guidance, and documented data requirements.
- Maintained land-cover and SAFE metadata notebooks with explicit configuration.

### Changed
- Group original project workspaces under descriptive `research/` directories.
- Move the original Persian time report and interactive HTML into `reports/`.
- Use the root README as the project setup and navigation entry point.

### Fixed
- Supported land-cover sampling avoids the historical row/column transposition,
  handles CRS transformation and missing cells, and discovers the omitted 2020 raster.
- Supported metadata inspection reads pass direction from the Sentinel-1 extension
  namespace used in the bundled SAFE manifest.

Historical analysis notebooks and their scientific outputs remain preserved;
known issues and validation limits are recorded in `docs/audit.md`.
