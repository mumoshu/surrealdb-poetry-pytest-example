# SurrealDB Python Example with Dev Containers

This project provides a starting point for developing Python applications using the SurrealDB Python SDK within a VS Code Dev Container environment.

## Features

*   **Python 3:** Configured using the standard dev container image.
*   **Poetry:** For dependency management and packaging.
*   **Pytest:** For writing tests and DB connection fixtures.
*   **SurrealDB:** Includes a SurrealDB container for local development and testing.
*   **VS Code Integration:** Pre-configured with useful Python extensions (Pylance, Ruff, Black, Pytest) and Dev Container settings.
*   **Dev Container Feature for installing SurrealDB CLI:** Includes a local [Dev Container Feature](https://containers.dev/implementors/features/) for installing the SurrealDB CLI into the dev container.

## Getting Started

1.  **Prerequisites:**
    *   Docker Desktop installed and running.
    *   VS Code with the "Dev Containers" extension installed.
2.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```
3.  **Open in Dev Container:**
    *   Open the project folder in VS Code.
    *   Click the green "><" icon in the bottom-left corner of VS Code.
    *   Select "Reopen in Container" from the command palette.
4.  **Wait for the container to build:** This might take a few minutes the first time.
    *   The `postCreateCommand` in `devcontainer.json` will automatically install Poetry and project dependencies (including `surrealdb`).
5.  **Start Developing:**
    *   The SurrealDB instance will be available at `ws://surrealdb:8000` from within the `app` container.
    *   The default credentials (set in `docker-compose.yml`) are user `root` and password `root`.
    *   You can open a terminal in VS Code (Terminal > New Terminal) to run commands inside the container (e.g., `poetry run python your_script.py`, `poetry run pytest`).

## Connecting to SurrealDB

Inside the `app` container, you can connect to SurrealDB using its container name (`surrealdb`) as the host.

Run either the `surreal sql` command or the example Python script to start your experiments!

Command:

```shell
surreal sql -e ws://surrealdb:8000 -u root -p root
```

Script:

```shell
poetry run python main.py
```

## Customization

*   **Python Version:** Change the `VARIANT` build argument in `.devcontainer/docker-compose.yml` and `.devcontainer/Dockerfile`.
*   **SurrealDB Configuration:** Modify the `command` for the `surrealdb` service in `.devcontainer/docker-compose.yml` to change startup options (e.g., persistent storage).
*   **VS Code Extensions:** Add or remove extension IDs in `.devcontainer/devcontainer.json`.
*   **OS Packages:** Uncomment and modify the `apt-get` command in `.devcontainer/Dockerfile` to install additional Debian packages.
