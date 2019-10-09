# -*- coding: utf-8 -*-
"""
**Collect**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team.

`Description`

Before use this module, set account information in the `WaterAccounting/config.yml` file.

**Examples:**
::

    >>> import os
    >>> from wateraccounting.Collect.collect import Collect
    >>> collect = Collect(os.getcwd(), 'FTP_WA_GUESS')
    "config.yml-encrypted" key is: ...

.. note::

    Create `config.yml` under root folder of the project,
    based on the `config-example.yml`.

    Run `Collect.credential.encrypt_cfg(path, file, password)`
    to generate `config.yml-encrypted` file.
"""
import os
import sys
import yaml

from cryptography.fernet import Fernet


class Collect(object):
    """This Collect class

    Description

    Args:
      workspace (str): Directory to config.yml.
      account (str): Account name of data portal.
    """
    __conf = {
        'path': os.path.dirname(os.path.realpath(__file__)),
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
        'status': {},
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
    sttemp = 'WA "{f}" status {c}: {m}.'

    def __init__(self,
                 workspace='',
                 account=''):
        """Class instantiation
        """
        is_continued = True

        if isinstance(workspace, str):
            if workspace != '':
                self.__user['path'] = workspace
            else:
                self.__user['path'] = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    '..', '..', '..',
                )

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
            self.get_conf()
            self.get_user()
            print('"{f}" key is: "{v}"'
                  .format(f=self.__user['file'],
                          v=self.__user['data']['credential']['key']))

    def get_conf(self):
        """Get configuration

        This function open collect.cfg configuration file.

        Returns:
          str: Status message.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.collect import Collect
            >>> collect = Collect(os.getcwd(), 'FTP_WA_GUESS')
            "config.yml-encrypted" key is: ...
            >>> conf = collect.get_conf()
            >>> print(conf)
            WA "get_conf" status 0: No error.
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
                except KeyError:
                    raise KeyError('"{k}" not found in "{f}".'.format(k=key, f=f_in))
        else:
            raise FileNotFoundError('Collect "{f}" not found.'.format(f=f_in))
            sys.exit(1)

        self.stcode = 0
        self.__conf['status'] = self.sttemp.format(
            f=sys._getframe().f_code.co_name,
            c=self.stcode,
            m=self.__conf['data']['messages'][self.stcode]['msg'])
        return self.__conf['status']

    def get_user(self):
        """Get user information

        This is the main function to configure user's credentials.

        **Don't synchronize the details to github.**

        - File to read: ``config.yml-encrypted``
        - File is from: ``config.yml``

        Returns:
          str: Status message.

        :Example:

            >>> import os
            >>> from wateraccounting.Collect.collect import Collect
            >>> collect = Collect(os.getcwd(), 'FTP_WA_GUESS')
            "config.yml-encrypted" key is: ...
            >>> user = collect.get_user()
            >>> print(user)
            WA "get_user" status 0: No error.
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
                except KeyError:
                    raise KeyError('Key "{k}" not found in "{f}".'
                                   .format(k=key, f=f_in))
                else:
                    # __user.account
                    for subkey in self.__user['account']:
                        try:
                            self.__user['account'][subkey] = conf[key][subkey]
                        except KeyError:
                            raise KeyError('Sub key "{k}" not found in "{f}".'
                                           .format(k=subkey, f=f_in))
        else:
            raise FileNotFoundError('User "{f}" not found.'.format(f=f_in))
            sys.exit(1)

        # self.__user['status'] = self.__user['data']['messages']['0']
        self.stcode = 0
        self.__user['status'] = self.sttemp.format(
            f=sys._getframe().f_code.co_name,
            c=self.stcode,
            m=self.__conf['data']['messages'][self.stcode]['msg'])
        return self.__user['status']

    def _user_key(self):
        """Getting a key

        This function fun.

        Returns:
          bytes: A URL-safe base64-encoded 32-byte key.
          This must be kept secret.
          Anyone with this key is able to create and read messages.

        **Examples:**
        ::

            import base64
            from cryptography.fernet import Fernet
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            # Convert to type bytes
            pswd = b'password'
            salt = b'salt'
            length = 32
            iterations = 100000

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                salt=salt,
                length=length,
                iterations=iterations,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(pswd))
        """
        # from cryptography.fernet import Fernet
        # key = Fernet.generate_key()

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

    def _user_encrypt(self, file):
        """Getting a key

        This function encrypt config.yml file.

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
        """Getting a key

        This function decrypt config.yml file.

        Returns:
          str: Decrypted Yaml data.
        """
        f_in = file
        key = self.__user['data']['credential']['key']

        with open(f_in, 'rb') as fp_in:
            data = fp_in.read()

        decrypted = Fernet(key).decrypt(data).decode('utf8')

        return decrypted

    def wait_bar(self, i, total,
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
    # path = os.getcwd()

    collect = Collect('',
                      '')
                      # 'test')
                      # 'FTP_WA')
                      #  'Copernicus')

    pprint(collect._Collect__conf)
    pprint(collect._Collect__user)


if __name__ == "__main__":
    main()
