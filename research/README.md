# Historical research workspaces

These six workspaces preserve the original project experiments and their bundled
inputs/results. See the [workflow catalog](../docs/research-workflows.md) for the
18 notebooks and the [audit](../docs/audit.md) for scientific correctness risks.

For new work, use `src/gobahar/` and `notebooks/`. The historical land-cover notebook
contains a row/column transposition; infrastructure notebooks include unsafe CRS
mismatch handling. Their retained outputs have not been revalidated.

Each workspace is kept intact so notebook-relative references resolve when its
kernel starts there. Some experiments still require absent external datasets,
manual configuration, shell commands, or online APIs. Do not execute every cell
as an automated pipeline. Keep new generated results under the root `outputs/`.
