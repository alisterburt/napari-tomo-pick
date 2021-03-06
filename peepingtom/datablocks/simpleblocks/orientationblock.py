import numpy as np
import xarray as xr

from .simpleblock import SimpleBlock


class OrientationBlock(SimpleBlock):
    """
    OrientationBlock objects represent orientations in a 2d or 3d space

    Contains factory methods for instantiation from eulerian angles

    data : (n, 2, 2) or (n, 3, 3) array of rotation matrices R
                        R should satisfy Rv = v' where v is a column vector

    """
    def _data_setter(self, data=()):
        data = np.array(data)
        # check for single matrix case and assert dimensionality
        val_error = ValueError(f'rotation matrices should be of shape '
                               f'(2, 2), (3, 3), (n, 2, 2) or (n, 3, 3), '
                               f'not {data.shape}')
        if data.ndim == 1:
            raise val_error
        if not data.shape[-1] == data.shape[-2]:
            raise val_error
        if not data.shape[-1] in (2, 3):
            raise val_error

        if data.ndim == 2:
            m = data.shape[-1]
            data = data.reshape((1, m, m))

        dims = ['x', 'y', 'z']
        return xr.DataArray(data, dims=['n', 'spatial', 'spatial2'],
                            coords=(range(len(data)), dims[:data.shape[1]], dims[:data.shape[1]]))

    @property
    def n(self):
        return len(self)

    @property
    def ndim(self):
        return self.data.shape[-1]

    def _unit_vector(self, axis: str):
        """
        Get a unit vector along a specified axis which matches the dimensionality of the VectorBlock object
        axis : str, named axis 'x', 'y' (or 'z')
        """
        # check dimensionality
        if self.ndim > 3:
            raise NotImplementedError('Unit vector generation for objects with greater '
                                      'than 3 spatial dimensions is not implemented')

        # initialise unit vector array
        unit_vector = xr.zeros_like(self.data.spatial, dtype=float)

        # construct unit vector
        unit_vector.loc[axis] = 1

        return unit_vector

    def oriented_vectors(self, axis):
        return xr.DataArray(np.dot(self.data, self._unit_vector(axis)),
                            dims=self.data.dims[:-1],
                            coords=[self.data.n, self.data.spatial])

    def __shape_repr__(self):
        return f'({self.n}, {self.ndim})'
