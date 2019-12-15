import sys

from main.config.config import PUBLIC_CONFIG
from main.model.config import SecretsModel
from main.util.get_env.django_settings_env import get_debug_from_env


def get_secrets_model_from_env() -> SecretsModel or None:
    DEBUG = get_debug_from_env()
    if 'pytest' in sys.modules:
        return None
    elif DEBUG:
        return SecretsModel(encrypted=False, secrets_path=PUBLIC_CONFIG.DEBUG_SECRETS_DIR,
                            read_only=True)
    else:
        return SecretsModel(auto_import=False)