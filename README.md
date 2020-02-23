# GhostSoulLauncher
Execute MStartPro.exe with proper arguments, by emulating login at homepage

## Usage

1. Install dependencies

2. Check if you can find your Ghost Soul Launcher `MStartPro.exe` at `C:\MGAME\Common\`

    - If you installed the launcher at another place, you should put your path at 14th line of `launcher.py`. `MStartProPath = 'C:\MGAME\Common\MStartPro.exe'`

3. Execute `launcher.py`, and type your ID and PW for GhostSoul (credentials for http://hon.mgame.com/)

## Dependency
```
Python3
requests
pycryptodome
```

## TODO
Make launcher runnable by executing script at once, by replacing `os.system` with `subprocess` module
