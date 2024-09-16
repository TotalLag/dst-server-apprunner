"""
Player List Handler Module

This module provides functionality to handle and process the output of the c_listallplayers() command
in a Don't Starve Together (DST) dedicated server. It includes a PlayerListHandler class that parses
the command output and updates the shared state with the current list of players.
"""

import logging
from typing import List, Any
from pygrok import Grok

from common.shared_state import shared_state, Player

logger = logging.getLogger(__name__)

PLAYER_LIST_PATTERN = (
    r"\[%{NUMBER:index}\] \(%{WORD:player_id}\) %{DATA:player_name} <%{WORD:character}>"
)


class PlayerListHandler:
    """
    Handles the processing of c_listallplayers() command output.

    This class is responsible for detecting the start of a player list in the log,
    collecting player information, and updating the shared state with the current
    list of players.
    """

    def __init__(self):
        self.waiting_for_player_list = False
        self.player_lines: List[str] = []
        self.grok = Grok(PLAYER_LIST_PATTERN)

    def handle_player_log_line(self, log_line: str) -> None:
        """
        Process log lines related to the c_listallplayers() command and its results.

        This method detects the start of a player list, collects player information,
        and finalizes the list when complete.

        Args:
            log_line (str): The log line to process.
        """
        logger.debug(f"Processing log line: {log_line}")

        if 'RemoteCommandInput: "c_listallplayers()"' in log_line:
            self._start_player_list_processing()
        elif self.waiting_for_player_list:
            if self.grok.match(log_line):
                self.player_lines.append(log_line)
            else:
                self._finalize_player_list()
                self.waiting_for_player_list = False

    def _start_player_list_processing(self) -> None:
        """
        Prepare for processing c_listallplayers() command results.

        This method is called when the c_listallplayers() command is detected in the log.
        It resets the player_lines list and sets the waiting_for_player_list flag to True.
        """
        self.waiting_for_player_list = True
        self.player_lines = []
        logger.debug(
            "c_listallplayers() command detected, starting player list update."
        )

    def _finalize_player_list(self) -> None:
        """
        Finalize the processing of the player list and update shared state.

        This method parses the collected player lines, creates Player objects,
        and updates the shared state with the new player list. It also handles
        any errors that occur during parsing and logs them appropriately.
        """
        for line in self.player_lines:
            match = self.grok.match(line)
            if match:
                player_id = match["player_id"]
                player_name = match["player_name"].strip()
                character = match["character"]

                if Player.is_valid_username(player_name):
                    player = Player(id=player_id, name=player_name, character=character)
                    shared_state.sync_player_state(player, character)
                else:
                    logger.error(f"Invalid username detected: {player_name}")
            else:
                logger.error(f"Failed to parse player list line: {line}")

        logger.debug(f"Player list updated based on c_listallplayers() output.")
        self.player_lines = []


def register_handlers(event_registry: Any) -> None:
    """
    Register the player list handler with the event registry.

    This function creates a PlayerListHandler instance and registers it
    to handle the c_listallplayers() command output.

    Args:
        event_registry: The event registry to register the handler with.
    """
    handler = PlayerListHandler()
    event_registry.register_handler(
        'RemoteCommandInput: "c_listallplayers()"',
        handler.handle_player_log_line,
    )
    logger.info("Registered player list handler for c_listallplayers() command")
