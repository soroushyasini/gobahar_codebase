# Repository modernization plan

Baseline: `b002bfa` on `main`, audited 2026-10-11.

The repository contains six geospatial research workspaces, 18 primary notebooks,
18 notebook checkpoints, and approximately 102 MiB of tracked research artifacts.
There is no installable package, dependency declaration, test suite, or CI workflow.

## Decisions

- Keep the research evidence and scientific assumptions traceable. Move each
  existing workspace intact under `research/` with a descriptive name; keep its
  internal filenames so relative data references continue to resolve.
- Preserve the original Persian project time report under `reports/` and replace
  the root README with a developer and research entry point.
- Introduce `src/gobahar/` for supported, tested operations: raster sampling,
  dated-series trends, and Sentinel-1 pass metadata. Keep exploratory notebooks
  explicitly separate from supported code.
- Add a maintained land-cover notebook using the shared raster sampler, including
  every available yearly TIFF rather than a manually maintained year list.
- Use explicit CRS arguments, mask missing/outside raster cells, validate temporal
  inputs, and preserve displacement units/sign. Do not infer scientific metadata.
- Use Python packaging, pinned development dependencies, CI on Linux/Windows,
  contributor guidance, and a severity-ranked audit with follow-up work.
- Do not assign a license to third-party research data or rewrite Git history.

## Order and checkpoints

1. Record baseline findings and acceptance criteria.
2. Reorganize historical workspaces and reports; verify file content hashes.
3. Implement shared operations and behavioral regression tests.
4. Add maintained notebooks, installation metadata, and quality automation.
5. Review changes, run quality gates and bundled-data smoke tests, publish a
   reviewable branch and pull request.

## Risks

Historical notebooks contain hidden state, duplicated experiments, saved errors,
missing external rasters, and inconsistent CRS assumptions. They cannot be treated
as validated pipelines. Their runtime inputs must be reconciled with source
metadata before rerunning analyses for publication. File moves change external
links; `docs/migration.md` records the mapping.

See `todo.md` for acceptance criteria and `docs/audit.md` for findings/evidence.
