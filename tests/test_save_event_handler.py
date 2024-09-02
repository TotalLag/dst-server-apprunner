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
