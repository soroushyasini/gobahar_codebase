# External data

Place local, untracked acquisitions in `raw/`. Historical bundled research assets
remain in `research/<workflow>/` to preserve notebook-relative paths and provenance.
Their origin, CRS, units, processing lineage, and redistribution rights still need
to be documented; a filename or old notebook assumption is not authoritative metadata.

The large InSAR time-slice stacks (`tiffs/`, `tiffs_reprojected/`) are absent from
Git. Obtain them from the project custodian before rerunning infrastructure analyses.
Do not commit credentials or raw satellite acquisitions. Save new derived products
under the repository's ignored `outputs/` directory and record the command, input
checksums, CRS, units, package versions, and processing date alongside each run.

For future dataset additions, record:

| Field | Required information |
| --- | --- |
| Identity | Dataset name/version and source/provider URL |
| Integrity | File list, byte sizes, SHA-256 checksums |
| Spatial reference | Authoritative CRS, axis order, resolution, and extent |
| Temporal reference | Date range, calendar, timezone, and acquisition dates |
| Values | Units, nodata markers, sign, LOS/vertical convention, reference epoch |
| Processing | Upstream method/tool/version and transformations |
| Rights | License/permission, attribution, and access restrictions |
