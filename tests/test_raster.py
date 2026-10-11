import numpy as np
import pytest
from pyproj import Transformer

from gobahar.raster import sample_raster


def test_rectangular_grid_uses_row_then_column_and_preserves_order(raster_factory):
    result = sample_raster(
        raster_factory(), [(12.5, 18.5), (11.5, 19.5), (10.5, 19.5)], points_crs="EPSG:4326"
    )
    np.testing.assert_equal(result, [22, 11, 0])


def test_nodata_and_outside_are_nan_but_valid_zero_is_zero(raster_factory):
    result = sample_raster(
        raster_factory(),
        [(11.5, 18.5), (9.5, 19.5), (13, 19), (12, 18), (10.5, 19.5)],
        points_crs="EPSG:4326",
    )
    np.testing.assert_equal(result, [np.nan, np.nan, np.nan, np.nan, 0])


def test_outside_is_nan_even_without_a_nodata_marker(raster_factory):
    result = sample_raster(raster_factory(nodata=None), [(0, 0)], points_crs="EPSG:4326")
    assert np.isnan(result[0])


def test_dataset_mask_is_respected(raster_factory):
    mask = np.array([[255, 0, 255], [255, 255, 255]], dtype="uint8")
    result = sample_raster(
        raster_factory(nodata=None, mask=mask), [(11.5, 19.5)], points_crs="EPSG:4326"
    )
    assert np.isnan(result[0])


def test_points_are_transformed_to_the_raster_crs(raster_factory):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    point = transformer.transform(12.5, 18.5)
    result = sample_raster(raster_factory(), [point], points_crs="EPSG:3857")
    assert result.tolist() == [22]


def test_empty_input_is_supported(raster_factory):
    assert sample_raster(raster_factory(), [], points_crs="EPSG:4326").shape == (0,)


@pytest.mark.parametrize("points", [[(np.nan, 2)], [(1, np.inf)], [1, 2], [(1, 2, 3)]])
def test_invalid_coordinates_raise(raster_factory, points):
    with pytest.raises(ValueError, match="N-by-2"):
        sample_raster(raster_factory(), points, points_crs="EPSG:4326")


def test_missing_raster_crs_raises(raster_factory):
    with pytest.raises(ValueError, match="no CRS"):
        sample_raster(raster_factory(crs=None), [(11, 19)], points_crs="EPSG:4326")


@pytest.mark.parametrize("band", [0, 2, True, 1.5])
def test_invalid_band_raises(raster_factory, band):
    with pytest.raises(ValueError, match="Band"):
        sample_raster(raster_factory(), [(11, 19)], points_crs="EPSG:4326", band=band)
