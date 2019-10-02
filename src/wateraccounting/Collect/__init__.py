# -*- coding: utf-8 -*-
"""
Get user account and password, from your ``config.yml`` file.

+------------+------------------------------------------+
| Portal     | Link                                     |
+============+==========================================+
| NASA       | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| GLEAM      | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| FTP_WA     | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| MSWEP      | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| Copernicus | https://land.copernicus.vgt.vito.be/PDF/ |
+------------+------------------------------------------+
| VITO       | https://www.vito-eodata.be/PDF/datapool/ |
+------------+------------------------------------------+

.. todo::

    20190931, QPan, Collect module

    1. Create `config.yml` contains
        a. Portal name
        b. Portal url
        c. Portal data name, directory
        d. Portal data range, resolution
        e. Portal data file name template on ftp
        f. Portal data file name template on local
    2. cryptography `config.yml` file
    3. Add exception to check data meta information
    4. Estimate data size and tiff location to decided download or not
    5. Add unit test, and test datasets under "tests/data"
    6. read `__version__` from setup.py (git tag)
"""
__version__ = '0.0.1'
