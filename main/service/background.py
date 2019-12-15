from main.model.config import SecretsModel
from main.util.get_env.secrets_model import get_secrets_model_from_env

SECRETS_MODEL: SecretsModel or None = get_secrets_model_from_env()


def update_secrets_model():
    global SECRETS_MODEL
    if SECRETS_MODEL is None:
        SECRETS_MODEL = get_secrets_model_from_env()