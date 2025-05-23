#!/usr/bin/env python

from KicadModTree import *  # NOQA
from scripts.tools.footprint_scripts_terminal_blocks import *


if __name__ == '__main__':

    script_generated_note="script-generated using https://gitlab.com/kicad/libraries/kicad-footprint-generator/-/tree/master/scripts/TerminalBlock_MetzConnect";
    classname="TerminalBlock_MetzConnect"

    pins=[2,3,4,5,6]
    rm=5
    package_height=12.5
    leftbottom_offset=[rm/2, 6.5]
    ddrill=1.4
    pad=[2.7,2.7]
    screw_diameter=2.2
    bevel_height=[5.4,9.2]
    vsegment_lines_offset=[]
    opening=[3.5,4]
    opening_xoffset=0
    opening_yoffset=1
    opening_elliptic=False
    secondDrillDiameter=0
    secondDrillOffset=[2.5,-5]
    secondDrillPad=pad
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[1.25,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[1.25,-5.75]
    fifthHoleDiameter=0
    fifthHoleOffset=[1.25,-0.75]
    secondEllipseSize=[3.6,2.8]
    secondEllipseOffset=[0,-4.4]
    fabref_offset=[0,-1]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type205_RT045{0:02}UBLC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/312051/863728.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlock45Degree(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad,  vsegment_lines_offset=vsegment_lines_offset,
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, opening_elliptic=opening_elliptic,
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, fifthHoleDiameter=fifthHoleDiameter,fifthHoleOffset=fifthHoleOffset,
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  secondEllipseSize=secondEllipseSize,secondEllipseOffset=secondEllipseOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,6+1)
    rm=3.81
    package_height=7.3
    leftbottom_offset=[1.85, 3.6]
    ddrill=1.1
    pad=[1.75,1.75]
    screw_diameter=2.5
    bevel_height=[0.6,1.9,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=[2,0.5]
    thirdHoleOffset=[0,-(3.6-0.5/2)]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.45]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type086_RT034{0:02}HBLC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/310861/863404.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,6+1)
    rm=5.0
    package_height=10.5
    leftbottom_offset=[2.5, 4]
    ddrill=1.4
    pad=[2.8,2.8]
    screw_diameter=3.2
    bevel_height=[2,package_height-4.5,package_height-3.5]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,4.5]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type011_RT055{0:02}HBLC".format(p)
        webpage="https://americancableassemblies.com/content/metz/863188.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)


    pins=range(2,5+1)
    rm=10
    package_height=8.2
    leftbottom_offset=[2.9, 4.1]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=3
    bevel_height=[2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type067_RT019{0:02}HDWC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/310671/863296.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)


    pins=range(2,3+1)
    rm=9.52
    package_height=12.5
    leftbottom_offset=[4.76, 8]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=4
    bevel_height=[0.5,4.5,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0.5]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=[2,1]
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.5]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type703_RT10N{0:02}HGLU".format(p)
        webpage="https://www.metz-connect.com/externalfiles/317031/863835.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,6+1)
    rm=5.0
    package_height=8.3
    leftbottom_offset=[2.5, 4]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=3
    bevel_height=[0.5,2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=[2,1]
    thirdHoleOffset=[0,-(4.3-0.5)]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.9]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type094_RT035{0:02}HBLU".format(p)
        webpage="https://www.metz-connect.com/externalfiles/310941/863441.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,6+1)
    rm=5.08
    package_height=8
    leftbottom_offset=[2.54, 4]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type101_RT016{0:02}HBWC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/311011/863468.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,6+1)
    rm=3.5
    package_height=6.5
    leftbottom_offset=[rm/2, 3.7]
    ddrill=1.2
    pad=[2.3,2.3]
    screw_diameter=2.75
    bevel_height=[1.5]
    slit_screw=True
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
        name="Type059_RT063{0:02}HBWC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/310591/863246.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)


    pins=range(2,3+1)
    rm=5.08
    package_height=11
    leftbottom_offset=[2.54, 5.5]
    ddrill=1.4
    pad=[2.6,2.6]
    screw_diameter=3.5
    bevel_height=[0.5,3,package_height-1.8]
    slit_screw=True
    screw_pin_offset=[0,-0.3]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.5]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type073_RT026{0:02}HBLU".format(p)
        webpage="https://www.metz-connect.com/externalfiles/310731/863336.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,3+1)
    rm=6.35
    package_height=12.5
    leftbottom_offset=[3.175, 8]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=4
    bevel_height=[0.5,5.5,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=[2,1]
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.5]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type701_RT11L{0:02}HGLU".format(p)
        webpage="https://www.metz-connect.com/externalfiles/317011/863830.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)


    pins=range(2,6+1)
    rm=7.5
    package_height=9
    leftbottom_offset=[3.75, 4.5]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.5]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type171_RT137{0:02}HBWC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/311711/863695.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,6+1)
    rm=7.5
    package_height=11
    leftbottom_offset=[3.75, 5.5]
    ddrill=1.4
    pad=[2.6,2.6]
    screw_diameter=3
    bevel_height=[0.6,2.5,package_height-1.9]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,4]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type175_RT027{0:02}HBLC".format(p)
        webpage="https://www.metz-connect.com/externalfiles/311751/863710.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,4+1)
    rm=5
    package_height=8
    leftbottom_offset=[2.5,4]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3]
    nibbleSize = None
    nibblePos = None
    for p in pins:
        name="Type055_RT015{0:02}HDWU".format(p)
        webpage="https://www.metz-connect.com/externalfiles/310551/863212.PDF"
        footprint_name="TerminalBlock_MetzConnect_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block Metz Connect {0}".format(name, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm,
                                  package_height=package_height, leftbottom_offset=leftbottom_offset,
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name=classname, classname=classname, classname_description=classname_description,
                                  webpage=webpage, script_generated_note=script_generated_note)
