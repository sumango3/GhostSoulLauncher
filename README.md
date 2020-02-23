# GhostSoulLauncher

Simple Korea Ghost Soul Launcher

## How it works?

This script emulates login logic at [Ghost Soul homepage](http://hon.mgame.com/), and executes `MStartPro.exe` with proper arguments.

## How to use

### Before running program

Check if you can find your `MStartPro.exe` at `C:\MGAME\Common\`

If you can't, you cannot use windows binary (because it assumes that launcher is at the path)

### How to run Python Script

Install dependencies
    - Python 3
    - requests
    - pycryptodome

Execute [launcher.py](/launcher.py), and type your ID & PW for GhostSoul (credentials for http://hon.mgame.com/)

### How to run Windows Binary

Execute [launcher.exe](/dist/launcher.exe), and type your ID & PW for GhostSoul (credentials for http://hon.mgame.com/)

## TODO
Adding GUI, or implementing in other programming languages
