#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This is derived from a cadquery script for generating PDIP models in X3D format
#
# from https://bitbucket.org/hyOzd/freecad-macros
# author hyOzd
# This is a
# Dimensions are from Microchips Packaging Specification document:
# DS00000049BY. Body drawing is the same as QFP generator#

## requirements
## cadquery FreeCAD plugin
##   https://github.com/jmwright/cadquery-freecad-module

## to run the script just do: freecad main_generator.py modelName
## e.g. c:\freecad\bin\freecad main_generator.py DIP8

## the script will generate STEP and VRML parametric models
## to be used with kicad StepUp script

# * These are a FreeCAD & cadquery tools                                     *
# * to export generated models in STEP & VRML format.                        *
# *                                                                          *
# * cadquery script for generating QFP/SOIC/SSOP/TSSOP models in STEP AP214  *
# *   Copyright (c) 2015                                                     *
# * Maurice https://launchpad.net/~easyw                                     *
# * All trademarks within this guide belong to their legitimate owners.      *
# *                                                                          *
# *   This program is free software; you can redistribute it and/or modify   *
# *   it under the terms of the GNU Lesser General Public License (LGPL)     *
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
# ****************************************************************************


# import cq_parameters  # modules parameters
# from cq_parameters import *

from collections import namedtuple
from collections.abc import Mapping

import cadquery as cq


class cq_parameters_StarMicronics_HMB_06_HMB_12:

    def __init__(self):
        x = 0

    # def get_dest_3D_dir(self):
    #     return 'Buzzer_Beeper.3dshapes'

    # def model_exist(self, modelName):
    #     for n in self.all_params:
    #         if n == modelName:
    #             return True

    #     return False

    # def get_list_all(self):
    #     list = []
    #     for n in self.all_params:
    #         list.append(n)

    #     return list

    # def make_3D_model(self, modelName):

    #     destination_dir = self.get_dest_3D_dir()

    #     case = self.make_case(self.all_params[modelName])
    #     pins = self.make_pins(self.all_params[modelName])
    #     show(case)
    #     show(pins)

    #     doc = FreeCAD.ActiveDocument
    #     objs=GetListOfObjects(FreeCAD, doc)

    #     body_color_key = self.all_params[modelName].body_color_key
    #     pin_color_key = self.all_params[modelName].pin_color_key

    #     body_color = shaderColors.named_colors[body_color_key].getDiffuseFloat()
    #     pin_color = shaderColors.named_colors[pin_color_key].getDiffuseFloat()

    #     Color_Objects(Gui,objs[0],body_color)
    #     Color_Objects(Gui,objs[1],pin_color)

    #     col_body=Gui.ActiveDocument.getObject(objs[0].Name).DiffuseColor[0]
    #     col_pin=Gui.ActiveDocument.getObject(objs[1].Name).DiffuseColor[0]

    #     material_substitutions={
    #         col_body[:-1]:body_color_key,
    #         col_pin[:-1]:pin_color_key,
    #     }

    #     expVRML.say(material_substitutions)
    #     while len(objs) > 1:
    #             FuseObjs_wColors(FreeCAD, FreeCADGui, doc.Name, objs[0].Name, objs[1].Name)
    #             del objs
    #             objs = GetListOfObjects(FreeCAD, doc)

    #     return material_substitutions

    def make_case(self, params):

        D = params["D"]  # package length
        E = params["E"]  # body overall width
        H = params["H"]  # body overall height
        A1 = params["A1"]  # package height
        pin = params["pin"]  # Pins
        npthhole = params["npthhole"]  # NPTH hole diameter
        rotation = params["rotation"]  # Rotation if required
        center = params["center"]  # Body center

        #
        #
        #
        x = center[0]
        y = center[1]

        case = (
            cq.Workplane("XY")
            .workplane(offset=A1)
            .moveTo(x, y)
            .circle(D / 2.0, False)
            .extrude(H)
        )
        case = case.faces("<Z").edges(">Y").fillet(D / 40.0)

        case1 = (
            cq.Workplane("XY")
            .workplane(offset=A1 + H - 2.5)
            .moveTo(x, y)
            .circle(D / 2.0 + 2.0, False)
            .extrude(4.0)
        )
        case2 = (
            cq.Workplane("XY")
            .workplane(offset=A1 + H - 2.5)
            .moveTo(x, y)
            .circle(7.0, False)
            .extrude(4.0)
        )
        case1 = case1.cut(case2)
        case = case.cut(case1)
        #
        # hole in top
        #
        case1 = (
            cq.Workplane("XY")
            .workplane(offset=A1 + (H - 2.0))
            .moveTo(x, y)
            .circle(npthhole / 2.0, False)
            .extrude(4.0)
        )
        case = case.cut(case1)

        #
        # Cut bottom
        #
        case1 = (
            cq.Workplane("XY")
            .workplane(offset=A1)
            .moveTo(0, 0)
            .rect(4.0, 30.0)
            .extrude(0.5)
        )
        case1 = case1.rotate((0, 0, 0), (0, 0, 1), 60)
        case1 = case1.translate((x, y))
        case = case.cut(case1)
        #
        case1 = (
            cq.Workplane("XY")
            .workplane(offset=A1)
            .moveTo(0, 0)
            .rect(4.0, 30.0)
            .extrude(0.5)
        )
        case1 = case1.rotate((0, 0, 0), (0, 0, 1), 120)
        case1 = case1.translate((x, y))
        case = case.cut(case1)
        #
        case1 = (
            cq.Workplane("XY")
            .workplane(offset=A1)
            .moveTo(0, 0)
            .rect(4.0, 30.0)
            .extrude(0.5)
        )
        case1 = case1.rotate((0, 0, 0), (0, 0, 1), 180)
        case1 = case1.translate((x, y))
        case = case.cut(case1)
        #
        case = case.faces(">Z").edges(">Y").fillet(D / 40.0)

        if rotation != 0:
            case = case.rotate((0, 0, 0), (0, 0, 1), rotation)

        return case

    def make_pins(self, params):

        D = params["D"]  # package length
        H = params["H"]  # body overall height
        A1 = params["A1"]  # Body seperation height
        b = params["b"]  # pin diameter or pad size
        ph = params["ph"]  # pin length
        rotation = params["rotation"]  # rotation if required
        pin = params["pin"]  # pin/pad cordinates
        center = params["center"]  # Body center

        p = pin[0]
        pins = (
            cq.Workplane("XY")
            .workplane(offset=A1 + 1.0)
            .moveTo(p[0], -p[1])
            .circle(b / 2.0, False)
            .extrude(0 - (ph + A1 + 1.0))
        )
        pins = pins.faces("<Z").fillet(b / 5.0)

        for i in range(1, len(pin)):
            p = pin[i]
            pint = (
                cq.Workplane("XY")
                .workplane(offset=A1 + 1.0)
                .moveTo(p[0], -p[1])
                .circle(b / 2.0, False)
                .extrude(0 - (ph + A1 + 1.0))
            )
            pint = pint.faces("<Z").fillet(b / 5.0)
            pins = pins.union(pint)

        if rotation != 0:
            pins = pins.rotate((0, 0, 0), (0, 0, 1), rotation)

        return pins

    ##enabling optional/default values to None
    def namedtuple_with_defaults(typename, field_names, default_values=()):

        T = namedtuple(typename, field_names)
        T.__new__.__defaults__ = (None,) * len(T._fields)
        if isinstance(default_values, Mapping):
            prototype = T(**default_values)
        else:
            prototype = T(*default_values)
        T.__new__.__defaults__ = tuple(prototype)
        return T

    Params = namedtuple_with_defaults(
        "Params",
        [
            "modelName",  # modelName
            "D",  # Body width/diameter
            "E",  # Body length
            "H",  # Body height
            "A1",  # Body PCB seperation
            "b",  # pin width
            "center",  # Body center
            "npthhole",  # NPTH hole diameter
            "ph",  # Pin length
            "pin",  # Pins
            "body_color_key",  # Body colour
            "pin_color_key",  # Pin color
            "rotation",  # Rotation if required
            "dest_dir_prefix",  # Destination directory
        ],
    )

    # all_params = {

    #     'MagneticBuzzer_StarMicronics_HMB-06_HMB-12': Params(
    #         #
    #         # Valve
    #         # This model have been auto generated based on the foot print file
    #         # A number of parameters have been fixed or guessed, such as A2
    #         #
    #         # The foot print that uses this 3D model is MagneticBuzzer_StarMicronics_HMB-06_HMB-12.kicad_mod
    #         #
    #         modelName = 'MagneticBuzzer_StarMicronics_HMB-06_HMB-12',   # modelName
    #         D = 16.00,                  # Body width/diameter
    #         H = 14.00,                  # Body height
    #         A1 = 0.03,                  # Body-board separation
    #         b = 0.70,                   # Pin diameter
    #         center = (3.81, 0.00),      # Body center
    #         npthhole = 3.2,             # NPTH hole diameter
    #         ph = 6.0,                   # Pin length
    #         pin = [(0.0, 0.0), (7.61, 0.00)],   # Pins
    #         body_color_key = 'black body',      # Body color
    #         pin_color_key = 'metal grey pins',  # Pin color
    #         rotation = 0,                       # Rotation if required
    #         dest_dir_prefix = '../Buzzer_Beeper.3dshapes',      # destination directory
    #         ),
    # }
