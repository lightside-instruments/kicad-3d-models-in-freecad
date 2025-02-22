#!/usr/bin/env python3

import sys
import os
import math
import argparse
import yaml

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

# load scripts
sys.path.append(os.path.join(sys.path[0], ".."))

from KicadModTree import *
from general.StandardBox import *

def qfn(args):

    extraffablines = []

    name = args["name"]
    description = args["description"]
    datasheet = args["datasheet"]
    tags = args["tags"]
    manufacture = args["manufacture"]
    serie = args["serie"]
    suffix = args["suffix"]

    W = args["W"]
    H = args["H"]
    WD = args["WD"]
    A1 = args["A1"]
    pinnumbers = args["pin_number"]
    PE = args["PE"]
    PS = args["PS"]
    PD = args["PD"]
    PL = args["PL"]
    PF = args["PF"]
    SW = args["SW"]
    DD = args["DD"]
    PD = args["PD"]
    rotation = args["rotation"]
    dest_dir_3D_prefix = args["dest_dir_3D_prefix"]


    for pinnumber in pinnumbers:
        footprint_name = ''
        footprint_name = footprint_name + manufacture + '_' + serie
        footprint_name = footprint_name + '_1x' + '{:02d}'.format(pinnumber)
        footprint_name = footprint_name + '_P' + '{:.2f}'.format(PS) + "mm"
        footprint_name = footprint_name + suffix

        f = Footprint(footprint_name, FootprintType.THT)


        file3Dname = "${KICAD9_3DMODEL_DIR}/" + dest_dir_3D_prefix + "/" + footprint_name + ".wrl"
        words = footprint_name.split("_")
        if words[-1].lower().startswith('handsolder'):
            words[-1] = ''
            ff = '_'.join(words)
            file3Dname = "${KICAD9_3DMODEL_DIR}/" + dest_dir_3D_prefix + "/" + ff + ".wrl"

        lw = ((2.0 * PE) + ((pinnumber - 1) * PS))
        at = [0.0 - PE, W - WD]
        size = [lw, W]
        extratexts = None
        SmdTht = None
        pins = []
        dx = 0.0
        for ii in range(1, pinnumber + 1):
            pins.append(["tht", str(ii), dx, 0.0, PD, PD, DD])
            dx = dx + PS
        f.append(StandardBox(footprint=f, description=description, datasheet=datasheet, at=at,
                             size=size, tags=tags, extratexts=extratexts, pins=pins,
                             file3Dname=file3Dname))


        output_dir = 'TerminalBlock_Altech.pretty' + os.sep
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        file_handler = KicadFileHandler(f)
        file_handler.writeFile(output_dir + footprint_name + ".kicad_mod")


if __name__ == '__main__':
	parser = ModArgparser(qfn)
	# the root node of .yml files is parsed as name
	parser.add_parameter("name",        type=str,   required=True)
	parser.add_parameter("description", type=str,   required=True)
	parser.add_parameter("datasheet",   type=str,   required=True)
	parser.add_parameter("tags",        type=str,   required=True)
	parser.add_parameter("manufacture", type=str,   required=True)
	parser.add_parameter("serie",       type=str,   required=True)
	parser.add_parameter("suffix",      type=str,   required=False)

	parser.add_parameter("W",           type=float, required=True)
	parser.add_parameter("H",           type=float, required=True)
	parser.add_parameter("WD",          type=float, required=True)
	parser.add_parameter("A1",          type=float, required=True)
	parser.add_parameter("pin_number",  type=list,  required=True)
	parser.add_parameter("PE",          type=float, required=True)
	parser.add_parameter("PS",          type=float, required=True)
	parser.add_parameter("PD",          type=list,  required=True)
	parser.add_parameter("PL",          type=float, required=True)
	parser.add_parameter("PF",          type=str,   required=True)
	parser.add_parameter("SW",          type=float, required=True)
	parser.add_parameter("DD",          type=float, required=True)
	parser.add_parameter("PD",          type=float, required=True)
	parser.add_parameter("rotation",    type=str,   required=True)
	parser.add_parameter("dest_dir_3D_prefix",    type=str,   required=True)

	# now run our script which handles the whole part of parsing the files
	parser.run()
