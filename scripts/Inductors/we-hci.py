#!/usr/bin/env python3

import sys
import os

from KicadModTree import *
from scripts.tools.global_config_files import global_config as GC
global_config = GC.DefaultGlobalConfig()


#http://katalog.we-online.com/en/pbs/WE-MAPI]

#sizes,shapes,etc]
#name, L, W, pad-w, pad-gap, pad-h
inductors = [
[5040,5.5,5.2,1.9,2.2,1.6],
[7030,6.9,6.9,2.7,2.4,2.2],
[7040,6.9,6.9,2.7,2.4,2.2],
[7050,6.9,6.9,2.7,2.4,2.2],
[1030,10.6,10.6,3.8,3.9,3.5],
[1040,10.2,10.2,3.5,4.5,4],
[1050,10.2,10.2,3.85,3.8,4],
[1335,12.8,12.8,3.85,6.3,5],
[1350,12.8,12.8,4.5,6,5],
[1365,12.8,12.8,4.5,6,5],
[2212,22.5,22.0,7,9.5,7],
[1890,18.2,18.2,6,7.3,6],
[1890,18.2,18.2,6,7.3,6],
]

output_dir = os.getcwd()

#if specified as an argument, extract the target directory for output footprints
if len(sys.argv) > 1:
    out_dir = sys.argv[1]

    if os.path.isabs(out_dir) and os.path.isdir(out_dir):
        output_dir = out_dir
    else:
        out_dir = os.path.join(os.getcwd(),out_dir)
        if os.path.isdir(out_dir):
            output_dir = out_dir

if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep

prefix = "L_"
part = "Wuerth_HCI-{pn}"
dims = "{l:0.1f}mmx{w:0.1f}mm"

desc = "Inductor, Wuerth Elektronik, {pn}"
tags = "inductor wurth hci smd"

for inductor in inductors:
    name,l,w,x,g,y = inductor

    fp_name = prefix + part.format(pn=str(name))

    fp = Footprint(fp_name, FootprintType.SMD)

    description = desc.format(pn = part.format(pn=str(name))) + ", " + dims.format(l=l,w=w)

    fp.setTags(tags)
    fp.setDescription(description)

    # set general values
    fp.append(Property(name=Property.REFERENCE, text='REF**', at=[0,-w/2 - 1], layer='F.SilkS'))
    fp.append(Property(name=Property.VALUE, text=fp_name, at=[0,w/2 + 1.5], layer='F.Fab'))

    #add inductor outline
    fp.append(RectLine(start=[-l/2,-w/2],end=[l/2,w/2],layer='F.Fab',width=0.1))

    #calculate pad center
    #pad-width pw
    pw = x
    c = g/2 + pw/2

    layers = Pad.LAYERS_SMT

    #add pads
    fp.append(Pad(number=1,at=[-c,0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[pw,y]))
    fp.append(Pad(number=2,at=[c,0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[pw,y]))

    #add inductor courtyard
    cx = c + pw/2
    cy = w / 2

    fp.append(RectLine(start=[-cx,-cy],end=[cx,cy],offset=0.3,width=0.05,grid=0.05,layer="F.CrtYd"))

    offset = 0.1
    ly = y/2 + 4 * offset

    x1 = l / 2 + offset
    y1 = w / 2 + offset

    top = [
    {'x': -x1, 'y': ly},
    {'x': -x1, 'y': y1},
    {'x':  x1, 'y': y1},
    {'x':  x1, 'y': ly},
    ]


    fp.append(PolygonLine(polygon=top))
    fp.append(PolygonLine(polygon=top, y_mirror=0))

    #Add a model
    lib_name = "Inductor_SMD"
    fp.append(Model(filename=global_config.model_3d_prefix + lib_name + ".3dshapes/" + fp_name + global_config.model_3d_suffix))

    lib = KicadPrettyLibrary(lib_name, None)
    lib.save(fp)
