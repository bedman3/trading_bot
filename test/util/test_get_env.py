import os

import pytest
from main.util.get_env.django_settings_env import get_debug_from_env
from main.util.get_env.secrets_key import get_secrets_key_from_env


@pytest.fixture(scope='function')
def setup():
    if 'SECRETS_KEY' in os.environ:
        del os.environ['SECRETS_KEY']
    if 'DEBUG' in os.environ:
        del os.environ['DEBUG']
    yield setup
    if 'SECRETS_KEY' in os.environ:
        del os.environ['SECRETS_KEY']
    if 'DEBUG' in os.environ:
        del os.environ['DEBUG']


def test_get_debug_from_env(setup):
    assert not get_debug_from_env()

    os.environ['DEBUG'] = 'TRUE'

    assert get_debug_from_env()

    os.environ['DEBUG'] = 'FALSE'

    assert not get_debug_from_env()

    os.environ['DEBUG'] = 'TrUe'

    assert get_debug_from_env()

    os.environ['DEBUG'] = 'TRUEE'

    assert not get_debug_from_env()

    del os.environ['DEBUG']


def test_get_secrets_key_from_env(setup):
    assert get_secrets_key_from_env() is None

    os.environ['SECRETS_KEY'] = 'key1,key2'

    result = get_secrets_key_from_env()

    assert isinstance(result, list)
    assert result == ['key1', 'key2']

    del os.environ['SECRETS_KEY']
