from dataclasses import dataclass
import re


class InvalidUsernameError(ValueError):
    pass


@dataclass
class Player:
    id: str
    name: str
    character: str = "unknown"
    authenticated: bool = False
    resumed: bool = False

    VALID_USERNAME_REGEX = r"^[a-zA-Z0-9._-]+$"

    @staticmethod
    def is_valid_username(username: str) -> bool:
        return re.match(Player.VALID_USERNAME_REGEX, username) is not None


def validate_username(username: str) -> None:
    if not Player.is_valid_username(username):
        raise InvalidUsernameError(f"Invalid username: {username}")
