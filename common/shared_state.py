"""
Shared State Module

This module provides a SharedState class for managing the shared state of players
in a Don't Starve Together (DST) dedicated server. It includes functionality for
tracking player information, authentication, and game events.
"""

from collections import deque
from typing import Dict, Deque, Optional
import logging
import threading
from common.player import Player, validate_username

logger = logging.getLogger(__name__)


class SharedState:
    """
    Manages the shared state of players in a DST dedicated server.

    This class provides methods for synchronizing player states, tracking authentications,
    and managing player-related events.
    """

    def __init__(self):
        """Initialize the SharedState with empty player dictionary and authentication queue."""
        self.players: Dict[str, Player] = {}
        self.recent_authentications: Deque[str] = deque(maxlen=10)
        self.auth_lock = threading.Lock()

    def sync_player_state(self, player: Player, character: str = "") -> None:
        """
        Synchronize the state of a player.

        Args:
            player (Player): The player object to synchronize.
            character (str, optional): The character name if available. Defaults to "".

        Raises:
            InvalidUsernameError: If the player's username is invalid.
        """
        validate_username(player.name)

        existing_player = self.players.get(player.id)
        if existing_player:
            existing_player.name = player.name
            if character:
                existing_player.character = character
            existing_player.authenticated = player.authenticated
            logger.info(
                f"Updated player: ({player.id}) {existing_player.name} <{player.character}>"
            )
        else:
            if character:
                player.character = character
            self.players[player.id] = player
            logger.info(
                f"Added new player: ({player.id}) {player.name} <{player.character}>"
            )

        self.output_player_list()

    def get_player_by_name(self, player_name: str) -> Optional[Player]:
        """
        Get a player object by their name.

        Args:
            player_name (str): The name of the player to find.

        Returns:
            Optional[Player]: The player object if found, None otherwise.
        """
        for player in self.players.values():
            if player.name == player_name:
                return player
        logger.warning(
            f"Player with name '{player_name}' not found in shared state. Current players: {', '.join(player.name for player in self.players.values())}"
        )
        return None

    def track_authentication(self, player_id: str) -> None:
        """
        Track the authentication of a player.

        Args:
            player_id (str): The ID of the player who authenticated.
        """
        try:
            with self.auth_lock:
                self.recent_authentications.append(player_id)
        except Exception as e:
            logger.error(
                f"Error tracking authentication for player {player_id}: {str(e)}"
            )

    def get_recent_authenticated_player(self) -> Optional[str]:
        """
        Get the most recently authenticated player's ID.

        Returns:
            Optional[str]: The ID of the most recently authenticated player, or None if no recent authentications.
        """
        with self.auth_lock:
            try:
                return self.recent_authentications.pop()
            except IndexError:
                logger.warning("No recent authenticated players found.")
                return None

    def remove_player(self, player_id: str) -> str:
        """
        Remove a player from the shared state.

        Args:
            player_id (str): The ID of the player to remove.

        Returns:
            str: The name of the removed player.
        """
        player = self.players.pop(player_id, None)
        if player:
            logger.info(
                f"Removed player: ({player.id}) {player.name} <{player.character}>"
            )
        else:
            logger.warning(f"Player with ID {player_id} not found in shared state.")
            player = Player(id=player_id, name="Unknown player")

        self.output_player_list()
        return player.name

    def update_player_event(
        self, player_id: str, event: str, character: str = None
    ) -> None:
        """
        Update a player's state based on an event.

        Args:
            player_id (str): The ID of the player to update.
            event (str): The event type ('resume' or 'character_update').
            character (str, optional): The new character name for character_update events.
        """
        if not player_id or not event:
            logger.error(f"Invalid input: player_id={player_id}, event={event}")
            return

        player = self.get_player_by_id(player_id)
        if player:
            if event == "resume":
                player.resumed = True
                logger.info(f"Player ({player.id}) {player.name} has resumed the game.")
            elif event == "character_update" and character:
                player.character = character
                logger.info(
                    f"Player ({player.id}) {player.name} character updated to <{player.character}>."
                )
            else:
                logger.warning(f"Unrecognized event '{event}' for player {player_id}")

            self.output_player_list()
        else:
            logger.warning(
                f"Player with ID {player_id} not found in shared state for event '{event}'."
            )

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        """
        Get a player object by their ID.

        Args:
            player_id (str): The ID of the player to find.

        Returns:
            Optional[Player]: The player object if found, None otherwise.
        """
        return self.players.get(player_id)

    def output_player_list(self):
        """Log the current list of players."""
        if self.players:
            player_info = ", ".join(
                [
                    f"{player.name} <{player.character}>"
                    for player in self.players.values()
                ]
            )
            logger.info(f"Current players: {player_info}")
        else:
            logger.info("No players currently online.")


shared_state = SharedState()
