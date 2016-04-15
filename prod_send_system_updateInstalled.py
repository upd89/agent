#!/usr/bin/env python

from lib.configloader.configloader import ConfigLoader
import lib.upstream
import lib.sysinfo
import lib.apt

_config = ConfigLoader("config")

packages = lib.apt.getPackageList()

print("Sending to server (updateInstalled " +
      lib.sysinfo.get_hostname() + ")...")
response = lib.upstream.pushSystemUpdateInstalled(_config,
                                                  lib.sysinfo.get_urn(),
                                                  packages)
print("Response:\n" + response)
