# -*- coding: utf-8 -*-
"""
**Download**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team.

`Description`

Before use this module, set account information
in the ``WaterAccounting/accounts.yml`` file.

**Examples:**
::

    import os
    from wateraccounting.Collect.download import Download
    download = Download(os.getcwd(), 'FTP_WA_GUESS', is_status=True)

"""
import os
# import sys
import inspect
# import shutil
# import yaml

import gzip

try:
    from .accounts import Accounts
except ImportError:
    from src.wateraccounting.Collect.accounts import Accounts

try:
    from .gis import GIS
except ImportError:
    from src.wateraccounting.Collect.gis import GIS


class Download(Accounts, GIS):
    """This Download class

    Description

    Args:
      workspace (str): Directory to accounts.yml.
      account (str): Account name of data product.
      is_status (bool): Is to print status message.
      kwargs (dict): Other arguments.
    """
    __conf = {
        'path': '',
        'file': '',
        'data': {}
    }

    def __init__(self, workspace='', account='', is_status=True, **kwargs):
        """Class instantiation
        """
        Accounts.__init__(self, workspace, account, is_status, **kwargs)
        GIS.__init__(self, workspace, is_status, **kwargs)
        # super(Download, self).__init__(workspace, account, is_status, **kwargs)
        self.stmsg = {
            0: 'S: WA.Download "{f}" status {c}: {m}',
            1: 'E: WA.Download "{f}" status {c}: {m}',
            2: 'W: WA.Download "{f}" status {c}: {m}',
        }
        self.stcode = 0
        self.status = 'Download status.'
        self.is_status = is_status

        if self.stcode == 0:
            # self._conf()
            message = ''

        self._status(
            inspect.currentframe().f_code.co_name,
            prt=self.is_status,
            ext=message)

    def check_latlon_lim(self):
        # if latlim[0] < -60 or latlim[1] > 70:
        #     print(
        #         'Latitude above 70N or below 60S is not possible. Value set to maximum')
        #     latlim[0] = np.max(latlim[0], -60)
        #     latlim[1] = np.min(latlim[1], 70)
        # if lonlim[0] < -180 or lonlim[1] > 180:
        #     print(
        #         'Longitude must be between 180E and 180W. Now value is set to maximum')
        #     lonlim[0] = np.max(lonlim[0], -180)
        #     lonlim[1] = np.min(lonlim[1], 180)
        pass

    def cal_latlon_index(self):
        # # Define IDs
        # yID = 3000 - np.int16(
        #     np.array([np.ceil((latlim[1] + 60) * 20), np.floor((latlim[0] + 60) * 20)]))
        # xID = np.int16(
        #     np.array([np.floor((lonlim[0]) * 20), np.ceil((lonlim[1]) * 20)]) + 3600)
        pass

    def check_time_lim(self):
        # # Check Startdate and Enddate
        # if not Startdate:
        #     if TimeStep == 'weekly':
        #         Startdate = pd.Timestamp('2003-01-01')
        #     if TimeStep == 'daily':
        #         Startdate = pd.Timestamp('2005-01-01')
        # if not Enddate:
        #     if TimeStep == 'weekly':
        #         Enddate = pd.Timestamp('2015-12-31')
        #     if TimeStep == 'daily':
        #         Enddate = pd.Timestamp('2016-12-31')
        #
        # # Make a panda timestamp of the date
        # try:
        #     Enddate = pd.Timestamp(Enddate)
        # except BaseException:
        #     Enddate = Enddate
        pass

    def cal_time_range(self):
        # if TimeStep == 'daily':
        #     # Define Dates
        #     Dates = pd.date_range(Startdate, Enddate, freq='D')
        #
        # if TimeStep == 'weekly':
        #     # Define the Startdate of ALEXI
        #     DOY = datetime.datetime.strptime(Startdate,
        #                                      '%Y-%m-%d').timetuple().tm_yday
        #     Year = datetime.datetime.strptime(Startdate,
        #                                       '%Y-%m-%d').timetuple().tm_year
        #
        #     # Change the startdate so it includes an ALEXI date
        #     DOYstart = int(math.ceil(DOY / 7.0) * 7 + 1)
        #     DOYstart = str('%s-%s' % (DOYstart, Year))
        #     Day = datetime.datetime.strptime(DOYstart, '%j-%Y')
        #     Month = '%02d' % Day.month
        #     Day = '%02d' % Day.day
        #     Date = (str(Year) + '-' + str(Month) + '-' + str(Day))
        #     DOY = datetime.datetime.strptime(Date,
        #                                      '%Y-%m-%d').timetuple().tm_yday
        #     # The new Startdate
        #     Date = pd.Timestamp(Date)
        #
        #     # amount of Dates weekly
        #     Dates = pd.date_range(Date, Enddate, freq='7D')
        pass

    def check_product(self, product=''):
        if product == '':
            pass
        elif product == 'ALEXI':
            pass
        elif product == 'ASCAT':
            pass
        elif product == 'CFSR':
            pass
        else:
            raise ValueError('Unknown method: {v}'.format(v=method))
        pass

    def check_method(self, method=''):
        if method == '':
            pass
        elif method == 'ftp':
            pass
        elif method == 'request':
            pass
        elif method == 'curl':
            pass
        else:
            raise ValueError('Unknown method: {v}'.format(v=method))
        pass

    def check_version(self, version=''):
        if version == '':
            pass
        elif version == 'v1':
            pass
        elif version == 'v2':
            pass
        elif version == 'v3':
            pass
        else:
            raise ValueError('Unknown version: {v}'.format(v=version))
        pass

    def create_folder(self):
        # # Define directory and create it if not exists
        # output_folder = os.path.join(Dir, 'Evaporation', 'ALEXI', 'Weekly')
        # if not os.path.exists(output_folder):
        #     os.makedirs(output_folder)

        # output_folder = os.path.join(Dir, 'Evaporation', 'ALEXI', 'Daily')
        # if not os.path.exists(output_folder):
        #     os.makedirs(output_folder)
        pass

    def clean_folder(self):
        # os.chdir(output_folder)
        # re = glob.glob("*.dat")
        # for f in re:
        #     os.remove(os.path.join(output_folder, f))
        pass

    def unzip_gz(self, file, outfile):
        """Extract zip file

        This function extract zip file as gz file.

        Args:
          file (str): Name of the file that must be unzipped.
          outfile (str): Directory where the unzipped data must be stored.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.download import Download
        """

        with gzip.GzipFile(file, 'rb') as zf:
            file_content = zf.read()
            save_file_content = open(outfile, 'wb')
            save_file_content.write(file_content)
        save_file_content.close()
        zf.close()
        os.remove(file)


def main():
    from pprint import pprint

    # @classmethod

    # Download __init__
    print('\nDownload\n=====')
    download = Download('', 'FTP_WA', is_status=False)
    # 'Copernicus', is_status=False)

    # # Base attributes
    # print('\ndownload._Base__conf\n=====')
    # pprint(download._Base__conf)
    #
    # # Accounts attributes
    # print('\ndownload._Accounts__conf\n=====')
    # pprint(download._Accounts__conf)
    #
    # # GIS attributes
    # print('\ndownload._GIS__conf:\n=====')
    # pprint(download._GIS__conf)
    #
    # # Download attributes
    #
    # # Download methods
    # print('\ndownload.Base.get_status()\n=====')
    # pprint(download.get_status())

    print('\n\n=====')
    for key, val in download._Base__conf['data']['products'].items():
        print(key)
        print('-----')
        pprint(val['meta'])
        pprint(val['data'])


if __name__ == "__main__":
    main()
