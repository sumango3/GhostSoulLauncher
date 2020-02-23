# GhostSoulLauncher
Execute MStartPro.exe with proper arguments, by imitating login form at homepage

## Usage

1. Place `launcher.py` at the same folder as MStartPro.exe (Default: `C:\MGAME\Common`)

2. Execute `launcher.py` on cmd, and type your ID and PW for GhostSoul (credentials for http://hon.mgame.com/)
    - You should run through CMD

## Dependency
```
Python3
requests
pycryptodome
```

## TODO
Make launcher runnable by executing script at once, by replacing `os.system` with `subprocess` module
