MineRCON
========

A simple RCON client for Minecraft

![image](https://i.imgur.com/ieOjAfr.png)


Features
--------

### Current:
* Interactive or one-shot execution
* Multi-platform Bukkit/Spigot color code support
* TLS support (tested with [stunnel](https://www.stunnel.org>))
* Compatible with Python 2.6+ and 3.x
* Runs on CentOS 7, Windows 10, and others

### Planned:
* Configurable timeout w/ watchdog functionality
* IPv6 support
* Anything cool that comes in via. well-formed Pull Request


Installation
------------

MineRCON requires [Python 2.6+ or 3.x](https://www.python.org/downloads/>) to be installed on your system to work. After installing Python into your PATH, download and extract (or `git clone`) MineRCON into a directory of your choosing. Then, you can install MineRCON system-wide like so:

```
cd minercon
python setup.py install
```

If the script completes without errors, you are ready to start using MineRCON!

---

Alternatively, you can install MineRCON directly from GitHub by running `pip install git+https://github.com/CraftySpaz/minercon.git --process-dependency-links`, or simply by saving [minercon.py](https://raw.githubusercontent.com/CraftySpaz/minercon/master/minercon.py>) and [mcrcon.py](https://raw.githubusercontent.com/CraftySpaz/MCRcon/master/mcrcon.py>) into a directory together.


Usage
-----

`minercon.py [flags] [host] [port] [password] [command]`

### flags:
```
  -c, --no-color      Disable colored output
  -q, --quiet         Disable all output except errors
  -s, --use-tls       Secure connection with TLS
  -i, --insecure-tls  Disable TLS certificate verification. This option
                      implies --use-tls
```

### args:
```
  host                Hostname or IP (Default: localhost)
  port                RCON port (Default: 25575)
  password            RCON password. If none is supplied, you will be prompted
                      to enter one
  command             The command to execute. If omitted, the client will run
                      in interactive mode
```


Resources
---------

* [MineRCON on GitHub](https://github.com/CraftySpaz)
* [MCRcon by @barneygale](https://github.com/barneygale/MCRcon)
* [RCON documentation for Minecraft](http://wiki.vg/RCON)
