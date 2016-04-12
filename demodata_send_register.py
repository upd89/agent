#!/usr/bin/env python

from random import randint

from lib.configloader.configloader import ConfigLoader
from classes.system_register import System
import lib.upstream

_config = ConfigLoader("config")
url = lib.upstream.getRegisterURL(_config)

# Demodata
hostname = "vm" + str(randint(11,999))
sys = System(hostname, "virt-" + hostname + "-nine", "Ubuntu 15.10", "127.0.0.1", "")

print("Sending to server (register " + hostname + ")...")
response = lib.upstream.push(url, sys)
print("Response:\n" + response)

