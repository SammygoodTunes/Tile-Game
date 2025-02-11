# Tile-Game

[![Readthedocs.io](https://img.shields.io/badge/repo-readthedocs.io-blue.svg?logo=readthedocs&logoColor=white&label=docs)](https://tile-game.readthedocs.io)
[![License: MIT](https://img.shields.io/github/license/SammygoodTunes/Tile-Game.svg)](https://opensource.org/license/mit)
[![](https://img.shields.io/github/v/release/SammygoodTunes/Tile-Game?include_prereleases&label=pre-release&logo=github)](https://github.com/SammygoodTunes/Tile-Game/releases/tag/alpha)
[![GitHub last commit](https://img.shields.io/github/last-commit/SammygoodTunes/Tile-Game?logo=git&logoColor=white)](https://github.com/SammygoodTunes/Tile-Game/commits/main)
<!-- 
Uncomment when officially released:
![GitHub Release](https://img.shields.io/github/v/release/SammygoodTunes/Tile-Game) 
-->

A tile-based multiplayer game with procedural terrain generation (using the Perlin Noise algorithm).

Currently in development.

Pre-release **v0.0.1a** is now **[available](https://github.com/SammygoodTunes/Tile-Game/releases/tag/alpha)**.

## Contents:
- [Preview](#preview)
- [Controls](#controls)
- [Setup](#setup)
  - [Debug mode](#debug-mode)
- [Documentation](#documentation)
- [Information](#information)
  - [Project](#project)
  - [Contributors](#contributors-a-z)
  - [Credits](#credits)
  - [Compatibility](#compatibility)
  - [Dependencies](#dependencies)

## Preview

![Preview](https://raw.githubusercontent.com/SammygoodTunes/Tile-Game/main/docs/ss.png)

## Controls

| Key(s)                            | Action                  |
|-----------------------------------|-------------------------|
| <kbd>Z/Q/S/D</kbd>                | Move player (temporary) |
| LMB                               | Break breakable tiles   |
| Mouse Wheel                       | Switch item in hotbar   |
| <kbd>Space</kbd>                  | Show map                |
| <kbd>Esc</kbd>                    | Pause menu/Main menu    |
| <kbd>Alt</kbd> + <kbd>Enter</kbd> | Fullscreen mode         |

## Setup

> **<ins>Requires:</ins>** Python 3.11 or later
> 
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

In order to install the necessary modules, Poetry is recommended but not required. You can install it using the following:

```bash
pip install poetry
```

Install the pre-requisites:

```bash
poetry install
```

> If you prefer not to install the development dependencies, then feel free to use the ```--only main``` flag.
> 
> If you prefer not to use `poetry`, then you may manually install the dependencies listed [here](#dependencies) with pip.


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

## Documentation

The official documentation of this repository is hosted on Readthedocs.

You may find it [here](https://tile-game.readthedocs.io/en/latest/).

Other versions in different languages may exist in the future, but for now it is only in English.

The `tools/gen_docs` tool must be run in order generate relevant doc files before pushing to the repository.

## Information

### Project

Current pre-release: [v0.0.1a](https://github.com/SammygoodTunes/Tile-Game/releases/tag/alpha)

### Contributors [A-Z]: 
- [Jatzylap](https://github.com/Jatzylap) (art, alpha-testing)
- [o.nihilist](https://github.com/onihilist) (programming, translation)
- Pickmonde (art)
- [SammygoodTunes](https://github.com/SammygoodTunes) (art, programming)

### Credits:
- Original ["Pixeled"](https://www.dafont.com/pixeled.font) typeface by OmegaPC777 
  - Edited to support more characters

### Compatibility

This project was tested on the following operating systems:
- Debian 12
- Windows 10

If you are using an operating system/distribution that isn't listed above, 
then the game may or may not work as intended.

### Dependencies

| Name        | Version | Required? |
|-------------|---------|-----------|
| Pygame-CE   | ^2.5.1  | Yes       |
| Python-i18n | ^0.3.9  | Yes       |
| PyYAML      | ^6.0.2  | Yes       |
| PyTest      | ^8.3.3  | No        |


> [Go back to the top](#tile-game)
