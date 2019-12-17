import json
import os
import shutil
import sys
from unittest.mock import patch

import pytest

from main.config.config import PUBLIC_CONFIG
from main.model.config import SecretsModel
from main.util.get_env.django_settings_env import get_debug_from_env, in_pytest
from main.util.get_env.secrets_key import get_secrets_key_from_env
from main.util.get_env.secrets_model import get_secrets_model_from_env
from test.test_config import TEST_CONFIG_FILES_BASE_DIR

TEMP_OUTPUT_FILE = os.path.join(TEST_CONFIG_FILES_BASE_DIR, 'temp_local.json')

TEST_JSON = [
    {
        'name': 'temp_local.json',
        'data': {
            "DJANGO_SECRET_KEY": "testing_import",
            "DJANGO_DB_NAME": "testing_import",
            "DJANGO_DB_USERNAME": "testing_import",
            "DJANGO_DB_PASSWORD": "testing_import",
            "DJANGO_DB_HOST": "testing_import",
            "DJANGO_DB_PORT": "testing_import",
            "MONGODB_DB_USERNAME": "testing_import",
            "MONGODB_DB_PASSWORD": "testing_import",
            "MONGODB_DB_CONNECTION_STR": "testing_import",
            "TD_AMERITRADE_USERNAME": "testing_import",
            "TD_AMERITRADE_PASSWORD": "testing_import",
            "TD_AMERITRADE_CLIENT_ID": "testing_import"
        }
    }
]


@pytest.fixture(scope='module')
def temp_local_config():
    try:
        os.makedirs(TEST_CONFIG_FILES_BASE_DIR)
    except FileExistsError:
        pass

    for json_obj in TEST_JSON:
        FILE_PATH = os.path.join(TEST_CONFIG_FILES_BASE_DIR, json_obj['name'])
        with open(FILE_PATH, 'w') as f:
            json.dump(json_obj['data'], f)

    yield temp_local_config
    shutil.rmtree(TEST_CONFIG_FILES_BASE_DIR)


@pytest.fixture(scope='function')
def setup():
    if 'SECRETS_KEY' in os.environ:
        del os.environ['SECRETS_KEY']
    if 'DEBUG' in os.environ:
        del os.environ['DEBUG']
    pytest_sys_module = None
    if in_pytest():
        pytest_sys_module = os.environ.get('pytest')

    yield setup

    if not in_pytest():
        sys.modules.update({'pytest': pytest_sys_module})
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


def test_in_pytest(setup):
    assert in_pytest()


def test_get_screts_model_from_env(setup, temp_local_config):
    assert get_secrets_model_from_env() is None

    del sys.modules['pytest']

    # try native import if it is under pytest
    secrets_model = get_secrets_model_from_env()

    assert isinstance(secrets_model, SecretsModel)
    assert not secrets_model._imported
    assert not secrets_model._read_only
    assert secrets_model._encrypted
    assert secrets_model._secrets_path == os.path.join(PUBLIC_CONFIG.BASE_DIR, PUBLIC_CONFIG.SECRETS_DIR)

    # not exactly TRUE in DEBUG
    os.environ['DEBUG'] = 'TRUEE'
    secrets_model = get_secrets_model_from_env()

    assert isinstance(secrets_model, SecretsModel)
    assert not secrets_model._imported
    assert not secrets_model._read_only
    assert secrets_model._encrypted
    assert secrets_model._secrets_path == os.path.join(PUBLIC_CONFIG.BASE_DIR, PUBLIC_CONFIG.SECRETS_DIR)

    # exactly FALSE in DEBUG
    os.environ['DEBUG'] = 'FALSE'
    secrets_model = get_secrets_model_from_env()

    assert isinstance(secrets_model, SecretsModel)
    assert not secrets_model._imported
    assert not secrets_model._read_only
    assert secrets_model._encrypted
    assert secrets_model._secrets_path == os.path.join(PUBLIC_CONFIG.BASE_DIR, PUBLIC_CONFIG.SECRETS_DIR)

    # exactly TRUE in DEBUG
    os.environ['DEBUG'] = 'TRUE'
    with patch.object(PUBLIC_CONFIG, 'DEBUG_SECRETS_DIR', TEMP_OUTPUT_FILE):
        secrets_model = get_secrets_model_from_env()

        assert isinstance(secrets_model, SecretsModel)
        assert not secrets_model._encrypted
        assert secrets_model._secrets_path == TEMP_OUTPUT_FILE
        assert secrets_model._read_only

        for cls_member in secrets_model._cls_members:
            assert secrets_model.get_config(cls_member) == 'testing_import'
