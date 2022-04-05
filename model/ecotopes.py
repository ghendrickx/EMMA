
class Ecotope:

    def __init__(self, **kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]

        self.__type = self.ecotope_type(**kwargs)

    @staticmethod
    def ecotope_type(**kwargs):
        args = list(kwargs.values())
        if args[0] < 1:
            return 'ecotope-1'
        elif args[1] < 1:
            return 'ecotope-2'

    @property
    def type(self):
        return self.__type


class EcotopeSearcher:

    def __init__(self, **kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]

    def __call__(self, *args, **kwargs):
        return self.ecotope_type(**kwargs)

    @staticmethod
    def ecotope_type(**kwargs):
        if kwargs['flow'] < 1:
            return Ecotope1(cell=1)
        elif kwargs['depth'] < 1:
            return 'ecotope-2'


class _Ecotope:
    def __init__(self, cell):
        pass


class Ecotope1(_Ecotope):
    _size = 0
    _cells = set()

    def __init__(self, cell):
        super().__init__(cell=cell)
        self._increment()
        self._add_cel(cell)

    @classmethod
    def _increment(cls):
        cls._size += 1

    @classmethod
    def _add_cel(cls, cell):
        cls._cells.add(cell)

    def __str__(self):
        return 'ecotope-1'


if __name__ == '__main__':
    eco = Ecotope(flow=.5, depth=5)
    print(eco.type)
