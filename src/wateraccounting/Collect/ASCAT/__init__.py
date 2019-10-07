# -*- coding: utf-8 -*-
"""
**ASCAT**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the ALEXI developers.

`Description`

This module downloads ASCAT data from
``https://land.copernicus.vgt.vito.be/PDF/datapool``.

Use the ASCAT.daily function to download
and create daily ASCAT images in Gtiff format.

The data is available between ``2007-01-01`` till ``present``.

The output file with the name ``2003.01.01`` contains
the **soil water** index.

**Examples:**
::

    from wateraccounting.Collect import ASCAT
    ASCAT.daily(Dir='C:/Temp/',
                Startdate='2003-12-01', Enddate='2004-01-20',
                latlim=[-10, 30], lonlim=[-20, -10])
"""
# from .daily import main as daily
#
# __all__ = ['daily']
#
# __version__ = '0.1'