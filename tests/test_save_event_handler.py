"""
Test Save Event Handler Module

This module contains unit tests for the SaveEventHandler class from the handlers.save_event_handler module.
It verifies that the SaveEventHandler correctly processes a sequence of log lines related to a save event
and sends the appropriate console message when the save sequence is complete.
"""

import unittest
from unittest.mock import patch, Mock
from handlers.save_event_handler import (
    SaveEventHandler,
    SAVE_EVENT_START_PATTERN,
    SAVE_EVENT_END_PATTERN,
)
from common.grouped_events import GroupedEventHandler


class TestSaveEventHandler(unittest.TestCase):
    @patch("handlers.save_event_handler.GameCommandExecutor")
    def test_complete_save_event_sequence(self, MockExecutor):
        """
        Test the complete save event sequence handling.

        This test verifies that:
        1. The SaveEventHandler correctly processes a sequence of log lines related to a save event.
        2. The GroupedEventHandler correctly identifies the start and end of the save event.
        3. The handle_save_event method is called with the correct sequence of event lines.
        4. The GameCommandExecutor is instantiated and used to send the correct console message.

        The test uses a mock GameCommandExecutor to verify the correct behavior without actually
        sending commands to the game console.
        """
        # Create a mock instance of GameCommandExecutor
        mock_executor_instance = Mock()
        MockExecutor.return_value = mock_executor_instance

        # Initialize SaveEventHandler
        handler = SaveEventHandler()

        # Create a GroupedEventHandler for the test
        grouped_handler = GroupedEventHandler(
            start_pattern=SAVE_EVENT_START_PATTERN,
            end_pattern=SAVE_EVENT_END_PATTERN,
            final_action=handler.handle_save_event,
        )

        # Define the sequence of log lines for a complete save event
        log_lines = [
            "Available disk space for save files: 887762 MB",
            "Saving...",
            "Compressing...",
            "Serializing world: session/84245C4CBF2C1D9B/0000000003",
        ]

        # Pass each log line to the grouped_handler to simulate the event sequence
        for line in log_lines:
            grouped_handler.handle_event_line(line)

        # Assert that GameCommandExecutor was instantiated
        MockExecutor.assert_called_once()

        # Assert that send_console_message was called with the correct message
        mock_executor_instance.send_console_message.assert_called_once_with(
            "Save sequence complete!"
        )


if __name__ == "__main__":
    unittest.main()
