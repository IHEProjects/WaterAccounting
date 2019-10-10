# -*- coding: utf-8 -*-
"""
**Collect**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team.

`Description`

Before use this module, set account information
in the ``WaterAccounting/config.yml`` file.

**Examples:**
::

    >>> import os
    >>> from wateraccounting.Collect.collect import Collect
    >>> collect = Collect(os.getcwd(), 'FTP_WA_GUESS')
    S: WA "function" status 0: No error
       "config.yml-encrypted" key is: ...

.. note::

    1. Create ``config.yml`` under root folder of the project,
       based on the ``config-example.yml``.
    #. Run ``Collect.credential.encrypt_cfg(path, file, password)``
       to generate ``config.yml-encrypted`` file.
    #. Save key to ``credential.yml``.
"""
import os
import sys
import inspect
# import shutil
import yaml

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# PyCharm
# if __name__ == "__main__":
#
# >>> from . import collect
# ImportError: cannot import name 'collect' from '__main__'
#
# >>> from Collect import collect
# ModuleNotFoundError
#
# PyCharm->Project Structure->"Sources": WaterAccounting\""
# from src.wateraccounting.Collect import collect
# OK
#
# PyCharm->Project Structure->"Sources": WaterAccounting\"src\wateraccounting"
# >>> from Collect import collect
# OK

__location__ = os.path.join(
    os.getcwd(),
    os.path.dirname(
        inspect.getfile(
            inspect.currentframe())))


class Collect(object):
    """This Collect class

    Description

    Args:
      workspace (str): Directory to config.yml.
      account (str): Account name of data portal.
    """
    __template = {
        0: 'S: WA "{f}" status {c}: {m}',
        1: 'E: WA "{f}" status {c}: {m}',
        2: 'W: WA "{f}" status {c}: {m}',
    }
    __conf = {
        'path': __location__,
        'file': 'collect.yml',
        'status': '',
        'data': {
            'messages': {
                '0': {}
            },
            'source': {
                'ALEXI': {
                    'E': {
                        'name': 'Evaporation',
                        'type': 'tif',
                        'url': 'ftp://'
                    }
                },
                'ASCAT': {
                    'SWI': {
                        'name': 'Soil Water Index',
                        'type': 'nc',
                        'url': 'https://land.copernicus.vgt.vito.be/PDF/datapool'
                               '/Vegetation/Soil_Water/SWI_V3'
                               '/{year}/{month}/{day}/{name}/{fname}'
                    }
                },
            }
        }
    }
    __user = {
        'path': '',
        'file': 'config.yml-encrypted',
        'account': {},
        'data': {
            'credential': {
                'file': 'credential.yml',
                'password': 'W@t3r@ccounting',
                'length': 32,
                'iterations': 100000,
                'salt': 'WaterAccounting_',
                'key': ''
            },
            'accounts': {
                'NASA': {},
                'GLEAM': {},
                'FTP_WA': {},
                'FTP_WA_GUESS': {},
                'MSWEP': {},
                'Copernicus': {},
                'VITO': {}
            },
        }
    }

    stcode = 0
    status = 'Status.'

    def __init__(self, workspace='', account=''):
        """Class instantiation
        """
        is_continued = True

        if isinstance(workspace, str):
            if workspace != '':
                self.__user['path'] = workspace
            else:
                self.__user['path'] = os.path.join(
                    __location__, '../', '../', '../'
                )

            # os.path.join(
            #     os.path.dirname(os.path.realpath(__file__)),
            #     '..', '..', '..'
            # )

                print('"{k}" use default value: "{v}"'
                      .format(k='workspace',
                              v=self.__user['path']))
        else:
            raise TypeError('"{k}" requires string, received "{t}"'
                            .format(k='workspace',
                                    t=type(workspace)))

        if isinstance(account, str):
            if account != '':
                if account in self.__user['data']['accounts']:
                    self.__user['account'][account] = {}
                else:
                    raise KeyError('"{k}" not supported.'
                                   .format(k=account))
            else:
                self.__user['account']['FTP_WA_GUESS'] = {}

                print('"{k}" use default value: "{v}"'
                      .format(k='account',
                              v=self.__user['account']))
        else:
            raise TypeError('"{k}" requires string, received "{t}"'
                            .format(k='account',
                                    t=type(account)))

        if is_continued:
            self._conf()
            self._user()
            message = '"{f}" key is: "{v}"'.format(
                f=self.__user['file'],
                v=self.__user['data']['credential']['key'])

        self._status(sys._getframe().f_code.co_name, prt=True, ext=message)

    def _conf(self):
        """Get configuration

        This function open collect.cfg configuration file.

        Returns:
          str: Status message.
        """
        f_in = os.path.join(self.__conf['path'], self.__conf['file'])

        if os.path.exists(f_in):
            conf = yaml.load(
                open(self.__conf['file'], 'r'),
                Loader=yaml.FullLoader)

            for key in conf:
                # __conf.data[messages, ]
                try:
                    self.__conf['data'][key] = conf[key]
                    self.stcode = 0
                except KeyError:
                    raise KeyError('"{k}" not found in "{f}".'.format(k=key, f=f_in))
        else:
            raise FileNotFoundError('Collect "{f}" not found.'.format(f=f_in))
            sys.exit(1)

        self._status(sys._getframe().f_code.co_name)
        return self.__conf['status']

    def _user(self):
        """Get user information

        This is the main function to configure user's credentials.

        **Don't synchronize the details to github.**

        - File to read: ``config.yml-encrypted``
        - File to read: ``credential.yml``

        Returns:
          str: Status message.
        """
        f_in = os.path.join(self.__user['path'], self.__user['file'])

        if os.path.exists(f_in):
            self._user_key()
            # self._user_encrypt(f_in)

            conf = yaml.load(
                self._user_decrypt(f_in),
                Loader=yaml.FullLoader)

            for key in conf:
                # __user.data[accounts, ]
                try:
                    self.__user['data'][key] = conf[key]
                    self.stcode = 0
                except KeyError:
                    raise KeyError('Key "{k}" not found in "{f}".'
                                   .format(k=key, f=f_in))
                else:
                    # __user.account
                    for subkey in self.__user['account']:
                        try:
                            self.__user['account'][subkey] = conf[key][subkey]
                            self.stcode = 0
                        except KeyError:
                            raise KeyError('Sub key "{k}" not found in "{f}".'
                                           .format(k=subkey, f=f_in))
        else:
            raise FileNotFoundError('User "{f}" not found.'.format(f=f_in))
            sys.exit(1)

        self._status(sys._getframe().f_code.co_name)
        return self.__conf['status']

    def _status(self, fun, prt=False, ext=''):
        """Set status

        Args:
          fun (str): Function name.
          prt (bool): Is to print on screen?
          ext (str): Extra message.
        """
        cod = self.stcode
        msg = self.__conf['data']['messages'][cod]['msg']
        lvl = self.__conf['data']['messages'][cod]['level']
        if ext != '':
            self.status = self.__template[lvl].format(
                f=fun, c=cod, m='{m}\n   {e}'.format(m=msg, e=ext))
        else:
            self.status = self.__template[lvl].format(
                f=fun, c=cod, m='{m}'.format(m=msg))
        self.__conf['status'] = self.status

        if prt:
            print(self.status)

    def _user_key(self):
        """Getting a key

        This function fun.

        Returns:
          bytes: A URL-safe base64-encoded 32-byte key.
          This must be kept secret.
          Anyone with this key is able to create and read messages.
        """
        f_in = os.path.join(self.__user['path'],
                            self.__user['data']['credential']['file'])

        if os.path.exists(f_in):
            with open(f_in, 'rb') as fp_in:
                key = fp_in.read()
        else:
            raise FileNotFoundError('User "{f}" not found.'.format(f=f_in))
            sys.exit(1)

        self.__user['data']['credential']['key'] = key

        return key

    def _user_key_generator(self):
        """Getting a key

        This function fun.

        Returns:
          bytes: A URL-safe base64-encoded 32-byte key.
          This must be kept secret.
          Anyone with this key is able to create and read messages.
        """
        # from cryptography.fernet import Fernet
        # key = Fernet.generate_key()

        # Convert to type bytes
        pswd = self.__user['data']['credential']['password'].encode()
        salt = self.__user['data']['credential']['salt'].encode()
        length = self.__user['data']['credential']['length']
        iterations = self.__user['data']['credential']['iterations']

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=salt,
            length=length,
            iterations=iterations,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(pswd))

        return key

    def _user_encrypt(self, file):
        """Encrypt file with given key

        This function encrypt config.yml file.

        Args:
          file (str): File name.

        Returns:
          bytes: A URL-safe base64-encoded 32-byte key.
          This must be kept secret.
          Anyone with this key is able to create and read messages.
        """
        f_in = file
        f_out = '{f}-encrypted'.format(f=f_in)
        key = self.__user['data']['credential']['key']

        with open(f_in, 'rb') as fp_in:
            data = fp_in.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(f_out, 'wb') as fp_out:
            fp_out.write(encrypted)

        return key

    def _user_decrypt(self, file):
        """Decrypt file with given key

        This function decrypt config.yml file.

        Args:
          file (str): File name.

        Returns:
          str: Decrypted Yaml data by utf-8.
        """
        f_in = file
        key = self.__user['data']['credential']['key']

        with open(f_in, 'rb') as fp_in:
            data = fp_in.read()

        decrypted = Fernet(key).decrypt(data).decode('utf8')

        return decrypted

    @classmethod
    def get_conf(cls, key):
        """Get configuration

        This is the function to get project's configuration data.

        Args:
          key (str): Key name.

        Returns:
          dict: Configuration data.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.collect import Collect
            >>> collect = Collect(os.getcwd(), 'FTP_WA_GUESS')
            S: WA "__init__" status 0: No error
               "config.yml-encrypted" key is: ...

            >>> status = collect.get_conf('status')
            >>> print(status)
            S: WA "get_conf" status 0: No error
        """
        if key in cls.__conf:
            cls.stcode = 0
        else:
            cls.stcode = 1
            raise KeyError('Key "{k}" not found in "{v}".'
                           .format(k=key, v=cls.__conf.keys()))

        cls._status(cls, sys._getframe().f_code.co_name)
        return cls.__conf[key]

    @classmethod
    def get_user(cls, key):
        """Get user information

        This is the function to get user's configuration data.

        **Don't synchronize the details to github.**

        - File to read: ``credential.yml``
          contains key: ``config.yml-encrypted``.
        - File to read: ``config.yml-encrypted``
          generated from: ``config.yml``.

        Args:
          key (str): Key name.

        Returns:
          dict: User data.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.collect import Collect
            >>> collect = Collect(os.getcwd(), 'FTP_WA_GUESS')
            S: WA "__init__" status 0: No error
               "config.yml-encrypted" key is: ...

            >>> account = collect.get_user('account')
            >>> account['FTP_WA_GUESS']
            {'username': 'wateraccountingguest', 'password': 'W@t3r@ccounting'}

            >>> accounts = collect.get_user('accounts')
            Traceback (most recent call last):
            ...
            KeyError:
        """
        if key in cls.__user:
            cls.stcode = 0
        else:
            cls.stcode = 1
            raise KeyError('Key "{k}" not found in "{v}".'
                           .format(k=key, v=cls.__user.keys()))

        cls._status(cls, sys._getframe().f_code.co_name)
        return cls.__user[key]

    @classmethod
    def get_status(cls):
        """Get status

        This is the function to get project status.

        Returns:
          str: Status.
        """
        return cls.status

    @staticmethod
    def wait_bar(i, total,
                 prefix='', suffix='',
                 decimals=1, length=100, fill='█'):
        """Wait Bar Console

        This function will print a waitbar in the console

        Args:
          i (int): Iteration number.
          total (int): Total iterations.
          prefix (str): Prefix name of bar.
          suffix (str): Suffix name of bar.
          decimals (int): Decimal of the wait bar.
          length (int): Width of the wait bar.
          fill (str): Bar fill.
        """
        # Adjust when it is a linux computer
        if os.name == 'posix' and total == 0:
            total = 0.0001

        percent = ('{0:.' + str(decimals) + 'f}').format(100 * (i / float(total)))
        filled = int(length * i // total)
        bar = fill * filled + '-' * (length - filled)

        sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        sys.stdout.flush()

        if i == total:
            print()


def main():
    from pprint import pprint

    print('\n__location__\n=====')
    print(__location__)
    print('0.1', inspect.currentframe())
    print('0.2', inspect.getfile(inspect.currentframe()))
    print('1. getcwd:', os.getcwd())
    print('2. dirname: ', os.path.dirname(inspect.getfile(inspect.currentframe())))

    print('\n__file__\n=====')
    print(__file__)

    print('\nsys.path\n=====')
    pprint(sys.path)

    print('\nCollect\n=====')
    collect = Collect('',
                      # '')
                      # 'test')
                      'FTP_WA')
                      # 'Copernicus')

    print('\ncollect._Collect__conf\n=====')
    pprint(collect._Collect__conf)
    print('\ncollect._Collect__user\n=====')
    pprint(collect._Collect__user)


if __name__ == "__main__":
    main()
