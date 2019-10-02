# -*- coding: utf-8 -*-
"""
"""
import os
import numpy as np

import pytest

import wateraccounting.Collect.credential as credential
import wateraccounting.Collect.core as core
import wateraccounting.Collect.ALEXI as ALEXI

__author__ = "Quan Pan"
__copyright__ = "Quan Pan"
__license__ = "apache"

__path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
__path_data = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


# import wateraccounting.Collect as Collect
# def test_Collect():
#     assert Collect.__version__ == '0.0.1'


def test_credential():
    path = __path_data
    file_org = 'config-example.yml'
    file_enc = 'config-example.yml-encrypted'
    password = 'WaterAccounting'

    key1 = credential.get_key(password)
    key2 = credential.encrypt_cfg(path, file_org, password)
    conf = credential.decrypt_cfg(path, file_enc, password)

    assert len(key1) == 44
    assert len(key2) == 44
    assert key1.decode('utf8') == key2.decode('utf8')
    assert type(conf) == str


def test_core_Accounts():
    path = __path_data
    file = 'config-example.yml-encrypted'
    password = 'WaterAccounting'

    assert core.Accounts(path, file, password, 'FTP_WA_GUESS') == \
           {'username': 'wateraccountingguest',
            'password': 'W@t3r@ccounting'}

    with pytest.raises(KeyError, match=r".* not .*"):
        core.Accounts(path, file, password, 'test')


def test_core_Open_tiff_array():
    path = __path_data
    file = os.path.join(path, 'BigTIFF', 'Classic.tif')
    data = core.Open_tiff_array(file, 1)

    assert type(data) == np.ndarray
    assert data.shape == (64, 64)

    with pytest.raises(AttributeError, match=r".* not .*"):
        core.Open_tiff_array(file, 99)


def test_core_Save_as_tiff():
    path = __path_data

    file_in = os.path.join(path, 'BigTIFF', 'Classic.tif')
    data = core.Open_tiff_array(file_in, 1)

    file_out = os.path.join(path, 'BigTIFF', 'test.tif')
    core.Save_as_tiff(file_out, data, [0, 1, 0, 0, 1, 0], "WGS84")
    data = core.Open_tiff_array(file_out, 1)

    assert type(data) == np.ndarray
    assert data.shape == (64, 64)


def test_ALEXI():
    assert ALEXI.__version__ == '0.1'

    ALEXI.DataAccess.DownloadData(Dir=os.path.join(__path_data, 'download'),
                                  Startdate='2005-01-01', Enddate='2005-02-01',
                                  latlim=[50, 54], lonlim=[3, 7], TimeStep='daily',
                                  Waitbar=1)
