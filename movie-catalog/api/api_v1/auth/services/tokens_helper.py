import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if token exists.
        :return:
        """
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Save token to storage.
        :param token:
        :return:
        """
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
