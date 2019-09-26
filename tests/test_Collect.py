# -*- coding: utf-8 -*-
"""
"""


import pytest
import wateraccounting.Collect.WebAccounts as WebAccounts
import wateraccounting.Collect.ALEXI as ALEXI

__author__ = "Quan Pan"
__copyright__ = "Quan Pan"
__license__ = "apache"


def test_WebAccounts():
    assert WebAccounts.Accounts('config.yml', 'FTP_WA') == \
           {'username': 'wateraccountingguest',
            'password': 'W@t3r@ccounting'}
    with pytest.raises(KeyError, match=r".* not .*"):
        WebAccounts.Accounts('config.yml', 'test')
