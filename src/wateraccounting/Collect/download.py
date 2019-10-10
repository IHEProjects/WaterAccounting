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
import gzip

try:
    # setup.py
    from . import collect
except ImportError:
    # PyCharm
    from src.wateraccounting.Collect import collect

__location__ = os.path.join(
    os.getcwd(),
    os.path.dirname(
        inspect.getfile(
            inspect.currentframe())))


class Download(collect.Collect):
    """This Download class

    Description

    Args:
      workspace (str): Directory to config.yml.
      account (str): Account name of data portal.
      is_status (bool): Is to print status message.
      kwargs (dict): Other arguments.
    """
    __path = 'Download'

    def __init__(self, workspace='', account='', is_status=True, **kwargs):
        """Class instantiation
        """
        # collect.Collect.__init__(self, workspace, account)
        super(Download, self).__init__(workspace, account,
                                       is_status=is_status, **kwargs)

    @classmethod
    def Extract_Data_gz(cls, file, outfile):
        """Extract zip file

        This function extract zip file as gz file.

        Args:
          file (str): Name of the file that must be unzipped.
          outfile (str): Directory where the unzipped data must be stored.

        :Example:

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

    print('\nDownload\n=====')
    download = Download()
                        # '', {'is_status': False)
    # download = Download('',
    #                     # '', 'is_status': False)
    #                     # 'test', is_status=False)
    #                     'FTP_WA', is_status=False)
    #                     # 'Copernicus', is_status=False)

    # print('\ndownload._Collect__conf\n=====')
    # pprint(download._Collect__conf)
    # print('\ndownload._Collect__user\n=====')
    # pprint(download._Collect__user)
    #
    # print('\ndownload._Download__path:\n=====')
    # pprint(download._Download__path)


if __name__ == "__main__":
    main()
