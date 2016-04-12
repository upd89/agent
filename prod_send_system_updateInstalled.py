#!/usr/bin/env python

from lib.configloader.configloader import ConfigLoader
import lib.upstream
import lib.sysinfo
import lib.apt

_config = ConfigLoader("config")

# Data
myHostname  = lib.sysinfo.get_hostname()
myURN       = lib.sysinfo.get_urn()

url = lib.upstream.getSystemUpdateInstalledURL(_config, myURN)

packages = lib.apt.getPackageList()

print("Sending to server (updateInstalled " + myHostname + ")...")
response = lib.upstream.push(url, packages)
print("Response:\n" + response)

