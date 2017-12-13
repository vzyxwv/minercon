#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Python 2
from __future__ import print_function
try: input = raw_input
except NameError: pass


import os
import sys
import argparse
import getpass
import re

import mcrcon


parser = argparse.ArgumentParser(description='A simple Minecraft RCON clint using MCRcon')
parser.add_argument('-c', '--no-color', action='store_true',
                    help='Disable colored output') 
parser.add_argument('-q', '--quiet', action='store_true',
                    help='Disable all output except errors')
parser.add_argument('-s', '--use-tls', action='store_true',
                    help='Secure connection with TLS')
parser.add_argument('-i', '--insecure-tls', action='store_true',
                    help='Disable TLS certificate verification. This option implies --use-tls')
parser.add_argument('host', default='localhost', nargs='?',
                    help='Hostname or IP (Default: localhost)')
parser.add_argument('port', default=25575, type=int, nargs='?',
                    help='RCON port (Default: 25575)')
parser.add_argument('password', default=None, nargs='?',
                    help='RCON password. If none is supplied, you will be prompted to enter one')
parser.add_argument('command', metavar='command', default=None, nargs=argparse.REMAINDER,
                    help='The command to execute. If omitted, the client will run in interactive mode')


COLOR_CODES = {
    '0': '\033[0;30m', # 00 BLACK    0x30
    '1': '\033[0;34m', # 01 BLUE     0x31
    '2': '\033[0;32m', # 02 GREEN    0x32
    '3': '\033[0;36m', # 03 CYAN     0x33
    '4': '\033[0;31m', # 04 RED      0x34
    '5': '\033[0;35m', # 05 PURPLE   0x35
    '6': '\033[0;33m', # 06 GOLD     0x36
    '7': '\033[0;37m', # 07 GREY     0x37
    '8': '\033[1;30m', # 08 DGREY    0x38
    '9': '\033[1;34m', # 09 LBLUE    0x39
    'a': '\033[1;32m', # 10 LGREEN   0x61
    'b': '\033[1;36m', # 11 LCYAN    0x62
    'c': '\033[1;31m', # 12 LRED     0x63
    'd': '\033[1;35m', # 13 LPURPLE  0x64
    'e': '\033[1;33m', # 14 YELLOW   0x65
    'f': '\033[1;37m', # 15 WHITE    0x66
    'r': '\033[0m',    # Reset
}

# Windows ANSI control code support
import platform
if platform.system().lower() == 'windows':
    if sys.getwindowsversion().major >= 10:
        # Native Windows 10 support
        from ctypes import windll, c_int, byref
        stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
        mode = c_int(0)
        windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
        mode = c_int(mode.value | 4)
        windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)
    else:
        # Colorama for older versions
        from colorama import init
        init()


def exec_cmd(rcon, command):
    try:
        response = rcon.command(command)
    except Exception as e:
        print('Failed to execute command: %s' % e, file=sys.stderr)

    if response:
        print(format_response(response), file=sys.stdout)
    else:
        print('Server sent empty response', file=sys.stdout)


def cli(rcon):
    global PRINT_COLORS, QUIET_MODE

    # CLI prompt format
    if QUIET_MODE is True:
        prompt = ''
    elif PRINT_COLORS is True:
        prompt = '\033[1;32m>\033[0m '
    else:
        prompt = '> '
    
    print('\nConnected. Press Ctrl-C to disconnect\n', file=sys.stdout)

    # Input loop 
    try:
        while True:
            command = input(prompt)
            if command in ['q', 'quit', 'exit', 'dc', 'disconnect']:
                break

            response = rcon.command(command)
            if response:
                print(format_response(response), file=sys.stdout)
    except KeyboardInterrupt:
        pass

    print('\nDisconnected', file=sys.stdout)
    rcon.disconnect()


def format_response(response):
    global PRINT_COLORS, COLOR_CODES

    lines = response.splitlines()
    regex = re.compile(u'\u00A7([0-9a-f])', re.IGNORECASE)
    out = ''

    # Format each line of response individually
    for line in lines:
        if PRINT_COLORS is True:
            # Convert codes according to our dict
            line = regex.sub(lambda m: COLOR_CODES.get(m.group(1)), line) 
        else:
            # Just strip codes
            line = regex.sub('', line)

        # Throw a little indent on the line
        out += '  ' + line + '\n'

    if PRINT_COLORS is True:
        # Reset after printing the entire response
        out += '\033[0m'

    return out

if __name__ == '__main__':
    args = parser.parse_args()
    PRINT_COLORS = not args.no_color
    QUIET_MODE = args.quiet

    # Redirect stdout to /dev/null in quiet mode
    if args.quiet is True:
        sys.stdout = open(os.devnull, 'w')

    print(('Connecting to %s:%s...' % (args.host, args.port)), file=sys.stdout)

    if args.password is not None:
        password = args.password
    else:
        # Get password from environment variable; prompt as a last resort
        password = os.getenv('RCON_PASSWORD', getpass.getpass('RCON Password: '))

    if args.insecure_tls is True:
        args.use_tls = 2

    # Establish the connection
    CONN_TIMEOUT = 10
    rcon = mcrcon.MCRcon()
    try:
        rcon.connect(args.host, int(args.port), password, int(args.use_tls))
    except Exception as e:
        print('Unable to connect to server: %s' % e, file=sys.stderr)
        sys.exit(1)

    # Start interactive mode or run the specified command
    if not args.command:
        cli(rcon)
    else:
        exec_cmd(rcon, ' '.join(args.command))

    sys.exit(0)
