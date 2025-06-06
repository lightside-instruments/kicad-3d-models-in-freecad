#!/usr/bin/env python3

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

"""

This family of parts is spread over 3 datasheets, depending on the 3rd number in the PN suffix:

502340-xx10 (14-80 pin):
http://www.molex.com/pdm_docs/sd/5024301410_sd.pdf

502340-0820 (8 pin)
http://www.molex.com/pdm_docs/sd/5024300820_sd.pdf

502340-xx30 (14-90 pin):
http://www.molex.com/pdm_docs/sd/5024307030_sd.pdf

"""

import argparse
import yaml

from KicadModTree import *
from scripts.tools.drawing_tools import round_to_grid
from scripts.tools.footprint_text_fields import addTextFields
from scripts.tools.global_config_files import global_config as GC


series = "SlimStack"
series_long = 'SlimStack Fine-Pitch SMT Board-to-Board Connectors'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2

#pins_per_row per row
valid_pns = [
    "1410","2010","2210","2410","2610","3010","3210","3410","4010","4410","5010","6010","6410","8010",
    "0820",
    #"1430","2030","2230","2430","2630","3230","4030","5030","6030","7030","8030","9030"
]


#Molex part number
#n = number of circuits per row
part_code = "502430-{pn:s}"

pitch = 0.4

def generate_one_footprint(global_config: GC.GlobalConfig, partnumber, configuration):
    pincount = int(partnumber[:2])
    if str(partnumber)[2:3] == "1":
        datasheet = "http://www.molex.com/pdm_docs/sd/5024301410_sd.pdf"
    elif str(partnumber)[2:3] == "2":
        datasheet = "http://www.molex.com/pdm_docs/sd/5024300820_sd.pdf"
    elif str(partnumber)[2:3] == "3":
        datasheet = "http://www.molex.com/pdm_docs/sd/5024307030_sd.pdf"
    mpn = part_code.format(pn=partnumber)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount//2, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name, FootprintType.SMD)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pincount, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    # calculate working values
    pad_x_spacing = pitch
    pad_y_spacing = 1.05 + 0.66
    pad_width = 0.22
    pad_height = 0.66
    pad_x_span = pad_x_spacing * ((pincount / 2) - 1)

    nail_x = pad_x_span / 2.0 + 0.95

    half_body_width = 1.54 / 2.0
    half_body_length = (pad_x_span / 2.0) + 1.33

    fab_width = configuration['fab_line_width']

    outline_x = half_body_length - (pad_x_span / 2.0) - pad_width/2 - (configuration['silk_pad_clearance'] + configuration['silk_line_width']/2)
    marker_y = 0.35
    silk_width = configuration['silk_line_width']
    nudge = configuration['silk_fab_offset']

    courtyard_width = configuration['courtyard_line_width']
    courtyard_precision = configuration['courtyard_grid']
    courtyard_clearance = configuration['courtyard_offset']['connector']
    courtyard_x = round_to_grid(half_body_length + courtyard_clearance, courtyard_precision)
    courtyard_y = round_to_grid((pad_y_spacing + pad_height) / 2.0 + courtyard_clearance, courtyard_precision)

    # create pads
    kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,center=[0,-pad_y_spacing/2.0],\
        initial=1, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,center=[0,pad_y_spacing/2.0],\
        initial=2, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],layers=Pad.LAYERS_SMT))

    # create "fitting nail" (npth mounting) holes
    #kicad_mod.append(Pad(at=[-nail_x, 0], type=Pad.TYPE_NPTH, shape=Pad.SHAPE_RECT, size=[0.35, 0.44], drill=[0.35, 0.44], layers=Pad.LAYERS_THT))
    #kicad_mod.append(Pad(at=[nail_x, 0], type=Pad.TYPE_NPTH, shape=Pad.SHAPE_RECT, size=[0.35, 0.44], drill=[0.35, 0.44], layers=Pad.LAYERS_THT))
    kicad_mod.append(RectLine(start=[-nail_x - 0.35 / 2.0, -0.22], end=[-nail_x + 0.35 / 2.0, 0.22], layer='Edge.Cuts', width=fab_width))
    kicad_mod.append(RectLine(start=[nail_x - 0.35 / 2.0, -0.22], end=[nail_x + 0.35 / 2.0, 0.22], layer='Edge.Cuts', width=fab_width))

    # create fab outline and pin 1 marker
    kicad_mod.append(RectLine(start=[-half_body_length, -half_body_width], end=[half_body_length, half_body_width], layer='F.Fab', width=fab_width))
    body_edge={
        'left':-half_body_length,
        'top':-half_body_width
    }
    body_edge['right'] = -body_edge['left']
    body_edge['bottom'] = -body_edge['top']
    kicad_mod.append(Line(start=[-half_body_length+outline_x, -half_body_width], end=[-half_body_length+outline_x, -half_body_width-marker_y], layer='F.Fab', width=fab_width))

    # create silkscreen outline and pin 1 marker
    left_outline = [[-half_body_length+outline_x, half_body_width+nudge], [-half_body_length-nudge, half_body_width+nudge], [-half_body_length-nudge, -half_body_width-nudge],\
                    [-half_body_length+outline_x, -half_body_width-nudge], [-half_body_length+outline_x, -half_body_width-marker_y]]
    right_outline = [[half_body_length-outline_x, half_body_width+nudge], [half_body_length+nudge, half_body_width+nudge], [half_body_length+nudge, -half_body_width-nudge],\
                     [half_body_length-outline_x, -half_body_width-nudge]]
    kicad_mod.append(PolygonLine(polygon=left_outline, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygonLine(polygon=right_outline, layer='F.SilkS', width=silk_width))

    # create courtyard
    kicad_mod.append(RectLine(start=[-courtyard_x, -courtyard_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=courtyard_width))

    ######################### Text Fields ###############################

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':-courtyard_y, 'bottom':+courtyard_y},
        fp_name=footprint_name, text_y_inside_position='center')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix',global_config.model_3d_prefix)
    model3d_path_suffix = configuration.get('3d_model_suffix',global_config.model_3d_suffix)

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}{model3d_path_suffix:s}'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name,
        model3d_path_suffix=model3d_path_suffix)
    kicad_mod.append(Model(filename=model_name))

    lib = KicadPrettyLibrary(lib_name, None)
    lib.save(kicad_mod)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
            global_config = GC.GlobalConfig(configuration)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for partnumber in valid_pns:
        generate_one_footprint(global_config, partnumber, configuration)
