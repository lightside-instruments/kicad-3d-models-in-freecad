# -*- coding: utf8 -*-
#!/usr/bin/python
#
# CadQuery script returning Molex PicoFlex 90325 Connectors

## requirements
## freecad (v1.5 and v1.6 have been tested)
## cadquery FreeCAD plugin (v0.3.0 and v0.2.0 have been tested)
##   https://github.com/jmwright/cadquery-freecad-module

## This script can be run from within the cadquery module of freecad.
## To generate VRML/ STEP files for, use launch-cq-molex
## script of the parent directory.

# * This is a cadquery script for the generation of MCAD Models.             *
# *                                                                          *
# *   Copyright (c) 2016                                                     *
# * Rene Poeschl https://github.com/poeschlr                                 *
# * All trademarks within this guide belong to their legitimate owners.      *
# *                                                                          *
# *   This program is free software; you can redistribute it and/or modify   *
# *   it under the terms of the GNU General Public License (GPL)             *
# *   as published by the Free Software Foundation; either version 2 of      *
# *   the License, or (at your option) any later version.                    *
# *   for detail see the LICENCE text file.                                  *
# *                                                                          *
# *   This program is distributed in the hope that it will be useful,        *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
# *   GNU Library General Public License for more details.                   *
# *                                                                          *
# *   You should have received a copy of the GNU Library General Public      *
# *   License along with this program; if not, write to the Free Software    *
# *   Foundation, Inc.,                                                      *
# *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
# *                                                                          *
# * The models generated with this script add the following exception:       *
# *   As a special exception, if you create a design which uses this symbol, *
# *   and embed this symbol or unaltered portions of this symbol into the    *
# *   design, this symbol does not by itself cause the resulting design to   *
# *   be covered by the GNU General Public License. This exception does not  *
# *   however invalidate any other reasons why the design itself might be    *
# *   covered by the GNU General Public License. If you modify this symbol,  *
# *   you may extend this exception to your version of the symbol, but you   *
# *   are not obligated to do so. If you do not wish to do so, delete this   *
# *   exception statement from your version.                                 *
# ****************************************************************************

__title__ = "model description for Molex Picoflex 90325 series connectors"
__author__ = "hackscribble"
__Comment__ = "model description for Picoflex 90325 series connectors using cadquery"

___ver___ = "0.1 2017-08-09"


class LICENCE_Info:
    ############################################################################
    STR_licAuthor = "Ray Benitez"
    STR_licEmail = "hackscribble@outlook.com"
    STR_licOrgSys = ""
    STR_licPreProc = ""

    LIST_license = [
        "",
    ]
    ############################################################################


import cadquery as cq

# from Helpers import show
# from collections import namedtuple
# import FreeCAD

# class series_params():
#     series = "Picoflex"
#     series_long = 'Picoflex Ribbon-Cable Connectors'
#     manufacturer = 'Molex'
#     orientation = 'V'
#     number_of_rows = 2
#     datasheet = 'http://www.molex.com/pdm_docs/sd/903250004_sd.pdf'
#     mpn_format_string = "90325-00{pincount:02}"
#     mount_pin = ''

#     #pins_per_row per row
#     pinrange = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26)

#     body_color_key = "black body"
#     pins_color_key = "metal grey pins"
#     color_keys = [
#         body_color_key,
#         pins_color_key
#     ]
#     obj_suffixes = [
#         '__body',
#         '__pins'
#     ]

#     pitch = 1.27

#     pin_width = 0.3
#     pin_chamfer_long = 0.25
#     pin_chamfer_short = 0.12
#     pin_height =  4.0					# Heaight above bottom surface of base
#     pin_depth =   3.3					# Depth below bottom surface of base
#     pin_inside_distance = 2.525			# Distance between centre of end pin and end of body

#     pig_depth = 2.8                     # Depth below bottom surface of the plastic guidence pin
#     pig_height = 6.4                    # Height above bottom surface of the plastic guidence pin

# calcDim = namedtuple( 'calcDim', ['length'])


def dimensions(series_params, num_pins):
    length = (num_pins - 1) * series_params["pitch"] + 2 * series_params[
        "pin_inside_distance"
    ]
    return length


def generate_straight_pin(series_params):
    pin_width = series_params["pin_width"]
    pin_depth = series_params["pin_depth"]
    chamfer_long = series_params["pin_chamfer_long"]
    chamfer_short = series_params["pin_chamfer_short"]

    pin = (
        cq.Workplane("XY")
        .workplane(offset=0, centerOption="CenterOfMass")
        .moveTo(-pin_width / 2.0, -pin_width / 2.0)
        .rect(pin_width, pin_width, False)
        .extrude(-pin_depth)
    )

    pin = pin.faces("<Z").edges(">X").chamfer(chamfer_short, chamfer_short)
    pin = pin.faces("<Z").edges("<X").chamfer(chamfer_short, chamfer_short)
    pin = pin.faces("<Z").edges(">Y").chamfer(chamfer_short, chamfer_short)
    pin = pin.faces("<Z").edges("<Y").chamfer(chamfer_short, chamfer_short)

    return pin


def generate_pins(series_params, num_pins):
    pin_pitch = series_params["pitch"]
    pin_width = series_params["pin_width"]
    chamfer_long = series_params["pin_chamfer_long"]
    chamfer_short = series_params["pin_chamfer_short"]
    pin_height = series_params["pin_height"]

    pins = generate_straight_pin(series_params)

    for i in range(1, num_pins):
        pin = generate_straight_pin(series_params)
        if (i % 2) == 0:
            pins = pins.union(pin.translate((0, -(i * pin_pitch), 0)))
        else:
            pins = pins.union(pin.translate((2.54, -(i * pin_pitch), 0)))

    for i in range(0, num_pins):
        body_x = 0
        body_y = (-pin_width / 2.0) - (i * pin_pitch)
        pinTop = (
            cq.Workplane("XY")
            .workplane(offset=-pin_width / 2.0, centerOption="CenterOfMass")
            .moveTo(body_x, body_y)
            .rect(2.54, pin_width, False)
            .extrude(pin_height)
        )

        pinTop = (
            pinTop.faces(">Z").edges(">X").chamfer(2 * chamfer_long, 2 * chamfer_long)
        )
        pinTop = (
            pinTop.faces(">Z").edges("<X").chamfer(2 * chamfer_long, 2 * chamfer_long)
        )
        pinTop = pinTop.faces(">Z").edges(">Y").chamfer(chamfer_short, 2 * chamfer_long)
        pinTop = pinTop.faces(">Z").edges("<Y").chamfer(chamfer_short, 2 * chamfer_long)

        pins = pins.union(pinTop)

    return pins


def generate_body(series_params, num_pins):
    pin_inside_distance = series_params["pin_inside_distance"]
    pin_width = series_params["pin_width"]
    pin_pitch = series_params["pitch"]

    #
    # Main body block
    #
    body_block_width = 5.0
    body_block_height = 1.5
    body_block_x = -(body_block_width / 4)
    body_block_y = 2.525
    body_block_width = 5.0
    body_block_height = 1.5
    body_block_length = ((num_pins - 1) * series_params["pitch"]) + 5.05

    body_block = (
        cq.Workplane("XY")
        .workplane(offset=0, centerOption="CenterOfMass")
        .moveTo(body_block_x, body_block_y)
        .rect(body_block_width, -body_block_length, False)
        .extrude(body_block_height)
    )

    #    body_block = body_block.faces(">X").edges("<Y").chamfer(series_params['pin_chamfer_short / 2.0,series_params['pin_chamfer_short / 2.0)
    #    body_block = body_block.faces("<X").edges("<Y").chamfer(series_params['pin_chamfer_short / 2.0,series_params['pin_chamfer_short / 2.0)

    #
    # Remove the cutout in main block
    #
    body_width = 0.5
    body_length = (body_block_length / num_pins) / 2
    body_x = body_block_x
    body_y = body_block_y - (2 * body_length)
    body_y_end = body_y - body_block_length - (1 * body_length)
    body_height = body_block_height / 3.0
    while body_y > body_y_end:

        body = (
            cq.Workplane("XY")
            .workplane(offset=0, centerOption="CenterOfMass")
            .moveTo(body_x, body_y)
            .rect(body_width, body_length, False)
            .extrude(body_height)
        )
        body_block = body_block.cut(body)

        body = (
            cq.Workplane("XY")
            .workplane(offset=0, centerOption="CenterOfMass")
            .moveTo(body_x + body_block_width - body_width, body_y)
            .rect(body_width, body_length, False)
            .extrude(body_height)
        )
        body_block = body_block.cut(body)

        body = (
            cq.Workplane("XY")
            .workplane(
                offset=body_block_height - body_height, centerOption="CenterOfMass"
            )
            .moveTo(body_x, body_y)
            .rect(body_width, body_length, False)
            .extrude(body_height)
        )
        body_block = body_block.cut(body)

        body = (
            cq.Workplane("XY")
            .workplane(
                offset=body_block_height - body_height, centerOption="CenterOfMass"
            )
            .moveTo(body_x + body_block_width - body_width, body_y)
            .rect(body_width, body_length, False)
            .extrude(body_height)
        )
        body_block = body_block.cut(body)

        body_y = body_y - (2 * body_length)

    #
    # Add larger top pig
    #
    body_width = 1.0
    body_length = 3.0
    body_height = series_params["pig_height"]
    body_x = 1.27 - (body_length / 2)
    body_y = body_block_y - body_width

    body = (
        cq.Workplane("XY")
        .workplane(offset=0, centerOption="CenterOfMass")
        .moveTo(body_x, body_y)
        .rect(body_length, body_width, False)
        .extrude(body_height)
    )

    body = (
        body.faces(">Z")
        .edges(">X")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )
    body = (
        body.faces(">Z")
        .edges("<X")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )
    body = (
        body.faces(">Z")
        .edges("<Y")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )

    body_block = body_block.union(body)

    #
    # Add smaller top pig
    #
    body_width = 1.0
    body_length = 2.0
    body_height = series_params["pig_height"]
    body_x = body_block_x
    body_y = body_block_y - body_block_length

    body = (
        cq.Workplane("XY")
        .workplane(offset=0, centerOption="CenterOfMass")
        .moveTo(body_x, body_y)
        .rect(body_length, body_width, False)
        .extrude(body_height)
    )

    body = (
        body.faces(">Z")
        .edges(">X")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )
    body = (
        body.faces(">Z")
        .edges("<X")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )
    body = (
        body.faces(">Z")
        .edges("<Y")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )

    body_block = body_block.union(body)

    #
    # Add bottom pig at big top pig
    #
    body_x = -1.48
    body_y = 1.8
    body_height = series_params["pig_depth"] + (body_block_height / 2.0)

    body = (
        cq.Workplane("XY")
        .workplane(offset=(body_block_height / 2.0), centerOption="CenterOfMass")
        .moveTo(body_x, body_y)
        .circle(0.75)
        .extrude(-body_height, False)
    )

    body = (
        body.faces("<Z")
        .edges(">X")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )
    body_block = body_block.union(body)

    #
    # Add bottom pig at smaller top pig
    #
    body_x = -1.48
    body_y = -((num_pins - 1) * series_params["pitch"]) - 1.8
    body_height = series_params["pig_depth"] + (body_block_height / 2.0)

    body = (
        cq.Workplane("XY")
        .workplane(offset=(body_block_height / 2.0), centerOption="CenterOfMass")
        .moveTo(body_x, body_y)
        .circle(0.75)
        .extrude(-body_height, False)
    )

    body = (
        body.faces("<Z")
        .edges(">X")
        .chamfer(series_params["pin_chamfer_long"], series_params["pin_chamfer_long"])
    )
    body_block = body_block.union(body)

    return body_block, None


def generate_part(series_params, num_pins):
    # calc_dim = dimensions(num_pins)
    pins = generate_pins(series_params, num_pins)
    body, insert = generate_body(series_params, num_pins)

    #
    # Rotate and move, due to KiCad fucked up cordinate system where y is decreasing upwards above X axis
    #
    #    pins = pins.rotate((0,0,0), (0,0,1), 180).translate((2.54, 0, 0))
    #    body = body.rotate((0,0,0), (0,0,1), 180).translate((2.54, 0, 0))

    return (pins, body, insert)


# opened from within freecad
# if "module" in __name__:
#     part_to_build = 4

#     FreeCAD.Console.PrintMessage("Started from CadQuery: building " +
#                                  str(part_to_build) + "pins variant\n")
#     (body, pins) = generate_part(part_to_build)

#     show(pins)
#     show(body)
