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

import argparse

from KicadModTree import *  # NOQA


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family",
        help="device type to build: TO-252 | TO-263 | TO-268  (default is all)",
        type=str,
        nargs=1,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="show extra information while generating the footprint",
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":

    print("Building DPAK")

    args = get_args()

    print("Rebuilding DPAK")

    from DPAK import DPAK, TO252, TO263, TO268, ATPAK, Texas_NDW

    CONFIG = "DPAK_config.yaml"

    if args.family:
        if args.family[0] == "TO252":
            build_list = [TO252(CONFIG)]
        elif args.family[0] == "TO263":
            build_list = [TO263(CONFIG)]
        elif args.family[0] == "TO268":
            build_list = [TO268(CONFIG)]
        elif args.family[0] == "ATPAK":
            build_list = [ATPAK(CONFIG)]
        elif args.family[0] == "Texas_NDW":
            build_list = [Texas_NDW(CONFIG)]
        else:
            print("ERROR: family not recognised")
            build_list = []
    else:
        build_list = [
            TO252(CONFIG),
            TO263(CONFIG),
            TO268(CONFIG),
            ATPAK(CONFIG),
            Texas_NDW(CONFIG),
        ]

    for package in build_list:
        package.build_series(verbose=args.verbose)
