#!/usr/bin/env python

import os,sys,time,json,urllib2
from random import randint
from json import JSONEncoder

from classes.update import Update
from classes.system_notify import System
from classes.encoder import MyEncoder

# Demodata
urn = 'vm1'
sys = System(urn, urn, "Ubuntu 15.10", "127.0.0.1", True)
sys.addUpdate(Update(name="vim", version="demoupdate", arch="amd64", repository="demorepo", baseversion="2:7.4.712-2ubuntu4"))
sys.addUpdate(Update(name="dnsutils", version="demoupdate", arch="amd64", repository="demorepo", baseversion="1:9.9.5.dfsg-11ubuntu1"))

#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/system/' + urn + '/notify'

print("Sending to server (notify system " + urn + ")...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(sys, cls=MyEncoder))
print("Response:")
print(response.read())

