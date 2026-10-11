"""Sentinel-1 SAFE orbit pass metadata."""

from os import PathLike
from xml.etree import ElementTree

S1_NAMESPACE = "http://www.esa.int/safe/sentinel-1.0/sentinel-1"


def read_pass_direction(path: str | PathLike[str]) -> str:
    """Return ASCENDING or DESCENDING, rejecting missing or conflicting metadata."""
    root = ElementTree.parse(path).getroot()
    elements = root.findall(f".//{{{S1_NAMESPACE}}}pass")
    values = {(element.text or "").strip().upper() for element in elements}
    if len(values) != 1 or not values <= {"ASCENDING", "DESCENDING"}:
        raise ValueError("Manifest must contain a consistent Sentinel-1 SAFE pass direction.")
    return values.pop()
