import unittest
from unittest.mock import Mock
import logging
from common.grouped_events import GroupedEventHandler

# Set up logging for the test
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestGroupedEventHandler(unittest.TestCase):
    def test_grouped_event_handling(self):
        logger.debug("Starting test_grouped_event_handling")

        # Mock final action
        final_action_mock = Mock()

        # Create a GroupedEventHandler for testing
        grouped_handler = GroupedEventHandler(
            start_pattern="Event Start",
            end_pattern="Event End",
            final_action=final_action_mock,
        )

        # Define log lines to simulate an event
        log_lines = ["Event Start", "Processing...", "Event End"]

        # Pass each log line to the grouped_handler to simulate the event
        for line in log_lines:
            logger.debug(f"Processing line: {line}")
            grouped_handler.handle_event_line(line)

        # Assert that final_action was called once with the correct lines
        final_action_mock.assert_called_once_with(
            ["Event Start", "Processing...", "Event End"]
        )
        logger.debug(f"Final action call count: {final_action_mock.call_count}")
        logger.debug(f"Final action call args: {final_action_mock.call_args}")

        logger.debug("Finished test_grouped_event_handling")


if __name__ == "__main__":
    unittest.main()
