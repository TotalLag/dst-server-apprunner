"""
Event Registry Module

This module provides an EventRegistry class for managing event handlers in a log-based system.
It allows registration and deregistration of handlers for specific event keywords and processes
log lines to invoke the appropriate handlers.
"""

import logging
import traceback


class EventRegistry:
    """
    A class to manage event handlers for different event keywords.

    This class allows registration and deregistration of event handlers, and processes
    log lines to invoke the appropriate handlers based on matching keywords.
    """

    def __init__(self):
        """Initialize the EventRegistry with an empty handler dictionary and a logger."""
        self._handlers = {}
        self._logger = logging.getLogger(__name__)

    def register_handler(self, event_keyword, handler):
        """
        Register a new event handler with the given event keyword.

        :param event_keyword: The keyword to match in log lines
        :param handler: The event handler function to be invoked
        """
        if event_keyword not in self._handlers:
            self._handlers[event_keyword] = []
        self._handlers[event_keyword].append(handler)
        self._logger.info(f"Registered handler for keyword: {event_keyword}")

    def deregister_handler(self, event_keyword):
        """
        Deregister an existing event handler with the given event keyword.

        :param event_keyword: The keyword to match in log lines
        """
        if event_keyword in self._handlers:
            del self._handlers[event_keyword]
            self._logger.info(f"Deregistered handlers for keyword: {event_keyword}")

    def handle_log_line(self, log_line):
        """
        Process a log line and invoke appropriate handlers based on matching keywords.

        :param log_line: The log line to process
        """
        for keyword, handlers in self._handlers.items():
            if keyword in log_line:
                for handler in handlers:
                    try:
                        handler(log_line)
                    except Exception as e:
                        self._logger.error(
                            f"Error handling log line with keyword '{keyword}': {str(e)}"
                        )
                        self._logger.debug(traceback.format_exc())

    def get_handlers(self):
        """
        Retrieve all registered handlers.

        :return: A dictionary of all registered handlers
        """
        return self._handlers
