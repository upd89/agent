#!/usr/bin/env python

from lib.configloader import ConfigLoader
import lib.upstream
import lib.sysinfo
import lib.pkg

_config = ConfigLoader("config")

packages = lib.pkg.getPackageList()

print("Sending to server (updateInstalled " +
      lib.sysinfo.get_hostname() + ")...")
response = lib.upstream.pushSystemUpdateInstalled(_config,
                                                  lib.sysinfo.get_urn(),
                                                  packages)
print("Response:\n" + response)
