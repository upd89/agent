#!/usr/bin/env python

import imp


def check_for(module):
    try:
        imp.find_module(module)
    except ImportError:
        print(module + " not installed")

check_for('os')
check_for('platform')
check_for('socket')
check_for('json')
check_for('urllib2')
check_for('apt')                # sudo apt install python-apt
check_for('daemonize')          # sudo apt install python-daemonize
check_for('schedule')           # sudo pip install schedule
check_for('configparser')       # sudo apt install python-configparser

print("checks done.")
