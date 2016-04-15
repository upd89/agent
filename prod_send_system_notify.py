#!/usr/bin/env python

from lib.configloader import ConfigLoader
import lib.upstream
import lib.sysinfo
import lib.pkg

_config = ConfigLoader("config")

sys = lib.sysinfo.get_notify_system()
sys = lib.pkg.addUpdates(sys)

print("Sending to server (notify " + lib.sysinfo.get_hostname() + ")...")
response = lib.upstream.pushSystemNotify(_config, lib.sysinfo.get_urn(), sys)
print("Response:\n" + response)
