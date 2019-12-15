from cryptography.fernet import Fernet

from main.util.get_env.secrets_key import get_secrets_key_from_env


class ConfigCrypter:

    def __init__(self, keys: list = None):
        self.keys = keys
        if self.keys is None:
            self.keys = get_secrets_key_from_env()

        if self.keys is None:
            raise ValueError('Keys missing!')

        self.__fernet_1 = Fernet(self.keys[0].encode())
        self.__fernet_2 = Fernet(self.keys[1].encode())

    def encrypt_value(self, text: str) -> str:
        first_encrypted_text = self.__fernet_1.encrypt(text.encode())
        return self.__fernet_2.encrypt(first_encrypted_text).decode()

    def decrypt_value(self, text: str) -> str:
        first_decrypted_text = self.__fernet_2.decrypt(text.encode())
        return self.__fernet_1.decrypt(first_decrypted_text).decode()

    @staticmethod
    def generate_random_keys():
        keys = [Fernet.generate_key().decode(), Fernet.generate_key().decode()]
        return keys