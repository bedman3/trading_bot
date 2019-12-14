import os

import pytest

from main.util.encrypt.config_crypter import ConfigCrypter
from test.test_config import PSEUDO_KEY_1, PSEUDO_KEY_2


@pytest.fixture(scope='function')
def setup():
    if 'SECRETS_KEY' in os.environ:
        del os.environ['SECRETS_KEY']
    yield setup
    if 'SECRETS_KEY' in os.environ:
        del os.environ['SECRETS_KEY']


def test_config_crypto_function(setup):
    key1 = PSEUDO_KEY_1
    key2 = PSEUDO_KEY_2

    testing_string = 'testing_str'

    cryp_obj = ConfigCrypter(keys=[key1, key2])

    first_encrypted_text = cryp_obj.encrypt_value(testing_string)

    assert isinstance(first_encrypted_text, str)
    assert testing_string == cryp_obj.decrypt_value(first_encrypted_text)

    # without inserting key, use the key in env
    SECRETS_KEY_ENV = f'{key1},{key2}'
    os.environ.update({'SECRETS_KEY': SECRETS_KEY_ENV})

    cryp_obj = ConfigCrypter()

    second_encrypted_text = cryp_obj.encrypt_value(testing_string)

    assert isinstance(second_encrypted_text, str)
    assert testing_string == cryp_obj.decrypt_value(second_encrypted_text)


def test_config_crypter_no_keys(setup):
    with pytest.raises(ValueError):
        ConfigCrypter()
