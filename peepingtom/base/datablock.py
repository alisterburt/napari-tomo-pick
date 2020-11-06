from .blockbasedata import BlockBaseData


class DataBlock(list):
    """
    represents a collection of data objects within the same n-dimensional reference space
    """
    # TODO: add napari-like indexing by attribute or by type
    def __init__(self, iterable=()):
        super().__init__(iterable)
        if not all([isinstance(i, BlockBaseData) for i in iterable]):
            raise Exception('DataBlock can only collect BaseData objects')
