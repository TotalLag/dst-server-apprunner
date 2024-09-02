import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


class GroupedEventHandler:
    def __init__(self, start_pattern, end_pattern, final_action):
        self.start_pattern = start_pattern
        self.end_pattern = end_pattern
        self.final_action = final_action
        self.in_event = False
        self.event_lines = []
        self.logger = logging.getLogger(__name__)

    def handle_event_line(self, line):
        """Handle a single log line for a grouped event."""
        if not line:
            self.logger.error("Encountered NoneType or empty log line, skipping")
            return

        # Try matching the start of the event
        if not self.in_event and self.start_pattern in line:
            self.logger.debug(f"Detected start of event: {line}")
            self.in_event = True
            self.event_lines = [line]

        # Try matching the end of the event
        elif self.in_event and self.end_pattern in line:
            self.logger.debug(f"Detected end of event: {line}")
            self.event_lines.append(line)
            self.finalize_event()

        # Collect lines within the event if in_event is True
        elif self.in_event:
            self.logger.debug(f"Collecting line for event: {line}")
            self.event_lines.append(line)

    def finalize_event(self):
        """Finalize and process the event."""
        if self.event_lines:
            self.logger.debug(f"Finalizing event with lines: {self.event_lines}")
            self.final_action(self.event_lines)
        else:
            self.logger.warning("Attempted to finalize event with no collected lines.")
        # Reset state after finalizing
        self.in_event = False
        self.event_lines = []


# Add a debug log at the module level
logger.debug("GroupedEventHandler module loaded")
