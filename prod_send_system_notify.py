#!/usr/bin/env python

from lib.configloader.configloader import ConfigLoader
from classes.update import Update
from classes.system_notify import System
import lib.upstream
import lib.sysinfo
import lib.apt

_config = ConfigLoader("config")

# Data
myHostname  = lib.sysinfo.get_hostname()
myURN       = lib.sysinfo.get_urn()
myDistro    = lib.sysinfo.get_distro()
myIP        = lib.sysinfo.get_ip()
needReboot  = lib.sysinfo.get_reboot_required()
sys = System(name=myHostname, urn=myURN, os=myDistro, address=myIP, reboot_required=needReboot)

url = lib.upstream.getSystemNotifyURL(_config, myURN)

sys = lib.apt.addUpdates(sys)

print("Sending to server (notify " + myHostname + ")...")
response = lib.upstream.push(url, sys)
print("Response:\n" + response)

