from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        Find password from username
        :param username:
        :return:
        """

    @classmethod
    def check_passwords_match(cls, password1: str, password2: str) -> bool:
        """Checking the password for matches"""
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Check if password matches username
        :param username:
        :param password:
        :return: True if password matches username else False
        """
        dp_password = self.get_user_password(username)
        if dp_password is None:
            return False
        return self.check_passwords_match(password1=dp_password, password2=password)
