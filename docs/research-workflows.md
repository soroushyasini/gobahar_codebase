# Research workflow catalog

The 18 notebooks below are historical research records, preserved byte-for-byte
from baseline `b002bfa`. Names such as `finale`, `ver_2`, and `improbed` do not establish
a validated canonical workflow. Launch them from their containing directory to
resolve local paths. Review the audit and inspect every input before execution.

| Workspace | Historical notebooks | Inputs and limitations |
| --- | --- | --- |
| `research/land_cover/` | `Untitled.ipynb` | `Metro-Subsidence.xlsx`, eight annual LULC TIFFs (2017–2024). Original list skips 2020; final sampling helper transposes row/column. Use maintained replacement. |
| `research/gnss_insar/` | `GPSvsInsar.ipynb`, `Untitled.ipynb`, `finale.ipynb`, `gmakan_gps_insar.ipynb`, `gps.ipynb` | `gps.json`, `disp.xlsx`, text series, and processed variants are bundled. Filtering/normalization and LOS versus vertical conventions need validation. Some experiments use online basemaps. |
| `research/groundwater_insar/` | `1Untitled.ipynb`, `backup_old.ipynb`, `conv.ipynb`, `improbed.ipynb`, `ver_2.ipynb` | `pizometer_data.xlsx`, coordinate workbooks, multi-sheet time series, and figures. Calendar, unit, baseline, and variant differences require reconciliation. |
| `research/infrastructure/` | `Untitled.ipynb`, `Untitled1.ipynb`, `multi_line_aprch.ipynb` | Bundled shapefiles, tables, and maps; external `tiffs/` and `tiffs_reprojected/` stacks are missing. Some cells contact Overpass/OSM; do not run the entire notebook blindly. |
| `research/critical_sites/` | `1Untitled.ipynb`, `Untitled.ipynb`, `conv.ipynb` | Coordinate workbooks, time-series exports, maps, and `critical_points.zip`. `conv.ipynb` refers to an absent `cord.xlsx`; identical conversion experiment also exists in groundwater workspace. |
| `research/sentinel_metadata/` | `manifest_proc.ipynb` | Bundled `manifest.safe`. Original assumes a pass element exists and installs an unused `sentinelhub` package. Use maintained replacement. |

The research optional dependency set covers observed Python imports plus Excel
engines and Jupyter. Shell commands such as `!ls` and notebook-local `!pip install`
are historical environment assumptions, not Python syntax defects. Saved exception
outputs represent previous failed runs, not necessarily currently failing cells.

## Migrating a historical analysis

1. Identify the exact notebook cells, inputs, date interval, and scientific question.
2. Record authoritative CRS, units, calendar, nodata markers, sign, baseline, and
   displacement geometry. Verify required external datasets are available.
3. Extract one coherent operation into the package and test a known-answer fixture.
4. Write a small maintained notebook that calls it with explicit parameters and
   saves fresh results under `outputs/`.
5. Compare results with independently verified references before replacing a
   scientific claim or historical report. Record any expected numeric differences.

## Maintained examples

`notebooks/land_cover.ipynb` discovers all eight bundled raster years, transforms
point coordinates to each raster's own CRS, and preserves masked/outside cells as
missing. Its source CRS deliberately requires configuration. `GOBAHAR_POINTS_CRS`
can supply that setting for controlled executions.

`notebooks/sentinel_metadata.ipynb` reads pass metadata using the tested package.
Both notebooks locate the repository from their working directory or its parents,
contain no installation cells, and are stored without execution outputs.
