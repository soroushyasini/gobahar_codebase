"""Validate notebook schemas; supported notebooks must also have clean outputs."""

import ast
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    paths += sorted((ROOT / "research").rglob("*.ipynb"))
    for path in paths:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        if path.parent == ROOT / "notebooks":
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    ast.parse(cell.source)
                    if cell.outputs or cell.execution_count is not None:
                        raise ValueError(f"Clear execution outputs before committing: {path}")
    print(f"Validated {len(paths)} notebooks; historical notebooks were not executed.")


if __name__ == "__main__":
    main()
