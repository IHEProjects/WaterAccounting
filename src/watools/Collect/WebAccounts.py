# -*- coding: utf-8 -*-
"""
Save user account and password

+------------+------------------------------------------+
| Portal     | Link                                     |
+============+==========================================+
| Copernicus | https://land.copernicus.vgt.vito.be/PDF/ |
+------------+------------------------------------------+
| VITO       | https://www.vito-eodata.be/PDF/datapool/ |
+------------+------------------------------------------+
"""


def Accounts(Type=None):
    """Save user account and password.

    .. note::

        This is the main function to configure user's credentials.
        Don't synchronize the details to github.

    :param Type: portal name
    :type Type: string
    :return: selected portal [username, password]
    :rtype: array

    :Example:

        >>> from watools.Collect.WebAccounts import Accounts
        >>> Accounts(Type='NASA')
        ['username', 'password']
    """
    User_Pass = {
        'NASA': ['username', 'password'],
        'GLEAM': ['', ''],
        'FTP_WA': ['', ''],
        'MSWEP': ['', ''],
        'Copernicus': ['', ''],
        'VITO': ['', '']}

    Selected_Path = User_Pass[Type]

    return (Selected_Path)
