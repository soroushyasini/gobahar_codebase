from xml.etree.ElementTree import ParseError

import pytest

from gobahar.manifest import S1_NAMESPACE, read_pass_direction


def test_pass_is_in_sentinel1_extension_not_generic_safe_namespace(tmp_path):
    path = tmp_path / "manifest.safe"
    path.write_text(
        '<root xmlns:safe="http://www.esa.int/safe/sentinel-1.0" '
        f'xmlns:s1="{S1_NAMESPACE}">'
        "<safe:orbitReference><safe:extension><s1:orbitProperties>"
        "<s1:pass>DESCENDING</s1:pass>"
        "</s1:orbitProperties></safe:extension></safe:orbitReference></root>"
    )
    assert read_pass_direction(path) == "DESCENDING"
    path.write_text(
        '<root xmlns:safe="http://www.esa.int/safe/sentinel-1.0">'
        "<safe:pass>DESCENDING</safe:pass></root>"
    )
    with pytest.raises(ValueError):
        read_pass_direction(path)


@pytest.mark.parametrize("value", ["ASCENDING", "DESCENDING", " descending "])
def test_pass_direction_handles_namespace_prefix_and_whitespace(tmp_path, value):
    path = tmp_path / "manifest.safe"
    path.write_text(f'<root xmlns:s="{S1_NAMESPACE}"><s:pass>{value}</s:pass></root>')
    assert read_pass_direction(path) == value.strip().upper()


@pytest.mark.parametrize(
    "body",
    [
        "",
        "<pass>ASCENDING</pass>",
        "<s:pass/>",
        "<s:pass>UNKNOWN</s:pass>",
        "<s:pass>ASCENDING</s:pass><s:pass>DESCENDING</s:pass>",
    ],
)
def test_missing_invalid_or_conflicting_direction_raises(tmp_path, body):
    path = tmp_path / "manifest.safe"
    path.write_text(f'<root xmlns:s="{S1_NAMESPACE}">{body}</root>')
    with pytest.raises(ValueError, match="consistent"):
        read_pass_direction(path)


def test_malformed_xml_raises(tmp_path):
    path = tmp_path / "manifest.safe"
    path.write_text("<root>")
    with pytest.raises(ParseError):
        read_pass_direction(path)
