"""
Example Unpause Event Handler Module

This module serves as an example of how to create an event handler for a Don't Starve Together (DST) dedicated server.
It demonstrates handling the "Server Unpaused" event, logging the event, and sending an in-game message.
This example can be used as a template for creating other custom event handlers.
"""

# This handler serves as an example to show how you can get started with something as simple as unpausing.
# It demonstrates how to create a handler that listens for specific keywords in the server log
# and triggers actions based on these events.

import logging
from common.game_commands import (
    GameCommandExecutor,
)  # Import the GameCommandExecutor to send in-game commands

# Set up logger for this module
logger = logging.getLogger(__name__)

# Instantiate the GameCommandExecutor, which will allow us to send commands to the server's console.
executor = GameCommandExecutor()


# Function to handle the "Server Unpaused" event. This function is called when the log contains "Server Unpaused".
def handle_server_unpaused(log_line):
    """
    Handles the 'Server Unpaused' event.

    This function is triggered when the server unpauses, which is detected by the "Server Unpaused" keyword in the log.

    - Logs the unpause event for auditing purposes.
    - Sends a message to the in-game console to notify players that the server is unpaused.

    :param log_line: The line from the server log file that contains the "Server Unpaused" event.
    """

    # Log the event at INFO level to track when the server unpauses.
    logger.info(f"Detected server unpause: {log_line}")

    # Send an in-game message to all connected players, notifying them that the server is unpaused.
    # This uses the GameCommandExecutor instance (executor) to send a message to the game's console.
    executor.send_console_message("Server has been unpaused!")


# This function registers the handler with the event registry.
# The handler will be called whenever the server log contains the phrase "Server Unpaused".
def register_unpause_event_handler(event_registry):
    """
    Register the unpause event handler with the event registry.

    This function tells the event registry (a system that dispatches events based on log keywords) to
    trigger the `handle_server_unpaused` function when the keyword "Server Unpaused" appears in the log.

    - Developers can use this function as a template for registering their own event handlers.
    - Simply change the keyword to match the log line you're interested in, and the handler function to whatever action you want to take.

    :param event_registry: The event registry object responsible for dispatching events.
    """

    # Register the "Server Unpaused" keyword and map it to the handle_server_unpaused function.
    # Whenever the log line contains "Server Unpaused", the `handle_server_unpaused` function will be triggered.
    event_registry.register_handler("Server Unpaused", handle_server_unpaused)

    # Log that the unpause event handler was successfully registered. This helps track which
    # event handlers are loaded during the application startup.
    logger.info("Registered handler for 'Server Unpaused' event")


# Developers can use this example as a template to create their own event handlers:
#
# 1. Choose the keyword you want to detect in the log file (e.g., "Player connected", "Server Restarted").
# 2. Create a function similar to `handle_server_unpaused` that defines what action should be taken when the event occurs.
# 3. In the `register_unpause_event_handler` function (or your own version of it), register the keyword with the event registry
#    and link it to the handler function you created.
# 4. Add any additional logic you may need, such as logging, sending in-game messages, or performing custom actions.
