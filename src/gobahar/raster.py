"""CRS-aware sampling without silently treating missing raster cells as zero."""

from collections.abc import Sequence
from os import PathLike

import numpy as np
import rasterio
from numpy.typing import NDArray
from pyproj import CRS, Transformer


def sample_raster(
    path: str | PathLike[str],
    coordinates: Sequence[tuple[float, float]] | NDArray,
    *,
    points_crs: str | CRS,
    band: int = 1,
) -> NDArray[np.float64]:
    """Sample containing pixels after transforming x/y into the raster CRS.

    Coordinates always follow x/y order (longitude/latitude for geographic CRS).
    Return one float per point in the original order. Outside pixels, masked cells,
    nodata, and nonfinite raster values become NaN; valid zero remains zero. This
    uses pixel lookup with no interpolation, preserving categorical class values.
    Missing CRS metadata and invalid coordinates raise rather than guessing.
    """
    source_crs = CRS.from_user_input(points_crs)
    xy = np.asarray(coordinates, dtype=float)
    if xy.size == 0 and xy.shape in {(0,), (0, 2)}:
        xy = xy.reshape(0, 2)
    if xy.ndim != 2 or xy.shape[1] != 2 or not np.isfinite(xy).all():
        raise ValueError("Coordinates must be a finite N-by-2 array of x/y pairs.")

    with rasterio.open(path) as src:
        if src.crs is None:
            raise ValueError(f"Raster has no CRS metadata: {path}")
        if not isinstance(band, int) or isinstance(band, bool) or band not in src.indexes:
            raise ValueError(f"Band must be one of {src.indexes}.")
        result = np.full(len(xy), np.nan, dtype=np.float64)
        if len(xy) == 0:
            return result
        transformer = Transformer.from_crs(source_crs, src.crs, always_xy=True)
        xs, ys = transformer.transform(xy[:, 0].tolist(), xy[:, 1].tolist(), errcheck=True)
        transformed = np.column_stack((xs, ys))
        if not np.isfinite(transformed).all():
            raise ValueError("Coordinate transformation produced nonfinite values.")

        inside_indices = []
        inside_xy = []
        for index, (x, y) in enumerate(transformed):
            row, col = src.index(x, y)
            if 0 <= row < src.height and 0 <= col < src.width:
                inside_indices.append(index)
                inside_xy.append((x, y))
        for index, sample in zip(
            inside_indices, src.sample(inside_xy, indexes=band, masked=True), strict=True
        ):
            if not np.ma.is_masked(sample[0]) and np.isfinite(sample[0]):
                result[index] = sample[0]
    return result
