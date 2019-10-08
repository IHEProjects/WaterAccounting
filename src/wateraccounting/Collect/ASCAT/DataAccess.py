# -*- coding: utf-8 -*-
"""
**ASCAT.DataAccess**

This script collects ASCAT data from the VITO server.

The data has a daily temporal resolution
and a spatial resolution of ``0.25`` degree.

The resulting tiff files are in the ``WGS84`` projection.

The data is available between ``2007-01-01`` till ``present``.

**Examples:**
::

    from wateraccounting.Collect.ASCAT.DataAccess import ASCAT
    ASCAT.DownloadData(Dir=os.path.join(__dir_data, 'download'),
                       Startdate='2005-01-01', Enddate='2005-02-01',
                       latlim=[50, 54], lonlim=[3, 7],
                       Waitbar=1)
"""
# General modules
import os
# import shutil
import requests
from requests.auth import HTTPBasicAuth

import numpy as np
import pandas as pd
# import h5py
from netCDF4 import Dataset

# Water Accounting Modules
import wateraccounting.Collect.collect as collect


# Global Variables
# this = sys.modules[__name__]


def _get_user():
    """Get user information from ``config.yml-encrypted``

    Returns:
      dict: {'username': '', 'password': ''}.
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..', '..', '..', '..'))
    file = 'config.yml-encrypted'
    password = 'WaterAccounting'

    user = collect.Accounts(path, file, password, Type='Copernicus')
    # print(path, user)

    return user


def DownloadData(Dir, Startdate, Enddate, latlim, lonlim, TimeStep, Waitbar):
    """Downloads ASCAT SWI data

    This scripts downloads ASCAT SWI data from the VITO server.
    The output files display the Surface Water Index.

    Args:
      Dir (str): 'C:/file/to/path/'.
      Startdate (str): 'yyyy-mm-dd'.
      Enddate (str): 'yyyy-mm-dd'.
      latlim (list): [ymin, ymax] (values must be between -60 and 70).
      lonlim (list): [xmin, xmax] (values must be between -180 and 180).
      TimeStep (str): 'daily' or 'weekly' (by using here monthly,
        an older dataset will be used).
      Waitbar (bool): Waitbar.

    :Example:

        >>> print('Example')
        Example
    """

    # Check the latitude and longitude and otherwise reset lat and lon.
    if latlim[0] < -90 or latlim[1] > 90:
        print('Latitude above 90N or below 90S is not possible.\
            Value set to maximum')
        latlim[0] = np.max(latlim[0], -90)
        latlim[1] = np.min(latlim[1], 90)
    if lonlim[0] < -180 or lonlim[1] > 180:
        print('Longitude must be between 180E and 180W.\
            Now value is set to maximum')
        lonlim[0] = np.max(lonlim[0], -180)
        lonlim[1] = np.min(lonlim[1], 180)

    # Check Startdate and Enddate
    if not Startdate:
        Startdate = pd.Timestamp('2007-01-01')
    if not Enddate:
        Enddate = pd.Timestamp.now()

    # Make a panda timestamp of the date
    try:
        Enddate = pd.Timestamp(Enddate)
    except BaseException:
        Enddate = Enddate

    # amount of Dates weekly
    Dates = pd.date_range(Startdate, Enddate, freq='D')

    # Create Waitbar
    total_amount = len(Dates)
    if Waitbar == 1:
        amount = 0
        collect.WaitBar(amount, total_amount,
                        prefix='ASCAT:', suffix='Complete',
                        length=50)

    # Define directory and create it if not exists
    output_folder = os.path.join(Dir, 'SWI', 'ASCAT', 'Daily')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_folder_temp = os.path.join(Dir, 'SWI', 'ASCAT', 'Daily', 'Temp')
    if not os.path.exists(output_folder_temp):
        os.makedirs(output_folder_temp)

    # loop over dates
    for Date in Dates:

        # Define end filename
        End_filename = os.path.join(output_folder,
                                    'SWI_ASCAT_V3_Percentage_daily_%d.%02d.%02d.tif'
                                    % (Date.year, Date.month, Date.day))

        # Define IDs
        xID = 1800 + np.int16(np.array([np.ceil((lonlim[0]) * 10),
                                        np.floor((lonlim[1]) * 10)]))

        yID = np.int16(np.array([np.floor((-latlim[1]) * 10),
                                 np.ceil((-latlim[0]) * 10)])) + 900

        # Download the data from FTP server if the file not exists
        if not os.path.exists(End_filename):
            try:
                data = Download_ASCAT_from_VITO(End_filename,
                                                output_folder_temp, Date,
                                                yID, xID)
                # make geotiff file
                geo = [lonlim[0], 0.1, 0, latlim[1], 0, -0.1]
                collect.Save_as_tiff(name=End_filename, data=data,
                                     geo=geo, projection="WGS84")
            except BaseException:
                print("\nWas not able to download file with date %s" % Date)

        # Adjust waitbar
        if Waitbar == 1:
            amount += 1
            collect.WaitBar(amount, total_amount,
                            prefix='ASCAT:', suffix='Complete',
                            length=50)

    # remove the temporary folder
    # shutil.rmtree(output_folder_temp)

    return 'daily'


def Download_ASCAT_from_VITO(End_filename, output_folder_temp, Date, yID, xID):
    """Retrieves ASCAT data

    This function retrieves ASCAT data for a given date from the
    ftp.wateraccounting.unesco-ihe.org server.

    Restrictions:
    The data and this python file may not be distributed to others without
    permission of the WA+ team due data restriction of the ALEXI developers.

    Keyword arguments:

    """
    # Collect account and FTP information
    Link = "https://land.copernicus.vgt.vito.be/PDF/datapool" \
           "/Vegetation/Soil_Water/SWI_V3" \
           "/%s/%s/%s" \
           "/%s/%s"
    user = _get_user()
    username = user['username']
    password = user['password']

    # Define date
    year_data = Date.year
    month_data = Date.month
    day_data = Date.day

    # filename of ASCAT data on server
    ASCAT_date = "%d%02d%02d1200" % (year_data, month_data, day_data)
    ASCAT_name = 'SWI_%s_GLOBE_ASCAT_V3.1.1' % ASCAT_date
    ASCAT_filename = "c_gls_SWI_%s_GLOBE_ASCAT_V3.1.1.nc" % ASCAT_date

    URL = Link % (
        year_data, month_data, day_data,
        ASCAT_name, ASCAT_filename)

    # Output zipfile
    output_ncfile_ASCAT = os.path.join(output_folder_temp, ASCAT_filename)

    # Download the ASCAT data
    try:
        y = requests.get(URL, auth=HTTPBasicAuth(username, password))
    except BaseException:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        y = requests.get(URL, auth=(username, password), verify=False)

    # Write the file in system
    z = open(output_ncfile_ASCAT, 'wb')
    z.write(y.content)
    z.close()

    # Open nc file
    fh = Dataset(output_ncfile_ASCAT)
    dataset = fh.variables['SWI_010'][:, yID[0]:yID[1], xID[0]:xID[1]]
    data = np.squeeze(dataset.data, axis=0)
    data = data * 0.5
    data[data > 100.] = -9999
    fh.close()

    return data
