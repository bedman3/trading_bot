import os
import shutil

import pytest
from main.model.config import SecretsModel
from rest_framework.utils import json
from test.test_config import TEST_CONFIG_FILES_BASE_DIR, PSEUDO_KEY_1, PSEUDO_KEY_2

# init pseudo keys else exception will raise in SecretsModel
pseudo_keys = [PSEUDO_KEY_1, PSEUDO_KEY_2]

TEST_JSON = [
    {
        'name': 'test_import_secrets_unencrypted_extra_keys.json',
        'data': {
            "DJANGO_SECRET_KEY": "<INPUT_HERE>",
            "DJANGO_DB_NAME": "<INPUT_HERE>",
            "DJANGO_DB_USERNAME": "<INPUT_HERE>",
            "DJANGO_DB_PASSWORD": "<INPUT_HERE>",
            "DJANGO_DB_HOST": "<INPUT_HERE>",
            "DJANGO_DB_PORT": "<INPUT_HERE>",
            "MONGODB_DB_USERNAME": "<INPUT_HERE>",
            "MONGODB_DB_PASSWORD": "<INPUT_HERE>",
            "MONGODB_DB_CONNECTION_STR": "<INPUT_HERE>",
            "TD_AMERITRADE_USERNAME": "<INPUT_HERE>",
            "TD_AMERITRADE_PASSWORD": "<INPUT_HERE>",
            "TD_AMERITRADE_CLIENT_ID": "<INPUT_HERE>",
            "JUST_TESTING": "<INPUT_HERE>"
        }
    },
    {
        'name': 'test_import_secrets_unencrypted_input_here.json',
        'data': {
            "DJANGO_SECRET_KEY": "<INPUT_HERE>",
            "DJANGO_DB_NAME": "<INPUT_HERE>",
            "DJANGO_DB_USERNAME": "<INPUT_HERE>",
            "DJANGO_DB_PASSWORD": "<INPUT_HERE>",
            "DJANGO_DB_HOST": "<INPUT_HERE>",
            "DJANGO_DB_PORT": "<INPUT_HERE>",
            "MONGODB_DB_USERNAME": "<INPUT_HERE>",
            "MONGODB_DB_PASSWORD": "<INPUT_HERE>",
            "MONGODB_DB_CONNECTION_STR": "<INPUT_HERE>",
            "TD_AMERITRADE_USERNAME": "<INPUT_HERE>",
            "TD_AMERITRADE_PASSWORD": "<INPUT_HERE>",
            "TD_AMERITRADE_CLIENT_ID": "<INPUT_HERE>",
        }
    },
    {
        'name': 'test_import_secrets_unencrypted_missing_keys.json',
        'data': {
            "DJANGO_SECRET_KEY": "<INPUT_HERE>",
            "DJANGO_DB_NAME": "<INPUT_HERE>",
            "DJANGO_DB_USERNAME": "<INPUT_HERE>",
            "DJANGO_DB_PASSWORD": "<INPUT_HERE>",
            "DJANGO_DB_HOST": "<INPUT_HERE>",
            "DJANGO_DB_PORT": "<INPUT_HERE>",
            "MONGODB_DB_USERNAME": "<INPUT_HERE>",
            "MONGODB_DB_PASSWORD": "<INPUT_HERE>",
            "MONGODB_DB_CONNECTION_STR": "<INPUT_HERE>",
            "TD_AMERITRADE_USERNAME": "<INPUT_HERE>",
            "TD_AMERITRADE_PASSWORD": "<INPUT_HERE>"
        }
    },
    {
        'name': 'test_import_secrets_unencrypted_number.json',
        'data': {
            "DJANGO_SECRET_KEY": 1,
            "DJANGO_DB_NAME": 2,
            "DJANGO_DB_USERNAME": 3,
            "DJANGO_DB_PASSWORD": 4,
            "DJANGO_DB_HOST": 5,
            "DJANGO_DB_PORT": 6,
            "MONGODB_DB_USERNAME": 7,
            "MONGODB_DB_PASSWORD": 8,
            "MONGODB_DB_CONNECTION_STR": 9,
            "TD_AMERITRADE_USERNAME": 10,
            "TD_AMERITRADE_PASSWORD": 11,
            "TD_AMERITRADE_CLIENT_ID": 12
        }
    },
    {
        'name': 'test_import_secrets_unencrypted_testing.json',
        'data': {
            "DJANGO_SECRET_KEY": "testing",
            "DJANGO_DB_NAME": "testing",
            "DJANGO_DB_USERNAME": "testing",
            "DJANGO_DB_PASSWORD": "testing",
            "DJANGO_DB_HOST": "testing",
            "DJANGO_DB_PORT": "testing",
            "MONGODB_DB_USERNAME": "testing",
            "MONGODB_DB_PASSWORD": "testing",
            "MONGODB_DB_CONNECTION_STR": "testing",
            "TD_AMERITRADE_USERNAME": "testing",
            "TD_AMERITRADE_PASSWORD": "testing",
            "TD_AMERITRADE_CLIENT_ID": "testing"
        }
    },

]


@pytest.fixture(scope='module')
def setup():
    try:
        os.makedirs(TEST_CONFIG_FILES_BASE_DIR)
    except FileExistsError:
        pass

    for json_obj in TEST_JSON:
        FILE_PATH = os.path.join(TEST_CONFIG_FILES_BASE_DIR, json_obj['name'])
        with open(FILE_PATH, 'w') as f:
            json.dump(json_obj['data'], f)

    yield setup
    shutil.rmtree(TEST_CONFIG_FILES_BASE_DIR)


def test_secrets_model_default():
    global pseudo_keys

    # first simple init
    secrets_model = SecretsModel(auto_import=False, crypt=pseudo_keys)
    assert secrets_model._encrypted
    assert secrets_model._secrets_path != 'testing'
    assert not secrets_model._imported
    assert secrets_model._validate_import
    assert isinstance(secrets_model._cls_members, dict)

    # second simple init
    secrets_model = SecretsModel(encrypted=False, secrets_path='testing', auto_import=False,
                                 validate_import=False, crypt=pseudo_keys)
    assert not secrets_model._encrypted
    assert secrets_model._secrets_path == 'testing'
    assert not secrets_model._imported
    assert not secrets_model._validate_import
    assert isinstance(secrets_model._cls_members, dict)


def test_import_secrets_from_file(setup):
    global pseudo_keys

    # first input <INPUT_HERE> as value
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_input_here.json')

    secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR,
                                 crypt=pseudo_keys)
    assert secrets_model._imported

    for cls_member in secrets_model._cls_members:
        assert getattr(secrets_model, cls_member) == '<INPUT_HERE>'

    # second input 'testing' as value
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_testing.json')

    secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR,
                                 crypt=pseudo_keys)
    assert secrets_model._imported

    for cls_member in secrets_model._cls_members:
        assert getattr(secrets_model, cls_member) == 'testing'

    # third input integer as value
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_number.json')

    secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR,
                                 crypt=pseudo_keys)
    assert secrets_model._imported

    for cls_member in secrets_model._cls_members:
        j = getattr(secrets_model, cls_member)
        assert isinstance(j, int)

    # fourth input exception raise because of missing key in secrets file
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_missing_keys.json')

    with pytest.raises(KeyError):
        secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR,
                                     crypt=pseudo_keys)

    # fifth input exception raise because of extra key in secrets file
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_extra_keys.json')

    with pytest.raises(KeyError):
        secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR,
                                     crypt=pseudo_keys)


def test_export_secrets_to_file(setup):
    global pseudo_keys

    # first input <INPUT_HERE> as value
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_input_here.json')

    secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR,
                                 crypt=pseudo_keys)

    for cls_member in secrets_model._cls_members:
        assert getattr(secrets_model, cls_member) == '<INPUT_HERE>'

    TEMP_OUTPUT_PATH = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                    'temp_output_file.json')
    secrets_model.export_secrets_to_config_file(encrypt=False, output_path=TEMP_OUTPUT_PATH)

    new_secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_OUTPUT_PATH,
                                     crypt=pseudo_keys)

    assert new_secrets_model._is_same_config(secrets_model)

    new_secrets_model.export_secrets_to_config_file(encrypt=True)

    new_secrets_model.import_secrets_from_config_file(encrypted=False)

    for cls_member in new_secrets_model._cls_members:
        assert getattr(new_secrets_model, cls_member) != '<INPUT_HERE>'

    new_secrets_model.import_secrets_from_config_file(encrypted=True)

    for cls_member in new_secrets_model._cls_members:
        assert getattr(new_secrets_model, cls_member) == '<INPUT_HERE>'


def test_secrets_model_read_only(setup):
    TEMP_CONFIG_FILE_DIR = os.path.join(TEST_CONFIG_FILES_BASE_DIR,
                                        'test_import_secrets_unencrypted_testing.json')

    secrets_model = SecretsModel(encrypted=False, secrets_path=TEMP_CONFIG_FILE_DIR, read_only=True)
    assert secrets_model._read_only

    with pytest.raises(ValueError):
        secrets_model.export_secrets_to_config_file()

    with pytest.raises(ValueError):
        secrets_model.import_secrets_from_config_file(encrypted=True)

