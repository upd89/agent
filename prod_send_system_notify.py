#!/usr/bin/env python

from lib.configloader.configloader import ConfigLoader
import lib.upstream
import lib.sysinfo
import lib.apt

_config = ConfigLoader("config")

sys = lib.sysinfo.get_notify_system()
sys = lib.apt.addUpdates(sys)

print("Sending to server (notify " + lib.sysinfo.get_hostname() + ")...")
response = lib.upstream.pushSystemNotify(_config, lib.sysinfo.get_urn(), sys)
print("Response:\n" + response)
