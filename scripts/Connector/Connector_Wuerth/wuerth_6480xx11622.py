#!/usr/bin/env python3

import argparse
import yaml

from KicadModTree import *
from scripts.tools.footprint_text_fields import addTextFields
from scripts.tools.global_config_files import global_config as GC
from KicadModTree.util.courtyard_builder import CourtyardBuilder

series = "WR-WTB"
manufacturer = 'Wuerth'
orientation = 'V'
number_of_rows = 1
datasheet = 'https://katalog.we-online.com/em/datasheet/6480xx11622.pdf'
mpn_pattern = "6480{n:02}11622"

fab_pin1_marker_type = 2
pin1_marker_offset = 0.3
pin1_marker_linelen = 1.25

drill_size = 0.87 #Datasheet: 0.7 +0.1/-0.0 => It might be better to assume 0.75 +/-0.05mm
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15



pitch = 1.5

# Connector Parameters
x_min = -1.5
y_min = -1.3
y_max = y_min + 3.5

def roundToBase(value, base):
    return round(value/base) * base

def generate_one_footprint(global_config: GC.GlobalConfig, pincount, configuration):
    silk_x_min = x_min - configuration['silk_fab_offset']
    silk_y_min = y_min - configuration['silk_fab_offset']
    silk_y_max = y_max + configuration['silk_fab_offset']


    x_mid = (pincount-1)*pitch/2.0
    x_max = (pincount-1)*pitch + 1.5
    silk_x_max = x_max + configuration['silk_fab_offset']

    # Through-hole type shrouded header, Top entry type
    mpn = mpn_pattern.format(n=pincount) # part number format string
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name, FootprintType.THT)
    kicad_mod.setDescription("{:s} {:s} series connector, {:s} ({:s}), generated with kicad-footprint-generator".format(manufacturer, series, mpn, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    ########################## Fab Outline ###############################
    kicad_mod.append(RectLine(start=[x_min,y_min], end=[x_max,y_max],
        layer='F.Fab', width=configuration['fab_line_width']))
    if fab_pin1_marker_type == 1:
        kicad_mod.append(PolygonLine(polygon=poly_pin1_marker, layer='F.Fab', width=configuration['fab_line_width']))
    if fab_pin1_marker_type == 2:
        poly_pin1_marker_type2 = [
            {'x':-1, 'y':y_min},
            {'x':0, 'y':y_min+1},
            {'x':1, 'y':y_min}
        ]
        kicad_mod.append(PolygonLine(polygon=poly_pin1_marker_type2, layer='F.Fab', width=configuration['fab_line_width']))

    # create Silkscreen
    kicad_mod.append(RectLine(start=[silk_x_min,silk_y_min], end=[silk_x_max,silk_y_max],
        layer='F.SilkS', width=configuration['silk_line_width']))


    wall_thikness=0.2
    if configuration['allow_silk_below_part'] == 'tht' or configuration['allow_silk_below_part'] == 'both':
        poly_silk_inner_outline = [
            {'x':silk_x_min, 'y':-0.35},
            {'x':silk_x_min+wall_thikness, 'y':-0.35},
            {'x':silk_x_min+wall_thikness, 'y':silk_y_min+wall_thikness},
            {'x':silk_x_max-wall_thikness, 'y':silk_y_min+wall_thikness},
            {'x':silk_x_max-wall_thikness, 'y':-0.35},
            {'x':silk_x_max, 'y':-0.35}
        ]
        kicad_mod.append(PolygonLine(polygon=poly_silk_inner_outline, layer='F.SilkS', width=configuration['silk_line_width']))
        poly_silk_inner_outline = [
            {'x':silk_x_min+wall_thikness, 'y':-0.35},
            {'x':silk_x_min+wall_thikness, 'y':0.35},
            {'x':silk_x_min, 'y':0.35}
        ]
        kicad_mod.append(PolygonLine(polygon=poly_silk_inner_outline, layer='F.SilkS', width=configuration['silk_line_width']))
        poly_silk_inner_outline = [
            {'x':silk_x_max-wall_thikness, 'y':-0.35},
            {'x':silk_x_max-wall_thikness, 'y':0.35},
            {'x':silk_x_max, 'y':0.35}
        ]
        kicad_mod.append(PolygonLine(polygon=poly_silk_inner_outline, layer='F.SilkS', width=configuration['silk_line_width']))
        poly_silk_inner_outline = [
            {'x':silk_x_min+wall_thikness, 'y':0.35},
            {'x':silk_x_min+wall_thikness, 'y':silk_y_max-wall_thikness},
            {'x':silk_x_max-wall_thikness, 'y':silk_y_max-wall_thikness},
            {'x':silk_x_max-wall_thikness, 'y':0.35},
        ]
        kicad_mod.append(PolygonLine(polygon=poly_silk_inner_outline, layer='F.SilkS', width=configuration['silk_line_width']))
    poly_pin1_marker = [
        {'x':silk_x_min-pin1_marker_offset+pin1_marker_linelen, 'y':silk_y_min-pin1_marker_offset},
        {'x':silk_x_min-pin1_marker_offset, 'y':silk_y_min-pin1_marker_offset},
        {'x':silk_x_min-pin1_marker_offset, 'y':silk_y_min-pin1_marker_offset+pin1_marker_linelen}
    ]
    kicad_mod.append(PolygonLine(polygon=poly_pin1_marker, layer='F.SilkS', width=configuration['silk_line_width']))

    ############################# Pads ##################################
    pad_size = [pitch - pad_to_pad_clearance, drill_size + 2*pad_copper_y_solder_length]
    if pad_size[0] - drill_size < 2*min_annular_ring:
        pad_size[0] = drill_size + 2*min_annular_ring

    # kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
    #                     at=[0, 0], size=pad_size,
    #                     drill=drill_size, layers=Pad.LAYERS_THT))

    optional_pad_params = {}
    optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(initial=1, start=[0, 0],
        x_spacing=pitch, pincount=pincount,
        size=pad_size, drill=drill_size,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT,
        round_radius_handler=global_config.roundrect_radius_handler,
        **optional_pad_params))

    ############################# CrtYd ##################################
    crt_offset = global_config.get_courtyard_offset(GC.GlobalConfig.CourtyardType.CONNECTOR)
    cb = CourtyardBuilder.from_node(
        node=kicad_mod,
        global_config=global_config,
        offset_fab=crt_offset
        )
    kicad_mod += cb.node

    ######################### Text Fields ###############################
    text_center_y = 1.5
    body_edge={'left':x_min, 'right':x_max, 'top':y_min, 'bottom':y_max}
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard=cb.bbox, fp_name=footprint_name, text_y_inside_position=text_center_y)

    model3d_path_prefix = configuration.get('3d_model_prefix',global_config.model_3d_prefix)
    model3d_path_suffix = configuration.get('3d_model_suffix',global_config.model_3d_suffix)

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}{model3d_path_suffix}'.format(
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

    for pincount in range(2,11):
        generate_one_footprint(global_config, pincount, configuration)
