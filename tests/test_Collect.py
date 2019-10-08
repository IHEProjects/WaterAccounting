# -*- coding: utf-8 -*-
"""
"""
import os
import numpy as np

import pytest

import wateraccounting.Collect.credential as credential
import wateraccounting.Collect.collect as collect

import wateraccounting.Collect.ALEXI as ALEXI
import wateraccounting.Collect.ASCAT as ASCAT

__author__ = "Quan Pan"
__copyright__ = "Quan Pan"
__license__ = "apache"

__path = os.path.dirname(os.path.realpath(__file__))
__path_data = os.path.join(__path, 'data')


def test_credential():
    path = __path_data
    file_org = 'config-test.yml'
    file_enc = 'config-test.yml-encrypted'
    password = 'WaterAccounting'

    key1 = credential.get_key(password)
    key2 = credential.encrypt_cfg(path, file_org, password)
    conf = credential.decrypt_cfg(path, file_enc, password)

    assert len(key1) == 44
    assert len(key2) == 44
    assert key1.decode('utf8') == key2.decode('utf8')
    assert type(conf) == str

    # credential.encrypt_cfg('', 'config.yml', 'WaterAccounting')
    # with pytest.raises(FileNotFoundError, match=r".* No .*"):
    #     credential.encrypt_cfg('', 'config.yml', 'WaterAccounting')


def test_collect_Accounts():
    path = __path_data
    file = 'config-test.yml-encrypted'
    password = 'WaterAccounting'

    assert collect.Accounts(path, file, password, 'FTP_WA_GUESS') == {
        'username': 'wateraccountingguest',
        'password': 'W@t3r@ccounting'}

    with pytest.raises(KeyError, match=r".* not .*"):
        collect.Accounts(path, file, password, 'test')


def test_collect_Open_tiff_array():
    path = __path_data
    file = os.path.join(path, 'BigTIFF', 'Classic.tif')
    data = collect.Open_tiff_array(file, 1)

    assert type(data) == np.ndarray
    assert data.shape == (64, 64)

    with pytest.raises(AttributeError, match=r".* not .*"):
        collect.Open_tiff_array(file, 99)


def test_collect_Save_as_tiff():
    path = __path_data

    file_in = os.path.join(path, 'BigTIFF', 'Classic.tif')
    data = collect.Open_tiff_array(file_in, 1)

    file_out = os.path.join(path, 'BigTIFF', 'test.tif')
    collect.Save_as_tiff(file_out, data, [0, 1, 0, 0, 1, 0], "WGS84")
    data = collect.Open_tiff_array(file_out, 1)

    assert type(data) == np.ndarray
    assert data.shape == (64, 64)


def test_ALEXI():
    # assert ALEXI.__version__ == '0.1'
    path = os.path.join(__path_data, 'download')

    timestep = 'daily'
    ALEXI.DownloadData(
        Dir=path,
        Startdate='2007-02-01', Enddate='2007-03-01',
        latlim=[50, 54], lonlim=[3, 7],
        TimeStep=timestep,
        Waitbar=1)
    nfiles = len(os.listdir(os.path.join(
        __path_data, 'download',
        'Evaporation', 'ALEXI', 'Daily')))
    print(nfiles)
    assert nfiles > 0

    timestep = 'weekly'
    ALEXI.DownloadData(
        Dir=path,
        Startdate='2007-02-01', Enddate='2007-03-01',
        latlim=[50, 54], lonlim=[3, 7],
        TimeStep=timestep,
        Waitbar=1)
    nfiles = len(os.listdir(os.path.join(
        path,
        'Evaporation', 'ALEXI', 'Weekly')))
    print(nfiles)
    assert nfiles > 0


def test_ASCAT():
    # assert ASCAT.__version__ == '0.1'
    path = os.path.join(__path_data, 'download')

    ASCAT.DownloadData(
        Dir=path,
        Startdate='2007-02-01', Enddate='2007-03-01',
        latlim=[50, 54], lonlim=[3, 7],
        TimeStep='daily',
        Waitbar=1)
    nfiles = len(os.listdir(os.path.join(
        path,
        'SWI', 'ASCAT', 'Daily')))
    print(nfiles)
    assert nfiles > 0
