# -*- coding: utf-8 -*-
"""
"""


import pytest
from wateraccounting.Collect.WebAccounts import Accounts

__author__ = "Quan Pan"
__copyright__ = "Quan Pan"
__license__ = "apache"


def test_Accounts():
    assert Accounts('config.yml', 'FTP_WA') == \
           {'username': 'wateraccountingguest',
            'password': 'W@t3r@ccounting'}
    with pytest.raises(KeyError, match=r".* not .*"):
        Accounts('config.yml', 'test')
