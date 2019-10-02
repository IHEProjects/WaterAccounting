# -*- coding: utf-8 -*-
"""
**Credential**

`Restrictions`

The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the ALEXI developers.

`Description`

des

**Examples:**
::

    from wateraccounting.Collect import credential

.. seealso::

    cryptography example:
    `<https://nitratine.net/blog/post/encryption-and-decryption-in-python/>`_
"""
import os
# import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Global Variables
# this = sys.modules[__name__]


def get_key(password='WaterAccounting'):
    """Getting a key

    This function fun.

    Args:
      password (str): Default value is "WaterAccounting".

    Returns:
      bytes: A URL-safe base64-encoded 32-byte key.
      This must be kept secret.
      Anyone with this key is able to create and read messages.

    :Example:

        >>> from wateraccounting.Collect.credential import get_key
        >>> password = 'WaterAccounting'
        >>> key = get_key(password)
        >>> key.decode('utf8')
        '3aQ3mbD6IV7SHJlQKgkQm4V92jEBuizVFxh-oFm79XQ='
    """
    # from cryptography.fernet import Fernet
    # key = Fernet.generate_key()

    pwd = password.encode()  # Convert to type bytes
    slt = b'WaterAccounting_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=slt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd))

    return key


def encrypt_cfg(path='', file='config.yml', password='WaterAccounting'):
    """Getting a key

    This function encrypt config.yml file.

    Args:
      path (str): Directory to config.yml.
      file (str): File name of config.yml.
      password (str): Default value is "WaterAccounting".

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


def decrypt_cfg(path='', file='config.yml-encrypted', password='WaterAccounting'):
    """Getting a key

    This function decrypt config.yml file.

    Args:
      path (str): Directory to config.yml-encrypted.
      file (str): File name of config.yml-encrypted.
      password (str): Default value is "WaterAccounting".

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
