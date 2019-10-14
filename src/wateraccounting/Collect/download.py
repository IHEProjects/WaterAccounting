# -*- coding: utf-8 -*-
"""
**Download**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team.

`Description`

Before use this module, set account information
in the ``WaterAccounting/config.yml`` file.

**Examples:**
::

    >>> import os
    >>> from wateraccounting.Collect.download import Download
    >>> download = Download(os.getcwd(), 'FTP_WA_GUESS', is_status=True)
    S: WA.Download "function" status 0: No error
       "config.yml-encrypted" key is: ...

"""
import os
import sys
import inspect
# import shutil
import yaml

import gzip

try:
    from .collect import Collect
except ImportError:
    from src.wateraccounting.Collect.collect import Collect

try:
    from .gis import GIS
except ImportError:
    from src.wateraccounting.Collect.gis import GIS


class Download(Collect, GIS):
    """This Download class

    Description

    Args:
      workspace (str): Directory to config.yml.
      account (str): Account name of data portal.
      is_status (bool): Is to print status message.
      kwargs (dict): Other arguments.
    """
    __conf = {
        'path': '',
        'file': 'download.yml',
        'download': '',
        'data': {}
    }

    def __init__(self, workspace='', account='', is_status=True, **kwargs):
        """Class instantiation
        """
        Collect.__init__(self, workspace, account, is_status, **kwargs)
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

    def get_gz(self, file, outfile):
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
    download = Download('',
                        'FTP_WA', is_status=False)
                        # 'Copernicus', is_status=False)

    # Base attributes
    print('\ndownload._Base__conf\n=====')
    pprint(download._Base__conf)

    # Collect attributes
    print('\ndownload._Collect__conf\n=====')
    pprint(download._Collect__conf)

    # GIS attributes
    print('\ndownload._GIS__conf:\n=====')
    pprint(download._GIS__conf)

    # Download attributes

    # Download methods
    print('\ndownload.Base.get_status()\n=====')
    pprint(download.get_status())


if __name__ == "__main__":
    main()
