# -*- coding: utf-8 -*-
"""
**Base**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the ALEXI developers.

`Description`

Before use this module, set account information in the `Collect/config.yml` file.

**Examples:**
::

    from wateraccounting.Collect import collect

.. note::

    Create `config.yml` under root folder of the project,
    based on the `config-example.yml`.

    Run `Collect.credential.encrypt_cfg(path, file, password)`
    to generate `config.yml-encrypted` file.
"""
import os
import sys
import yaml

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Base:
    """This Base class

    Description
    """
    __conf = {
        'path': os.path.dirname(os.path.realpath(__file__)),
        'file': 'collect.yml',
        'conf': {
            'message': {},
        }
    }
    __user = {
        'path': '',
        'file': 'config.yml-encrypted',
        'password': 'WaterAccounting',
        'salt': b'WaterAccounting_',
        'key': '',
        'account': 'FTP_WA_GUESS',
        'conf': {
            'account': {
                'NASA': {
                    'username': '',
                    'password': '',
                },
                'GLEAM': {
                    'username': '',
                    'password': '',
                },
                'FTP_WA': {
                    'username': '',
                    'password': '',
                },
                'FTP_WA_GUESS': {
                    'username': '',
                    'password': ''
                },
                'MSWEP': {
                    'username': '',
                    'password': '',
                },
                'Copernicus': {
                    'username': '',
                    'password': '',
                },
                'VITO': {
                    'username': '',
                    'password': '',
                }
            },
        }
    }

    def __init__(self,
                 workspace='',
                 configfile='',
                 password='',
                 account=''):
        """Class instantiation

        Args:
          workspace (str): Directory to config.yml.
          configfile (str): File name of config.yml.
          password (str): Default value is "WaterAccounting".
          account (str): Account name of data portal.
        """
        if workspace != '':
            self.__user['path'] = workspace
        else:
            self.__user['path'] = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '..', '..', '..',
            )

        if account != '':
            self.__user['account'] = account

        if configfile != '':
            self.__user['file'] = configfile

        if password != '':
            self.__user['password'] = password

        self.get_conf()
        self.get_user()

    def get_conf(self):
        """Get configuration

        This function open collect.cfg configuration file.

        Returns:
          dict: Collect configuration data.

        :Example:

            >>> from wateraccounting.Collect.base import Base
            >>> base = Base()
            >>> len(base.get_conf())
            2
        """
        file = os.path.join(self.__conf['path'], self.__conf['file'])

        if os.path.exists(file):
            conf = yaml.load(
                open(self.__conf['file'], 'r'),
                Loader=yaml.FullLoader)

            for key in self.__conf['conf']:
                try:
                    self.__conf['conf'][key] = conf[key]
                except KeyError:
                    raise KeyError("{k} not found in {f}.".format(
                        k=key, f=file))
        elif FileNotFoundError:
            raise FileNotFoundError("Collect {file} not found.".format(file=file))
            sys.exit(1)

        return self.__conf['conf']

    def get_user(self):
        """Get user information

        This is the main function to configure user's credentials.
        Don't synchronize the details to github.

        ``config.yml-encrypted``.


        Args:
          portal (str): Portal name.

        Returns:
          dict: User configuration data.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.base import Base
            >>> base = Base(os.getcwd())
            >>> user = base.get_user('')
            Traceback (most recent call last):
                ...
            KeyError:

            >>> user = base.get_user('test')
            Traceback (most recent call last):
                ...
            KeyError:

            >>> user = base.get_user('FTP_WA_GUESS')
            >>> user
            {'username': 'wateraccountingguest', 'password': 'W@t3r@ccounting'}
        """
        file = os.path.join(self.__user['path'], self.__user['file'])

        if os.path.exists(file):
            self.__user['key'] = self._user_key()

            conf = yaml.load(
                self._user_decrypt(),
                Loader=yaml.FullLoader)

            for key in self.__user['conf']:
                try:
                    self.__user['conf'][key] = conf[key]
                except KeyError:
                    raise KeyError("{k} not found in {f}.".format(
                        k=key, f=file))
        elif FileNotFoundError:
            raise FileNotFoundError("User {file} not found.".format(file=file))
            sys.exit(1)

        return self.__user['conf']

    def _user_key(self):
        """Getting a key

        This function fun.

        Returns:
          bytes: A URL-safe base64-encoded 32-byte key.
          This must be kept secret.
          Anyone with this key is able to create and read messages.

        :Example:

            >>> from wateraccounting.Collect.credential import Credential
            >>> password = 'WaterAccounting'
            >>> auth = Credential(password)
            >>> key = auth.get_key()
            >>> key.decode('utf8')
            '3aQ3mbD6IV7SHJlQKgkQm4V92jEBuizVFxh-oFm79XQ='
        """
        # from cryptography.fernet import Fernet
        # key = Fernet.generate_key()

        pwd = self.__user['password'].encode()  # Convert to type bytes
        slt = self.__user['salt']
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=slt,
            iterations=100000,
            backend=default_backend()
        )
        self.__user['key'] = base64.urlsafe_b64encode(kdf.derive(pwd))

        return self.__user['key']

    def _user_encrypt(self):
        """Getting a key

        This function encrypt config.yml file.

        Returns:
          bytes: A URL-safe base64-encoded 32-byte key.
          This must be kept secret.
          Anyone with this key is able to create and read messages.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.credential import encrypt_cfg
            >>> path = os.path.join(os.getcwd(), 'tests', 'data')
            >>> file = 'config-test.yml'
            >>> password = 'WaterAccounting'
            >>> key = encrypt_cfg(path, file, password)
            >>> key.decode('utf8')
            '3aQ3mbD6IV7SHJlQKgkQm4V92jEBuizVFxh-oFm79XQ='
        """
        file_in = os.path.join(path, file)
        file_out = '{fn}-encrypted'.format(fn=file_in)
        key = get_key(password)

        with open(file_in, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(file_out, 'wb') as f:
            f.write(encrypted)

        return key

    def _user_decrypt(self):
        """Getting a key

        This function decrypt config.yml file.

        Returns:
          str: Decrypted Yaml data.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.credential import decrypt_cfg
            >>> path = os.path.join(os.getcwd(), 'tests', 'data')
            >>> file = 'config-test.yml-encrypted'
            >>> password = 'WaterAccounting'
            >>> config = decrypt_cfg(path, file, password)
            >>> type(config)
            <class 'str'>
        """
        file_in = os.path.join(path, file)
        key = get_key(password)

        with open(file_in, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(data).decode('utf8')

        return decrypted

    def wait_bar(i, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
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
        if os.name == "posix" and total == 0:
            total = 0.0001

        percent = ("{0:." + str(decimals) + "f}").format(100 * (i / float(total)))
        filled = int(length * i // total)
        bar = fill * filled + '-' * (length - filled)

        sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        sys.stdout.flush()

        if i == total:
            print()


def main():
    from pprint import pprint
    path = os.getcwd()
    base = Base('', 'config.yml-encrypted', 'pwd', 'FTP_WA_GUESS')
    pprint(base._Base__conf)
    pprint(base._Base__user)


if __name__ == "__main__":
    main()
