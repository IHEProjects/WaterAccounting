# -*- coding: utf-8 -*-
"""
**Name**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team.

`Description`

des

**Examples:**
::

    from wateraccounting import module
"""
import os
import sys
import inspect
# import shutil
# import yaml
# import gzip

import numpy as np

try:
    from osgeo import gdal, osr
except ImportError:
    import gdal
    import osr

try:
    # setup.py
    from . import collect
except ImportError:
    # PyCharm
    from src.wateraccounting.Collect import collect


class GIS(collect.Collect):
    """This Base class

    Description

    Args:
      workspace (str): Directory to config.yml.
      account (str): Account name of data portal.
      is_status (bool): Is to print status message.
      kwargs (dict): Other arguments.
    """
    __path = 'GIS'

    def __init__(self, workspace, account, is_status, **kwargs):
        """Class instantiation
        """
        # collect.Collect.__init__(self, workspace, account)
        super(GIS, self).__init__(workspace, account,
                                  is_status=is_status, **kwargs)

    def get_tiff(self, file='', band=1):
        """Get tiff band data

        This function get tiff band as numpy.ndarray.

        Args:
          file (str): 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(file))
            string that defines the input tiff file or gdal file.
          band (int): Defines the band of the tiff that must be opened.

        Returns:
          :obj:`numpy.ndarray`: Band data.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.gis import GIS
            >>> path = os.path.join(os.getcwd(), 'tests', 'data', 'BigTIFF')
            >>> file = os.path.join(path, 'Classic.tif')
            >>> data = Open_tiff_array(file, 1)

            >>> type(data)
            <class 'numpy.ndarray'>

            >>> data.shape
            (64, 64)

            >>> data
            array([[255, 255, 255, ...   0,   0,   0],
                   [255, 255, 255, ...   0,   0,   0],
                   [255, 255, 255, ...   0,   0,   0],
                   ...,
                   [  0,   0,   0, ...,   0,   0,   0],
                   [  0,   0,   0, ...,   0,   0,   0],
                   [  0,   0,   0, ...,   0,   0,   0]], dtype=uint8)
        """
        Data = np.ndarray

        if band == '':
            band = 1

        f = gdal.Open(file)
        if f is not None:
            try:
                Data = f.GetRasterBand(band).ReadAsArray()
            except AttributeError:
                raise AttributeError('Band {band} not found.'.format(band=band))
        else:
            raise IOError('{} not found.'.format(file))

        return Data

    def save_as_tiff(self, name='', data='', geo='', projection=''):
        """Save as tiff

        This function save the array as a geotiff.

        Args:
          name (str): Directory name.
          data (:obj:`numpy.ndarray`): Dataset of the geotiff.
          geo (list): Geospatial dataset, [minimum lon, pixelsize, rotation,
            maximum lat, rotation, pixelsize].
          projection (int): EPSG code.

        :Example:

            >>> from wateraccounting.Collect.collect import Open_tiff_array
            >>> from wateraccounting.Collect.collect import Save_as_tiff
            >>> path = os.path.join(os.getcwd(), 'tests', 'data', 'BigTIFF')
            >>> file = os.path.join(path, 'Classic.tif')
            >>> test = os.path.join(path, 'test.tif')

            >>> data = Open_tiff_array(file, 1)
            >>> data
            array([[255, 255, 255, ...   0,   0,   0],
                   [255, 255, 255, ...   0,   0,   0],
                   [255, 255, 255, ...   0,   0,   0],
                   ...,
                   [  0,   0,   0, ...,   0,   0,   0],
                   [  0,   0,   0, ...,   0,   0,   0],
                   [  0,   0,   0, ...,   0,   0,   0]], dtype=uint8)

            >>> Save_as_tiff(test, data, [0, 1, 0, 0, 1, 0], "WGS84")
            >>> data = Open_tiff_array(test, 1)
            >>> data
            array([[255., 255., 255., ...   0.,   0.,   0.],
                   [255., 255., 255., ...   0.,   0.,   0.],
                   [255., 255., 255., ...   0.,   0.,   0.],
                   ...,
                   [  0.,   0.,   0., ...,   0.,   0.,   0.],
                   [  0.,   0.,   0., ...,   0.,   0.,   0.],
                   [  0.,   0.,   0., ...,   0.,   0.,   0.]], dtype=float32)
        """
        # save as a geotiff
        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(name, int(data.shape[1]), int(data.shape[0]), 1,
                               gdal.GDT_Float32, ['COMPRESS=LZW'])
        srse = osr.SpatialReference()
        if projection == '':
            srse.SetWellKnownGeogCS("WGS84")

        else:
            try:
                if not srse.SetWellKnownGeogCS(projection) == 6:
                    srse.SetWellKnownGeogCS(projection)
                else:
                    try:
                        srse.ImportFromEPSG(int(projection))
                    except BaseException as err:
                        print(err)
                    else:
                        srse.ImportFromWkt(projection)
            except BaseException:
                try:
                    srse.ImportFromEPSG(int(projection))
                except BaseException as err:
                    print(err)
                else:
                    srse.ImportFromWkt(projection)

        dst_ds.SetProjection(srse.ExportToWkt())
        dst_ds.SetGeoTransform(geo)
        dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
        dst_ds.GetRasterBand(1).WriteArray(data)
        dst_ds = None

        return


def main():
    from pprint import pprint

    print('\nGIS\n=====')
    gis = GIS('',
              # '', 'is_status': False)
              # 'test', is_status=False)
              'FTP_WA', is_status=False)
              # 'Copernicus', is_status=False)

    # print('\ngis._Collect__conf\n=====')
    # pprint(gis._Collect__conf)
    # print('\ngis._Collect__user\n=====')
    # pprint(gis._Collect__user)


if __name__ == "__main__":
    main()
