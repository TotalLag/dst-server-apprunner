# handlers/player_join_handler.py

import logging
from typing import Any
from common.game_commands import GameCommandExecutor
from common.shared_state import shared_state, Player
from common.player_utils import (
    extract_player_info_from_join,
    extract_player_id_from_leave,
    extract_player_character_from_spawn,
)

logger = logging.getLogger(__name__)
executor = GameCommandExecutor()


def handle_player_join(line: str) -> None:
    """
    Handles the player authentication event.

    Args:
        line (str): The log line containing player join information.
    """
    player_id, username = extract_player_info_from_join(line)

    if not (player_id and username):
        logger.error(f"Failed to process authentication event: {line}")
        return

    if not Player.is_valid_username(username):
        logger.error(f"Invalid username detected: {username}")
        return

    # Create or update the player in shared_state
    player = Player(id=player_id, name=username, authenticated=True)
    shared_state.sync_player_state(player)

    # Track the player's ID for recent authentication
    shared_state.track_authentication(player_id)

    # Send welcome message (in-game)
    executor.send_console_message(f"{username} has joined the server!")


def handle_player_leave(line: str) -> None:
    """
    Handles the player disconnection event.

    Args:
        line (str): The log line containing player leave information.
    """
    player_id, _ = extract_player_id_from_leave(line)

    if not player_id:
        logger.error(f"Failed to process leave event: {line}")
        return

    # Remove the player from shared_state and get the player's name
    player_name = shared_state.remove_player(player_id)

    # Send leave message (in-game)
    executor.send_console_message(f"{player_name} has left the server!")


def handle_player_resume(line: str) -> None:
    """
    Handles the player resume event.

    Args:
        line (str): The log line containing player resume information.
    """
    # Use the most recent authenticated player ID
    player_id = shared_state.get_recent_authenticated_player()
    if player_id:
        # Update the player's event in shared_state and sync character information if available
        shared_state.update_player_event(player_id, "resume")

        # Send welcome back message (in-game)
        player = shared_state.get_player_by_id(player_id)
        if player:
            executor.send_console_message(f"Welcome back {player.name}!")
    else:
        logger.warning(
            "No recent authenticated player ID found to handle resume event."
        )


def handle_player_spawn(line: str) -> None:
    """
    Handles the player spawn event and updates their character.

    Args:
        line (str): The log line containing player spawn information.
    """
    player_name, character = extract_player_character_from_spawn(line)
    if player_name and character:
        player = shared_state.get_player_by_name(player_name)

        if player:
            # Sync player state with the character information
            shared_state.sync_player_state(player, character=character)

            # Send in-game notification
            executor.send_console_message(f"{player.name} has spawned as {character}!")
        else:
            logger.warning(f"No authenticated player found with name {player_name}")
    else:
        logger.warning(f"Failed to parse spawn event from line: {line}")


def register_player_join_handler(event_registry: Any) -> None:
    """
    Registers the player join, leave, resume, and spawn handlers with the event registry.

    Args:
        event_registry (Any): The event registry to register the handlers with.
    """
    event_registry.register_handler("Client authenticated:", handle_player_join)
    event_registry.register_handler("disconnected from", handle_player_leave)
    event_registry.register_handler("Resuming user", handle_player_resume)
    event_registry.register_handler("Spawn request:", handle_player_spawn)
    logger.info("Registered player join, leave, and resume handlers")
