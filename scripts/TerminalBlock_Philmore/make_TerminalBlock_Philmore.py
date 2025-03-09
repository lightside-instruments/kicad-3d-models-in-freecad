#!/usr/bin/env python3

from KicadModTree import *  # NOQA
from scripts.tools.footprint_scripts_terminal_blocks import *


if __name__ == '__main__':

    script_generated_note="script-generated using https://gitlab.com/kicad/libraries/kicad-footprint-generator/-/tree/master/scripts/TerminalBlock_Philmore";
    classname="TerminalBlock_Philmore"




    pins=range(2,3+1)
    rm=5
    package_height=10.2
    leftbottom_offset=[rm/2, 5.4]
    ddrill=1.2
    pad=[2.4,2.4]
    screw_diameter=2.75
    bevel_height=[0.5,1.6]
    slit_screw=False
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.5]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="TB13{0}".format(p);
        webpage="http://www.philmore-datak.com/mc/Page%20197.pdf";
        classname_description="Terminal Block Philmore ".format(name);
        footprint_name="TerminalBlock_Philmore_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

