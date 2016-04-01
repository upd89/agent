#!/usr/bin/env python

import os,sys,time,apt,json,socket,platform
import urllib2
from random import randint

import tools
from classes.system_register import System
from classes.encoder import MyEncoder

myHostname = socket.gethostname()
myURN = 'demo-' + myHostname + '-demo'
myDistro = ' '.join(platform.linux_distribution())
myIP = tools.get_ip()

#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/register'

sys = System(name=myHostname, urn=myURN, os=myDistro, address=myIP, tag="")

print("Sending to server (register " + myHostname + ")...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(sys, cls=MyEncoder))
print("Response:")
print(response.read())

