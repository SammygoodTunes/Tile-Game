# Tile-Game

A tile-based multiplayer game with procedural terrain generation (using the Perlin Noise algorithm).

Currently in development.

Pre-release **v0.0.1a** is now **[available](https://github.com/SammygoodTunes/Tile-Game/releases/tag/alpha)**.

## Preview

![Preview](https://raw.githubusercontent.com/SammygoodTunes/Tile-Game/main/docs/ss.png)

## Controls

- [**ZQSD**] -> Move player (temporary)
- [**LMB**] -> Break cobblestone tiles
- [**Mouse Wheel**] -> Switch item in hotbar
- [**Space Bar**] -> Show map
- [**Escape**] -> Pause menu
- [**Alt+Enter**] -> Fullscreen mode

## Setup

> Before installing the necessary modules, it is recommended to set up a virtual environment. This allows for a clean workspace and avoids installing packages to your global environment.

Set up a new virtual environment. For the sake of conventions, we'll call ours `venv`:

```bash
python -m venv venv   # Windows
python3 -m venv venv  # MacOS / Unix	
```

Activate it using:

```bash
venv\Scripts\activate     # Windows
source venv/bin/activate  # MacOS / Unix
```

Install the pre-requisites:

```bash
pip install -e .
```

Run the game using:

```bash
python -m game  # Windows
python3 -m game # MacOS / Unix
```

### Debug mode

If you wish to launch the game with extra debugging information, use the `--debug` or `-d` flag:

```bash
python -m game --debug   # Windows
python3 -m game --debug  # MacOS / Unix
```

> Note that using this mode will significantly impact the performance of the game, and therefore should not be used when playing normally.

## Information

Current Game Version: [v0.0.1a](https://github.com/SammygoodTunes/Tile-Game/releases/tag/alpha)


Developed by [SammygoodTunes](https://github.com/SammygoodTunes)

Tested on Debian 12 and Windows 10

Libraries used: Pygame 2.5.2, Crayons 0.4.0
