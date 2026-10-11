# Layout migration

The modernization starts from commit `b002bfa`. Use `git log --follow -- <path>`
to inspect an individual file's history across a rename.

| Original path | Current path | Purpose |
| --- | --- | --- |
| `gobl_LCLU/` | `research/land_cover/` | Land-cover raster and metro subsidence experiments |
| `GPS_vs_InSAR/` | `research/gnss_insar/` | GNSS and InSAR time-series comparisons |
| `InSAR_extent/` | `research/sentinel_metadata/` | Sentinel-1 SAFE manifest inspection |
| `phase_2/` | `research/infrastructure/` | Infrastructure corridors, profiles, and OSM experiments |
| `Pisometer_vs_InSAR/` | `research/groundwater_insar/` | Piezometer and InSAR comparisons |
| `sensitive_locations/` | `research/critical_sites/` | Critical-site coordinate and time-series experiments |
| `README.md` | `reports/project_time_report.fa.md` | Original Persian project time report |
| `final_intractive_report.html` | `reports/project_time_report.html` | Original interactive time report |

All internal workspace filenames and retained research contents are preserved.
Relative references inside each workspace still use that workspace as the working
directory. Open historical notebooks from their own directory; update any external
bookmarks or scripts that referred to the old root directories.

Tracked Jupyter checkpoints, office lock files, a temporary file, and a debug log
were removed. They remain recoverable from Git history. No original analytical
notebook, raster, table, shapefile component, figure, archive, or report was deleted.

## Supported replacement paths

- `notebooks/land_cover.ipynb` replaces the duplicated land-cover sampling experiment
  for new work. Set `POINTS_CRS` explicitly from the input's authoritative metadata.
- `notebooks/sentinel_metadata.ipynb` replaces the one-off manifest inspection.
- `gobahar sample`, `gobahar trend`, and `gobahar pass-direction` provide scriptable
  operations with explicit inputs and output paths; see the root README.

The historical notebooks are retained as research records. Moving them does not
certify their scientific results. See `audit.md` before reusing historical outputs.
