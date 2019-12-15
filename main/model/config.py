import json
import os

from main.config.config import PUBLIC_CONFIG
from main.util.encrypt.config_crypter import ConfigCrypter


class SecretsModel:
    """
    Model to store secrets, useful in handle de/encryption with secret keys
    """

    def __init__(self, encrypted: bool = True, secrets_path: str = None, auto_import: bool = True,
                 validate_import: bool = True, crypt: ConfigCrypter or list = None,
                 read_only: bool = False):
        """
        Initiate the config class, capture parameters for custom actions
        """
        self._secrets_path: str = os.path.join(PUBLIC_CONFIG.BASE_DIR, PUBLIC_CONFIG.SECRETS_DIR)
        self._imported: bool = False
        self._validate_import: bool = validate_import
        if secrets_path is not None:
            self._secrets_path: str = secrets_path
        self._encrypted: bool = encrypted
        self._read_only: bool = read_only

        if isinstance(crypt, list):
            self.__crypter: ConfigCrypter = ConfigCrypter(keys=crypt)
        elif isinstance(crypt, ConfigCrypter):
            self.__crypter: ConfigCrypter = crypt
        else:
            try:
                self.__crypter: ConfigCrypter = ConfigCrypter()
            except ValueError:
                self.__crypter = None

        self.DJANGO_SECRET_KEY: str = None
        self.DJANGO_DB_NAME: str = None
        self.DJANGO_DB_USERNAME: str = None
        self.DJANGO_DB_PASSWORD: str = None
        self.DJANGO_DB_HOST: str = None
        self.DJANGO_DB_PORT: str = None
        self.MONGODB_DB_USERNAME: str = None
        self.MONGODB_DB_PASSWORD: str = None
        self.MONGODB_DB_CONNECTION_STR: str = None
        self.TD_AMERITRADE_USERNAME: str = None
        self.TD_AMERITRADE_PASSWORD: str = None
        self.TD_AMERITRADE_CLIENT_ID: str = None

        # get dict of class members
        raw_cls_members = vars(self)
        self._cls_members: dict = {k: raw_cls_members.get(k) for k in raw_cls_members if
                                   not k.startswith('_')}

        if auto_import:
            self.import_secrets_from_config_file(self._encrypted)

    def import_secrets_from_config_file(self, encrypted: bool = True) -> None:
        if encrypted and (self._read_only or not self._has_keys()):
            raise ValueError('Read only mode does not support de/encryption, please use keys')

        with open(self._secrets_path) as json_file:
            data: dict = json.load(json_file)

        # validate the secrets file integrity
        if self._validate_import:
            if self._cls_members.keys() != data.keys():
                raise KeyError('Secrets file corrupted! Keys do not match model!')

        for cls_member in self._cls_members:
            value = data.get(cls_member)

            if encrypted:
                value = self.__crypter.decrypt_value(value)

            self.set_config(cls_member, value)

        self._imported = True

    def export_secrets_to_config_file(self, encrypt: bool = True, output_path: str = None) -> None:
        if not self._has_keys() and encrypt:
            raise ValueError('Crypters not initialized')

        if self._read_only:
            raise ValueError('Read only mode does not support export')

        if not self._imported:
            raise ValueError('Secrets not imported, run import before export!')

        output_path = output_path
        if output_path is None:
            output_path = self._secrets_path

        json_obj = {}

        for cls_member in self._cls_members:
            value = self.get_config(cls_member)

            if encrypt:
                value = self.__crypter.encrypt_value(value)

            json_obj[cls_member] = value

        with open(output_path, 'w') as file:
            json.dump(json_obj, file)

    def get_config(self, cls_member):
        return super().__getattribute__(cls_member)

    def set_config(self, cls_member, value):
        return super().__setattr__(cls_member, value)

    def flush_config(self) -> None:
        for cls_member in self._cls_members:
            self.set_config(cls_member, None)
        self._imported = False

    def _is_same_config(self, obj: "SecretsModel") -> bool:
        if self._cls_members != obj._cls_members:
            return False

        for cls_member in self._cls_members:
            if self.get_config(cls_member) != obj.get_config(cls_member):
                return False

        return True

    def _has_keys(self) -> bool:
        return self.__crypter is not None

    def update_crypter(self, crypter):
        if isinstance(crypter, ConfigCrypter):
            self.__crypter = crypter
        else:
            raise ValueError('Crypter invalid, remain the original crypter')
