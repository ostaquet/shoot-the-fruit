# Shoot the fruit!

Simple game written in Pygame to teach basics of Python and Pygame to beginners.

## Rules of the game

Apples appear on the screen and you have 30 seconds to shoot a maximum of apples by clicking with the mouse.

<img src="docs/demo_animation.gif" width="640"/>

## How to build and run?

 - Install Python 3.7+ on your computer.
 - Download the source code of Shoot the fruit!
 - Install required library with `pip install -r requirements.txt`
 - Run the game with `python main.py`

## How to create the package?

 - Install `pyinstaller` with `pip install pyinstaller`
 - Run `pyinstaller main.py`
 - Copy the `assets` directory into the new `dist` directory with `cp -Rf assets dist/`
 - The package is ready to share from the directory `dist`
 - You can play by starting the executable `Launcher`
