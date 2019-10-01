# -*- coding: utf-8 -*-
"""
**core**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the ALEXI developers.

`Description`

Before use this module, set account information in the `Collect/config.yml` file.

**Examples:**
::

    from wateraccounting.Collect import core

.. note::

    config.yml is in **"src/wateraccounting/Collect"** module.

.. warning::

    TODO, 20190931, QPan, core.py

    1. Create config.yml contains
        a. Portal name
        b. Portal url
        c. Portal data name, directory
        d. Portal data range, resolution
        e. Portal data file name template on ftp
        f. Portal data file name template on local
    2. Add exception to check data meta information
    3. Estimate data size and tiff location to decided download or not
    4. Add unit test, and test datasets under "tests/data"
"""
# General modules
import os
import sys

# Configuration modules
import yaml

# File modules
import gzip
import zipfile
import tarfile

# Data modules
import numpy as np
import pandas as pd

# GIS modules
try:
    from osgeo import gdal, osr
except ImportError:
    import gdal
    import osr

# Global Variables
this = sys.modules[__name__]
this.conf = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml')
this.port = ['NASA', 'GLEAM', 'FTP_WA', 'FTP_WA_GUESS', 'MSWEP', 'Copernicus', 'VITO']
this.user = {'username': '', 'password': ''}


def Accounts(Type=None):
    """Save user account and password.

    This is the main function to configure user's credentials.
    Don't synchronize the details to github.

    Args:
      Type (str): portal name

    Returns:
      dict: {'username': '', 'password': ''}

    :Example:

        >>> from wateraccounting.Collect.core import Accounts
        >>> user = Accounts(Type='test')
        Traceback (most recent call last):
            ...
        KeyError: 'test'

        >>> user = Accounts(Type='FTP_WA_GUESS')
        >>> user
        {'username': 'wateraccountingguest', 'password': 'W@t3r@ccounting'}
    """
    _file = this.conf
    _list = this.port
    _user = this.user

    if os.path.exists(_file):
        with open(_file, 'r') as fp_cfg:
            conf = yaml.load(fp_cfg, Loader=yaml.FullLoader)

            if Type in _list:
                _user = conf['account'][Type]
            else:
                raise KeyError("{err} not supported {list}.".format(
                    err=Type, list=_list))
    elif IOError:
        raise IOError("{file} not found.".format(file=_file))
        sys.exit(1)
    return _user


def Open_tiff_array(file='', band=''):
    """Load tiff data

    This function load tiff band as numpy.ndarray.

    Args:
      file (str): 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(file))
        string that defines the input tiff file or gdal file
      band (int): Defines the band of the tiff that must be opened

    Returns:
      :obj:`numpy.ndarray`: data

    :Example:

        >>> from wateraccounting.Collect.core import Open_tiff_array
        >>> file = 'tests/data/BigTIFF/Classic.tif'
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

    if band is '':
        band = 1

    f = gdal.Open(file)
    if f is not None:
        try:
            Data = f.GetRasterBand(band).ReadAsArray()
        except AttributeError as err:
            raise AttributeError('Band {band} not found.'.format(band=band))
    else:
        raise IOError('{} not found.'.format(file))

    return Data


def Extract_Data_gz(file, outfile):
    """Extract zip file

    This function extract zip file as gz file.

    Args:
      file (str): 'C:/file/to/path/file.zip' name of the file that must be unzipped
      outfile (str): directory where the unzipped data must be stored

    :Example:

        >>> from wateraccounting.Collect.core import Extract_Data_gz
    """

    with gzip.GzipFile(file, 'rb') as zf:
        file_content = zf.read()
        save_file_content = open(outfile, 'wb')
        save_file_content.write(file_content)
    save_file_content.close()
    zf.close()
    os.remove(file)


def Save_as_tiff(name='', data='', geo='', projection=''):
    """Save as tiff

    This function save the array as a geotiff.

    Args:
      name (str): directory name
      data (:obj:`numpy.ndarray`): dataset of the geotiff
      geo (list): geospatial dataset, [minimum lon, pixelsize, rotation,
        maximum lat, rotation, pixelsize]
      projection (int): the EPSG code

    :Example:

        >>> from wateraccounting.Collect.core import Open_tiff_array
        >>> from wateraccounting.Collect.core import Save_as_tiff
        >>> file = 'tests/data/BigTIFF/Classic.tif'
        >>> test = 'tests/data/BigTIFF/test.tif'

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
                except:
                    srse.ImportFromWkt(projection)
        except:
            try:
                srse.ImportFromEPSG(int(projection))
            except:
                srse.ImportFromWkt(projection)

    dst_ds.SetProjection(srse.ExportToWkt())
    dst_ds.SetGeoTransform(geo)
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds = None

    return


def WaitBar(i, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """Wait Bar Console

    This function will print a waitbar in the console

    Args:
      i (int): Iteration number
      total (int): Total iterations
      prefix (str): Prefix name of bar
      suffix (str): Suffix name of bar
      decimals (int): decimal of the wait bar
      length (int): width of the wait bar
      fill (str): bar fill
    """
    import sys
    import os

    # Adjust when it is a linux computer
    if os.name == "posix" and total == 0:
        total = 0.0001

    percent = ("{0:." + str(decimals) + "f}").format(100 * (i / float(total)))
    filled = int(length * i // total)
    bar = fill * filled + '-' * (length - filled)

    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    sys.stdout.flush()

    if i == total:
        print()
