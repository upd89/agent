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
check_for('apt')
check_for('daemonize')
check_for('schedule')
check_for('configparser')

print("checks done.")
