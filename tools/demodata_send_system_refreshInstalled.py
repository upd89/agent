#!/usr/bin/env python

import syspath
from upd89.lib.configloader import ConfigLoader
import demodata
import upd89.lib.upstream

_config = ConfigLoader("../config")

# Demodata
hostname = demodata.hostname
packages = demodata.packages

print("Sending to server (refreshInstalled " + hostname + ")...")
response = upd89.lib.upstream.pushSystemRefreshInstalled(_config, hostname, packages)
print("Response:\n" + response)
