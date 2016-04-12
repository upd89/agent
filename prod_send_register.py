#!/usr/bin/env python

import os,sys,time,apt,socket,platform

from lib.configloader.configloader import ConfigLoader
from classes.system_register import System
import lib.upstream
import lib.sysinfo

_config = ConfigLoader("config")
url = lib.upstream.getRegisterURL(_config)

# Data
myHostname = socket.gethostname()
myURN = 'demo-' + myHostname + '-demo'
myDistro = ' '.join(platform.linux_distribution())
myIP = lib.sysinfo.get_ip()
sys = System(name=myHostname, urn=myURN, os=myDistro, address=myIP, tag="")

print("Sending to server (register " + myHostname + ")...")
response = lib.upstream.push(url, sys)
print("Response:\n" + response)

