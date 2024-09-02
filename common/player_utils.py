import logging
from typing import Tuple, Optional
from pygrok import Grok
from common.shared_state import Player

logger = logging.getLogger(__name__)

# Define custom Grok patterns
custom_patterns = {
    "USERNAME": r"[^\s]+",  # This will capture everything up to a whitespace
    "BASE16NUM": "(?:0x)?[0-9a-fA-F]+",
    "WORD": r"\w+",
    "DATA": ".*?",
}

# Adjusted grok patterns for player info extraction
PLAYER_JOIN_PATTERN = (
    r"Client authenticated: \(%{WORD:player_id}\) %{USERNAME:player_name}"
)
PLAYER_LEAVE_PATTERN = r"(?:\[Shard\] )?\(%{WORD:player_id}\)(?: %{USERNAME:player_name})? disconnected from(?: \[.*\])?"
PLAYER_SPAWN_PATTERN = r"Spawn request: %{WORD:character} from %{USERNAME:player_name}"

# Create grok instances
player_join_grok = Grok(PLAYER_JOIN_PATTERN, custom_patterns=custom_patterns)
player_leave_grok = Grok(PLAYER_LEAVE_PATTERN, custom_patterns=custom_patterns)
player_spawn_grok = Grok(PLAYER_SPAWN_PATTERN, custom_patterns=custom_patterns)


def extract_player_info_from_join(
    line: str,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract player ID and name from a join event log line.

    Args:
        line (str): The log line to parse.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the player ID and name,
        or (player_id, None) if the username is invalid.

    Example:
        >>> line = "Client authenticated: (KU_Xo93QaLmG1) DST_Player"
        >>> extract_player_info_from_join(line)
        ('KU_Xo93QaLmG1', 'DST_Player')
    """
    match = player_join_grok.match(line)
    if match:
        player_id = match["player_id"]
        player_name = match["player_name"]
        if Player.is_valid_username(player_name):
            return player_id, player_name
        else:
            return player_id, None
    logger.warning(f"Failed to parse player join line: {line}")
    return None, None


def extract_player_id_from_leave(
    line: str,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract player ID and name from a leave event log line.

    Args:
        line (str): The log line to parse.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the player ID and name (if available),
        or (player_id, None) if the username is invalid.

    Example:
        >>> line = "[Shard] (KU_Xo93QaLmG1) DST_Player disconnected from [SHDMASTER](1)"
        >>> extract_player_id_from_leave(line)
        ('KU_Xo93QaLmG1', 'DST_Player')
    """
    match = player_leave_grok.match(line)
    if match:
        player_id = match["player_id"]
        player_name = match.get("player_name")
        if player_name and Player.is_valid_username(player_name):
            return player_id, player_name
        else:
            return player_id, None
    logger.warning(f"Failed to parse player leave line: {line}")
    return None, None


def extract_player_character_from_spawn(
    line: str,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract player name and character from a spawn event log line.

    Args:
        line (str): The log line to parse.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the player name and character,
        or (None, None) if parsing fails or the username is invalid.

    Example:
        >>> line = "Spawn request: wilson from DST_Player"
        >>> extract_player_character_from_spawn(line)
        ('DST_Player', 'wilson')
    """
    match = player_spawn_grok.match(line)
    if match:
        player_name = match["player_name"]
        character = match["character"]
        if Player.is_valid_username(player_name):
            return player_name, character
    logger.warning(f"Failed to parse player spawn line or invalid username: {line}")
    return None, None
