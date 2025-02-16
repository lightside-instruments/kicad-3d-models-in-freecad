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
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import io
import os

from KicadModTree.nodes.Footprint import Footprint


class FileHandler(object):
    r"""some basic methods to write footprints, and which is the base class of footprint writer implementations

    :param kicad_mod:
        Main object representing the footprint
    :type kicad_mod: ``KicadModTree.Footprint``

    :Example:

    >>> from KicadModTree import *
    >>> kicad_mod = Footprint("example_footprint", FootprintType.THT)
    >>> file_handler = KicadFileHandler(kicad_mod)  # KicadFileHandler is a implementation of FileHandler
    >>> file_handler.writeFile('example_footprint.kicad_mod')
    """
    kicad_mod: Footprint

    def __init__(self, kicad_mod: Footprint):
        self.kicad_mod = kicad_mod

    def writeFile(self, filename, **kwargs):
        r"""Write the output of FileHandler.serialize to a file

        :param filename:
            path of the output file
        :type filename: ``str``

        :Example:

        >>> from KicadModTree import *
        >>> kicad_mod = Footprint("example_footprint", FootprintType.THT)
        >>> file_handler = KicadFileHandler(kicad_mod)  # KicadFileHandler is a implementation of FileHandler
        >>> file_handler.writeFile('example_footprint.kicad_mod')
        """

        fp = None
        with io.open(filename, "w") as f:
            output = self.serialize(**kwargs)

            if not output.endswith("\n"):
                output += "\n"

            f.write(output)

            fp = os.path.realpath(f.name)

            f.close()
        return fp

    def serialize(self, **kwargs):
        r"""Get a valid string representation of the footprint in the specified format

        :Example:

        >>> from KicadModTree import *
        >>> kicad_mod = Footprint("example_footprint", FootprintType.THT)
        >>> file_handler = KicadFileHandler(kicad_mod)  # KicadFileHandler is a implementation of FileHandler
        >>> print(file_handler.serialize())
        """

        raise NotImplementedError(
            "serialize has to be implemented by child class")
