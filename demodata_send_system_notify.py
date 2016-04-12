#!/usr/bin/env python

from lib.configloader.configloader import ConfigLoader
from classes.update import Update
from classes.system_notify import System
import lib.upstream

_config = ConfigLoader("config")

# Demodata
hostname = 'vm1'
sys = System(hostname, hostname, "Ubuntu 15.10", "127.0.0.1", True)
sys.addUpdate(Update(name="vim", version="demoupdate", arch="amd64", repository="demorepo", baseversion="2:7.4.712-2ubuntu4"))
sys.addUpdate(Update(name="dnsutils", version="demoupdate", arch="amd64", repository="demorepo", baseversion="1:9.9.5.dfsg-11ubuntu1"))

url = lib.upstream.getSystemNotifyURL(_config, hostname)

print("Sending to server (notify " + hostname + ")...")
response = lib.upstream.push(url, sys)
print("Response:\n" + response)

