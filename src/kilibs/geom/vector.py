# kilibs is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kilibs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

from __future__ import division
from builtins import round

from math import sin, cos, hypot, atan2, degrees, radians


class Vector2D(object):
    r"""Representation of a 2D Vector in space

    :Example:

    >>> from KicadModTree import *
    >>> Vector2D(0, 0)
    >>> Vector2D([0, 0])
    >>> Vector2D((0, 0))
    >>> Vector2D({'x': 0, 'y':0})
    >>> Vector2D(Vector2D(0, 0))
    """

    _x: float
    _y: float

    def __init__(self, coordinates=None, y=None):
        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif isinstance(coordinates, (float, int)):
            if y is not None:
                coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give x and y coordinate')
        elif isinstance(coordinates, Vector2D):
            # convert Vector2D as well as Vector3D to dict
            coordinates = coordinates.to_dict()

        # parse vectors with format: Vector2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            return

        # parse vectors with format: Vector2D([0, 0]) or Vector2D((0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) == 2:
                self._x = float(coordinates[0])
                self._y = float(coordinates[1])
                return
            else:
                raise TypeError('invalid list size (2 elements expected)')

        raise TypeError(f'invalid parameters given: {coordinates}')

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, (float, int)):
            self._x = float(value)
        else:
            raise TypeError('invalid type for x coordinate')

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if isinstance(value, (float, int)):
            self._y = float(value)
        else:
            raise TypeError('invalid type for y coordinate')

    def round_to(self, base):
        r"""Round to a specific base (like it's required for a grid)

        :param base: base we want to round to
        :return: rounded point

        >>> from KicadModTree import *
        >>> Vector2D(0.1234, 0.5678).round_to(0.01)
        >>> # or
        >>> Vector3D(0.123, 0.456, 0.789).round_to(0.01)
        """
        if base == 0 or base is None:
            return self.__copy__()

        return self.__class__([round(v / base) * base for v in self])

    def distance_to(self, other: "Vector2D"):
        r"""Distance between this and another point

        :param value: the other point
        :return: distance between self and other point
        """
        return hypot(other.x - self.x, other.y - self.y)

    def is_close(self, other: "Vector2D", tol: float = 1e-7):
        r"""Check if two points are close to each other

        :param other: the other point
        :return: True if the points are close
        """
        return self.distance_to(other) < tol

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Vector2D):
            return value
        elif type(value) in [int, float]:
            return Vector2D([value, value])
        else:
            return Vector2D(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x + other.x,
                         'y': self.y + other.y})

    def __iadd__(self, value):
        other = Vector2D.__arithmetic_parse(value)
        self.x += other.x
        self.y += other.y

        return self

    def __neg__(self):
        return Vector2D({'x': -self.x, 'y': -self.y})

    def __sub__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x - other.x,
                         'y': self.y - other.y})

    def __isub__(self, value):
        other = Vector2D.__arithmetic_parse(value)
        self.x -= other.x
        self.y -= other.y

        return self

    def __mul__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x * other.x,
                         'y': self.y * other.y})

    def __rmul__(self, other):
        return Vector2D.__mul__(self, other)

    def __div__(self, value):
        other = Vector2D.__arithmetic_parse(value)

        return Vector2D({'x': self.x / other.x,
                         'y': self.y / other.y})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def __abs__(self):
        """
        Gets the length of the vector (same as norm())
        """
        return hypot(*self)

    def min(self, other):
        return Vector2D(*[min(*v) for v in zip(self, other)])

    def max(self, other):
        return Vector2D(*[max(*v) for v in zip(self, other)])

    def to_dict(self):
        return {'x': self.x, 'y': self.y}

    def __repr__(self):
        return f"Vector2D(x={self.x}, y={self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __getitem__(self, key):
        if key == 0 or key == 'x':
            return self.x
        if key == 1 or key == 'y':
            return self.y

        raise IndexError('Index {} is out of range'.format(key))

    def __setitem__(self, key, item):
        if key == 0 or key == 'x':
            self.x = item
        elif key == 1 or key == 'y':
            self.y = item
        else:
            raise IndexError('Index {} is out of range'.format(key))

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __copy__(self):
        return Vector2D(self.x, self.y)

    def rotate(self, angle, origin=(0, 0), use_degrees=True) -> "Vector2D":
        r""" Rotate vector around given origin

        When the co-ordinates are y-up (schematic), this is visually Clockwise
        When y-down (PCB), this is Counterclockwise.

        :params:
            * *angle* (``float``)
                rotation angle
            * *origin* (``Vector2D``)
                origin point for the rotation. default: (0, 0)
            * *use_degrees* (``boolean``)
                rotation angle is given in degrees. default:True
        """

        op = Vector2D(origin)

        if use_degrees:
            angle = radians(angle)

        temp = op.x + cos(angle) * (self.x - op.x) - sin(angle) * (self.y - op.y)
        self.y = op.y + sin(angle) * (self.x - op.x) + cos(angle) * (self.y - op.y)
        self.x = temp

        return self

    def with_rotation(self, angle, origin=(0, 0), use_degrees=True) -> "Vector2D":
        r""" Return a new vector that is rotated around given origin"""

        new_vec = self.__copy__()
        new_vec.rotate(angle, origin, use_degrees)
        return new_vec

    def to_polar(self, origin=(0, 0), use_degrees=True):
        r""" Get polar representation of the vector

        :params:
            * *origin* (``Vector2D``)
                origin point for polar conversion. default: (0, 0)
            * *use_degrees* (``boolean``)
                angle in degrees. default:True
        """

        op = Vector2D(origin)

        diff = self - op
        radius = diff.norm()
        angle = diff.arg(use_degrees)

        return (radius, angle)

    def norm(self):
        """
        Calculate the length (cartesian norm) of a vector
        """
        return hypot(*self)

    def arg(self, use_degrees=True):
        """
        Calculate the angle of a vector

        Args:
            use_degrees: angle in degrees (default: True)

        Returns:
            angle of the vector
        """
        phi = atan2(self.y, self.x)
        if use_degrees:
            phi = degrees(phi)
        return phi

    def dot_product(self, other):
        """
        Calculate the inner product of a vector with ``other``
        """
        return self.x * other.x + self.y * other.y

    def orthogonal(self) -> "Vector2D":
        """
        Calculate the orthogonal onto a vector
        """
        return Vector2D(-self.y, self.x)

    def is_nullvec(self, tol: float = 1e-7) -> bool:
        """
        Check if a vector is the null-vector (up to tol)

        Args:
            tol: minimum length to be considered as null vector
        """
        return Vector2D.norm(self) < tol

    def normalize(self, tol: float = 1e-7) -> "Vector2D":
        """
        Normalize a vector (scale it to unit length)

        Args:
            tol: minimum length to be considered as null vector
        """
        norm = self.norm()
        if norm > tol:
            self /= norm
        return self

    def resize(self, new_len: float, tol: float = 1e-7) -> "Vector2D":
        """
        Resize the vector to a new length, but same angle

        Raises if the vector is the null vector.
        """
        norm = self.norm()
        if norm < tol:
            raise ValueError("Cannot resize null vector")
        ratio = new_len / self.norm()
        self *= ratio
        return self

    @staticmethod
    def from_polar(radius, angle, origin=(0, 0), use_degrees=True):
        r""" Generate a vector from its polar representation

        :params:
            * *radius* (``float``)
                length of the vector
            * *angle* (``float``)
                angle of the vector
            * *origin* (``Vector2D``)
                origin point for polar conversion. default: (0, 0)
            * *use_degrees* (``boolean``)
                angle in degrees. default:True
        """

        if use_degrees:
            angle = radians(angle)

        x = radius * cos(angle)
        y = radius * sin(angle)

        return Vector2D({'x': x, 'y': y})+Vector2D(origin)

    def to_homogeneous(self):
        r""" Get homogeneous representation
        """

        return Vector3D(self.x, self.y, 1)

    @staticmethod
    def from_homogeneous(source):
        r""" Recover 2d vector from its homogeneous representation

        :params:
            * *source* (``Vector3D``)
                3d homogeneous representation
        """

        return Vector2D(source.x/source.z, source.y/source.z)


class Vector3D(Vector2D):
    r"""Representation of a 3D Vector in space

    :Example:

    >>> from KicadModTree import *
    >>> Vector3D(0, 0, 0)
    >>> Vector3D([0, 0, 0])
    >>> Vector3D((0, 0, 0))
    >>> Vector3D({'x': 0, 'y':0, 'z':0})
    >>> Vector3D(Vector2D(0, 0))
    >>> Vector3D(Vector3D(0, 0, 0))
    """

    def __init__(self, coordinates=None, y=None, z=None):
        # we don't need a super constructor here

        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif type(coordinates) in [int, float]:
            if y is not None:
                if z is not None:
                    coordinates = [coordinates, y, z]
                else:
                    coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give at least x and y coordinate')
        elif isinstance(coordinates, Vector2D):
            # convert Vector2D as well as Vector3D to dict
            coordinates = coordinates.to_dict()

        # parse vectors with format: Vector2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            self.z = float(coordinates.get('z', 0.))
            return

        # parse vectors with format: Vector3D([0, 0]), Vector3D([0, 0, 0]) or Vector3D((0, 0)), Vector3D((0, 0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) >= 2:
                self.x = float(coordinates[0])
                self.y = float(coordinates[1])
            else:
                raise TypeError('invalid list size (to small)')

            if len(coordinates) == 3:
                self.z = float(coordinates[2])
            else:
                self.z = 0.

            if len(coordinates) > 3:
                raise TypeError('invalid list size (to big)')

        else:
            raise TypeError('dict or list type required')

    def cross_product(self, other):
        other = Vector3D.__arithmetic_parse(other)

        return Vector3D({
                    'x': self.y*other.z - self.z*other.y,
                    'y': self.z*other.x - self.x*other.z,
                    'z': self.x*other.y - self.y*other.x})

    def dot_product(self, other):
        other = Vector3D.__arithmetic_parse(other)

        return self.x*other.x + self.y*other.y + self.z*other.z

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Vector3D):
            return value
        elif type(value) in [int, float]:
            return Vector3D([value, value, value])
        else:
            return Vector3D(value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x + other.x,
                         'y': self.y + other.y,
                         'z': self.z + other.z})

    def __iadd__(self, value):
        other = Vector2D.__arithmetic_parse(value)
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __neg__(self):
        return Vector2D({'x': -self.x,
                         'y': -self.y,
                         'z': -self.z})

    def __sub__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x - other.x,
                         'y': self.y - other.y,
                         'z': self.z - other.z})

    def __isub__(self, value):
        other = Vector2D.__arithmetic_parse(value)
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def __mul__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x * other.x,
                         'y': self.y * other.y,
                         'z': self.z * other.z})

    def __div__(self, value):
        other = Vector3D.__arithmetic_parse(value)

        return Vector3D({'x': self.x / other.x,
                         'y': self.y / other.y,
                         'z': self.z / other.z})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def __repr__(self):
        return "Vector3D (x={x}, y={y}, z={z})".format(**self.to_dict())

    def __str__(self):
        return "(x={x}, y={y}, z={z})".format(**self.to_dict())

    def __getitem__(self, key):
        if key == 0 or key == 'x':
            return self.x
        if key == 1 or key == 'y':
            return self.y
        if key == 2 or key == 'z':
            return self.z

        raise IndexError('Index {} is out of range'.format(key))

    def __setitem__(self, key, item):
        if key == 0 or key == 'x':
            self.x = item
        elif key == 1 or key == 'y':
            self.y = item
        elif key == 2 or key == 'z':
            self.z = item
        else:
            raise IndexError('Index {} is out of range'.format(key))

    def __len__(self):
        return 3

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __copy__(self):
        return Vector3D(self.x, self.y, self.z)
