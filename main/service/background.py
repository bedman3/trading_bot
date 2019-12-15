import traceback

from main.model.config import SecretsModel
from main.util.get_env.secrets_model import get_secrets_model_from_env
from main.util.logger.init_logger import get_logger

logger = get_logger(__name__)

SECRETS_MODEL: SecretsModel or None = None


def update_secrets_model():
    global SECRETS_MODEL
    if SECRETS_MODEL is None:
        SECRETS_MODEL = get_secrets_model_from_env()


def update_secrets_model_import():
    global SECRETS_MODEL

    if SECRETS_MODEL is None:
        SECRETS_MODEL = get_secrets_model_from_env()
        print(SECRETS_MODEL._has_keys(), SECRETS_MODEL._read_only, SECRETS_MODEL._imported)

    try:
        SECRETS_MODEL.import_secrets_from_config_file()
        logger.info('Model successfully updated!')
    except ValueError as e:
        if SECRETS_MODEL.reload_crypter_keys_from_env():
            SECRETS_MODEL.import_secrets_from_config_file()
            logger.info('Model successfully updated!')
        else:
            logger.error(traceback.format_exc())


update_secrets_model_import()
