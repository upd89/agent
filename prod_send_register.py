#!/usr/bin/env python

from lib.configloader.configloader import ConfigLoader
import lib.upstream
import lib.sysinfo

_config = ConfigLoader("config")

sys = lib.sysinfo.get_register_system()

print("Sending to server (register " + lib.sysinfo.get_hostname() + ")...")
response = lib.upstream.pushRegister(_config, sys)
print("Response:\n" + response)
