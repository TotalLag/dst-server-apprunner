import logging
from common.game_commands import GameCommandExecutor
from common.grouped_events import GroupedEventHandler

# Set up logger for this module
logger = logging.getLogger(__name__)

# Define patterns for save event
SAVE_EVENT_START_PATTERN = "Available disk space for save files:"
SAVE_EVENT_END_PATTERN = "Serializing"


class SaveEventHandler:
    def __init__(self):
        self._executor = None

    @property
    def executor(self):
        if self._executor is None:
            self._executor = GameCommandExecutor()
        return self._executor

    def handle_save_event(self, event_lines):
        """
        Finalize the save event processing.
        """
        logger.info(f"Save event completed. Collected {len(event_lines)} log lines.")
        for line in event_lines:
            logger.debug(f"Save event log: {line}")
        self.executor.send_console_message("Save sequence complete!")


def register_save_event_handler(event_registry):
    """
    Register the save event handler with the event registry.

    Args:
        event_registry: The event registry to register the handler with.
    """
    handler = SaveEventHandler()
    # Create a GroupedEventHandler for save events
    grouped_handler = GroupedEventHandler(
        start_pattern=SAVE_EVENT_START_PATTERN,
        end_pattern=SAVE_EVENT_END_PATTERN,
        final_action=handler.handle_save_event,
    )
    # Register the start and end patterns using GroupedEventHandler
    event_registry.register_handler(
        SAVE_EVENT_START_PATTERN, grouped_handler.handle_event_line
    )
    event_registry.register_handler(
        SAVE_EVENT_END_PATTERN, grouped_handler.handle_event_line
    )

    logger.info("Registered save event handler for save sequence events")
