"""
Shard Server Handler Module

This module provides functionality to handle shard server events in a Don't Starve Together (DST) dedicated server.
It includes a ShardServerHandler class and a function to register the handler with an event registry.
"""

import logging
from typing import List, Any
from common.game_commands import GameCommandExecutor
from common.grouped_events import GroupedEventHandler
from common.mod_manager import get_installed_mods

# Set up logger for this module
logger = logging.getLogger(__name__)

# Define patterns for shard events
SHARD_START_PATTERN = "[Shard] Starting master server"
SHARD_END_PATTERN = "Server registered via geo DNS"


class ShardServerHandler:
    """
    Handler for shard server events in a DST dedicated server.

    This class processes shard server events, sends console messages,
    and logs information about installed mods when the server starts up.
    """

    def __init__(self):
        """
        Initialize the ShardServerHandler.
        """
        self._executor = None

    @property
    def executor(self):
        """
        Lazy-loaded GameCommandExecutor instance.

        Returns:
            GameCommandExecutor: An instance of the GameCommandExecutor.
        """
        if self._executor is None:
            self._executor = GameCommandExecutor()
        return self._executor

    def handle_shard_event(self, event_lines: List[str]) -> None:
        """
        Process the collected log lines for the shard server event.

        This method is called when a complete shard server event (from start to end)
        has been detected in the log. It logs the server status, sends a console message,
        and logs information about installed mods.

        Args:
            event_lines (List[str]): The list of log lines that comprise the shard server event.
        """
        logger.info("Server UP!")
        self.executor.send_console_message("Server is up and running!")

        # Log enabled mods
        enabled_mods = get_installed_mods()
        if enabled_mods:
            mod_info = "\n".join([f"[{mod[0]}]: {mod[1]}" for mod in enabled_mods])
            logger.info(f"Installed mods:\n{mod_info}")
        else:
            logger.info("No mods are currently installed.")


def register_shard_event_handler(event_registry: Any) -> None:
    """
    Register the shard server event handler with the event registry.

    This function creates a ShardServerHandler and a GroupedEventHandler,
    then registers the appropriate patterns with the event registry to handle
    shard server start and end events.

    Args:
        event_registry (Any): The event registry to register the handlers with.
    """
    handler = ShardServerHandler()
    # Use the patterns for grouped event handler
    grouped_handler = GroupedEventHandler(
        start_pattern=SHARD_START_PATTERN,
        end_pattern=SHARD_END_PATTERN,
        final_action=handler.handle_shard_event,
    )

    # Register the start and end patterns using GroupedEventHandler
    event_registry.register_handler(
        SHARD_START_PATTERN, grouped_handler.handle_event_line
    )
    event_registry.register_handler(
        SHARD_END_PATTERN, grouped_handler.handle_event_line
    )

    logger.info("Registered shard server start and end handlers")
