# Don't Starve Together Server AppRunner

This project provides a Python-based application for managing and monitoring a Don't Starve Together (DST) dedicated server. It offers real-time log monitoring, event handling, player management capabilities, and mod management.

## Features

- Real-time log monitoring and event handling
- Player management (join, leave, resume, spawn)
- Shared state management for consistent player information
- Modular event handler system
- Docker support for easy deployment
- Code linting and formatting with Flake8 and Black
- Static type checking with mypy
- Unit testing with Python's unittest framework
- Automatic server startup only after successful test execution
- Mod management system

## Setup and Configuration

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone this repository to your local machine.
3. Configure your DST server settings in the `config/Cluster_1/` directory.
4. Set up your cluster token:
   - For local testing, create a `.env` file in the project root with the following content:
     ```
     CLUSTER_TOKEN="your_cluster_token_here"
     ```
   - Replace `your_cluster_token_here` with your actual Don't Starve Together cluster token.

## Using the Makefile

The project includes a Makefile with various commands to simplify development and deployment. Here are the available commands:

```bash
# Build Docker images
make build

# Run tests in Docker
make test

# Run linter (flake8) in Docker
make lint

# Run formatter (black) in Docker
make format

# Run static type checker (mypy) in Docker
make typecheck

# Run tests and start server if tests pass
make run

# Clean up Docker resources
make clean

# Run all checks (linting, type checking, and tests)
make check

# Add a mod to the dedicated_server_mods_setup.lua file
make add-mod <mod_id>

# Remove a mod from the dedicated_server_mods_setup.lua file
make remove-mod <mod_id>

# List all mods in the dedicated_server_mods_setup.lua file
make list-mods
```

## Mod Management

The project now includes a mod management system. You can add, remove, and list mods using the Makefile commands:

- To add a mod: `make add-mod <mod_id>`
- To remove a mod: `make remove-mod <mod_id>`
- To list all mods: `make list-mods`

These commands will update the `dedicated_server_mods_setup.lua` and `modsettings.lua` file accordingly.

## GitHub Actions Deployment

To deploy using GitHub Actions:

1. Go to your GitHub repository's Settings > Secrets and variables > Actions.
2. Add a new repository secret named `CLUSTER_TOKEN` with your Don't Starve Together cluster token as the value.

## AWS App Runner Considerations

This project is configured to be compatible with AWS App Runner. However, there are some important considerations:

1. Persistent Storage: AWS App Runner does not support persistent volumes. As a result, game state will be lost when the container restarts or is replaced.

2. Data Backup: To mitigate the lack of persistent storage, consider implementing a backup solution that periodically saves game state to an external service like Amazon S3.

## TODO List

The following items are planned improvements for this project:

- [ ] Implement backup of game state and restore to/from Amazon S3
- [x] Add support for mod management and updates

## Key Components

### Common

- `shared_state.py`: Manages shared state across the application, including player information.
- `player_utils.py`: Utilities for extracting player information from log lines, including join, leave, resume, and spawn events.
- `event_registry.py`: Handles event registration and dispatching.
- `game_commands.py`: Interfaces with DST server commands.
- `mod_manager.py`: Manages mods for the DST server.
- `fetch_mod_info.py`: Fetches information about mods from the Steam Workshop.

### Handlers

- `example_unpause_event_handler.py`: An example handler demonstrating how to create custom event handlers.
- `player_join_handler.py`: Manages player join, leave, resume, and spawn events.
- `player_list_handler.py`: Handles player listing operations.
- `save_event_handler.py`: Manages save events.
- `shard_server_handler.py`: Handles shard-related events.

### Tests

- `test_player_utils.py`: Unit tests for player utilities, including join, leave, resume, and spawn event parsing.
- `test_shared_state.py`: Unit tests for shared state management.
- `test_grouped_event_handler.py`: Unit tests for grouped event handling.
- `test_save_event_handler.py`: Unit tests for save event handling.
- `test_shard_server_handler.py`: Unit tests for shard server handling.

## Development

### Creating Custom Event Handlers

To create a new event handler:

1. Create a new Python file in the `handlers/` directory (e.g., `my_custom_handler.py`).
2. Define a function that takes a log line as an argument.
3. Implement your logic to handle specific events.
4. Register your handler in the main `log_monitor.py` file.

Example (based on `example_unpause_event_handler.py`):

```python
def handle_unpause_event(log_line):
    if "Unpaused the server" in log_line:
        print("Server has been unpaused!")
        # Add your custom logic here
```

### Running Tests and Checks

To run the unit tests:

```bash
make test
```

To run all checks (linting, type checking, and tests):

```bash
make check
```

### Code Style

This project uses Flake8 for linting and Black for formatting. To maintain code quality:

1. Run Flake8:
   ```bash
   make lint
   ```

2. Format code with Black:
   ```bash
   make format
   ```

3. Run static type checking with mypy:
   ```bash
   make typecheck
   ```

## Contributing

Contributions are welcome! Please ensure your code passes all tests and adheres to the project's code style before submitting a pull request. Use the `make check` command to run all checks before submitting your contribution.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
