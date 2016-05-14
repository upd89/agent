#!/usr/bin/env python

# import syspath
from lib.configloader import ConfigLoader
import demodata
import lib.upstream

_config = ConfigLoader("config")

# Demodata
hostname = demodata.hostname
packages = demodata.packages

print("Sending to server (refreshInstalled " + hostname + ")...")
response = lib.upstream.pushSystemRefreshInstalled(_config, hostname, packages)
print("Response:\n" + response)
