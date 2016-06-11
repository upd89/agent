#!/usr/bin/env python

import sys

import syspath
from random import randint
from upd89.lib.configloader import ConfigLoader
import demodata
import upd89.lib.upstream

_config = ConfigLoader("../config")

if '-h' in sys.argv:
    print("\n '--random' generates random hostname\n")
    sys.exit()

# Demodata
reg_sys = demodata.register_sys

if '--random' in sys.argv:
    hostname = "demo-vm" + str(randint(11, 999))
    reg_sys.urn = hostname
    reg_sys.name = hostname


print("Sending to server (register " + reg_sys.name + ")...")
response = upd89.lib.upstream.pushRegister(_config, reg_sys)
print("Response:\n" + response)
