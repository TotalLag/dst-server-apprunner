"""
Test Shard Server Handler Module

This module contains unit tests for the ShardServerHandler class from the handlers.shard_server_handler module.
It verifies that the ShardServerHandler correctly processes a sequence of log lines related to a shard server start event
and sends the appropriate console message when the server is up and running.
"""

import unittest
from unittest.mock import patch, Mock
from handlers.shard_server_handler import (
    ShardServerHandler,
    SHARD_START_PATTERN,
    SHARD_END_PATTERN,
)
from common.grouped_events import GroupedEventHandler


class TestShardServerHandler(unittest.TestCase):
    @patch("handlers.shard_server_handler.GameCommandExecutor")
    def test_shard_server_event_sequence(self, MockExecutor):
        """
        Test the complete shard server start event sequence handling.

        This test verifies that:
        1. The ShardServerHandler correctly processes a sequence of log lines related to a shard server start event.
        2. The GroupedEventHandler correctly identifies the start and end of the shard server event.
        3. The handle_shard_event method is called with the correct sequence of event lines.
        4. The GameCommandExecutor is instantiated and used to send the correct console message.

        The test uses a mock GameCommandExecutor to verify the correct behavior without actually
        sending commands to the game console.
        """
        # Create a mock instance of GameCommandExecutor
        mock_executor_instance = Mock()
        MockExecutor.return_value = mock_executor_instance

        # Initialize ShardServerHandler
        handler = ShardServerHandler()

        # Create a GroupedEventHandler for the test
        grouped_handler = GroupedEventHandler(
            start_pattern=SHARD_START_PATTERN,
            end_pattern=SHARD_END_PATTERN,
            final_action=handler.handle_shard_event,
        )

        # Define the sequence of log lines for a complete shard server start event
        log_lines = [
            "[Shard] Starting master server",
            "Initializing...",
            "Server registered via geo DNS",
        ]

        # Pass each log line to the grouped_handler to simulate the event sequence
        for line in log_lines:
            grouped_handler.handle_event_line(line)

        # Assert that GameCommandExecutor was instantiated
        MockExecutor.assert_called_once()

        # Assert that send_console_message was called with the correct message
        mock_executor_instance.send_console_message.assert_called_once_with(
            "Server is up and running!"
        )


if __name__ == "__main__":
    unittest.main()
