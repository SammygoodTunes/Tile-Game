# Tile-Game

A tile-based game with procedural terrain generation (using the Perlin Noise algorithm).

Currently in-development.

## Preview

![Preview](https://raw.githubusercontent.com/SammygoodTunes/Tile-Game/main/docs/ss.png)

## Controls

- [**ZQSD**] -> Move player (temporary)
- [**LMB**] -> Break cobblestone tiles
- [**Escape**] -> Pause menu
- [**Alt+Enter**] -> Fullscreen mode

## Setup

> Before installing the necessary modules, it is recommended to set up a virtual environment. This allows for a clean workspace and avoids installing packages to your actual environment.

Set up a new virtual environment. For the sake of conventions, we'll call ours `venv`:

```shell
python -m venv venv   # Windows
python3 -m venv venv  # MacOS / Unix	
```

Activate it:

```shell
venv\Scripts\activate     # Windows
source venv/bin/activate  # MacOS / Unix
```

Install the pre-requisites from the requirements file (root dir) using:

```shell
pip install -r requirements.txt
```

## Information

Developed by [SammygoodTunes](https://github.com/SammygoodTunes)

Tested on Debian 12 and Windows 10

Libraries used: Pygame 2.5.2, Crayons 0.4.0, Numpy 1.26.4
