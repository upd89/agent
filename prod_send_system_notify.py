#!/usr/bin/env python

import os,sys,time,apt,json,socket,platform

from lib.configloader.configloader import ConfigLoader
from classes.update import Update
from classes.system_notify import System
import lib.upstream
import lib.sysinfo

_config = ConfigLoader("config")

# Data
myHostname = socket.gethostname()
myURN = 'demo-' + myHostname + '-demo'
myDistro = ' '.join(platform.linux_distribution())
myIP = lib.sysinfo.get_ip()
needReboot = os.path.isfile("/var/run/reboot-required")
sys = System(name=myHostname, urn=myURN, os=myDistro, address=myIP, reboot_required=needReboot)

url = lib.upstream.getSystemNotifyURL(_config, myURN)

print("Reading local cache...")
cache = apt.Cache()

print("Reading Upgradable Packages...")
for pkg in cache:
   if (pkg.is_upgradable):
      #print(pkg.name)
      pkg_base = pkg.versions[-1]
      pkg_origin = pkg.versions[0].origins[0]
      repo_string = pkg_origin.origin + "_" + pkg_origin.archive + "_" + pkg_origin.component
      sys.addUpdate(Update(
           name        = pkg.name,
           version     = pkg.candidate.version,
           arch        = pkg.architecture(),
           repository  = repo_string,
           baseversion = pkg_base.version
      ))

print("Sending to server (notify " + myHostname + ")...")
response = lib.upstream.push(url, sys)
print("Response:\n" + response)

