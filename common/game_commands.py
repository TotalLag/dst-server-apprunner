import subprocess
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


class GameCommandExecutor:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def _run_tmux_command(self, command):
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
        """Send a message to the DST server via tmux."""
        self._run_tmux_command(f'c_announce("{message}")')

    def kick_player(self, player_name):
        """Kick a player from the server using their name."""
        self._run_tmux_command(f'TheNet:Kick("{player_name}")')

    def send_listallplayers_command(self):
        """Send the c_listallplayers() command to the DST server via tmux."""
        self._run_tmux_command("c_listallplayers()")
