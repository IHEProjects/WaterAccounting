# -*- coding: utf-8 -*-
"""
**CMRSET**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team.

`Description`

This module downloads CMRSET data from
``ftp.wateraccounting.unesco-ihe.org``.

Use the CMRSET.monthly function to download
and create weekly ALEXI images in Gtiff format.

The data is available between ``2003-01-01 till 2015-12-31``.

The output file with the name ``2003.01.01`` contains
the **total evaporation** in ``mm`` for the period of ``1 January - 7 January``.

**Examples:**
::

    from wateraccounting.Collect import CMRSET
    CMRSET.monthly(Dir='C:/Temp/',
                Startdate='2003-12-01', Enddate='2004-01-20',
                latlim=[-10, 30], lonlim=[-20, -10])
"""
# General modules
import os
# import sys
# import glob
# import shutil

# # import math
# # import datetime

from ftplib import FTP
# from joblib import Parallel, delayed

import numpy as np
import pandas as pd
# from netCDF4 import Dataset

# Water Accounting Modules
try:
    from .download import Download
except ImportError:
    from src.wateraccounting.Collect.download import Download


def DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar):
    """
    This scripts downloads CMRSET ET data from the UNESCO-IHE ftp server.
    The output files display the total ET in mm for a period of one month.
    The name of the file corresponds to the first day of the month.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    lonlim -- [ymin, ymax] (values must be between -90 and 90)
    latlim -- [xmin, xmax] (values must be between -180 and 180)
    """
    # Check the latitude and longitude and otherwise set lat or lon on greatest extent
    if latlim[0] < -90 or latlim[1] > 90:
        print('Latitude above 90N or below -90S is not possible. Value set to maximum')
        latlim[0] = np.max(latlim[0], -90)
        latlim[1] = np.min(latlim[1], 90)
    if lonlim[0] < -180 or lonlim[1] > 180:
        print('Longitude must be between 180E and 180W. Now value is set to maximum')
        lonlim[0] = np.max(lonlim[0], -180)
        lonlim[1] = np.min(lonlim[1], 180)

    # Check Startdate and Enddate
    if not Startdate:
        Startdate = pd.Timestamp('2000-01-01')
    if not Enddate:
        Enddate = pd.Timestamp('2012-12-31')

    # Creates dates library
    Dates = pd.date_range(Startdate, Enddate, freq="MS")

    # Create Waitbar
    if Waitbar == 1:
        import watools.Functions.Start.WaitbarConsole as WaitbarConsole
        total_amount = len(Dates)
        amount = 0
        WaitbarConsole.printWaitBar(amount, total_amount, prefix='Progress:',
                                    suffix='Complete', length=50)

    # Define directory and create it if not exists
    output_folder = os.path.join(Dir, 'Evaporation', 'CMRSET', 'Monthly')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for Date in Dates:

        # Define year and month
        year = Date.year
        month = Date.month

        # Date as printed in filename
        Filename_out = os.path.join(output_folder,
                                    'ETa_CMRSET_mm-month-1_monthly_%s.%02s.%02s.tif' % (
                                    Date.strftime('%Y'), Date.strftime('%m'),
                                    Date.strftime('%d')))

        # Define end filename
        Filename_in = os.path.join("M01CMRSETGlobalY%dM%02d.tif" % (year, month))

        # Temporary filename for the downloaded global file
        local_filename = os.path.join(output_folder, Filename_in)

        # Download the data from FTP server if the file not exists
        if not os.path.exists(Filename_out):
            try:
                Download_CMRSET_from_WA_FTP(local_filename, Filename_in)

                # Clip dataset
                RC.Clip_Dataset_GDAL(local_filename, Filename_out, latlim, lonlim)
                os.remove(local_filename)

            except:
                print("Was not able to download file with date %s" % Date)

        # Adjust waitbar
        if Waitbar == 1:
            amount += 1
            WaitbarConsole.printWaitBar(amount, total_amount, prefix='Progress:',
                                        suffix='Complete', length=50)

    return


def Download_CMRSET_from_WA_FTP(local_filename, Filename_in):
    """
    This function retrieves CMRSET data for a given date from the
    ftp.wateraccounting.unesco-ihe.org server.

    Restrictions:
    The data and this python file may not be distributed to others without
    permission of the WA+ team due data restriction of the CMRSET developers.

    Keyword arguments:
	 local_filename -- name of the temporary file which contains global CMRSET data
    Filename_in -- name of the end file with the monthly CMRSET data
    """

    # Collect account and FTP information
    username, password = WebAccounts.Accounts(Type='FTP_WA')
    ftpserver = "ftp.wateraccounting.unesco-ihe.org"

    # Download data from FTP
    ftp = FTP(ftpserver)
    ftp.login(username, password)
    directory = "/WaterAccounting/Data_Satellite/Evaporation/CMRSET/Global/"
    ftp.cwd(directory)
    lf = open(local_filename, "wb")
    ftp.retrbinary("RETR " + Filename_in, lf.write)
    lf.close()

    return
