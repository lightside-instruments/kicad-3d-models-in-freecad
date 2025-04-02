#!/usr/bin/env python

import math
import enum
from typing import Tuple, List, Union, Optional, Any

from KicadModTree import (
    Arc,
    Circle,
    Footprint,
    Line,
    Node,
    PolygonLine,
    RectLine,
    Pad,
)
from kilibs.geom import (
    Direction,
    Vector2D,
    BoundingBox,
    geometricCircle,
    geometricArc,
    geometricLine,
)
from kilibs.geom.rounding import (
    round_to_grid,
    round_to_grid_down,
    round_to_grid_up,
    round_to_grid_nearest,
)
from kilibs.geom.keepout import Keepout, KeepoutRect, KeepoutRound
from scripts.tools.footprint_global_properties import *
from scripts.tools.nodes import pin1_arrow


# round for grid g
def sqr(x):
    return x*x


# round for courtyard grid
def roundCrt(x):
    return round_to_grid(x, grid_crt)


def courtyardFromBoundingBox(bbox: BoundingBox, off: float, grid: float) -> dict:
    """
    Get a courtyard of the given box, with some offset, rounded to the grid

    :param bbox: bounding box of the body
    :param off: clearance
    :param grid: grid size to round to
    """
    return {
        'left': round_to_grid_down(bbox.left - off, grid),
        'right': round_to_grid_up(bbox.right + off, grid),
        'top': round_to_grid_down(bbox.top - off, grid),
        'bottom': round_to_grid_up(bbox.bottom + off, grid)
    }

# float-variant of range()
def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


# inclusice float-variant of range()
def frangei(x, y, jump):
    while x <= y:
        yield x
        x += jump


# returns a list with a single rectangle around x,y with width and height w and h
def addKeepoutRect(x, y, w, h):
    return [KeepoutRect(Vector2D(x, y), Vector2D(w, h))]


# returns a series of rectangle that lie around the circular pad around (x,y) with radius w=h
# if w!=h, addKeepoutRect() is called
def addKeepoutRound(x, y, w, h):
    if w != h:
        # Could do two circles and a rect if we cared enough
        return [KeepoutRect(Vector2D(x, y), Vector2D(w, h))]

    return [KeepoutRound(Vector2D(x, y), w / 2)]


def getKeepoutsForPads(pads: Pad | list[Pad], clearance: float) -> list[Keepout]:
    """
    Return suitable keepouts for the given pads.

    For the clearance, a common value may be 0.26 for the
    standard silk-pad clearance, for example.

    :param pads: Pad or list of pads
    :param clearance: clearance around pads
    :param keepout: keepout around pads
    :return: list of Keepout objects
    """

    kos = []
    pads = pads if isinstance(pads, list) else [pads]

    def get_shape_center(pad: Pad) -> Vector2D:

        center = Vector2D(pad.at)

        if pad.rotation == 0 or pad.rotation == 180:
            center += pad.offset
        elif pad.rotation == 90:
            center += Vector2D(pad.offset.y, pad.offset.x)
        elif pad.rotation == 270:
            center += Vector2D(-pad.offset.y, -pad.offset.x)
        else:
            raise ValueError(
                f"Pad rotation {pad.rotation} not supported for non-square pads"
            )

        return center

    for pad in pads:
        center = get_shape_center(pad)
        if pad.shape == Pad.SHAPE_CIRCLE:
            kos.append(KeepoutRound(center, pad.size.x / 2 + clearance))
        else:
            # Everything else.
            # ovals and roundrects can be more accurate if needed
            # by handling them as a circles + rects

            size = Vector2D(pad.size) + 2 * Vector2D(clearance, clearance)

            if pad.rotation == 0 or pad.rotation == 180:
                pass
            elif pad.rotation == 90 or pad.rotation == 270:
                size = Vector2D(pad.size.y, pad.size.x)
            else:
                # We'll need a polygonal keepout here
                raise ValueError(
                    f"Pad rotation {pad.rotation} not supported for non-square pads"
                )

            kos.append(KeepoutRect(center=pad.at, size=size))

    return kos


# internal method for keepout-processing
def applyKeepouts(
    items: List[Union[geometricLine, geometricCircle, geometricArc]],
    keepouts: List[Keepout],
) -> List[Union[geometricLine, geometricArc, geometricCircle]]:

    if len(keepouts) == 0:
        return items

    # Apply all the keepouts to a single line
    def applyKeepoutsToOneItem(item, kos: List[Keepout]):
        items = [item]

        for ko in kos:

            # Items left after applying this keepout
            new_items = []

            for i in items:
                kept_out: Optional[list[Any]] = []

                if isinstance(i, geometricLine):
                    kept_out = ko.keepout_line(i)
                elif isinstance(i, geometricCircle):
                    kept_out = ko.keepout_circle(i)
                elif isinstance(i, geometricArc):
                    kept_out = ko.keepout_arc(i)

                if kept_out is None:
                    # This keepout does not affect this item
                    new_items.append(i)
                else:
                    # Whatever is left after applying the keepout
                    new_items += kept_out

            # Once one Keepout has been applied, we need to apply the next one(s)
            # to the new items
            items = new_items

        return items

    new_parts = []

    for item in items:
        this_part_kept_out = applyKeepoutsToOneItem(item, keepouts)
        new_parts += this_part_kept_out

    return new_parts


# gives True if the given point (x,y) is contained in any keepout
def containedInAnyKeepout(p: Vector2D, keepouts: List[Keepout]) -> bool:
    for ko in keepouts:
        if ko.contains(p):
            return True
    return False


def renderKeepouts(
    keeouts: list[Keepout], layer: str = "Cmts.User", width: float = 0.1
) -> list[Node]:
    """
    Debugging function to render keepouts.

    Just add the returned nodes to the footprint to see the keepouts
    (e.g. with `mod.extend( renderKeepouts( keepouts ) ) )`)
    """

    nodes: list[Node] = []
    for ko in keeouts:
        if isinstance(ko, KeepoutRect):
            nodes.append(
                RectLine(
                    start=Vector2D(ko.left, ko.top),
                    end=Vector2D(ko.right, ko.bottom),
                    layer=layer,
                    width=width,
                )
            )
        elif isinstance(ko, KeepoutRound):
            nodes.append(
                Circle(
                    center=Vector2D(ko.center[0], ko.center[1]),
                    radius=ko.radius,
                    layer=layer,
                    width=width,
                )
            )
        else:
            raise ValueError(f"Unknown keepout type: {ko}")

    return nodes


def _add_kept_out(
    items: List[Union[geometricArc, geometricCircle, geometricLine]], layer, width, roun
) -> List[Node]:
    """
    Internal method to add the kept out items to the kicad_mod
    """

    tiny_threshold = width / 2

    # Prune tiny lines and arcs left over from keepout trims
    for item in items:

        tiny = False
        if isinstance(item, geometricLine):
            tiny = item.length < tiny_threshold
        elif isinstance(item, geometricArc):
            tiny = (
                item.start_pos - item.getMidPoint()
            ).norm() < tiny_threshold / 2

        if tiny:
            items.remove(item)

    nodes: list[Node] = []
    for item in items:
        # In here, round off coordinates to the nearest grid point,
        # but be mindful of the fact that we are rounding off to the nearest
        # grid point, not necessarily rounding away from zero (so 1.000003 should be
        # rounded to 1, not 1.01, say).

        if isinstance(item, geometricLine):
            nodes.append(
                Line(
                    start=[
                        round_to_grid_nearest(item.start_pos.x, roun),
                        round_to_grid_nearest(item.start_pos.y, roun),
                    ],
                    end=[
                        round_to_grid_nearest(item.end_pos.x, roun),
                        round_to_grid_nearest(item.end_pos.y, roun),
                    ],
                    layer=layer,
                    width=width,
                )
            )
        elif isinstance(item, geometricCircle):
            nodes.append(
                Circle(
                    center=[
                        round_to_grid_nearest(item.center_pos.x, roun),
                        round_to_grid_nearest(item.center_pos.y, roun),
                    ],
                    radius=round_to_grid_nearest(item.radius, roun),
                    layer=layer,
                    width=width,
                )
            )
        elif isinstance(item, geometricArc):
            nodes.append(
                Arc(
                    center=[
                        round_to_grid_nearest(item.center_pos.x, roun),
                        round_to_grid_nearest(item.center_pos.y, roun),
                    ],
                    start=[
                        round_to_grid_nearest(item.start_pos.x, roun),
                        round_to_grid_nearest(item.start_pos.y, roun),
                    ],
                    angle=item.angle,
                    layer=layer,
                    width=width,
                )
            )
        else:
            raise ValueError(f"Unknown geometric item: {item}")
    return nodes


def makeLineWithKeepout(line: geometricLine, layer, width, keepouts=[], roun=0.001):
    """
    Split an arbitrary line so it does not interfere with keepout areas
    """
    kept_out = applyKeepouts([line], keepouts)
    return _add_kept_out(kept_out, layer, width, roun)


def addLineWithKeepout(kicad_mod, line: geometricLine, layer, width, keepouts=[], roun=0.001):
    """Compatibility shim, prefer makeLineWithKeepout in new code"""
    nodes = makeLineWithKeepout(line, layer, width, keepouts, roun)
    for node in nodes:
        kicad_mod.append(node)


# split a horizontal line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts=[], roun=0.001, dashed=False):
    if dashed:
        addHDLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts, roun)
    else:
        # print("addHLineWithKeepout",y)
        line = geometricLine(start=[x0, y], end=[x1, y])
        addLineWithKeepout(kicad_mod, line, layer, width, keepouts, roun)


# split a vertical line so it does not interfere with keepout areas
def addVLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts=[], roun=0.001, dashed=False):
    if dashed:
        addVDLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts, roun)
    else:
        # print("addVLineWithKeepout",x)
        line = geometricLine(start=[x, y0], end=[x, y1])
        addLineWithKeepout(kicad_mod, line, layer, width, keepouts, roun)


def makeCircleWithKeepout(circle: geometricCircle, layer, width, keepouts=[], roun=0.001):
    """
    Draw a circle minding the keepouts
    """
    parts_out = applyKeepouts([circle], keepouts)
    return _add_kept_out(parts_out, layer, width, roun)


def addCircleWithKeepout(kicad_mod, x, y, radius, layer, width, keepouts=[], roun=0.001):
    """Compatibility shim, prefer makeCircleWithKeepout in new code"""
    c = geometricCircle(center=[x, y], radius=radius)
    nodes = makeCircleWithKeepout(c, layer, width, keepouts, roun)
    for node in nodes:
        kicad_mod.append(node)


def makeArcWithKeepout(arc: geometricArc, layer, width, keepouts=[], roun=0.001):
    """
    Draw an arc minding the keepouts
    """
    parts_out = applyKeepouts([arc], keepouts)
    return _add_kept_out(parts_out, layer, width, roun)


def addArcWithKeepout(kicad_mod, arc: geometricArc, layer, width, keepouts, roun):
    """Compatibility shim, prefer makeArcWithKeepout in new code"""
    nodes = makeArcWithKeepout(arc, layer, width, keepouts, roun)
    for node in nodes:
        kicad_mod.append(node)


# draw an arc
def addArcByAngles(kicad_mod, x, y, radius, angle_start, angle_end, layer, width, roun=0.001):
    startx = x + radius * math.sin(angle_start/180*3.1415)
    starty = y + radius * math.cos(angle_start/180*3.1415)
    kicad_mod.append( Arc(center=[round_to_grid(x, roun), round_to_grid(y, roun)], start=[round_to_grid(startx, roun), round_to_grid(starty, roun)], angle=-(angle_end-angle_start), layer=layer, width=width))

# draw an arc minding the keepouts
def addArcByAnglesWithKeepout(kicad_mod, x, y, radius, angle_start, angle_end, layer, width, keepouts=[], roun=0.001):
    startx = x + radius * math.sin(angle_start/180*3.1415)
    starty = y + radius * math.cos(angle_start/180*3.1415)
    arc = geometricArc(center=[x, y], start=[startx, starty], angle=-(angle_end-angle_start))
    addArcWithKeepout(kicad_mod, arc, layer, width, keepouts, roun)

# draw an ellipse with one axis along x-axis and one axis along y-axis and given width/height
def addEllipse(kicad_mod, x, y, w, h, layer, width, roun=0.001):
    factor=h/w
    alpha=math.atan(h/w)*2
    radius=w/2/math.sin(alpha)
    addArcByAngles(kicad_mod=kicad_mod, x=x, y=y+radius*math.cos(alpha), radius=radius, angle_start=180-alpha/3.1415*180, angle_end=180+alpha/3.1415*180, layer=layer, width=width, roun=roun);
    addArcByAngles(kicad_mod=kicad_mod, x=x, y=y-radius*math.cos(alpha), radius=radius, angle_start=alpha/3.1415*180, angle_end=-alpha/3.1415*180, layer=layer, width=width, roun=roun);

# draw an ellipse with one axis along x-axis and one axis along y-axis and given width/height
def addEllipseWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    factor=h/w
    alpha=math.atan(h/w)*2
    radius=w/2/math.sin(alpha)
    addArcByAnglesWithKeepout(kicad_mod=kicad_mod, x=x, y=y+radius*math.cos(alpha), radius=radius, angle_start=180-alpha/3.1415*180, angle_end=180+alpha/3.1415*180, keepouts=keepouts, layer=layer, width=width, roun=roun);
    addArcByAnglesWithKeepout(kicad_mod=kicad_mod, x=x, y=y-radius*math.cos(alpha), radius=radius, angle_start=alpha/3.1415*180, angle_end=-alpha/3.1415*180, keepouts=keepouts, layer=layer, width=width, roun=roun);

# split an arbitrary line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addPolyLineWithKeepout(kicad_mod, poly, layer, width, keepouts=[], roun=0.001):
    if len(poly) > 1:
        for p in range(0, len(poly) - 1):
            line = geometricLine(start=poly[p], end=poly[p+1])
            addLineWithKeepout(kicad_mod, line, layer, width, keepouts, roun)


def makePrimitivesWithKeepout(primitives: list[geometricLine | geometricArc | geometricCircle],
                                layer: str, width: float, keepouts: list[Keepout], roun=0.001) -> list[Node]:
    """
    Turn a list of primitives into a list of nodes, keeping the keepouts in mind.

    Eventually we should do this with a transparent Keepout Node, as that will handle Translations, say,
    but for now this centralises logic.
    """
    kept_out_prims = applyKeepouts(primitives, keepouts)
    return _add_kept_out(kept_out_prims, layer, width, roun)


# draw a circle with a screw slit under 45 degrees
def addSlitScrew(kicad_mod, c, radius, layer, width, keepouts=[], roun=0.001):
    """
    Draw a circle with a screw slit under 45 degrees

    :param keepouts: list of keepouts (can be empty)
    """
    c = Vector2D(c)

    addCircleWithKeepout(kicad_mod, c.x, c.y, radius, layer, width, keepouts, roun)

    da = 5
    dx1 = 0.99 * radius * math.sin((135 - da) / 180 * 3.1415)
    dy1 = 0.99 * radius * math.cos((135 - da) / 180 * 3.1415)
    dx2 = 0.99 * radius * math.sin((135 + da) / 180 * 3.1415)
    dy2 = 0.99 * radius * math.cos((135 + da) / 180 * 3.1415)
    dx3 = 0.99 * radius * math.sin((315 - da) / 180 * 3.1415)
    dy3 = 0.99 * radius * math.cos((315 - da) / 180 * 3.1415)
    dx4 = 0.99 * radius * math.sin((315 + da) / 180 * 3.1415)
    dy4 = 0.99 * radius * math.cos((315 + da) / 180 * 3.1415)

    line1 = geometricLine(start=c + [dx1, dy1], end=c + [dx4, dy4])
    line2 = geometricLine(start=c + [dx2, dy2], end=c + [dx3, dy3])

    addLineWithKeepout(kicad_mod, line1, layer, width, keepouts)
    addLineWithKeepout(kicad_mod, line2, layer, width, keepouts)


def addCrossScrew(kicad_mod, c, radius, layer, width, keepouts=[], roun=0.001):
    """
    Draw a circle with a cross-screw under 45 degrees

    :param keepouts: list of keepouts (can be empty)
    """
    c = Vector2D(c)
    dw = 0.75 * radius

    addCircleWithKeepout(kicad_mod, c.x, c.y, radius, layer, width, keepouts, roun)
    addHLineWithKeepout(kicad_mod, c.x - dw, c.x + dw, c.y, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, c.x, c.y - dw, c.y + dw, layer, width, keepouts, roun)

# split a dashed horizontal line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHDLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts=[], roun=0.001):
    dx=3*width
    x=min(x0,x1)
    while x<max(x0,x1):
        addHLineWithKeepout(kicad_mod, x,min(x+dx,x1), y, layer, width, keepouts, roun)
        x=x+dx*2

# split a dashed vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addVDLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts=[], roun=0.001):
    dy = 3 * width
    y = min(y0, y1)
    while y < max(y0, y1):
        addVLineWithKeepout(kicad_mod, x, y, min(y1,y+dy), layer, width, keepouts, roun)
        y = y + dy * 2


# split a rectangle
def addRectWith(kicad_mod, x, y, w, h, layer, width, roun=0.001):
	kicad_mod.append(RectLine(start=[round_to_grid(x, roun),round_to_grid(y, roun)], end=[round_to_grid(x+w, roun),round_to_grid(y+h, roun)], layer=layer, width=width))


# split a rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addRectWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)

# split a rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addRectAndTLMarkWithKeepout(kicad_mod, x, y, w, h, mark_len, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)
    addHLineWithKeepout(kicad_mod, x-2*width, x+mark_len, y-2*width, layer,width,keepouts,roun)
    addVLineWithKeepout(kicad_mod, x-2*width, y-2*width, y+mark_len, layer,width,keepouts,roun)


# split a dashed rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addDRectWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHDLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHDLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVDLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVDLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)

# split a plus sign so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addPlusWithKeepout(km, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(km, x, x+w, y+h/2, layer,width,keepouts,roun)
    addVLineWithKeepout(km, x+w/2, y, y+h, layer, width, keepouts, roun)

# draw a rectangle with bevel on all sides (e.g. for crystals), or a simple rectangle if bevel_size0=0)
#
#   /----\
#  /      \
# |        |
# |        |
# |        |
# |        |
# |        |
#  \      /
#   \----/
def allBevelRect(model, x, size, layer, width, bevel_size=0.2):
    if bevel_size <= 0:
        model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    else:
        model.append(PolygonLine(polygon=[[x[0] + bevel_size, x[1]],
                                           [x[0] + size[0] - bevel_size, x[1]],
                                           [x[0] + size[0], x[1] + bevel_size],
                                           [x[0] + size[0], x[1] + size[1] - bevel_size],
                                           [x[0] + size[0] - bevel_size, x[1] + size[1]],
                                           [x[0] + bevel_size, x[1] + size[1]],
                                           [x[0], x[1] + size[1] - bevel_size],
                                           [x[0], x[1] + bevel_size],
                                           [x[0] + bevel_size, x[1]]], layer=layer, width=width))

# draw a downward equal-sided triangle
def allEqualSidedDownTriangle(model, xcenter, side_length, layer, width):
    h=math.sqrt(3)/6*side_length
    model.append(PolygonLine(polygon=[[xcenter[0] - side_length / 2, xcenter[1] - h],
                                       [xcenter[0]+side_length/2, xcenter[1]-h],
                                       [xcenter[0], xcenter[1]+2*h],
                                       [xcenter[0]-side_length/2, xcenter[1]-h],
                                       ], layer=layer, width=width))

# draws a filled circle consisting of concentric circles of varying widths (e.g. for glue dots!)
def fillCircle(model, center, radius, layer, width):
    model.append(Circle(center=center, radius=radius, layer=layer, width=width))
    r = radius
    w = radius / 3
    r = radius - w / 2
    while r > w / 2:
        if r - 0.9 * w <= w / 2:
            model.append(Circle(center=center, radius=r, layer=layer, width=r * 2))
        else:
            model.append(Circle(center=center, radius=r, layer=layer, width=w))
        r = r - 0.9 * w


#     +------+
#    /       |
#   /        |
#   |        |
#   |        |
#   |        |
#   |        |
#   +--------+
#
#
def bevelRectTL(model, x, size, layer, width, bevel_size=1):
    model.append(PolygonLine(
        polygon=[[x[0] + bevel_size, x[1]], [x[0] + size[0], x[1]], [x[0] + size[0], x[1] + size[1]],
                  [x[0], x[1] + size[1]], [x[0], x[1] + bevel_size], [x[0] + bevel_size, x[1]]], layer=layer,
        width=width))


#   +--------+
#   |        |
#   |        |
#   |        |
#   |        |
#   \        |
#    \       |
#     +------+
#
#
def bevelRectBL(model, x, size, layer, width, bevel_size=1):
    model.append(PolygonLine(polygon=[[x[0], x[1]], [x[0] + size[0], x[1]], [x[0] + size[0], x[1] + size[1]],
                                       [x[0] + bevel_size, x[1] + size[1]], [x[0], x[1] + size[1] - bevel_size],
                                       [x[0], x[1]]], layer=layer, width=width))

# draws a DIP-package with half-circle at the top
#
# +----------+
# |   \  /   |
# |    ~~    |
# |          |
# |          |
# |          |
# |          |
# +----------+
def DIPRectT(model, x, size, layer, width, marker_size=2):
    model.append(PolygonLine(
        polygon=[[x[0] + size[0] / 2 - marker_size / 2, x[1]], [x[0], x[1]], [x[0], x[1] + size[1]],
                  [x[0] + size[0], x[1] + size[1]], [x[0] + size[0], x[1]],
                  [x[0] + size[0] / 2 + marker_size / 2, x[1]]], layer=layer, width=width))
    model.append(Arc(center=[x[0] + size[0] / 2, x[1]], start=[x[0] + size[0] / 2 - marker_size / 2, x[1]], angle=-180,
                     layer=layer, width=width))


# draws a DIP-package with half-circle at the left
#
# +---------------+
# |-\             |
# |  |            |
# |-/             |
# +---------------+
def DIPRectL(model, x, size, layer, width, marker_size=2):
    model.append(PolygonLine(polygon=[[x[0], x[1] + size[1] / 2 - marker_size / 2],
                                       [x[0], x[1]],
                                       [x[0] + size[0], x[1]],
                                       [x[0] + size[0], x[1] + size[1]],
                                       [x[0], x[1] + size[1]],
                                       [x[0], x[1] + size[1] / 2 + marker_size / 2]], layer=layer, width=width))
    model.append(Arc(center=[x[0], x[1] + size[1] / 2], start=[x[0], x[1] + size[1] / 2 - marker_size / 2], angle=180,
                     layer=layer, width=width))


# draws the left part of a DIP-package with half-circle at the left
#
# +--------
# |-\
# |  |
# |-/
# +--------
def DIPRectL_LeftOnly(model, x, size, layer, width, marker_size=2):
    model.append(Line(start=[x[0], x[1] + size[1] / 2 - marker_size / 2], end=[x[0], x[1]], layer=layer, width=width))
    model.append(
        Line(start=[x[0], x[1] + size[1]], end=[x[0], x[1] + size[1] / 2 + marker_size / 2], layer=layer, width=width))
    if size[0] > 0:
        model.append(Line(start=[x[0], x[1]], end=[x[0] + size[0], x[1]], layer=layer, width=width))
        model.append(Line(start=[x[0], x[1] + size[1]], end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))

    model.append(Arc(center=[x[0], x[1] + size[1] / 2], start=[x[0], x[1] + size[1] / 2 - marker_size / 2], angle=180,
                     layer=layer, width=width))


# draws a THT quartz footprint (HC49) with a rect around it
#  +-------------------------+
#  |                         |
#  |   +----------------+    |
#  |  /                  \   |
#  |  \                  /   |
#  |   +----------------+    |
#  |                         |
#  +-------------------------+
def THTQuartzRect(model, x, size, inner_size, layer, width):
    model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    THTQuartz(model, [x[0] + (size[0] - inner_size[0]) / 2, x[1] + (size[1] - inner_size[1]) / 2], inner_size, layer,
              width)


# draws a THT quartz footprint (HC49)
#     +----------------+
#    /                  \
#    \                  /
#     +----------------+
def THTQuartz(model, x, size, layer, width):
    THTQuartzIncomplete(model, x, size, 180, layer, width)


# draws a THT quartz footprint (HC49)
#     +----------------+
#    /                  \
#    \                  /
#     +----------------+
def THTQuartzIncomplete(model, x, size, angle, layer, width):
    inner_size = size
    r = inner_size[1] / 2
    xtl = [x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2 - inner_size[1] / 2]
    xtr = [x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2 - inner_size[1] / 2]
    xbl = [x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2 + inner_size[1] / 2]
    xbr = [x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2 + inner_size[1] / 2]
    cl = [x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2]
    cr = [x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2]
    model.append(Line(start=xtl, end=xtr, layer=layer, width=width))
    model.append(Line(start=xbl, end=xbr, layer=layer, width=width))
    if angle >= 180:
        model.append(Arc(center=cl, start=xtl, angle=-angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xtr, angle=angle, layer=layer, width=width))
    else:
        model.append(Arc(center=cl, start=xtl, angle=-angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xtr, angle=angle, layer=layer, width=width))
        model.append(Arc(center=cl, start=xbl, angle=angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xbr, angle=-angle, layer=layer, width=width))


def CornerBracketWithArrowPointingSouthEast(model: Footprint, apex: Vector2D,
                                            arrow_size: float,
                                            arrow_length: float,
                                            bracket_max_x: float,
                                            bracket_max_y: float,
                                            layer: str,
                                            line_width_mm: float,
                                            silk_min_len: float):
    """Create an south-east triangular arrow and 90-degree bracket lines

      +
     /|
    +-+  ---
            | bracket_max_x
      |
      | __bracket_max_y

    """
    # minimum clearance between nodes of the lines
    silk_silk_node_clearance = 2 * line_width_mm

    model.append(
        pin1_arrow.Pin1SilkScreenArrow45Deg(
            apex, Direction.SOUTHEAST, arrow_size, layer, line_width_mm)
        )

    pin_1_silk_line_len_x = bracket_max_x - (apex.x + silk_silk_node_clearance)
    pin_1_silk_line_len_y = bracket_max_y - (apex.y + silk_silk_node_clearance)

    # There's a gap to avoid merging with the arrow
    # make sure there's enough line left to draw the lines

    if pin_1_silk_line_len_x > silk_min_len:
        tl_horz_line = Line(
            start=Vector2D(apex.x + 2 * line_width_mm, apex.y),
            end=Vector2D(bracket_max_x, apex.y),
            width=line_width_mm)
        model.append(tl_horz_line)

    if pin_1_silk_line_len_y > silk_min_len:
        tl_vert_line = Line(
            start=Vector2D(apex.x, apex.y + 2 * line_width_mm),
            end=Vector2D(apex.x, bracket_max_y),
            width=line_width_mm)
        model.append(tl_vert_line)


def CornerBracketWithArrowPointingSouth(model: Footprint, apex: Vector2D,
                                        arrow_size: float,
                                        arrow_length: float,
                                        bracket_max_x: float,
                                        bracket_max_y: float,
                                        layer: str,
                                        line_width_mm: float,
                                        silk_min_len: float):
    r"""Create an south-east triangular arrow and 90-degree bracket lines

    Move the whole triangle left if it will hit the pad on the right.

    +---+
     \ /
      +  ---
            | bracket_max_x
      |
      | __bracket_max_y

    """

    # minimum clearance between nodes of the lines
    silk_silk_node_clearance = 2 * line_width_mm

    # shove arrow left away from the pad on the right
    apex.x = min(apex.x, bracket_max_x - arrow_size / 2)

    # Round the apex away from the body corner
    apex.x = round_to_grid_down(apex.x, 0.01)
    apex.y = round_to_grid_down(apex.y, 0.01)

    model.append(
        pin1_arrow.Pin1SilkscreenArrow(
            apex, Direction.SOUTH, arrow_size, arrow_length, layer, line_width_mm
        )
    )

    # a little extra clearance on the side of the arrow
    pin_1_silk_line_len_x = bracket_max_x - (apex.x + silk_silk_node_clearance + line_width_mm / 2)
    pin_1_silk_line_len_y = bracket_max_y - (apex.y + silk_silk_node_clearance)

    # There's a gap to avoid merging with the arrow
    # make sure there's enough line left to draw the lines

    if pin_1_silk_line_len_x > silk_min_len:
        tl_horz_line = Line(
            start=Vector2D(bracket_max_x, apex.y),
            end=Vector2D(bracket_max_x - pin_1_silk_line_len_x, apex.y),
            width=line_width_mm)
        model.append(tl_horz_line)

    if pin_1_silk_line_len_y > silk_min_len:
        tl_vert_line = Line(
            start=Vector2D(apex.x, bracket_max_y),
            end=Vector2D(apex.x, bracket_max_y - pin_1_silk_line_len_y),
            width=line_width_mm)
        model.append(tl_vert_line)


class SilkArrowSize(enum.Enum):
    """
    Silkscreen arrow edge length in mm.
    """
    SMALL = 0.4
    MEDIUM = 0.6
    LARGE = 0.8
    HUGE = 1.0  # IPC maximum


def getStandardSilkArrowSize(size: SilkArrowSize,
                             silk_line_width: float) -> Tuple[float, float]:
    """
    Get the normal size of the arrow for a given enum value.

    This gives the "node-node" size.
    """
    # slight squashed relative to equilateral triangle
    # reduces intrusion of arrows into other footprints' spaces
    standard_arrow_aspect_ratio = 0.7

    # allows for 0.01mm grid-snap on each side of the apex
    width = round_to_grid_down(size.value - silk_line_width, 0.02)
    length = round_to_grid_down(width * standard_arrow_aspect_ratio, 0.01)

    return width, length


#
# This is an alternative to using silk keepout areas for simple cases.
# It calculates a new endpoint for a horizontal or vertical line such that
# the silk line has the correct minimal clearance. If the line is to short
# given the default clearance, the clearance is reduced and new points are
# calculated.
#
# Parameters:
#   - pad_size, pad_position, and pad_radius are the dimensions of the reference pad.
#     (pad that is expected to be intersected by the line)
#   - fixed_point: The fixed reference point
#   - moving_point: The point that will be moved (toward the fixed point)
#     if the line intersects the pads clearance area.
#   - silk_pad_offset: offset between edge of the pad and silk line center.
#   - min_length: minimum silk line length
#
# Returns a new point along the line or None if no valid point could be found
#
def nearestSilkPointOnOrthogonalLineSmallClerance(pad_size, pad_position, pad_radius, fixed_point, moving_point,
        silk_pad_offset_default, silk_pad_offset_reduced, min_length):
    if silk_pad_offset_reduced < silk_pad_offset_default:
        offset = (silk_pad_offset_default, silk_pad_offset_reduced)
    else:
        offset = (silk_pad_offset_default)

    for silk_pad_offset in (silk_pad_offset_default, silk_pad_offset_reduced):
        point = nearestSilkPointOnOrthogonalLine(
                pad_size, pad_position, pad_radius, fixed_point, moving_point,
                silk_pad_offset, min_length)
        if point is not None:
            return point
    return None

#
# This is an alternative to using silk keepout areas for simple cases.
# It calculates a new endpoint for a horizontal or vertical line such that
# the silk line has the correct minimal clearance.
#
# Parameters:
#   - pad_size, pad_position, and pad_radius are the dimensions of the reference pad.
#     (pad that is expected to be intersected by the line)
#   - fixed_point: The fixed reference point
#   - moving_point: The point that will be moved (toward the fixed point)
#     if the line intersects the pads clearance area.
#   - silk_pad_offset: offset between edge of the pad and silk line center.
#   - min_length: minimum silk line length
#
# Returns a new point along the line or None if no valid point could be found
#
def nearestSilkPointOnOrthogonalLine(pad_size, pad_position, pad_radius, fixed_point, moving_point,
        silk_pad_offset, min_length):
    if fixed_point[0] == moving_point[0]:
        normal_dir_idx = 0
    elif fixed_point[1] == moving_point[1]:
        normal_dir_idx = 1
    else:
        raise ValueError("nearestSilkPointOnOrthogonalLine only works for horizontal or vertical lines. \n"
                        "(Either x or y coordinate of the two reference points must be equal)")

    inline_dir_idx = (normal_dir_idx+1)%2

    line_pad_offset = fixed_point[normal_dir_idx] - pad_position[normal_dir_idx]

    rc_normal_dir = pad_size[normal_dir_idx]/2-pad_radius

    sign = 1 if pad_position[inline_dir_idx] - fixed_point[inline_dir_idx] > 0 else -1
    ep_new = Vector2D(moving_point)

    if rc_normal_dir < line_pad_offset:
        # the silk outline is in the area where the radius of the pad is.

        dr_normal_dir = line_pad_offset - rc_normal_dir

        r = pad_radius + silk_pad_offset

        # rounding to avoid floating point errors
        if round(dr_normal_dir, 6) >= round(r, 6):
            return moving_point

        dr_inline = math.sqrt(r**2 - dr_normal_dir**2)

        ep_new[inline_dir_idx] =  pad_position[inline_dir_idx] -\
            sign*(pad_size[inline_dir_idx]/2 - (pad_radius-dr_inline))
    else:
        ep_new[inline_dir_idx] =  pad_position[inline_dir_idx] -\
            sign*(pad_size[inline_dir_idx]/2 + silk_pad_offset)

    if sign*(ep_new[inline_dir_idx] - fixed_point[inline_dir_idx]) <  min_length:
        return None

    if abs(ep_new[inline_dir_idx] - fixed_point[inline_dir_idx]) > math.fabs(moving_point[inline_dir_idx] - fixed_point[inline_dir_idx]):
        return moving_point

    return ep_new

#
# Check if c point intersects the line segment from a to b points
#
# Parameters:
#    a: point coordinates as Vector2D
#    b: point coordinates as Vector2D
#    c: point coordinates as Vector2D
#
# Return iff point c intersects the line segment from a to b.
#
# Code adapted from post from Darius Bacon (code posted at 2008) at:
# https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
#
# StackOverflow licensing is CC BY-SA 2.5. Check at: https://stackoverflow.com/help/licensing
#
def point_is_on_segment(a, b, c):
    "Return true iff point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    return (collinear_points(a, b, c)
            and (point_within(a.x, c.x, b.x) if a.x != b.x else
                 point_within(a.y, c.y, b.y)))

#
# Check if a,b,c points all lie on the same line.
#
# Parameters:
#    a: point coordinates as Vector2D
#    b: point coordinates as Vector2D
#    c: point coordinates as Vector2D
#
# Return true iff a, b, and c all lie on the same line.
#
# Code adapted from post from Darius Bacon (code posted at 2008) at:
# https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
#
# StackOverflow licensing is CC BY-SA 2.5. Check at: https://stackoverflow.com/help/licensing
#
def collinear_points(a, b, c):
    "Return true iff a, b, and c all lie on the same line."
    if  ( abs(((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y)) )) <= 0.000001:
        return True
    else:
        return False

#
# Check if q point is between p and r points
#
# Parameters:
#    p: scalar coordinate
#    q: scalar coordinate
#    r: scalar coordinate
#
# Return true iff q is between p and r (inclusive).
#
# Code adapted from post from Darius Bacon (code posted at 2008) at:
# https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
#
# StackOverflow licensing is CC BY-SA 2.5. Check at: https://stackoverflow.com/help/licensing
#
def point_within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p
