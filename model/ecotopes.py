"""
Ecotope-definitions

Author: Gijs G. Hendrickx
"""
import sys
import abc


# class Ecotope:
#
#     def __init__(self, **kwargs):
#         [setattr(self, key, value) for key, value in kwargs.items()]
#
#         self.__type = self.ecotope_type(**kwargs)
#
#     @staticmethod
#     def salinity(**kwargs):
#         args = list(kwargs.values())
#         if args[0] >18:
#             return 'Brackish Ecotope:'
#         elif args[0] > 5.4 args[0] < 18:
#             return 'Marine Ecotope:'
#
#     @staticmethod
#     def littoralzone(**kwargs):
#         args = list(kwargs.values())
#         if args[0] = 1:
#             return 'in the sublittoral zone'
#         elif args[0] = 0:
#             return 'in the supralittoral zone'
#         else:
#             return 'in the littoral zone'
#
#     @property
#     def type(self):
#         return self.__type


# Below, I will experiment a bit with the "complicated" set-up for defining ecotopes.


class _Ecotope(abc.ABC):
    """Parent ecotope-object."""
    _cells: set = NotImplemented

    def __new__(cls, *args, **kwargs):
        """Prevent initiation of this parent ecotope-object."""
        if cls is _Ecotope:
            msg = f'Only children of \"{cls.__name__}\" may be initiated.'
            raise TypeError(msg)

        return super().__new__(cls)

    def __init__(self, cell):
        """
        :param cell: grid cell
        :type cell: Cell
        """
        self._cell = cell
        self._add_cell(cell)
        cell.ecotope = self

    def __init_subclass__(cls, **kwargs):
        """Ensure that _Ecotope's children are correctly implemented."""
        super().__init_subclass__(**kwargs)

        if cls._cells is NotImplemented:
            msg = f'Please, implement the `_cells` class attribute.'
            raise NotImplementedError(msg)

    def __len__(self):
        """Length (or size) of an ecotope is defined by the number of cells that are labelled as the ecotope.

        :return: length/size of ecotope
        :rtype: int
        """
        return len(self._cells)

    def __repr__(self):
        """An ecotope is represented by its object-name and the cell that it is linked to.

        :return: object-representation
        :rtype: str
        """
        return f'{self.__class__.__name__}(cell={self.cell})'

    @abc.abstractmethod
    def __str__(self):
        """String-representation: <ecotope>."""

    @property
    def is_ecotope(self):
        """Property proofing that this object - and subsequently its children - is an ecotope.

        :return: ecotope
        :rtype: bool
        """
        return True

    @property
    def cell(self):
        """
        :return: grid cell
        :rtype: Cell
        """
        return self._cell

    @classmethod
    def _add_cell(cls, cell):
        """Add grid cell to the set of cells of this ecotope-object.

        :param cell: grid cell
        :type cell: Cell
        """
        cls._cells.add(cell)

    @classmethod
    @abc.abstractmethod
    def criteria(cls, cell):
        """Test if the criteria of the ecotope are met by the cell's characteristics. To be overwritten by children,
        i.e. ecotopes.

        :param cell: grid cell
        :type cell: Cell

        :return: criteria check
        :rtype: bool
        """
        return False

    @classmethod
    def verify(cls, cell):
        """Verify if the abiotic characteristics assigned to the cell comply with the criteria of the ecotope.

        :param cell: grid cell
        :type cell: Cell

        :return: ecotope-object
        :rtype: _Ecotope
        """
        if cls.criteria(cell):
            return cls.__call__(cell)

    @classmethod
    def get_cells(cls):
        """Get object-level set of grid cells.

        :return: grid cells
        :rtype: set
        """
        return cls._cells

    @property
    def cells(self):
        """
        :return: grid cells
        :rtype: set
        """
        return self.get_cells()


class Ecotope1(_Ecotope):
    """<Ecotope1>-object."""
    _cells = set()

    def __str__(self):
        """String-representation: <Ecotope1>."""
        return 'ecotope-1'

    @classmethod
    def criteria(cls, cell):
        """Criteria of <Ecotope1>.

        :param cell: grid cell
        :type cell: Cell

        :return: criteria met
        :rtype: bool
        """
        if cell.x >= 0:
            return True
        else:
            return False


class Ecotope2(_Ecotope):
    """<Ecotope2>-object."""
    _cells = set()

    def __str__(self):
        """String-representation: <Ecotope2>."""
        return 'ecotope-2'

    @classmethod
    def criteria(cls, cell):
        """Criteria of <Ecotope2>.

        :param cell: grid cell
        :type cell: Cell

        :return: criteria met
        :rtype: bool
        """
        if cell.x < 0:
            return True
        else:
            return False


def ecotope_searcher(cell):
    """Search through ecotopes to determine which ecotope belongs complies with the cell's characteristics.

    :param cell: grid cell
    :type cell: Cell
    """
    # loop through all _Ecotope-children, i.e. subclasses
    for ecotope in _Ecotope.__subclasses__():
        # get class-instance
        cls = getattr(sys.modules[__name__], ecotope.__name__)
        # verify ecotope's criteria
        out = cls.verify(cell)
        # stop searching when ecotope is found
        if isinstance(out, _Ecotope):
            break


def set_ecotopes(grid):
    """Set ecotopes of all grid cells.

    :param grid: grid
    :type grid: Grid
    """
    [ecotope_searcher(cell) for cell in grid.cells]


if __name__ == '__main__':
    from model.grid import Grid, Cell

    Grid.add_square(xy_range=[-10, 10], spacing=10)
    set_ecotopes(Grid())

    print(f'Ecotope1\t:\t{Ecotope1.get_cells()}')
    print(f'Ecotope2\t:\t{Ecotope2.get_cells()}')
    print(f'_Ecotope\t:\t{_Ecotope.get_cells()}')
