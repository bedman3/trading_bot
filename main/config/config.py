import os


class PUBLIC_CONFIG:
    CHROME_DRIVER_URL = "downloads/chromedriver"
    SECRETS_DIR = "main/config/secrets.json"
    DEBUG_SECRETS_DIR = "main/config/secrets_local.json"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

