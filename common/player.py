"""
Player Module

This module defines the Player class and related utilities for managing player
information in a Don't Starve Together (DST) dedicated server.

It includes functionality for validating usernames and handling player data.
"""

from dataclasses import dataclass
import re


class InvalidUsernameError(ValueError):
    """Exception raised for invalid usernames."""

    pass


@dataclass
class Player:
    """
    Represents a player in the Don't Starve Together game.

    Attributes:
        id (str): The unique identifier for the player.
        name (str): The player's username.
        character (str): The character chosen by the player. Defaults to "unknown".
        authenticated (bool): Whether the player is authenticated. Defaults to False.
        resumed (bool): Whether the player has resumed a previous session. Defaults to False.
    """

    id: str
    name: str
    character: str = "unknown"
    authenticated: bool = False
    resumed: bool = False

    VALID_USERNAME_REGEX = r"^[a-zA-Z0-9._-]+$"

    @staticmethod
    def is_valid_username(username: str) -> bool:
        """
        Check if a username is valid according to the defined regex pattern.

        Args:
            username (str): The username to validate.

        Returns:
            bool: True if the username is valid, False otherwise.
        """
        return re.match(Player.VALID_USERNAME_REGEX, username) is not None


def validate_username(username: str) -> None:
    """
    Validate a username and raise an exception if it's invalid.

    Args:
        username (str): The username to validate.

    Raises:
        InvalidUsernameError: If the username is invalid.
    """
    if not Player.is_valid_username(username):
        raise InvalidUsernameError(f"Invalid username: {username}")
