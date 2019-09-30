# -*- coding: utf-8 -*-
"""
"""
import os
import numpy as np

import pytest

# import wateraccounting.Collect as Collect
import wateraccounting.Collect.core as core
import wateraccounting.Collect.ALEXI as ALEXI

__author__ = "Quan Pan"
__copyright__ = "Quan Pan"
__license__ = "apache"

__dir_data = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


# def test_Collect():
#     assert Collect.__version__ == '0.0.1'


def test_core_Accounts():
    assert core.Accounts('FTP_WA') == \
           {'username': 'wateraccountingguest',
            'password': 'W@t3r@ccounting'}

    with pytest.raises(KeyError, match=r".* not .*"):
        core.Accounts('test')


def test_core_Open_tiff_array():
    file = os.path.join(__dir_data, 'BigTIFF', 'Classic.tif')
    data = core.Open_tiff_array(file, 1)

    assert type(data) == np.ndarray
    assert data.shape == (64, 64)

    with pytest.raises(AttributeError, match=r".* not .*"):
        core.Open_tiff_array(file, 99)


def test_core_Save_as_tiff():
    fn_in = os.path.join(__dir_data, 'BigTIFF', 'Classic.tif')
    data = core.Open_tiff_array(fn_in, 1)

    fn_out = os.path.join(__dir_data, 'BigTIFF', 'test.tif')
    core.Save_as_tiff(fn_out, data, [0, 1, 0, 0, 1, 0], "WGS84")
    data = core.Open_tiff_array(fn_out, 1)

    assert type(data) == np.ndarray
    assert data.shape == (64, 64)


def test_ALEXI():
    assert ALEXI.__version__ == '0.1'

    ALEXI.DataAccess.DownloadData(Dir=os.path.join(__dir_data, 'download'),
                                  Startdate='2003-01-01', Enddate='2003-02-01',
                                  latlim=[50, 54], lonlim=[3, 7], TimeStep='daily',
                                  Waitbar=1)
