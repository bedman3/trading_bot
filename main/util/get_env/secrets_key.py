import os


def get_secrets_key_from_env() -> list or None:
    secrets_key: str = os.environ.get('SECRETS_KEY')

    if secrets_key is not None:
        secrets_key: list = secrets_key.split(',')

    return secrets_key
