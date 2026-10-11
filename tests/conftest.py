import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin


@pytest.fixture
def raster_factory(tmp_path):
    """Rectangular grid makes accidental transposition observable."""

    def create(name="grid.tif", crs="EPSG:4326", nodata=-9999.0, mask=None):
        path = tmp_path / name
        data = np.array(
            [[0, 11, 12], [20, nodata if nodata is not None else 21, 22]], dtype="float32"
        )
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=2,
            width=3,
            count=1,
            dtype="float32",
            crs=crs,
            transform=from_origin(10, 20, 1, 1),
            nodata=nodata,
        ) as dst:
            dst.write(data, 1)
            if mask is not None:
                dst.write_mask(mask)
        return path

    return create
