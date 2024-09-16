"""
Game Commands Module

This module provides a GameCommandExecutor class for executing various game commands
on a Don't Starve Together (DST) dedicated server running in a tmux session.
It uses subprocess to send commands to the tmux session.
"""

import subprocess
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


class GameCommandExecutor:
    """
    A class to execute game commands on a DST dedicated server running in a tmux session.
    """

    def __init__(self, logger=None):
        """
        Initialize the GameCommandExecutor.

        Args:
            logger (logging.Logger, optional): A custom logger. If not provided, a default logger will be used.
        """
        self.logger = logger or logging.getLogger(__name__)

    def _run_tmux_command(self, command):
        """
        Run a command in the DST dedicated server tmux session.

        Args:
            command (str): The command to run in the tmux session.

        Raises:
            subprocess.CalledProcessError: If the command execution fails.
            FileNotFoundError: If tmux is not installed or not found in PATH.
            Exception: For any other unexpected errors.
        """
        try:
            subprocess.run(
                ["tmux", "send-keys", "-t", "DST-dedicated", command, "Enter"],
                check=True,
            )
            self.logger.info(f"Ran command: {command}")
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Command '{command}' failed with return code {e.returncode}"
            )
        except FileNotFoundError:
            self.logger.error("tmux is not installed or not found in PATH.")
        except Exception as e:
            self.logger.error(f"Unexpected error running command '{command}': {e}")

    def send_console_message(self, message):
        """
        Send a message to the DST server console via tmux.

        Args:
            message (str): The message to send to the server console.
        """
        self._run_tmux_command(f'c_announce("{message}")')

    def kick_player(self, player_name):
        """
        Kick a player from the server using their name.

        Args:
            player_name (str): The name of the player to kick.
        """
        self._run_tmux_command(f'TheNet:Kick("{player_name}")')

    def send_listallplayers_command(self):
        """
        Send the c_listallplayers() command to the DST server via tmux.
        This command lists all players currently on the server.
        """
        self._run_tmux_command("c_listallplayers()")
