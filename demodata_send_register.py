#!/usr/bin/env python

import os,sys,time,json,urllib2
from random import randint

from classes.system_register import System
from classes.encoder import MyEncoder

#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/register'

hostname = "vm" + str(randint(11,999))
sys = System(hostname, "virt-" + hostname + "-nine", "Ubuntu 15.10", "127.0.0.1", "")

print("Sending to server (register " + hostname + ")...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(sys, cls=MyEncoder))
print("Response:")
print(response.read())

