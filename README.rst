.. -*- mode: rst -*-

|CoverAlls|_ |Travis|_ |ReadTheDocs|_ |DockerHub|_ |PyPI|_

.. |CoverAlls| image:: https://coveralls.io/repos/github/IHEProjects/WaterAccounting/badge.svg?branch=master
.. _CoverAlls: https://coveralls.io/github/IHEProjects/WaterAccounting?branch=master

.. |Travis| image:: https://travis-ci.org/IHEProjects/WaterAccounting.svg?branch=master
.. _Travis: https://travis-ci.org/IHEProjects/WaterAccounting

.. |ReadTheDocs| image:: https://readthedocs.org/projects/wateraccounting/badge/?version=latest
.. _ReadTheDocs: https://wateraccounting.readthedocs.io/en/latest/

.. |DockerHub| image:: https://img.shields.io/docker/cloud/build/quanpan302/ihe_projects_wateraccounting
.. _DockerHub: https://hub.docker.com/r/quanpan302/ihe_projects_wateraccounting

.. |PyPI| image:: https://img.shields.io/pypi/v/WaterAccounting
.. _PyPI: https://pypi.org/project/WaterAccounting/


WaterAccounting
===============

Water Accounting Tools

Temporary **watools** project, for development only.

Collect
-------

+------------+------------------------------------------+
| Products   | Link                                     |
+============+==========================================+
| NASA       | https://www.nasa.gov                     |
+------------+------------------------------------------+
| GLEAM      | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| FTP_WA     | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| MSWEP      | https://www.wateraccounting.org/         |
+------------+------------------------------------------+
| Copernicus | https://land.copernicus.vgt.vito.be/     |
+------------+------------------------------------------+
| VITO       | https://www.vito-eodata.be/PDF/datapool/ |
+------------+------------------------------------------+

Data type
---------

+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| C              | Python  | Numpy         | NetCDF    | Decsription      | Bits | Min                  | Max                  |
+================+=========+===============+===========+==================+======+======================+======================+
| signed char    |         | np.byte       | NC_BYTE   | Byte             | 8    | -128                 | 127                  |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| unsigned char  |         | np.ubyte      | NC_UBYTE  | Unsigned byte    | 8    | 0                    | 255                  |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| int8_t         |         | np.int8       | NC_UBYTE  | Byte             | 8    | -128                 | 127                  |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| int16_t        |         | np.int16      | NC_SHORT  | Integer          | 16   | -32768               | 32767                |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| int32_t        |         | np.int32      | NC_INT    | Integer          | 32   | -2147483648          | 2147483647           |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| int64_t        |         | np.int64      | NC_INT64  | Integer          | 64   | -9223372036854775808 | 9223372036854775807  |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| uint8_t        |         | np.uint8      | NC_UBYTE  | Unsigned integer | 8    | 0                    | 255                  |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| uint16_t       |         | np.uint16     | NC_USHORT | Unsigned integer | 16   | 0                    | 65535                |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| uint32_t       |         | np.uint32     | NC_UINT   | Unsigned integer | 32   | 0                    | 4294967295           |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| uint64_t       |         | np.uint64     | NC_UINT64 | Unsigned integer | 64   | 0                    | 18446744073709551615 |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| float          |         | np.float32    | NC_FLOAT  | Float            | 32   | 1.17549e-38          | 3.40282e+38          |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| double         | float   | np.float64    | NC_DOUBLE | Double           | 64   | 2.22507e-308         | 1.79769e+308         |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| double         | float   | np.float\_    |           |                  |      |                      |                      |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| float complex  |         | np.complex64  |           |                  |      |                      |                      |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
| double complex | complex | np.complex128 |           |                  |      |                      |                      |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+
|                | complex | np.complex\_  |           |                  |      |                      |                      |
+----------------+---------+---------------+-----------+------------------+------+----------------------+----------------------+


Note
====

This project has been set up using PyScaffold 3.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
