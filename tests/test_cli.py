import json

import pandas as pd
import pytest

from gobahar.cli import main
from gobahar.manifest import S1_NAMESPACE


def test_cli_samples_csv_and_refuses_to_overwrite(tmp_path, raster_factory):
    points = tmp_path / "points.csv"
    points.write_text("x,y,name\n12.5,18.5,station\n")
    output = tmp_path / "results" / "samples.csv"
    args = [
        "sample",
        "--points",
        str(points),
        "--x-column",
        "x",
        "--y-column",
        "y",
        "--points-crs",
        "EPSG:4326",
        "--raster",
        str(raster_factory()),
        "--output",
        str(output),
    ]
    assert main(args) == 0
    assert pd.read_csv(output)["grid"].tolist() == [22]
    previous = output.read_bytes()
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 2
    assert output.read_bytes() == previous


def test_cli_trend_from_excel_has_unit_and_year_metadata(tmp_path, capsys):
    path = tmp_path / "series.xlsx"
    pd.DataFrame({"date": ["2020-01-01", "2020-01-02"], "disp": [0, -1]}).to_excel(
        path, index=False
    )
    assert (
        main(
            [
                "trend",
                "--input",
                str(path),
                "--date-column",
                "date",
                "--value-column",
                "disp",
                "--unit",
                "mm",
            ]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert result["value_unit"] == "mm"
    assert result["rate_per_year"] == -365.25


def test_cli_pass_direction(tmp_path, capsys):
    path = tmp_path / "manifest.safe"
    path.write_text(f'<root xmlns:s="{S1_NAMESPACE}"><s:pass>ASCENDING</s:pass></root>')
    assert main(["pass-direction", str(path)]) == 0
    assert capsys.readouterr().out.strip() == "ASCENDING"


@pytest.mark.parametrize("case", ["missing_file", "bad_extension", "missing_column", "bad_value"])
def test_cli_input_errors_are_concise(tmp_path, capsys, case):
    path = tmp_path / ("input.txt" if case == "bad_extension" else "input.csv")
    if case != "missing_file":
        path.write_text(
            "wrong,disp\n2020-01-01,1\n"
            if case == "missing_column"
            else "date,disp\ninvalid,1\n2020-01-02,2\n"
        )
    with pytest.raises(SystemExit) as error:
        main(
            [
                "trend",
                "--input",
                str(path),
                "--date-column",
                "date",
                "--value-column",
                "disp",
                "--unit",
                "mm",
            ]
        )
    assert error.value.code == 2
    stderr = capsys.readouterr().err
    assert "gobahar:" in stderr
    assert "Traceback" not in stderr


@pytest.mark.parametrize("duplicate", [False, True])
def test_cli_rejects_output_column_collisions(tmp_path, raster_factory, duplicate):
    path = tmp_path / "points.csv"
    path.write_text("x,y,grid\n12,19,3\n" if not duplicate else "x,y\n12,19\n")
    raster = raster_factory()
    rasters = [str(raster), str(raster)] if duplicate else [str(raster)]
    output = tmp_path / "output.csv"
    with pytest.raises(SystemExit):
        main(
            [
                "sample",
                "--points",
                str(path),
                "--x-column",
                "x",
                "--y-column",
                "y",
                "--points-crs",
                "EPSG:4326",
                "--raster",
                *rasters,
                "--output",
                str(output),
            ]
        )
    assert not output.exists()
