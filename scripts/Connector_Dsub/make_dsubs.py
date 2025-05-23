#!/usr/bin/env python

import scripts.tools.footprint_scripts_dsub as DSubScripts
from scripts.tools.footprint_generator import FootprintGenerator


class DSubGenerator(FootprintGenerator):
    lib_name = "Connector_Dsub"

    classname = "DSUB"
    classname_description = "D-Sub connector"
    webpage = "https://disti-assets.s3.amazonaws.com/tonar/files/datasheets/16730.pdf"

    pindrill = 1.0
    pad = 1.6
    mountingdrill = 3.2
    mountingpad = 4

    side_angle_degree = 10
    conn_cornerradius = 1.6
    outline_cornerradius = 1
    shieldthickness = 0.4

    can_height_male = 6
    can_height_female = 6.17

    backcan_height = 4.5
    smaller_backcan_height = 2.8

    nut_diameter = 5
    nut_length = 5

    soldercup_length = 2.9
    soldercup_diameter = 1.2

    def finalise_and_write(self, fp):
        self.add_standard_3d_model_to_footprint(fp, self.lib_name, fp.name)
        self.write_footprint(fp, self.lib_name)

    def generate_regular_density(self):

        HighDensity = False
        rmx = 2.77
        rmy = 2.84
        rmy_unboxed2 = 2.54

        soldercup_padsize = [2 * rmx / 3, self.soldercup_length * 1.2]
        soldercup_pad_edge_offset = 0.25
        smaller_backcan_offset = 1

        # unboxed connectors
        webpage_unboxed = "https://docs.rs-online.com/02d6/0900766b81585df2.pdf"
        backcan_height_unboxed = 4.1

        # fmt: off
        #                  0,             1,             2,             3,         4,                5,                  6
        #               pins, mounting_dist, outline_sizex, outlinesize_y, connwidth,  connheight_male,  connheight_female
        sizes_table=[
                    [      9,            25,         30.85,         12.50,      16.3,              8.3,              7.9 ],
                    [     15,         33.30,         39.20,         12.50,      24.6,              8.3,              7.9 ],
                    [     25,         47.10,         53.10,         12.50,      38.3,              8.3,              7.9 ],
                    [     37,         63.50,         69.40,         12.50,      54.8,              8.3,              7.9 ],
        ]

        # boxed angled
        #                   mounting_pcb_distance,   pin_pcb_distance
        angled_distances=[
                            [                5.34,               5.34 ],
                            [                9.52,               8.10 ],
                            [               11.72,              10.30 ],
                            [               16.38,              14.96 ],
                            [                8.60,              14.96 ],
                        ]

        subvariant_straight = [
            # has_pins, connheight, mountingdrill,      can_height
            [True,      8.3,        self.mountingdrill, self.can_height_male],
            [False,     7.9,        self.mountingdrill, self.can_height_female],
            [True,      8.3,        0,                  self.can_height_male],
            [False,     7.9,        0,                  self.can_height_female]
        ]
        # fmt: on

        #
        # Make regular density connectors
        for (
            pins,
            mounting_dist,
            outline_sizex,
            outline_sizey,
            connwidth,
            connheight_male,
            connheight_female,
        ) in sizes_table:
            for (
                has_pins,
                connheight,
                mountingdrill_v,
                can_height_v,
            ) in subvariant_straight:
                # Straight, Pins&Socket, with and without mountingholes
                fp = DSubScripts.makeDSubStraight(
                    global_config=self.global_config,
                    pins=pins,
                    isMale=has_pins,
                    HighDensity=HighDensity,
                    rmx=rmx,
                    rmy=rmy,
                    pindrill=self.pindrill,
                    pad=self.pad,
                    mountingdrill=mountingdrill_v,
                    mountingpad=self.mountingpad,
                    mountingdistance=mounting_dist,
                    outline_size=[outline_sizex, outline_sizey],
                    outline_cornerradius=self.outline_cornerradius,
                    connwidth=connwidth,
                    side_angle_degree=self.side_angle_degree,
                    connheight=connheight,
                    conn_cornerradius=self.conn_cornerradius,
                    tags_additional=[],
                    classname=self.classname,
                    classname_description=self.classname_description,
                    webpage=self.webpage,
                )

                self.finalise_and_write(fp)

                # Edge-mount variant, Pins&Socket
                fp = DSubScripts.makeDSubEdge(
                    global_config=self.global_config,
                    pins=pins,
                    isMale=has_pins,
                    rmx=rmx,
                    pad=soldercup_padsize,
                    mountingdrill=self.mountingdrill,
                    mountingdistance=mounting_dist,
                    shield_width=outline_sizex,
                    shieldthickness=self.shieldthickness,
                    connwidth=connwidth,
                    can_height=can_height_v,
                    backcan_width=connwidth + 2 * self.shieldthickness,
                    backcan_height=self.backcan_height,
                    smaller_backcan_offset=smaller_backcan_offset,
                    smaller_backcan_height=self.smaller_backcan_height,
                    soldercup_length=self.soldercup_length,
                    soldercup_diameter=self.soldercup_diameter,
                    soldercup_pad_edge_offset=soldercup_pad_edge_offset,
                    tags_additional=[],
                    classname=self.classname,
                    classname_description=self.classname_description,
                    webpage=self.webpage,
                )

                self.finalise_and_write(fp)

            # Horizontal connectors, Pins&Socket, 5 different 'distances'
            for mounting_pcb_distance_v, pin_pcb_distance_v in angled_distances:
                mounting_pcb_distance = mounting_pcb_distance_v - self.shieldthickness
                pin_pcb_distance = pin_pcb_distance_v - self.shieldthickness

                # backbox_height is the y-size of the plastic part that encloses the pins.
                # If we don't know how big the backbox_height should be, so we estimate its size by finding the copper part which is furthest
                # from the front of the connector. And then adding 1mm as magic value.
                backbox_height = (
                    max(
                        pin_pcb_distance + rmy + self.pad / 2,
                        mounting_pcb_distance + self.mountingpad / 2,
                    )
                    + 1
                )
                # reuse the subvariant_straight to get the mapping of variant and can_height
                for (
                    has_pins,
                    connheight,
                    mountingdrill_v,
                    can_height_v,
                ) in subvariant_straight:
                    fp = DSubScripts.makeDSubAngled(
                        global_config=self.global_config,
                        pins=pins,
                        isMale=has_pins,
                        HighDensity=HighDensity,
                        rmx=rmx,
                        rmy=rmy,
                        pindrill=self.pindrill,
                        pad=self.pad,
                        pin_pcb_distance=pin_pcb_distance,
                        mountingdrill=self.mountingdrill,
                        mountingpad=self.mountingpad,
                        mountingdistance=mounting_dist,
                        mounting_pcb_distance=mounting_pcb_distance,
                        shield_width=outline_sizex,
                        shield_thickness=self.shieldthickness,
                        can_width=connwidth,
                        can_height=can_height_v,
                        backbox_width=outline_sizex,
                        backbox_height=backbox_height,
                        nut_diameter=self.nut_diameter,
                        nut_length=self.nut_length,
                        tags_additional=[],
                        classname=self.classname,
                        classname_description=self.classname_description,
                        webpage=self.webpage,
                    )

                    self.finalise_and_write(fp)

        #
        # unboxed angled
        #
        pin_pcb_distance = 9.4
        mounting_pcb_distance = 0
        for (
            pins,
            mounting_dist,
            outline_sizex,
            outline_sizey,
            connwidth,
            connheight_male,
            connheight_female,
        ) in sizes_table:
            for (
                has_pins,
                connheight,
                mountingdrill_v,
                can_height_v,
            ) in subvariant_straight:
                # two y-pin-pitch variants
                for rmy_v in [rmy, rmy_unboxed2]:
                    fp = DSubScripts.makeDSubAngled(
                        global_config=self.global_config,
                        pins=pins,
                        isMale=has_pins,
                        HighDensity=HighDensity,
                        rmx=rmx,
                        rmy=rmy_v,
                        pindrill=self.pindrill,
                        pad=self.pad,
                        pin_pcb_distance=pin_pcb_distance,
                        mountingdrill=0,
                        mountingpad=self.mountingpad,
                        mountingdistance=mounting_dist,
                        mounting_pcb_distance=pin_pcb_distance,
                        shield_width=outline_sizex,
                        shield_thickness=self.shieldthickness,
                        backbox_width=0,
                        backbox_height=0,
                        can_width=connwidth,
                        can_height=can_height_v,
                        backcan_width=connwidth + 2 * self.shieldthickness,
                        backcan_height=backcan_height_unboxed,
                        nut_diameter=0,
                        nut_length=0,
                        tags_additional=[],
                        classname=self.classname,
                        classname_description=self.classname_description,
                        webpage=webpage_unboxed,
                    )

                    self.finalise_and_write(fp)

        # fmt: off

    def generate_high_density(self):

        #
        # build HighDensity connectors
        #
        HighDensity = True
        rmy_hd = 1.98

        #               pins, mounting_dist, outline_sizex, outlinesize_y, connwidth,  connheight_male,  connheight_female,  rmx,  HighDensityOffsetMidLeft
        hd_sizes_table = [
            [15, 25, 30.85, 12.50, 16.3, 8.3, 7.9, 2.29, 7.04],
            [26, 33.30, 39.20, 12.50, 24.6, 8.3, 7.9, 2.29, 6.88],
            [44, 47.10, 53.10, 12.50, 38.3, 8.3, 7.9, 2.29, 6.88],
            [62, 63.50, 69.40, 12.50, 54.8, 8.3, 7.9, 2.41, 7.00],
        ]
        #                   mounting_pcb_distance,  pin_pcb_distance,   rmy,  backbox_height
        angled_distances = [
            [5.34, 3.43, 1.90, 8.6],
            [11.29, 8.75, 2.54, 15.2],  # 15.2mm is an estimate (missing from datasheet)
        ]
        # fmt: on
        for (
            pins,
            mounting_dist,
            outline_sizex,
            outlinesize_y,
            connwidth,
            connheight_male,
            connheight_female,
            rmx,
            HighDensityOffsetMidLeft,
        ) in hd_sizes_table:
            # Build Pins- and Socket variants
            for has_pins in [True, False]:
                connheight = connheight_male if has_pins else connheight_female
                can_height = (
                    self.can_height_male if has_pins else self.can_height_female
                )

                # regular straight HD (kicad calls this vertical)
                fp = DSubScripts.makeDSubStraight(
                    global_config=self.global_config,
                    pins=pins,
                    isMale=has_pins,
                    HighDensity=HighDensity,
                    rmx=rmx,
                    rmy=rmy_hd,
                    pindrill=self.pindrill,
                    pad=self.pad,
                    mountingdrill=self.mountingdrill,
                    mountingpad=self.mountingpad,
                    mountingdistance=mounting_dist,
                    outline_size=[outline_sizex, outlinesize_y],
                    outline_cornerradius=self.outline_cornerradius,
                    connwidth=connwidth,
                    side_angle_degree=self.side_angle_degree,
                    connheight=connheight,
                    conn_cornerradius=self.conn_cornerradius,
                    tags_additional=[],
                    classname=self.classname,
                    classname_description=self.classname_description,
                    webpage=self.webpage,
                    HighDensityOffsetMidLeft=HighDensityOffsetMidLeft,
                )

                self.finalise_and_write(fp)

                # HD angled, with different distances
                for (
                    mounting_pcb_distance,
                    pin_pcb_distance,
                    rmy,
                    backbox_height,
                ) in angled_distances:
                    mounting_pcb_distance -= self.shieldthickness
                    pin_pcb_distance -= self.shieldthickness
                    # regular angled (kicad calles this horizontal)
                    fp = DSubScripts.makeDSubAngled(
                        global_config=self.global_config,
                        pins=pins,
                        isMale=has_pins,
                        HighDensity=HighDensity,
                        rmx=rmx,
                        rmy=rmy,
                        pindrill=self.pindrill,
                        pad=self.pad,
                        pin_pcb_distance=pin_pcb_distance,
                        mountingdrill=self.mountingdrill,
                        mountingpad=self.mountingpad,
                        mountingdistance=mounting_dist,
                        mounting_pcb_distance=mounting_pcb_distance,
                        shield_width=outline_sizex,
                        shield_thickness=self.shieldthickness,
                        can_width=connwidth,
                        can_height=self.can_height_male,  # this might be a bug!
                        backbox_width=outline_sizex,
                        backbox_height=backbox_height,
                        nut_diameter=self.nut_diameter,
                        nut_length=self.nut_length,
                        tags_additional=[],
                        classname=self.classname,
                        classname_description=self.classname_description,
                        webpage=self.webpage,
                        HighDensityOffsetMidLeft=HighDensityOffsetMidLeft,
                    )

                    self.finalise_and_write(fp)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Create DSub footprints.")

    args = FootprintGenerator.add_standard_arguments(parser)

    g = DSubGenerator(
        output_dir=args.output_dir,
        global_config=args.global_config,
    )

    # For now, just always generate - we will handle filtering at some point
    # But these are quick anyway
    g.generate_regular_density()
    g.generate_high_density()
