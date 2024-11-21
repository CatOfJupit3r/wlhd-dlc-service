# Walenholde Combat System — DLC Service

This repository contains code for DLC service, which is supposed to be run in Docker compose files

Only supports GitHub links. Any other will be rejected.

Currently, this service does not offer hot reload for both Python Engine and TypeScript Backends. 

## Description

This is a passion project, created to provide a platform for playing Walenholde Combat System.

WLHD is a tabletop RPG system, created by me, that is still in active development. For more detailed information, check [Learn More](#Learn-More).

## Prerequisites (LAUNCH)

Before you begin, ensure you have met the following requirements:

-   You have installed [Docker](https://nodejs.org/en/download/) (built using NodeJS v21.6.1).

## Prerequisites (DEVELOPMENT)

Before you begin, ensure you have met the following requirements:

- You have installed [Python](https://www.python.org/downloads/) (recommended 3.11.4).

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/CatOfJupit3r/wlhd-dlc-service
    ```

2. Install dependencies:

    ```bash
    pip install .
    ```

3. Create a `.env` file in the root directory of the project and populate it with the variables from `.env.example`.

## Environment Variables

- `SOURCES_TO_INSTALL` — "List" of sources to install from environment variables. In the format of `source1,source2,source3`.
- `GITHUB_USERNAME` — GitHub username. Used for cloning repositories.
- `GITHUB_TOKEN` — GitHub token. Used for cloning repositories. Make sure it is both valid and has access to the repositories you want to clone.
- `DLC_MOVEMENT_STRATEGY` — Strategy for moving DLCs. Either `dockerfile` or `local`. More details in settings.py
- `IGNORE_LOCAL_STRATEGY_CONFIRMATION` — If set to `True` AND strategy is `local`, will not ask for confirmation. Use with caution.

## Usage

### Local

Open a terminal inside the project directory run according to your package manager:

```bash
npm run start
# or
yarn start
# or
pnpm start
# or
bun start
```

## Learn More

To learn more about Walenholde Combat System... Well, you can't, as it's still a WIP. But in future you will be able to find more information about it on GitHub Wiki page, including:

-   Creating your own lobbies, characters and hosting them.
-   Mechanics of the game, including combat, spells, and other features.

## Related

-   [React Frontend](https://github.com/CatOfJupit3r/wlhd-frontend-web) — Frontend for the game coordinator, built using React, Redux and GraphQL. (You are here!)
-   [Game Coordinator](https://github.com/CatOfJupit3r/wlhd-coordinator-server) — Backend for the game coordinator, built using ExpressJS and MongoDB.
-   [Game Engine](https://youtu.be/h81WXIfCnoE?si=LS7HpLYhI-LBg4-9) — Core game engine, built using Python, Python and Python. (also, FastAPI).
-   [Building your own WLHD Package](https://github.com/CatOfJupit3r/wlhd-example-package) — Guide on how to build your own WLHD package, including all the necessary information.
-   [Discord Bot Interface](https://github.com/CatOfJupit3r/wlhd-frontend-discord) — Frontend for the game coordinator, built using Discord API. (Deprecated)
-   [Game Guide] — Contains all the necessary information about the game and its various mechanics in a traditional TTRPG format. (WIP)
-   [Game Wiki] — Contains all the necessary information about the game and its various mechanics in easily navigable way. (WIP)
