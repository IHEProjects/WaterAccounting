# -*- coding: utf-8 -*-
"""
"""


import os
import sys
import yaml


def _list():
    """List.

    :return: suppored portals
    :rtype: list
    """
    return ['NASA', 'GLEAM', 'FTP_WA', 'MSWEP', 'Copernicus', 'VITO']


def Accounts(File='', Type=None):
    """Save user account and password.

    This is the main function to configure user's credentials.
    Don't synchronize the details to github.

    :param File: configuration yaml file
    :type File: string
    :param Type: portal name
    :type Type: string
    :return: {'username': '', 'password': ''}
    :rtype: dict

    :Example:

        >>> from wateraccounting.Collect.WebAccounts import Accounts
        >>> Accounts(File='config.yml', Type='test')
        Traceback (most recent call last):
            ...
        KeyError: 'test'

        >>> Accounts(File='config.yml', Type='FTP_WA')
        {'username': 'wateraccountingguest', 'password': 'W@t3r@ccounting'}
    """
    if os.path.exists(File):
        list = _list()
        user = {'username': '', 'password': ''}

        with open(File, 'r') as fp_cfg:
            try:
                cfg = yaml.load(fp_cfg, Loader=yaml.FullLoader)
                user = cfg['account'][Type]

                return user
            except KeyError as err:
                raise KeyError("{err} is not supported.".format(err=err))
    elif IOError:
        print("Can't find {file}".format(file=File))
        sys.exit()
