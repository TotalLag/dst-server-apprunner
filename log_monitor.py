"""
DST Server Log Monitor

This module implements a log monitor for Don't Starve Together server logs.
It watches for changes in the log file and processes new log entries.
"""

import os
import sys
import time
import importlib
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from common.event_registry import EventRegistry

# Constants
LOGFILE = (
    "/home/steam/.klei/DoNotStarveTogether/Cluster_1/Master/server_log.txt"
)
HANDLERS_DIR = "handlers"

# Global debug flag
DEBUG_MODE = False


class LogEventHandler(FileSystemEventHandler):
    """
    Handles file system events for the log file.

    This class extends FileSystemEventHandler to process modifications
    to the monitored log file.
    """

    def __init__(self, logger: logging.Logger, event_registry: EventRegistry):
        """
        Initialize the LogEventHandler.

        Args:
            logger (logging.Logger): Logger instance for this handler.
            event_registry (EventRegistry): Registry for event handlers.
        """
        self.last_file_position = 0
        self.logger = logger
        self.event_registry = event_registry

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handle file modification events.

        Args:
            event (FileSystemEvent): The event object representing the file system event.
        """
        if event.src_path == LOGFILE:
            self._process_new_log_lines()

    def _process_new_log_lines(self) -> None:
        """Process new lines added to the log file since last read."""
        try:
            with open(LOGFILE, "r") as f:
                f.seek(self.last_file_position)
                for line in f:
                    self._process_log_line(line.strip())
                self.last_file_position = f.tell()
        except IOError as e:
            self.logger.error(f"Error reading log file: {str(e)}")

    def _process_log_line(self, line: str) -> None:
        """
        Process a single log line.

        Args:
            line (str): A single line from the log file.
        """
        cleaned_line = line.split("]:", 1)[-1].strip()
        self.event_registry.handle_log_line(cleaned_line)


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration.

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def import_and_register_handlers(
    event_registry: EventRegistry, logger: logging.Logger
) -> None:
    """
    Import and register all handler modules.

    This function dynamically imports all Python files in the handlers directory
    and registers any functions that start with 'register_'.

    Args:
        event_registry (EventRegistry): Registry for event handlers.
        logger (logging.Logger): Logger instance for logging messages.
    """
    handlers_directory = os.path.join(os.path.dirname(__file__), HANDLERS_DIR)
    logger.info(f"Searching for handlers in: {handlers_directory}")

    for filename in os.listdir(handlers_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{HANDLERS_DIR}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for name in dir(module):
                    if name.startswith("register_"):
                        getattr(module, name)(event_registry)
                        logger.info(
                            f"Registered handler: {name} from {filename}"
                        )
            except Exception as e:
                logger.error(f"Error loading handler {filename}: {str(e)}")


def run_log_monitor() -> None:
    """
    Run the main log monitoring process.

    This function sets up logging, waits for the log file to be available,
    imports and registers handlers, and starts the file system observer.
    """
    logger = setup_logging()
    logger.info(f"Starting log monitor for: {LOGFILE}")

    while not os.path.exists(LOGFILE):
        logger.info("Waiting for log file to be created...")
        time.sleep(5)

    if not os.access(LOGFILE, os.R_OK):
        logger.error(f"Log file is not readable: {LOGFILE}")
        sys.exit(1)

    event_registry = EventRegistry()
    import_and_register_handlers(event_registry, logger)

    event_handler = LogEventHandler(logger, event_registry)
    observer = Observer()
    observer.schedule(
        event_handler, path=os.path.dirname(LOGFILE), recursive=False
    )

    try:
        observer.start()
        logger.info("Log monitoring started")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Stopping log monitor.")
    finally:
        observer.stop()
        observer.join()
        logger.info("Log monitor stopped.")


def main() -> None:
    """
    Main entry point for the log monitor script.

    This function parses command-line arguments and starts the log monitor.
    """
    global DEBUG_MODE
    parser = argparse.ArgumentParser(description="DST Server Log Monitor")
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )
    args = parser.parse_args()
    DEBUG_MODE = args.debug

    run_log_monitor()


if __name__ == "__main__":
    main()
