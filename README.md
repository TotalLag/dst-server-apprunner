# Don't Starve Together Server on Kubernetes with KubeVirt

This project provides a Python-based application for managing and monitoring a Don't Starve Together (DST) dedicated server, deployed on Kubernetes using KubeVirt for virtualization and Karpenter for managing spot instances.

## Features

- Real-time log monitoring and event handling
- Player management (join, leave, resume, spawn)
- Shared state management for consistent player information
- Modular event handler system
- Kubernetes deployment with KubeVirt for virtualization
- Karpenter for spot instance management
- Docker support for containerization
- Code linting and formatting with Flake8 and Black
- Static type checking with mypy
- Unit testing with Python's unittest framework
- Automatic server startup only after successful test execution
- Mod management system
- Live migration support through KubeVirt

## Setup and Configuration

1. Ensure you have the following tools installed:
   - Docker
   - kubectl
   - AWS CLI (configured with appropriate credentials)
2. Clone this repository to your local machine.
3. Configure your DST server settings in the `config/Cluster_1/` directory.
4. Set up your cluster token as a Kubernetes secret (this will be done automatically by the GitHub Actions workflow).

## Deployment

This project uses GitHub Actions for automated deployment to a Kubernetes cluster with KubeVirt. The workflow is defined in `.github/workflows/deploy.yml`.

To set up deployment:

1. Go to your GitHub repository's Settings > Secrets and variables > Actions.
2. Add the following secrets:
   - `CLUSTER_TOKEN`: Your Don't Starve Together cluster token
   - `AWS_ROLE_ARN`: The ARN of the IAM role to assume for AWS operations
   - `AWS_REGION`: Your AWS region
   - `EKS_CLUSTER_NAME`: Your EKS cluster name

The GitHub Actions workflow will:
- Build and push the Docker image to Amazon Elastic Container Registry (ECR)
- Apply the Kubernetes manifests
- Deploy KubeVirt to the cluster
- Create a VirtualMachine resource for the DST server
- Deploy the DST server as a VirtualMachine on your EKS cluster

### KubeVirt Deployment

This project uses KubeVirt to deploy the DST server as a virtual machine on Kubernetes. This allows for live migration between nodes without stopping the process or losing any memory state. The `deploy.yml` workflow file handles the deployment process, including:

1. Installing KubeVirt on the cluster
2. Creating a VirtualMachine resource with the DST server image
3. Deploying the VirtualMachine to the cluster

The VirtualMachine resource is configured to use the container image built from this project as the root disk, allowing for seamless updates and rollbacks.

## Using the Makefile

The project includes a Makefile with various commands to simplify development. Here are the available commands:

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

The project includes a mod management system. You can add, remove, and list mods using the Makefile commands:

- To add a mod: `make add-mod <mod_id>`
- To remove a mod: `make remove-mod <mod_id>`
- To list all mods: `make list-mods`

These commands will update the `dedicated_server_mods_setup.lua` and `modsettings.lua` files accordingly.

## Kubernetes and KubeVirt Configuration

The project uses the following Kubernetes resources:

- VirtualMachine: Manages the DST server as a virtual machine
- Service: Exposes the DST server ports
- ConfigMap: Stores configuration files
- PersistentVolumeClaim: Provides persistent storage for game data

The Kubernetes manifests are located in the `k8s/` directory:

- `deployment.yaml`: Defines the DST server deployment (now replaced by VirtualMachine)
- `service.yaml`: Exposes the DST server ports
- `configmap.yaml`: Contains configuration files for the DST server
- `persistent-volume-claim.yaml`: Defines the persistent storage for game data

## TODO List

The following items are planned improvements for this project:

- [ ] Implement backup of game state and restore to/from Amazon S3
- [x] Add support for mod management and updates
- [ ] Implement auto-scaling based on player count
- [ ] Add monitoring and alerting for server health
- [x] Implement KubeVirt deployment for live migration support

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
