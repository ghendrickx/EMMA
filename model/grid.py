"""
Grid settings.

Author: Gijs G. Hendrickx
"""
import logging
import numpy as np

LOG = logging.getLogger(__name__)

#TODO: There are some "scary" things in this script (sorry for that) that I will explain. For now, try to understand
# what is happening by searching the Internet; essentially, coding/programming is knowing how to use the Internet.


class _CellVariables:
    #TODO: These "cell-variables" are customised for the CoralModel. The **kwargs-statement allows for some flexibility
    # (have a look online what it means; it commonly goes together with *args)
    #TODO: We might want to use a similar structure, but do not necessarily need to; I used it for clarity-reasons.

    def __init__(self, capacity=None, water_depth=None, velocity=None, **kwargs):
        """
        :param capacity: carrying capacity of cell, defaults to None
        :param water_depth: water depth at cell, defaults to None
        :param velocity: depth-averaged flow velocity at cell, defaults to None
        :param kwargs: non-essential cell characteristics

        :type capacity: float, optional
        :type water_depth: float, optional
        :type velocity: float, optional
        """
        self.capacity = 1 if capacity is None else capacity
        self.water_depth = water_depth
        self.flow_velocity = velocity
        [setattr(self, key, value) for key, value in kwargs.items()]

    def __repr__(self):
        """Object-representation."""
        return f'_CellVariables(**kwargs)'

    def __str__(self):
        """String-representation."""
        return f'_CellVariables'


class Cell:
    _cells = dict()

    def __new__(cls, x, y, **kwargs):
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :param kwargs: key-worded arguments: cell characteristics

        :type x: float
        :type y: float
        """
        # use predefined cell with same (x, y)-coordinates
        if (x, y) in cls._cells:
            return cls._cells[(x, y)]

        # create new cell
        cell = super().__new__(cls)
        cell._already_initiated = False
        cls._cells[(x, y)] = cell
        return cell

    def __init__(self, x, y, **kwargs):
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :param kwargs: key-worded arguments: cell characteristics

        :type x: float
        :type y: float
        """
        if not self._already_initiated:
            self._x = x
            self._y = y
            self._ecotope = None
            self._variables = _CellVariables(**kwargs)
            self._already_initiated = True

    def __str__(self):
        """String-representation of Cell."""
        return f'Cell at {self.coordinates}'

    def __repr__(self):
        """Object-representation of Cell."""
        return f'Cell({self._x}, {self._y})'

    @property
    def ecotope(self):
        return self._ecotope

    @ecotope.setter
    def ecotope(self, ecotope_):
        if hasattr(ecotope_, 'is_ecotope') and ecotope_.is_ecotope:
            self._ecotope = ecotope_
        else:
            msg = f'Unknown type was attempted to be set as ecotope to {self}: {ecotope_}'
            LOG.warning(msg)

    @property
    def x(self):
        """
        :return: x-coordinate
        :rtype: float
        """
        return self._x

    @property
    def y(self):
        """
        :return: y-coordinate
        :rtype: float
        """
        return self._y

    @property
    def coordinates(self):
        """
        :return: (x, y)-coordinates
        :rtype: tuple
        """
        return self._x, self._y

    @property
    def capacity(self):
        """
        :return: carrying capacity of cell
        :rtype: float
        """
        return self._variables.capacity

    @capacity.setter
    def capacity(self, carrying_capacity):
        """
        :param carrying_capacity: carrying capacity of cell
        :type carrying_capacity: float

        :raises ValueError: if value is not in range [0, 1]
        """
        if not 0 < carrying_capacity < 1:
            msg = f'Carrying capacity is a value in the range [0, 1]; {carrying_capacity} is given.'
            raise ValueError(msg)

        self._variables.capacity = carrying_capacity

    @property
    def water_depth(self):
        """
        :return: water depth at cell location
        :rtype: float
        """
        return self._variables.water_depth

    @water_depth.setter
    def water_depth(self, depth):
        """
        :param depth: water depth at cell location
        :type depth: float
        """
        self._variables.water_depth = depth

    @property
    def flow_velocity(self):
        """
        :return: depth-averaged flow velocity
        :rtype: float
        """
        return self._variables.flow_velocity

    @flow_velocity.setter
    def flow_velocity(self, velocity):
        """
        :param velocity: depth-averaged flow velocity
        :type velocity: float
        """
        self._variables.flow_velocity = velocity

    def get_var(self, variable):
        """Get cell characteristic.

        :param variable: cell characteristic
        :type variable: str
        """
        if hasattr(self._variables, variable):
            return getattr(self._variables, variable)
        LOG.warning(f'{self} does not have the characteristic \"{variable}\".')

    @classmethod
    def get_cells(cls):
        """Get all defined cells.

        :return: grid cells
        :rtype: set
        """
        return list(cls._cells.values())


class Grid:
    #TODO: This class should (eventually) be able to read the grid from DFM - I guess.
    _cells = set()

    def __init__(self, x=None, y=None):
        """
        :param x: x-coordinate(s), defaults to None
        :param y: y-coordinate(s), defaults to None

        :type x: float, int, iterable, optional
        :type y: float, int, iterable, optional
        """
        if not (x is None and y is None):
            self.grid_from_xy(0 if x is None else x, 0 if y is None else y)

    @classmethod
    def grid_from_xy(cls, x, y):
        """Create grid from x- and/or y-coordinates.

        :param x: x-coordinate(s)
        :param y: y-coordinate(s)

        :type x: float, int, iterable
        :type y: float, int, iterable
        """
        def size(_v):
            """
            :param _v: variable
            :return: variable length
            """
            try:
                return len(_v)
            except TypeError:
                return 1

        # x,y-sizes
        x_len = size(x)
        y_len = size(y)
        if (x_len > 1 and y_len > 1) and not x_len == y_len:
            raise ValueError

        # x,y as arrays
        x_array = x if x_len > 1 else [x] * y_len
        y_array = y if y_len > 1 else [y] * x_len

        # add cells
        [cls.add_cell(xx, yy) for xx, yy in zip(x_array, y_array)]

    @property
    def cells(self):
        """
        :return: cells included in the grid
        :rtype: set
        """
        return self.get_cells()

    @classmethod
    def get_cells(cls):
        """Get grid cells."""
        return cls._cells

    @property
    def number_of_cells(self):
        """
        :return: number of cells included in the grid
        :rtype: int
        """
        return self.get_size()

    @property
    def size(self):
        """
        :return: size of grid (i.e. number of cells)
        :rtype: int
        """
        return self.get_size()

    @classmethod
    def get_size(cls):
        """Get size of grid, i.e. number of cells."""
        return len(cls._cells)

    @staticmethod
    def _create_array(range_, spacing, edge='round'):
        """Create array of equally spaced coordinates.

        :param range_: range of the array
        :param spacing: spacing between coordinates
        :param edge: edge-case method, defaults to 'round'

        :type range_: iterable
        :type spacing: float
        :type edge: str, optional
        """
        different_max = False

        dist = max(range_) - min(range_)

        if dist % spacing:
            LOG.warning(
                f'Range cannot be equally subdivided. Edge-case method \"{edge}\" used:'
                f'\n\trange  \t:\t{range_}'
                f'\n\tspacing\t:\t{spacing}'
            )
            different_max = True

        edges = ('round', 'above', 'below')
        if edge == 'round':
            n = round(dist / spacing)
        elif edge == 'above':
            n = dist // spacing + (1 if different_max else 0)
        elif edge == 'below':
            n = dist // spacing
        else:
            msg = f'Unknown edge-case method: choose one of {edges}.'
            raise ValueError(msg)

        max_ = min(range_) + n * spacing
        if different_max:
            LOG.warning(f'Modified range\t:\t{min(range_), max_}')

        return np.linspace(min(range_), max_, int(n + 1))

    @classmethod
    def add_transect(cls, x_range, spacing, edge='round'):
        """Add transect of cells, where all y-coordinates are set equal to 0.

        :param x_range: range of x-coordinates
        :param spacing: spacing between cells
        :param edge: edge-case method, defaults to 'round'

        :type x_range: iterable
        :type spacing: float
        :type edge: str, optional
        """
        # create array of x-coordinates
        array = cls._create_array(x_range, spacing, edge)
        # create cells at x-coordinates
        [cls._cells.add(Cell(x, 0)) for x in array]

    @classmethod
    def add_square(cls, xy_range, spacing, edge='round'):
        """Add square grid of cells.

        :param xy_range: range of x- and y-coordinates
        :param spacing: spacing between cells
        :param edge: edge-case method, defaults to 'round'

        :type xy_range: iterable
        :type spacing: float
        :type edge: str, optional
        """
        cls.add_rectangle(xy_range, xy_range, spacing, edge)

    @classmethod
    def add_rectangle(cls, x_range, y_range, spacing, edge='round'):
        """Add rectangular grid of cells.

        :param x_range: range of x-coordinates
        :param y_range: range of y-coordinates
        :param spacing: spacing between cells
        :param edge: edge-case method, defaults to 'round'

        :type x_range: iterable
        :type y_range: iterable
        :type spacing: float
        :type edge: str, optional
        """
        # create arrays of x- and y-coordinates
        x_array = cls._create_array(x_range, spacing, edge)
        y_array = cls._create_array(y_range, spacing, edge)
        # create cells at (x,y)-coordinates
        [cls._cells.add(Cell(x, y)) for x in x_array for y in y_array]

    @classmethod
    def add_cell(cls, x, y, **kwargs):
        """Add individual cell to grid.

        :param x: x-coordinate
        :param y: y-coordinate
        :param kwargs: non-essential cell characteristics

        :type x: float
        :type y: float
        """
        cls._cells.add(Cell(x, y, **kwargs))

    @classmethod
    def reset(cls):
        """Reset grid."""
        cls._cells = set()


if __name__ == '__main__':
    #TODO: Have a little play-around with making a grid yourself; also try to modify the Cell- and _CellVariables-
    # classes by, e.g., removing redundant methods and properties.
    grid = Grid()
    grid.add_rectangle(x_range=[0, 10], y_range=[0, 20], spacing=5)
    #grid.add_square(xy_range=[0,2], spacing=1)
    print(f'Number of cells in grid\t:\t{grid.size}')
    print(f'Cells in grid:\n{grid.cells}')
