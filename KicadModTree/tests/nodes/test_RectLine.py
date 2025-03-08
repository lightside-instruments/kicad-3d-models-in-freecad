import pytest

from KicadModTree import Line, RectLine, Vector2D
from KicadModTree.tests.test_utils import custom_assertions as CA
from kilibs.geom.geometric_util import geometricLine


@pytest.mark.parametrize(
    "start, end, layer, width",
    [
        ((0, 0), (1, 1), "F.SilkS", 0.1),
    ],
)
def test_Rect(start, end, layer, width):

    s = Vector2D(start)
    e = Vector2D(end)

    r = RectLine(start=s, end=e, layer=layer, width=width)

    # Check that the properties are set correctly
    assert r.start_pos == s
    assert r.end_pos == e
    assert r.layer == layer
    assert r.width == width

    # Flatten the object and check the output
    #
    # Rect is a base object, so it should flatten to itself
    serialised = r.serialize()

    lines = CA.assert_contains_n_of_type(serialised, 4, Line)

    exp_line_pts = [
        ((s.x, s.y), (e.x, s.y)),
        ((e.x, s.y), (e.x, e.y)),
        ((e.x, e.y), (s.x, e.y)),
        ((s.x, e.y), (s.x, s.y)),
    ]
    exp_lines = [
        geometricLine(start=Vector2D(p1), end=Vector2D(p2)) for p1, p2 in exp_line_pts
    ]

    actual_line_pts = []
    for line in lines:
        actual_line_pts.append(geometricLine(start=line.start_pos, end=line.end_pos))

    CA.assert_contains_lines(actual_line_pts, exp_lines)
