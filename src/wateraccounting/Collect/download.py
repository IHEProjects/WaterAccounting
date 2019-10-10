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
import gzip


class Download:
    """This Download class

    Description
    """
    __path = ''

    def __init__(self, workspace=''):
        if workspace != '':
            self.__path = workspace
        else:
            self.__path = os.path.dirname(__file__)

    def Extract_Data_gz(file, outfile):
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

